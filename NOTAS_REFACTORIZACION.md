# Notas de Refactorización — EnvíaYa (Cálculo de costos de envío)

Documento de auditoría técnica del módulo heredado `envios.py` (etiqueta `v1.0.0`).
Identifica los **malos olores (code smells)**, su impacto como **deuda técnica** y la
estrategia de mantenimiento aplicada en las ramas de corrección y refactorización.

## 1. Malos olores detectados (Code Smells)

| # | Mal olor (nombre técnico) | Ubicación en `envios.py` | Deuda técnica que genera |
|---|---------------------------|--------------------------|--------------------------|
| 1 | **Magic Numbers** | líneas 16, 18, 20, 29, 34, 36 | Literales sin nombre (`6000`, `9000`, `800`, `0.05`, `0.10`, `5000`) dispersos por la lógica. Si cambia una tarifa o un porcentaje hay que buscar/editar a ciegas: alto riesgo de inconsistencia y errores de mantenimiento. |
| 2 | **Long Method / God Function** | líneas 12–39 | `calc` concentra validación, cálculo de tramos, recargos de zona, recargo de fin de semana, descuentos, piso mínimo, impresión y redondeo. Difícil de leer, probar de forma aislada y modificar sin efectos colaterales. |
| 3 | **Flag Argument** | líneas 12, 37–38 | El parámetro `flag` mezcla el cálculo con la salida por consola, violando el **Principio de Responsabilidad Única (SRP)**. Acopla la lógica de negocio a la presentación y ensucia la firma pública. |
| 4 | **Undefined Variable / Bug** | línea 32 | Se usa el nombre global `DESC_VIP` en lugar de `CONFIG["DESC_VIP"]`. Provoca `NameError` en la rama VIP: es un defecto latente en producción. |
| 5 | **Missing Input Validation** | líneas 21–28 | No hay validación explícita de zona inválida ni de día fuera del rango 1..7. Entradas mal formadas se procesan silenciosamente y producen resultados incorrectos (fallo de robustez y seguridad de negocio). |
| 6 | **Incorrect Truncation Logic** | línea 39 | `int(t / 100) * 100` **trunca** en lugar de **redondear** al múltiplo de 100 más cercano. Debería redondearse de forma comercial (los `$50` suben): `9080 → 9100`, `8550 → 8600`. Genera cobros sistemáticamente a la baja. |

## 2. Clasificación del mantenimiento (ISO/IEC 14764)

| Defecto | Descripción | Tipo de mantenimiento |
|---------|-------------|-----------------------|
| DEF-01 | Usar `CONFIG["DESC_VIP"]` en cliente VIP | **Correctivo** |
| DEF-02 | Validar que la zona sea `urbana`, `rural` o `nacional` | **Correctivo** |
| DEF-03 | Validar que el día sea entero entre 1 y 7 | **Correctivo** |
| DEF-04 | Validar cupón: sólo `None` o `"ENVIO10"` | **Correctivo** |
| DEF-05 | Fin de semana `d >= 6` (sábado y domingo), antes de descuentos | **Correctivo** |
| DEF-06 | Redondeo comercial al múltiplo de 100 más cercano (los `$50` suben) | **Correctivo** |
| DEF-07 | Redondeo con `Decimal`/`ROUND_HALF_UP` para evitar errores de punto flotante | **Correctivo** (preventivo de precisión) |
| — | Eliminar el argumento `flag` de `calc` | **Perfectivo** (SRP / limpieza de API) |
| — | Extraer funciones pequeñas y limpias (validación, tramos, descuentos) | **Perfectivo / Preventivo** |
| — | Aplicar **Patrón Estrategia** para los recargos por zona | **Perfectivo / Preventivo** (extensibilidad y bajo acoplamiento) |

## 3. Ramas de trabajo

- `test/suite`: suite de pruebas automatizadas (caja negra + caja blanca).
- `fix/DEF-01` … `fix/DEF-07`: una rama por defecto, fusionadas con `--no-ff`.
- `refactor/estrategia`: refactorización con Patrón Estrategia + extracción de funciones,
  fusión `--no-ff` a la rama principal.

> Nota de QA: el caso **CP-22** de la suite original declaraba `8400` como resultado esperado,
> pero la secuencia de reglas de negocio vigente (base 9000 → +10 % rural → +2000 fin de semana
> → −15 % VIP → −10 % cupón → piso → redondeo) produce `9100`. Ver sección de trazabilidad en
> el reporte de pruebas.

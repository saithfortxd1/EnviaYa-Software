# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

## [1.1.0] - 2026-11-12

### Añadido
- Cliente **`"empresarial"`** con un **12 % de descuento** sobre la tarifa
  (constante `DESC_EMPRESARIAL`, rama en `_aplicar_descuentos`).
- **Exoneración del recargo de zona** para el cliente empresarial cuando el
  peso supera `L2` (> 10 kg), mediante el helper `_exonerar_recargo_zona`.
- Casos de prueba CP para el cliente empresarial (peso ≤ 10 kg y peso > 10 kg).
- `ANALISIS_IMPACTO.md` (CAMBIO = 1) y `NOTAS_REFACTORIZACION.md`.

### Cambiado
- Sin cambios en la firma pública `calc(p, z, c, d, cup=None)` (retrocompatible).

### Notas de versión
- **`v1.1.0` (MINOR).** El cambio es una funcionalidad nueva retrocompatible:
  no se rompe ninguna API ni se altera el comportamiento de los clientes
  `normal`, `frecuente` ni `vip`. Se habría usado `v2.0.0` (MAJOR) solo si la
  firma de `calc` hubiera cambiado de forma incompatible; no es el caso.

## [1.0.0] - 2026-11-12

### Añadido
- Módulo `envios.py` con la función heredada `calc` y el diccionario `CONFIG`.
- Suite de pruebas de caja negra y caja blanca `tests/test_envios.py`.
- Refactorización con Patrón Estrategia por zona, constantes con nombre,
  funciones extraídas y eliminación del argumento `flag`.
- Correcciones DEF-01 a DEF-07 (NameError `DESC_VIP`, validación de zona, día y
  cupón, recargo de fin de semana `d >= 6` y redondeo comercial `ROUND_HALF_UP`).

### Corregido
- `NameError` en la rama de cliente VIP (`CONFIG["DESC_VIP"]`).
- Ausencia de validación de zona, día y cupón.
- Truncado incorrecto del costo (`int(t/100)*100` → redondeo half-up).

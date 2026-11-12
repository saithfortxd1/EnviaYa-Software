# Análisis de Impacto — EnvíaYa

## 1. Solicitud de cambio

**CAMBIO = 1 — Cliente Empresarial**

- Nuevo tipo de cliente `"empresarial"` con un **12 % de descuento** sobre la tarifa.
- **Exoneración de recargo de zona**: si `peso > L2` (es decir, `peso > 10` kg), el cliente
  empresarial **no** paga el recargo de zona (`urbana`/`rural`/`nacional`).

## 2. Tipo de mantenimiento (ISO/IEC 14764)

**Perfectivo / Evolutivo.** No corrige un defecto existente ni previene una falla: agrega
funcionalidad nueva solicitada por el negocio y evoluciona las reglas de tarificación. La
firma pública `calc(p, z, c, d, cup=None)` **no cambia**, por lo que el cambio es
retrocompatible.

## 3. Trazabilidad de impacto

| Artefacto | Elemento | Impacto |
|-----------|----------|---------|
| Requisitos | **R4** (descuentos por tipo de cliente) | Se extiende con el 12 % empresarial |
| Requisitos | **R6** (recargos de zona) | Se añade la exoneración por peso > L2 |
| Historia de Usuario | **HU2** | "Como cliente empresarial quiero tarifas preferentes por volumen" |
| Código | `envios.py` | Nueva constante, rama de descuento y condición de exoneración de zona |
| Pruebas | `tests/test_envios.py` | 2 casos nuevos (peso ≤ 10 y peso > 10) |
| Documentación | `CHANGELOG.md` | Entrada de versión nueva |
| Git | rama `feature/cliente-empresarial`, tag `v1.1.0` | Trazabilidad de la evolución |

## 4. Reglas de cálculo del cliente empresarial

Sea `base` la tarifa por tramos de peso:

1. `base = tarifa_tramos(p)`.
2. Si `c == "empresarial"` **y** `p > 10` → **se exonera** el recargo de zona.
   En caso contrario se aplica la estrategia de zona (`urbana`/`rural`/`nacional`).
3. Recargo de fin de semana (`d >= 6`) según regla vigente.
4. Descuentos sucesivos: cliente (empresarial **−12 %**), luego cupón.
5. Piso `$5000` y redondeo comercial al múltiplo de 100 más cercano (los `$50` suben).

## 5. Análisis de riesgo

- **Riesgo:** bajo. Cambio **aditivo**, no altera el comportamiento de `normal`,
  `frecuente` ni `vip`. La firma de `calc` se mantiene, sin ruptura de API.
- **Mitigación:** TDD (pruebas primero en RED) + suite de regresión existente
  (16 casos) + cobertura de ramas al 100 %.
- **Compatibilidad:** total con la v1.0.0/v1.1.0 al no introducir cambios de firma.

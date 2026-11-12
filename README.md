# Sistema de Envíos — EnvíaYa (Evaluación de Calidad de Software)

## Descripción

Proyecto académico de **auditoría y aseguramiento de la calidad de software** sobre el
módulo de cálculo de costos de envío de *EnvíaYa*. Partiendo de un código heredado con
defectos lógicos (*code smells*), se realizó:

- **Auditoría** del código heredado y documentación de malos olores
  (magic numbers, *God Function*, *flag argument*, variable no definida, validación
  ausente, truncado incorrecto).
- **Corrección** de los defectos `DEF-01` … `DEF-07` en ramas independientes.
- **Refactorización** aplicando el **Patrón Estrategia (Strategy)** para los recargos por
  zona, extracción de funciones y eliminación de números mágicos y del argumento `flag`.
- **Pruebas automatizadas** de caja negra y caja blanca con `pytest`, con **cobertura
  100 %** (líneas y ramas).
- **Evolución** controlada con Git (ramas `fix/*`, `refactor/*`, `feature/*`),
  versionado semántico (`v1.0.0`, `v1.1.0`) y `CHANGELOG`.

## Requisitos

- **Python 3.x** (probado con Python 3.14)
- **pytest**
- **pytest-cov**

## Instrucciones de Ejecución

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la suite de pruebas con cobertura:

```bash
python -m pytest -v --cov=envios
```

Reportes generados: `htmlcov/index.html` (HTML) y `coverage.xml` (XML).

## Estructura del Proyecto

| Archivo / Carpeta | Descripción |
|-------------------|-------------|
| `envios.py` | Módulo principal: `CONFIG`, Patrón Estrategia por zona y `calc(...)`. |
| `tests/test_envios.py` | Suite de pruebas (caja negra y caja blanca). |
| `requirements.txt` | Dependencias de pruebas y cobertura (`pytest`, `pytest-cov`). |
| `pytest.ini` | Configuración de pytest y reportes de cobertura detallados. |
| `NOTAS_REFACTORIZACION.md` | Auditoría de los 6 *code smells* y clasificación del mantenimiento. |
| `ANALISIS_IMPACTO.md` | Solicitud de cambio `CAMBIO = 1` (cliente empresarial) y trazabilidad. |
| `CHANGELOG.md` | Historial de cambios (formato *Keep a Changelog*). |
| `README.md` | Este documento. |

## Autor

**Saith Moises Martinez Vergara**
Código: **0182410089**

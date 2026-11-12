import pytest
from envios import EstrategiaZona, calc

# Pruebas de validaciones y excepciones (Reglas R1, R2, R7)
def test_peso_invalido():
    with pytest.raises(ValueError, match="peso invalido"):
        calc(0, "urbana", "normal", 1)  # CP-01: Límite inferior
    with pytest.raises(ValueError, match="peso invalido"):
        calc(50.1, "urbana", "normal", 1)  # CP-02: Límite superior

def test_zona_invalida():
    # CP-04: Zona 'marte' debería lanzar error, pero el código heredado no lo hace
    with pytest.raises(ValueError):
        calc(5, "marte", "normal", 1)

def test_dia_invalido():
    # CP-05 y CP-06: Días fuera de rango 1-7
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", 8)
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", 0)

def test_cupon_invalido():
    # CP-07: Según regla F=9 (impar), un cupón falso debe lanzar error
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", 1, cup="FALSO")

def test_peso_tipo_invalido():
    # CP-08: Peso no numérico debe lanzar ValueError
    with pytest.raises(ValueError, match="peso invalido"):
        calc("cinco", "urbana", "normal", 1)

def test_estrategia_zona_abstracta():
    # Caja blanca: la clase base abstracta EstrategiaZona no debe implementar el cálculo
    class EstrategiaDummy(EstrategiaZona):
        def calcular(self, tarifa):
            return super().calcular(tarifa)
    with pytest.raises(NotImplementedError):
        EstrategiaDummy().calcular(1000)

# Pruebas parametrizadas de cálculo de costos (Reglas R3, R4, R5, R6, R8)
@pytest.mark.parametrize("p, z, c, d, cup, esperado", [
    (3.0, "urbana", "normal", 1, None, 6000),      # CP-10: Límite Tramo 1 (D=0 par, incluye límite)
    (10.1, "urbana", "normal", 1, None, 9100),     # CP-15: Límite Tramo 2 y redondeo normal (9080 sube a 9100)
    (4, "urbana", "normal", 6, None, 11000),       # CP-20: Sábado (d=6) suma recargo. Falla por 'd>6' en heredado
    (50.0, "nacional", "normal", 1, None, 57400),  # CP-17: PMAX y recargo nacional (40%)
    (1, "urbana", "vip", 1, "ENVIO10", 5000),      # CP-28: Regla de piso $5000 y falla NameError DESC_VIP
    (5, "urbana", "frecuente", 1, None, 8600),     # CP-31: Regla de redondeo terminada en 50 (8550 sube a 8600)
    # CP-22: Tabla decisión (B=1, E=8). Múltiples recargos acumulados:
    # 9000 -> +10% rural=9900 -> +2000 finde=11900 -> -15% vip=10115
    # -> -10% cupón=9103.5 -> redondeo half-up=9100
    (5, "rural", "vip", 6, "ENVIO10", 9100),
    (5, "urbana", "normal", 7, None, 11000),       # CP-23: Domingo (d=7) suma recargo de fin de semana
    (5, "urbana", "normal", 5, None, 9000),        # CP-24: Viernes (d=5) sin recargo de fin de semana
    (2, "nacional", "frecuente", 1, None, 8000),   # CP-25: Tramo 1 + nacional + frecuente (6000*1.4*0.95=7980 -> 8000)
    # CAMBIO=1 (cliente empresarial). Caso 1: peso <= 10 mantiene recargo de zona.
    # 9000 -> +10% rural=9900 -> -12% empresarial=8712 -> redondeo=8700
    (5, "rural", "empresarial", 1, None, 8700),
    # CAMBIO=1. Caso 2: peso > 10 exonera el recargo de zona (nacional NO se aplica).
    # 9800 (base) -> zona exonerada=9800 -> -12% empresarial=8624 -> redondeo=8600
    (11, "nacional", "empresarial", 1, None, 8600),
])
def test_calculo_costos(p, z, c, d, cup, esperado):
    assert calc(p, z, c, d, cup=cup) == esperado

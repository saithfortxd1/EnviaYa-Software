import pytest
from envios import calc

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

# Pruebas parametrizadas de cálculo de costos (Reglas R3, R4, R5, R6, R8)
@pytest.mark.parametrize("p, z, c, d, cup, esperado", [
    (3.0, "urbana", "normal", 1, None, 6000),      # CP-10: Límite Tramo 1 (D=0 par, incluye límite)
    (10.1, "urbana", "normal", 1, None, 9100),     # CP-15: Límite Tramo 2 y redondeo normal (9080 sube a 9100)
    (4, "urbana", "normal", 6, None, 11000),       # CP-20: Sábado (d=6) suma recargo. Falla por 'd>6' en heredado
    (50.0, "nacional", "normal", 1, None, 57400),  # CP-17: PMAX y recargo nacional (40%)
    (1, "urbana", "vip", 1, "ENVIO10", 5000),      # CP-28: Regla de piso $5000 y falla NameError DESC_VIP
    (5, "urbana", "frecuente", 1, None, 8600),     # CP-31: Regla de redondeo terminada en 50 (8550 sube a 8600)
    (5, "rural", "vip", 6, "ENVIO10", 8400),       # CP-22: Tabla decisión (B=1, E=8). Múltiples recargos.
])
def test_calculo_costos(p, z, c, d, cup, esperado):
    assert calc(p, z, c, d, cup=cup) == esperado

"""Cálculo de costos de envío de EnvíaYa.

Módulo refactorizado a partir del sistema heredado. Se aplica el Patrón
Estrategia para los recargos por zona y se extraen funciones pequeñas y
limpias para validación, tramos, recargos y descuentos. Se eliminan los
números mágicos y el argumento ``flag``.
"""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP


CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.10,
    "RECARGO_NACIONAL": 0.40,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,
}

# Constantes con nombre: eliminan los Magic Numbers del código heredado.
PESO_MINIMO = 0
PESO_MAXIMO = 50
TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_EXCEDENTE = 800
DESC_FRECUENTE = 0.05
DESC_CUPON_ENVIO10 = 0.10
TARIFA_MINIMA = 5000
DIA_MINIMO = 1
DIA_MAXIMO = 7
DIA_FIN_DE_SEMANA_INICIO = 6
UNIDAD_REDONDEO = 100
CUPON_ENVIO10 = "ENVIO10"


class EstrategiaZona(ABC):
    """Patrón Estrategia: aplica el recargo propio de cada zona."""

    @abstractmethod
    def calcular(self, tarifa):
        """Devuelve la tarifa con el recargo de la zona aplicado."""
        raise NotImplementedError


class ZonaUrbana(EstrategiaZona):
    def calcular(self, tarifa):
        return tarifa


class ZonaRural(EstrategiaZona):
    def calcular(self, tarifa):
        return tarifa + tarifa * CONFIG["RECARGO_RURAL"]


class ZonaNacional(EstrategiaZona):
    def calcular(self, tarifa):
        return tarifa + tarifa * CONFIG["RECARGO_NACIONAL"]


_ESTRATEGIAS_ZONA = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


def _validar_peso(p):
    if not isinstance(p, (int, float)) or isinstance(p, bool):
        raise ValueError("peso invalido")
    if p <= PESO_MINIMO or p > PESO_MAXIMO:
        raise ValueError("peso invalido")


def _validar_zona(z):
    if not isinstance(z, str) or z not in _ESTRATEGIAS_ZONA:
        raise ValueError("zona invalida")


def _validar_dia(d):
    if not isinstance(d, int) or isinstance(d, bool) or not (DIA_MINIMO <= d <= DIA_MAXIMO):
        raise ValueError("dia invalido")


def _validar_cupon(cup):
    if cup is not None and cup != CUPON_ENVIO10:
        raise ValueError("cupon invalido")


def _calcular_tarifa_base(p):
    if p <= CONFIG["L1"]:
        return TARIFA_TRAMO_1
    if p <= CONFIG["L2"]:
        return TARIFA_TRAMO_2
    return TARIFA_TRAMO_2 + (p - CONFIG["L2"]) * TARIFA_KG_EXCEDENTE


def _aplicar_recargo_fin_de_semana(tarifa, d):
    if d >= DIA_FIN_DE_SEMANA_INICIO:
        return tarifa + CONFIG["RECARGO_FINDE"]
    return tarifa


def _aplicar_descuentos(tarifa, c, cup):
    if c == "frecuente":
        tarifa = tarifa - tarifa * DESC_FRECUENTE
    if c == "vip":
        tarifa = tarifa - tarifa * CONFIG["DESC_VIP"]
    if cup == CUPON_ENVIO10:
        tarifa = tarifa - tarifa * DESC_CUPON_ENVIO10
    return tarifa


def _aplicar_tarifa_minima(tarifa):
    return max(tarifa, TARIFA_MINIMA)


def _redondear(tarifa):
    """Redondeo comercial al múltiplo de 100 más cercano (los 50 suben)."""
    factor = Decimal(str(tarifa)) / UNIDAD_REDONDEO
    return int(factor.quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * UNIDAD_REDONDEO


def calc(p, z, c, d, cup=None):
    """Calcula el costo final del envío.

    ``p`` peso en kg, ``z`` zona, ``c`` tipo de cliente, ``d`` día de la
    semana (1..7), ``cup`` cupón opcional.
    """
    _validar_peso(p)
    _validar_zona(z)
    _validar_dia(d)
    _validar_cupon(cup)

    tarifa = _calcular_tarifa_base(p)
    tarifa = _ESTRATEGIAS_ZONA[z].calcular(tarifa)
    tarifa = _aplicar_recargo_fin_de_semana(tarifa, d)
    tarifa = _aplicar_descuentos(tarifa, c, cup)
    tarifa = _aplicar_tarifa_minima(tarifa)
    return _redondear(tarifa)

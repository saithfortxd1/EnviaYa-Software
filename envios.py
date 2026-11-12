from decimal import Decimal, ROUND_HALF_UP


CONFIG = {
    "L1": 3,
    "L2": 10,
    "RECARGO_RURAL": 0.10,
    "RECARGO_NACIONAL": 0.40,
    "DESC_VIP": 0.15,
    "RECARGO_FINDE": 2000,
}


def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > 50:
        raise ValueError("peso invalido")
    if z not in ("urbana", "rural", "nacional"):
        raise ValueError("zona invalida")
    if not isinstance(d, int) or isinstance(d, bool) or not (1 <= d <= 7):
        raise ValueError("dia invalido")
    if cup is not None and cup != "ENVIO10":
        raise ValueError("cupon invalido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    # fin de semana (sabado=6 y domingo=7), antes de los descuentos
    if d >= 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    # redondeo comercial estandar (ROUND_HALF_UP) con Decimal para evitar
    # errores de punto flotante (los 50 suben)
    return int((Decimal(str(t)) / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) * 100

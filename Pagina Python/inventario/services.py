from decimal import Decimal
from .models import Estampado


def calcular_precio_estampado(est):
    print("EST:", est)

    subtotal = Decimal("0")

    est_id = est.get("id")
    tamano = int(est.get("tamano") or 40)

    print("ID:", est_id)
    print("TAMAÑO:", tamano)

    if est_id == "imagen_propia":
        subtotal += Decimal(str(est.get("precio", 0)))
    else:
        try:
            estampado = Estampado.objects.get(
                id_estamp=est_id
            )

            print("ENCONTRÓ:", estampado)
            print("COSTO:", estampado.costo_adi)

            subtotal += Decimal(
                str(estampado.costo_adi)
            )

        except Estampado.DoesNotExist:
            print("NO EXISTE EL ESTAMPADO")
            return Decimal("0")

    if tamano >= 180:
        subtotal += Decimal("12000")
    elif tamano >= 90:
        subtotal += Decimal("5000")

    print("SUBTOTAL:", subtotal)

    return subtotal

def calcular_precio_personalizacion(
    precio_producto,
    lista_estampados
):
    precio = Decimal(str(precio_producto))
    print("INICIO:", precio)

    for est in lista_estampados:
        adicional = calcular_precio_estampado(est)
        print("ADICIONAL:", adicional)

        precio += adicional
        print("ACUMULADO:", precio)

    return precio
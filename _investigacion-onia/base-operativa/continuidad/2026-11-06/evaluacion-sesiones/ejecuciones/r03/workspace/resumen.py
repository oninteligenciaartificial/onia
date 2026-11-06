from decimal import Decimal, ROUND_HALF_UP, localcontext


def subtotal(pedido):
    activos = []
    enteros = 1
    decimales = 2
    for fila in pedido:
        unidades = fila["unidades"]
        precio = Decimal(fila["precio"])
        estado = fila["estado"]
        if unidades < 0 or not precio.is_finite() or precio < 0:
            raise ValueError("Unidades y precio deben ser no negativos")
        if estado not in ("activo", "anulado"):
            raise ValueError("Estado desconocido")
        if estado == "activo":
            activos.append((unidades, precio))
            # Reservar precisión para multiplicar y sumar sin redondeo previo.
            digitos = len(precio.as_tuple().digits)
            exponente = precio.as_tuple().exponent
            enteros = max(enteros, digitos + exponente + len(str(unidades)))
            decimales = max(decimales, -exponente)

    with localcontext() as contexto:
        contexto.prec = enteros + decimales + len(str(len(activos))) + 2
        total = sum((unidades * precio for unidades, precio in activos), Decimal(0))
        return format(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")

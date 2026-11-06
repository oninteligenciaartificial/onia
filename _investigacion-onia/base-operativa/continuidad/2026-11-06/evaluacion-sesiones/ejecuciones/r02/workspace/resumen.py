from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


def subtotal(pedido):
    total = Decimal("0")
    for fila in pedido:
        unidades = fila["unidades"]
        try:
            precio = Decimal(fila["precio"])
        except (InvalidOperation, ValueError):
            raise ValueError("precio inválido") from None
        if unidades < 0 or not precio.is_finite() or precio < 0:
            raise ValueError("unidades y precio deben ser no negativos")
        estado = fila["estado"]
        if estado not in ("activo", "anulado"):
            raise ValueError("estado desconocido")
        if estado == "activo":
            total += unidades * precio
    return format(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")

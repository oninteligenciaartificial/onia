from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext


def subtotal(pedido):
    filas = []
    for fila in pedido:
        unidades = fila["unidades"]
        if not isinstance(unidades, int) or isinstance(unidades, bool) or unidades < 0:
            raise ValueError("Las unidades deben ser enteras no negativas")
        try:
            precio = Decimal(fila["precio"])
        except (InvalidOperation, TypeError, ValueError) as error:
            raise ValueError("Precio inválido") from error
        if not precio.is_finite() or precio < 0:
            raise ValueError("El precio debe ser un decimal no negativo")
        if fila["estado"] not in ("activo", "anulado"):
            raise ValueError("Estado desconocido")
        if fila["estado"] == "activo":
            filas.append((unidades, precio))

    # Mantener precisión suficiente para multiplicar y sumar antes de redondear.
    decimales = max((max(0, -p.as_tuple().exponent) for _, p in filas), default=0)
    enteros = max((max(1, p.adjusted() + 1) + len(str(u)) for u, p in filas), default=1)
    with localcontext() as contexto:
        contexto.prec = max(28, enteros + decimales + len(str(len(filas))) + 2)
        total = sum((u * p for u, p in filas), Decimal(0))
        return str(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

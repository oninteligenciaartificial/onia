"""Cálculo decimal del subtotal de pedidos."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, localcontext


def subtotal(pedido):
    filas = []
    for fila in pedido:
        unidades = fila["unidades"]
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades < 0:
            raise ValueError("Las unidades deben ser enteras no negativas")
        try:
            precio = Decimal(fila["precio"])
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("El precio debe ser decimal no negativo") from exc
        if not precio.is_finite() or precio < 0:
            raise ValueError("El precio debe ser decimal no negativo")
        estado = fila["estado"]
        if estado not in ("activo", "anulado"):
            raise ValueError("Estado desconocido")
        if estado == "activo":
            filas.append((unidades, precio))

    # Cubrir todos los dígitos de los productos y la suma antes de redondear.
    escala = min([-2] + [p.as_tuple().exponent for _, p in filas])
    enteros = max([1] + [p.adjusted() + len(str(u)) + 1 for u, p in filas])
    with localcontext() as contexto:
        contexto.prec = max(28, enteros - escala + len(str(len(filas) + 1)))
        total = sum((u * p for u, p in filas), Decimal(0))
        return format(total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP), ".2f")

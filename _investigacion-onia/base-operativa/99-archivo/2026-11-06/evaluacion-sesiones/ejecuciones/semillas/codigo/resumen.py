def subtotal(pedido):
    total = 0.0
    for fila in pedido:
        total += fila["unidades"] * float(fila["precio"])
    return str(round(total, 2))

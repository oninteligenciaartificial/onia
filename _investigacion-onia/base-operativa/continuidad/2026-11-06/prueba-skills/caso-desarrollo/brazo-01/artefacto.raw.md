# Corrección del selector

La versión original convierte `seq` en texto y ordena la lista in situ: con 9 y 10 devuelve 9 y cambia el orden de entrada. La corrección recorre los eventos, compara enteros y reemplaza el candidato también en empate, conservando la última aparición. Para una lista vacía devuelve `None` y no modifica la entrada.

```python
def select_latest(events):
    latest = None
    for event in events:
        if latest is None or event["seq"] >= latest["seq"]:
            latest = event
    return latest
```

El fallo original se reprodujo con 9 y 10: devolvió 9 y reordenó la lista. El check funcional posterior pasó sus cinco escenarios, incluidos empate, vacío y preservación de entrada; salida completa en `checks.stdout.txt`. No se añadió validación fuera del contrato.

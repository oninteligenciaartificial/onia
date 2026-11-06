# Corrección de select_latest

```python
def select_latest(events):
    latest = None
    for event in events:
        if latest is None or event["seq"] >= latest["seq"]:
            latest = event
    return latest
```

La implementación original convertía `seq` a cadena antes de ordenar: por eso `"9"` queda después de `"10"`. Además, `sort` modificaba la lista recibida. Se reprodujo con los eventos 9 y 10: devolvió 9 y cambió el orden de entrada. No se dispone de historial de cambios en este caso aislado.

El recorrido compara enteros sin ordenar ni modificar la entrada; `>=` conserva la última aparición del máximo. Para una lista vacía devuelve `None`.

Se ejecutó `python -B check_funcional.py .` sobre `solution.py`. Los cinco escenarios pasaron: vacío, 9/10, empate, cero y 100/11; en todos la entrada permaneció igual. La salida completa está en `checks.stdout.txt`. La comprobación cubre los escenarios suministrados, no todas las entradas posibles del contrato.

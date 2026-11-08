"""Comprueba el resultado de C sin escribir archivos."""

import json
from pathlib import Path
import sys


ESPERADO = {"tarea": "c", "valores": [11, 13, 17], "suma": 41, "maximo": 17}


def coincide(actual, esperado):
    """Compara el objeto completo y exige tipos exactos en cada nivel."""
    if type(actual) is not type(esperado):
        return False
    if type(esperado) is dict:
        return actual.keys() == esperado.keys() and all(
            coincide(actual[clave], valor) for clave, valor in esperado.items()
        )
    if type(esperado) is list:
        return len(actual) == len(esperado) and all(
            coincide(a, e) for a, e in zip(actual, esperado)
        )
    return actual == esperado


def verificar(objeto):
    if not coincide(objeto, ESPERADO):
        raise ValueError("El objeto no coincide exactamente con el resultado de C")


def main():
    try:
        objeto = json.loads(Path(__file__).with_name("resultado.json").read_text(encoding="utf-8"))
        verificar(objeto)
    except (OSError, ValueError) as error:
        print(f"PARALELO_C_ERROR: {error}", file=sys.stderr)
        return 1
    print("PARALELO_C_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

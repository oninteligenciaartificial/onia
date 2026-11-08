"""Comprueba el resultado sintético del juguete b sin escribir archivos."""

import json
from pathlib import Path
import sys


def verificar(objeto):
    esperado = {"tarea": "b", "valores": [3, 5, 7], "suma": 15, "maximo": 7}
    if type(objeto) is not dict or objeto.keys() != esperado.keys():
        raise ValueError("Objeto o claves discrepantes")
    if type(objeto["tarea"]) is not str:
        raise ValueError("tarea debe ser texto")
    if type(objeto["valores"]) is not list:
        raise ValueError("valores debe ser una lista")
    if any(type(valor) is not int for valor in objeto["valores"]):
        raise ValueError("valores debe contener sólo enteros")
    if any(type(objeto[clave]) is not int for clave in ("suma", "maximo")):
        raise ValueError("suma y maximo deben ser enteros")
    if objeto != esperado:
        raise ValueError("Resultado discrepante")


def main():
    try:
        objeto = json.loads(Path(__file__).with_name("resultado.json").read_text(encoding="utf-8"))
        verificar(objeto)
    except (OSError, ValueError) as error:
        print(f"PARALELO_B_ERROR: {error}", file=sys.stderr)
        return 1
    print("PARALELO_B_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

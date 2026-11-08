import json
from pathlib import Path


ESPERADO = {"tarea": "a", "valores": [2, 4, 6], "suma": 12, "maximo": 6}


def verificar(objeto):
    if type(objeto) is not dict or objeto != ESPERADO:
        raise ValueError("Objeto discrepante")
    if type(objeto["valores"]) is not list:
        raise ValueError("valores debe ser una lista")
    enteros = [*objeto["valores"], objeto["suma"], objeto["maximo"]]
    if any(type(valor) is not int for valor in enteros):
        raise ValueError("Se requieren enteros exactos")


def main():
    ruta = Path(__file__).resolve().parent / "resultado.json"
    try:
        verificar(json.loads(ruta.read_text(encoding="utf-8")))
    except (OSError, ValueError) as error:
        raise SystemExit(f"PARALELO_A_ERROR: {error}")
    print("PARALELO_A_OK")


if __name__ == "__main__":
    main()

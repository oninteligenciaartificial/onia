import json
from pathlib import Path
import sys


def main():
    esperado = {
        "valores": [4, 1, 7],
        "ordenados": [1, 4, 7],
        "suma": 12,
        "cuadrados": [16, 1, 49],
    }
    try:
        ruta = Path(__file__).resolve().parent / "resultado.json"
        resultado = json.loads(ruta.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        print(f"AUTOPUSH_ERROR {error}", file=sys.stderr)
        return 1

    if json.dumps(resultado, sort_keys=True) != json.dumps(esperado, sort_keys=True):
        print("AUTOPUSH_ERROR objeto discrepante", file=sys.stderr)
        return 1

    print("AUTOPUSH_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

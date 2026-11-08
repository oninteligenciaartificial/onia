import json
import sys
from pathlib import Path


def main():
    carpeta = Path(__file__).resolve().parent
    esperados = {
        "checkpoint.json": {"etapa": "preparado", "valores": [2, 3, 5]},
        "resultado.json": {
            "etapa": "completo", "valores": [2, 3, 5], "total": 10, "cantidad": 3
        },
    }
    try:
        for nombre, esperado in esperados.items():
            contenido = json.loads((carpeta / nombre).read_text(encoding="utf-8"))
            if contenido != esperado:
                print(f"PILOTO_ERROR: {nombre} no coincide", file=sys.stderr)
                return 1
    except (OSError, ValueError) as error:
        print(f"PILOTO_ERROR: {error}", file=sys.stderr)
        return 1
    print("PILOTO_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

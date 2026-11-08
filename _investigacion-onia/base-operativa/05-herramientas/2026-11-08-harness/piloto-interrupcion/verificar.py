from pathlib import Path
import hashlib
import json
import sys


CHECKPOINT = b'{"etapa":"antes-interrupcion","valores":[6,9,12]}\n'
NOTA = b'Nota sin seguimiento: conservar estos bytes al retomar.\n'
SHA256 = "ab0a32d8c67d70450bd6d29dbae11f10aef561917223f49e4b289ce79d28f483"
RESULTADO = {"valores": [6, 9, 12], "total": 27, "checkpoint_sha256": SHA256}


def objeto_unico(pares):
    objeto = dict(pares)
    if len(objeto) != len(pares):
        raise ValueError("Claves duplicadas en resultado")
    return objeto


def verificar():
    carpeta = Path(__file__).resolve().parent
    checkpoint = (carpeta / "checkpoint.json").read_bytes()
    if checkpoint != CHECKPOINT:
        raise ValueError("Bytes del checkpoint discrepantes")
    if (carpeta / "nota.txt").read_bytes() != NOTA:
        raise ValueError("Bytes de la nota discrepantes")
    if hashlib.sha256(checkpoint).hexdigest() != SHA256:
        raise ValueError("SHA256 discrepante")
    resultado = json.loads(
        (carpeta / "resultado.json").read_text(encoding="utf-8"),
        object_pairs_hook=objeto_unico,
    )
    if json.dumps(resultado, sort_keys=True) != json.dumps(RESULTADO, sort_keys=True):
        raise ValueError("Resultado discrepante")


def main():
    try:
        verificar()
    except (OSError, ValueError) as error:
        print(f"RETOMA_ERROR {error}", file=sys.stderr)
        return 1
    print("RETOMA_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

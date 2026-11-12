"""Prepara una copia privada inactiva del workflow aprobado, sin contactar n8n."""

import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import urlsplit

CARPETA = Path(__file__).resolve().parent
FUENTE = CARPETA.parent / "trabajos/fabrica-chatbot-whatsapp-20261110/workflow-despacho-n8n.json"
SHA256_APROBADO = "62567c0267b82c2725091ecfa6c7ddc9e6c86f65ef2b82964d928dcf36e39b49"


def preparar(plan):
    raw = FUENTE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA256_APROBADO:
        raise ValueError("La fuente difiere del artefacto aprobado")
    origen = plan["origen_privado"]
    if origen != plan["origen_permitido"]:
        raise ValueError("El origen debe coincidir exactamente con el permitido")
    url = urlsplit(origen)
    if (url.scheme not in ("http", "https") or not url.hostname
            or url.username is not None or url.password is not None
            or url.query or url.fragment or url.path or url.port == 0
            or origen != origen.strip() or "\\" in origen):
        raise ValueError("Se requiere un origen sin rutas, credenciales ni barras finales")
    dispatcher = plan["credencial_dispatcher_id"]
    operador = plan["credencial_operador_id"]
    if (not isinstance(dispatcher, str) or not dispatcher.strip()
            or not isinstance(operador, str) or not operador.strip()
            or dispatcher.strip() == operador.strip()):
        raise ValueError("Las referencias dispatcher y operador deben ser distintas")
    workflow = json.loads(raw)
    workflow["name"] += " · Copia de ensayo manual"
    nodo = workflow["nodes"][1]
    nodo["parameters"]["url"] = origen + "/operador/despachar"
    nodo["credentials"] = {"httpHeaderAuth": {"id": dispatcher,
                                              "name": "ONIA dispatcher · ensayo manual"}}
    return workflow


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    os.umask(0o077)
    try:
        workflow = preparar(json.loads(args.plan.read_text()))
        # x evita sobrescribir exports o una copia preparada anteriormente.
        with args.salida.open("x", encoding="utf-8") as stream:
            json.dump(workflow, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
    except (OSError, ValueError, KeyError, TypeError):
        parser.exit(2, "Preparación bloqueada. Revisar plan, fuente y destino privados.\n")
    print("Copia privada inactiva preparada. Conectividad e importación pendientes.")


if __name__ == "__main__":
    main()

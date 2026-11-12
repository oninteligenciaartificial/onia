"""Arranque temporal de staging: loopback, sin despacho ni conexiones salientes."""

import argparse
import json
import os
from pathlib import Path
import signal
import sys
import time
from wsgiref.simple_server import make_server

from comun import cargar_adaptador
from fixture import AHORA, CONFIG


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--puerto", type=int, default=8765)
    parser.add_argument("--reloj-ficticio", action="store_true",
                        help="Sólo admite la configuración exacta generada por fixture.py")
    args = parser.parse_args()
    if not 0 <= args.puerto <= 65535:
        parser.error("puerto fuera de rango")
    os.umask(0o077)
    adaptador = cargar_adaptador()
    try:
        archivo, cfg = adaptador.leer_config(args.config)
        if cfg.get("envios_habilitados", False) is not False:
            raise ValueError("staging exige envíos deshabilitados")
        if args.reloj_ficticio and cfg != CONFIG:
            raise ValueError("el reloj ficticio exige el fixture exacto")
        adaptador.validar_config(cfg, False)
    except (OSError, ValueError, adaptador.ErrorHTTP):
        parser.exit(2, "Configuración privada inválida para staging; no se muestran valores.\n")

    contadores = {"conexiones_salientes_intentadas": 0, "transporte_invocado": 0}

    def bloquear_red(evento, argumentos):
        if evento == "socket.connect":
            contadores["conexiones_salientes_intentadas"] += 1
            raise PermissionError("STAGING_SIN_EGRESO")

    def bloquear_transporte(*args):
        contadores["transporte_invocado"] += 1
        raise PermissionError("STAGING_SIN_TRANSPORTE")

    # Defensa adicional a permitir_envios=False. También bloquea un connect accidental.
    sys.addaudithook(bloquear_red)
    app = adaptador.crear_app(archivo.with_name("chatbot.sqlite3"), cfg,
                             permitir_envios=False, transporte=bloquear_transporte,
                             reloj=(lambda: AHORA) if args.reloj_ficticio else time.time)

    def detener(signum, frame):
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, detener)
    signal.signal(signal.SIGINT, detener)
    try:
        with make_server("127.0.0.1", args.puerto, app,
                         handler_class=adaptador.SinRegistro) as servidor:
            print(json.dumps({"evento": "listo", "host": "127.0.0.1",
                              "puerto": servidor.server_port, "envios_habilitados": False,
                              "reloj_ficticio": args.reloj_ficticio}), flush=True)
            servidor.serve_forever()
    finally:
        print(json.dumps({"evento": "detenido", **contadores}), flush=True)


if __name__ == "__main__":
    main()

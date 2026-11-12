"""Genera exclusivamente configuración ficticia en un temporal propio de /tmp."""

from datetime import datetime
import json
import os
from pathlib import Path
import tempfile

AHORA = int(datetime.fromisoformat("2026-11-12T00:00:00+00:00").timestamp())
CLIENTE = "999000000001"
CONFIG = {
    "phone_number_id": "000",
    "app_secret": "fixture-app-secret-no-real",
    "verify_token": "fixture-verify-token-no-real",
    "operator_token": "fixture-operator-token-no-real",
    "dispatcher_token": "fixture-dispatch-token-no-real",
    "envios_habilitados": False,
    "pago_ttl_segundos": 3600,
    "cierre_inscripcion_epoch": AHORA + 86400,
    "qr_media_id": "000001",
    "meet_urls": [f"https://meet.google.com/fixture-{i}" for i in range(1, 4)],
}


def escribir(carpeta):
    archivo = Path(carpeta) / "config.json"
    with archivo.open("x", encoding="utf-8") as destino:
        json.dump(CONFIG, destino)
    archivo.chmod(0o600)
    return archivo


if __name__ == "__main__":
    os.umask(0o077)
    print(escribir(tempfile.mkdtemp(prefix="onia-whatsapp-fixture-", dir="/tmp")))

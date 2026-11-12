"""Referencias al producto existente; no contiene lógica de inscripción."""

import importlib.util
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
PRODUCTO = CARPETA.parent / "trabajos" / "fabrica-chatbot-whatsapp-20261110"


def cargar_adaptador():
    spec = importlib.util.spec_from_file_location("adaptador_aceptado", PRODUCTO / "adaptador.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

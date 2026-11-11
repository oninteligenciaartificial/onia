"""Consume el contrato con el lector existente en un módulo aislado; no modifica UI."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[3]
EXPORT = str((ROOT / "estado-fabrica.json").relative_to(BASE))
PANEL = BASE / "05-herramientas/fabrica-contenido/20261109-lector-panel"


def reader():
    # Dependencias existentes, sólo lectura. No se lanza panel/servidor/harness.
    sys.path.insert(0, str(PANEL))
    try:
        spec = importlib.util.spec_from_file_location("meta_lector_aislado", PANEL / "operacion.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def consume():
    module = reader()
    # La fuente actual rechaza automatizaciones: conservar evidencia de ese límite.
    try:
        module.load_export(EXPORT, {}, {})
    except ValueError:
        native = "rechazado_por_lista_de_productores"
    else:
        native = "admitido"
    # Extensión explícita sólo en esta instancia, limitada a la ruta del encargo.
    module.PRODUCERS = {**module.PRODUCERS, "automatizaciones": str(ROOT.relative_to(BASE))}
    documents, targets = {}, {}
    data = module.load_export(EXPORT, documents, targets)
    model = module.build([EXPORT])
    factory = next(f for f in model["fabricas"] if f["id"] == "automatizaciones")
    return {"modo": "contrato_local", "ui_publicada": False, "lector_sin_puente": native,
            "id": data["id"], "estado": data["estado"], "exports_consumidos": len(factory["exports"]),
            "documentos": len(documents), "targets_revision": len(targets),
            "documentos_disponibles": all(d["disponible"] for d in
                [data["documento_fuente"]] + [e for p in data["pasos"] for e in p["evidencias"]]
                + [d["documento"] for d in data["entregables"]]),
            "entradas_faltantes": len(data["pendientes"]), "errores_modelo": model["errores"]}


if __name__ == "__main__":
    print(json.dumps(consume(), ensure_ascii=False, indent=2))

"""Reproducción sintética, sin red. Salida pública agregada; DB temporal privada."""
from copy import deepcopy
import hashlib
import hmac
import json
from pathlib import Path
import tempfile

from adaptador import Adapter, ROOT, Store

NOW = 1794430800  # 2026-11-11T21:00:00Z, reloj fijo del ensayo


def fixture_config():
    # Sólo valores sintéticos; no sirven para Meta.
    return {"envios_habilitados": False,
            "cuentas": {"instagram": "10001", "facebook": "10002"},
            "app_secret": "ENSAYO_FICTICIO_APP_SECRET_0001",
            "verify_token": "ENSAYO_FICTICIO_VERIFY_TOKEN_0002"}


def signed(config, payload):
    raw = json.dumps(payload, separators=(",", ":")).encode()
    signature = hmac.new(config["app_secret"].encode(), raw, hashlib.sha256).hexdigest()
    return raw, {"content-type": "application/json", "x-hub-signature-256": "sha256=" + signature}


def post(adapter, payload, now=NOW):
    raw, headers = signed(adapter.config, payload)
    return adapter.handle("POST", headers, raw, {}, now)


def run():
    fixture = json.loads((ROOT / "fixtures/recorridos.json").read_text())
    result = {"tipo_evidencia": "SIMULACION_LOCAL_NO_E2E", "envios_reales": 0, "canales": []}
    for index, scenario in enumerate(fixture["recorridos"]):
        with tempfile.TemporaryDirectory(prefix="onia-meta-ensayo-") as directory:
            cfg = fixture_config()
            store = Store(Path(directory) / "estado.sqlite", cfg["cuentas"])
            adapter = Adapter(cfg, store)
            reception = post(adapter, scenario["payload"])
            output = store.simulate_one("exito", NOW)
            duplicate = post(adapter, scenario["payload"])
            # Reinicio sobre la misma DB: no reconstruye ni vacía el estado.
            restored = Store(Path(directory) / "estado.sqlite", cfg["cuentas"])
            again = post(Adapter(cfg, restored), scenario["payload"])
            dm = deepcopy(fixture["recorridos"][index if index % 2 else index + 1]["payload"])
            message = dm["entry"][0]["messaging"][0]
            message["message"]["text"] = "WHATSAPP"
            message["message"]["mid"] += "_derivacion1"
            message["timestamp"] = (NOW + 1) * 1000
            missing_destination = post(Adapter(cfg, restored), dm, NOW + 1)
            # Destino estrictamente FICTICIO, sólo en memoria y DB temporal; jamás en salida pública.
            cfg["whatsapp_destino"] = "https://wa.me/" + "1" + "0" * 10
            message["message"]["mid"] += "2"
            message["timestamp"] = (NOW + 2) * 1000
            routing = post(Adapter(cfg, restored), dm, NOW + 2)
            routing_output = restored.simulate_one("exito", NOW + 2)
            message["message"].update(mid=message["message"]["mid"] + "_baja", text="BAJA")
            message["timestamp"] = (NOW + 3) * 1000
            stop = post(Adapter(cfg, restored), dm, NOW + 3)
            message["message"].update(mid=message["message"]["mid"] + "_tras_baja", text="NEGOCIO")
            message["timestamp"] = (NOW + 4) * 1000
            after_stop = post(Adapter(cfg, restored), dm, NOW + 4)
            result["canales"].append({"canal": scenario["canal"], "entrada": reception,
                "transporte_ficticio": output, "repeticion": duplicate, "tras_reinicio": again,
                "destino_ausente": missing_destination, "derivacion_con_destino_ficticio": routing,
                "transporte_derivacion_ficticio": routing_output, "baja": stop, "tras_baja": after_stop,
                "resumen": restored.summary()})
    result["resultados_transporte_por_canal"] = []
    outcomes = json.loads((ROOT / "fixtures/resultados.json").read_text())["casos"]
    for scenario in fixture["recorridos"]:
        for outcome in outcomes:
            with tempfile.TemporaryDirectory(prefix="onia-meta-fallo-") as directory:
                cfg = fixture_config()
                store = Store(Path(directory) / "estado.sqlite", cfg["cuentas"])
                post(Adapter(cfg, store), scenario["payload"])
                result["resultados_transporte_por_canal"].append({"canal": scenario["canal"],
                    "fixture": outcome["resultado"], "salida": store.simulate_one(outcome["resultado"], NOW),
                    "siguiente_intento": store.simulate_one("exito", NOW)})
    return result


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))

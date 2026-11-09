#!/usr/bin/env python3
"""Lectura REST acotada. Sólo persiste whitelist, nunca cuerpos ni errores remotos."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

HERE = Path(__file__).resolve().parent
WORKFLOWS = {
    "NDXLJiR00ciQx72V": "Guiones Diarios",
    "QGXVyRSgrArxfolj": "Radar",
    "nAGwe7DzxNQzMxXk": "Video Intake",
    "fop5l1FEirkYoZke": "demo4campos",
    "nZkaXaZVKzgtwUqU": "borradores",
    "b6hjjNJFLuLXhRm3": "digest",
    "vuicWsvh0hwqKhYs": "Command Center",
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def get_json(path):
    base = os.environ["N8N_API_URL"].rstrip("/")
    if base.endswith("/api/v1"):
        base = base[:-7]
    parsed = urllib.parse.urlsplit(base)
    if parsed.scheme != "https" or parsed.username or parsed.query or parsed.fragment:
        return None, "configuracion_rechazada"
    headers = {"Accept": "application/json"}
    if path.startswith("/api/v1/"):
        headers["X-N8N-API-KEY"] = os.environ["N8N_API_KEY"]
    request = urllib.request.Request(base + path, headers=headers, method="GET")
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=20) as response:
            raw = response.read(4_000_001)
            if len(raw) > 4_000_000:
                return None, "respuesta_excesiva"
            return json.loads(raw), response.status
    except urllib.error.HTTPError as error:
        return None, error.code
    except Exception:
        return None, "dependencia_no_disponible"


def collect():
    credentials, destinations = {}, {}
    report = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "solo_lectura": True,
              "ejecuciones": "última metadata por workflow, sin payloads", "workflows": []}
    settings, status = get_json("/rest/settings")
    version = (settings or {}).get("data", {}).get("versionCli")
    report["version_instancia"] = version if isinstance(version, str) and re.fullmatch(r"\d+\.\d+\.\d+", version) else None
    report["version_http"] = status
    for workflow_id, label in WORKFLOWS.items():
        data, status = get_json("/api/v1/workflows/" + workflow_id + "?excludePinnedData=true")
        item = {"id": workflow_id, "alias": label, "http": status}
        report["workflows"].append(item)
        if data is None:
            continue
        item.update({"active": data.get("active"), "nodos": [], "probado_en_esta_sesion": False})
        for node in data.get("nodes", []):
            node_type = node.get("type", "")
            if not re.fullmatch(r"[\w.@/-]+", node_type):
                node_type = "tipo_no_publicado"
            safe = {"tipo": node_type, "version": node.get("typeVersion"),
                    "deshabilitado": node.get("disabled", False), "credenciales": []}
            for kind, ref in node.get("credentials", {}).items():
                identity = (kind, ref.get("id"))
                alias = credentials.setdefault(identity, "credencial-" + str(len(credentials) + 1))
                safe["credenciales"].append({"tipo": kind, "alias": alias, "referencia_presente": bool(ref.get("id"))})
            params = node.get("parameters", {})
            if "telegram" in node_type.lower():
                destination = params.get("chatId")
                safe["destino_configurado"] = bool(destination)
                safe["destino_expresion"] = isinstance(destination, str) and destination.startswith("=")
                if destination:
                    alias = destinations.setdefault(str(destination), "destino-" + str(len(destinations) + 1))
                    safe["destino_alias"] = alias
            if node_type.endswith(".code"):
                code = params.get("jsCode", "")
                safe["indicios_codigo"] = {key: key in code.lower() for key in
                                           ("telegram", "chat_id", "user_id", "update_id", "revision", "harness")}
            item["nodos"].append(safe)
        executions, execution_status = get_json("/api/v1/executions?workflowId=" + workflow_id + "&limit=1&includeData=false")
        item["ejecucion_metadata_http"] = execution_status
        rows = (executions or {}).get("data", [])
        item["ultima_ejecucion"] = None
        if rows:
            row = rows[0]
            item["ultima_ejecucion"] = {"estado": row.get("status") if row.get("status") in
                                      ("success", "error", "waiting", "running", "canceled", "crashed", "new", "unknown") else "otro",
                                      "inicio": row.get("startedAt"), "fin": row.get("stoppedAt")}
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--salida", required=True, type=Path)
    args = parser.parse_args()
    destination = args.salida.resolve()
    if not destination.is_relative_to(HERE / "evidencia"):
        parser.error("Salida restringida a evidencia/ de esta entrega")
    destination.parent.mkdir(parents=True, exist_ok=True)
    report = collect()
    with destination.open("x") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"resultado": "inventario_guardado", "workflows": len(report["workflows"])}))

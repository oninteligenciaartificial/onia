#!/usr/bin/env python3
"""Crea como máximo una copia propia inactiva. Nunca ejecuta ni modifica flujos."""
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from inventario import HERE, WORKFLOWS, NoRedirect, get_json
from preparar import build


def write_once(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def fingerprint(workflow):
    value = {key: workflow.get(key) for key in ("name", "active", "nodes", "connections", "settings", "staticData")}
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def originals():
    result = {}
    for workflow_id in WORKFLOWS:
        workflow, status = get_json("/api/v1/workflows/" + workflow_id + "?excludePinnedData=true")
        if status != 200 or workflow is None:
            raise ValueError("No se pudieron cotejar originales")
        result[workflow_id] = {"active": workflow["active"], "config_sha256": fingerprint(workflow)}
    return result


def lookup(name):
    query = urllib.parse.urlencode({"name": name, "limit": 100, "excludePinnedData": "true"})
    listing, status = get_json("/api/v1/workflows?" + query)
    if status != 200 or listing is None or listing.get("nextCursor"):
        raise ValueError("Búsqueda no concluyente. Se conserva el JSON importable")
    rows = [row for row in listing["data"] if row.get("name") == name]
    if len(rows) > 1:
        raise ValueError("Nombre duplicado. Conciliación manual requerida")
    return rows


def main():
    folder = HERE / "evidencia"
    folder.mkdir(exist_ok=True)
    receipt_path = folder / "importacion.json"
    intent_path = folder / "intento-importacion.json"
    if receipt_path.exists():
        raise ValueError("Ya existe recibo. Consultarlo antes de otra operación")
    workflow = json.loads((HERE / "workflow-n8n.json").read_text())
    if workflow != build()[1] or workflow["active"] is not False:
        raise ValueError("Workflow distinto del generado o activo")
    if [node["type"] for node in workflow["nodes"]] != [
            "n8n-nodes-base.manualTrigger", "n8n-nodes-base.code", "n8n-nodes-base.code"]:
        raise ValueError("Tipos fuera de alcance")
    if any(node.get("credentials") or node.get("webhookId") for node in workflow["nodes"]):
        raise ValueError("Referencias externas rechazadas")
    before = originals()
    matches = lookup(workflow["name"])
    post_status = None
    post_active = None
    if not matches:
        if intent_path.exists():
            raise ValueError("Intento previo sin coincidencia remota. Conciliar, nunca repetir POST")
        # Persistir intento antes de escribir en remoto permite un reinicio conservador.
        write_once(intent_path, {"fecha_utc": datetime.now(timezone.utc).isoformat(),
                                "nombre": workflow["name"], "local_active": False,
                                "busqueda_previa": "sin_coincidencias", "originales_antes": before})
        payload = {key: workflow[key] for key in ("name", "nodes", "connections", "settings")}
        base = os.environ["N8N_API_URL"].rstrip("/")
        if not base.endswith("/api/v1"):
            base += "/api/v1"
        parsed = urllib.parse.urlsplit(base)
        if parsed.scheme != "https" or parsed.username or parsed.query or parsed.fragment:
            raise ValueError("Configuración rechazada")
        request = urllib.request.Request(base + "/workflows", data=json.dumps(payload).encode(), method="POST",
                                         headers={"X-N8N-API-KEY": os.environ["N8N_API_KEY"],
                                                  "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.build_opener(NoRedirect).open(request, timeout=20) as response:
                post_status = response.status
                created = json.loads(response.read(1_000_000))
                post_active = created.get("active")
        except urllib.error.HTTPError as error:
            post_status = error.code
        except Exception:
            post_status = "incierto_conciliar_GET"
        matches = lookup(workflow["name"])
    if len(matches) != 1:
        write_once(folder / "importacion-bloqueada.json", {"post_http": post_status,
                   "coincidencias": len(matches), "accion": "Conservar JSON. Conciliar por nombre antes de cualquier POST"})
        raise ValueError("Creación no confirmada. No repetir POST")
    workflow_id = matches[0].get("id", "")
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", workflow_id) or workflow_id in WORKFLOWS:
        raise ValueError("ID remoto rechazado")
    remote, status = get_json("/api/v1/workflows/" + workflow_id + "?excludePinnedData=true")
    after = originals()
    same_nodes = remote is not None and len(remote.get("nodes", [])) == len(workflow["nodes"]) and all(
        all(actual.get(key) == value for key, value in expected.items())
        for expected, actual in zip(workflow["nodes"], remote["nodes"]))
    receipt = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "id": workflow_id,
               "nombre": workflow["name"], "local_active_antes": workflow["active"],
               "post_http": post_status, "post_active": post_active, "get_http": status,
               "remote_active_despues": (remote or {}).get("active"),
               "remote_active_version_presente": bool((remote or {}).get("activeVersionId")),
               "nodos_coinciden": same_nodes,
               "conexiones_coinciden": (remote or {}).get("connections") == workflow["connections"],
               "ajustes_coinciden": all((remote or {}).get("settings", {}).get(key) == value
                                         for key, value in workflow["settings"].items()),
               "originales_antes": before, "originales_despues": after, "originales_sin_cambios": before == after,
               "ejecutado_en_n8n": False}
    write_once(receipt_path, receipt)
    if (remote is None or remote.get("active") is not False or remote.get("activeVersionId") or before != after
            or not same_nodes or not receipt["conexiones_coinciden"] or not receipt["ajustes_coinciden"]):
        raise ValueError("Comprobación remota requiere revisión. Leer recibo saneado")
    print(json.dumps({"resultado": "importado_inactivo", "id": workflow_id, "active": False,
                      "originales_sin_cambios": True}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Sólo errores propios constantes pueden salir. Los detalles HTTP nunca.
        print(json.dumps({"resultado": "requiere_revision", "tipo": type(error).__name__}))
        raise SystemExit(1)

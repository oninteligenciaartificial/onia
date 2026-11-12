"""Cotejo de lectura acotado. Imprime sólo campos permitidos y agregados."""

from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

HOST = "https://n8n-sergio-n8n.hqdqgh.easypanel.host"


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


def consultar(ruta, clave=None):
    headers = {"Accept": "application/json"}
    if clave:
        headers["X-N8N-API-KEY"] = clave
    row = {"ruta": ruta, "metodo": "GET", "clave_disponible": bool(clave)}
    request = urllib.request.Request(HOST + ruta, headers=headers, method="GET")
    try:
        with urllib.request.build_opener(SinRedireccion()).open(request, timeout=15) as response:
            row["http"] = response.status
            raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                row["bloqueo"] = "RESPUESTA_EXCESIVA"
                return row
            data = json.loads(raw)
            if ruta == "/rest/settings":
                settings = data.get("data", {})
                version = settings.get("versionCli")
                row["version"] = version if isinstance(version, str) and re.fullmatch(
                    r"\d+\.\d+\.\d+", version) else None
                mode = settings.get("executionMode")
                row["modo_ejecucion"] = mode if mode in ("regular", "queue") else None
                blocked = settings.get("blockEnvAccessInNode")
                row["env_bloqueado"] = blocked if isinstance(blocked, bool) else None
            elif ruta.startswith("/api/v1/workflows"):
                rows = data.get("data")
                if isinstance(rows, list):
                    row["workflows_en_pagina"] = len(rows)
                    row["activos_en_pagina"] = sum(w.get("active") is True for w in rows)
            elif ruta == "/api/v1/discover":
                # Un 200 acredita lectura de discovery. El cuerpo puede incluir activos
                # privados y no se conserva ni se interpreta como permiso de escritura.
                row["discovery_leido"] = True
    except urllib.error.HTTPError as error:
        row["http"] = error.code
        error.close()
    except (OSError, ValueError, AttributeError, TypeError):
        row["bloqueo"] = "CONEXION_O_FORMATO_NO_CONFIRMADO"
    return row


def main():
    key = os.environ.get("N8N_API_KEY")
    if key == "REPLACE_IN_SECRET_STORE":
        key = None
    rows = []
    unreadable = 0
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            comm = (proc / "comm").read_text().strip()
            if comm not in ("node", "n8n"):
                continue
            args = (proc / "cmdline").read_bytes().split(b"\0")
            if not any(re.search(rb"(?:^|/)n8n(?:/bin/n8n)?$", arg) for arg in args[:3]):
                continue
            rows.append({"namespace_igual": os.readlink(proc / "ns/net")
                         == os.readlink("/proc/self/ns/net")})
        except OSError:
            unreadable += 1
    status = Path("/proc/self/status").read_text()
    capabilities = int(re.search(r"^CapEff:\s+([0-9a-f]+)$", status, re.M)[1], 16)
    receipt = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "api_key_disponible": bool(key),
        "procesos_n8n_visibles": rows,
        "procesos_no_inspeccionables": unreadable,
        "cap_sys_admin": bool(capabilities & (1 << 21)),
        "cap_sys_ptrace": bool(capabilities & (1 << 19)),
        "consultas": [consultar("/healthz"), consultar("/rest/settings"),
                      consultar("/api/v1/workflows?limit=1&excludePinnedData=true", key),
                      consultar("/api/v1/discover", key)],
        "version_actual_confirmada": None,
        "ruta_privada_confirmada": False,
        "modificaciones_remotas": 0,
    }
    receipt["version_actual_confirmada"] = receipt["consultas"][1].get("version")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

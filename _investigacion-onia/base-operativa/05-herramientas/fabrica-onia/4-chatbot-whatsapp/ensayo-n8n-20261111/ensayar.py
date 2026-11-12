"""Ensayo CLI aislado: una ejecución manual, transporte apagado y datos ficticios."""

import argparse
from datetime import datetime, timezone
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import select
import signal
import socket
import sqlite3
import subprocess
import sys
import tempfile
import threading

CARPETA = Path(__file__).resolve().parent
PRODUCTO = CARPETA.parent / "trabajos/fabrica-chatbot-whatsapp-20261110"
TOKEN = "fixture-dispatch-token-no-real"
CRED_ID = "OniaWaCredFic001"
FLOW_ID = "OniaWaEnsayo2026"


def escribir(path, valor):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(valor, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def disponible(puerto):
    try:
        with socket.create_connection(("127.0.0.1", puerto), timeout=0.2):
            return True
    except OSError:
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--node-bin", type=Path, required=True)
    parser.add_argument("--n8n", type=Path, required=True)
    parser.add_argument("--referencia", type=Path, required=True,
                        help="Carpeta ensayo-vps-20261111 ya cotejada con 241f49a")
    parser.add_argument("--evidencia", type=Path, required=True,
                        help="Directorio nuevo; nunca sobrescribe un intento")
    args = parser.parse_args()
    os.umask(0o077)
    args.evidencia.mkdir(mode=0o700)
    recibo = {"fecha_utc": datetime.now(timezone.utc).isoformat(),
              "resultado": "pendiente", "ejecuciones_manuales": 0,
              "comandos": [], "peticiones": [], "procesos": [],
              "envios_habilitados": False, "secretos_reales": False,
              "n8n_produccion": False, "meta_invocada": False}
    source = PRODUCTO / "workflow-despacho-n8n.json"
    recibo["workflow_fuente_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    procesos = []
    puertos = []
    adapter = None
    bridge = None
    thread = None
    temporal_path = None

    def sanear(texto):
        texto = re.sub(r"\x1b\[[0-9;]*m", "", texto)
        texto = re.sub(r'("resumeToken"\s*:\s*")[^"]+(")',
                       r'\1<token-efimero-retirado>\2', texto)
        texto = re.sub(r'/tmp/onia-n8n-ensayo-[^/\s"\\]+', "<runtime-temporal>", texto)
        for original, sustituto in ((TOKEN, "<credencial-ficticia>"),
                                    (str(args.node_bin), "<node-bin>"),
                                    (str(args.n8n), "<n8n>"),
                                    (str(args.referencia), "<referencia>"),
                                    (str(CARPETA), "<entrega>")):
            texto = texto.replace(original, sustituto)
        if temporal_path:
            texto = texto.replace(str(temporal_path), "<temporal>")
        return texto

    def cli(env, nombre, *argv, permitidos=(0,)):
        proceso = subprocess.Popen([str(args.n8n), *argv], env=env, cwd=temporal_path,
                                   stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True, start_new_session=True)
        procesos.append((nombre, proceso))
        try:
            salida, _ = proceso.communicate(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(proceso.pid, signal.SIGTERM)
            try:
                salida, _ = proceso.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(proceso.pid, signal.SIGKILL)
                salida, _ = proceso.communicate(timeout=5)
            (args.evidencia / (nombre + ".log")).write_text(sanear(salida))
            raise RuntimeError(nombre + ": timeout; no reintentar ejecución") from None
        (args.evidencia / (nombre + ".log")).write_text(sanear(salida))
        recibo["comandos"].append({"nombre": nombre, "argv": [sanear(a) for a in argv],
                                    "rc": proceso.returncode})
        if proceso.returncode not in permitidos:
            raise RuntimeError(nombre + ": rc=" + str(proceso.returncode))
        return salida, proceso.returncode

    try:
        with tempfile.TemporaryDirectory(prefix="onia-n8n-db-", dir="/tmp") as tmp:
            temporal_path = Path(tmp)
            home = temporal_path / "home"
            home.mkdir(mode=0o700)
            env = {"HOME": str(home), "PATH": str(args.node_bin) + ":/usr/bin:/bin",
                   "LANG": "C.UTF-8", "N8N_USER_FOLDER": str(temporal_path / "user"),
                   "N8N_LISTEN_ADDRESS": "127.0.0.1", "DB_TYPE": "sqlite",
                   "N8N_DIAGNOSTICS_ENABLED": "false",
                   "N8N_VERSION_NOTIFICATIONS_ENABLED": "false",
                   "N8N_TEMPLATES_ENABLED": "false", "N8N_RUNNERS_ENABLED": "false",
                   "N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS": "true"}
            try:
                node = subprocess.check_output([str(args.node_bin / "node"), "--version"],
                                               env=env, text=True, timeout=10).strip()
                recibo["node"] = node
                version, _ = cli(env, "version", "--version")
                recibo["n8n"] = version.strip()
                assert version.strip() == "2.43.7", "Versión n8n distinta de la ensayada"
                for comando in ("import:credentials", "import:workflow", "execute"):
                    cli(env, "ayuda-" + comando.replace(":", "-"), comando, "--help")

                sys.path.insert(0, str(args.referencia))
                from fixture import escribir as fixture
                workspace = temporal_path / "adaptador"
                workspace.mkdir(mode=0o700)
                config = fixture(workspace)
                adapter = subprocess.Popen(
                    [sys.executable, "-B", str(args.referencia / "arrancar.py"),
                     "--config", str(config), "--puerto", "0", "--reloj-ficticio"],
                    env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}, cwd=temporal_path,
                    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True)
                procesos.append(("adaptador", adapter))
                assert select.select([adapter.stdout], [], [], 5)[0], "Adaptador sin anuncio"
                ready = json.loads(adapter.stdout.readline())
                assert ready["host"] == "127.0.0.1" and ready["envios_habilitados"] is False
                puertos.append(ready["puerto"])
                recibo["adaptador_inicio"] = ready

                class Puente(BaseHTTPRequestHandler):
                    def log_message(self, *_):
                        pass

                    def do_POST(self):
                        caso = {"metodo": "POST", "ruta": self.path,
                                "credencial_ficticia_correcta": self.headers.get("Authorization") == "Bearer " + TOKEN,
                                "cuerpo_vacio": self.headers.get("Content-Length", "0") == "0",
                                "destino_loopback": True}
                        recibo["peticiones"].append(caso)
                        # Una segunda petición se registra pero nunca llega al adaptador.
                        if (len(recibo["peticiones"]) != 1 or self.path != "/operador/despachar"
                                or not caso["credencial_ficticia_correcta"] or not caso["cuerpo_vacio"]):
                            caso["http"] = 403
                            self.send_error(403)
                            return
                        conn = http.client.HTTPConnection("127.0.0.1", ready["puerto"], timeout=5)
                        try:
                            conn.request("POST", self.path, body=b"",
                                         headers={"Authorization": "Bearer " + TOKEN})
                            response = conn.getresponse()
                            body = response.read()
                            caso.update(http=response.status, respuesta=json.loads(body))
                            self.send_response(response.status)
                            self.send_header("Content-Type", "application/json")
                            self.send_header("Content-Length", str(len(body)))
                            self.end_headers()
                            self.wfile.write(body)
                        finally:
                            conn.close()

                bridge = ThreadingHTTPServer(("127.0.0.1", 0), Puente)
                puertos.append(bridge.server_port)
                thread = threading.Thread(target=bridge.serve_forever)
                thread.start()
                workflow = json.loads(source.read_text())
                assert workflow["active"] is False and len(workflow["nodes"]) == 2
                workflow["id"] = FLOW_ID
                request = workflow["nodes"][1]
                assert request["typeVersion"] == 4.2 and request["retryOnFail"] is False
                # URL explícita en la copia: no se habilita acceso a $env en n8n 2.x.
                request["parameters"]["url"] = f"http://127.0.0.1:{bridge.server_port}/operador/despachar"
                request["credentials"] = {"httpHeaderAuth": {"id": CRED_ID, "name": "Credencial ficticia OnIA"}}
                escribir(temporal_path / "workflow.json", [workflow])
                escribir(args.evidencia / "workflow-copia.json", [workflow])
                escribir(temporal_path / "credencial.json", [{"id": CRED_ID,
                         "name": "Credencial ficticia OnIA", "type": "httpHeaderAuth",
                         "data": {"name": "Authorization", "value": "Bearer " + TOKEN}}])
                cli(env, "importar-credencial", "import:credentials", "--input=" + str(temporal_path / "credencial.json"))
                cli(env, "importar-workflow", "import:workflow", "--input=" + str(temporal_path / "workflow.json"))
                db_path = temporal_path / "user/.n8n/database.sqlite"

                def inspeccionar():
                    with sqlite3.connect(db_path.as_uri() + "?mode=ro", uri=True) as db:
                        fila = db.execute("SELECT active, activeVersionId FROM workflow_entity WHERE id=?", (FLOW_ID,)).fetchone()
                        workflows = db.execute("SELECT count(*) FROM workflow_entity").fetchone()[0]
                        cred = db.execute("SELECT type, data FROM credentials_entity WHERE id=?", (CRED_ID,)).fetchone()
                        return {"active": fila[0], "activeVersionId": fila[1],
                                "total_workflows": workflows, "credencial_tipo": cred[0],
                                "credencial_cifrada": TOKEN not in cred[1] and bool(cred[1])}

                recibo["sqlite_antes"] = inspeccionar()
                assert recibo["sqlite_antes"] == {"active": 0, "activeVersionId": None,
                    "total_workflows": 1, "credencial_tipo": "httpHeaderAuth", "credencial_cifrada": True}
                recibo["ejecuciones_manuales"] += 1
                _, rc = cli(env, "ejecutar-workflow", "execute", "--id=" + FLOW_ID, permitidos=(0, 1))
                recibo["ejecucion_rc"] = rc
                recibo["sqlite_despues"] = inspeccionar()
                assert recibo["sqlite_antes"] == recibo["sqlite_despues"]
                assert len(recibo["peticiones"]) == 1, "Se esperaba un único POST"
                caso = recibo["peticiones"][0]
                assert caso["http"] == 409 and caso["respuesta"] == {"error": "ENVIOS_DESHABILITADOS"}
                assert caso["credencial_ficticia_correcta"] and caso["cuerpo_vacio"]
                assert rc == 1, "HTTP Request debe informar el 409 como error"
                with sqlite3.connect((workspace / "chatbot.sqlite3").as_uri() + "?mode=ro", uri=True) as db:
                    recibo["salidas_aceptadas_o_inciertas"] = db.execute(
                        "SELECT count(*) FROM salida WHERE estado IN ('aceptado','incierto')").fetchone()[0]
                assert recibo["salidas_aceptadas_o_inciertas"] == 0
                recibo["resultado"] = "correcto"
            finally:
                if bridge:
                    bridge.shutdown()
                    bridge.server_close()
                if thread:
                    thread.join(5)
                if adapter:
                    if adapter.poll() is None:
                        adapter.terminate()
                    try:
                        salida, _ = adapter.communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        adapter.kill()
                        salida, _ = adapter.communicate(timeout=5)
                    (args.evidencia / "adaptador.log").write_text(sanear(salida))
                    guardia = next(json.loads(line) for line in salida.splitlines() if '"detenido"' in line)
                    recibo["adaptador_cierre"] = guardia
                    assert guardia["conexiones_salientes_intentadas"] == guardia["transporte_invocado"] == 0
                recibo["procesos"] = [{"nombre": nombre, "pid": p.pid, "rc": p.poll()}
                                        for nombre, p in procesos]
                recibo["procesos_propios_vivos"] = sum(p.poll() is None for _, p in procesos)
                recibo["listeners_propios_abiertos"] = [p for p in puertos if disponible(p)]
                recibo["hilo_puente_vivo"] = thread.is_alive() if thread else False
                assert recibo["procesos_propios_vivos"] == 0
                assert not recibo["listeners_propios_abiertos"] and not recibo["hilo_puente_vivo"]
    except Exception as exc:
        recibo["resultado"] = "bloqueado"
        recibo["fallo"] = sanear(type(exc).__name__ + ": " + str(exc))
    recibo["temporal_db_eliminado"] = temporal_path is not None and not temporal_path.exists()
    escribir(args.evidencia / "recibo.json", recibo)
    print(json.dumps(recibo, ensure_ascii=False, indent=2))
    return 0 if recibo["resultado"] == "correcto" else 1


if __name__ == "__main__":
    sys.exit(main())

"""Regresión acotada de la preparación y del diagnóstico nuevos, con datos ficticios."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import select
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile
import threading

from preparar import CARPETA, FUENTE, SHA256_APROBADO, preparar

REFERENCIA = CARPETA.parent / "ensayo-vps-20261111"
sys.path.insert(0, str(REFERENCIA))
from fixture import CONFIG, AHORA, CLIENTE, escribir


def main():
    os.umask(0o077)
    receipt = {"fecha_utc": datetime.now(timezone.utc).isoformat(),
               "alcance": "simulado_loopback", "controles": [],
               "ejecuciones_n8n_nuevas": 0, "post_despacho": 0}
    process = None
    ports = []

    def check(name, condition):
        receipt["controles"].append({"nombre": name, "correcto": bool(condition)})
        if not condition:
            raise AssertionError(name)

    def diagnose(origin, allowed):
        env = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8",
               "ONIA_ORIGEN_PRIVADO": origin, "ONIA_ORIGEN_PERMITIDO": allowed}
        result = subprocess.run([shutil.which("node"), str(CARPETA / "diagnostico-runtime.cjs")],
                                env=env, capture_output=True, text=True, timeout=12)
        check("diagnostico_emite_json_saneado", result.returncode in (0, 2) and not result.stderr)
        return json.loads(result.stdout)

    try:
        check("fuente_aprobada_intacta", hashlib.sha256(FUENTE.read_bytes()).hexdigest() == SHA256_APROBADO)
        # Evalúa la expresión original con el motor JS. n8n no se inicia.
        js = """
const fs = require('node:fs');
const vm = require('node:vm');
const workflow = JSON.parse(fs.readFileSync(process.argv[1], 'utf8'));
const expression = workflow.nodes[1].parameters.url.slice(3, -2).trim();
const cases = [undefined, '', 'http://127.0.0.1:8765', 'http://127.0.0.1:8765/', 'http://127.0.0.1:8765///'];
console.log(JSON.stringify(cases.map(base => vm.runInNewContext(expression,
  {$env: {ONIA_CHATBOT_DISPATCH_BASE_URL: base}}))));
"""
        expression = subprocess.check_output([shutil.which("node"), "-e", js, str(FUENTE)],
                                             text=True, timeout=5)
        expected = ["", ""] + ["http://127.0.0.1:8765/operador/despachar"] * 3
        check("expresion_original_cinco_entradas", json.loads(expression) == expected)
        with tempfile.TemporaryDirectory(prefix="onia-ruta-n8n-", dir="/tmp") as tmp:
            root = Path(tmp)
            config = escribir(root)
            process = subprocess.Popen([sys.executable, "-B", str(REFERENCIA / "arrancar.py"),
                                        "--config", str(config), "--puerto", "0", "--reloj-ficticio"],
                                       env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"},
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True)
            check("arranque_acotado_disponible", bool(select.select([process.stdout], [], [], 5)[0]))
            ready = json.loads(process.stdout.readline())
            port = ready["puerto"]
            ports.append(port)
            origin = f"http://127.0.0.1:{port}"
            check("loopback_efimero_envios_apagados", ready["host"] == "127.0.0.1"
                  and ready["envios_habilitados"] is False and ready["reloj_ficticio"] is True)
            plan = {"origen_privado": origin, "origen_permitido": origin,
                    "credencial_dispatcher_id": "fixture-dispatcher-id",
                    "credencial_operador_id": "fixture-operator-id"}
            workflow = preparar(plan)
            original = json.loads(FUENTE.read_bytes())
            restored = deepcopy(workflow)
            restored["name"] = original["name"]
            restored["nodes"][1]["parameters"]["url"] = original["nodes"][1]["parameters"]["url"]
            del restored["nodes"][1]["credentials"]
            check("mismo_workflow_solo_nombre_url_referencia", restored == original)
            check("inactivo_sin_id_importable_ni_secretos", workflow["active"] is False
                  and "id" not in workflow and CONFIG["dispatcher_token"] not in json.dumps(workflow))
            private_plan = root / "plan.json"
            private_plan.write_text(json.dumps(plan))
            output = root / "workflow.json"
            cli = [sys.executable, "-B", str(CARPETA / "preparar.py"),
                   "--plan", str(private_plan), "--salida", str(output)]
            first = subprocess.run(cli, capture_output=True, timeout=5)
            check("copia_privada_0600", first.returncode == 0 and output.stat().st_mode & 0o777 == 0o600)
            second = subprocess.run(cli, capture_output=True, timeout=5)
            check("no_sobrescribe_copia", second.returncode == 2 and json.loads(output.read_text()) == workflow)
            for field, value in (("credencial_dispatcher_id", plan["credencial_operador_id"]),
                                 ("origen_permitido", "http://127.0.0.1:1"),
                                 ("origen_privado", "https://usuario:clave@localhost")):
                invalid = {**plan, field: value}
                if field == "origen_privado":
                    invalid["origen_permitido"] = value
                rejected = False
                try:
                    preparar(invalid)
                except ValueError:
                    rejected = True
                check("rechazo_" + field + "_" + str(len(receipt["controles"])), rejected)

            db_path = root / "chatbot.sqlite3"
            with sqlite3.connect(db_path) as db:
                db.execute("INSERT INTO clientes(telefono, ultimo) VALUES (?, ?)", (CLIENTE, AHORA))
                db.execute("INSERT INTO salida(telefono, tipo) VALUES (?, 'qr')", (CLIENTE,))

            def counters():
                with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as db:
                    return dict(db.execute("SELECT estado, COUNT(*) FROM salida GROUP BY estado"))

            before = counters()
            diagnosis = diagnose(origin, origin)
            receipt["diagnostico_simulado"] = diagnosis
            check("get_reconoce_adaptador", diagnosis.get("conectividad", {}).get("ruta_disponible") is True)
            check("no_atribuye_namespace_n8n_al_fixture", diagnosis["resultado"] == "bloqueado"
                  and not diagnosis["runtime"])
            mismatch = diagnose(origin, "http://127.0.0.1:1")
            check("diagnostico_rechaza_origen_no_permitido", mismatch.get("bloqueo") == "ORIGEN_SIN_PERMISO_EXACTO")
            public = diagnose("http://192.0.2.1:8765", "http://192.0.2.1:8765")
            check("diagnostico_rechaza_destino_no_privado", public.get("bloqueo") == "DESTINO_FUERA_DE_RED_PRIVADA")
            conn = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
            try:
                receipt["post_despacho"] += 1
                conn.request("POST", "/operador/despachar", body=b"",
                             headers={"Authorization": "Bearer " + CONFIG["dispatcher_token"]})
                response = conn.getresponse()
                check("unico_post_409_sin_envios", response.status == 409
                      and json.loads(response.read()) == {"error": "ENVIOS_DESHABILITADOS"})
            finally:
                conn.close()
            receipt["salidas_antes"] = before
            receipt["salidas_despues"] = counters()
            check("salida_pendiente_conservada", before == {"pendiente": 1}
                  and receipt["salidas_despues"] == before)
            process.terminate()
            stdout, stderr = process.communicate(timeout=5)
            closed = json.loads(stdout.strip())
            receipt["adaptador_cierre"] = closed
            check("cierre_sin_transporte_ni_egreso", process.returncode == 0 and not stderr
                  and closed["conexiones_salientes_intentadas"] == 0 and closed["transporte_invocado"] == 0)

            class Redirect(BaseHTTPRequestHandler):
                requests = 0

                def log_message(self, *args):
                    pass

                def do_GET(self):
                    Redirect.requests += 1
                    self.send_response(302)
                    self.send_header("Location", origin + "/operador/revisar")
                    self.send_header("Content-Length", "0")
                    self.end_headers()

            with HTTPServer(("127.0.0.1", 0), Redirect) as server:
                redirect_origin = f"http://127.0.0.1:{server.server_port}"
                ports.append(server.server_port)
                thread = threading.Thread(target=server.serve_forever)
                thread.start()
                try:
                    redirected = diagnose(redirect_origin, redirect_origin)
                    check("no_sigue_redireccion_operador", Redirect.requests == 1
                          and redirected["conectividad"]["http"] == 302
                          and redirected["conectividad"]["ruta_disponible"] is False)
                finally:
                    server.shutdown()
                    thread.join(timeout=5)
            receipt["temporal_eliminado"] = str(root)
        check("temporal_eliminado", not Path(receipt.pop("temporal_eliminado")).exists())
        for port in ports:
            with socket.socket() as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(("127.0.0.1", port))
        check("listeners_propios_cerrados", True)
        receipt["resultado"] = "correcto"
    except Exception as error:
        receipt["resultado"] = "fallido"
        receipt["fallo_tipo"] = type(error).__name__
    finally:
        if process is not None and process.poll() is None:
            process.terminate()
            try:
                process.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate(timeout=5)
        receipt["procesos_propios_vivos"] = int(process is not None and process.poll() is None)
        print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return receipt["resultado"] != "correcto"


if __name__ == "__main__":
    sys.exit(main())

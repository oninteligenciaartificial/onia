"""Ensayo ejecutable HTTP + proxy TLS temporal. Sólo datos ficticios y loopback."""

from datetime import datetime, timezone
import hashlib
import hmac
import http.client
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import ssl
import subprocess
import sys
import tempfile
import time

from comun import CARPETA, PRODUCTO, cargar_adaptador
from fixture import AHORA, CLIENTE, CONFIG, escribir

ENTORNO = {"PATH": os.defpath, "LANG": "C.UTF-8"}


class Ensayo:
    def __init__(self):
        self.pasos = []
        self.procesos = []
        self.archivos_log = []
        self.comandos = []

    def cotejar(self, nombre, esperado, observado):
        self.pasos.append({"caso": nombre, "esperado": esperado, "observado": observado})
        if esperado != observado:
            raise AssertionError(nombre)

    def lanzar(self, comando, raiz, nombre):
        log = raiz / (nombre + ".log")
        salida = log.open("w")
        self.archivos_log.append(salida)
        proceso = subprocess.Popen(comando, cwd=raiz, env=ENTORNO, stdin=subprocess.DEVNULL,
                                   stdout=salida, stderr=subprocess.STDOUT)
        self.procesos.append((nombre, proceso))
        self.comandos.append({"nombre": nombre,
                              "argv": [a.replace(str(raiz), "<temporal>").replace(str(CARPETA), "<entrega>") for a in comando]})
        return proceso, log

    def terminar(self, nombre, proceso):
        if proceso.poll() is None:
            proceso.terminate()
        try:
            codigo = proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proceso.kill()
            proceso.wait(timeout=5)
            raise AssertionError(nombre + " no terminó con SIGTERM") from None
        self.cotejar(nombre + " termina limpiamente", 0, codigo)

    def limpiar(self):
        for _, proceso in reversed(self.procesos):
            if proceso.poll() is None:
                proceso.terminate()
                try:
                    proceso.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proceso.kill()
                    proceso.wait(timeout=5)
        for archivo in self.archivos_log:
            archivo.close()

    def ejecutar(self, raiz):
        adaptador = cargar_adaptador()
        config = escribir(raiz)
        base = raiz / "chatbot.sqlite3"
        comando = [sys.executable, "-B", str(CARPETA / "arrancar.py"),
                   "--config", str(config), "--puerto", "0", "--reloj-ficticio"]
        proceso, log = self.lanzar(comando, raiz, "adaptador")
        inicio = esperar(lambda: json.loads(log.read_text().splitlines()[0])
                         if log.stat().st_size else None, proceso)
        self.cotejar("bind exclusivamente loopback", "127.0.0.1", inicio["host"])
        self.cotejar("bandera de envío deshabilitada", False, inicio["envios_habilitados"])
        puerto = inicio["puerto"]
        self.cotejar("permisos directorio/config/SQLite", [0o700, 0o600, 0o600],
                     [p.stat().st_mode & 0o777 for p in (raiz, config, base)])

        def sql(consulta):
            with sqlite3.connect(base) as db:
                return [list(fila) for fila in db.execute(consulta)]

        def mensaje(id_, texto="NEGOCIO", **otros):
            return {"id": "wamid." + id_, "from": CLIENTE, "timestamp": str(AHORA),
                    "type": "text", "text": {"body": texto}, **otros}

        def lote(*mensajes, numero="000"):
            return json.dumps({"object": "whatsapp_business_account", "entry": [{"changes": [{
                "field": "messages", "value": {"messaging_product": "whatsapp",
                "metadata": {"phone_number_id": numero}, "messages": mensajes}}]}]},
                ensure_ascii=False, indent=2).encode("utf-8")

        def firma(raw):
            return "sha256=" + hmac.new(CONFIG["app_secret"].encode(), raw, hashlib.sha256).hexdigest()

        def meta(raw, port=puerto, contexto=None, firma_alternativa=None):
            return pedir(port, "POST", "/meta", raw,
                         {"X-Hub-Signature-256": firma_alternativa or firma(raw)}, contexto)

        operador = {"Authorization": "Bearer " + CONFIG["operator_token"]}
        dispatcher = {"Authorization": "Bearer " + CONFIG["dispatcher_token"]}
        challenge = "/meta?hub.mode=subscribe&hub.verify_token=" + CONFIG["verify_token"] + "&hub.challenge=00123"
        self.cotejar("challenge exacto con ceros", [200, "00123"], pedir(puerto, "GET", challenge))
        self.cotejar("token incorrecto", 403, pedir(puerto, "GET", challenge.replace("fixture-verify", "fixture-otro"))[0])
        self.cotejar("challenge repetido", 403, pedir(puerto, "GET", challenge + "&hub.challenge=9")[0])

        raw = lote(mensaje("interes", "NEGOCIO"), mensaje("unicode", "AYUDA", nota="inscripción ficticia"))
        self.cotejar("HMAC de bytes con espacios y UTF-8", [200, {"nuevos": 2}], meta(raw))
        self.cotejar("entrada repetida", [200, {"nuevos": 0}], meta(raw))
        self.cotejar("reeserializar con firma anterior se rechaza", [403, {"error": "FIRMA_RECHAZADA"}],
                     meta(json.dumps(json.loads(raw)).encode(), firma_alternativa=firma(raw)))
        self.cotejar("firma ausente", 403, pedir(puerto, "POST", "/meta", raw)[0])
        self.cotejar("JSON inválido aun con HMAC válida", 400, meta(b"{invalido")[0])
        self.cotejar("lote mixto no se escribe parcialmente", 400,
                     meta(lote(mensaje("no-guardar"), {"id": "invalido"}))[0])
        self.cotejar("phone_number_id ajeno", 403, meta(lote(mensaje("ajeno"), numero="999"))[0])
        self.cotejar("rechazos no agregan vistos", [[2]], sql("SELECT count(*) FROM vistos"))
        self.cotejar("info encolada una sola vez", [[1]], sql("SELECT count(*) FROM salida WHERE tipo='informacion'"))
        self.cotejar("inscripción GRUPAL", [200, {"nuevos": 1}], meta(lote(mensaje("grupal", "GRUPAL"))))
        self.cotejar("estado pendiente", [["pendiente", "grupal"]], sql("SELECT estado, plan FROM clientes"))
        self.cotejar("QR encolado único", [[1]], sql("SELECT count(*) FROM salida WHERE tipo='qr'"))
        payload_qr = adaptador.payload_salida(CONFIG, {"tipo": "qr", "plan": "grupal", "telefono": CLIENTE})
        self.cotejar("QR simulado renderizado por adaptador", ["image", "000001"],
                     [payload_qr["type"], payload_qr["image"]["id"]])
        self.cotejar("captura recibida", [200, {"nuevos": 1}],
                     meta(lote(mensaje("captura", type="image", image={"id": "000002"}))))
        self.cotejar("captura conserva pendiente", [["pendiente", "COMPROBANTE_NO_VERIFICADO"]],
                     sql("SELECT estado, revision FROM clientes"))
        self.cotejar("captura no genera acceso", [[0]], sql("SELECT count(*) FROM salida WHERE tipo='confirmado'"))
        self.cotejar("operador sin autenticación", 401, pedir(puerto, "GET", "/operador/revisar")[0])
        self.cotejar("dispatcher no revisa pagos", 401,
                     pedir(puerto, "GET", "/operador/revisar", headers=dispatcher)[0])
        revision = pedir(puerto, "GET", "/operador/revisar", headers=operador)
        self.cotejar("bandeja privada autenticada", [200, "COMPROBANTE_NO_VERIFICADO"],
                     [revision[0], revision[1]["revision"][0]["revision"]])
        pago = {"telefono": CLIENTE, "decision": "confirmar", "referencia": "FICTICIO-001",
                "importe": 50, "moneda": "BOB", "movimientoVerificado": True, "destinoVerificado": True}
        pago_raw = json.dumps(pago).encode()
        self.cotejar("dispatcher no confirma", 401,
                     pedir(puerto, "POST", "/operador/confirmar", pago_raw, dispatcher)[0])
        self.cotejar("conciliación incompleta", [409, {"resultado": "CONCILIACION_INCOMPLETA"}],
                     pedir(puerto, "POST", "/operador/confirmar",
                           json.dumps({**pago, "movimientoVerificado": False}).encode(), operador))
        self.cotejar("confirmación manual simulada", [200, {"resultado": "confirmado"}],
                     pedir(puerto, "POST", "/operador/confirmar", pago_raw, operador))
        self.cotejar("confirmación repetida", [200, {"resultado": "ya_confirmado"}],
                     pedir(puerto, "POST", "/operador/confirmar", pago_raw, operador))
        self.cotejar("acceso encolado único", [[1]], sql("SELECT count(*) FROM salida WHERE tipo='confirmado'"))
        acceso = adaptador.payload_salida(CONFIG, {"tipo": "confirmado", "plan": "grupal", "telefono": CLIENTE})
        self.cotejar("acceso renderizado con tres enlaces ficticios", 3,
                     sum(url in acceso["text"]["body"] for url in CONFIG["meet_urls"]))
        for nombre, headers in (("sin credencial", {}), ("operador", operador), ("dispatcher", dispatcher)):
            self.cotejar("despacho rechazado: " + nombre, [409, {"error": "ENVIOS_DESHABILITADOS"}],
                         pedir(puerto, "POST", "/operador/despachar", headers=headers))
        self.cotejar("ninguna salida aceptada ni incierta", [[0]],
                     sql("SELECT count(*) FROM salida WHERE estado IN ('aceptado','incierto')"))

        # Reinicio del mismo arranque y SQLite: deduplicación persiste por HTTP.
        self.terminar("adaptador primer proceso", proceso)
        guardia1 = json.loads(log.read_text().splitlines()[-1])
        self.cotejar("guardia de egreso primer proceso", [0, 0],
                     [guardia1["conexiones_salientes_intentadas"], guardia1["transporte_invocado"]])
        proceso, log2 = self.lanzar(comando, raiz, "adaptador-retoma")
        inicio2 = esperar(lambda: json.loads(log2.read_text().splitlines()[0])
                          if log2.stat().st_size else None, proceso)
        puerto = inicio2["puerto"]
        self.cotejar("duplicado tras reinicio", [200, {"nuevos": 0}], meta(raw, port=puerto))
        self.cotejar("acceso único tras reinicio", [[1]], sql("SELECT count(*) FROM salida WHERE tipo='confirmado'"))

        # Se usa el bloque HTTPS propuesto sin cambiar sus locations ni proxy_pass.
        nginx = shutil.which("nginx")
        openssl = shutil.which("openssl")
        if not nginx or not openssl:
            raise RuntimeError("Se requieren nginx y openssl ya instalados; no se instalan")
        certificado, clave = raiz / "fixture.crt", raiz / "fixture.key"
        comando_tls = [openssl, "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
                       "-keyout", str(clave), "-out", str(certificado), "-subj", "/CN=ensayo.invalid",
                       "-addext", "subjectAltName=IP:127.0.0.1,DNS:ensayo.invalid"]
        resultado_tls = subprocess.run(comando_tls, cwd=raiz, env=ENTORNO,
                                       capture_output=True, timeout=15, text=True)
        self.comandos.append({"nombre": "certificado_ficticio",
                              "argv": [a.replace(str(raiz), "<temporal>") for a in comando_tls],
                              "rc": resultado_tls.returncode,
                              "stdout": resultado_tls.stdout, "stderr": resultado_tls.stderr})
        self.cotejar("creación de certificado ficticio", 0, resultado_tls.returncode)
        puerto_tls = puerto_libre()
        plantilla = (CARPETA / "meta.nginx.conf.in").read_text()
        for clave_, valor in {"LISTEN": f"127.0.0.1:{puerto_tls}", "SERVER_NAME": "ensayo.invalid",
                              "TLS_CERT": str(certificado), "TLS_KEY": str(clave),
                              "ADAPTER_PORT": str(puerto)}.items():
            plantilla = plantilla.replace("@" + clave_ + "@", valor)
        nginx_conf = raiz / "nginx.conf"
        nginx_conf.write_text("daemon off;\nmaster_process off;\nworker_processes 1;\n"
                              f"pid {raiz}/nginx.pid;\nerror_log stderr crit;\nevents {{}}\nhttp {{\n"
                              f"client_body_temp_path {raiz}/body;\nproxy_temp_path {raiz}/proxy;\n"
                              + plantilla + "\n}\n")
        prefijo = [nginx, "-p", str(raiz) + "/", "-c", str(nginx_conf), "-e", "stderr"]
        validacion = subprocess.run([*prefijo, "-t"], env=ENTORNO, cwd=raiz,
                                    capture_output=True, timeout=5, text=True)
        self.comandos.append({"nombre": "nginx_sintaxis",
                              "argv": [a.replace(str(raiz), "<temporal>") for a in [*prefijo, "-t"]],
                              "rc": validacion.returncode,
                              "stdout": validacion.stdout.replace(str(raiz), "<temporal>"),
                              "stderr": validacion.stderr.replace(str(raiz), "<temporal>")})
        self.cotejar("nginx -t del archivo propio", 0, validacion.returncode)
        proxy, proxy_log = self.lanzar(prefijo, raiz, "nginx")
        contexto = ssl.create_default_context(cafile=str(certificado))
        esperar(lambda: disponible(puerto_tls), proxy)
        self.cotejar("challenge por TLS con certificado verificado", [200, "00123"],
                     pedir(puerto_tls, "GET", challenge, contexto=contexto))
        raw_tls = lote(mensaje("proxy", "AYUDA", nota="firma sobre bytes: inscripción"))
        self.cotejar("HMAC de bytes conservados por nginx", [200, {"nuevos": 1}],
                     meta(raw_tls, port=puerto_tls, contexto=contexto))
        self.cotejar("replay por proxy", [200, {"nuevos": 0}],
                     meta(raw_tls, port=puerto_tls, contexto=contexto))
        self.cotejar("bytes alterados por proxy se rechazan", 403,
                     meta(raw_tls + b" ", port=puerto_tls, contexto=contexto,
                          firma_alternativa=firma(raw_tls))[0])
        self.cotejar("proxy rechaza PUT", 405,
                     pedir(puerto_tls, "PUT", "/meta", contexto=contexto)[0])
        rutas = ["/operador/revisar", "/operador/confirmar", "/operador/despachar",
                 "/meta/../operador/revisar", "/meta%2f..%2foperador%2frevisar",
                 "//operador/revisar", "/meta/operador/revisar", "/meta/", "/"]
        for ruta in rutas:
            self.cotejar("proxy aísla " + ruta, 404,
                         pedir(puerto_tls, "GET", ruta, headers=operador, contexto=contexto)[0])
        for ruta, cuerpo, headers in (("/operador/confirmar", pago_raw, operador),
                                     ("/operador/despachar", b"", dispatcher)):
            self.cotejar("proxy bloquea POST " + ruta, 404,
                         pedir(puerto_tls, "POST", ruta, cuerpo, headers, contexto)[0])
        self.cotejar("operador sigue disponible sólo por origen privado", 200,
                     pedir(puerto, "GET", "/operador/revisar", headers=operador)[0])

        # Contrato del workflow ya existente; no se crea otro ni se llama a n8n.
        workflow = json.loads((PRODUCTO / "workflow-despacho-n8n.json").read_text())
        nodo = workflow["nodes"][1]
        self.cotejar("workflow inactivo", False, workflow["active"])
        self.cotejar("sólo trigger manual y HTTP Request", ["n8n-nodes-base.manualTrigger", "n8n-nodes-base.httpRequest"],
                     [n["type"] for n in workflow["nodes"]])
        self.cotejar("despacho POST sin cuerpo ni reintento", ["POST", False, False],
                     [nodo["parameters"]["method"], nodo["parameters"]["sendBody"], nodo["retryOnFail"]])
        self.cotejar("sin redirecciones", False,
                     nodo["parameters"]["options"]["redirect"]["redirect"]["followRedirects"])
        self.cotejar("credenciales sin vincular", False, any("credentials" in n for n in workflow["nodes"]))
        self.cotejar("origen privado parametrizado", True,
                     "ONIA_CHATBOT_DISPATCH_BASE_URL" in nodo["parameters"]["url"])
        self.cotejar("no guarda ejecuciones manuales", False, workflow["settings"]["saveManualExecutions"])

        self.terminar("nginx temporal", proxy)
        self.terminar("adaptador retoma", proceso)
        guardia2 = json.loads(log2.read_text().splitlines()[-1])
        self.cotejar("guardia de egreso retoma", [0, 0],
                     [guardia2["conexiones_salientes_intentadas"], guardia2["transporte_invocado"]])
        for nombre, archivo_log in (("adaptador", log), ("adaptador-retoma", log2), ("nginx", proxy_log)):
            self.comandos.append({"nombre": nombre + "_salida", "stdout_stderr": archivo_log.read_text()})
        self.cotejar("ninguna credencial en logs", False,
                     any(CONFIG[k] in p.read_text() for k in ("app_secret", "operator_token", "verify_token", "dispatcher_token")
                         for p in (log, log2, proxy_log)))
        self.cotejar("ningún listener propio queda abierto", [False, False],
                     [disponible(puerto), disponible(puerto_tls)])

        # El lanzador no acepta habilitar envíos ni usar un reloj ficticio con datos ajenos.
        for nombre, cfg in (("envíos habilitados", {**CONFIG, "envios_habilitados": True}),
                            ("reloj con config distinta", {**CONFIG, "phone_number_id": "111"})):
            config.write_text(json.dumps(cfg))
            resultado = subprocess.run(comando, cwd=raiz, env=ENTORNO, capture_output=True, timeout=5)
            self.cotejar("rechazo de arranque: " + nombre, 2, resultado.returncode)
        config.write_text(json.dumps(CONFIG))
        resultado = subprocess.run([*comando, "--permitir-envios"], cwd=raiz, env=ENTORNO,
                                   capture_output=True, timeout=5)
        self.cotejar("flag de envío inexistente", 2, resultado.returncode)


def pedir(puerto, metodo, ruta, cuerpo=b"", headers=None, contexto=None):
    if contexto:
        conn = http.client.HTTPSConnection("127.0.0.1", puerto, timeout=3, context=contexto)
    else:
        conn = http.client.HTTPConnection("127.0.0.1", puerto, timeout=3)
    try:
        conn.request(metodo, ruta, body=cuerpo, headers={"Content-Type": "application/json", **(headers or {})})
        respuesta = conn.getresponse()
        raw = respuesta.read()
        return [respuesta.status, json.loads(raw) if respuesta.getheader("Content-Type", "").startswith("application/json") else raw.decode()]
    finally:
        conn.close()


def puerto_libre():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def disponible(puerto):
    try:
        with socket.create_connection(("127.0.0.1", puerto), timeout=0.2):
            return True
    except OSError:
        return False


def esperar(condicion, proceso):
    limite = time.monotonic() + 5
    while time.monotonic() < limite:
        if proceso.poll() is not None:
            raise RuntimeError("Proceso temporal terminó antes de estar listo")
        valor = condicion()
        if valor:
            return valor
        time.sleep(0.025)
    raise TimeoutError("Arranque temporal no disponible en cinco segundos")


def main():
    os.umask(0o077)
    ensayo = Ensayo()
    recibo = {"fecha_utc": datetime.now(timezone.utc).isoformat(), "modo": "HTTP_loopback_y_TLS_nginx_temporal",
              "python": sys.version.split()[0], "n8n_invocado": False,
              "graph_invocado": False, "envios_reales": 0, "pagos_reales": 0,
              "reloj_ficticio": AHORA, "casos": ensayo.pasos, "comandos_internos": ensayo.comandos}
    try:
        with tempfile.TemporaryDirectory(prefix="onia-whatsapp-http-", dir="/tmp") as temporal:
            try:
                ensayo.ejecutar(Path(temporal))
            finally:
                ensayo.limpiar()
        recibo["resultado"] = "correcto"
    except Exception as exc:
        recibo["resultado"] = "fallo"
        recibo["fallo"] = str(exc)
    recibo["procesos_propios_vivos"] = sum(p.poll() is None for _, p in ensayo.procesos)
    recibo["total_casos"] = len(ensayo.pasos)
    recibo["sha256_fuentes_reutilizadas"] = {
        nombre: hashlib.sha256((PRODUCTO / nombre).read_bytes()).hexdigest()
        for nombre in ("adaptador.py", "motor.cjs", "mensajes.json", "workflow-despacho-n8n.json")}
    print(json.dumps(recibo, ensure_ascii=False, indent=2))
    return 0 if recibo["resultado"] == "correcto" else 1


if __name__ == "__main__":
    sys.exit(main())

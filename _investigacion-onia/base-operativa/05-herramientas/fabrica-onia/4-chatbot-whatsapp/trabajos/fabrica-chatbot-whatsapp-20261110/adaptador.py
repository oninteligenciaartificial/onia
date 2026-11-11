"""Webhook y registro privado de un workshop. Python 3.10+, biblioteca estándar."""

import argparse
from contextlib import contextmanager
from datetime import datetime
import hashlib
import hmac
import http.client
from ipaddress import IPv4Address
import json
import os
from pathlib import Path
import re
from socket import INADDR_LOOPBACK
import sqlite3
import stat
import time
from urllib.parse import parse_qs
from wsgiref.simple_server import WSGIRequestHandler, make_server


CATALOGO = json.loads(Path(__file__).with_name("mensajes.json").read_text(encoding="utf-8"))
OFERTA = CATALOGO["oferta"]
VENTANA = 24 * 60 * 60
MAX_BODY = 256 * 1024
TELEFONO = r"[1-9][0-9]{7,14}"
META_ID = r"[0-9]{1,32}"
WAMID = r"wamid\.[A-Za-z0-9_=.\-/+]{1,500}"
REFERENCIA = r"[A-Z0-9][A-Z0-9._/-]{0,79}"
COMANDOS = {"NEGOCIO": "interes", "GRUPAL": "grupal", "VIP": "vip",
            "AYUDA": "ayuda", "BAJA": "baja"}

ESQUEMA = """
CREATE TABLE IF NOT EXISTS cuenta (id INTEGER PRIMARY KEY CHECK(id = 1), numero TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS clientes (
    telefono TEXT PRIMARY KEY,
    ultimo INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'interesado',
    plan TEXT,
    vence INTEGER,
    referencia TEXT UNIQUE,
    cese INTEGER NOT NULL DEFAULT 0,
    revision TEXT
);
CREATE TABLE IF NOT EXISTS vistos (id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS salida (
    id INTEGER PRIMARY KEY,
    telefono TEXT NOT NULL REFERENCES clientes(telefono),
    tipo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    meta_id TEXT UNIQUE
);
CREATE INDEX IF NOT EXISTS salida_estado ON salida(estado, id);
"""


class ErrorHTTP(Exception):
    def __init__(self, estado, motivo):
        self.estado = estado
        self.motivo = motivo


def coincide(patron, valor):
    return isinstance(valor, str) and re.fullmatch(patron, valor) is not None


def igual(esperado, recibido):
    return isinstance(recibido, str) and hmac.compare_digest(
        esperado.encode("utf-8"), recibido.encode("utf-8")
    )


def objeto(valor):
    if not isinstance(valor, dict):
        raise ErrorHTTP("400 Bad Request", "OBJETO_INVALIDO")
    return valor


def lista(valor):
    if not isinstance(valor, list):
        raise ErrorHTTP("400 Bad Request", "LISTA_INVALIDA")
    return valor


def leer_json(raw):
    try:
        return objeto(json.loads(raw))
    except (UnicodeError, ValueError, RecursionError):
        raise ErrorHTTP("400 Bad Request", "JSON_INVALIDO") from None


def mensajes_meta(payload, numero):
    if payload.get("object") != "whatsapp_business_account":
        raise ErrorHTTP("400 Bad Request", "OBJETO_META_INVALIDO")
    for entry in lista(payload.get("entry")):
        for change in lista(objeto(entry).get("changes")):
            if objeto(change).get("field") != "messages":
                continue
            value = objeto(change.get("value"))
            if (value.get("messaging_product") != "whatsapp"
                    or objeto(value.get("metadata")).get("phone_number_id") != numero):
                raise ErrorHTTP("403 Forbidden", "NUMERO_META_INCORRECTO")
            for message in lista(value.get("messages", [])):
                message = objeto(message)
                mid, telefono, fecha = (message.get(k) for k in ("id", "from", "timestamp"))
                if not (coincide(WAMID, mid) and coincide(TELEFONO, telefono)
                        and coincide(r"[0-9]{1,11}", fecha)):
                    raise ErrorHTTP("400 Bad Request", "MENSAJE_META_INVALIDO")
                tipo = message.get("type")
                accion = "desconocido"
                if tipo == "text":
                    texto = objeto(message.get("text")).get("body")
                    if not isinstance(texto, str):
                        raise ErrorHTTP("400 Bad Request", "TEXTO_META_INVALIDO")
                    accion = COMANDOS.get(texto.strip().upper(), accion)
                elif tipo == "image" and coincide(META_ID, objeto(message.get("image")).get("id")):
                    accion = "captura"
                yield mid, telefono, int(fecha), accion


def verificar_privado(path, tipo):
    info = path.lstat()
    if not tipo(info.st_mode) or info.st_uid != os.geteuid() or info.st_mode & 0o077:
        raise ValueError("La configuración y la base requieren dueño local y permisos privados.")


def leer_config(path):
    path = path.absolute()
    raiz = next((p for p in Path(__file__).resolve().parents if (p / ".git").exists()), None)
    if raiz and path.resolve().is_relative_to(raiz):
        raise ValueError("La configuración y la base deben estar fuera del repositorio.")
    verificar_privado(path.parent, stat.S_ISDIR)
    verificar_privado(path, stat.S_ISREG)
    return path, leer_json(path.read_bytes())


def validar_config(cfg, permitir_envios):
    if not isinstance(cfg, dict):
        raise ValueError("Config inválida: objeto requerido")
    if type(cfg.get("envios_habilitados", False)) is not bool:
        raise ValueError("Config inválida: envios_habilitados")
    for k in ("app_secret", "verify_token", "operator_token"):
        if not coincide(r"[A-Za-z0-9_.~-]{24,256}", cfg.get(k)):
            raise ValueError(f"Config inválida: {k}")
    if len({cfg[k] for k in ("app_secret", "verify_token", "operator_token")}) != 3:
        raise ValueError("Se necesitan tres credenciales distintas.")
    if not coincide(META_ID, cfg.get("phone_number_id")):
        raise ValueError("Config inválida: phone_number_id")
    ttl = cfg.get("pago_ttl_segundos")
    cierre = cfg.get("cierre_inscripcion_epoch")
    # Límite por INICIO de la última clase. Su hora final no está confirmada.
    ultima_clase = int(datetime.fromisoformat(OFERTA["clases"][-1]).timestamp())
    if type(ttl) is not int or not 0 < ttl <= VENTANA:
        raise ValueError("Config inválida: pago_ttl_segundos")
    if type(cierre) is not int or not 0 < cierre <= ultima_clase:
        raise ValueError("Config inválida: cierre_inscripcion_epoch")
    if not permitir_envios:
        return
    if (not coincide(r"[A-Za-z0-9_.~-]{24,256}", cfg.get("dispatcher_token"))
            or cfg["dispatcher_token"] in {cfg[k] for k in ("app_secret", "verify_token", "operator_token")}):
        raise ValueError("Config inválida: dispatcher_token")
    for k, patron in (("graph_version", r"v[0-9]{1,3}\.[0-9]{1,3}"),
                      ("graph_token", r"[A-Za-z0-9_.~-]{24,4096}"),
                      ("qr_media_id", META_ID)):
        if not coincide(patron, cfg.get(k)):
            raise ValueError(f"Config inválida: {k}")
    enlaces = cfg.get("meet_urls")
    if not isinstance(enlaces, list) or len(enlaces) != len(OFERTA["clases"]):
        raise ValueError("Config inválida: meet_urls")
    for url in enlaces:
        if (not isinstance(url, str) or len(url) > 160
                or not coincide(r"https://meet\.google\.com/[A-Za-z0-9-]+", url)):
            raise ValueError("Config inválida: meet_urls")


def preparar_base(path, numero):
    verificar_privado(path.parent, stat.S_ISDIR)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        verificar_privado(path, stat.S_ISREG)
    else:
        os.close(fd)
    with transaccion(path) as db:
        for sentencia in ESQUEMA.strip().rstrip(";").split(";"):
            db.execute(sentencia)
        db.execute("INSERT OR IGNORE INTO cuenta VALUES (1, ?)", (numero,))
        if db.execute("SELECT numero FROM cuenta").fetchone()[0] != numero:
            raise ValueError("La base pertenece a otro phone_number_id.")


@contextmanager
def transaccion(path):
    db = sqlite3.connect(path, timeout=3, isolation_level=None)
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA foreign_keys = ON")
        db.execute("BEGIN IMMEDIATE")
        yield db
        db.commit()
    finally:
        db.close()


def emitir(db, telefono, tipo):
    db.execute("INSERT INTO salida(telefono, tipo) VALUES (?, ?)", (telefono, tipo))


def cancelar(db, telefono):
    db.execute("UPDATE salida SET estado = 'cancelado' WHERE telefono = ? AND estado = 'pendiente'",
               (telefono,))


def excepcion(db, telefono, motivo):
    db.execute("UPDATE clientes SET estado = 'excepcion', revision = ? WHERE telefono = ?",
               (motivo, telefono))
    cancelar(db, telefono)
    emitir(db, telefono, "excepcion")


def vencer(db, ahora):
    for cliente in db.execute(
        "SELECT telefono FROM clientes WHERE estado = 'pendiente' AND cese = 0 AND vence <= ?",
        (ahora,),
    ).fetchall():
        excepcion(db, cliente["telefono"], "PAGO_VENCIDO")


def vip_lleno(db):
    cantidad = db.execute(
        "SELECT count(*) FROM clientes WHERE plan = 'vip' AND estado = 'confirmado'"
    ).fetchone()[0]
    return cantidad >= OFERTA["vip"]["cupos"]


def recibir(db, cfg, mensaje, ahora):
    mid, telefono, fecha, accion = mensaje
    if not db.execute("INSERT OR IGNORE INTO vistos VALUES (?)", (mid,)).rowcount:
        return 0
    fecha = min(fecha, ahora)
    if accion != "baja" and fecha <= ahora - VENTANA:
        return 1
    db.execute("""INSERT INTO clientes(telefono, ultimo) VALUES (?, ?)
                  ON CONFLICT(telefono) DO UPDATE SET ultimo = MAX(ultimo, excluded.ultimo)""",
               (telefono, fecha))
    cliente = db.execute("SELECT * FROM clientes WHERE telefono = ?", (telefono,)).fetchone()
    if cliente["cese"]:
        return 1
    if accion == "baja":
        db.execute("UPDATE clientes SET cese = 1, revision = NULL WHERE telefono = ?", (telefono,))
        cancelar(db, telefono)
        emitir(db, telefono, "cese")
    elif accion == "interes" and ahora < cfg["cierre_inscripcion_epoch"]:
        emitir(db, telefono, "informacion")
    elif accion == "ayuda":
        db.execute("UPDATE clientes SET revision = COALESCE(revision, 'AYUDA_SOLICITADA') WHERE telefono = ?",
                   (telefono,))
    elif accion in ("grupal", "vip") and cliente["estado"] == "interesado":
        cierre = cfg["cierre_inscripcion_epoch"]
        if ahora >= cierre:
            excepcion(db, telefono, "INSCRIPCION_CERRADA")
        elif accion == "vip" and vip_lleno(db):
            excepcion(db, telefono, "VIP_SIN_CUPO")
        else:
            vence = min(ahora + cfg["pago_ttl_segundos"], cierre)
            db.execute("""UPDATE clientes SET estado = 'pendiente', plan = ?, vence = ?,
                          revision = 'INSCRIPCION_PENDIENTE' WHERE telefono = ?""", (accion, vence, telefono))
            emitir(db, telefono, "pendiente")
            emitir(db, telefono, "qr")
    elif accion == "captura" and cliente["estado"] == "pendiente":
        db.execute("UPDATE clientes SET revision = 'COMPROBANTE_NO_VERIFICADO' WHERE telefono = ?",
                   (telefono,))
        emitir(db, telefono, "captura")
    elif accion == "desconocido":
        emitir(db, telefono, "ayuda")
    return 1


def confirmar(db, pago):
    telefono = pago.get("telefono")
    referencia = pago.get("referencia")
    referencia = referencia.strip().upper() if isinstance(referencia, str) else None
    if (not coincide(TELEFONO, telefono) or not coincide(REFERENCIA, referencia)
            or pago.get("decision") != "confirmar"):
        return "400 Bad Request", {"resultado": "DATOS_CONFIRMACION_INVALIDOS"}
    cliente = db.execute("SELECT * FROM clientes WHERE telefono = ?", (telefono,)).fetchone()
    if not cliente or cliente["cese"]:
        return "409 Conflict", {"resultado": "INSCRIPCION_NO_DISPONIBLE"}
    if cliente["estado"] == "confirmado" and cliente["referencia"] == referencia:
        return "200 OK", {"resultado": "ya_confirmado"}
    if cliente["estado"] != "pendiente":
        return "409 Conflict", {"resultado": cliente["revision"] or "ESTADO_NO_CONFIRMABLE"}
    if (pago.get("movimientoVerificado") is not True or pago.get("destinoVerificado") is not True
            or pago.get("moneda") != OFERTA["moneda"] or type(pago.get("importe")) is not int
            or pago["importe"] != OFERTA[cliente["plan"]]["importe"]):
        return "409 Conflict", {"resultado": "CONCILIACION_INCOMPLETA"}
    if db.execute("SELECT 1 FROM clientes WHERE referencia = ?", (referencia,)).fetchone():
        excepcion(db, telefono, "REFERENCIA_REUTILIZADA")
        return "409 Conflict", {"resultado": "REFERENCIA_REUTILIZADA"}
    if cliente["plan"] == "vip" and vip_lleno(db):
        excepcion(db, telefono, "VIP_SIN_CUPO")
        return "409 Conflict", {"resultado": "VIP_SIN_CUPO"}
    db.execute("""UPDATE clientes SET estado = 'confirmado', referencia = ?, revision = NULL
                  WHERE telefono = ?""", (referencia, telefono))
    cancelar(db, telefono)
    emitir(db, telefono, "confirmado")
    return "200 OK", {"resultado": "confirmado"}


def payload_salida(cfg, fila):
    tipo, plan = fila["tipo"], fila["plan"]
    payload = {"messaging_product": "whatsapp", "recipient_type": "individual", "to": fila["telefono"]}
    if tipo == "qr":
        importe = OFERTA[plan]["importe"]
        caption = (f"{plan.upper()} · Bs {importe} (bolivianos). "
                   "Tras el pago, enviá el comprobante. Sergio verifica el movimiento manualmente.")
        return {**payload, "type": "image", "image": {"id": cfg["qr_media_id"], "caption": caption}}
    if tipo == "confirmado":
        enlaces = "\n".join(f"Clase {i}: {url}" for i, url in enumerate(cfg["meet_urls"], 1))
        texto = f"Pago confirmado por Sergio. Entrá a Google Meet con tu cuenta propia.\n{enlaces}"
        if plan == "vip":
            texto += "\nSergio coordina tu llamada privada de 30 minutos."
    elif tipo == "pendiente":
        texto = CATALOGO["textos"][tipo].format(plan=plan.upper(), importe=OFERTA[plan]["importe"])
    else:
        texto = CATALOGO["textos"][tipo]
    return {**payload, "type": "text", "text": {"body": texto, "preview_url": False}}


def enviar_graph(cfg, payload):
    """Devuelve el wamid de aceptación. Sin redirecciones ni reintentos."""
    conn = http.client.HTTPSConnection("graph.facebook.com", timeout=5)
    ruta = f"/{cfg['graph_version']}/{cfg['phone_number_id']}/messages"
    try:
        conn.request("POST", ruta, json.dumps(payload).encode("utf-8"),
                     {"Authorization": "Bearer " + cfg["graph_token"], "Content-Type": "application/json"})
        respuesta = conn.getresponse()
        if respuesta.status != 200:
            return None
        datos = json.loads(respuesta.read(65537))
        mensajes = datos.get("messages") if isinstance(datos, dict) else None
        if isinstance(mensajes, list) and len(mensajes) == 1 and isinstance(mensajes[0], dict):
            return mensajes[0].get("id")
        return None
    except (OSError, http.client.HTTPException, ValueError, RecursionError):
        return None
    finally:
        conn.close()


def despachar(path, cfg, ahora, transporte):
    with transaccion(path) as db:
        vencer(db, ahora)
        db.execute("""UPDATE salida SET estado = 'cancelado' WHERE estado = 'pendiente'
                      AND telefono IN (SELECT telefono FROM clientes WHERE ultimo <= ?)""", (ahora - VENTANA,))
        db.execute("""UPDATE salida SET estado = 'cancelado' WHERE estado = 'pendiente'
                      AND tipo != 'cese' AND telefono IN (SELECT telefono FROM clientes WHERE cese = 1)""")
        if ahora >= cfg["cierre_inscripcion_epoch"]:
            db.execute("UPDATE salida SET estado = 'cancelado' WHERE estado = 'pendiente' AND tipo = 'informacion'")
        fila = db.execute("""SELECT salida.*, clientes.plan FROM salida JOIN clientes USING (telefono)
                             WHERE salida.estado = 'pendiente' ORDER BY salida.id LIMIT 1""").fetchone()
        if not fila:
            return {"resultado": "vacio"}
        payload = payload_salida(cfg, fila)
        # La reserva se confirma en disco antes de llamar al proveedor.
        db.execute("UPDATE salida SET estado = 'incierto' WHERE id = ?", (fila["id"],))

    try:
        meta_id = transporte(cfg, payload)
    except (OSError, http.client.HTTPException):
        meta_id = None
    if coincide(WAMID, meta_id):
        with transaccion(path) as db:
            registrado = db.execute("UPDATE OR IGNORE salida SET estado = 'aceptado', meta_id = ? WHERE id = ?",
                                    (meta_id, fila["id"])).rowcount
        if registrado:
            return {"resultado": "aceptado", "id": fila["id"]}
    return {"resultado": "incierto", "id": fila["id"]}


def crear_app(path, cfg, permitir_envios=False, transporte=enviar_graph, reloj=time.time):
    envios = permitir_envios and cfg.get("envios_habilitados") is True
    validar_config(cfg, envios)
    preparar_base(path, cfg["phone_number_id"])

    def responder(entorno):
        ruta, metodo = entorno["PATH_INFO"], entorno["REQUEST_METHOD"]
        if ruta == "/meta" and metodo == "GET":
            query = parse_qs(entorno.get("QUERY_STRING", ""), max_num_fields=12)
            challenge = query.get("hub.challenge", [])
            if (query.get("hub.mode") != ["subscribe"] or len(challenge) != 1
                    or not coincide(r"[0-9]{1,64}", challenge[0])
                    or len(query.get("hub.verify_token", [])) != 1
                    or not igual(cfg["verify_token"], query["hub.verify_token"][0])):
                raise ErrorHTTP("403 Forbidden", "VERIFICACION_RECHAZADA")
            return "200 OK", challenge[0]
        if (ruta, metodo) not in {("/meta", "POST"), ("/operador/confirmar", "POST"),
                                  ("/operador/despachar", "POST"), ("/operador/revisar", "GET")}:
            raise ErrorHTTP("404 Not Found", "RUTA_INVALIDA")
        ahora = int(reloj())
        if ruta == "/operador/despachar":
            if not envios:
                raise ErrorHTTP("409 Conflict", "ENVIOS_DESHABILITADOS")
            if not igual("Bearer " + cfg["dispatcher_token"], entorno.get("HTTP_AUTHORIZATION")):
                raise ErrorHTTP("401 Unauthorized", "DESPACHADOR_NO_AUTENTICADO")
            return "200 OK", despachar(path, cfg, ahora, transporte)
        if ruta != "/meta" and not igual("Bearer " + cfg["operator_token"], entorno.get("HTTP_AUTHORIZATION")):
            raise ErrorHTTP("401 Unauthorized", "OPERADOR_NO_AUTENTICADO")
        if ruta == "/operador/revisar":
            with transaccion(path) as db:
                vencer(db, ahora)
                revision = db.execute("""SELECT telefono, estado, plan, vence, revision
                                         FROM clientes WHERE revision IS NOT NULL AND cese = 0
                                         ORDER BY telefono""")
                inciertos = db.execute("SELECT id, telefono, tipo FROM salida WHERE estado = 'incierto'")
                return "200 OK", {"revision": [dict(x) for x in revision],
                                  "inciertos": [dict(x) for x in inciertos]}
        longitud = entorno.get("CONTENT_LENGTH", "")
        if not coincide(r"[0-9]{1,9}", longitud):
            raise ErrorHTTP("411 Length Required", "LONGITUD_REQUERIDA")
        if int(longitud) > MAX_BODY:
            raise ErrorHTTP("413 Payload Too Large", "CUERPO_DEMASIADO_GRANDE")
        raw = entorno["wsgi.input"].read(int(longitud))
        if len(raw) != int(longitud):
            raise ErrorHTTP("400 Bad Request", "CUERPO_INCOMPLETO")
        if ruta == "/meta":
            esperado = "sha256=" + hmac.new(cfg["app_secret"].encode(), raw, hashlib.sha256).hexdigest()
            if not igual(esperado, entorno.get("HTTP_X_HUB_SIGNATURE_256")):
                raise ErrorHTTP("403 Forbidden", "FIRMA_RECHAZADA")
            mensajes = list(mensajes_meta(leer_json(raw), cfg["phone_number_id"]))
            with transaccion(path) as db:
                vencer(db, ahora)
                nuevos = sum(recibir(db, cfg, mensaje, ahora) for mensaje in mensajes)
            return "200 OK", {"nuevos": nuevos}
        pago = leer_json(raw)
        with transaccion(path) as db:
            vencer(db, ahora)
            return confirmar(db, pago)

    def app(entorno, start_response):
        try:
            estado, cuerpo = responder(entorno)
        except ErrorHTTP as exc:
            estado, cuerpo = exc.estado, {"error": exc.motivo}
        except ValueError:
            estado, cuerpo = "400 Bad Request", {"error": "SOLICITUD_INVALIDA"}
        except sqlite3.Error:
            estado, cuerpo = "503 Service Unavailable", {"error": "BASE_NO_DISPONIBLE"}
        texto = isinstance(cuerpo, str)
        contenido = (cuerpo if texto else json.dumps(cuerpo)).encode("utf-8")
        tipo = "text/plain" if texto else "application/json"
        start_response(estado, [("Content-Type", tipo + "; charset=utf-8"),
                                ("Content-Length", str(len(contenido))), ("Cache-Control", "no-store")])
        return [contenido]

    return app


class SinRegistro(WSGIRequestHandler):
    def log_message(self, formato, *args):
        # El challenge contiene un secreto en la URL.
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--puerto", type=int, default=8765)
    parser.add_argument("--permitir-envios", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    try:
        path, cfg = leer_config(args.config)
        app = crear_app(path.with_name("chatbot.sqlite3"), cfg, args.permitir_envios)
    except (ErrorHTTP, OSError, ValueError, sqlite3.Error):
        parser.exit(2, "No se pudo abrir la configuración o la base privada. Revisá ADAPTADOR.md.\n")
    loopback = str(IPv4Address(INADDR_LOOPBACK))
    with make_server(loopback, args.puerto, app, handler_class=SinRegistro) as server:
        print(f"Adaptador local en localhost:{server.server_port}", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()

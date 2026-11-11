"""Adaptadores de ENSAYO IG/FB: stdlib, sin servidor, shell ni transporte de red."""
from contextlib import contextmanager
from dataclasses import asdict
from datetime import datetime
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
from urllib.parse import urlencode

from motor import Event, State, decide

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[3]
REPO = BASE.parents[1]
MAX_BODY = 256 * 1024
MAX_EVENTS = 100
ID = r"[0-9]{1,40}"
COMMENT_ID = r"[0-9]{1,40}(?:_[0-9]{1,40})?"
MESSAGE_ID = r"[A-Za-z0-9_.:=+/-]{1,256}"


class Rejected(Exception):
    """Sólo códigos estáticos; nunca incluye datos de entrada o secretos."""
    def __init__(self, code, status=400):
        super().__init__(code)
        self.code, self.status = code, status


def require(condition, code, status=400):
    if not condition:
        raise Rejected(code, status)


def match(pattern, value):
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def obj(value):
    require(isinstance(value, dict), "OBJETO_INVALIDO")
    return value


def rows(value, maximum=MAX_EVENTS):
    require(isinstance(value, list) and len(value) <= maximum, "LISTA_INVALIDA")
    return value


def integer(value):
    require(type(value) is int and value > 0, "FECHA_INVALIDA")
    return value


def text(value):
    require(isinstance(value, str) and 0 < len(value) <= 2000, "TEXTO_INVALIDO")
    require(not any(ord(c) < 32 and c not in "\r\n\t" for c in value), "TEXTO_INVALIDO")
    return value


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha(value):
    return hashlib.sha256(value.encode()).hexdigest()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "JSON_CLAVE_DUPLICADA")
            result[key] = value
        return result
    try:
        return obj(json.loads(raw, object_pairs_hook=pairs,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError())))
    except (ValueError, UnicodeError, RecursionError):
        raise Rejected("JSON_INVALIDO") from None


def normalize(payload, accounts, now):
    """Subconjunto estricto de sobres; todos se validan antes de persistir un lote."""
    platform = {"instagram": "instagram", "page": "facebook"}.get(payload.get("object"))
    require(platform is not None, "OBJETO_META_INVALIDO")
    events = []
    for entry in rows(payload.get("entry"), 50):
        entry = obj(entry)
        account = entry.get("id")
        require(match(ID, account) and account == accounts[platform], "CUENTA_INVALIDA", 403)
        for change in rows(entry.get("changes", [])):
            change = obj(change)
            if change.get("field") != ("comments" if platform == "instagram" else "feed"):
                continue
            value = obj(change.get("value"))
            if platform == "facebook":
                if value.get("item") != "comment" or value.get("verb") != "add":
                    continue  # ediciones y bajas de publicaciones no son mensajes entrantes
                eid, origin = value.get("comment_id"), value.get("post_id")
                message, date = value.get("message"), value.get("created_time")
            else:
                eid, origin = value.get("id"), obj(value.get("media")).get("id")
                message, date = value.get("text"), entry.get("time")
            actor = obj(value.get("from")).get("id")
            require(match(ID, actor) and match(COMMENT_ID, eid) and match(COMMENT_ID, origin),
                    "IDENTIDAD_COMENTARIO_INVALIDA")
            date = integer(date)
            require(date <= now + 300, "FECHA_FUTURA")
            message = text(message)
            if actor != account:
                events.append(Event(platform + "_comentario", account, actor, eid, date, message, origin))
        for item in rows(entry.get("messaging", [])):
            item = obj(item)
            actor = obj(item.get("sender")).get("id")
            recipient = obj(item.get("recipient")).get("id")
            require(match(ID, actor) and match(ID, recipient), "IDENTIDAD_DM_INVALIDA")
            message = item.get("message")
            if message is None:
                require(recipient == account or actor == account, "DESTINATARIO_INVALIDO", 403)
                continue  # recibos y postbacks no se convierten en texto
            message = obj(message)
            require(type(message.get("is_echo", False)) is bool, "ECHO_INVALIDO")
            if message.get("is_echo"):
                require(actor == account, "ECHO_IDENTIDAD_INVALIDA", 403)
                continue
            require(recipient == account and actor != account, "DESTINATARIO_INVALIDO", 403)
            eid = message.get("mid")
            require(match(MESSAGE_ID, eid), "ID_DM_INVALIDO")
            date = integer(item.get("timestamp")) // 1000
            require(0 < date <= now + 300, "FECHA_FUTURA")
            # Adjuntos no activan venta ni pago. Un texto ausente no es NEGOCIO.
            if "text" not in message:
                continue
            events.append(Event(platform + "_dm", account, actor, eid, date, text(message["text"]), eid))
        require(len(events) <= MAX_EVENTS, "DEMASIADOS_EVENTOS", 413)
    return events


def private_file(path, directory=False):
    info = path.lstat()
    require((stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode))
            and info.st_uid == os.geteuid() and not info.st_mode & 0o077, "ARCHIVO_NO_PRIVADO")


def outside_repo(path):
    path = Path(path).absolute()
    require(not path.resolve().is_relative_to(REPO), "RUTA_EN_REPOSITORIO")
    private_file(path.parent, directory=True)
    return path


def validate_config(config):
    config = obj(config)
    require(config.get("envios_habilitados", False) is False, "ACTIVACION_PENDIENTE", 403)
    accounts = obj(config.get("cuentas"))
    require(set(accounts) == {"instagram", "facebook"} and all(match(ID, x) for x in accounts.values()),
            "CUENTAS_INVALIDAS")
    for key in ("app_secret", "verify_token"):
        require(match(r"[A-Za-z0-9_.~-]{24,256}", config.get(key)), "CREDENCIAL_INVALIDA")
    require(config["app_secret"] != config["verify_token"], "CREDENCIALES_REPETIDAS")
    destination = config.get("whatsapp_destino")
    require(destination is None or match(r"https://wa\.me/[1-9][0-9]{7,14}", destination),
            "DESTINO_PRIVADO_INVALIDO")
    return config


def read_config(path):
    path = outside_repo(path)
    private_file(path)
    require(path.stat().st_size <= 16384, "CONFIG_DEMASIADO_GRANDE")
    return validate_config(strict_json(path.read_bytes()))


def load_offer(now):
    """Reutiliza oferta estructurada existente; hash de decisión evita deriva silenciosa."""
    manifest = strict_json((ROOT / "oferta-referencia.json").read_bytes())
    decisions = BASE / "05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md"
    catalog = BASE / manifest["catalogo"]
    offer = strict_json(catalog.read_bytes())["oferta"]
    valid = (hashlib.sha256(decisions.read_bytes()).hexdigest() == manifest["decisiones_sha256"]
             and sha(canonical(offer)) == manifest["oferta_sha256"]
             and now < int(datetime.fromisoformat(offer["clases"][-1]).timestamp()))
    # Texto propio mínimo, sin condiciones históricas de otras partes del catálogo.
    reply = (f'{offer["nombre"]}. Google Meet: 13 nov 2026, 20:00; 14 nov, 14:00; '
             '16 nov, 20:00 (America/La_Paz). Grupal Bs 50. VIP Bs 150: 5 cupos totales '
             'y llamada privada de 30 minutos; disponibilidad por confirmar. '
             'Sergio confirma cada pago manualmente; una captura no concede acceso. '
             'Para continuar por WhatsApp, escribí WHATSAPP por DM. Para detener el contacto: BAJA.')
    return valid, reply


SCHEMA = """
CREATE TABLE IF NOT EXISTS binding (id INTEGER PRIMARY KEY CHECK(id=1), fingerprint TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS contacts (
 scope TEXT PRIMARY KEY, last INTEGER NOT NULL, stopped INTEGER NOT NULL,
 origin TEXT NOT NULL, interested INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS events (
 event_key TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, result TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS outbox (
 id TEXT PRIMARY KEY, scope TEXT NOT NULL, channel TEXT NOT NULL, event_time INTEGER NOT NULL,
 payload TEXT NOT NULL, status TEXT NOT NULL, outcome TEXT);
"""


class Store:
    def __init__(self, path, accounts):
        self.accounts = dict(accounts)
        self.path = outside_repo(path)
        try:
            fd = os.open(self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            private_file(self.path)
        else:
            os.close(fd)
        with self.transaction() as db:
            for statement in SCHEMA.strip().split(";"):
                if statement.strip():
                    db.execute(statement)
            fingerprint = sha(canonical({"modo": "simulacion-v1", "cuentas": accounts}))
            db.execute("INSERT OR IGNORE INTO binding VALUES(1, ?)", (fingerprint,))
            require(db.execute("SELECT fingerprint FROM binding").fetchone()[0] == fingerprint,
                    "BASE_DE_OTRAS_CUENTAS")

    @contextmanager
    def transaction(self):
        private_file(self.path)
        db = sqlite3.connect(self.path, isolation_level=None, timeout=3)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA secure_delete=ON")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def ingest(self, events, now, offer_valid, offer_reply, destination=None):
        results = []
        with self.transaction() as db:
            for event in events:
                scope = sha(canonical([event.channel.split("_")[0], event.account, event.actor]))
                key = sha(canonical([event.channel, event.account, event.event_id]))
                fingerprint = sha(canonical(asdict(event)))
                existing = db.execute("SELECT fingerprint FROM events WHERE event_key=?", (key,)).fetchone()
                if existing:
                    require(existing[0] == fingerprint, "ID_REUTILIZADO_CON_OTROS_DATOS", 409)
                    results.append({"canal": event.channel, "resultado": "duplicado"})
                    continue
                row = db.execute("SELECT * FROM contacts WHERE scope=?", (scope,)).fetchone()
                previous = State(row["last"], bool(row["stopped"]), row["origin"], bool(row["interested"])) if row else State()
                decision = decide(event, previous, now, offer_valid)
                result, state = decision.result, decision.state
                if decision.action == "whatsapp" and destination is None:
                    result = "destino_privado_faltante"
                elif decision.action:
                    response = offer_reply
                    if decision.action == "whatsapp":
                        # Referencia opaca conserva origen en DB; no vincula identidades entre redes.
                        response = destination + "?" + urlencode({"text": "NEGOCIO ref " + key[:16]})
                    payload = {"modo": "simulacion", "tipo": "private_reply" if event.channel.endswith("comentario") else "dm",
                               "cuenta": event.account, "destinatario": event.event_id if event.channel.endswith("comentario") else event.actor,
                               "texto": response, "origen_inicial": state.origin, "evento": event.event_id}
                    db.execute("INSERT INTO outbox VALUES(?,?,?,?,?,?,NULL)",
                               (key, scope, event.channel, event.timestamp, canonical(payload), "pendiente_simulacion"))
                if state.stopped:
                    db.execute("UPDATE outbox SET status='cancelado_baja' WHERE scope=? AND status='pendiente_simulacion'", (scope,))
                db.execute("INSERT OR REPLACE INTO contacts VALUES(?,?,?,?,?)",
                           (scope, state.last, int(state.stopped), state.origin, int(state.interested)))
                db.execute("INSERT INTO events VALUES(?,?,?)", (key, fingerprint, result))
                results.append({"canal": event.channel, "resultado": result})
        return results

    def simulate_one(self, outcome, now):
        require(outcome in {"exito", "rechazo", "timeout", "incierto"}, "FIXTURE_RESULTADO_INVALIDO")
        with self.transaction() as db:
            row = db.execute("SELECT * FROM outbox WHERE status='pendiente_simulacion' ORDER BY rowid LIMIT 1").fetchone()
            if not row:
                return {"modo": "simulacion", "resultado": "sin_pendientes", "envios_reales": 0}
            # Ningún resultado incierto se reintenta. Todo permanece exclusivamente simulado.
            status = {"exito": "exito_simulado", "rechazo": "fallo_simulado",
                      "timeout": "incierto_simulado", "incierto": "incierto_simulado"}[outcome]
            if now - row["event_time"] > 3600:
                status = "cancelado_caducidad_local"
            db.execute("UPDATE outbox SET status=?, outcome=? WHERE id=?", (status, outcome, row["id"]))
            return {"modo": "simulacion", "canal": row["channel"], "resultado": status, "envios_reales": 0}

    def summary(self):
        with self.transaction() as db:
            return {"modo": "simulacion", "envios_reales": 0,
                    "eventos": db.execute("SELECT count(*) FROM events").fetchone()[0],
                    "salidas": {row[0]: row[1] for row in db.execute("SELECT status,count(*) FROM outbox GROUP BY status")}}


class RealConnector:
    """Bloqueo explícito. No hay ruta de envío real en esta entrega."""
    enabled = False

    def send(self, *args, **kwargs):
        raise Rejected("ACTIVACION_PENDIENTE", 403)


class Adapter:
    def __init__(self, config, store, offer_loader=load_offer):
        self.config = validate_config(strict_json(canonical(config)))
        require(self.config["cuentas"] == store.accounts, "BASE_DE_OTRAS_CUENTAS")
        self.store = store
        self.offer_loader = offer_loader

    def handle(self, method, headers, raw, query, now):
        if method == "GET":
            require(query.get("hub.mode") == "subscribe" and isinstance(query.get("hub.verify_token"), str)
                    and hmac.compare_digest(query["hub.verify_token"].encode(), self.config["verify_token"].encode()),
                    "VERIFICACION_INVALIDA", 403)
            challenge = query.get("hub.challenge")
            require(match(r"[0-9]{1,128}", challenge), "CHALLENGE_INVALIDO")
            return {"status": 200, "challenge": challenge}
        require(method == "POST", "METODO_INVALIDO", 405)
        require(isinstance(raw, bytes) and len(raw) <= MAX_BODY, "PAYLOAD_EXCESIVO", 413)
        lowered = {k.lower(): v for k, v in headers.items()}
        require(len(lowered) == len(headers), "CABECERAS_DUPLICADAS")
        require(lowered.get("content-type", "").split(";")[0].strip() == "application/json", "TIPO_INVALIDO", 415)
        signature = lowered.get("x-hub-signature-256")
        expected = "sha256=" + hmac.new(self.config["app_secret"].encode(), raw, hashlib.sha256).hexdigest()
        require(match(r"sha256=[0-9a-f]{64}", signature) and hmac.compare_digest(signature, expected), "FIRMA_INVALIDA", 403)
        events = normalize(strict_json(raw), self.config["cuentas"], now)
        try:
            offer_valid, reply = self.offer_loader(now)
        except (OSError, ValueError, KeyError, TypeError, Rejected):
            # La baja no depende de la disponibilidad del catálogo comercial.
            offer_valid, reply = False, ""
        results = self.store.ingest(events, now, offer_valid, reply, self.config.get("whatsapp_destino"))
        return {"status": 200, "modo": "simulacion", "envios_reales": 0, "resultados": results}

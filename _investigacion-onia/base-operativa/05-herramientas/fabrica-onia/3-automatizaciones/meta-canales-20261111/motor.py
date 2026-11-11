"""Decisiones puras. Texto entrante = datos; nunca código, plantilla ni instrucciones."""
from dataclasses import dataclass, replace
import re
import unicodedata

CHANNELS = ("instagram_comentario", "instagram_dm", "facebook_comentario", "facebook_dm")


@dataclass(frozen=True)
class Event:
    channel: str
    account: str
    actor: str
    event_id: str
    timestamp: int
    text: str
    origin: str


@dataclass(frozen=True)
class State:
    last: int = 0
    stopped: bool = False
    origin: str = ""
    interested: bool = False


@dataclass(frozen=True)
class Decision:
    state: State
    result: str
    action: str | None = None


def command(text):
    normalized = unicodedata.normalize("NFKC", text).strip().upper()
    words = re.findall(r"\w+", normalized)
    # Cese prevalece incluso en texto ambiguo o tardío.
    if set(words) & {"BAJA", "STOP"}:
        return "baja"
    if normalized in {"NO", "NO GRACIAS", "NO QUIERO", "NO QUIERO NEGOCIO"}:
        return "baja"
    if re.fullmatch(r"(?:QUIERO |INFO )?NEGOCIO[.!?¡¿, ]*", normalized):
        return "negocio"
    if normalized == "WHATSAPP":
        return "whatsapp"
    if any(c in normalized for c in "<>`$;{}\\") or "IGNORE" in normalized or "IGNORA" in normalized:
        return "inyeccion"
    return "manual"


def decide(event, previous, now, offer_valid):
    """Sin reloj, disco, red ni datos privados implícitos. Ventana LOCAL, no de Meta."""
    intent = command(event.text)
    if intent == "baja":
        return Decision(replace(previous, stopped=True, last=max(previous.last, event.timestamp)), "baja")
    if previous.stopped:
        return Decision(previous, "cese_vigente")
    if event.timestamp <= previous.last:
        return Decision(previous, "orden_tardio")
    if now - event.timestamp > 3600:
        return Decision(previous, "evento_caducado_local")
    current = replace(previous, last=event.timestamp, origin=previous.origin or event.origin)
    if intent in {"inyeccion", "manual"}:
        return Decision(current, intent)
    if not offer_valid:
        return Decision(current, "oferta_no_vigente")
    if intent == "negocio":
        return Decision(replace(current, interested=True), "informacion_preparada", "informacion")
    if event.channel.endswith("_dm") and previous.interested:
        return Decision(current, "derivacion_preparada", "whatsapp")
    return Decision(current, "requiere_dm_con_contexto")

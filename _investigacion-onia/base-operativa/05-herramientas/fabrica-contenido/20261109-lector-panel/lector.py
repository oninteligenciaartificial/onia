"""Consulta manual pública y proyección de sólo lectura. Python stdlib, sin cuentas."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import signal
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BASE = ROOT.parents[2]
REPO = BASE.parents[1]
MAX_BYTES = 512 * 1024
TIMEOUT = 12
MAX_SOURCES = 3
MAX_ITEMS = 20
CONTENT = "01-negocio/workshop-20261108/noche-20261109"
TASKS = ("fabrica-contenido-diseno-20261108", "noche-telegram-20261109",
         "noche-workshop-contenido-20261109")
# Lista cerrada: las URLs del documento remoto nunca se siguen.
SOURCES = (
    {"id": "F01", "url": "https://support.claude.com/en/articles/8114491-get-started-with-claude",
     "autor": "Anthropic", "titulo_esperado": "Get started with Claude",
     "resumen": "Guía de acceso y primeros pasos con Claude. El acceso personal y los límites de uso requieren comprobación propia.",
     "cobertura": "Título y fecha visible extraídos automáticamente; contenido de acceso y primeros pasos cotejado manualmente el 9/11/2026. No se siguen enlaces."},
    {"id": "F02", "url": "https://support.claude.com/en/articles/7996857-my-prompt-isn-t-giving-me-a-helpful-answer",
     "autor": "Anthropic", "titulo_esperado": "My prompt",
     "resumen": "Guía para pedir con claridad, aportar contexto, dividir tareas y dar seguimiento. No valida nuestros ejemplos ni garantiza resultados.",
     "cobertura": "Título y fecha visible extraídos automáticamente; recomendaciones cotejadas manualmente el 9/11/2026. No se siguen enlaces."},
    {"id": "F06", "url": "https://claude.com/resources/articles/claude-enterprise-security-updates",
     "autor": "Anthropic", "titulo_esperado": "More visibility and control over Claude Enterprise for security teams",
     "tipo_contenido": "noticia", "publicacion_esperada": "2026-11-05",
     "resumen": "Anuncio de controles de seguridad y administración para Claude Enterprise, con condiciones y funciones beta. No acredita disponibilidad en Free ni despliegue en una cuenta propia.",
     "cobertura": "Título, fecha visible y metadato de publicación cotejados; introducción, controles y condiciones leídos manualmente el 9/11/2026. No se siguen enlaces.",
     "referencia_previa": "FUENTES-Y-MATRIZ.md, F06/N01: artículo comprobado el 9/11/2026; anuncio del 5/11. Esta referencia no sustituye una consulta nueva."},
)


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def clean(value, limit=300):
    return " ".join(re.sub(r"[\x00-\x1f\x7f]", " ", str(value)).split())[:limit]


class Rejected(ValueError):
    pass


def canonical_url(url):
    """Identidad por URL; sólo parámetros de seguimiento conocidos se descartan."""
    u = urllib.parse.urlsplit(url)
    if (u.scheme != "https" or u.port
            or u.username or u.password
            or any(c in url for c in "\r\n\\")):
        raise Rejected("URL_NO_PERMITIDA")
    params = [(k, v) for k, v in urllib.parse.parse_qsl(u.query)
              if not k.lower().startswith("utm_") and k.lower() not in {"fbclid", "gclid"}]
    if params:
        raise Rejected("PARAMETROS_NO_PERMITIDOS")
    normalized = urllib.parse.urlunsplit(("https", u.hostname, u.path.rstrip("/"), "", ""))
    if normalized not in {s["url"] for s in SOURCES}:
        raise Rejected("URL_NO_PERMITIDA")
    return normalized


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Rejected("REDIRECCION_RECHAZADA")


@contextmanager
def deadline(seconds):
    # Este CLI se ejecuta en el hilo principal del VPS Linux. Límite TOTAL por fuente,
    # además del timeout de socket: también interrumpe respuestas que gotean bytes.
    def expired(*_):
        raise TimeoutError("TIMEOUT")
    previous = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


def fetch(url):
    if url not in {s["url"] for s in SOURCES}:
        raise Rejected("URL_NO_PERMITIDA")
    opener = urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(url, headers={
        "User-Agent": "ONIA-manual-reader/1.0", "Accept": "text/html",
        "Accept-Encoding": "identity"})
    # No cookie jar, autenticación, cabeceras heredadas ni reintentos.
    with deadline(TIMEOUT), opener.open(request, timeout=TIMEOUT) as response:
        if response.status != 200 or response.geturl() != url:
            raise Rejected("RESPUESTA_NO_PERMITIDA")
        if response.headers.get_content_type() != "text/html":
            raise Rejected("TIPO_NO_PERMITIDO")
        if response.headers.get("Content-Encoding", "identity").lower() != "identity":
            raise Rejected("COMPRESION_NO_PERMITIDA")
        length = response.headers.get("Content-Length")
        if length and (not length.isdigit() or int(length) > MAX_BYTES):
            raise Rejected("TAMANO_EXCEDIDO")
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise Rejected("TAMANO_EXCEDIDO")
        return data


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title = []
        self.times = []
        self.time = None
        self.publication = []
        self.date_labels = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "time":
            self.time = {"valor": attrs.get("datetime"), "etiqueta": attrs.get("title", ""), "texto": ""}
        if tag == "meta" and attrs.get("property") == "article:published_time":
            self.publication.append(attrs.get("content", ""))

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.time is not None:
            self.time["texto"] += data
        if re.fullmatch(r"[A-Z][a-z]+ \d{1,2}, \d{4}", data.strip()):
            self.date_labels.append(data.strip())

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "time" and self.time is not None:
            self.times.append(self.time)
            self.time = None


def parse_page(data, source, consulted):
    if len(data) > MAX_BYTES:
        raise Rejected("TAMANO_EXCEDIDO")
    parser = Metadata()
    parser.feed(data.decode("utf-8", errors="strict"))
    title = clean("".join(parser.title), 240)
    if source["titulo_esperado"].casefold() not in title.casefold():
        # Un challenge/login/HTML de error con 200 no es la fuente comprobada.
        raise Rejected("PAGINA_NO_RECONOCIDA")
    visible = None
    for t in parser.times:
        try:
            dt = datetime.fromisoformat(str(t["valor"]).replace("Z", "+00:00"))
            if dt.tzinfo is None:
                continue
            visible = {"valor": dt.isoformat(), "etiqueta": clean(t["etiqueta"], 90),
                       "texto": clean(t["texto"], 90), "funcion": "visible_no_acredita_publicacion_original"}
            break
        except ValueError:
            continue
    news = source.get("tipo_contenido") == "noticia"
    published = None
    if news and parser.publication:
        candidate = parser.publication[0]
        try:
            parsed = datetime.strptime(candidate, "%Y-%m-%d")
            label = parsed.strftime("%B") + f" {parsed.day}, {parsed.year}"
        except ValueError:
            raise Rejected("FECHA_PUBLICACION_INVALIDA")
        if (set(parser.publication) != {source["publicacion_esperada"]}
                or label not in parser.date_labels):
            raise Rejected("FECHA_PUBLICACION_NO_COINCIDE")
        published = candidate  # precisión de día, sin fabricar hora ni zona
        visible = {"valor": published, "etiqueta": "Date", "texto": label,
                   "funcion": "publicacion_explicita", "precision": "dia"}
    return {
        "id": source["id"], "url_original": source["url"], "url_canonica": canonical_url(source["url"]),
        "autor": source["autor"], "tipo": "primaria", "tipo_contenido": "noticia" if news else "guia_evergreen",
        "titulo": title, "fecha_consulta": consulted, "fecha_publicacion": published,
        "fecha_hecho": published, "fecha_visible": visible, "resumen": source["resumen"],
        "cobertura": source["cobertura"], "sha256_respuesta": sha(data), "bytes_respuesta": len(data),
        "ficticio": False, "alias": [], "error": None, "elegible_noticia": bool(published),
        "seleccionada_para_guiones": False if news else None,
        "pendiente": ("Candidata no seleccionada para G01/G02. Fecha del hecho: anuncio, no despliegue individual. No trasladar Enterprise a Free."
                      if published else "Publicación original y fecha del hecho desconocidas; no presentar como noticia de hoy."),
    }


def ingest(sources=SOURCES, transport=fetch):
    if not 1 <= len(sources) <= MAX_SOURCES:
        raise Rejected("LIMITE_FUENTES")
    receipts, items, index = [], [], {}
    for source in sources:
        consulted = now()
        receipt = {"fuente": source["id"], "url": source["url"], "consulta_iniciada": consulted}
        try:
            url = canonical_url(source["url"])
            if url not in {s["url"] for s in SOURCES}:
                raise Rejected("URL_NO_PERMITIDA")
            if url in index:
                index[url]["alias"].append({"id": source["id"], "url": source["url"]})
                receipt.update(resultado="duplicado", item=index[url]["id"])
            else:
                # Cada fuente seleccionada es una página: un item, nunca un crawler.
                item = parse_page(transport(url), source, consulted)
                index[url] = item
                items.append(item)
                receipt.update(resultado="leida", item=item["id"])
        except Exception as e:
            if isinstance(e, Rejected):
                code = str(e)
            elif isinstance(e, (TimeoutError, socket.timeout)):
                code = "TIMEOUT"
            elif isinstance(e, urllib.error.HTTPError):
                code = "HTTP_" + str(e.code)
            elif isinstance(e, urllib.error.URLError):
                code = "RED_NO_DISPONIBLE"
            elif isinstance(e, UnicodeError):
                code = "CODIFICACION_NO_PERMITIDA"
            else:
                code = "LECTURA_FALLIDA"
            receipt.update(resultado="fallo", error=code)
            if source.get("referencia_previa"):
                receipt["referencia_previa_sin_lectura_nueva"] = source["referencia_previa"]
        receipt["consulta_finalizada"] = now()
        receipts.append(receipt)
    return {"consultas": receipts, "items": items, "limites": {
        "max_fuentes": MAX_SOURCES, "max_items_por_fuente": MAX_ITEMS, "items_por_pagina": 1,
        "timeout_total_segundos_por_fuente": TIMEOUT, "max_bytes_por_fuente": MAX_BYTES,
        "redirecciones": False, "reintentos": 0}}


def git(*args):
    return subprocess.check_output(["git", "-C", str(REPO), *args], stderr=subprocess.DEVNULL, timeout=10)


def git_bytes(commit, relative):
    prefix = BASE.relative_to(REPO).as_posix()
    return git("show", f"{commit}:{prefix}/{relative}")


def load_harness():
    spec = importlib.util.spec_from_file_location("trabajo", BASE / "05-herramientas/scripts/trabajo.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def project_task(task_id, harness, head):
    path = f"04-operacion-agentes/tareas/{task_id}.json"
    projection = {"id": task_id, "origen": path, "integridad": "fallo", "revision_tecnica": None}
    try:
        row = harness.read_task(BASE, task_id)
        harness.verify(BASE, row)
        raw = (BASE / path).read_bytes()
        if raw != git_bytes(head, path):
            raise Rejected("REGISTRO_FUERA_COMMIT")
        review = row.get("revision_independiente") or {}
        acceptance = row.get("aceptacion") or {}
        reviewed = review.get("commit")
        good = (row["estado"] == "aceptado" and review.get("veredicto") == "bueno"
                and reviewed == (row.get("cierre") or {}).get("commit")
                and acceptance.get("revisor") == review.get("revisor"))
        if good:
            receipt = json.loads((BASE / review["evidencia"]["archivo"]).read_text())
            good = receipt.get("veredicto") == "bueno" and receipt.get("commit") == reviewed
            git("merge-base", "--is-ancestor", reviewed, head)
        projection.update(estado=row["estado"], revision=row["revision"], actualizado=row["actualizado"],
                          sha256_registro=sha(raw), integridad="verificada", proximo_paso=row["proximo_paso"],
                          revision_tecnica={"buena": bool(good), "commit": reviewed,
                                            "revisor": review.get("revisor"), "fecha": acceptance.get("fecha"),
                                            "evidencia": review.get("evidencia")})
    except Exception as e:
        projection.update(error=str(e) if isinstance(e, Rejected) else "EVIDENCIA_CANONICA_NO_VERIFICABLE",
                          proximo_paso="Coordinador: reconciliar evidencia canónica antes de usar esta proyección.")
    return projection


def project_scripts(task):
    scripts, ideas = [], []
    review = task.get("revision_tecnica") or {}
    for number, filename in [(1, "GUION-01-WORKSHOP.md"), (2, "GUION-02-EVERGREEN.md")]:
        relative = f"{CONTENT}/{filename}"
        script = {"id": f"G0{number}", "origen": relative, "integridad": "fallo", "texto": "",
                  "publicacion": "Sin aprobación de publicación; borrador", "revision_editorial": "Pendiente de Sergio/Boss"}
        try:
            raw = (BASE / relative).read_bytes()
            commit = review.get("commit")
            if not review.get("buena") or raw != git_bytes(commit, relative):
                raise Rejected("GUION_NO_COINCIDE_CON_REVISION_TECNICA")
            # El manifiesto también debe pertenecer al mismo commit revisado.
            manifest_path = f"{CONTENT}/evidencia/MANIFIESTO.json"
            manifest_raw = (BASE / manifest_path).read_bytes()
            if manifest_raw != git_bytes(commit, manifest_path):
                raise Rejected("MANIFIESTO_ALTERADO")
            ref = next(x for x in json.loads(manifest_raw)["archivos"] if x["ruta"] == filename)
            if ref["sha256"] != sha(raw) or ref["bytes"] != len(raw):
                raise Rejected("GUION_ALTERADO")
            text = raw.decode("utf-8")
            idea = next(line for line in text.splitlines() if line.startswith(f"Idea I0{number}:"))
            script.update(titulo=text.splitlines()[0].lstrip("# "), texto=text,
                          sha256=sha(raw), bytes=len(raw), integridad="verificada",
                          revision_tecnica=review, idea=f"I0{number}", fuentes=["F02"],
                          pendientes=text.split("## ")[-1].strip())
            ideas.append({"id": f"I0{number}", "texto": idea, "guion": script["id"],
                          "origen": relative, "fuentes": ["F02"], "tipo": "evergreen / propuesta OnIA"})
        except Exception as e:
            script["error"] = str(e) if isinstance(e, Rejected) else "GUION_NO_VERIFICABLE"
        scripts.append(script)
    return scripts, ideas


def build_snapshot(public):
    head = git("rev-parse", "HEAD").decode().strip()
    harness = load_harness()
    tasks = [project_task(task, harness, head) for task in TASKS]
    scripts, ideas = project_scripts(tasks[-1])
    return {"schema": "onia-lector-panel-v1", "generado": now(), "commit_entradas_repo": head,
            "alcance": "Recibo de consulta manual y proyección; no es registro de tareas ni cola editable.",
            "fuentes": public, "tareas": tasks, "guiones": scripts, "ideas": ideas,
            "efectos": {"scheduler": False, "ingesta_recurrente": False, "telegram_real": False,
                        "publicacion": False, "mutacion_harness": False}}


def own_output(path):
    path = Path(path).absolute()
    if not path.resolve().is_relative_to(ROOT) or path == ROOT:
        raise Rejected("SALIDA_FUERA_RUTA_ASIGNADA")
    for candidate in [path, *path.parents]:
        if candidate == ROOT:
            break
        if candidate.is_symlink():
            raise Rejected("SALIDA_CON_ENLACE")
    return path


def write_new(path, data):
    with own_output(path).open("x", encoding="utf-8") as stream:
        stream.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fuente", action="append", choices=[s["id"] for s in SOURCES], help="Por defecto las tres fuentes comprobadas")
    parser.add_argument("--salida", required=True, type=Path, help="Directorio NUEVO dentro de esta entrega")
    args = parser.parse_args()
    selected = [next(s for s in SOURCES if s["id"] == key) for key in (args.fuente or [s["id"] for s in SOURCES])]
    if len(selected) > MAX_SOURCES:
        parser.error("Máximo tres fuentes por consulta")
    target = own_output(args.salida)
    target.mkdir(parents=True, exist_ok=False)  # antes de cualquier red; preserva recibos previos
    snapshot = build_snapshot(ingest(selected))
    encoded = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    write_new(target / "snapshot.json", encoded)
    from panel import render
    write_new(target / "panel.html", render(snapshot))
    failed = (any(c["resultado"] == "fallo" for c in snapshot["fuentes"]["consultas"])
              or any(t["integridad"] != "verificada" for t in snapshot["tareas"])
              or any(g["integridad"] != "verificada" for g in snapshot["guiones"]))
    print(json.dumps({"salida": str(target.relative_to(ROOT)), "items": len(snapshot["fuentes"]["items"]),
                      "snapshot_sha256": sha(encoded.encode()), "resultado": "parcial_con_fallos" if failed else "OK"}))
    return 2 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

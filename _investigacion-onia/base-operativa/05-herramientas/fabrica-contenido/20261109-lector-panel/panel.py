"""HTML autónomo sin JavaScript, formularios, red automática o mutaciones."""
import argparse
from html import escape
import json
from pathlib import Path
from lector import SOURCES, canonical_url, own_output, write_new


def e(value):
    return escape(str(value), quote=True)


def link(url, label):
    try:
        safe = canonical_url(url)
        if safe not in {s["url"] for s in SOURCES}:
            raise ValueError("URL fuera del catálogo")
        return f'<a href="{e(safe)}" rel="noreferrer noopener">{e(label)} ↗</a>'
    except (ValueError, TypeError):
        return f'<span>{e(label)} · enlace no permitido</span>'


def badge(text, good=False):
    return f'<span class="badge {"good" if good else "pending"}">{e(text)}</span>'


def render(s):
    if s.get("schema") != "onia-lector-panel-v1":
        raise ValueError("Schema de snapshot no admitido")
    public = s.get("fuentes", {})
    items = public.get("items", [])
    scripts = s.get("guiones", [])
    tasks = s.get("tareas", [])
    sources_html = []
    for item in items:
        visible = item.get("fecha_visible") or {}
        news = item.get("tipo_contenido") == "noticia"
        kind = ('Noticia candidata · no seleccionada para guiones' if item.get('elegible_noticia') else 'Candidata con fecha pendiente') if news else 'Guía atemporal · no noticia de hoy'
        date_note = 'Publicación explícita cotejada con fecha visible; precisión de día. Fecha del hecho: anuncio, sin probar despliegue.' if news and item.get('fecha_publicacion') else 'Actualización o fecha visible; no acredita publicación original.'
        sources_html.append(f'''<article class="card source">
          <div class="eyebrow">{e(item['id'])} · {e(item['autor'])} · {e(item['tipo'])}</div>
          <h3>{link(item['url_canonica'], item['titulo'])}</h3>
          {badge(kind)}
          <p>{e(item['resumen'])}</p>
          <dl><dt>Consulta UTC</dt><dd>{e(item['fecha_consulta'])}</dd>
          <dt>Publicación original</dt><dd>{e(item.get('fecha_publicacion') or 'Desconocida')}</dd>
          <dt>Fecha del hecho</dt><dd>{e(item.get('fecha_hecho') or 'Sin hecho noticioso determinado')}</dd>
          <dt>Fecha visible / función</dt><dd>{e(visible.get('valor') or 'Ausente')} · {e(visible.get('texto', ''))}<br>{e(date_note)}</dd></dl>
          <p class="small">{e(item.get('pendiente', ''))}</p>
          <p class="small">{e(item['cobertura'])}</p>
          <details><summary>Huella y procedencia</summary><p class="mono">{e(item['url_original'])}</p>
          <p class="mono">SHA-256 respuesta: {e(item['sha256_respuesta'])}<br>{e(item['bytes_respuesta'])} bytes leídos; HTML remoto no conservado.</p></details>
        </article>''')
    if not sources_html:
        sources_html.append('<p class="empty">Sin fuentes leídas en este recibo. Revisá los fallos; no se presume actualidad ni se inventa un reemplazo.</p>')
    consultations = []
    for c in public.get("consultas", []):
        consultations.append(f'<li><strong>{e(c["fuente"])} · {e(c["resultado"])}</strong> '
                             f'{e(c.get("error", ""))}<br><span class="small">{e(c["consulta_iniciada"])} → {e(c["consulta_finalizada"])}<br>{e(c.get("referencia_previa_sin_lectura_nueva", ""))}</span></li>')
    ideas = ''.join(f'<article class="card"><div class="eyebrow">{e(i["id"])} → {e(i["guion"])} · {e(i["tipo"])}</div>'
                    f'<p>{e(i["texto"])}</p><p class="small">Fuente: {e(", ".join(i["fuentes"]))}. Origen: {e(i["origen"])}</p></article>'
                    for i in s.get("ideas", [])) or '<p class="empty">Sin ideas verificables en este recibo.</p>'
    scripts_html = []
    for g in scripts:
        verified = g.get("integridad") == "verificada"
        review = g.get("revision_tecnica") or {}
        scripts_html.append(f'''<article class="card script">
          <div class="eyebrow">{e(g['id'])} · v1 · {e(g.get('idea', 'Sin idea verificada'))}</div>
          <h3>{e(g.get('titulo', g['id']))}</h3>
          {badge('Borrador · sin aprobación de publicación')}
          {badge('Técnicamente revisado' if verified else 'Evidencia no válida', verified)}
          <p>Revisión editorial: {e(g['revision_editorial'])}.</p>
          <p class="small">{e(g.get('error', 'Texto coincide con el commit revisado y con el manifiesto original.'))}</p>
          <p class="mono">Origen: {e(g['origen'])}<br>SHA-256: {e(g.get('sha256', 'No verificado'))}<br>Commit revisado: {e(review.get('commit', 'No verificado'))}</p>
          <details><summary>Leer guion y sus fuentes</summary><pre>{e(g.get('texto', '') or 'Texto no disponible: primero reconciliar la evidencia.')}</pre></details>
          <details><summary>Pendientes de esta versión</summary><pre>{e(g.get('pendientes', 'Reconciliar evidencia canónica.'))}</pre></details>
        </article>''')
    if not scripts_html:
        scripts_html.append('<p class="empty">Sin guiones verificables en este recibo.</p>')
    tasks_html = []
    for t in tasks:
        review = t.get('revision_tecnica') or {}
        tasks_html.append(f'''<article class="card task">
          <h3>{e(t['id'])}</h3>{badge(t.get('estado', 'Estado no verificable'), t.get('integridad') == 'verificada')}
          <p>Revisión de tarea: <strong>{e(t.get('revision', 'Desconocida'))}</strong> · Integridad: {e(t['integridad'])}</p>
          <p>Revisión técnica del alcance: {e('buena' if review.get('buena') else 'no acreditada en esta proyección')}.</p>
          <p class="small">{e(t.get('error', ''))}</p><p><strong>Próximo paso canónico</strong><br>{e(t['proximo_paso'])}</p>
          <details><summary>Origen canónico y versión</summary><p class="mono">{e(t['origen'])}<br>Actualizado: {e(t.get('actualizado', 'Desconocido'))}<br>SHA-256: {e(t.get('sha256_registro', 'No verificado'))}<br>Commit revisado: {e(review.get('commit', 'Sin revisión'))}</p></details>
        </article>''')
    return f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="no-referrer"><title>Fábrica OnIA · consulta manual</title>
<style>
:root{{font-family:system-ui,sans-serif;color:#182b3a;background:#f2f5f4;line-height:1.6}}
*{{box-sizing:border-box}}body{{margin:0}}a{{color:#075b79;text-underline-offset:3px}}a:focus-visible,summary:focus-visible{{outline:3px solid #a55a00;outline-offset:4px}}
header{{background:#142f40;color:#fff;padding:38px max(22px,calc((100vw - 1160px)/2)) 30px}}header a{{color:#c9eff3}}h1{{font-size:clamp(2rem,4vw,3rem);margin:6px 0}}h2{{font-size:1.55rem;margin:34px 0 12px}}h3{{font-size:1.05rem;line-height:1.4;margin:9px 0 13px;overflow-wrap:anywhere}}p{{margin:12px 0}}
main{{max-width:1204px;margin:auto;padding:22px}}nav{{display:flex;gap:22px;flex-wrap:wrap}}.eyebrow{{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700}}.intro{{max-width:850px;color:#e0eaef}}
.notice{{border-left:5px solid #a55a00;background:#fff3d7;padding:16px 20px;border-radius:6px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:18px}}.tasks{{grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}}
.card{{background:white;border:1px solid #cfdbdc;border-radius:12px;padding:22px;min-width:0}}.badge{{display:inline-block;border-radius:5px;padding:3px 8px;margin:3px 5px 3px 0;font-size:.78rem;font-weight:700}}.good{{background:#d9eee8;color:#174a3e}}.pending{{background:#fff0cb;color:#704100}}
.small{{font-size:.84rem;color:#415663}}.mono{{font: .78rem/1.65 ui-monospace,monospace;overflow-wrap:anywhere}}dl{{font-size:.85rem}}dt{{font-weight:700;margin-top:9px}}dd{{margin:0;overflow-wrap:anywhere}}summary{{cursor:pointer;color:#075b79;font-weight:650;padding:10px 0}}pre{{font: .88rem/1.7 system-ui,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7f7;padding:16px;border-radius:7px;max-width:100%}}.empty{{background:#fff;padding:20px;border:1px dashed #718692}}li{{margin:12px 0;overflow-wrap:anywhere}}footer{{border-top:1px solid #cad7d9;padding:26px 0;margin-top:32px}}code{{overflow-wrap:anywhere}}@media(max-width:480px){{main{{padding:14px}}header{{padding:26px 18px}}.card{{padding:17px}}}}
</style></head><body>
<header><div class="eyebrow">OnIA / fábrica de contenido / sólo lectura</div><h1>Fuentes, ideas y guiones</h1>
<p class="intro">Dos borradores para revisar con sus fuentes y límites. La revisión técnica y el permiso de publicación se muestran por separado.</p>
<nav aria-label="Secciones"><a href="#guiones">Guiones</a><a href="#fuentes">Fuentes</a><a href="#ideas">Ideas</a><a href="#pendientes">Estado y pendientes</a></nav></header>
<main><aside class="notice"><strong>Fotografía manual · no se actualiza sola</strong><br>Generada: {e(s['generado'])}. Reconsultar antes de usar afirmaciones de producto.
<br>Sin aprobación de publicación. No hay scheduler, ingesta recurrente ni Telegram real.</aside>
<section id="guiones"><h2>Guiones reales · borradores</h2><div class="grid">{''.join(scripts_html)}</div></section>
<section id="fuentes"><h2>Fuentes públicas · {len(items)} páginas leídas</h2><div class="grid">{''.join(sources_html)}</div>
<details><summary>Consultas y fallos por fuente</summary><ul>{''.join(consultations) or '<li>Sin consultas registradas.</li>'}</ul></details></section>
<section id="ideas"><h2>Ideas que originaron los guiones</h2><div class="grid">{ideas}</div></section>
<section id="pendientes"><h2>Estado derivado y próximos pasos</h2><p>La autoridad sigue en los JSON canónicos del harness. “Aceptado” describe el alcance técnico de cada entrega; no concede permiso para publicar estos guiones.</p>
<div class="grid tasks">{''.join(tasks_html) or '<p class="empty">Sin tareas verificadas.</p>'}</div></section>
<footer><p>{e(s['alcance'])}</p><p class="mono">Commit de las entradas del repo: {e(s['commit_entradas_repo'])}</p>
<p class="small">Sin botones de aprobación, envíos, cuentas, rastreadores o recursos remotos. Los enlaces oficiales sólo se abren por acción de quien consulta. Los recibos preservan metadatos y resúmenes propios, no artículos íntegros.</p></footer></main></body></html>'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--salida", required=True, type=Path)
    args = parser.parse_args()
    snapshot = json.loads(own_output(args.snapshot).read_text(encoding="utf-8"))
    write_new(args.salida, render(snapshot))

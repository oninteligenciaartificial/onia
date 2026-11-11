"""Panel HTML existente, con consulta estática y revisión local opcional."""
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


def render(s, operativo=None, session=None):
    if s.get("schema") != "onia-lector-panel-v1":
        raise ValueError("Schema de snapshot no admitido")
    if operativo:
        import diseno
        return diseno.render(s, operativo, session)
    form_policy = "self" if session else "none"
    operation_html = render_operation(operativo, session) if operativo else ""
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
          <div class="eyebrow">{e(g['id'])} · {e(g.get('version', 'v1'))} · {e(g.get('idea', 'Sin idea verificada'))}</div>
          <h3>{e(g.get('titulo', g['id']))}</h3>
          {badge('Borrador · sin aprobación de publicación')}
          {badge('Técnicamente revisado' if verified else ('Revisión técnica pendiente' if g.get('integridad') == 'pendiente_revision' else 'Evidencia no válida'), verified)}
          <p>Revisión editorial: {e(g['revision_editorial'])}.</p>
          <p class="small">{e(g.get('error', 'Texto coincide con el commit revisado y con el manifiesto original.'))}</p>
          <p class="mono">Origen: {e(g['origen'])}<br>SHA-256: {e(g.get('sha256', 'No verificado'))}<br>Commit revisado: {e(review.get('commit', 'No verificado'))}</p>
          <details><summary>Leer guion y sus fuentes</summary><pre>{e(g.get('texto', '') or 'Texto no disponible: primero reconciliar la evidencia.')}</pre></details>
          <details><summary>Pendientes de esta versión</summary><pre>{e(g.get('pendientes', 'Reconciliar evidencia canónica.'))}</pre></details>
          {review_form(g.get('target'), operativo, session)}
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
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action '{form_policy}'">
<meta name="referrer" content="same-origin"><title>Fábrica OnIA · consulta manual</title>
<style>
:root{{font-family:system-ui,sans-serif;color:#182b3a;background:#f2f5f4;line-height:1.6}}
*{{box-sizing:border-box}}body{{margin:0;overflow-wrap:anywhere}}a{{color:#075b79;text-underline-offset:3px}}a:focus-visible,summary:focus-visible{{outline:3px solid #a55a00;outline-offset:4px}}
header{{background:#142f40;color:#fff;padding:38px max(22px,calc((100vw - 1160px)/2)) 30px}}header a{{color:#c9eff3}}h1{{font-size:clamp(2rem,4vw,3rem);margin:6px 0}}h2{{scroll-margin-top:18px;font-size:1.55rem;margin:34px 0 12px}}h3{{font-size:1.05rem;line-height:1.4;margin:9px 0 13px;overflow-wrap:anywhere}}p{{margin:12px 0}}
main{{max-width:1204px;margin:auto;padding:22px}}nav{{display:flex;gap:22px;flex-wrap:wrap}}.eyebrow{{font-size:.8rem;letter-spacing:.06em;text-transform:uppercase;font-weight:700}}.intro{{max-width:850px;color:#e0eaef}}
.notice{{border-left:5px solid #a55a00;background:#fff3d7;padding:16px 20px;border-radius:6px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,340px),1fr));gap:18px}}.tasks{{grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr))}}
.card{{background:white;border:1px solid #cfdbdc;border-radius:12px;padding:22px;min-width:0}}.badge{{display:inline-block;border-radius:5px;padding:3px 8px;margin:3px 5px 3px 0;font-size:.78rem;font-weight:700}}.good{{background:#d9eee8;color:#174a3e}}.pending{{background:#fff0cb;color:#704100}}
.small{{font-size:.84rem;color:#415663}}.mono{{font: .78rem/1.65 ui-monospace,monospace;overflow-wrap:anywhere}}dl{{font-size:.85rem}}dt{{font-weight:700;margin-top:9px}}dd{{margin:0;overflow-wrap:anywhere}}summary{{cursor:pointer;color:#075b79;font-weight:650;padding:10px 0}}pre{{font: .88rem/1.7 system-ui,sans-serif;white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7f7;padding:16px;border-radius:7px;max-width:100%}}.empty{{background:#fff;padding:20px;border:1px dashed #718692}}li{{margin:12px 0;overflow-wrap:anywhere}}footer{{border-top:1px solid #cad7d9;padding:26px 0;margin-top:32px}}code{{overflow-wrap:anywhere}}@media(max-width:480px){{main{{padding:14px}}header{{padding:26px 18px}}.card{{padding:17px}}}}
input,textarea,select,button{{font:inherit;max-width:100%;border:1px solid #718692;border-radius:5px;padding:9px}}textarea{{width:100%;min-height:100px}}label{{display:block;margin-top:12px}}button{{background:#075b79;color:white;cursor:pointer;margin-top:12px}}button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible{{outline:3px solid #a55a00;outline-offset:3px}}.flow{{padding-left:22px}}.flow>li{{border-left:3px solid #cfdbdc;padding:0 0 16px 14px}}.history{{border-left:3px solid #a55a00;padding-left:14px}}.calendar{{display:flex;gap:18px;flex-wrap:wrap}}.calendar article{{flex:1;min-width:min(100%,220px)}}.factory-nav{{margin:18px 0;display:flex;gap:14px;flex-wrap:wrap}}
</style></head><body>
<header><div class="eyebrow">OnIA / {'revisión local' if operativo else 'fábrica de contenido / sólo lectura'}</div><h1>{"Fábricas y revisión" if operativo else "Fuentes, ideas y guiones"}</h1>
<p class="intro">{len(scripts)} borradores para revisar con sus fuentes y límites. La revisión técnica y el permiso de publicación se muestran por separado.</p>
<nav aria-label="Secciones">{operation_nav(operativo)}<a href="#guiones">Guiones</a><a href="#fuentes">Fuentes</a><a href="#ideas">Ideas</a><a href="#pendientes">Estado y pendientes</a></nav></header>
<main><aside class="notice"><strong>Fotografía manual · no se actualiza sola</strong><br>Generada: {e(s['generado'])}. Reconsultar antes de usar afirmaciones de producto.
<br>Sin aprobación de publicación. No hay scheduler, ingesta recurrente ni Telegram real.</aside>
{operation_html}
<section id="guiones"><h2>Guiones reales · borradores</h2><div class="grid">{''.join(scripts_html)}</div></section>
<section id="fuentes"><h2>Fuentes públicas · {len(items)} páginas leídas</h2><div class="grid">{''.join(sources_html)}</div>
<details><summary>Consultas y fallos por fuente</summary><ul>{''.join(consultations) or '<li>Sin consultas registradas.</li>'}</ul></details></section>
<section id="ideas"><h2>Ideas que originaron los guiones</h2><div class="grid">{ideas}</div></section>
<section id="pendientes"><h2>Estado derivado y próximos pasos</h2><p>La autoridad sigue en los JSON canónicos del harness. “Aceptado” describe el alcance técnico de cada entrega; no concede permiso para publicar estos guiones.</p>
<div class="grid tasks">{''.join(tasks_html) or '<p class="empty">Sin tareas verificadas.</p>'}</div></section>
<footer><p>{e(s['alcance'])}</p><p class="mono">Commit de las entradas del repo: {e(s['commit_entradas_repo'])}</p>
<p class="small">{"Las observaciones locales quedan pendientes para revisión de Sergio y la coordinadora." if operativo else "Consulta local de recibos y fuentes."} Los enlaces oficiales se abren por acción de quien consulta. Los recibos preservan metadatos y resúmenes propios.</p></footer></main></body></html>'''


def operation_nav(operation):
    if not operation:
        return ''
    return '<a href="#fabricas">Fábricas</a><a href="#calendario">Calendario</a><a href="#cerebro">Cerebro</a>'


def document_link(document):
    label = e(document['ruta'])
    if not document['disponible']:
        return label + ' · archivo pendiente'
    href = document.get('href', '/documento?id=' + document['id'])
    return f'<a href="{e(href)}">{label}</a>'


def review_form(target_id, operation, session):
    if not operation or not target_id:
        return ''
    item = operation['targets'][target_id]
    history = operation.get('histories', {}).get(target_id, [])
    records = []
    for row in history:
        changed = ' · la fuente actual tiene otros bytes' if (
            row['sha256_fuente'] != item['sha256_fuente'] or json.loads(row['original']) != item['original']) else ''
        records.append(f'''<article class="history"><h4>Revisión local v{e(row['version'])} · pendiente{changed}</h4>
        <p>{e(row['fecha'])}</p><p>Motivo<br>{e(row['motivo'])}</p>
        <pre>{e(row['correccion'])}</pre><details><summary>Original conservado de esta revisión</summary>
        <p class="mono">{e(row['fuente'])}<br>SHA-256 de la fuente {e(row['sha256_fuente'])}</p>
        <pre>{e(row['original'])}</pre></details></article>''')
    form = '<p class="small">Para guardar una observación, abrir el modo local indicado en GUIA-REVISION.md.</p>'
    if session:
        version = history[-1]['version'] if history else 0
        form = f'''<form action="/revision" method="post">
        <input type="hidden" name="csrf" value="{e(session['csrf'])}">
        <input type="hidden" name="target" value="{e(target_id)}">
        <input type="hidden" name="source_hash" value="{e(item['huella_revision'])}">
        <input type="hidden" name="version" value="{e(version)}">
        <label>Motivo de la observación<input name="motivo" required maxlength="2000"></label>
        <label>Observación o corrección propuesta<textarea name="correccion" required maxlength="12000"></textarea></label>
        <button type="submit">Guardar revisión pendiente v{version + 1}</button>
        <p class="small">Original conservado. La coordinadora y Sergio revisan la propuesta.</p></form>'''
    return f'''<details id="revision-{e(target_id)}"><summary>Revisar resultado · {len(history)} observaciones</summary>
    {''.join(records)}{form}</details>'''


def export_view(data, operation, session):
    synthetic = '<p class="notice"><strong>ENSAYO SINTÉTICO</strong> · fixture de prueba local</p>' if data['sintetico'] else ''
    steps = []
    for step in data['pasos']:
        evidence = ''.join(f'<li>{document_link(ref)}</li>' for ref in step['evidencias'])
        steps.append(f'''<li><strong>{e(step['nombre'])}</strong> {badge(step['estado'])}
        <ul>{evidence or '<li>Evidencia pendiente de aportar por el productor.</li>'}</ul>
        {review_form(step['target'], operation, session)}</li>''')
    deliveries = ''.join(f'''<article><h4>{e(row['nombre'])}</h4><p>{document_link(row['documento'])}</p>
                         {review_form(row['target'], operation, session)}</article>''' for row in data['entregables'])
    pending = ''.join(f'''<li>{e(row['motivo'])}<br>Responsable {e(row['responsable'])}<br>
                      Siguiente paso · {e(row['siguiente'])}</li>''' for row in data['pendientes'])
    return f'''{synthetic}{badge(data['estado'])}<details class="provenance"><summary>Fuente, fecha y versión del resumen</summary><p class="mono">Resumen del productor generado {e(data['generado'])}<br>
    Export {e(data['ruta_export'])}<br>SHA-256 {e(data['sha256'])}</p>
    <p>Informe o recibo · {document_link(data['documento_fuente'])}</p></details>
    <ol class="flow">{''.join(steps) or '<li>Pasos pendientes de declarar.</li>'}</ol>
    <h4>Entregas</h4>{deliveries or '<p>Entregas pendientes de declarar.</p>'}
    <h4>Bloqueos y pendientes</h4><ul>{pending or '<li>El resumen no declara pendientes adicionales.</li>'}</ul>'''


def render_operation(operation, session):
    factories = []
    for factory in operation['fabricas']:
        exports = factory['exports']
        content = ''.join(export_view(data, operation, session) for data in exports) if exports else (
            '<p>Estado pendiente de recibir en un export validado.</p>'
            '<p>Responsable · coordinadora y productor. Siguiente paso · aportar estado-fabrica.json '
            'y sus evidencias para esta fábrica. La conexión y prueba real quedan pendientes.</p>')
        factories.append(f'''<article class="card" id="fabrica-{e(factory['id'])}">
        <h3>{e(factory['nombre'])}</h3>{content}<details><summary>Documentación existente</summary>
        <p>{document_link(factory['documento'])}</p><p class="small">Antecedente documental con su fecha de origen.</p></details></article>''')
    panel_exports = ''.join(export_view(data, operation, session) for data in operation['exports_panel'])
    calendar = ''.join(f'''<article class="card"><h3>{e(name)}</h3><time datetime="{e(date)}">{e(date[:10])} · {e(date[11:16])}</time></article>'''
                       for name, date in operation['clases'])
    brain_result = operation.get('brain')
    brain_html = '<p>Elegí un tema o uso para consultar el cerebro existente con sus controles de integridad.</p>'
    if brain_result:
        patterns = []
        for row in brain_result['resultados']:
            patterns.append(f'''<article class="card"><h3>{e(row['titulo'])}</h3><p>{e(row['nombre'])} · {e(row['pieza'])}</p>
            <p>{e(row['hecho_documentado'])}</p><p>Inferencia<br>{e(row['inferencia_acotada'])}</p>
            <p>Aplicación propuesta<br>{e(row['propuesta_onia']['aplicacion'])}</p>
            <p>Comprobación pendiente<br>{e(row['propuesta_onia']['comprobacion_pendiente'])}</p>
            <details><summary>Fuente, pasaje y límites heredados</summary><pre>{e(json.dumps(row, ensure_ascii=False, indent=2))}</pre></details></article>''')
        brain_html = f'<p>{e(brain_result["mensaje"])} {e(brain_result["cantidad"])} patrones.</p><div class="grid">{"".join(patterns)}</div>'
    uses = ('ordenar', 'vender', 'ensenar', 'contenido', 'workshop', 'ideas', 'guiones', 'automatizar')
    options = '<option value="">Todos los usos</option>' + ''.join(f'<option value="{use}">{use}</option>' for use in uses)
    brain_form = f'''<form method="get" action="/#cerebro"><label>Tema<input name="tema" maxlength="80" placeholder="oferta, contenido, revision"></label>
    <label>Uso<select name="uso">{options}</select></label><button>Consultar cerebro</button></form>''' if session else (
        '<p>Consulta interactiva disponible en el modo local de revisión.</p>')
    historical = '<p class="notice">Tanda v2 histórica · contiene horarios sustituidos. Revisar una versión nueva del productor antes de usarla para la venta.</p>' if operation.get('tanda_historica') else ''
    batch = operation.get('tanda')
    batch_info = ''
    if batch:
        slots = ''.join(f'<li>{e(g["id"])} · {e(g.get("slot", "slot pendiente"))} · {e(g["titulo"])}</li>' for g in batch['guiones'])
        batch_info = f'<p>Fecha editorial declarada {e(batch["fecha_tanda"])} · cinco piezas T01–T05. Salidas horizontal y vertical pendientes de prueba en esta vista.</p><ul>{slots}</ul>'
    previous = ''.join(f'''<details><summary>Revisión local v{e(row['version'])} · pendiente · {e(row['fuente'])}</summary>
                      <p>Fuente ausente de la selección actual. Original y propuesta conservados.</p>
                      <p>{e(row['fecha'])}</p><p>{e(row['motivo'])}</p><pre>{e(row['correccion'])}</pre>
                      <pre>{e(row['original'])}</pre></details>''' for row in operation.get('revisiones_anteriores', []))
    previous_html = f'<section><h2>Revisiones de fuentes anteriores</h2>{previous}</section>' if previous else ''
    errors = ''.join(f'<p class="notice" role="alert">{e(message)}</p>' for message in operation['errores'])
    saved = '<p class="notice" role="status">Observación guardada · pendiente de revisión.</p>' if operation.get('guardado') else ''
    return f'''{saved}{errors}<section id="fabricas"><h2>Fábricas</h2>
    <p>Resúmenes fechados de productores. El harness conserva la autoridad de las tareas. Cada export conserva su fecha y fuente.</p>
    <nav class="factory-nav" aria-label="Seis fábricas">{''.join(f'<a href="#fabrica-{e(f["id"])}">{e(f["nombre"])}</a>' for f in operation['fabricas'])}</nav>
    <div class="grid">{''.join(factories)}</div>{panel_exports}</section>{previous_html}
    <section id="calendario"><h2>Calendario del workshop</h2><p>America/La_Paz · confirmación de Sergio del 11 de noviembre de 2026.</p>
    <div class="calendar">{calendar}</div><p>Claude de 0 a 100: tu negocio con IA · grupo Bs 50 · VIP Bs 150, 5 cupos, llamada de 30 minutos.</p>
    <p>QR y seguimiento con confirmación manual de cada pago por Sergio. Calendar/Meet y canales reales requieren conciliación y prueba.</p>
    <details><summary>Fuente del calendario y alcance</summary><p>{document_link(operation['decisiones'])}</p>
    <p class="mono">SHA-256 {e(operation['decisiones_sha256'])}</p><p>{document_link(operation['alcance'])}</p></details>
    <h3>Tanda en consulta</h3>{batch_info}{historical}<p class="mono">{e(operation.get('tanda_ruta', 'Tanda pendiente'))}</p>
    <p><a href="#guiones">Abrir los cinco resultados y registrar una revisión</a></p></section>
    <section id="cerebro"><h2>Cerebro editorial existente</h2><p>{document_link(operation['cerebro_doc'])}</p>{brain_form}{brain_html}
    <p class="small">Catálogo documental del 9 de noviembre. Cada consulta valida fuentes y pasajes conservados.</p></section>'''


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--salida", required=True, type=Path)
    args = parser.parse_args()
    snapshot = json.loads(own_output(args.snapshot).read_text(encoding="utf-8"))
    write_new(args.salida, render(snapshot))

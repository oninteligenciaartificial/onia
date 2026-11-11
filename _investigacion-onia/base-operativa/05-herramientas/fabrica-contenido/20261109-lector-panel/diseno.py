"""Propuesta 1 sobre el render del panel. Interacción nativa por enlaces, radio y details."""
import base64
from datetime import datetime
from functools import lru_cache
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import panel

ROOT = Path(__file__).resolve().parent
ICONS = ('home', 'building-factory-2', 'calendar', 'brain', 'movie', 'file-description',
         'video', 'bolt', 'brand-whatsapp', 'code', 'stack-2', 'chevron-right', 'clock',
         'circle', 'circle-check-filled', 'circle-dashed', 'brand-youtube', 'arrow-left')
FACTORY_STYLE = {
    'guiones': ('file-description', '#d99119', ('Fuentes', 'Ideas', 'Guiones', 'Revisión'), 'Revisar tanda'),
    'edicion': ('video', '#398fdf', ('Recibir', 'Transcribir', 'Montar', 'Revisar'), 'Ver pasos'),
    'automatizaciones': ('bolt', '#7b60ad', ('Entrada', 'Proceso', 'Resultado'), 'Ver pasos'),
    'whatsapp': ('brand-whatsapp', '#339c42', ('Consulta', 'QR', 'Confirmación manual', 'Acceso'), 'Ver preparación'),
    'codigo': ('code', '#3f90d0', ('Encargo', 'Construcción', 'Pruebas', 'Revisión'), 'Ver pasos'),
    'plataforma': ('stack-2', '#9b9f9f', ('Definir', 'Construir', 'Probar', 'Publicar'), 'Ver pasos'),
}
e = panel.e


def icon(name, extra=''):
    if name not in ICONS:
        raise ValueError('Icono fuera de la biblioteca local')
    return f'<span class="icon icon-{name} {e(extra)}" aria-hidden="true"></span>'


@lru_cache(maxsize=1)
def styles():
    font = base64.b64encode((ROOT / 'recursos/inter/inter-latin.woff2').read_bytes()).decode('ascii')
    css = f'@font-face{{font-family:Inter;font-style:normal;font-weight:100 900;font-display:swap;src:url(data:font/woff2;base64,{font}) format("woff2")}}\n'
    css += (ROOT / 'diseno.css').read_text()
    for name in ICONS:
        raw = (ROOT / 'recursos/tabler' / (name + '.svg')).read_bytes()
        encoded = base64.b64encode(raw).decode('ascii')
        css += f'.icon-{name}{{mask-image:url("data:image/svg+xml;base64,{encoded}")}}\n'
    for key in FACTORY_STYLE:
        for condition in (f'#fabrica-{key}:target', f'#detalle-{key}:target', f'#detalle-{key} :target'):
            css += f'body:has({condition}) .inspector-main{{display:none}}\n'
            css += f'body:has({condition}) .inspector-main[data-for="{key}"]{{display:block}}\n'
            css += f'body:has({condition}) #detalle-{key}{{display:block}}\n'
    for section in ('hoy', 'calendario', 'cerebro', 'montaje', 'guiones', 'fuentes', 'ideas', 'pendientes'):
        css += f'body:has(#{section}:target) .nav-fabricas{{background:transparent;font-weight:400}}\n'
        css += f'body:has(#{section}:target) .nav-{section}{{background:#f6e9cf;font-weight:700}}\n'
    return css


def provenance(content, label='Procedencia y versión'):
    return f'<details class="provenance"><summary>{e(label)}</summary>{content}</details>'


def step_strip(factory):
    """Se completan círculos únicamente con un paso completado en un export validado."""
    exports = factory['exports']
    if exports:
        steps = [(s['nombre'], s['estado']) for s in exports[0]['pasos']]
    else:
        steps = [(name, 'pendiente') for name in FACTORY_STYLE[factory['id']][2]]
    items = []
    for name, state in steps:
        completed = state == 'completado'
        symbol = 'circle-check-filled' if completed else 'circle'
        items.append(f'<li class="step {"completed" if completed else ""}">{icon(symbol)}'
                     f'<span class="step-label">{e(name)}</span><span class="sr-only">{e(state)}</span></li>')
    return '<ol class="steps" aria-label="Pasos declarados">' + ''.join(items) + '</ol>'


def factory_rows(operation):
    rows = []
    for factory in operation['fabricas']:
        key = factory['id']
        symbol, color, _, action = FACTORY_STYLE[key]
        exports = factory['exports']
        status = 'Resumen pendiente de recibir'
        if exports:
            status = exports[0]['estado'].replace('_', ' ')
            if exports[0]['sintetico']:
                status = 'ENSAYO SINTÉTICO · ' + status
        elif key == 'guiones' and operation.get('tanda'):
            status = '5 borradores históricos · por revisar'
        rows.append(f'''<article class="factory-row" id="fabrica-{e(key)}" style="--factory-color:{color}">
          <span class="factory-symbol">{icon(symbol)}</span><div><h3>{e(factory['nombre'])}</h3>
          <p class="factory-status">{e(status)}</p></div>{step_strip(factory)}
          <a class="row-action" href="#fabrica-{e(key)}">{e(action)}{icon('chevron-right')}</a></article>''')
    return '<div class="factory-list factory-nav">' + ''.join(rows) + '</div>'


def factory_details(operation, session):
    sections = []
    for factory in operation['fabricas']:
        exports = factory['exports']
        content = ''.join(panel.export_view(data, operation, session) for data in exports)
        if not exports:
            content = '<p>Estado pendiente de recibir en un export validado.</p><p class="small">El productor y la coordinadora deben aportar el resumen fechado y sus evidencias.</p>'
        sections.append(f'''<section class="factory-details" id="detalle-{e(factory['id'])}"><h2>{e(factory['nombre'])}</h2>
        <div class="doc-block">{content}{provenance(panel.document_link(factory['documento']), 'Documentación de origen')}</div></section>''')
    return ''.join(sections)


def inspector(operation):
    batch = operation.get('tanda')
    scripts = batch['guiones'] if batch else []
    rows = []
    for script in scripts:
        rows.append(f'''<li><a href="#guion-{e(script['id'])}"><span class="result-symbol">{icon('file-description')}</span>
        <span class="result-copy"><strong>{e(script['id'])} · {e(script.get('slot', 'borrador'))}</strong>
        <small>{e(script['titulo'])}</small></span>{icon('chevron-right', 'chevron')}</a></li>''')
    historical = '<p class="history-note">Tanda v2 histórica · horarios sustituidos. Revisar antes de usar para la venta.</p>' if operation.get('tanda_historica') else ''
    date = batch['fecha_tanda'] if batch else 'pendiente'
    version = 'v2 histórica' if operation.get('tanda_historica') else 'versión declarada'
    source = f'<p class="small">Fecha editorial {e(date)}</p>' + provenance(
        f'<p>{e(operation.get("tanda_ruta", "Paquete pendiente"))}</p>'
        + ''.join(f'<p class="mono">{e(g["id"])} · SHA-256 {e(g.get("sha256", "pendiente"))}<br>{e(g["origen"])}</p>' for g in scripts))
    changes = '<p class="small">Las correcciones locales quedan pendientes para Sergio y la coordinadora.</p>'
    histories = operation.get('histories', {})
    history_count = sum(len(history) for history in histories.values())
    changes += f'<p class="small">{history_count} observaciones en la selección actual.</p><a class="secondary-link" href="#guiones">Abrir textos y versiones</a>'
    result = f'''<div class="inspector-main" data-for="guiones"><p class="inspector-title">Tanda en consulta</p>
    <h2>{len(scripts)} guiones · {e(version) if scripts else 'pendiente'}</h2>
    <p class="status-chip">{icon('clock')}Pendiente de revisión</p>{historical}
    <fieldset class="inspector-tabs"><legend class="sr-only">Vista del inspector</legend>
    <input class="tab-radio" type="radio" id="tab-resultado" name="inspector" checked>
    <input class="tab-radio" type="radio" id="tab-fuentes" name="inspector">
    <input class="tab-radio" type="radio" id="tab-cambios" name="inspector">
    <div class="tab-controls"><label for="tab-resultado">Resultado</label><label for="tab-fuentes">Fuentes</label><label for="tab-cambios">Cambios</label></div>
    <div class="tab-pane tab-resultado"><ul class="result-list">{''.join(rows) or '<li>Paquete editorial pendiente.</li>'}</ul></div>
    <div class="tab-pane tab-fuentes">{source}</div><div class="tab-pane tab-cambios">{changes}</div></fieldset>
    <a class="button inspector-cta" href="#guiones">Abrir guiones {icon('chevron-right')}</a></div>'''
    for factory in operation['fabricas'][1:]:
        key = factory['id']
        data = factory['exports']
        state = data[0]['estado'].replace('_', ' ') if data else 'Resumen pendiente'
        result += f'''<div class="inspector-main inspector-other" data-for="{e(key)}"><p class="inspector-title">Resultado de fábrica</p>
        <h2>{e(factory['nombre'])}</h2><p class="status-chip">{icon('clock')}{e(state)}</p>
        <p>Consultá los pasos, entregas y requisitos documentados de esta fábrica.</p>
        <a class="button" href="#detalle-{e(key)}">Abrir pasos {icon('chevron-right')}</a>
        {provenance(panel.document_link(factory['documento']), 'Documentación existente')}</div>'''
    return f'<aside class="inspector" aria-label="Inspector de resultados">{result}</aside>'


def script_cards(snapshot, operation, session):
    cards = []
    for g in snapshot.get('guiones', []):
        fields = ('origen', 'version', 'sha256', 'bytes', 'integridad', 'revision_tecnica', 'error', 'pendientes')
        metadata = {key: g[key] for key in fields if key in g}
        info = '<pre>' + e(json.dumps(metadata, ensure_ascii=False, indent=2)) + '</pre>'
        verified = g.get('integridad') == 'verificada'
        technical = 'Técnicamente revisado' if verified else 'Revisión técnica pendiente'
        cards.append(f'''<article class="script" id="guion-{e(g['id'])}"><h3>{e(g['id'])} · {e(g.get('titulo', g['id']))}</h3>
        {panel.badge('Borrador · sin aprobación de publicación')}{panel.badge(technical, verified)}
        <p>Revisión editorial · {e(g.get('revision_editorial', 'pendiente'))}</p>
        <details><summary>Leer guion y sus fuentes</summary><pre>{e(g.get('texto', 'Texto pendiente'))}</pre></details>
        {provenance(info)}{panel.review_form(g.get('target'), operation, session)}</article>''')
    return '<div class="scripts">' + ''.join(cards) + '</div>'


def brain_view(operation, session):
    content = '<p class="small">Consultá los patrones del cerebro editorial por tema y uso.</p>'
    if session:
        uses = ('ordenar', 'vender', 'ensenar', 'contenido', 'workshop', 'ideas', 'guiones', 'automatizar')
        options = '<option value="">Todos los usos</option>' + ''.join(f'<option>{use}</option>' for use in uses)
        content += f'''<form class="brain-form" method="get" action="/#cerebro"><div class="fields">
        <label>Tema<input name="tema" maxlength="80" placeholder="oferta, revision, contenido"></label>
        <label>Uso<select name="uso">{options}</select></label></div><button>Consultar cerebro</button></form>'''
    else:
        content += '<p class="fallback-note">La consulta interactiva se abre con el servidor local de GUIA-REVISION-DISENO.md.</p>'
    brain = operation.get('brain')
    if brain:
        content += f'<p class="brain-result">{e(brain["mensaje"])} {e(brain["cantidad"])} patrones.</p>'
        for row in brain['resultados']:
            content += f'''<article class="brain-card"><h3>{e(row['titulo'])}</h3><p>{e(row['nombre'])} · {e(row['pieza'])}</p>
            <p>{e(row['hecho_documentado'])}</p><p>Inferencia · {e(row['inferencia_acotada'])}</p>
            <p>Aplicación propuesta · {e(row['propuesta_onia']['aplicacion'])}</p>
            <p>Comprobación pendiente · {e(row['propuesta_onia']['comprobacion_pendiente'])}</p>
            {provenance('<pre>' + e(json.dumps(row, ensure_ascii=False, indent=2)) + '</pre>', 'Fuente, pasaje y límites heredados')}</article>'''
    return content + provenance(panel.document_link(operation['cerebro_doc']))


def classes(operation):
    labels = ('Vie 13', 'Sáb 14', 'Lun 16')
    times = ''.join(f'<time datetime="{e(date)}">{labels[i]} · {e(date[11:16])}</time>' for i, (_, date) in enumerate(operation['clases']))
    return f'''<div class="classes-strip"><strong class="classes-label">{icon('calendar')}Próximas clases</strong>
    <p class="class-workshop">Claude de 0 a 100: tu negocio con IA<small>Hora de La Paz</small></p><div class="class-times">{times}</div></div>'''


def render(snapshot, operation, session=None):
    generated = datetime.fromisoformat(operation['generado']).astimezone(ZoneInfo('America/La_Paz'))
    weekdays = ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo')
    months = ('ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic')
    date_label = f'{weekdays[generated.weekday()]} {generated.day} {months[generated.month - 1]} {generated.year}'
    nav = [('hoy', 'home', 'Hoy'), ('fabricas', 'building-factory-2', 'Fábricas'), ('calendario', 'calendar', 'Calendario'),
           ('cerebro', 'brain', 'Cerebro'), ('montaje', 'movie', 'Sala de montaje')]
    navigation = ''.join(f'<a href="#{key}" class="nav-{key}">{icon(symbol)}<span>{label}</span></a>' for key, symbol, label in nav)
    errors = ''.join(f'<p class="notice" role="alert">{e(message)}</p>' for message in operation['errores'])
    saved = '<p class="status-message" role="status">Observación guardada · pendiente de revisión.</p>' if operation.get('guardado') else ''
    historical = '<p class="notice">Tanda v2 histórica · horarios sustituidos. Revisar antes de usar para la venta.</p>' if operation.get('tanda_historica') else ''
    state = ''.join(panel.export_view(data, operation, session) for data in operation['exports_panel'])
    previous = ''.join(f'''<details><summary>Revisión local v{e(row['version'])} · pendiente</summary><p>{e(row['motivo'])}</p>
                    <pre>{e(row['correccion'])}</pre>{provenance('<pre>' + e(row['original']) + '</pre>', 'Original conservado')}</details>'''
                       for row in operation.get('revisiones_anteriores', []))
    previous = f'<h3>Revisiones de fuentes anteriores</h3>{previous}' if previous else ''
    calendar_source = provenance(panel.document_link(operation['decisiones']) + f'<p class="mono">SHA-256 {e(operation["decisiones_sha256"])}</p>' + panel.document_link(operation['alcance']))
    title = '<h1>Tu fábrica, paso a paso</h1><p class="subtitle">Entradas claras. Resultados revisables.</p>'
    licenses = provenance('<pre>' + e((ROOT / 'recursos/tabler/LICENSE').read_text()) + '</pre><pre>'
                          + e((ROOT / 'recursos/inter/OFL.txt').read_text()) + '</pre>', 'Licencias de iconos y tipografía')
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="referrer" content="same-origin"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; font-src data:; style-src 'unsafe-inline'; base-uri 'none'; form-action '{'self' if session else 'none'}'">
    <title>ONIA · Fábricas y revisión</title><style>{styles()}</style></head><body>
    <header class="topbar"><a class="brand" href="#fabricas"><strong>ONIA</strong><span class="slash">/</span><span>Fábricas</span></a>
    <time class="snapshot-date" datetime="{e(operation['generado'])}">{e(date_label)}</time><span class="context-label">Consulta local · fuentes fechadas</span></header>
    <div class="app-layout"><aside class="sidebar"><nav aria-label="Secciones">{navigation}</nav></aside>
    <main class="workspace">{saved}{errors}<div class="work-grid"><div class="main-content">
    <section class="screen" id="fabricas">{title}{factory_rows(operation)}{factory_details(operation, session)}</section>
    <section class="screen" id="hoy"><h1>Hoy</h1><p class="subtitle">Preparar la revisión del workshop</p>
    <article class="info-card"><h3>Tanda en consulta</h3><p>{len(snapshot.get('guiones', []))} borradores para revisar</p>{historical}
    <a class="button" href="#guiones">Abrir guiones {icon('chevron-right')}</a></article>
    <article class="info-card"><h3>Decisiones y pendientes</h3><p>QR y seguimiento. Sergio confirma cada pago.</p>
    <a class="secondary-link" href="#pendientes">Ver entregas y bloqueos</a></article></section>
    <section class="screen" id="guiones"><h1>Guiones en revisión</h1><p class="subtitle">Texto, fuentes y correcciones locales</p>{historical}
    {script_cards(snapshot, operation, session)}<a class="secondary-link" href="#fabricas">{icon('arrow-left')}Volver a fábricas</a></section>
    <section class="screen" id="calendario"><h1>Calendario</h1><p class="subtitle">Workshop · America/La_Paz</p>
    <article class="info-card"><h3>Horarios confirmados por Sergio</h3><p>Confirmación documental del 11 de noviembre de 2026.</p>
    <p>13 nov · 20:00 / 14 nov · 14:00 / 16 nov · 20:00</p><p>Grupo Bs 50 · VIP Bs 150 · 5 cupos · llamada de 30 minutos.</p>
    <p>Calendar/Meet y canales reales requieren conciliación y prueba.</p>{calendar_source}</article>
    <article class="info-card"><h3>Fecha editorial de la tanda</h3><p>{e(operation['tanda']['fecha_tanda'] if operation.get('tanda') else 'Pendiente')}</p>
    {historical}<a class="secondary-link" href="#guiones">Revisar los cinco resultados</a></article></section>
    <section class="screen" id="cerebro"><h1>Cerebro editorial</h1><p class="subtitle">Patrones, pasajes y criterios recuperables</p>{brain_view(operation, session)}</section>
    <section class="screen" id="montaje"><h1>Sala de montaje</h1><p class="subtitle">Preparación y requisitos de edición</p>
    <article class="info-card"><h3>Recorrido audiovisual pendiente</h3><p>Falta conectar la grabación y los resultados del editor a esta vista.</p>
    <p>La revisión de audio, encuadre y variantes horizontal/vertical corresponde a los siguientes pasos.</p>
    <a class="button" href="#detalle-edicion">Ver pasos de edición {icon('chevron-right')}</a></article></section>
    <section class="screen" id="fuentes"><h1>Fuentes</h1><article class="info-card"><p>La procedencia de cada guion está en su texto y sus detalles de versión.</p>
    <a class="button" href="#guiones">Abrir textos y fuentes</a>{provenance('<p>' + e(operation.get('tanda_ruta', 'Paquete pendiente')) + '</p>')}</article></section>
    <section class="screen" id="ideas"><h1>Ideas de la tanda</h1>{''.join('<article class="info-card"><h3>' + e(g['id']) + '</h3><p>' + e(g.get('idea', 'Idea pendiente')) + '</p></article>' for g in snapshot.get('guiones', []))}</section>
    <section class="screen" id="pendientes"><h1>Entregas y bloqueos</h1><p class="subtitle">Resúmenes fechados para la coordinadora</p>
    <div class="doc-block">{state or '<p>Resumen del panel pendiente de recibir.</p>'}</div>{previous}</section>
    </div>{inspector(operation)}</div>{classes(operation)}
    <p class="vlog-note">{icon('brand-youtube')}Vlog diario · se publica entero, fuera del montaje.</p>
    <details class="delivery-summary"><summary>Procedencia de esta consulta</summary><p class="small">Generada {e(operation['generado'])} · America/La_Paz.</p>
    <p class="small">Resúmenes de productores. El harness conserva la autoridad de las tareas.</p><p class="mono">Commit de las entradas {e(snapshot.get('commit_entradas_repo', 'Sin anclar'))}</p>
    <p class="small">{e(snapshot.get('alcance', 'Consulta local'))}</p>{calendar_source}{licenses}</details></main></div></body></html>'''

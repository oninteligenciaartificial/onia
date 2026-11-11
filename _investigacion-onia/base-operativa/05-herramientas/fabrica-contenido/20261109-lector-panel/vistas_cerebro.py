"""Vistas de fuentes, estrategias y versiones locales dentro de Propuesta 1."""
import panel

e = panel.e


def knowledge(operation):
    data = operation.get('conocimiento')
    if not data:
        return ''
    rows = ''.join(f'<tr><th scope="row">{e(name)}</th><td>{e(value)}</td></tr>' for name,value in data['decisiones'])
    rules = ''.join(f'<article class="info-card"><h3>Regla aprobada documentada</h3><pre>{e(row["texto"])}</pre><p>{panel.document_link(row["documento"])}</p></article>' for row in data['reglas'])
    sources = ''.join(f'''<details class="provenance"><summary>{e(row['documento']['ruta'].split('/')[-1])} · {e(row['fecha_documental'])}</summary>
        <p>{panel.document_link(row['documento'])}</p><p class="mono">SHA-256 {e(row['sha256'])}<br>{e(row['bytes'])} bytes</p></details>''' for row in data['fuentes'])
    return f'''<article class="info-card"><h2>Decisiones de negocio vigentes</h2><p>Confirmaciones documentadas de Sergio. Los cambios de precios, fechas o roles se solicitan como decisión canónica.</p>
    <div class="table-wrap"><table class="knowledge-table"><tbody>{rows}</tbody></table></div></article>
    <h2>Fuentes y versiones</h2><p class="small">Selección de documentos operativos permitidos y del cerebro editorial de referentes.</p>{sources}
    <h2 class="section-gap">Reglas aprendidas y aprobadas</h2>{rules or '<p>Regla aprobada pendiente de documentar.</p>'}
    <p class="small">Las sugerencias de esta interfaz conservan su revisión pendiente en Correcciones.</p>'''


def strategies(operation, session=None):
    data = operation.get('estrategias', {'estado':'pendiente'})
    if data['estado'] != 'disponible':
        return f'''<article class="info-card"><h2>Productor pendiente</h2><p>{e(data.get('motivo', 'Export versionado pendiente de recibir.'))}</p>
        <details class="provenance"><summary>Contrato esperado</summary><p>{e(data.get('ruta_esperada', 'Índice pendiente'))}</p>
        <p>onia-estrategias-v1 · export-estrategias-v1.json, estrategias.schema.json y fuentes.json del productor.</p></details></article>'''
    output = f'<p class="small">Export generado {e(data["generado"])} · estrategia actual {e(data["actual"])}</p>'
    output += '<details class="provenance"><summary>Índice, fecha y versión del productor</summary>' + panel.document_link(data['documento']) + '<p class="mono">SHA-256 ' + e(data['sha256']) + '</p></details>'
    if data.get('fuentes_requieren_conciliacion'):
        output += '<p class="notice">Fuentes técnicas modificadas desde la lectura del productor. Conciliación pendiente · ' + e(', '.join(data['fuentes_requieren_conciliacion'])) + '</p>'
    output += '<p class="small">Las métricas reales conservan el valor desconocido declarado por el productor. Los escenarios son propuestas de cálculo.</p>'
    for row in data['estrategias']:
        label = 'Actual · ' if row['id'] == data['actual'] else 'Biblioteca · '
        if row.get('propuesta_futura'):
            label = 'Propuesta futura · '
        actions = []
        for action in row['acciones']:
            refs = []
            for relative in action['piezas'] + action['evidencias']:
                entry = next(({'id':key,'ruta':doc['ruta'],'disponible':True} for key,doc in operation['documents'].items() if doc['ruta']==relative), None)
                if entry:
                    # Las rutas de documentos se revalidan al abrirlas en el servidor.
                    import lector
                    entry['disponible'] = (lector.BASE / relative).is_file()
                    stored = operation['documents'][entry['id']]
                    if 'href' in stored:
                        entry['href'] = stored['href']
                    refs.append(panel.document_link(entry))
            actions.append(f'<li><strong>{e(action["nombre"])}</strong> · {e(action["estado"])}<p>Responsable {e(action["responsable"])}</p><p>Dependencias · {e(", ".join(action["dependencias"]) or "Sin dependencias declaradas")}</p><p>{"<br>".join(refs) or "Evidencia pendiente"}</p></li>')
        target_id = row['target']
        href = '/?objetivo=' + target_id + '#correcciones' if session else '#correcciones'
        pieces = ''.join(f'''<details><summary>{e(piece['id'])} · {e(piece['titulo'])} · {e(piece['estado'])}</summary><pre>{e(piece['texto'])}</pre>
                        <a class="secondary-link" href="{'/?objetivo=' + e(piece['target']) + '#correcciones' if session else '#correcciones'}">Corregir esta pieza</a></details>''' for piece in row.get('piezas', []))
        output += f'''<article class="info-card"><h2>{e(row['titulo'])}</h2><p>{e(label)}{e(row['estado'])} · v{e(row['version'])}</p>
        <p>{e(row['diagnostico'])}</p><p>Audiencia · {e(row['audiencia'])}</p><p>Oferta · {e(row['oferta'])}</p>
        <p>Evidencia declarada · {e(' / '.join(row.get('evidencia_declarada', [])))}</p>
        <ol>{''.join(actions)}</ol>{pieces}<details class="provenance"><summary>Fuente y versión</summary>{panel.document_link(row['documento'])}</details>
        <a class="secondary-link" href="{e(href)}">Corregir esta estrategia</a></article>'''
    return output


def corrections(operation, session):
    output = '<p class="small">Guardá una sugerencia con motivo y alcance. Después podés crear una versión local de una pieza editable o exportar una solicitud concreta a la coordinadora.</p>'
    chosen = operation.get('correction_target')
    if chosen:
        form = panel.review_form(chosen, operation, session)
        form = form.replace('id="revision-' + chosen + '"', 'id="correccion-' + chosen + '"', 1)
        output += '<article class="info-card"><h2>' + e(operation['targets'][chosen]['nombre']) + '</h2>' + form + '</article>'
    output += '<div class="correction-links">'
    for name,key in operation.get('context_targets', {}).items():
        href = '/?objetivo=' + key + '#correcciones' if session else '#correcciones'
        output += f'<a class="secondary-link" href="{e(href)}">Corregir {e(operation["targets"][key]["nombre"])}</a>'
    output += '</div><h2 class="section-gap">Versiones locales</h2>'
    for row in operation.get('versiones_locales', []):
        output += f'''<article class="info-card"><h3>Versión local v{e(row['version'])} · pendiente de revisión</h3><p>{e(row['motivo'])}</p>
        <pre>{e(row['texto'])}</pre><p><a href="/version?id={e(row['id'])}">Previsualizar antes y después</a></p>
        <a class="secondary-link" href="/?objetivo={e(row['target_local'])}#correcciones">Corregir esta versión local</a></article>'''
    if not operation.get('versiones_locales'):
        output += '<p class="small">Todavía no hay versiones locales aplicadas.</p>'
    output += '<h2 class="section-gap">Solicitudes de coordinación</h2>'
    for row in operation.get('solicitudes', []):
        output += f'<p><a class="secondary-link" href="/solicitud?id={e(row["id"])}">{e(row["id"])} · pendiente de coordinación</a></p>'
    return output


def section_actions(html, operation, session):
    """Cada pantalla disponible ofrece el mismo acceso a su objetivo versionado."""
    targets = operation.get('context_targets', {})
    for section,key in targets.items():
        marker = f'<section class="screen" id="{section}">'
        href = '/?objetivo=' + key + '#correcciones' if session else '#correcciones'
        link = f'<a class="section-correct" href="{e(href)}">Corregir esta sección</a>'
        html = html.replace(marker, marker + link, 1)
    return html


def capabilities(operation):
    rows = [('Anuncios Meta y VSL','Guiones y calendario','guiones'),
            ('Recursos con IA','Guiones y calendario','guiones'),
            ('Edición horizontal y vertical','Edición de video','edicion'),
            ('WhatsApp, Instagram y Facebook','Automatizaciones y WhatsApp','whatsapp')]
    output = ''
    for name,owner,key in rows:
        factory = next(row for row in operation['fabricas'] if row['id']==key)
        state = ', '.join(row['estado'] for row in factory['exports']) or 'Resumen del productor pendiente'
        drafts = ''
        if name == 'Anuncios Meta y VSL' and operation.get('estrategias', {}).get('estado') == 'disponible':
            pieces = operation['estrategias']['estrategias'][0].get('piezas', [])
            available = [piece for piece in pieces if piece['id'] in ('A01','A02','VSL01')]
            drafts = '<p>Borradores documentados · ' + e(', '.join(piece['titulo'] for piece in available)) + '</p><a class="secondary-link" href="#estrategias">Abrir piezas de estrategia</a>'
        output += f'''<article class="info-card"><h2>{e(name)}</h2><p>Fábrica · {e(owner)}</p><p>{e(state)}</p>
        {drafts}
        <p>La evidencia de producción y del canal real debe aportarla el productor. Las generaciones con gasto y las activaciones requieren su autorización aplicable.</p>
        <a class="secondary-link" href="#detalle-{e(key)}">Abrir pasos y evidencia disponibles</a>
        <details class="provenance"><summary>Documentación existente</summary>{panel.document_link(factory['documento'])}</details></article>'''
    return output

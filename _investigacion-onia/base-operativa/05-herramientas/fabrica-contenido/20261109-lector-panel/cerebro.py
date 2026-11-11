"""Fuentes documentadas y contrato acotado de estrategias. Recuperación offline."""
import json

import lector
import operacion as op

STRATEGY_ROOT = '01-negocio/estrategias-operativas-20261111'
STRATEGY_INDEX = STRATEGY_ROOT + '/export-estrategias-v1.json'
RULES = '04-operacion-agentes/reglas-comunes.md'
PLAN = '05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md'
SOURCES = (op.DECISIONS, RULES, PLAN, op.BRAIN_ROOT + '/catalogo.json', op.BRAIN_ROOT + '/GUIA-APLICADA.md')
SECTIONS = {'hoy':'Hoy', 'fabricas':'Fábricas', 'calendario':'Calendario', 'cerebro':'Cerebro',
            'montaje':'Sala de montaje', 'guiones':'Guiones', 'fuentes':'Fuentes', 'ideas':'Ideas',
            'pendientes':'Entregas y bloqueos', 'estrategias':'Estrategias', 'capacidades':'Anuncios, VSL, IA y canales'}


def source(path, model):
    raw = op.read_relative(path, [path])
    return {'documento': op.document(path, [path], model['documents']), 'sha256': lector.sha(raw),
            'bytes': len(raw), 'fecha_documental': '2026-11-11' if path in (op.DECISIONS, RULES, PLAN) else '2026-11-09',
            'texto': raw.decode('utf-8')}


def strategies(model, index_path=STRATEGY_INDEX):
    from jsonschema import Draft202012Validator, FormatChecker
    from jsonschema.exceptions import SchemaError
    op.require(index_path == STRATEGY_INDEX, 'Export de estrategias fuera de la ruta precisa')
    raw = op.read_relative(index_path, [STRATEGY_ROOT])
    data = json.loads(raw)
    schema = json.loads(op.read_relative(STRATEGY_ROOT + '/estrategias.schema.json', [STRATEGY_ROOT]))
    # El contrato v1 usa un esquema local autocontenido. Nunca resolver referencias de red.
    encoded_schema = json.dumps(schema)
    op.require(not any('"' + key + '"' in encoded_schema for key in ('$ref','$dynamicRef','$recursiveRef')),
               'Referencias de esquema externas rechazadas')
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        raise ValueError('Esquema de productor inválido') from None
    op.require(Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(data), 'Schema de estrategias inválido')
    op.require(data.get('schema') == 'onia-estrategias-v1' and data.get('version_export') == 1
               and data.get('raiz') == STRATEGY_ROOT, 'Contrato de estrategias inválido')
    workshop = data['workshop']
    op.require((workshop['precio_grupo_Bs'], workshop['precio_vip_Bs'], workshop['capacidad_vip'], workshop['vip_minutos'])
               == (50,150,5,30), 'Oferta requiere nueva decisión explícita')
    op.require([row['inicio'] for row in workshop['clases']] == [row[1] for row in model['clases']], 'Fechas distintas de la decisión vigente')
    sources_path = data['fuentes_documento']
    op.require(sources_path == STRATEGY_ROOT + '/fuentes.json', 'Fuentes de estrategias fuera de contrato')
    sources = json.loads(op.read_relative(sources_path, [STRATEGY_ROOT]))
    allowed_sources = set(SOURCES) | {
        '01-negocio/workshop-20261108/noche-20261109/CLASE1-PRIMEROS10MIN.md',
        '02-contenido/formatos-onia.md',
        '04-operacion-agentes/ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md',
        op.PANEL_ROOT + '/operacion.py', op.PANEL_ROOT + '/GUIA-REVISION.md',
        '01-negocio/preparar-oferta-y-embudo/SKILL.md',
        '05-herramientas/compartibles/skills/preparar-campana-meta/SKILL.md',
        '04-operacion-agentes/BITACORA-BOSS.md'}
    source_ids, divergences = set(), []
    for row in sources['fuentes']:
        op.require(row['ruta'] in allowed_sources and row['id'] not in source_ids, 'Fuente de estrategia no permitida')
        source_ids.add(row['id'])
        raw_source = op.read_relative(row['ruta'], [row['ruta']])
        matches = lector.sha(raw_source) == row['sha256'] and len(raw_source) == row['bytes']
        if row['id'] == 'S01':
            op.require(row['ruta'] == op.DECISIONS and matches, 'Decisión comercial cambió; conciliar con productor')
        elif not matches:
            divergences.append(row['id'])
    op.require('S01' in source_ids, 'S01 es obligatoria para cotejar la decisión comercial vigente')
    op.require(set(data['fuentes_ids']) == source_ids, 'Índice de fuentes inconsistente')
    documents, targets = {}, {}
    def reference(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('documento','fuentes_documento'):
                    op.document(child, [STRATEGY_ROOT], documents)
                elif key == 'fuentes' and isinstance(child, list):
                    op.require(set(child) <= source_ids, 'ID de fuente desconocido')
                reference(child)
        elif isinstance(value, list):
            for child in value:
                reference(child)
    reference(data)
    op.require(not any(data['permisos'].values()), 'Permisos comerciales fuera de este export')
    results = []
    fingerprint = lector.sha(raw)
    for item in [workshop, *data['biblioteca']]:
        op.identifier(item['id'])
        op.require(type(item['version']) is int and item['version'] > 0, 'Versión inválida')
        current = item is workshop
        op.require(item['estado'] == ('borrador_preparado' if current else 'propuesto'), 'Aprobación no acreditada')
        actions = []
        for action in item.get('acciones', []):
            actions.append({'id':action['id'], 'nombre':action['accion'], 'estado':action['estado'],
                            'responsable':action['responsable'], 'dependencias':action['dependencias'],
                            'piezas':[], 'evidencias':[], 'fecha':action['fecha'], 'salida':action['salida']})
        selected = {'id':item['id'], 'version':item['version'], 'estado':item['estado'],
                    'titulo': item.get('nombre') or item.get('proyecto'),
                    'diagnostico':item.get('problema') or 'Estrategia de venta documentada del workshop',
                    'audiencia':item.get('publico') or 'Audiencia declarada en las piezas del productor',
                    'oferta':('Grupo Bs 50 · VIP Bs 150' if current else item['entrega']), 'acciones':actions,
                    'piezas':[], 'propuesta_futura':not current,
                    'evidencia_declarada':item.get('evidencia') or item.get('fuentes', [])}
        selected['target'] = op.target(index_path, item['id'], selected['titulo'], item, fingerprint, targets)
        for piece in item.get('piezas', []):
            text_raw = op.read_relative(piece['documento'], [STRATEGY_ROOT]).decode('utf-8')
            op.require(piece['contenido'] in text_raw and piece['revision_editorial'] is None
                       and piece['autorizacion_comercial'] is None, 'Pieza alterada o aprobación no acreditada')
            piece_target = op.target(index_path, piece['id'], piece['titulo'], {'texto':piece['contenido'],
                                  'version':piece['version'], 'documento':piece['documento']}, fingerprint, targets)
            targets[piece_target]['editable_local'] = True
            selected['piezas'].append({'id':piece['id'], 'titulo':piece['titulo'], 'texto':piece['contenido'],
                                       'estado':piece['estado'], 'target':piece_target})
        selected['documento'] = op.document(item['documento'], [STRATEGY_ROOT], documents)
        results.append(selected)
    op.require(len({row['id'] for row in results}) == len(results), 'Estrategia duplicada')
    model['documents'].update(documents)
    model['targets'].update(targets)
    return {'estado':'disponible', 'generado':data['generado'], 'sha256':fingerprint,
            'actual':workshop['id'], 'estrategias':results, 'fuentes_requieren_conciliacion':divergences,
            'metricas_reales':workshop['metricas_reales'],
            'documento':op.document(index_path, [STRATEGY_ROOT], model['documents'])}


def current_decisions(document):
    rows = []
    for line in document.split('\n## ', 1)[0].splitlines():
        if line.startswith('|'):
            cells = [cell.strip() for cell in line.strip('|').split('|')]
            if len(cells) == 2 and cells[0] not in ('Tema', '---'):
                rows.append(cells)
    # El contrato documental conserva la tabla inicial y esta excepción posterior.
    # Mostrar ambos períodos evita atribuir a Contenido la redacción hasta el 13.
    for section in document.split('\n## ')[1:]:
        heading, _, body = section.partition('\n')
        if heading.strip() == 'Agregado 08:22: guiones y plan B':
            author = ' '.join(line.removeprefix('- ').replace('**', '') for line in body.splitlines()
                              if line.startswith(('- **Hasta el ', '- **Desde el ')))
            op.require(author, 'Reparto de autoría sin conciliar en la fuente de decisiones')
            for row in rows:
                if row[0] == 'Autor de los 5 guiones diarios':
                    row[1] = author
    return rows


def attach(model):
    model['conocimiento'] = {'fuentes': [], 'decisiones': [], 'reglas': []}
    for path in SOURCES:
        try:
            item = source(path, model)
            model['conocimiento']['fuentes'].append(item)
            if path == op.DECISIONS:
                model['conocimiento']['decisiones'] = current_decisions(item['texto'])
            if path == RULES:
                heading = '## Cierre completo del trabajo autorizado'
                excerpt = item['texto'].split(heading, 1)[-1].split('\n## ', 1)[0]
                if heading in item['texto']:
                    model['conocimiento']['reglas'].append({'texto': excerpt.split('\n', 1)[-1].strip(), 'documento': item['documento'], 'estado': 'aprobada_documentada'})
        except (OSError, ValueError, TypeError):
            model['errores'].append('Fuente documental permitida ausente o inválida. Revisar la lista de fuentes del cerebro.')
    try:
        model['estrategias'] = strategies(model)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError, ImportError):
        model['estrategias'] = {'estado': 'pendiente', 'ruta_esperada': STRATEGY_INDEX,
                                'motivo': 'Índice o estrategia ausente o inválida. El productor y la coordinadora deben aportar el contrato versionado.'}
    model['context_targets'] = {}
    source_hash = lector.sha(''.join(row['sha256'] for row in model['conocimiento']['fuentes']).encode())
    # Capturar los contratos mostrados, incluida su procedencia y disponibilidad.
    # La hora de render y los avisos de sesión no cambian la versión del contenido.
    displayed = {key: model.get(key) for key in (
        'fabricas', 'exports_panel', 'exports_estrategias', 'errores', 'tanda',
        'tanda_historica', 'diario', 'daily_stale', 'estrategias')}
    displayed = json.loads(json.dumps(displayed, ensure_ascii=False))
    if displayed['tanda'] and not model.get('diario'):
        # tanda.snapshot fecha la consulta; el contenido y sus hashes ya van incluidos.
        displayed['tanda'].pop('generado', None)
    for section, title in SECTIONS.items():
        original = {'seccion': section, 'objetivo': title,
                    'fuentes': [row['documento']['ruta'] for row in model['conocimiento']['fuentes']],
                    'decisiones': model['conocimiento']['decisiones'], 'clases': [list(row) for row in model['clases']],
                    'reglas_aprobadas': [row['texto'] for row in model['conocimiento']['reglas']],
                    'datos_mostrados': displayed,
                    'tanda': model.get('tanda_ruta'),
                    'piezas': [{'id':row['id'], 'sha256':row.get('sha256'), 'version':row.get('version')}
                               for row in (model.get('tanda') or {}).get('guiones', [])],
                    'estrategias': {key:value for key,value in model['estrategias'].items()
                                    if key in ('estado','sha256','generado','actual')}}
        key = op.target('panel/seccion/' + section, section, title, original, source_hash, model['targets'])
        model['context_targets'][section] = key
    for item in model['targets'].values():
        source_path = item['fuente']
        if isinstance(item['original'].get('texto'), str) and source_path.startswith(op.PANEL_ROOT + '/fixtures/'):
            item['editable_local'] = True
    batch = model.get('tanda')
    if batch:
        for script in batch['guiones']:
            model['targets'][script['target']]['editable_local'] = True

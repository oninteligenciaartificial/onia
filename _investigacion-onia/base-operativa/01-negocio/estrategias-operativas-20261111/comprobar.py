"""Comprobación offline del paquete; no escribe ni usa servicios o cuentas."""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent.parent
REPO = BASE.parent.parent
PREFIX = ROOT.relative_to(REPO).as_posix() + '/'
REL = ROOT.relative_to(BASE).as_posix()
CHECKS = []


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(name):
    return json.loads((ROOT / name).read_text())


def local(value, own=False):
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and '\\' not in value,
            'Ruta inválida: ' + value)
    require(str(path) == value, 'Ruta no canónica')
    resolved = (BASE / value).resolve()
    require(resolved.is_relative_to(ROOT if own else BASE), 'Escape de raíz')
    current = BASE
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), 'Symlink no admitido')
    require(resolved.is_file(), 'Falta archivo: ' + value)
    return resolved


def slug(title):
    title = re.sub(r'[*_`]', '', title).strip().lower()
    title = ''.join(c for c in title if c.isalnum() or c in ' -_')
    return title.replace(' ', '-')


def negative(name, callback):
    try:
        callback()
    except (ValueError, AssertionError):
        CHECKS.append({'control': name, 'resultado': 'rechazado_como_se_esperaba'})
    else:
        raise ValueError('Caso inválido admitido: ' + name)


def semantics(data):
    w = data['workshop']
    require(w['nombre'] == 'Claude de 0 a 100: tu negocio con IA', 'Nombre desviado')
    require((w['precio_grupo_Bs'], w['precio_vip_Bs'], w['capacidad_vip'], w['vip_minutos'])
            == (50, 150, 5, 30), 'Oferta desviada')
    expected = ['2026-11-13T20:00:00-04:00', '2026-11-14T14:00:00-04:00',
                '2026-11-16T20:00:00-04:00']
    require([c['inicio'] for c in w['clases']] == expected, 'Fechas históricas o incorrectas')
    require(all(c['termina'] is None for c in w['clases']), 'Fin inventado')
    require(w['pago']['confirmador'] == 'Sergio' and w['pago']['confirmacion'] == 'manual'
            and w['pago']['captura_concede_acceso'] is False, 'Confirmación de pago inválida')
    for row in w['escenarios']:
        g, v = row['grupo'], row['vip']
        require(type(g) is int and type(v) is int and g >= 0 and 0 <= v <= 5,
                'Unidades o capacidad inválidas')
        income = 50 * g + 150 * v
        require(row['ingreso_bruto_Bs'] == income and row['personas'] == g + v
                and row['diferencia_meta_Bs'] == income - 3000, 'Escenario incoherente')
    require(w['frontera_meta'] == [{'vip': v, 'grupo': 60 - 3*v} for v in range(6)],
            'Frontera al objetivo incorrecta')
    for key, value in w['metricas_reales'].items():
        if key not in ('corte', 'origen'):
            require(value is None, 'Se inventó un resultado real')
    for key in ('revision_tecnica', 'revision_editorial', 'autorizacion_comercial'):
        require(w[key] is None, 'Aprobación de workshop inventada')
    ids = set()
    for piece in w['piezas']:
        require(piece['id'] not in ids, 'Pieza duplicada')
        ids.add(piece['id'])
        require(piece['revision_editorial'] is None and piece['autorizacion_comercial'] is None,
                'Aprobación de pieza inventada')
    require(ids == {'P01', 'P02', 'P03', 'P04', 'P05', 'VSL01', 'A01', 'A02', 'C01', 'M01-M07'},
            'Faltan piezas del primer paquete')
    require(all(a['fecha'] >= '2026-11-12' and a['estado'] == 'propuesto' for a in w['acciones']),
            'Acción fuera de calendario o presentada como ejecutada')
    require(data['tipos_pieza_lista_abierta'] is True and not any(data['permisos'].values()),
            'Tipos cerrados o efectos externos habilitados')
    for item in data['biblioteca']:
        require(item['estado'] == 'propuesto' and item['metricas_reales'] is None
                and item['revision_editorial'] is None, 'Futuro lanzado/aprobado sin evidencia')
        for key in ('problema', 'brecha', 'entrega', 'prueba_pequena', 'avanzar_si', 'descartar_si'):
            require(bool(item[key].strip()), 'Ficha futura incompleta')
    correction = data['correcciones'][0]
    v1, v2 = correction['versiones']
    require(v1['version'] == 1 and v2['version'] == 2 and v2['padre'] == 1
            and v1['estado'] == 'historico_excluido' and v2['estado'] == 'revision_pendiente',
            'Cadena de corrección inválida')
    require(v1['texto'] != v2['texto'] and correction['evidencia_fuente'] == 'S01',
            'Corrección sin antes/después o evidencia')
    require(all(v['revision_editorial'] is None for v in (v1, v2)),
            'Corrección autoaprobada')


def run():
    data, schema, sources = read('export-estrategias-v1.json'), read('estrategias.schema.json'), read('fuentes.json')
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def validate(value):
        errors = list(validator.iter_errors(value))
        require(not errors, 'Schema: ' + '; '.join(e.message for e in errors[:3]))
        semantics(value)

    validate(data)
    CHECKS.append({'control': 'schema_y_semantica_export', 'resultado': 'correcto'})
    for source in sources['fuentes']:
        raw = local(source['ruta']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == source['sha256'] and len(raw) == source['bytes'],
                'Fuente cambió; conciliar antes de reusar: ' + source['id'])
    source_ids = {s['id'] for s in sources['fuentes']}
    require(set(data['fuentes_ids']) == source_ids and len(source_ids) == 12, 'Fuentes inconsistentes')
    decisions = local(sources['fuentes'][0]['ruta']).read_text()
    for literal in ('Claude de 0 a 100: tu negocio con IA', 'Bs 50', 'Bs 150', '5 cupos',
                    '30 minutos', 'Viernes 8pm / Sabado 2pm / Lunes 8pm', 'Sergio, a mano',
                    'cero devoluciones', 'Bs 3.000'):
        require(literal in decisions, 'Decisión comercial sin respaldo literal: ' + literal)
    CHECKS.append({'control': 'fuentes_locales_y_decisiones', 'resultado': 'correcto', 'fuentes': len(source_ids)})

    def walk(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ('documento', 'fuentes_documento'):
                    local(child, own=True)
                if key == 'fuentes' and isinstance(child, list):
                    require(set(child) <= source_ids, 'ID de fuente inexistente')
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    walk(data)
    md = (ROOT / 'PIEZAS-v1.md').read_text()
    for piece in data['workshop']['piezas']:
        require(piece['contenido'] in md, 'Texto del export distinto de Markdown: ' + piece['id'])
        require(piece['contenido'].strip(), 'Pieza vacía')
    CHECKS.append({'control': 'piezas_export_vs_markdown_y_referencias_JSON', 'resultado': 'correcto', 'piezas': 10})

    links = 0
    for path in sorted(ROOT.rglob('*.md')):
        content = path.read_text()
        for value in re.findall(r'\[[^\]\n]*\]\(([^)]+)\)', content):
            parsed = urlsplit(value)
            require(not parsed.scheme, 'Enlace externo no previsto en paquete nuevo')
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            require(target.is_relative_to(BASE) and target.is_file(), 'Enlace roto: ' + value)
            if parsed.fragment and target.suffix == '.md':
                headers = re.findall(r'^#{1,6}\s+(.+)$', target.read_text(), re.M)
                require(unquote(parsed.fragment) in {slug(h) for h in headers}, 'Ancla rota: ' + value)
            links += 1
    CHECKS.append({'control': 'enlaces_locales_y_anclas_markdown', 'resultado': 'correcto', 'enlaces': links})

    # Recorrer todas las combinaciones de 0..60 grupales y 0..5 VIP.
    cases = 0
    for vip in range(6):
        for group in range(61):
            income = 50*group + 150*vip
            require((income >= 3000) == (group >= 60 - 3*vip), 'Frontera no exacta')
            cases += 1
    CHECKS.append({'control': 'frontera_ventas_grupo_VIP', 'resultado': 'correcto', 'combinaciones': cases})

    mutations = [
        ('sexto_VIP', lambda d: d['workshop']['escenarios'][0].update(vip=6)),
        ('precio_alterado', lambda d: d['workshop'].update(precio_grupo_Bs=51)),
        ('fecha_historica', lambda d: d['workshop']['clases'][1].update(inicio='2026-11-14T20:00:00-04:00')),
        ('ingreso_mal_sumado', lambda d: d['workshop']['escenarios'][0].update(ingreso_bruto_Bs=501)),
        ('escenario_como_cobro', lambda d: d['workshop']['metricas_reales'].update(ingresos_cobrados_Bs=3000)),
        ('captura_concede_acceso', lambda d: d['workshop']['pago'].update(captura_concede_acceso=True)),
        ('correccion_autoaprobada', lambda d: d['correcciones'][0]['versiones'][1].update(revision_editorial='aprobado')),
        ('futuro_iniciado', lambda d: d['biblioteca'][2].update(estado='en_desarrollo')),
        ('raiz_escape', lambda d: d['workshop'].update(documento='../privado/contexto.md')),
    ]
    for name, mutation in mutations:
        changed = deepcopy(data)
        mutation(changed)
        negative(name, lambda value=changed: validate(value))
    flexible = deepcopy(data)
    flexible['workshop']['piezas'][0]['tipo'] = 'formato_nuevo_pertinente'
    validate(flexible)
    CHECKS.append({'control': 'tipos_de_pieza_ampliables', 'resultado': 'correcto'})

    panel_path = BASE / '05-herramientas/fabrica-contenido/20261109-lector-panel'
    sys.path.insert(0, str(panel_path))
    panel = importlib.import_module('operacion')
    export_path = REL + '/estado-fabrica.json'
    require(panel.PRODUCERS.get('estrategias') == REL, 'Falta consumidor real de estrategias')
    docs, targets = {}, {}
    loaded = panel.load_export(export_path, docs, targets)
    require(loaded['fabrica'] == 'estrategias' and all(d['documento']['disponible'] for d in loaded['entregables']),
            'Export incompleto en consumidor real')
    require(len(targets) == len(loaded['pasos']) + len(loaded['entregables']), 'Targets incompletos')
    for row in read('estado-fabrica.json')['pasos']:
        for evidence in row['evidencias']:
            local(evidence, own=True)
    CHECKS.append({'control': 'panel_consumidor_real', 'resultado': 'correcto',
                   'documentos': len(docs), 'targets': len(targets), 'integracion_real': True})
    negative('panel_rechaza_documento_fuera_raiz', lambda: panel.relative_path(
        '04-operacion-agentes/reglas-comunes.md', [REL]))

    # Control del alcance real del checkout; no consulta otro almacén Git.
    status = subprocess.run(['git', 'status', '--porcelain', '-z', '--untracked-files=all'],
                            cwd=REPO, check=True, capture_output=True).stdout.decode()
    paths = [entry[3:] for entry in status.split('\0') if entry]
    require(all(p.startswith(PREFIX) for p in paths), 'Hay cambios fuera de rutas asignadas')
    CHECKS.append({'control': 'alcance_git', 'resultado': 'correcto', 'archivos_en_cambio': len(paths)})
    # Revisión auxiliar: contenido compartible, sin direcciones de red ni claves.
    for path in ROOT.rglob('*'):
        if path.is_file() and path.suffix in ('.json', '.md', '.py'):
            content = path.read_text()
            require(not re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content), 'Dirección de red literal: ' + path.name)
            require(not re.search(r'sk-[A-Za-z0-9]{24,}', content), 'Posible secreto: ' + path.name)
            require(not re.search(r'https://meet\.google\.com/[a-z]{3}-', content), 'Meet privado: ' + path.name)
    CHECKS.append({'control': 'revision_auxiliar_datos_compartibles', 'resultado': 'correcto'})
    return {'resultado': 'correcto', 'ejecutado': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'commit_fuentes': data['commit_base'], 'controles': CHECKS,
            'limites': ['Sin revisión independiente/editorial ni ensayo de voz',
                        'Sin cuentas/CTA/pago/acceso real probados ni autorización comercial',
                        'Consumidor local real probado; servicio y teléfono no acreditados por este comprobador',
                        'Revisión auxiliar de secretos no sustituye inspección humana']}


if __name__ == '__main__':
    try:
        print(json.dumps(run(), ensure_ascii=False, indent=2))
    except Exception as error:
        print(json.dumps({'resultado': 'fallo', 'error': str(error), 'controles_previos': CHECKS}, ensure_ascii=False, indent=2))
        sys.exit(1)

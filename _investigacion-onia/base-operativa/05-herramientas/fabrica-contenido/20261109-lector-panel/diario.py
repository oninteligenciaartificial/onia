"""Proyección opcional del ciclo privado. No consulta ni modifica el harness."""
import hashlib
import json
import re
from datetime import date, datetime
from pathlib import Path

import lector
import operacion


def read(path):
    path = Path(path).absolute()
    operacion.require(path.name == 'panel.json' and not path.resolve().is_relative_to(lector.REPO.resolve()), 'Proyección debe ser privada')
    for p in (path, *path.parents):
        operacion.require(not p.is_symlink() and not ((p / '.git').is_file() or (p / '.git/HEAD').is_file()), 'Proyección enlazada o en Git')
    operacion.require(path.is_file() and path.stat().st_size <= 2*1024*1024, 'Proyección ausente o excesiva')
    data = json.loads(path.read_bytes())
    operacion.require(data.get('schema') == 'onia-flujo-panel-v1', 'Contrato diario inválido')
    operacion.require(len(data['candidatas']) <= 20 and len(data['ciclos']) <= 14 and len(data['errores']) <= 80, 'Proyección excesiva')
    for cycle in data['ciclos']:
        result = cycle.get('resultado')
        if result:
            rows = result['piezas']
            operacion.require([r['id'] for r in rows] == ['T01','T02','T03','T04','T05'], 'Cinco piezas requeridas')
            for row in rows:
                operacion.require(hashlib.sha256(row['texto'].encode()).hexdigest() == row['sha256'], 'Texto diario alterado')
    validate(data)
    return data



def validate(data):
    # Cotejar TODOS los campos usados por fragment/attach antes de adoptar la caché.
    for field in ('candidatas', 'ciclos', 'errores'):
        operacion.require(isinstance(data[field], list), 'Lista diaria inválida')
    schedule = data.get('programacion') or {}
    operacion.require(isinstance(schedule, dict), 'Programación inválida')
    for item in data['candidatas']:
        for field in ('titulo', 'url', 'publicada', 'consultada'):
            operacion.text(item[field], 2000)
    for item in data['errores']:
        for field in ('codigo', 'siguiente'):
            operacion.text(item[field], 2000)
    for cycle in data['ciclos']:
        for field in ('id', 'dia', 'fase'):
            operacion.text(cycle[field], 200)
        date.fromisoformat(cycle['dia'])
        operacion.require(isinstance(cycle.get('harness') or {}, dict), 'Harness inválido')
        operacion.require(isinstance(cycle.get('revision_tecnica') or {}, dict), 'Dictamen inválido')
        result = cycle.get('resultado')
        if result is None:
            continue
        for field in ('huella', 'version', 'generado'):
            operacion.text(result[field], 200)
        operacion.require(re.fullmatch(r'[a-f0-9]{64}', result['huella']), 'Huella inválida')
        operacion.require(datetime.fromisoformat(result['generado']).tzinfo is not None, 'Fecha sin zona')
        operacion.require(type(result.get('sintetico')) is bool, 'Procedencia inválida')
        for row in result['piezas']:
            for field in ('id', 'titulo', 'texto', 'sha256', 'version_editorial'):
                operacion.text(row[field], 200000)


def attach(model, data):
    model['diario'] = data
    cycles = [c for c in data['ciclos'] if c.get('resultado')]
    if not cycles:
        return
    cycle = cycles[-1]
    result = cycle['resultado']
    review = cycle.get('revision_tecnica') or {}
    reviewed = bool(result.get('commit') and review.get('verdict') == 'bueno'
                    and review.get('commit') == result['commit']
                    == (cycle.get('harness') or {}).get('commit'))
    scripts = []
    source = 'flujo/' + cycle['id'] + '/' + result['huella']
    for row in result['piezas']:
        script = {**row, 'origen': 'Resultado privado del ciclo ' + cycle['dia'],
                  'integridad': 'verificada' if reviewed else 'pendiente_revision', 'revision_editorial': 'pendiente',
                  'revision_tecnica': cycle.get('revision_tecnica'), 'version': result['version']}
        script['target'] = operacion.target(source, row['id'], row['titulo'], script.copy(), row['sha256'], model['targets'])
        scripts.append(script)
    model['tanda'] = {'schema': 'onia-lector-panel-v1', 'fecha_tanda': cycle['dia'],
                      'generado': result['generado'], 'guiones': scripts,
                      'alcance': 'Proyección privada; aprobación editorial pendiente', 'commit_entradas_repo': result.get('commit')}
    model['tanda_ruta'], model['tanda_historica'] = source, False


def fragment(data, stale=False):
    from panel import e
    schedule = data.get('programacion') or {}
    if schedule.get('habilitada'):
        label = 'Programación habilitada · ' + e(schedule.get('hora_tanda') or 'hora pendiente') + ' · America/La_Paz.'
    else:
        label = 'Programación deshabilitada · hora de tanda pendiente.'
    out = ['<p>' + label + '</p>']
    if stale:
        out.append('<p role="alert">Actualización fallida. Se conserva la última proyección válida; revisar archivo del productor.</p>')
    out.append('<p>Última consulta: ' + e(data.get('fuente_ultimo_intento') or 'sin consulta') +
               '<br>Último éxito de fuente: ' + e(data.get('fuente_ultimo_exito') or 'sin éxito') + '</p>')
    for error in data.get('errores', []):
        out.append('<p role="alert">' + e(error['codigo']) + ' · ' + e(error['siguiente']) + '</p>')
    out.append('<details><summary>Ver novedades y progreso</summary>')
    out.append('<details><summary>Novedades / candidatas (' + str(len(data.get('candidatas', []))) + ')</summary>')
    for row in data.get('candidatas', []):
        # Sólo texto, sin convertir una URL externa en navegación ejecutable.
        out.append('<article><strong>' + e(row['titulo']) + '</strong><p>Publicada ' + e(row['publicada']) +
                   ' · consultada ' + e(row['consultada']) + '</p><p>' + e(row['url']) + '</p></article>')
    out.append('</details>')
    for cycle in reversed(data.get('ciclos', [])):
        harness = cycle.get('harness') or {}
        out.append('<article><h3>' + e(cycle['dia']) + ' · ' + e(cycle['fase']) + '</h3><p>Tarea ' + e(cycle['id']) +
                   ' · harness ' + e(harness.get('state') or 'sin registrar') + ' · revisión ' + e(harness.get('revision') or 'pendiente') + '</p>')
        review = cycle.get('revision_tecnica') or {}
        out.append('<p>Revisión técnica: ' + e(review.get('verdict') or 'pendiente') + ' · revisión editorial pendiente.</p>')
        result = cycle.get('resultado')
        if result:
            label = 'ENSAYO SINTÉTICO · ' if result.get('sintetico') else ''
            out.append('<p>' + label + 'Resultado ' + e(result['version']) + ' · generado ' + e(result['generado']) + '</p>')
            for row in result['piezas']:
                out.append('<details><summary>' + e(row['id']) + ' · ' + e(row['titulo']) + '</summary><pre>' + e(row['texto']) + '</pre></details>')
            out.append('<a href="/?guardado=0#guiones">Abrir esta versión para revisar (recarga)</a>')
        out.append('</article>')
    out.append('</details>')
    return ''.join(out)


def script():
    return (Path(__file__).parent / 'diario.js').read_text()


def script_hash():
    import base64
    return base64.b64encode(hashlib.sha256(script().encode()).digest()).decode()

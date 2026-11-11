"""Proyección opcional del ciclo privado. No consulta ni modifica el harness."""
import hashlib
import json
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
    return data


def attach(model, data):
    model['diario'] = data
    cycles = [c for c in data['ciclos'] if c.get('resultado')]
    if not cycles:
        return
    cycle = cycles[-1]
    result = cycle['resultado']
    scripts = []
    source = 'flujo/' + cycle['id'] + '/' + result['huella']
    for row in result['piezas']:
        script = {**row, 'origen': 'Resultado privado del ciclo ' + cycle['dia'],
                  'integridad': 'pendiente_revision', 'revision_editorial': 'pendiente',
                  'revision_tecnica': cycle.get('revision_tecnica'), 'version': result['version']}
        script['target'] = operacion.target(source, row['id'], row['titulo'], script.copy(), row['sha256'], model['targets'])
        scripts.append(script)
    model['tanda'] = {'schema': 'onia-lector-panel-v1', 'fecha_tanda': cycle['dia'],
                      'generado': result['generado'], 'guiones': scripts,
                      'alcance': 'Proyección privada; aprobación editorial pendiente', 'commit_entradas_repo': (cycle.get('harness') or {}).get('commit')}
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

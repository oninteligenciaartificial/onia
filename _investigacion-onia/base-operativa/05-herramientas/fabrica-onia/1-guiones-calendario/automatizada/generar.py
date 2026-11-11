#!/usr/bin/env python3
"""Valida redacción aportada por un LLM/operador y crea una tanda nueva, sin red."""
import argparse
import copy
from datetime import date, datetime
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unicodedata
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[3]
OUTPUT_ROOT = HERE.parent / 'salida/guiones-tanda-20261111-v3'
BRAIN = BASE / '03-referentes/cerebro-operativo/20261109'
V2 = HERE.parent / 'salida/guiones-tanda-20261111-v2'
IDS = ['T01', 'T02', 'T03', 'T04', 'T05']
OFFER = {
    'nombre': 'Claude de 0 a 100: tu negocio con IA', 'grupo_bs': 50,
    'vip_bs': 150, 'vip_cupos': 5, 'vip_minutos': 30,
    'zona': 'America/La_Paz', 'plataforma': 'Google Meet',
    'clases': ['2026-11-13T20:00:00-04:00', '2026-11-14T14:00:00-04:00',
               '2026-11-16T20:00:00-04:00'],
    'pago': 'QR y seguimiento; Sergio confirma cada pago manualmente',
}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(data):
    return (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode()


def fingerprint(data):
    return digest(json.dumps(data, ensure_ascii=False, sort_keys=True).encode())


def load(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f'Clave JSON duplicada: {key}')
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def text_field(obj, field):
    value = obj.get(field)
    require(isinstance(value, str) and bool(value.strip()), f'Falta texto: {field}')
    return value


def stamp(value):
    result = datetime.fromisoformat(value)
    require(result.tzinfo is not None, 'Fecha sin zona')
    return result


def normalized(text):
    value = unicodedata.normalize('NFKD', text.casefold())
    return ' '.join(re.findall(r'\w+', ''.join(c for c in value if not unicodedata.combining(c))))


def brain_module():
    spec = importlib.util.spec_from_file_location('cerebro_editorial', BRAIN / 'consultar.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_corrections(draft, corrections):
    result = copy.deepcopy(draft)
    if corrections is None:
        return result, []
    require(corrections.get('schema') == 'onia-correcciones-v1', 'Correcciones incompatibles')
    require(corrections.get('entrada_sha256') == fingerprint(draft), 'Corrección de otra entrada')
    require(corrections.get('version_base') == draft.get('version'), 'Versión base diferente')
    require(corrections.get('version_nueva') != draft.get('version'), 'Se requiere nueva versión')
    result['version'] = text_field(corrections, 'version_nueva')
    rules = corrections.get('reglas')
    require(isinstance(rules, list) and rules, 'Correcciones vacías')
    changes = []
    for rule in rules:
        rule_id = text_field(rule, 'id')
        reason = text_field(rule, 'motivo')
        targets = rule.get('piezas')
        fields = rule.get('campos')
        require(isinstance(targets, list) and targets and len(set(targets)) == len(targets)
                and set(targets) <= set(IDS), 'Piezas de corrección inválidas')
        require(isinstance(fields, list) and fields and len(set(fields)) == len(fields)
                and set(fields) <= {'guion_hablado', 'copy', 'cta', 'planos', 'pendientes'},
                'Campos de corrección inválidos')
        before, after = text_field(rule, 'antes'), text_field(rule, 'despues')
        require(before != after, 'Corrección sin cambio')
        for target in targets:
            row = next(p for p in result['guiones'] if p['id'] == target)
            for field in fields:
                require(row[field].count(before) == 1, f'Precondición fallida: {target}/{field}')
                old = row[field]
                row[field] = old.replace(before, after)
                changes.append({'regla': rule_id, 'pieza': target, 'campo': field,
                                'motivo': reason, 'antes_sha256': digest(old.encode()),
                                'despues_sha256': digest(row[field].encode())})
    return result, changes


def validate(brief, sources, draft):
    require(brief.get('schema') == 'onia-brief-guiones-v1', 'Brief incompatible')
    day = date.fromisoformat(brief['fecha_tanda'])
    require(brief.get('oferta') == OFFER, 'Oferta/horarios no coinciden con decisiones vigentes')
    generated = stamp(brief['generado'])
    require(generated.date() == day, 'Fecha de generación diferente de tanda')
    require(brief.get('revision_editorial') == 'pendiente', 'No se admite aprobación editorial')
    require(brief.get('canal', {}).get('estado') == 'no_probado', 'Canal real fuera del ensayo')
    for key in ('nombre', 'responsable', 'prueba_requerida'):
        text_field(brief['canal'], key)
    text_field(brief, 'entrada_relato_real')
    require(sources.get('schema') == 'onia-fuentes-guiones-v1', 'Fuentes incompatibles')
    items = sources.get('items')
    require(isinstance(items, list) and items, 'Faltan fuentes')
    source_map = {}
    for item in items:
        sid = text_field(item, 'id')
        require(sid not in source_map, 'Fuente duplicada')
        source_map[sid] = item
        text_field(item, 'titulo')
        text_field(item, 'localizador')
        text_field(item, 'limites')
        consulted = stamp(item['consultada'])
        require(consulted <= generated, 'Consulta posterior a generación')
        if item['tipo'] == 'local':
            path = Path(item['ruta'])
            require(not path.is_absolute() and '..' not in path.parts, 'Fuente local fuera de base')
            require(path.parts[0] in {'03-referentes', '05-herramientas'}, 'Fuente local no permitida')
            dest = (BASE / path).resolve(strict=True)
            require(dest.is_relative_to(BASE) and not (BASE / path).is_symlink(), 'Fuente con enlace externo')
            require(digest(dest.read_bytes()) == item['sha256'], f'Fuente alterada: {sid}')
        else:
            require(item['tipo'] == 'web_primaria' and item.get('primaria') is True,
                    'Noticia sin fuente primaria')
            url = urlsplit(item['url'])
            require(url.scheme == 'https' and url.hostname in {'www.anthropic.com', 'anthropic.com', 'claude.com'}
                    and not url.query and not url.fragment and not url.username, 'URL primaria no admitida')
            published = date.fromisoformat(item['publicada'])
            event = date.fromisoformat(item['fecha_hecho'])
            require(event <= published <= consulted.date(), 'Fechas de noticia inconsistentes')
            require(isinstance(item.get('hechos'), list) and item['hechos'], 'Faltan hechos respaldados')
    require(draft.get('schema') == 'onia-redaccion-guiones-v1', 'Redacción incompatible')
    text_field(draft, 'version')
    require(draft.get('autor', {}).get('modo') == 'LLM_en_sesion', 'Declarar autoría LLM')
    rows = draft.get('guiones')
    require(isinstance(rows, list) and [r['id'] for r in rows] == IDS, 'Se requieren cinco piezas T01–T05 en orden')
    require(rows[0]['slot'] == 'venta' and rows[1]['slot'] == 'marca'
            and rows[2]['slot'] in {'noticia_ia', 'evergreen'}
            and rows[3]['slot'] in {'venta', 'marca'} and rows[4]['slot'] == 'prueba', 'Mezcla editorial inválida')
    seen = {field: set() for field in ('idea', 'guion_hablado')}
    module = brain_module()
    catalog = module.cargar(BRAIN / 'catalogo.json')  # valida las 28 fuentes heredadas
    brain_ids = {p['id'] for p in catalog['patrones']}
    for row in rows:
        for field in ('titulo', 'idea', 'proposito', 'apertura', 'guion_hablado', 'planos',
                      'copy', 'cta', 'pendientes', 'criterio', 'seleccion_motivo', 'tipo_evidencia'):
            text_field(row, field)
        for field in seen:
            value = normalized(row[field])
            require(value not in seen[field], f'Pieza duplicada por {field}')
            seen[field].add(value)
        require(row['guion_hablado'].startswith(row['apertura']), 'Apertura no entregada en voz')
        for field in ('guion_hablado', 'copy'):
            require(row[field].count(row['cta']) == 1, f'CTA incoherente: {row["id"]}/{field}')
        require(35 <= len(row['guion_hablado'].split()) <= 220, 'Locución fuera de rango revisable')
        require(isinstance(row.get('fuentes'), list) and row['fuentes']
                and set(row['fuentes']) <= source_map.keys(), 'Referencia de fuente incompleta')
        require(isinstance(row.get('patrones'), list) and row['patrones']
                and set(row['patrones']) <= brain_ids, 'Patrón del cerebro desconocido')
        require(set(row.get('variantes', {})) == {'vertical', 'horizontal'}, 'Faltan adaptaciones por pieza')
        for name, ratio in [('vertical', '9:16'), ('horizontal', '16:9')]:
            variant = row['variantes'][name]
            require(variant.get('relacion') == ratio, 'Relación de aspecto inválida')
            for field in ('encuadre', 'texto_pantalla', 'montaje'):
                text_field(variant, field)
        if row['slot'] == 'noticia_ia':
            evidence = [source_map[s] for s in row['fuentes'] if source_map[s]['tipo'] == 'web_primaria']
            require(evidence and all(0 <= (day-date.fromisoformat(s['fecha_hecho'])).days <= 7 for s in evidence),
                    'Noticia sin primaria fechada reciente; usar evergreen explícito')
            require(all(s['publicada'] in row['copy'] for s in evidence), 'Falta fecha de noticia en copy')
            require(row['tipo_evidencia'] == 'anuncio_primario_no_demo', 'Anuncio no equivale a demo')
        if row['slot'] == 'evergreen':
            text_field(row, 'motivo_evergreen')
    return catalog


def target_path(output):
    output = Path(output).absolute()
    require(output.resolve().is_relative_to(OUTPUT_ROOT.resolve()), 'Salida fuera de v3 asignada')
    for part in [output, *output.parents]:
        require(not part.is_symlink(), 'Salida con enlace simbólico')
        if part == BASE:
            break
    require(not output.exists(), 'Salida duplicada; no se pisa ninguna versión')
    return output


def markdown(row, version, brief):
    duration = row['duracion_orientativa']
    lines = [f'# {row["id"]} · {row["titulo"]}', '',
             f'Versión editorial: {version}. Slot: {row["slot"]}.',
             'Borrador; revisión técnica distinta y editorial pendientes. Sin aprobación de publicación.', '',
             f'Propósito: {row["proposito"]}', '', '## Idea y selección', '', row['idea'], '',
             row['seleccion_motivo'], '', f'Patrones: {", ".join(row["patrones"])}. Fuentes: {", ".join(row["fuentes"])}; ver FUENTES.md y seleccion.json.', '',
             '## Guion hablado', '', row['guion_hablado'], '', '## Planos y apoyos', '', row['planos'], '',
             'No usar el logo de Claude/Anthropic como propio. No fabricar capturas de Claude.', '',
             f'Duración estimada: {duration}; cálculo por palabras, pendiente de ensayo humano.', '',
             f'Evidencia: {row["tipo_evidencia"]}.', '', '## Dos adaptaciones de la misma pieza', '']
    for key, variant in row['variantes'].items():
        lines += [f'### {key.title()} · {variant["relacion"]}', '',
                  variant['encuadre'], '', f'Pantalla: {variant["texto_pantalla"]}', '', variant['montaje'], '']
    lines += ['## Copy', '', row['copy'], '', '## CTA único', '', row['cta'], '',
              f'Canal: {brief["canal"]["nombre"]} — NO PROBADO. Responsable: {brief["canal"]["responsable"]}.',
              f'Antes de publicar: {brief["canal"]["prueba_requerida"]}', '',
              '## Revisión y faltantes', '', row['criterio'], '', row['pendientes'], '',
              'Los personajes y el crítico del proceso son hipótesis editoriales, sin entrevistas ni datos de audiencia real.']
    if row['slot'] == 'evergreen':
        lines += ['', 'Evergreen explícito: ' + row['motivo_evergreen']]
    return '\n'.join(lines) + '\n'


def build(brief, sources, draft, corrections, output):
    output = target_path(output)
    corrected, changes = apply_corrections(draft, corrections)
    catalog = validate(brief, sources, corrected)
    # El original también debe ser completo: una corrección no repara entradas incompletas.
    validate(brief, sources, draft)
    files = {}
    rows = []
    for item in corrected['guiones']:
        row = copy.deepcopy(item)
        words = len(row['guion_hablado'].split())
        row['duracion_orientativa'] = f'{math.floor(words/150*60)}–{math.ceil(words/115*60)} s'
        row.update({'origen': (output / (row['id']+'.md')).relative_to(BASE).as_posix(),
                    'integridad': 'pendiente_revision', 'revision_tecnica': None,
                    'revision_editorial': 'pendiente', 'publicacion': 'Sin aprobación; borrador',
                    'error': 'Integridad de bytes no equivale a aprobación editorial.',
                    'version_editorial': corrected['version']})
        row['texto'] = markdown(row, corrected['version'], brief)
        raw = row['texto'].encode()
        row.update({'sha256': digest(raw), 'bytes': len(raw)})
        files[row['id']+'.md'] = raw
        rows.append(row)
    files['guiones-panel.json'] = encoded({'tipo': 'datos-guiones-no-snapshot-canonico',
        'fecha_tanda': brief['fecha_tanda'], 'version_editorial': corrected['version'], 'guiones': rows})
    files['fuentes.json'] = encoded(sources)
    files['brief-editorial.json'] = encoded(brief)
    files['redaccion-aplicada.json'] = encoded(corrected)
    files['correcciones-aplicadas.json'] = encoded({'entrada_sha256': fingerprint(draft),
        'salida_sha256': fingerprint(corrected), 'version_base': draft['version'],
        'version_nueva': corrected['version'], 'cambios': changes,
        'naturaleza': 'Corrección local declarada por productor; no revisión independiente ni aprobación'})
    selections = []
    module = brain_module()
    all_patterns = module.consultar(catalog, [], [])['resultados']
    for row in rows:
        selections.append({'pieza': row['id'], 'motivo': row['seleccion_motivo'],
            'patrones': [p for p in all_patterns if p['id'] in row['patrones']]})
    files['seleccion.json'] = encoded({'naturaleza': 'Criterio editorial propuesto; hipótesis, no audiencia investigada',
        'candidatas': brief['candidatas'], 'seleccion': selections})
    source_lines = ['# Fuentes y trazabilidad', '', 'Lectura documental; no nuevo ASR ni capturas. Hashes de fuentes locales en fuentes.json.', '']
    for item in sources['items']:
        href = item.get('url') or os.path.relpath(BASE / item['ruta'], output)
        source_lines += [f'- **{item["id"]}** · [{item["titulo"]}]({href}). Consulta: {item["consultada"]}. Localizador: {item["localizador"]}. Límite: {item["limites"]}.']
        if item['tipo'] == 'web_primaria':
            source_lines += [f'  Publicada: {item["publicada"]}; hecho: {item["fecha_hecho"]}. Hechos utilizados: ' + '; '.join(item['hechos']) + '.']
    files['FUENTES.md'] = ('\n'.join(source_lines) + '\n').encode()
    calendar = {'naturaleza': 'Propuesta editorial local; sin Calendar ni scheduler',
        'zona': OFFER['zona'], 'clases': OFFER['clases'], 'hora_fin': None,
        'piezas': [{'id': r['id'], 'fecha_editorial': brief['fecha_tanda'], 'orden': i,
                    'hora_publicacion': None, 'estado': 'pendiente_revision',
                    'formatos': ['vertical', 'horizontal']} for i, r in enumerate(rows, 1)]}
    files['calendario.json'] = encoded(calendar)
    files['CALENDARIO.md'] = ('# Calendario propuesto\n\n' + brief['fecha_tanda'] + ': revisar T01–T05 en ese orden; horarios de publicación sin fijar.\n'
        'Cinco ideas, dos adaptaciones por pieza. No se tocó Calendar.\n\n'
        '| Clase | Inicio America/La_Paz | Fin |\n|---|---|---|\n'
        '| Ordenar | viernes 13-nov-2026 20:00 | Sin confirmar |\n'
        '| Vender | sábado 14-nov-2026 14:00 | Sin confirmar |\n'
        '| Automatizar | lunes 16-nov-2026 20:00 | Sin confirmar |\n\n'
        'Publicación sujeta a revisión y sí de Sergio. El lunes 16 requiere operador/materiales; no se presume modelo después del 14.\n').encode()
    files['README.md'] = ('# Tanda v3 · ' + brief['fecha_tanda'] + '\n\nCinco borradores, versión editorial ' + corrected['version'] +
        '. Revisión técnica distinta/editorial y ensayo humano pendientes.\n\n' +
        '\n'.join(f'- [{r["id"]}]({r["id"]}.md): {r["titulo"]} · {r["slot"]} · {r["duracion_orientativa"]} estimados.' for r in rows) +
        '\n\nVoz y selección propuestas por el LLM de esta sesión. Programa fijo: validación, correcciones literales, cálculo orientativo, calendarios y export. '
        'No investiga, no escribe creatividad ni despacha automáticamente.\n\n'
        'Ver FUENTES.md, seleccion.json, correcciones-aplicadas.json y calendario.json. '
        'Canal NEGOCIO no probado; pagos manuales por Sergio. Sin publicación ni venta acreditada.\n\n'
        'Entrada concreta para un relato real futuro: ' + brief['entrada_relato_real'] + '\n').encode()
    rel = lambda name: (output / name).relative_to(BASE).as_posix()
    files['estado-fabrica.json'] = encoded({'schema': 'onia-fabrica-estado-v1',
        'id': 'guiones-tanda-automatizada-20261111', 'fabrica': 'guiones', 'estado': 'para_revision',
        'generado': brief['generado'], 'fuente': rel('recibo.json'),
        'pasos': [{'id': 'seleccion', 'nombre': 'Seleccionar ideas con cerebro', 'estado': 'completado', 'evidencias': [rel('seleccion.json')]},
                  {'id': 'correccion', 'nombre': 'Aplicar corrección versionada', 'estado': 'completado' if changes else 'pendiente', 'evidencias': [rel('correcciones-aplicadas.json')]},
                  {'id': 'revision', 'nombre': 'Revisión editorial y ensayo humano', 'estado': 'pendiente', 'evidencias': []}],
        'entregables': [{'nombre': 'Tanda', 'ruta': rel('guiones-panel.json')}, {'nombre': 'Calendario propuesto', 'ruta': rel('calendario.json')}],
        'pendientes': [{'motivo': 'Ensayo hablado y autorización editorial', 'responsable': 'Contenido/Sergio', 'siguiente': 'Leer las cinco piezas y ensayar ambas adaptaciones'},
            {'motivo': 'Canal NEGOCIO no probado', 'responsable': 'Operaciones/Sergio', 'siguiente': brief['canal']['prueba_requerida']},
            {'motivo': 'Relato real no aportado', 'responsable': 'Sergio', 'siguiente': brief['entrada_relato_real']}]})
    reference = {p.name: digest(p.read_bytes()) for p in sorted(V2.iterdir()) if p.is_file()}
    files['recibo.json'] = encoded({'schema': 'onia-recibo-tanda-v1', 'generado': brief['generado'],
        'ensayo_local': True, 'revision_independiente': None, 'aprobacion_editorial': None,
        'entradas': {'brief': fingerprint(brief), 'fuentes': fingerprint(sources), 'redaccion': fingerprint(draft),
                     'correcciones': fingerprint(corrections)},
        'v2_solo_lectura': reference, 'archivos': {name: {'sha256': digest(raw), 'bytes': len(raw)} for name, raw in files.items()},
        'limite': 'Recibo no se hashea a sí mismo. Hashes verifican bytes; no verdad ni aceptación.'})
    # Toda validación y render se completa antes de crear el destino. No reemplaza una salida previa.
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.tanda-', dir=HERE))
    try:
        for name, raw in files.items():
            (staging / name).write_bytes(raw)
        output.mkdir(exist_ok=False)  # reserva exclusiva, incluso ante dos invocaciones simultáneas
        try:
            for file in staging.iterdir():
                file.rename(output / file.name)
        except OSError:
            # Un corte de E/S deja salida incompleta visible, que se rechaza al repetir.
            raise
    finally:
        shutil.rmtree(staging)
    return {'salida': output.relative_to(BASE).as_posix(), 'version': corrected['version'],
            'piezas': len(rows), 'cambios': len(changes), 'estado': 'para_revision'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for field in ('brief', 'fuentes', 'redaccion', 'salida'):
        parser.add_argument('--' + field, required=True, type=Path)
    parser.add_argument('--correcciones', type=Path)
    args = parser.parse_args(argv)
    try:
        result = build(load(args.brief), load(args.fuentes), load(args.redaccion),
                       load(args.correcciones) if args.correcciones else None, args.salida)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError, StopIteration) as error:
        print(json.dumps({'error': 'Tanda rechazada', 'detalle': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

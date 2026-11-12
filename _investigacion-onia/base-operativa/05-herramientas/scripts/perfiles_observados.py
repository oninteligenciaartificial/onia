#!/usr/bin/env python3
"""Recibo saneado de perfiles; stdlib, sin búsqueda de logs predeterminada.

Uso: python3 perfiles_observados.py DIRECTORIO SID_PADRE [SID_PADRE ...]
Recorre *.jsonl bajo el directorio explícito, sin seguir enlaces simbólicos.
SID y turn_id deben ser UUID. Incluye padres y descendientes por parent_thread_id.
Cada fila resume un perfil, sin publicar turnos, agent_path ni texto libre.
Alcance: uso_confirmado (token_usage_record propio), contexto_no_confirmado o
no_observado. Un contexto sin thread_id sólo se confirma mediante turno + SID
propios. No se deduce uso del orden de eventos, tokens totales ni del nombre del
archivo. agent_path permite descartar contextos de otro agente cuando aparece.
Los errores son deliberadamente fijos: nunca incluyen rutas ni líneas de entrada.
"""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from uuid import UUID


class ArgumentosSeguros(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, 'Argumentos inválidos. Use --help.\n')


class ErrorLectura(ValueError):
    """Entrada ilegible o ambigua; no conserva detalles privados."""


def identificador(value):
    if not isinstance(value, str):
        return None
    try:
        return str(UUID(value))
    except ValueError:
        return None


def objeto(value):
    return value if isinstance(value, dict) else {}


def modelo(value):
    # Sólo nombres de modelos, nunca URLs, rutas o texto arbitrario.
    if isinstance(value, str) and re.fullmatch(r'(?:gpt|o[134]|codex)[a-zA-Z0-9._-]{0,75}', value):
        return value
    return None


def esfuerzo(value):
    return value if isinstance(value, str) and value in {
        'none', 'minimal', 'low', 'medium', 'high', 'xhigh', 'ultra'
    } else None


def leer(path):
    meta = None
    contexts = []
    usage = set()
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            if not line.strip():
                continue
            try:
                record = objeto(json.loads(line))
            except (ValueError, RecursionError):
                raise ErrorLectura('JSONL inválido') from None
            kind = record.get('type')
            payload = objeto(record.get('payload'))
            if kind == 'event_msg':
                kind = payload.get('type')
            if kind == 'session_meta':
                spawn = objeto(objeto(objeto(payload.get('source')).get('subagent')).get('thread_spawn'))
                raw_parent = payload.get('parent_thread_id', spawn.get('parent_thread_id'))
                parent = identificador(raw_parent)
                if raw_parent is not None and parent is None:
                    raise ErrorLectura('Metadatos inválidos')
                current = (identificador(payload.get('id') or payload.get('thread_id')),
                           parent, payload.get('agent_path', spawn.get('agent_path')))
                if not current[0] or (meta is not None and meta != current):
                    raise ErrorLectura('Metadatos ambiguos')
                meta = current
            elif kind == 'turn_context':
                contexts.append(payload)
            elif kind == 'token_usage_record':
                sid = identificador(payload.get('thread_id'))
                turn = identificador(payload.get('turn_id'))
                if sid and turn:
                    usage.add((sid, turn))
    if meta is None:
        return None
    sid, parent, agent_path = meta
    profiles = set()
    for context in contexts:
        context_sid = context.get('thread_id')
        if context_sid is not None and identificador(context_sid) != sid:
            continue
        if (context.get('agent_path') is not None and agent_path is not None
                and context['agent_path'] != agent_path):
            continue
        turn = identificador(context.get('turn_id'))
        confirmed = (sid, turn) in usage
        # Sin pertenencia explícita, el contexto puede proceder del padre.
        if context_sid is None and not confirmed and parent is not None:
            continue
        profiles.add((modelo(context.get('model')),
                      esfuerzo(context.get('effort', context.get('reasoning_effort'))),
                      'uso_confirmado' if confirmed else 'contexto_no_confirmado'))
    return sid, parent, profiles


def observar(directory, parents):
    """Devuelve sólo campos permitidos; no modifica el directorio indicado."""
    roots = {identificador(sid) for sid in parents}
    if not roots or None in roots:
        raise ErrorLectura('SID inválido')
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise ErrorLectura('Directorio inválido')
    sessions = {}
    try:
        def walk_error(_error):
            raise ErrorLectura('Directorio ilegible')
        for base, dirs, files in os.walk(directory, followlinks=False, onerror=walk_error):
            dirs[:] = sorted(d for d in dirs if not (Path(base) / d).is_symlink())
            for name in sorted(files):
                path = Path(base) / name
                if path.suffix != '.jsonl' or path.is_symlink() or not path.is_file():
                    continue
                result = leer(path)
                if result is None:
                    continue
                sid, parent, profiles = result
                if sid in sessions:
                    old_parent, old_profiles = sessions[sid]
                    if old_parent != parent:
                        raise ErrorLectura('Metadatos ambiguos')
                    profiles |= old_profiles
                sessions[sid] = parent, profiles
    except (OSError, UnicodeError):
        raise ErrorLectura('Entrada ilegible') from None
    selected = set(roots)
    while True:
        expanded = selected | {sid for sid, (parent, _) in sessions.items() if parent in selected}
        if expanded == selected:
            break
        selected = expanded
    rows = []
    for sid in sorted(selected):
        parent, profiles = sessions.get(sid, (None, set()))
        for mod, effort, scope in sorted(profiles or {(None, None, 'no_observado')},
                                         key=lambda item: tuple(v or '' for v in item)):
            rows.append(dict(thread_id=sid, parent_thread_id=parent, model=mod,
                             effort=effort, alcance=scope))
    return rows


def main(argv=None):
    parser = ArgumentosSeguros(description=__doc__)
    parser.add_argument('directorio')
    parser.add_argument('sids', nargs='+')
    # argparse también puede repetir argumentos privados en errores: salida fija.
    try:
        args = parser.parse_args(argv)
        result = observar(args.directorio, args.sids)
    except ErrorLectura:
        print('No se pudo leer una entrada válida.', file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())

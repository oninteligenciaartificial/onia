#!/usr/bin/env python3
"""Reescribe enlaces Markdown según mapa-rutas.json (old→new).

El mapa sale de los git mv reales. No usar git diff -M: con archivos idénticos
(copias de harness.py) Git empareja el renombre equivocado.


No toca los fixtures congelados de evaluacion-sesiones/casos ni el listado
histórico MAPA-listado-2026-11-08.md. Después actualiza las rutas y los hashes
vigentes de los registros de tarea para que sigan coincidiendo con los bytes.
El historial de cada registro conserva los hashes anteriores.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "_investigacion-onia" / "base-operativa"
MAP_PATH = Path(__file__).with_name("mapa-rutas.json")
SKIP_PARTS = (
    "evaluacion-sesiones/casos/",
    "consolidacion-harness/historico/",
)
SKIP_FILES = {"_investigacion-onia/base-operativa/99-archivo/MAPA-listado-2026-11-08.md"}
# Carpetas partidas: el grueso quedó en un sitio y una pieza salió aparte.
MANUAL = {
    "_investigacion-onia/base-operativa/compartibles":
        "_investigacion-onia/base-operativa/05-herramientas/compartibles",
    "_investigacion-onia/base-operativa/compartibles/skills":
        "_investigacion-onia/base-operativa/05-herramientas/compartibles/skills",
}
FENCE = re.compile(r"^( {0,3})(`{3,}|~{3,})")
LINK = re.compile(
    r"(?P<bang>!?)\[(?P<text>(?:[^\]\\]|\\.)*)\]"
    r"\((?P<open><)?(?P<url>[^)\s>]+)(?P<close>>)?(?P<title>\s+\"[^\"]*\")?\)"
)
REFDEF = re.compile(r"^(\[[^\]]+\]:\s*)(<?)(\S+?)(>?)(\s+.*)?$")
TOKEN = re.compile(
    r"(?<![A-Za-z0-9_./-])"
    r"((?:_investigacion-onia/)?base-operativa/(?:[A-Za-z0-9_.+-]+/)*[A-Za-z0-9_.+-]+)"
)


def git_renames():
    output = subprocess.check_output(
        ["git", "diff", "--cached", "--name-status", "-M", "--find-renames=100%"],
        cwd=ROOT, text=True)
    mapping = {}
    for line in output.splitlines():
        parts = line.split("\t")
        if parts and parts[0].startswith("R") and len(parts) == 3:
            mapping[parts[1]] = parts[2]
    if not mapping:
        raise SystemExit("No hay renombres en el índice. Ejecutar después de git mv.")
    return mapping


def uniform_prefixes(mapping):
    grouped = {}
    for old, new in mapping.items():
        parts = old.split("/")
        for index in range(1, len(parts)):
            grouped.setdefault("/".join(parts[:index]), []).append((old, new))
    prefixes = {}
    for prefix, pairs in grouped.items():
        news, ok = set(), True
        for old, new in pairs:
            rest = old[len(prefix) + 1:]
            if new.endswith(rest) and (len(new) == len(rest) or new[-(len(rest) + 1)] == "/"):
                news.add(new[:len(new) - len(rest)].rstrip("/"))
            else:
                ok = False
                break
        if ok and len(news) == 1:
            prefixes[prefix] = news.pop()
    return prefixes


def load_map():
    if MAP_PATH.is_file() and "--desde-git" not in sys.argv:
        data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
        return data["archivos"], data["prefijos"]
    files = git_renames()
    prefixes = uniform_prefixes(files)
    MAP_PATH.write_text(json.dumps({"archivos": files, "prefijos": prefixes},
                                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return files, prefixes


def forms(old, new):
    """Ruta de repo y las formas que aparecen en prosa, sin segmentos sueltos."""
    pairs = []
    for left, right in ((old, new),):
        pairs.append((left, right))
        needle = "_investigacion-onia/"
        if left.startswith(needle) and right.startswith(needle):
            pairs.append((left[len(needle):], right[len(needle):]))
        base = "_investigacion-onia/base-operativa/"
        if left.startswith(base) and right.startswith(base) and "/" in left[len(base):]:
            pairs.append((left[len(base):], right[len(base):]))
    return pairs


def build_lookup(files, prefixes):
    lookup = {}
    combined = {**prefixes, **files, **MANUAL}
    for old, new in combined.items():
        for left, right in forms(old, new):
            lookup[left] = right
    return lookup


def normalize(path):
    parts = []
    for part in Path(path).as_posix().split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            else:
                return None
        else:
            parts.append(part)
    return "/".join(parts)


def locate(old_rel, files, prefixes):
    old_rel = old_rel.rstrip("/")
    if old_rel in files:
        return files[old_rel]
    manual = None
    for prefix, dest in MANUAL.items():
        if old_rel == prefix or old_rel.startswith(prefix + "/"):
            if manual is None or len(prefix) > len(manual[0]):
                manual = (prefix, dest)
    if manual:
        candidate = manual[1] + old_rel[len(manual[0]):]
        if old_rel == manual[0] or (ROOT / candidate).exists():
            return candidate
    if (ROOT / old_rel).exists():
        return old_rel
    prefix = old_rel + "/"
    found = set()
    for old, new in files.items():
        if not old.startswith(prefix):
            continue
        rest = old[len(prefix):]
        if new.endswith(rest) and (len(new) == len(rest) or new[-(len(rest) + 1)] == "/"):
            found.add(new[:len(new) - len(rest)].rstrip("/"))
        else:
            return None
    if len(found) == 1:
        return found.pop()
    best = None
    for old_prefix, new_prefix in prefixes.items():
        if old_rel == old_prefix or old_rel.startswith(old_prefix + "/"):
            if best is None or len(old_prefix) > len(best[0]):
                best = (old_prefix, new_prefix)
    if best:
        return best[1] + old_rel[len(best[0]):]
    return None


def split_url(url):
    if "#" in url:
        path, fragment = url.split("#", 1)
        fragment = "#" + fragment
    else:
        path, fragment = url, ""
    if "?" in path:
        path, query = path.split("?", 1)
        fragment = "?" + query + fragment
    return path, fragment


def skipped(path):
    text = path.as_posix()
    return text in SKIP_FILES or any(part in text for part in SKIP_PARTS)


def rewrite_url(url, old_file, new_file, files, prefixes):
    if not url or url.startswith(("#", "mailto:", "http://", "https://", "data:")):
        return url, "externo"
    path, fragment = split_url(url)
    if not path or path.startswith(("#", "mailto:", "http://", "https://")):
        return url, "externo"
    if "\\" in path:
        path = path.replace("\\", "/")
    if path.startswith("/"):
        resolved = normalize(path.lstrip("/"))
    else:
        resolved = normalize(str(PurePosix(old_file).parent / path))
    if resolved is None:
        return url, "roto"
    target = locate(resolved, files, prefixes)
    if not target:
        return url, "roto"
    parent = PurePosix(new_file).parent.as_posix()
    if parent in ("", "."):
        parent = "."
    try:
        relative = Path(os.path.relpath(target, parent)).as_posix()
    except ValueError as exc:
        raise ValueError(f"{exc}: url={url!r} target={target!r} new_file={new_file!r} parent={parent!r}") from exc
    exists = (ROOT / target).exists()
    return relative + fragment, "resuelto" if exists else "roto"


class PurePosix(Path):
    def __new__(cls, *args):
        return Path(*args)


def rewrite_markdown(text, old_file, new_file, files, prefixes, stats):
    lines, fenced, fence = [], False, None
    for line in text.splitlines(keepends=True):
        mark = FENCE.match(line.rstrip("\r\n"))
        if mark:
            token = mark.group(2)[0]
            if not fenced:
                fenced, fence = True, token
            elif token == fence and len(mark.group(2)) >= 3:
                fenced = False
            lines.append(line)
            continue
        if fenced:
            lines.append(line)
            continue

        def replace_link(match):
            url = match.group("url")
            new_url, state = rewrite_url(url, old_file, new_file, files, prefixes)
            if state == "externo":
                stats["externos"] += 1
            elif state == "resuelto" and new_url != url:
                stats["corregidos"] += 1
            elif state == "resuelto":
                stats["ya_resolvian"] += 1
            else:
                stats["rotos"] += 1
                if new_url != url:
                    stats["rotos_reescritos"] += 1
            if new_url == url:
                return match.group(0)
            open_b = "<" if match.group("open") else ""
            close_b = ">" if match.group("close") or match.group("open") else ""
            title = match.group("title") or ""
            bang = match.group("bang") or ""
            return f"{bang}[{match.group('text')}]({open_b}{new_url}{close_b}{title})"

        updated = LINK.sub(replace_link, line)
        ref = REFDEF.match(updated.rstrip("\r\n"))
        if ref and not ref.group(3).startswith(("#", "http://", "https://", "mailto:")):
            new_url, state = rewrite_url(ref.group(3), old_file, new_file, files, prefixes)
            if state == "resuelto" and new_url != ref.group(3):
                stats["corregidos"] += 1
            elif state == "resuelto":
                stats["ya_resolvian"] += 1
            elif state == "roto":
                stats["rotos"] += 1
            ending = "\n" if updated.endswith("\n") else ""
            tail = ref.group(5) or ""
            updated = f"{ref.group(1)}{ref.group(2)}{new_url}{ref.group(4)}{tail}{ending}"
        lines.append(updated)
    return "".join(lines)


def remap_token(token, lookup):
    current = token.rstrip("/")
    while current:
        if current in lookup:
            return lookup[current] + token[len(current):]
        if "/" not in current:
            return None
        current = current.rsplit("/", 1)[0]
    return None


def rewrite_path_tokens(text, lookup, stats):
    def replace(match):
        token = match.group(1)
        mapped = remap_token(token, lookup)
        if mapped and mapped != token:
            stats["rutas_texto"] += 1
            return match.group(0).replace(token, mapped, 1)
        return match.group(0)
    return TOKEN.sub(replace, text)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def remap_repo(path, files, prefixes):
    full = path if path.startswith("_investigacion-onia/") else "_investigacion-onia/base-operativa/" + path
    found = locate(full, files, prefixes)
    if found and found.startswith("_investigacion-onia/base-operativa/"):
        return found[len("_investigacion-onia/base-operativa/"):]
    return path


def refresh_ref(ref, files, prefixes, changed_files):
    if not isinstance(ref, dict) or not isinstance(ref.get("archivo"), str):
        return False
    new_path = remap_repo(ref["archivo"], files, prefixes)
    target = BASE / new_path
    changed = new_path != ref["archivo"]
    ref["archivo"] = new_path
    if target.is_file() and new_path in changed_files:
        data = target.read_bytes()
        file_hash, size = digest(data), len(data)
        if ref.get("sha256") != file_hash or ref.get("bytes") != size:
            ref["sha256"] = file_hash
            ref["bytes"] = size
            changed = True
    return changed


def reconcile_tasks(files, prefixes, changed_files):
    updated = 0
    missing = []
    folder = BASE / "04-operacion-agentes" / "tareas"
    for path in sorted(folder.glob("*.json")):
        raw = path.read_bytes()
        crlf = b"\r\n" in raw and raw.replace(b"\r\n", b"").count(b"\n") == 0
        row = json.loads(raw.decode("utf-8"))
        dirty = False
        for ref in row.get("evidencias") or []:
            before = json.dumps(ref, sort_keys=True)
            if refresh_ref(ref, files, prefixes, changed_files):
                dirty = True
            if isinstance(ref, dict) and not (BASE / ref.get("archivo", "")).is_file():
                missing.append(f"{path.name}: {ref.get('archivo')}")
        for decision in row.get("decisiones") or []:
            if isinstance(decision, dict) and refresh_ref(decision.get("fuente"), files, prefixes, changed_files):
                dirty = True
        observed = ((row.get("ejecucion") or {}).get("observado") or {})
        if isinstance(observed, dict) and refresh_ref(observed.get("fuente"), files, prefixes, changed_files):
            dirty = True
        brief = row.get("briefing")
        if isinstance(brief, dict) and isinstance(brief.get("archivo"), str):
            new_path = remap_repo(brief["archivo"], files, prefixes)
            target = BASE / new_path
            if new_path != brief["archivo"]:
                brief["archivo"] = new_path
                dirty = True
            if target.is_file():
                encoded = target.read_bytes()
                content = encoded.decode("utf-8")
                file_hash = digest(encoded)
                if brief.get("contenido") != content or brief.get("sha256") != file_hash:
                    brief["contenido"] = content
                    brief["sha256"] = file_hash
                    brief["bytes"] = len(encoded)
                    dirty = True
            else:
                missing.append(f"{path.name}: briefing {new_path}")
        if dirty:
            text = json.dumps(row, ensure_ascii=False, indent=2) + "\n"
            if crlf:
                text = text.replace("\n", "\r\n")
            path.write_bytes(text.encode("utf-8"))
            updated += 1
    return updated, missing


def main():
    files, prefixes = load_map()
    lookup = build_lookup(files, prefixes)
    inverse = {new: old for old, new in files.items()}
    stats = {"corregidos": 0, "rotos": 0, "rotos_reescritos": 0, "ya_resolvian": 0,
             "externos": 0, "rutas_texto": 0, "markdown": 0, "omitidos": 0}
    changed_files = set()
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or skipped(path.relative_to(ROOT)):
            stats["omitidos"] += 1
            continue
        relative = path.relative_to(ROOT).as_posix()
        old = inverse.get(relative, relative)
        raw = path.read_bytes()
        original = raw.decode("utf-8")
        rewritten = rewrite_markdown(original, old, relative, files, prefixes, stats)
        rewritten = rewrite_path_tokens(rewritten, lookup, stats)
        if b"\r\n" in raw and raw.replace(b"\r\n", b"").count(b"\n") == 0:
            rewritten = rewritten.replace("\r\n", "\n").replace("\n", "\r\n")
        output = rewritten.encode("utf-8")
        if output != raw:
            path.write_bytes(output)
            if relative.startswith("_investigacion-onia/base-operativa/"):
                changed_files.add(relative[len("_investigacion-onia/base-operativa/"):])
            stats["markdown"] += 1
    tasks, missing = reconcile_tasks(files, prefixes, changed_files)
    report = {"enlaces_corregidos": stats["corregidos"], "enlaces_que_siguen_rotos": stats["rotos"],
              "de_ellos_reescritos_pero_sin_destino": stats["rotos_reescritos"],
              "enlaces_que_ya_resolvian": stats["ya_resolvian"], "enlaces_externos": stats["externos"],
              "rutas_en_prosa_actualizadas": stats["rutas_texto"], "markdown_modificados": stats["markdown"],
              "markdown_omitidos": stats["omitidos"], "registros_reconciliados": tasks,
              "referencias_sin_archivo": missing[:30], "referencias_sin_archivo_total": len(missing)}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

"""Registro único por tarea, local o compartible; no lanza agentes ni usa la red."""
import argparse
from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import sys
import tempfile
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[2]
PUBLIC_TASKS = "04-operacion-agentes/tareas/"
PUBLIC_EVIDENCE = "04-operacion-agentes/evidencias/"
PUBLIC_BRIEFS = "04-operacion-agentes/encargos/"
LEGACY_TASKS = "continuidad/tareas/"
LEGACY_EVIDENCE = "continuidad/evidencias/"
LEGACY_BRIEFS = "continuidad/encargos/"
STATES = {"preparado", "en_curso", "en_espera", "para_revision", "aceptado"}
CHECKS = {"pendiente", "fallo", "correcta"}
CLOSED_NEXT = "Encargo aceptado; conservar la evidencia. No iniciar nueva ejecución sin otro encargo."
EFFORTS = {"low", "medium", "high", "xhigh", "max", "ultra"}
EXTENSIONS = ("decisiones", "ejecucion", "asignacion")


def now():
    return datetime.now(timezone.utc).isoformat()


def safe_path(base, name):
    if not isinstance(name, str) or not name:
        raise ValueError("Se requiere una ruta relativa.")
    parts = PurePosixPath(name.replace("\\", "/")).parts
    if PurePosixPath(name).is_absolute() or PureWindowsPath(name).drive or ".." in parts:
        raise ValueError("Ruta fuera de la base.")
    if any(p.casefold() in {"privado", "onia-central", ".git"}
           or p.casefold().startswith(".env") or p.lower().endswith((".pem", ".key"))
           for p in parts):
        raise ValueError("Ruta privada o excluida.")
    base = Path(base).resolve()
    path = base.joinpath(*parts)
    for candidate in [path, *path.parents]:
        if candidate == base:
            break
        if os.path.lexists(candidate):
            info = candidate.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
                raise ValueError("La ruta contiene un enlace o reparse point.")
    if not path.resolve().is_relative_to(base):
        raise ValueError("Ruta fuera de la base.")
    return path


def prefer_existing(base, current, legacy):
    """Los registros nuevos van a la carpeta vigente. Uno ya guardado en continuidad/ se sigue leyendo."""
    current_path, legacy_path = safe_path(base, current), safe_path(base, legacy)
    if os.path.lexists(legacy_path) and not os.path.lexists(current_path):
        return legacy_path
    return current_path


def paths(base, task_id):
    if not isinstance(task_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", task_id):
        raise ValueError("ID inválido: usar minúsculas, números y guiones.")
    return (safe_path(base, "operacion/tareas/" + task_id + ".json"),
            prefer_existing(base, PUBLIC_TASKS + task_id + ".json", LEGACY_TASKS + task_id + ".json"))


def task_path(base, task_id, shared=None):
    local, public = paths(base, task_id)
    if os.path.lexists(local) and os.path.lexists(public):
        raise ValueError("ID ambiguo: hay dos registros. Conservarlos y reconciliar; no se eligió uno.")
    if shared is None:
        return public if os.path.lexists(public) else local
    return public if shared else local


def brief_path(base, task_id, shared=False):
    paths(base, task_id)
    if not shared:
        return safe_path(base, "operacion/encargos/" + task_id + ".md")
    return prefer_existing(base, PUBLIC_BRIEFS + task_id + ".md", LEGACY_BRIEFS + task_id + ".md")


def regular_bytes(path):
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("Se requiere un archivo regular existente: " + str(path))
    return path.read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def evidence(base, name, shared=False):
    path = safe_path(base, name)
    relative = path.relative_to(Path(base).resolve()).as_posix()
    if shared and not (relative.startswith(PUBLIC_EVIDENCE) or relative.startswith(LEGACY_EVIDENCE)):
        raise ValueError("Evidencia compartible debe estar saneada en " + PUBLIC_EVIDENCE)
    content = regular_bytes(path)
    return {"archivo": relative, "sha256": digest(content), "bytes": len(content)}


def validate_ref(ref):
    if not isinstance(ref, dict) or not isinstance(ref.get("archivo"), str):
        raise ValueError("Referencia de evidencia inválida.")
    if not isinstance(ref.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]):
        raise ValueError("Hash de evidencia inválido.")
    if "bytes" in ref and (type(ref["bytes"]) is not int or ref["bytes"] < 0):
        raise ValueError("Tamaño de evidencia inválido.")


def nonempty(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Se requiere contenido: " + label)
    return value.strip()


def active_decisions(decisions):
    replaced = {item["sustituye"] for item in decisions if item.get("sustituye")}
    return [item for item in decisions if item["id"] not in replaced]


def validate_extensions(row):
    decisions = row.get("decisiones", [])
    if not isinstance(decisions, list):
        raise ValueError("Decisiones inválidas.")
    seen, replaced = set(), set()
    for item in decisions:
        if not isinstance(item, dict):
            raise ValueError("Decisión inválida.")
        ident = nonempty(item.get("id"), "id de decisión")
        if ident != item["id"] or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", ident) or ident in seen:
            raise ValueError("Identificador de decisión inválido o duplicado.")
        for key in ("texto", "autor", "fecha"):
            nonempty(item.get(key), key)
        validate_ref(item.get("fuente"))
        previous = item.get("sustituye")
        if previous is not None:
            if not isinstance(previous, str) or previous not in seen or previous in replaced:
                raise ValueError("La decisión sustituida debe existir y estar vigente.")
            replaced.add(previous)
        seen.add(ident)
    execution = row.get("ejecucion")
    if execution is not None:
        if not isinstance(execution, dict):
            raise ValueError("Ficha de ejecución inválida.")
        for key in ("criterio", "escalamiento"):
            nonempty(execution.get(key), key)
        for key in ("recomendado", "solicitado", "observado"):
            profile = execution.get(key)
            if profile is None:
                continue
            if not isinstance(profile, dict):
                raise ValueError("Perfil de modelo inválido: " + key)
            nonempty(profile.get("modelo"), "modelo " + key)
            if profile.get("esfuerzo") not in EFFORTS:
                raise ValueError("Esfuerzo inválido: " + key)
            if key == "observado":
                validate_ref(profile.get("fuente"))
    assignment = row.get("asignacion")
    if assignment is not None:
        if not isinstance(assignment, dict):
            raise ValueError("Asignación inválida.")
        for key in ("responsable", "fecha"):
            nonempty(assignment.get(key), key)
        if assignment["responsable"] != assignment["responsable"].strip():
            raise ValueError("Responsable de asignación no canónico.")
        routes = assignment.get("rutas")
        if not isinstance(routes, list) or not routes or any(not isinstance(p, str) or not p for p in routes):
            raise ValueError("Asignación requiere rutas.")
        if type(assignment.get("revision_base")) is not int or assignment["revision_base"] < 1:
            raise ValueError("Revisión base de asignación inválida.")


def validate(row, task_id):
    if (not isinstance(row, dict) or type(row.get("schema")) is not int
            or row["schema"] not in (1, 2) or row.get("id") != task_id):
        raise ValueError("Esquema o identidad de tarea inválidos.")
    for key in ("objetivo", "estado", "proximo_paso", "resultado", "comprobacion", "actualizado"):
        if not isinstance(row.get(key), str):
            raise ValueError("Campo de tarea inválido: " + key)
    if not row["objetivo"].strip() or not row["proximo_paso"].strip():
        raise ValueError("Objetivo y siguiente paso requieren contenido.")
    if not isinstance(row.get("historial"), list) or not isinstance(row.get("evidencias"), list):
        raise ValueError("Historial o evidencias inválidos.")
    for ref in row["evidencias"]:
        validate_ref(ref)
    for entry in row["historial"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("evidencias"), list):
            raise ValueError("Entrada de historial inválida.")
        for ref in entry["evidencias"]:
            validate_ref(ref)
    if row["schema"] == 1:
        if row["estado"] not in {"preparado", "en_curso", "en_espera", "terminado"}:
            raise ValueError("Estado histórico inválido.")
        return
    if type(row.get("revision")) is not int or row["revision"] < 1:
        raise ValueError("Revisión inválida.")
    if type(row.get("compartible")) is not bool or row["estado"] not in STATES:
        raise ValueError("Alcance o estado inválido.")
    if row.get("verificacion") not in CHECKS:
        raise ValueError("Verificación inválida.")
    validate_extensions(row)
    brief = row.get("briefing")
    if brief is not None:
        validate_ref(brief)
        if (not isinstance(brief.get("contenido"), str)
                or digest(brief["contenido"].encode("utf-8")) != brief["sha256"]
                or len(brief["contenido"].encode("utf-8")) != brief.get("bytes")):
            raise ValueError("Contenido canónico del briefing alterado.")
    if row["estado"] in {"para_revision", "aceptado"}:
        if row["verificacion"] != "correcta" or not row["evidencias"] or not row["resultado"].strip() or not row["comprobacion"].strip():
            raise ValueError("Entrega requiere comprobación correcta, resultado y evidencia.")
    if row["estado"] == "aceptado":
        acceptance = row.get("aceptacion")
        if not isinstance(acceptance, dict) or any(not isinstance(acceptance.get(k), str) or not acceptance[k].strip()
                                                 for k in ("revisor", "criterio", "fecha")):
            raise ValueError("Falta aceptación explícita.")


def read_task(base, task_id):
    path = task_path(base, task_id)
    row = json.loads(regular_bytes(path).decode("utf-8"))
    validate(row, task_id)
    if row["schema"] == 1 and path == task_path(base, task_id, True):
        raise ValueError("Schema 1 sólo es histórico local; no publicar una copia como registro compartible.")
    if row["schema"] == 2 and path != task_path(base, task_id, row["compartible"]):
        raise ValueError("La ubicación contradice el alcance del registro.")
    return row


def verify(base, row, missing_brief=False):
    shared = row.get("compartible", False)
    # En v1 un archivo podía cambiar entre entradas. El historial registra esos
    # hashes anteriores; no implica que todos describan los bytes actuales.
    # En v2 update conserva un inventario acumulativo de evidencia inmutable.
    refs = list(row["evidencias"])
    refs.extend(item["fuente"] for item in row.get("decisiones", []))
    observed = (row.get("ejecucion") or {}).get("observado")
    if observed:
        refs.append(observed["fuente"])
    for ref in refs:
        referenced = safe_path(base, ref["archivo"])
        canonical = task_path(base, row["id"], shared)
        if referenced == canonical or (referenced.exists() and canonical.exists()
                                        and os.path.samefile(referenced, canonical)):
            raise ValueError("El registro canónico no puede ser su propia evidencia o fuente mutable.")
        actual = evidence(base, ref["archivo"], shared)
        if actual["sha256"] != ref["sha256"] or ("bytes" in ref and actual["bytes"] != ref["bytes"]):
            raise ValueError("Evidencia cambió: " + ref["archivo"])
    for route in (row.get("asignacion") or {}).get("rutas", []):
        if normalize_route(base, route) != route:
            raise ValueError("Ruta de asignación no canónica.")
    brief = row.get("briefing")
    if brief is not None:
        expected = brief_path(base, row["id"], shared).relative_to(Path(base).resolve()).as_posix()
        if brief["archivo"] != expected:
            raise ValueError("Ruta del briefing incompatible con el registro.")
        path = safe_path(base, brief["archivo"])
        if missing_brief and not os.path.lexists(path):
            return
        if digest(regular_bytes(path)) != brief["sha256"]:
            raise ValueError("Briefing cambió; no se actualizó su hash automáticamente.")


def atomic_json(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=path.parent, suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(row, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        if os.name != "nt":
            fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


@contextmanager
def locked(base, task_id, assignment=False):
    paths(base, task_id)
    lock = safe_path(base, "operacion/bloqueos/" + (".asignaciones" if assignment else task_id) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError("Tarea bloqueada. Comprobar proceso/propietario antes de retirar un lock abandonado.") from None
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump({"pid": os.getpid(), "fecha": now()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        yield
    finally:
        lock.unlink()


def expected(row, revision):
    actual = row.get("revision", 0)
    if type(revision) is not int or revision != actual:
        raise ValueError("Revisión obsoleta o ausente: esperada " + str(revision) + ", actual " + str(actual) + ".")


def materialize(base, row):
    brief = row.get("briefing")
    if brief is None:
        return
    path = safe_path(base, brief["archivo"])
    if os.path.lexists(path):
        if regular_bytes(path) != brief["contenido"].encode("utf-8"):
            raise ValueError("Briefing existente diferente; conservar y revisar.")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(brief["contenido"].encode("utf-8"))
        stream.flush()
        os.fsync(stream.fileno())


def create(base, task_id, goal, next_step, shared=False, briefing=None, execution=None):
    with locked(base, task_id):
        if any(os.path.lexists(p) for p in paths(base, task_id)):
            raise ValueError("La tarea ya existe; retomar, no sobrescribir.")
        row = {"schema": 2, "id": task_id, "revision": 1, "compartible": shared,
               "objetivo": goal, "estado": "preparado", "proximo_paso": next_step,
               "resultado": "", "comprobacion": "", "verificacion": "pendiente",
               "evidencias": [], "actualizado": now(), "historial": [], "briefing": None,
               "aceptacion": None}
        if execution is not None:
            row["ejecucion"] = deepcopy(execution)
        if briefing is not None:
            path = brief_path(base, task_id, shared)
            if os.path.lexists(path):
                raise ValueError("Briefing huérfano existente; conservar y revisar antes de crear.")
            content = briefing.encode("utf-8")
            row["briefing"] = {"archivo": path.relative_to(Path(base).resolve()).as_posix(),
                               "sha256": digest(content), "bytes": len(content), "contenido": briefing}
        validate(row, task_id)
        verify(base, row, missing_brief=True)
        # El JSON es la autoridad atómica. El Markdown es una proyección recuperable.
        atomic_json(task_path(base, task_id, shared), row)
        materialize(base, row)
        return row


def mutate(base, task_id, revision, transform, actor=None, review=False):
    with locked(base, task_id):
        row = read_task(base, task_id)
        expected(row, revision)
        if row["schema"] != 2:
            raise ValueError("Registro histórico: ejecutar migrar explícitamente con revisión 0.")
        verify(base, row)
        assignment = row.get("asignacion")
        if assignment and not review and actor != assignment["responsable"]:
            raise ValueError("Responsable distinto o ausente; indicar --actor y conciliar la asignación.")
        prior = {k: deepcopy(row[k]) for k in ("revision", "actualizado", "estado", "resultado",
                  "comprobacion", "verificacion", "evidencias", "proximo_paso", "aceptacion")}
        prior.update({k: deepcopy(row[k]) for k in EXTENSIONS if k in row})
        changed = transform(deepcopy(row))
        changed["historial"].append(prior)
        changed["revision"] += 1
        changed["actualizado"] = now()
        validate(changed, task_id)
        verify(base, changed)
        atomic_json(task_path(base, task_id), changed)
        return changed


def update(base, task_id, status, result, check, next_step, files, revision=None, verification="pendiente", actor=None):
    if status not in STATES - {"aceptado"}:
        raise ValueError("Estado inválido para actualizar; la aceptación usa aceptar.")
    def transform(row):
        refs = {ref["archivo"]: ref for ref in row["evidencias"]}
        for name in files:
            ref = evidence(base, name, row["compartible"])
            refs[ref["archivo"]] = ref
        row.update(estado=status, resultado=result, comprobacion=check, proximo_paso=next_step,
                   verificacion=verification, evidencias=list(refs.values()),
                   aceptacion=None)
        return row
    return mutate(base, task_id, revision, transform, actor=actor)


def accept(base, task_id, revision, reviewer, criterion, next_step=CLOSED_NEXT):
    reviewer = nonempty(reviewer, "revisor")
    def transform(row):
        if row["estado"] != "para_revision":
            raise ValueError("Sólo una entrega para_revision puede aceptarse.")
        if row.get("asignacion") and reviewer == row["asignacion"]["responsable"]:
            raise ValueError("El responsable ejecutor no puede autoaceptar su entrega.")
        row.update(estado="aceptado", proximo_paso=next_step,
                   aceptacion={"revisor": reviewer, "criterio": criterion, "fecha": now()})
        return row
    return mutate(base, task_id, revision, transform, review=True)


def recover(base, task_id, revision, actor=None):
    with locked(base, task_id):
        row = read_task(base, task_id)
        expected(row, revision)
        if row["schema"] != 2:
            raise ValueError("Recuperación requiere schema 2.")
        if row.get("asignacion") and actor != row["asignacion"]["responsable"]:
            raise ValueError("Responsable distinto o ausente para recuperar.")
        verify(base, row, missing_brief=True)
        materialize(base, row)
        verify(base, row)
        return {"tarea": row, "nota": "Proyección comprobada/recuperada; registro canónico sin cambios."}


def migrate(base, task_id, revision):
    with locked(base, task_id):
        row = read_task(base, task_id)
        expected(row, revision)
        if row["schema"] != 1:
            raise ValueError("La tarea ya usa schema 2; no se migró.")
        verify(base, row)
        old = deepcopy(row)
        brief = brief_path(base, task_id)
        row.update(schema=2, revision=1, compartible=False, verificacion="pendiente",
                   aceptacion=None, briefing=None, migracion={"fecha": now(), "estado_anterior": old["estado"]})
        if old["estado"] == "terminado":
            row["estado"] = "en_espera"
        if os.path.lexists(brief):
            content = regular_bytes(brief)
            row["briefing"] = {**evidence(base, brief.relative_to(Path(base).resolve()).as_posix()),
                               "contenido": content.decode("utf-8")}
        row["historial"].append({k: old[k] for k in ("actualizado", "estado", "resultado", "comprobacion",
                                                    "evidencias", "proximo_paso")})
        row["actualizado"] = now()
        validate(row, task_id)
        verify(base, row)
        atomic_json(task_path(base, task_id), row)
        return row


def brief_view(row):
    """Proyección de lectura: nunca reemplaza ni persiste el registro canónico."""
    result = {k: deepcopy(v) for k, v in row.items() if k != "historial"}
    if "decisiones" in result:
        result["decisiones"] = active_decisions(result["decisiones"])
    return result


def resume(base, task_id, complete=False):
    row = read_task(base, task_id)
    verify(base, row)
    return {"tarea": row if complete else brief_view(row),
            "vista": "completa" if complete else "breve",
            "contexto": {"entradas_historial": len(row["historial"]),
                         "decisiones_sustituidas": len(row.get("decisiones", [])) - len(active_decisions(row.get("decisiones", []))),
                         "detalle": "retomar " + task_id + " --completo",
                         "historial": "historial " + task_id + " [--revision N]"},
            "advertencias": [] if row["schema"] == 2 else
            ["Registro schema 1: lectura histórica; migrar explícitamente antes de modificar. Terminado no es aceptación."],
            "nota": "Integridad comprobada; comprobación y revisor son declaraciones, no identidad autenticada ni garantía de calidad."}


def history(base, task_id, revision=None):
    row = read_task(base, task_id)
    verify(base, row)
    entries = deepcopy(row["historial"])
    entries.append({k: v for k, v in row.items() if k not in {"historial", "briefing"}})
    if revision is not None:
        entries = [entry for entry in entries if entry.get("revision") == revision]
        if not entries:
            raise ValueError("Revisión histórica inexistente; schema 1 puede no numerar entradas.")
    return {"id": task_id, "revision_actual": row.get("revision"), "historial": entries,
            "nota": "Historia operativa; no sustituye las decisiones ni autorizaciones vigentes. Sin escrituras."}


def require_open(row):
    if row["estado"] in {"aceptado", "para_revision"}:
        raise ValueError("Reabrir explícitamente con actualizar antes de cambiar decisiones, ejecución o asignación.")


def decide(base, task_id, revision, decision_id, text, source, author, replaces=None, actor=None):
    def transform(row):
        require_open(row)
        row.setdefault("decisiones", []).append({"id": decision_id, "texto": nonempty(text, "decisión"),
            "fuente": evidence(base, source, row["compartible"]), "autor": nonempty(author, "autor"),
            "sustituye": replaces, "fecha": now()})
        return row
    return mutate(base, task_id, revision, transform, actor=actor)


def set_execution(base, task_id, revision, execution, actor=None):
    def transform(row):
        require_open(row)
        value = deepcopy(execution)
        if not isinstance(value, dict):
            raise ValueError("Ficha de ejecución inválida.")
        for key in ("recomendado", "solicitado", "observado"):
            value.setdefault(key, None)
        observed = value.get("observado")
        if isinstance(observed, dict) and isinstance(observed.get("fuente"), str):
            observed["fuente"] = evidence(base, observed["fuente"], row["compartible"])
        row["ejecucion"] = value
        return row
    return mutate(base, task_id, revision, transform, actor=actor)


def normalize_route(base, route):
    path = safe_path(base, route)
    relative = path.relative_to(Path(base).resolve()).as_posix()
    if relative == "." or any(":" in p or p.rstrip(". ") != p for p in PurePosixPath(relative).parts):
        raise ValueError("Ruta de asignación ambigua o demasiado amplia.")
    return relative


def overlapping(a, b):
    # Conservador también en Linux: entregas pueden terminar en Windows.
    left, right = PurePosixPath(a.casefold()).parts, PurePosixPath(b.casefold()).parts
    return left[:len(right)] == right or right[:len(left)] == left


def all_ids(base):
    folders = ("operacion/tareas", PUBLIC_TASKS.rstrip("/"), LEGACY_TASKS.rstrip("/"))
    return sorted({p.stem for folder in folders for p in safe_path(base, folder).glob("*.json")})


def assign(base, task_id, revision, responsible=None, routes=(), actor=None, replace=False, release=False):
    # Serializa sólo reservas de este checkout. Nunca bloquea editores externos o clones.
    with locked(base, task_id, assignment=True):
        normalized = list(dict.fromkeys(normalize_route(base, route) for route in routes))
        if release and (responsible is not None or normalized or replace):
            raise ValueError("Liberar no admite responsable, rutas ni reasignación.")
        if not release:
            nonempty(responsible, "responsable")
            if not normalized:
                raise ValueError("La asignación necesita rutas.")
            for other_id in all_ids(base):
                if other_id == task_id:
                    continue
                other = read_task(base, other_id)
                assignment = other.get("asignacion")
                if assignment:
                    verify(base, other)
                    if any(overlapping(a, b) for a in normalized for b in assignment["rutas"]):
                        raise ValueError("Colisión de rutas con " + other_id + "; conservar trabajos y conciliar antes de asignar.")
        def transform(row):
            previous = row.get("asignacion")
            if release:
                if not previous:
                    raise ValueError("No hay asignación que liberar.")
                row["asignacion"] = None
            else:
                require_open(row)
                if previous and not replace:
                    raise ValueError("Asignación existente: usar --reasignar con actor y revisión vigentes.")
                row["asignacion"] = {"responsable": responsible.strip(), "rutas": normalized,
                                     "revision_base": revision, "fecha": now()}
            return row
        return mutate(base, task_id, revision, transform, actor=actor)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("listar")
    p = sub.add_parser("crear")
    p.add_argument("id")
    p.add_argument("--objetivo", required=True)
    p.add_argument("--siguiente", required=True)
    p.add_argument("--compartible", action="store_true", help="Estado saneado versionable; no copia tareas privadas.")
    p = sub.add_parser("retomar")
    p.add_argument("id")
    p.add_argument("--completo", action="store_true", help="Incluir el registro íntegro; por defecto omite historia y decisiones sustituidas.")
    p = sub.add_parser("historial")
    p.add_argument("id")
    p.add_argument("--revision", type=int)
    p = sub.add_parser("actualizar")
    p.add_argument("id")
    p.add_argument("--estado", choices=sorted(STATES - {"aceptado"}), required=True)
    p.add_argument("--resultado", required=True)
    p.add_argument("--comprobacion", default="")
    p.add_argument("--verificacion", choices=sorted(CHECKS), default="pendiente")
    p.add_argument("--siguiente", required=True)
    p.add_argument("--evidencia", action="append", default=[])
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--actor", help="Responsable declarado si existe asignación; no autentica identidad.")
    p = sub.add_parser("aceptar")
    p.add_argument("id")
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--revisor", required=True)
    p.add_argument("--criterio", required=True)
    p.add_argument("--siguiente", default=CLOSED_NEXT, help="Próximo paso después de aceptar; por defecto cierra el encargo.")
    for command in ("recuperar", "migrar"):
        p = sub.add_parser(command)
        p.add_argument("id")
        p.add_argument("--revision-esperada", type=int, required=True)
        if command == "recuperar":
            p.add_argument("--actor")
    for command in ("decidir", "ejecucion", "asignar"):
        p = sub.add_parser(command)
        p.add_argument("id")
        p.add_argument("--revision-esperada", type=int, required=True)
        p.add_argument("--actor")
        if command == "decidir":
            p.add_argument("--decision", required=True)
            p.add_argument("--texto", required=True)
            p.add_argument("--fuente", required=True, help="Archivo de procedencia conservado; compartible exige 04-operacion-agentes/evidencias/.")
            p.add_argument("--autor", required=True)
            p.add_argument("--sustituye")
        elif command == "ejecucion":
            p.add_argument("--ficha", required=True, help="JSON relativo a la base; no modifica el runtime ni lanza modelos.")
        else:
            p.add_argument("--responsable")
            p.add_argument("--ruta", action="append", default=[])
            p.add_argument("--reasignar", action="store_true")
            p.add_argument("--liberar", action="store_true")
    args = parser.parse_args(argv)
    base = args.base.resolve()
    if args.command == "crear":
        data = create(base, args.id, args.objetivo, args.siguiente, args.compartible)
    elif args.command == "actualizar":
        data = update(base, args.id, args.estado, args.resultado, args.comprobacion, args.siguiente,
                      args.evidencia, args.revision_esperada, args.verificacion, actor=args.actor)
    elif args.command == "aceptar":
        data = accept(base, args.id, args.revision_esperada, args.revisor, args.criterio, args.siguiente)
    elif args.command == "recuperar":
        data = recover(base, args.id, args.revision_esperada, actor=args.actor)
        data["tarea"] = brief_view(data["tarea"])
    elif args.command == "migrar":
        data = migrate(base, args.id, args.revision_esperada)
    elif args.command == "retomar":
        data = resume(base, args.id, complete=args.completo)
    elif args.command == "historial":
        data = history(base, args.id, args.revision)
    elif args.command == "decidir":
        data = decide(base, args.id, args.revision_esperada, args.decision, args.texto,
                      args.fuente, args.autor, args.sustituye, actor=args.actor)
    elif args.command == "ejecucion":
        ficha = json.loads(regular_bytes(safe_path(base, args.ficha)).decode("utf-8"))
        data = set_execution(base, args.id, args.revision_esperada, ficha, actor=args.actor)
    elif args.command == "asignar":
        data = assign(base, args.id, args.revision_esperada, args.responsable, args.ruta,
                      actor=args.actor, replace=args.reasignar, release=args.liberar)
    else:
        data = [{k: row[k] for k in ("id", "objetivo", "estado", "proximo_paso")}
                for row in (read_task(base, task_id) for task_id in all_ids(base))]
    if isinstance(data, dict) and "schema" in data:
        data = brief_view(data)
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)

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

BASE = Path(__file__).resolve().parents[1]
STATES = {"preparado", "en_curso", "en_espera", "para_revision", "aceptado"}
CHECKS = {"pendiente", "fallo", "correcta"}


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


def paths(base, task_id):
    if not isinstance(task_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", task_id):
        raise ValueError("ID inválido: usar minúsculas, números y guiones.")
    return (safe_path(base, "operacion/tareas/" + task_id + ".json"),
            safe_path(base, "continuidad/tareas/" + task_id + ".json"))


def task_path(base, task_id, shared=None):
    local, public = paths(base, task_id)
    if os.path.lexists(local) and os.path.lexists(public):
        raise ValueError("ID ambiguo: hay dos registros. Conservarlos y reconciliar; no se eligió uno.")
    if shared is None:
        return public if os.path.lexists(public) else local
    return public if shared else local


def brief_path(base, task_id, shared=False):
    paths(base, task_id)
    return safe_path(base, ("continuidad" if shared else "operacion") + "/encargos/" + task_id + ".md")


def regular_bytes(path):
    if not path.is_file() or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("Se requiere un archivo regular existente: " + str(path))
    return path.read_bytes()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def evidence(base, name, shared=False):
    path = safe_path(base, name)
    relative = path.relative_to(Path(base).resolve()).as_posix()
    if shared and not relative.startswith("continuidad/evidencias/"):
        raise ValueError("Evidencia compartible debe estar saneada en continuidad/evidencias/.")
    content = regular_bytes(path)
    return {"archivo": relative, "sha256": digest(content), "bytes": len(content)}


def validate_ref(ref):
    if not isinstance(ref, dict) or not isinstance(ref.get("archivo"), str):
        raise ValueError("Referencia de evidencia inválida.")
    if not isinstance(ref.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", ref["sha256"]):
        raise ValueError("Hash de evidencia inválido.")
    if "bytes" in ref and (type(ref["bytes"]) is not int or ref["bytes"] < 0):
        raise ValueError("Tamaño de evidencia inválido.")


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
    refs = row["evidencias"]
    for ref in refs:
        actual = evidence(base, ref["archivo"], shared)
        if actual["sha256"] != ref["sha256"] or ("bytes" in ref and actual["bytes"] != ref["bytes"]):
            raise ValueError("Evidencia cambió: " + ref["archivo"])
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
def locked(base, task_id):
    paths(base, task_id)
    lock = safe_path(base, "operacion/bloqueos/" + task_id + ".lock")
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


def create(base, task_id, goal, next_step, shared=False, briefing=None):
    with locked(base, task_id):
        if any(os.path.lexists(p) for p in paths(base, task_id)):
            raise ValueError("La tarea ya existe; retomar, no sobrescribir.")
        row = {"schema": 2, "id": task_id, "revision": 1, "compartible": shared,
               "objetivo": goal, "estado": "preparado", "proximo_paso": next_step,
               "resultado": "", "comprobacion": "", "verificacion": "pendiente",
               "evidencias": [], "actualizado": now(), "historial": [], "briefing": None,
               "aceptacion": None}
        if briefing is not None:
            path = brief_path(base, task_id, shared)
            if os.path.lexists(path):
                raise ValueError("Briefing huérfano existente; conservar y revisar antes de crear.")
            content = briefing.encode("utf-8")
            row["briefing"] = {"archivo": path.relative_to(Path(base).resolve()).as_posix(),
                               "sha256": digest(content), "bytes": len(content), "contenido": briefing}
        validate(row, task_id)
        # El JSON es la autoridad atómica. El Markdown es una proyección recuperable.
        atomic_json(task_path(base, task_id, shared), row)
        materialize(base, row)
        return row


def mutate(base, task_id, revision, transform):
    with locked(base, task_id):
        row = read_task(base, task_id)
        expected(row, revision)
        if row["schema"] != 2:
            raise ValueError("Registro histórico: ejecutar migrar explícitamente con revisión 0.")
        verify(base, row)
        prior = {k: deepcopy(row[k]) for k in ("revision", "actualizado", "estado", "resultado",
                  "comprobacion", "verificacion", "evidencias", "proximo_paso", "aceptacion")}
        changed = transform(deepcopy(row))
        changed["historial"].append(prior)
        changed["revision"] += 1
        changed["actualizado"] = now()
        validate(changed, task_id)
        verify(base, changed)
        atomic_json(task_path(base, task_id), changed)
        return changed


def update(base, task_id, status, result, check, next_step, files, revision=None, verification="pendiente"):
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
    return mutate(base, task_id, revision, transform)


def accept(base, task_id, revision, reviewer, criterion):
    def transform(row):
        if row["estado"] != "para_revision":
            raise ValueError("Sólo una entrega para_revision puede aceptarse.")
        row.update(estado="aceptado", aceptacion={"revisor": reviewer, "criterio": criterion, "fecha": now()})
        return row
    return mutate(base, task_id, revision, transform)


def recover(base, task_id, revision):
    with locked(base, task_id):
        row = read_task(base, task_id)
        expected(row, revision)
        if row["schema"] != 2:
            raise ValueError("Recuperación requiere schema 2.")
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


def resume(base, task_id):
    row = read_task(base, task_id)
    verify(base, row)
    return {"tarea": row, "advertencias": [] if row["schema"] == 2 else
            ["Registro schema 1: lectura histórica; migrar explícitamente antes de modificar. Terminado no es aceptación."],
            "nota": "Integridad comprobada; comprobación y revisor son declaraciones, no identidad autenticada ni garantía de calidad."}


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
    p = sub.add_parser("actualizar")
    p.add_argument("id")
    p.add_argument("--estado", choices=sorted(STATES - {"aceptado"}), required=True)
    p.add_argument("--resultado", required=True)
    p.add_argument("--comprobacion", default="")
    p.add_argument("--verificacion", choices=sorted(CHECKS), default="pendiente")
    p.add_argument("--siguiente", required=True)
    p.add_argument("--evidencia", action="append", default=[])
    p.add_argument("--revision-esperada", type=int, required=True)
    p = sub.add_parser("aceptar")
    p.add_argument("id")
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--revisor", required=True)
    p.add_argument("--criterio", required=True)
    for command in ("recuperar", "migrar"):
        p = sub.add_parser(command)
        p.add_argument("id")
        p.add_argument("--revision-esperada", type=int, required=True)
    args = parser.parse_args(argv)
    base = args.base.resolve()
    if args.command == "crear":
        data = create(base, args.id, args.objetivo, args.siguiente, args.compartible)
    elif args.command == "actualizar":
        data = update(base, args.id, args.estado, args.resultado, args.comprobacion, args.siguiente,
                      args.evidencia, args.revision_esperada, args.verificacion)
    elif args.command == "aceptar":
        data = accept(base, args.id, args.revision_esperada, args.revisor, args.criterio)
    elif args.command in {"recuperar", "migrar"}:
        data = (recover if args.command == "recuperar" else migrate)(base, args.id, args.revision_esperada)
    elif args.command == "retomar":
        data = resume(base, args.id)
    else:
        ids = {p.stem for folder in ("operacion/tareas", "continuidad/tareas")
               for p in safe_path(base, folder).glob("*.json")}
        data = [{k: row[k] for k in ("id", "objetivo", "estado", "proximo_paso")}
                for row in (read_task(base, task_id) for task_id in sorted(ids))]
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)

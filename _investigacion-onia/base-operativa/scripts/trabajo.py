"""Registro local de tareas: no lanza agentes, red ni comandos externos."""
import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def task_path(base, task_id):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", task_id):
        raise ValueError("ID inválido: usar minúsculas, números y guiones.")
    return base / "operacion" / "tareas" / (task_id + ".json")


def evidence(base, name):
    path = (base / name).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError("La evidencia debe ser un archivo existente dentro de la base.")
    # Nunca tratar credenciales o contexto personal como evidencia exportable.
    rel = path.relative_to(base.resolve())
    if "privado" in rel.parts or any(p.startswith('.env') for p in rel.parts):
        raise ValueError("La evidencia no puede ser contexto privado ni un archivo .env.")
    return {"archivo": rel.as_posix(), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def read_task(base, task_id):
    return json.loads(task_path(base, task_id).read_text(encoding="utf-8"))


def save_task(base, task_id, transform):
    path = task_path(base, task_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_suffix(".lock")
    # Una segunda escritura debe esperar/revisar, no perder la primera.
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError("Tarea bloqueada por otra escritura. Revisar el proceso antes de reintentar.")
    os.close(fd)
    temp = None
    try:
        prior = read_task(base, task_id) if path.exists() else None
        result = transform(prior)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         suffix=".tmp", delete=False) as f:
            temp = Path(f.name)
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(temp, path)
        return result
    finally:
        if temp and temp.exists():
            temp.unlink()
        lock.unlink()


def create(base, task_id, goal, next_step):
    def transform(prior):
        if prior is not None:
            raise ValueError("La tarea ya existe. Retomarla o actualizarla; no sobrescribirla.")
        return {"schema": 1, "id": task_id, "objetivo": goal, "estado": "preparado",
                "proximo_paso": next_step, "resultado": "", "comprobacion": "",
                "evidencias": [], "actualizado": now(), "historial": []}
    return save_task(base, task_id, transform)


def update(base, task_id, status, result, check, next_step, files):
    if status == "terminado" and (not files or not check.strip() or not result.strip()):
        raise ValueError("Terminado requiere resultado, comprobación y al menos una evidencia.")
    refs = [evidence(base, p) for p in files]
    def transform(prior):
        if prior is None:
            raise ValueError("La tarea no existe.")
        prior["historial"].append({k: prior[k] for k in
                                   ("actualizado", "estado", "resultado", "comprobacion", "evidencias", "proximo_paso")})
        prior.update(estado=status, resultado=result, comprobacion=check,
                     proximo_paso=next_step, evidencias=refs, actualizado=now())
        return prior
    return save_task(base, task_id, transform)


def resume(base, task_id):
    result = read_task(base, task_id)
    warnings = []
    for item in result["evidencias"]:
        try:
            if evidence(base, item["archivo"])["sha256"] != item["sha256"]:
                warnings.append("Evidencia cambió: " + item["archivo"])
        except ValueError:
            warnings.append("Evidencia inaccesible: " + item["archivo"])
    return {"tarea": result, "advertencias": warnings,
            "nota": "Estado registrado por el ejecutor; los hashes comprueban integridad, no calidad."}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("listar")
    p = sub.add_parser("crear")
    p.add_argument("id")
    p.add_argument("--objetivo", required=True)
    p.add_argument("--siguiente", required=True)
    p = sub.add_parser("retomar")
    p.add_argument("id")
    p = sub.add_parser("actualizar")
    p.add_argument("id")
    p.add_argument("--estado", choices=["preparado", "en_curso", "en_espera", "terminado"], required=True)
    p.add_argument("--resultado", required=True)
    p.add_argument("--comprobacion", default="")
    p.add_argument("--siguiente", required=True)
    p.add_argument("--evidencia", action="append", default=[])
    args = parser.parse_args()
    base = args.base.resolve()
    if args.command == "crear":
        data = create(base, args.id, args.objetivo, args.siguiente)
    elif args.command == "actualizar":
        data = update(base, args.id, args.estado, args.resultado, args.comprobacion, args.siguiente, args.evidencia)
    elif args.command == "retomar":
        data = resume(base, args.id)
    else:
        data = []
        for p in sorted((base / "operacion" / "tareas").glob("*.json")):
            row = json.loads(p.read_text(encoding="utf-8"))
            data.append({k: row[k] for k in ("id", "objetivo", "estado", "proximo_paso")})
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)

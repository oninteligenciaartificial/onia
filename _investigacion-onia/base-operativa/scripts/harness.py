"""Prepara encargos y comprueba archivos; no crea agentes ni ejecuta red o tareas."""
import argparse
import json
import os
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

import trabajo

BASE = Path(__file__).resolve().parents[1]
LIMITACION = ("Este comando no crea agentes, abre chats, ejecuta encargos ni usa la red. "
              "El registro y briefing quedan en operacion/, ignorado por Git; "
              "no se sincronizan automáticamente entre entornos.")


def safe_path(base, relative):
    """Valida antes de leer o escribir; incluye destinos de enlaces existentes."""
    if not isinstance(relative, str) or not relative:
        raise ValueError("Se requiere una ruta relativa dentro de la base.")
    parts = PurePosixPath(relative.replace("\\", "/")).parts
    if (PurePosixPath(relative).is_absolute() or PureWindowsPath(relative).drive
            or ".." in parts):
        raise ValueError("Ruta fuera de la base: " + relative)
    base = base.resolve()
    path = (base / Path(*parts)).resolve()
    if not path.is_relative_to(base):
        raise ValueError("La ruta o su enlace sale de la base: " + relative)
    for part in path.relative_to(base).parts:
        if part.casefold() in {"privado", "onia-central"} or part.casefold().startswith(".env"):
            raise ValueError("Contexto privado o excluido no permitido: " + relative)
    return path


def manifest(base):
    path = safe_path(base, "orquestacion.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError("Falta orquestacion.json. Verificar la base y actualizar el checkout de onia.") from None
    if data.get("schema") != 1 or data.get("reglas") != "reglas-comunes.md":
        raise ValueError("Manifest incompatible: se requiere schema 1 y reglas-comunes.md.")
    skills, areas = data.get("skills"), data.get("areas")
    if not isinstance(skills, dict) or not skills or not isinstance(areas, dict) or not areas:
        raise ValueError("Manifest inválido: se requieren skills y áreas declaradas.")
    paths = [data["reglas"], *data.get("contexto_comun", []),
             *data.get("archivos_cloud", []), *skills.values()]
    for name, route in areas.items():
        if not isinstance(route, dict) or route.get("skill_directora") not in skills:
            raise ValueError("Área sin skill directora válida: " + name)
        support = route.get("skills_apoyo", [])
        if not isinstance(support, list) or any(item not in skills for item in support):
            raise ValueError("Área con skill de apoyo desconocida: " + name)
        if route.get("modo") not in {"encargo", "briefing"}:
            raise ValueError("Área sin modo válido: " + name)
        if not isinstance(route.get("salidas"), list) or not route["salidas"]:
            raise ValueError("Área sin salidas definidas: " + name)
        paths.extend(route.get("contexto", []))
    for relative in paths:
        safe_path(base, relative)
    return data


def doctor(base):
    result = {"base": str(base.resolve()), "archivos": [], "errores": [],
              "limite": "Sólo presencia de archivos. No prueba instalación, descubrimiento de skills, "
                        "navegador, secretos, conectividad ni publicación cloud."}
    try:
        data = manifest(base)
        paths = [data["reglas"], *data["contexto_comun"],
                 *data["archivos_cloud"], *data["skills"].values()]
        for route in data["areas"].values():
            paths.extend(route["contexto"])
        for relative in dict.fromkeys(paths):
            present = safe_path(base, relative).is_file()
            result["archivos"].append({"ruta": relative, "presente": present})
            if not present:
                result["errores"].append("Falta " + relative + ". Verificar la ruta base y HEAD; "
                                         "actualizar el checkout de onia sin descartar cambios. "
                                         "Los tests Python no acreditan este archivo.")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result["errores"].append(str(exc))
    result["ok"] = not result["errores"]
    return result


def task_paths(base, task_id):
    # Reutiliza la validación de ID del registro existente antes de construir rutas.
    base = base.resolve()
    task = trabajo.task_path(base, task_id)
    brief = base / "operacion" / "encargos" / (task_id + ".md")
    for path in (task, task.with_suffix(".lock"), brief):
        safe_path(base, path.relative_to(base).as_posix())
        # No reemplazar enlaces ni escribir registros a través de un padre enlazado.
        for candidate in [path, *path.parents]:
            if candidate == base:
                break
            if os.path.lexists(candidate) and candidate.resolve() != candidate:
                raise ValueError("La ruta operativa contiene un enlace; no se modificó: " + str(candidate))
    return task, brief


def prepare(base, task_id, area, goal, deliverable, acceptance, inputs=None, skill=None,
            ensayo=False, investigacion=None, capacidad=None, hipotesis=None, control=None, leccion=None,
            apoyos=None):
    base = base.resolve()
    task, brief = task_paths(base, task_id)
    data = manifest(base)
    if area not in data["areas"]:
        raise ValueError("Área inválida. Elegir: " + ", ".join(data["areas"]))
    if not all(isinstance(value, str) and value.strip() for value in (goal, deliverable, acceptance)):
        raise ValueError("Objetivo, entregable y aceptación deben tener contenido.")
    datos_ensayo = (investigacion, capacidad, hipotesis, control, leccion)
    if ensayo:
        if not all(isinstance(value, str) and value.strip() for value in datos_ensayo):
            raise ValueError("Ensayo requiere investigación, capacidad/fuente, hipótesis, control/criterio y lección previa.")
        fuente = safe_path(base, investigacion.strip())
        if not fuente.is_file():
            raise ValueError("La investigación debe enlazar un archivo existente dentro de la base.")
        investigacion = fuente.relative_to(base).as_posix()
    elif any(value is not None for value in datos_ensayo):
        raise ValueError("Los datos de investigación requieren declarar --ensayo.")
    if os.path.lexists(task) or os.path.lexists(brief):
        raise ValueError("El encargo ya existe. Usar retomar; no se sobrescribió ningún archivo.")
    route = data["areas"][area]
    allowed_skills = list(dict.fromkeys([route["skill_directora"], *route.get("skills_apoyo", [])]))
    skill = route["skill_directora"] if skill is None else skill
    if skill not in allowed_skills:
        raise ValueError("Skill no habilitada para el área " + area + ". Elegir: " + ", ".join(allowed_skills))
    if skill.startswith("tercero-"):
        raise ValueError("Las referencias de terceros se seleccionan como apoyo, no como directora.")
    support = [name for name in allowed_skills if name != skill]
    selected_support = list(dict.fromkeys(apoyos or []))
    if any(name not in support for name in selected_support):
        raise ValueError("Apoyo no habilitado para el área o elegido como directora.")
    context = list(dict.fromkeys([data["reglas"], *data["contexto_comun"],
                                 *route["contexto"], data["skills"][skill],
                                 *[data["skills"][name] for name in selected_support]]))
    for relative in [*context, *[data["skills"][name] for name in support]]:
        if not safe_path(base, relative).is_file():
            raise ValueError("Falta contexto " + relative + ". Ejecutar doctor y revisar checkout.")
    lines = ["# Encargo " + task_id, "", "Área: " + area,
             "Modo: " + route["modo"], "Skill directora: " + skill, "",
             "## Objetivo", "", goal.strip(), "", "## Entregable", "", deliverable.strip(),
             "", "## Criterio de aceptación", "", acceptance.strip(), "",
             "## Entrada y alcance", "", route["alcance"], ""]
    lines.extend("- " + item for item in (inputs or ["Sin entradas adicionales indicadas."]))
    if ensayo:
        lines.extend(["", "## Investigación previa al ensayo", "",
                      "- Investigación: [fuente](../../" + investigacion + ")",
                      "- Capacidad y fuente: " + capacidad.strip(),
                      "- Hipótesis: " + hipotesis.strip(),
                      "- Control y criterio que cambia la decisión: " + control.strip(),
                      "- Lección previa: " + leccion.strip()])
    lines.extend(["", "## Contexto mínimo", "",
                  "Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.", ""])
    lines.extend("- [" + relative + "](../../" + relative + ")" for relative in context)
    if support:
        lines.extend(["", "## Skills de apoyo disponibles", "",
                      "No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada "
                      "del encargo; no reemplazan la skill directora elegida.", ""])
        lines.extend("- [" + name + "](../../" + data["skills"][name] + ")" for name in support)
    lines.extend(["", "## Salidas de referencia del área", ""])
    lines.extend("- " + item for item in route["salidas"])
    lines.extend(["", "## Registro", "", "Estado: [registro de trabajo](../tareas/" + task_id + ".json).",
                  "Consultar el registro al retomar; este briefing no duplica su estado.", "", LIMITACION, ""])
    brief.parent.mkdir(parents=True, exist_ok=True)
    # Creación exclusiva: un segundo proceso no reemplaza este briefing.
    with brief.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))
    try:
        record = trabajo.create(base, task_id, goal.strip(),
                                "Leer operacion/encargos/" + task_id + ".md y ejecutar el encargo dentro de su alcance.")
    except Exception:
        brief.unlink()
        raise
    return {"tarea": record, "briefing": brief.relative_to(base).as_posix(),
            "area": area, "skill_directora": skill, "skills_apoyo": support,
            "apoyos_seleccionados": selected_support, "modo": route["modo"], "nota": LIMITACION}


def resume(base, task_id):
    _, brief = task_paths(base, task_id)
    result = trabajo.resume(base.resolve(), task_id)
    result["briefing"] = brief.read_text(encoding="utf-8")
    result["nota_harness"] = LIMITACION
    return result


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    p = commands.add_parser("preparar", help="Guardar un encargo sin ejecutarlo.")
    p.add_argument("id")
    p.add_argument("--area", required=True)
    p.add_argument("--skill", help="Skill directora para este encargo, entre las declaradas para el área.")
    p.add_argument("--objetivo", required=True)
    p.add_argument("--entregable", required=True)
    p.add_argument("--aceptacion", required=True)
    p.add_argument("--entrada", action="append", default=[])
    p.add_argument("--apoyo", action="append", default=[], help="Apoyo pertinente del área; se puede repetir.")
    p.add_argument("--ensayo", action="store_true", help="Declarar un ensayo que requiere investigación previa.")
    p.add_argument("--investigacion", help="Archivo existente relativo a la base, con investigación previa.")
    p.add_argument("--capacidad", help="Capacidad relevante y fuente en la investigación.")
    p.add_argument("--hipotesis", help="Hipótesis e incertidumbre a resolver.")
    p.add_argument("--control", help="Control y resultado que cambia la decisión.")
    p.add_argument("--leccion", help="Lección previa aplicable.")
    p = commands.add_parser("retomar")
    p.add_argument("id")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            result = doctor(args.base)
            code = 0 if result["ok"] else 1
        elif args.command == "preparar":
            result = prepare(args.base, args.id, args.area, args.objetivo,
                             args.entregable, args.aceptacion, args.entrada, skill=args.skill,
                             ensayo=args.ensayo, investigacion=args.investigacion,
                             capacidad=args.capacidad, hipotesis=args.hipotesis,
                             control=args.control, leccion=args.leccion, apoyos=args.apoyo)
            code = 0
        else:
            result, code = resume(args.base, args.id), 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result, code = {"error": str(exc)}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())

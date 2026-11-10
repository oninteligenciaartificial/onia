"""Prepara y coordina tareas; lanza, retoma y revisa sesiones Codex con worktrees."""
import argparse
import json
import os
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath

import trabajo

BASE = Path(__file__).resolve().parents[2]
REGLAS = "04-operacion-agentes/reglas-comunes.md"
LIMITACION = ("Preparar/retomar sólo recuperan archivos y no crean agentes. "
              "Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. "
              "--dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. "
              "No hay scheduler ni permisos implícitos para servicios externos.")


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
    path = safe_path(base, "04-operacion-agentes/orquestacion.json")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError("Falta 04-operacion-agentes/orquestacion.json. Verificar la base y actualizar el checkout de onia.") from None
    if data.get("schema") != 1 or data.get("reglas") != REGLAS:
        raise ValueError("Manifest incompatible: se requiere schema 1 y " + REGLAS + ".")
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
    profiles = data.get("perfiles_ejecucion", {})
    if not isinstance(profiles, dict):
        raise ValueError("Perfiles de ejecución inválidos.")
    for profile in profiles.values():
        if not isinstance(profile, dict):
            raise ValueError("Perfil de ejecución inválido.")
        trabajo.validate_extensions({"ejecucion": {"recomendado": profile,
            "criterio": profile.get("criterio"), "escalamiento": profile.get("escalamiento")}})
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


def task_paths(base, task_id, shared=None):
    # Reutiliza la validación de ID del registro existente antes de construir rutas.
    base = base.resolve()
    task = trabajo.task_path(base, task_id, shared)
    shared = task == trabajo.task_path(base, task_id, True)
    brief = trabajo.brief_path(base, task_id, shared)
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
            apoyos=None, shared=False, profile=None):
    base = base.resolve()
    task, brief = task_paths(base, task_id, shared)
    data = manifest(base)
    execution = None
    if profile is not None:
        selected = data.get("perfiles_ejecucion", {}).get(profile)
        if selected is None:
            raise ValueError("Perfil de ejecución desconocido; elegir uno declarado en orquestacion.json.")
        execution = {"perfil": profile,
                     "recomendado": {k: selected[k] for k in ("modelo", "esfuerzo")},
                     "solicitado": None, "observado": None,
                     "criterio": selected["criterio"], "escalamiento": selected["escalamiento"]}
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
    if any(os.path.lexists(p) for p in (*trabajo.paths(base, task_id),
                                       trabajo.brief_path(base, task_id, False),
                                       trabajo.brief_path(base, task_id, True))):
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
    def href(relative):
        return Path(os.path.relpath(base / relative, brief.parent)).as_posix()

    lines = ["# Encargo " + task_id, "", "Área: " + area,
             "Modo: " + route["modo"], "Skill directora: " + skill, "",
             "## Objetivo", "", goal.strip(), "", "## Entregable", "", deliverable.strip(),
             "", "## Criterio de aceptación", "", acceptance.strip(), "",
             "## Entrada y alcance", "", route["alcance"], ""]
    lines.extend("- " + item for item in (inputs or ["Sin entradas adicionales indicadas."]))
    if ensayo:
        lines.extend(["", "## Investigación previa al ensayo", "",
                      "- Investigación: [fuente](" + href(investigacion) + ")",
                      "- Capacidad y fuente: " + capacidad.strip(),
                      "- Hipótesis: " + hipotesis.strip(),
                      "- Control y criterio que cambia la decisión: " + control.strip(),
                      "- Lección previa: " + leccion.strip()])
    lines.extend(["", "## Contexto mínimo", "",
                  "Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.", ""])
    lines.extend("- [" + relative + "](" + href(relative) + ")" for relative in context)
    if support:
        lines.extend(["", "## Skills de apoyo disponibles", "",
                      "No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada "
                      "del encargo; no reemplazan la skill directora elegida.", ""])
        lines.extend("- [" + name + "](" + href(data["skills"][name]) + ")" for name in support)
    lines.extend(["", "## Salidas de referencia del área", ""])
    lines.extend("- " + item for item in route["salidas"])
    lines.extend(["", "## Registro", "", "Estado: [registro de trabajo](../tareas/" + task_id + ".json).",
                  "El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.",
                  "No editar la proyección ni rehashear evidencia alterada para continuar.", "", LIMITACION, ""])
    record = trabajo.create(base, task_id, goal.strip(),
                            "Leer " + brief.relative_to(base).as_posix() + " y ejecutar el encargo dentro de su alcance.",
                            shared=shared, briefing="\n".join(lines), execution=execution)
    return {"tarea": record, "briefing": brief.relative_to(base).as_posix(),
            "area": area, "skill_directora": skill, "skills_apoyo": support,
            "apoyos_seleccionados": selected_support, "modo": route["modo"], "nota": LIMITACION}


def resume(base, task_id, complete=False):
    task_paths(base, task_id)
    result = trabajo.resume(base.resolve(), task_id, complete=complete)
    brief = result["tarea"].get("briefing")
    if brief is None:
        raise ValueError("Sin briefing íntegro registrado. Para schema 1, revisar y migrar explícitamente antes de continuar.")
    # Un único contenido, en tarea.briefing.contenido; preparar conserva su ruta.
    result["nota_harness"] = LIMITACION
    return result


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=BASE)
    parser.add_argument("--operacion", type=Path, default=Path.home() / "operacion")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    p = commands.add_parser("preparar", help="Guardar un encargo sin ejecutarlo.")
    p.add_argument("id")
    p.add_argument("--area", required=True)
    p.add_argument("--skill", help="Skill directora para este encargo, entre las declaradas para el área.")
    p.add_argument("--perfil", help="Recomendación declarativa por tipo de trabajo; no cambia el modelo del runtime.")
    p.add_argument("--objetivo", required=True)
    p.add_argument("--entregable", required=True)
    p.add_argument("--aceptacion", required=True)
    p.add_argument("--entrada", action="append", default=[])
    p.add_argument("--compartible", action="store_true", help="Registro único saneado y versionable en continuidad/.")
    p.add_argument("--apoyo", action="append", default=[], help="Apoyo pertinente del área; se puede repetir.")
    p.add_argument("--ensayo", action="store_true", help="Declarar un ensayo que requiere investigación previa.")
    p.add_argument("--investigacion", help="Archivo existente relativo a la base, con investigación previa.")
    p.add_argument("--capacidad", help="Capacidad relevante y fuente en la investigación.")
    p.add_argument("--hipotesis", help="Hipótesis e incertidumbre a resolver.")
    p.add_argument("--control", help="Control y resultado que cambia la decisión.")
    p.add_argument("--leccion", help="Lección previa aplicable.")
    p = commands.add_parser("retomar")
    p.add_argument("id")
    p.add_argument("--completo", action="store_true")
    p = commands.add_parser("historial")
    p.add_argument("id")
    p.add_argument("--revision", type=int)
    p = commands.add_parser("asignar", help="Reservar rutas mediante el modelo de trabajo existente.")
    p.add_argument("id")
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--responsable", required=True)
    p.add_argument("--ruta", action="append", required=True)
    p.add_argument("--actor")
    for name in ("lanzar", "reanudar", "revisar"):
        p = commands.add_parser(name)
        p.add_argument("id")
        p.add_argument("--revision-esperada", type=int, required=True)
        p.add_argument("--actor")
        p.add_argument("--si-sergio", action="store_true")
        p.add_argument("--modelo", help="Modelo explícito para esta sesión, sin cambiar config global.")
        p.add_argument("--esfuerzo", choices=sorted(trabajo.EFFORTS))
        p.add_argument("--auth-chatgpt", action="store_true", help="Exigir login ChatGPT y quitar variables API del hijo; no mide cuota.")
        p.add_argument("--subagentes-maximos", type=int, choices=range(3), help="Hijos abiertos por ejecutora: 0 a 2; defecto 0, retoma hereda. Revisores: 0.")
        p.add_argument("--dry-run", action="store_true")
        if name == "revisar":
            p.add_argument("--revisor")
            p.add_argument("--recoger", action="store_true")
            p.add_argument("--conservar-worktree", action="store_true",
                           help="Con --recoger, conservar el checkout revisor con sus archivos locales.")
    p = commands.add_parser("estado")
    p.add_argument("--dry-run", action="store_true")
    p = commands.add_parser("cerrar")
    p.add_argument("--retorno-boss", action="store_true", help="Publicar registro y avisar al webhook privado de Boss tras cerrar; sólo IDs configurados.")
    p.add_argument("id")
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--actor", required=True)
    p.add_argument("--resultado", required=True)
    p.add_argument("--comprobacion", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--conservar-worktree", action="store_true",
                   help="Conservar el checkout y sus archivos locales. Exige HEAD y archivos versionados al día.")
    p = commands.add_parser("aceptar")
    p.add_argument("id")
    p.add_argument("--revision-esperada", type=int, required=True)
    p.add_argument("--revisor", required=True)
    p.add_argument("--criterio", required=True)
    p = commands.add_parser("skills", help="Crear enlaces faltantes de skills propias sin reemplazar existentes.")
    p.add_argument("--dry-run", action="store_true")
    p = commands.add_parser("notificar-boss", help="Publicar registro cerrado y enviar su aviso deduplicado a Boss.")
    p.add_argument("id")
    p = commands.add_parser("notificar-fin-boss", help="Publicar aviso de un intento terminado o recuperar pendiente; nunca reenvía inciertos.")
    p.add_argument("id")
    p.add_argument("--intento", type=int, required=True)
    p = commands.add_parser("_ejecutar", help=argparse.SUPPRESS)
    p.add_argument("id")
    p.add_argument("--intento", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command in {"lanzar", "reanudar", "revisar", "estado", "cerrar", "skills", "_ejecutar"}:
            import harness_sesiones as sessions
            if args.command == "_ejecutar":
                return sessions.worker(args.base, args.id, args.operacion, args.intento)
            if args.command == "estado":
                result = sessions.status(args.base, args.operacion, args.dry_run)
            elif args.command == "skills":
                result = sessions.link_skills(sessions.repo_for(args.base), args.base, args.dry_run)
            elif args.command == "cerrar":
                if args.dry_run and args.retorno_boss:
                    raise ValueError("Una simulación no publica ni notifica a Boss.")
                result = sessions.close(args.base, args.id, args.operacion, args.revision_esperada,
                                        args.actor, args.resultado, args.comprobacion, args.dry_run,
                                        retain_worktree=args.conservar_worktree)
                if args.retorno_boss:
                    import harness_retorno
                    result['retorno_boss'] = harness_retorno.configured(args.base, args.operacion, args.id,
                                                                      expected_revision=result['tarea']['revision'])
            elif args.command == "revisar" and args.recoger:
                if args.dry_run:
                    raise ValueError("Una simulación no produce un veredicto real.")
                result = sessions.collect_review(args.base, args.id, args.operacion, args.revision_esperada,
                                                 retain_worktree=args.conservar_worktree)
            else:
                if args.command == "revisar" and args.conservar_worktree:
                    raise ValueError("--conservar-worktree requiere --recoger al revisar.")
                if args.command == "revisar" and not args.revisor:
                    raise ValueError("Revisar requiere --revisor distinto del ejecutor.")
                result = sessions.launch(args.base, args.id, args.operacion, args.revision_esperada,
                    args.actor, approved=args.si_sergio, dry_run=args.dry_run,
                    resume=args.command == "reanudar", reviewer=getattr(args, "revisor", None),
                    model=args.modelo, effort=args.esfuerzo, auth_chatgpt=args.auth_chatgpt,
                    subagents=args.subagentes_maximos)
            code = 0
        elif args.command == "notificar-boss":
            import harness_retorno
            result, code = harness_retorno.configured(args.base, args.operacion, args.id), 0
        elif args.command == "notificar-fin-boss":
            import harness_retorno
            result, code = harness_retorno.session_finished(args.base.resolve(), args.operacion,
                                                           args.id, args.intento, retry_pending=True), 0
        elif args.command == "asignar":
            result = trabajo.assign(args.base.resolve(), args.id, args.revision_esperada,
                                    args.responsable, args.ruta, actor=args.actor)
            code = 0
        elif args.command == "aceptar":
            result = trabajo.accept(args.base.resolve(), args.id, args.revision_esperada,
                                    args.revisor, args.criterio)
            code = 0
        elif args.command == "doctor":
            result = doctor(args.base)
            code = 0 if result["ok"] else 1
        elif args.command == "preparar":
            result = prepare(args.base, args.id, args.area, args.objetivo,
                             args.entregable, args.aceptacion, args.entrada, skill=args.skill,
                             ensayo=args.ensayo, investigacion=args.investigacion,
                             capacidad=args.capacidad, hipotesis=args.hipotesis,
                             control=args.control, leccion=args.leccion, apoyos=args.apoyo, shared=args.compartible,
                             profile=args.perfil)
            code = 0
        elif args.command == "historial":
            result, code = trabajo.history(args.base.resolve(), args.id, args.revision), 0
        else:
            result, code = resume(args.base, args.id, complete=args.completo), 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result, code = {"error": str(exc)}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())

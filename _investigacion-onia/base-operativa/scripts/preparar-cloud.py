"""Enlaza las skills canónicas del repositorio; no descarga ni instala paquetes."""
import argparse
import json
import os
from pathlib import Path
import sys

SOURCE = Path("_investigacion-onia/base-operativa/compartibles/skills")
DESTINATION = Path(".agents/skills")


def repository_root(script=Path(__file__)):
    """La ubicación del script define la raíz; no depende del cwd ni de Git."""
    script = script.resolve()
    root = script.parents[3]
    if script.parent != root / "_investigacion-onia/base-operativa/scripts":
        raise ValueError("El script debe conservar su ubicación dentro del repositorio.")
    return root


def present(path):
    # exists() por sí solo no detecta un enlace roto que tampoco se debe pisar.
    return os.path.lexists(path)


def inspect(root):
    root = root.resolve()
    source = root / SOURCE
    if not source.is_dir() or not source.resolve().is_relative_to(root):
        raise ValueError("La fuente canónica no existe dentro del repositorio.")
    for parent in (root / ".agents", root / DESTINATION):
        if present(parent) and (not parent.is_dir() or parent.resolve() != parent):
            raise ValueError(f"Destino padre ajeno o no regular: {parent}")
    entries = []
    for skill in sorted(source.iterdir()):
        if skill.name.startswith("."):
            continue
        if not skill.is_dir() or not (skill / "SKILL.md").is_file():
            raise ValueError(f"Entrada de skill inválida: {skill.name}")
        if not skill.resolve().is_relative_to(source.resolve()):
            raise ValueError(f"Skill fuera de la fuente canónica: {skill.name}")
        if not (skill / "SKILL.md").resolve().is_relative_to(source.resolve()):
            raise ValueError(f"SKILL.md fuera de la fuente canónica: {skill.name}")
        destination = root / DESTINATION / skill.name
        if not present(destination):
            state = "missing"
        elif destination.is_dir() and destination.resolve() == skill.resolve():
            state = "ready"
        else:
            state = "conflict"
        entries.append({"name": skill.name, "state": state,
                        "source": skill.relative_to(root).as_posix(),
                        "destination": destination.relative_to(root).as_posix()})
    if not entries:
        raise ValueError("La fuente canónica no contiene skills.")
    return entries


def prepare(root, install=False):
    root = root.resolve()
    entries = inspect(root)
    result = {"mode": "install" if install else "check", "root": str(root),
              "skills": entries, "created": [], "errors": [],
              "note": "El descubrimiento debe comprobarse en una nueva sesión; no hay recarga automática garantizada."}
    if any(entry["state"] == "conflict" for entry in entries):
        result["errors"].append("Hay destinos ajenos. No se creó ni reemplazó ningún enlace.")
        return result, 2
    if install:
        destination_root = root / DESTINATION
        try:
            destination_root.mkdir(parents=True, exist_ok=True)
            for entry in entries:
                if entry["state"] == "ready":
                    continue
                source = root / entry["source"]
                destination = root / entry["destination"]
                # El enlace relativo sigue funcionando al mover el checkout.
                target = os.path.relpath(source, destination.parent)
                os.symlink(target, destination, target_is_directory=True)
                result["created"].append(entry["destination"])
            result["skills"] = inspect(root)
        except OSError as exc:
            # No borrar destinos ni hacer fallback a copias o enlaces distintos.
            result["errors"].append(f"No se pudo crear el enlace: {exc}")
            return result, 2
    ready = all(entry["state"] == "ready" for entry in result["skills"])
    return result, 0 if ready else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Sólo leer; salida 1 si faltan enlaces.")
    mode.add_argument("--install", action="store_true", help="Crear únicamente enlaces faltantes, sin sobrescribir.")
    args = parser.parse_args(argv)
    try:
        result, code = prepare(repository_root(), install=args.install)
    except (OSError, ValueError) as exc:
        result, code = {"errors": [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())

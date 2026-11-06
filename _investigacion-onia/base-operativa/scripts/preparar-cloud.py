"""Enlaza las skills canónicas del repositorio; no descarga ni instala paquetes."""
import argparse
import base64
import json
import os
from pathlib import Path
import sys
import subprocess

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


def discovery_parent(root, requested):
    """El alias opcional sólo pertenece al workspace que contiene este checkout."""
    if requested is None:
        return None
    requested = Path(requested)
    if not requested.is_absolute():
        raise ValueError("La raíz de descubrimiento debe ser absoluta.")
    resolved = requested.resolve()
    if requested != resolved or resolved != root.resolve().parent or resolved == resolved.parent:
        raise ValueError("La raíz de descubrimiento debe ser el padre directo real del checkout, sin enlaces.")
    return resolved


def inspect(root, destination_root=None):
    root = root.resolve()
    destination_root = root if destination_root is None else discovery_parent(root, destination_root)
    source = root / SOURCE
    if not source.is_dir() or not source.resolve().is_relative_to(root):
        raise ValueError("La fuente canónica no existe dentro del repositorio.")
    for parent in (destination_root / ".agents", destination_root / DESTINATION):
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
        destination = destination_root / DESTINATION / skill.name
        if not present(destination):
            state = "missing"
        elif destination.is_dir() and destination.resolve() == skill.resolve():
            state = "ready"
        else:
            state = "conflict"
        entries.append({"name": skill.name, "state": state,
                        "source": skill.relative_to(root).as_posix(),
                        "destination": Path(os.path.relpath(destination, root)).as_posix()})
    if not entries:
        raise ValueError("La fuente canónica no contiene skills.")
    return entries


def create_junction(source, destination):
    """Alternativa explícita Windows, sin privilegio de symlink ni copia de la skill."""
    if os.name != "nt":
        raise ValueError("Las junctions sólo están disponibles en Windows.")
    quote = lambda value: "'" + str(value).replace("'", "''") + "'"
    command = ("$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path " + quote(destination)
               + " -Target " + quote(source) + " | Out-Null")
    encoded = base64.b64encode(command.encode("utf-16-le")).decode("ascii")
    subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                   check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)


def prepare(root, install=False, discovery_root=None, windows_junctions=False):
    root = root.resolve()
    discovery_root = discovery_parent(root, discovery_root)
    if windows_junctions and (not install or os.name != "nt"):
        raise ValueError("--junctions-windows requiere --install en Windows.")
    entries = inspect(root)
    discovery_entries = inspect(root, discovery_root) if discovery_root is not None else []
    result = {"mode": "install" if install else "check", "root": str(root),
              "skills": entries, "created": [], "errors": [],
              "discovery_root": str(discovery_root) if discovery_root is not None else None,
              "discovery_skills": discovery_entries,
              "note": "El descubrimiento debe comprobarse en una nueva sesión; no hay recarga automática garantizada."}
    all_entries = entries + discovery_entries
    # Comprobar ambos destinos antes de escribir: un conflicto del workspace
    # tampoco debe instalar parcialmente los enlaces del repositorio.
    if any(entry["state"] == "conflict" for entry in all_entries):
        result["errors"].append("Hay destinos ajenos. No se creó ni reemplazó ningún enlace.")
        return result, 2
    if install:
        try:
            for entry in all_entries:
                if entry["state"] == "ready":
                    continue
                source = root / entry["source"]
                destination = root / entry["destination"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                # El enlace relativo sigue funcionando al mover el checkout.
                target = os.path.relpath(source, destination.parent)
                if windows_junctions:
                    create_junction(source, destination)
                else:
                    os.symlink(target, destination, target_is_directory=True)
                result["created"].append(entry["destination"])
            result["skills"] = inspect(root)
            if discovery_root is not None:
                result["discovery_skills"] = inspect(root, discovery_root)
        except (OSError, subprocess.CalledProcessError) as exc:
            # No borrar destinos ni hacer fallback a copias o enlaces distintos.
            result["errors"].append(f"No se pudo crear el enlace: {exc}")
            return result, 2
    ready = all(entry["state"] == "ready" for entry in result["skills"] + result["discovery_skills"])
    return result, 0 if ready else 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Sólo leer; salida 1 si faltan enlaces.")
    mode.add_argument("--install", action="store_true", help="Crear únicamente enlaces faltantes, sin sobrescribir.")
    parser.add_argument("--discovery-root", type=Path,
                        help="Raíz absoluta opcional del workspace padre; crea también aliases allí.")
    parser.add_argument("--junctions-windows", action="store_true",
                        help="Usar junctions explícitas si Windows no permite symlinks. Destino absoluto; no portable al mover checkout.")
    args = parser.parse_args(argv)
    try:
        result, code = prepare(repository_root(), install=args.install, discovery_root=args.discovery_root,
                               windows_junctions=args.junctions_windows)
    except (OSError, ValueError) as exc:
        result, code = {"errors": [str(exc)]}, 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())

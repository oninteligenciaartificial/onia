"""Una pasada de la cola existente; sin SSH salvo habilitación explícita."""
import argparse
import json
import os
from pathlib import Path
import sys

# En origen usa los módulos canónicos; el paquete los lleva junto a este archivo.
module_dir = Path(__file__).resolve().parent
if not (module_dir / "cola_homelab.py").is_file():
    module_dir = module_dir.parent
sys.path.insert(0, str(module_dir))
import cola_homelab as cola


def run(root, stop, *, ssh=False, transport=None):
    # lexists incluye un enlace roto: cualquier entrada con este nombre detiene.
    if os.path.lexists(stop):
        return {"estado": "detenido"}
    os.umask(0o077)

    def dispatch(job):
        # Comprobar otra vez después de adquirir el lock de la cola.
        if os.path.lexists(stop):
            raise cola.RetryLater("parada_solicitada")
        if transport is not None:
            return transport(job)
        if not ssh:
            raise cola.RetryLater("ssh_deshabilitado")
        return cola.remote(job)

    return cola.Queue(root).tick(dispatch)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, required=True)
    cli.add_argument("--stop", type=Path, required=True)
    cli.add_argument("--sin-ssh", action="store_true")
    args = cli.parse_args()
    try:
        setting = os.environ.get("ONIA_HOMELAB_SSH", "0")
        if setting not in {"0", "1"}:
            raise ValueError("ONIA_HOMELAB_SSH debe ser 0 o 1")
        result = run(args.root, args.stop, ssh=setting == "1" and not args.sin_ssh)
        # No volcar medios, rutas privadas ni respuestas del transporte al journal.
        result = {key: result[key] for key in
                  ("estado", "intentos", "sha256", "bytes", "reutilizado", "motivo", "proximo_intento")
                  if key in result}
    except (ValueError, OSError, KeyError, TypeError) as exc:
        result = {"estado": "fallo_local", "motivo": type(exc).__name__}
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 1 if result["estado"] in {"bloqueado", "fallo_local"} else 0


if __name__ == "__main__":
    raise SystemExit(main())

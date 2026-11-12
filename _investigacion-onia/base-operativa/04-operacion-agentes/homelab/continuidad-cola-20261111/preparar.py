"""Construye un paquete nuevo; no instala ni activa servicios."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent


def prepare(dest):
    os.umask(0o077)
    dest.mkdir(mode=0o700)  # No sobrescribir instalaciones o paquetes existentes.
    (dest / "app").mkdir(mode=0o700)
    (dest / "systemd").mkdir(mode=0o700)
    sources = {
        "app/pasada.py": HERE / "pasada.py",
        "app/cola_homelab.py": HERE.parent / "cola_homelab.py",
        "app/worker_render.py": HERE.parent / "worker_render.py",
        **{"systemd/" + name: HERE / "systemd" / name for name in
           ("onia-homelab-cpu.service", "onia-homelab-cpu.timer")},
    }
    hashes = {}
    for name, source in sources.items():
        target = dest / name
        shutil.copyfile(source, target)
        target.chmod(0o600)
        hashes[name] = hashlib.sha256(target.read_bytes()).hexdigest()
    (dest / "STOP").touch(mode=0o600)
    (dest / "config.env").write_text("ONIA_HOMELAB_SSH=0\n")
    for name in ("STOP", "config.env"):
        hashes[name] = hashlib.sha256((dest / name).read_bytes()).hexdigest()
    (dest / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(hashes.items())))
    return hashes


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--dest", type=Path, required=True)
    args = cli.parse_args()
    print(json.dumps(prepare(args.dest), sort_keys=True))

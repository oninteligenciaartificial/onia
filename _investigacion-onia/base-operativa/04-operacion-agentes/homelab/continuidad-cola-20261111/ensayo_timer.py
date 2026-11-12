"""Ensayo transitorio local: render sintético y segunda pasada vacía; nunca SSH."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

HERE = Path(__file__).resolve().parent


def command(args, *, check=True):
    return subprocess.run(args, capture_output=True, text=True, timeout=10, check=check)


def child(base):
    sys.path.insert(0, str(base / "paquete/app"))
    import pasada
    import worker_render as worker

    def forbidden(*args, **kwargs):
        raise AssertionError("SSH prohibido en este fixture")

    pasada.cola.remote = forbidden
    pasada.cola.ssh_command = forbidden
    result = pasada.run(base / "cola", base / "STOP",
                        transport=lambda job: worker.execute(job, base / "worker"))
    event = {key: result[key] for key in
             ("estado", "intentos", "sha256", "bytes", "reutilizado") if key in result}
    event["instante_ns"] = time.time_ns()
    pasada.cola.save(base / "eventos" / f"{time.time_ns()}.json", event)
    if result["estado"] == "sin_trabajo":
        (base / "STOP").touch(mode=0o600)
    return event


def exercise(base):
    sys.path.insert(0, str(HERE))
    import pasada
    import preparar

    base = base.resolve()
    os.umask(0o077)
    # Raíz nueva y exclusiva: no se acepta una cola existente.
    base.mkdir(mode=0o700)
    for name in ("worker", "eventos"):
        (base / name).mkdir(mode=0o700)
    preparar.prepare(base / "paquete")
    pasada.cola.Queue(base / "cola").enqueue("fixture-timer")
    unit = "onia-homelab-fixture-" + uuid.uuid4().hex[:12]
    properties = ["Type=oneshot", "TimeoutStartSec=80s", "TimeoutStopSec=10s",
                  "KillMode=control-group", "Restart=no", "UMask=0077", "Nice=10",
                  "CPUQuota=25%", "MemoryMax=256M", "TasksMax=16", "NoNewPrivileges=yes",
                  "RestrictSUIDSGID=yes", "LockPersonality=yes"]
    argv = ["systemd-run", "--user", "--collect", "--unit=" + unit,
            "--on-active=1s", "--on-unit-inactive=2s", "--timer-property=AccuracySec=100ms"]
    for prop in properties:
        argv.append("--property=" + prop)
    argv += [sys.executable, "-I", "-B", str(HERE / "ensayo_timer.py"), "--child", str(base)]
    started = False
    try:
        command(argv)
        started = True
        deadline = time.monotonic() + 35
        while time.monotonic() < deadline:
            events = [json.loads(path.read_text()) for path in sorted((base / "eventos").glob("*.json"))]
            if len(events) >= 2:
                break
            time.sleep(0.2)
        else:
            raise TimeoutError("El timer no produjo dos recibos en 35 s")
        assert [event["estado"] for event in events] == ["entregado", "sin_trabajo"], events
        local = base / "cola/fixture-timer.mp4"
        remote = base / "worker/cola-cpu-v1/fixture-timer/muestra.mp4"
        checksum = hashlib.sha256(local.read_bytes()).hexdigest()
        assert checksum == events[0]["sha256"] == hashlib.sha256(remote.read_bytes()).hexdigest()
        assert len(list(remote.parent.glob("intento-*"))) == 1
        assert (base / "STOP").exists()
        stopped = pasada.run(base / "cola", base / "STOP", ssh=True)
        assert stopped == {"estado": "detenido"}
        receipt = {"estado": "probado", "programador": "systemd-usuario-transitorio",
                   "transporte": "worker-local-sin-ssh", "unidad": unit, "eventos": events,
                   "sha256": checksum, "un_render": True, "parada": stopped,
                   "intervalo_ensayo_s": 2, "intervalo_entrega_s": 60}
    finally:
        if started:
            # Únicamente las dos unidades efímeras de este ensayo.
            command(["systemctl", "--user", "stop", unit + ".timer"], check=False)
            command(["systemctl", "--user", "stop", unit + ".service"], check=False)
            states = {}
            for suffix in (".timer", ".service"):
                state = command(["systemctl", "--user", "show", unit + suffix,
                                 "--property=ActiveState", "--value"], check=False).stdout.strip()
                if state not in {"inactive", "failed", ""}:
                    raise RuntimeError("Unidad de ensayo todavía activa: " + suffix)
                states[suffix] = state
    receipt["unidades_al_final"] = states
    return receipt


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dest", type=Path)
    mode.add_argument("--child", type=Path)
    args = cli.parse_args()
    print(json.dumps(child(args.child) if args.child else exercise(args.dest), indent=2))

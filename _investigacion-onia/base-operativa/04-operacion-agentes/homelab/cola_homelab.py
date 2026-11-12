"""Encola un trabajo CPU y ejecuta, como máximo, un intento por pasada."""
import argparse
import base64
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import time

from worker_render import JOB_ID, MAX_VIDEO, private_directory

RUNTIME = Path.home() / "operacion/homelab"
HOST_KEY = "SHA256:4ClsP1NH8JWxBWUNjW2DP7Egn4UcHcqMUYBUu3sL1Gk"


class RetryLater(Exception):
    pass


def atomic_write(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".parcial-", delete=False) as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(stream.name, path)
    fd = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def save(path, record):
    atomic_write(path, (json.dumps(record, ensure_ascii=False) + "\n").encode())


def ssh_command():
    known_hosts = RUNTIME / "ssh/known_hosts-worker-2224"
    key = known_hosts.read_text().strip().split()
    if len(key) != 3 or key[:2] != ["onia-homelab-worker-2224", "ssh-ed25519"]:
        raise ValueError("Known_hosts inesperado")
    fingerprint = base64.b64encode(hashlib.sha256(base64.b64decode(key[2], validate=True)).digest())
    if "SHA256:" + fingerprint.decode().rstrip("=") != HOST_KEY:
        raise ValueError("Huella remota distinta")
    proxy = shlex.join([str(RUNTIME / "tailscale/bin/tailscale"), "--socket",
                        str(RUNTIME / "tailscale/tailscaled.sock"), "nc", "desktop-0gggnmf", "2224"])
    return [
        "ssh", "-F", "/dev/null", "-T", "-p", "2224", "-i", str(RUNTIME / "ssh/id_ed25519"),
        "-o", "IdentitiesOnly=yes", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=yes",
        "-o", "HostKeyAlias=onia-homelab-worker-2224", "-o", "UserKnownHostsFile=" + str(known_hosts),
        "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=5", "-o", "ServerAliveCountMax=2",
        "-o", "ProxyCommand=" + proxy, "onia-worker@desktop-0gggnmf", "python3 -I -B -",
    ]


def remote(job):
    source = Path(__file__).with_name("worker_render.py").read_text()
    request = json.dumps(job)
    program = f"{source}\nprint(json.dumps(execute(json.loads({request!r}), Path.home())))\n"
    try:
        process = subprocess.run(ssh_command(), input=program, text=True, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired as exc:
        raise RetryLater("sin_respuesta") from exc
    if process.returncode == 255:
        raise RetryLater("conexion_no_disponible")
    if process.returncode != 0:
        raise ValueError("Worker falló: código " + str(process.returncode))
    if len(process.stdout) > 2 * MAX_VIDEO:
        raise ValueError("Respuesta remota demasiado grande")
    return json.loads(process.stdout)


class Queue:
    def __init__(self, root):
        self.root = private_directory(root)

    def enqueue(self, job_id):
        if not JOB_ID.fullmatch(job_id):
            raise ValueError("ID inválido")
        with (self.root / "cola.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            path = self.root / (job_id + ".json")
            if path.exists():
                return json.loads(path.read_text())
            record = {"job": {"id": job_id, "tipo": "render-sintetico-v1"},
                      "creado": datetime.now(timezone.utc).isoformat(),
                      "estado": "pendiente", "intentos": 0}
            save(path, record)
            return record

    def tick(self, transport=remote):
        with (self.root / "cola.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return {"estado": "ocupado"}
            now = time.time()
            records = ((json.loads(path.read_text()), path) for path in self.root.glob("*.json"))
            ready = [(record, path) for record, path in records
                     if record["estado"] in {"pendiente", "en_curso", "reintento"}
                     and record.get("proximo_intento", 0) <= now]
            if not ready:
                return {"estado": "sin_trabajo"}
            record, path = min(ready, key=lambda item: item[0]["creado"])
            record.update(estado="en_curso", intentos=record["intentos"] + 1)
            save(path, record)
            try:
                result = transport(record["job"])
                if result == {"estado": "ocupado"}:
                    raise RetryLater("worker_ocupado")
                self.deliver(record, result)
            except RetryLater as exc:
                delay = min(300, 2 ** min(9, record["intentos"]))
                record.update(estado="reintento", motivo=str(exc), proximo_intento=time.time() + delay)
            except (ValueError, OSError, KeyError, TypeError) as exc:
                record.update(estado="bloqueado", motivo=type(exc).__name__)
            save(path, record)
            return record

    def deliver(self, record, result):
        job_id = record["job"]["id"]
        if result["estado"] != "resultado" or result["id"] != job_id or type(result["reutilizado"]) is not bool:
            raise ValueError("Resultado no corresponde al encargo")
        encoded = result["video"]
        if not isinstance(encoded, str) or len(encoded) > 2 * MAX_VIDEO:
            raise ValueError("Respuesta fuera de límite")
        video = base64.b64decode(encoded, validate=True)
        checksum = hashlib.sha256(video).hexdigest()
        if not 0 < len(video) <= MAX_VIDEO or result["sha256"] != checksum:
            raise ValueError("Resultado corrupto")
        output = self.root / (job_id + ".mp4")
        if output.exists():
            if output.read_bytes() != video:
                raise ValueError("La copia local existente difiere")
        else:
            atomic_write(output, video)
        record.pop("motivo", None)
        record.pop("proximo_intento", None)
        record.update(estado="entregado", sha256=checksum, bytes=len(video),
                      reutilizado=result["reutilizado"])


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--root", type=Path, default=RUNTIME / "cola-cpu-v1")
    commands = cli.add_subparsers(dest="action", required=True)
    commands.add_parser("encolar").add_argument("id")
    commands.add_parser("tick")
    args = cli.parse_args()
    queue = Queue(args.root)
    result = queue.enqueue(args.id) if args.action == "encolar" else queue.tick()
    print(json.dumps(result, ensure_ascii=False))
    return 1 if result["estado"] == "bloqueado" else 0


if __name__ == "__main__":
    raise SystemExit(main())

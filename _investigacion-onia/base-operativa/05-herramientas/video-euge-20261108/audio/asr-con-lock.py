#!/usr/bin/env python3
"""Ejecuta una inferencia local bajo un lock compartido entre namespaces."""

import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import stat
import subprocess
import time

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("lock", type=Path)
parser.add_argument("events", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("source_sha256")
parser.add_argument("command", nargs=argparse.REMAINDER)
args = parser.parse_args()
if not args.command or args.output.exists():
    parser.error("Se necesita un comando y un destino de ASR nuevo.")

os.umask(0o077)
parent = args.lock.parent.stat()
if (
    parent.st_uid != os.getuid()
    or stat.S_IMODE(parent.st_mode) != 0o700
    or args.lock.parent.resolve() != args.lock.parent.absolute()
):
    parser.error("El lock debe estar en un directorio propio 0700 sin symlinks.")
fd = os.open(args.lock, os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW, 0o600)
with os.fdopen(fd, "a") as lock:
    lock_stat = os.fstat(lock.fileno())
    if (
        lock_stat.st_uid != os.getuid()
        or not stat.S_ISREG(lock_stat.st_mode)
        or stat.S_IMODE(lock_stat.st_mode) != 0o600
        or lock_stat.st_nlink != 1
    ):
        parser.error("El lock debe ser un archivo propio 0600 con un enlace.")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(75)
    if args.output.exists():
        parser.error("El destino de ASR ya existe.")
    boot_id = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
    with args.events.open("x", encoding="utf-8") as events:
        identity = {"boot_id": boot_id, "source_sha256": args.source_sha256}

        def record(state, **extra):
            row = {
                **identity, **extra, "state": state,
                "utc": datetime.now(timezone.utc).isoformat(),
                "monotonic_s": round(time.monotonic(), 3),
            }
            events.write(json.dumps(row, ensure_ascii=False) + "\n")
            events.flush()

        record("launching")
        # Inherit the lock so the inference holds it even if this wrapper exits.
        child = subprocess.Popen(args.command, pass_fds=(lock.fileno(),))
        identity["pid_in_namespace"] = child.pid
        try:
            fields = Path(f"/proc/{child.pid}/stat").read_text().rsplit(")", 1)[1].split()
            identity["start_ticks"] = int(fields[19])
        except (OSError, ValueError, IndexError):
            identity["start_ticks"] = None
        try:
            identity["pid_namespace"] = os.readlink(f"/proc/{child.pid}/ns/pid")
        except OSError:
            identity["pid_namespace"] = None
        record("running")
        while True:
            try:
                child_rc = child.wait(timeout=15)
                break
            except subprocess.TimeoutExpired:
                record("heartbeat")
                print("ASR local activo " + datetime.now(timezone.utc).isoformat(), flush=True)

        try:
            result = json.loads(args.output.read_text())
            segments = result["segments"]
            valid = (
                result["source_sha256"] == args.source_sha256
                and isinstance(segments, list)
                and result["segment_count"] == len(segments)
            )
        except (OSError, ValueError, TypeError, KeyError):
            valid = False
        record("output_valid" if valid else "output_invalid", child_rc=child_rc)
        raise SystemExit(0 if valid else 1)

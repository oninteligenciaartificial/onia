"""Trabajo de CPU acotado que el VPS envía por el SSH privado existente."""
import base64
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

JOB_ID = re.compile(r"[a-z0-9][a-z0-9-]{0,63}")
MAX_VIDEO = 1024 * 1024


def private_directory(path):
    path.mkdir(mode=0o700, exist_ok=True)
    info = path.stat()
    if path.is_symlink() or not path.is_dir() or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise ValueError("Directorio operativo no privado")
    return path


def render(source, target, lock):
    subprocess.run(
        ["ffmpeg", "-nostdin", "-n", "-v", "error", "-f", "lavfi", "-i", source,
         "-t", "2", "-c:v", "libx264", "-threads", "2", "-pix_fmt", "yuv420p", str(target)],
        check=True, timeout=30, stdin=subprocess.DEVNULL, pass_fds=(lock.fileno(),),
    )


def probe(path):
    raw = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,width,height,nb_frames:format=duration", "-of", "json", str(path)],
        timeout=10, stdin=subprocess.DEVNULL,
    )
    data = json.loads(raw)
    expected = {"codec_name": "h264", "width": 640, "height": 360, "nb_frames": "48"}
    if data["streams"] != [expected] or abs(float(data["format"]["duration"]) - 2) >= 0.1:
        raise ValueError("Video remoto inválido")


def execute(job, home):
    if set(job) != {"id", "tipo"} or not JOB_ID.fullmatch(job["id"]) or job["tipo"] != "render-sintetico-v1":
        raise ValueError("Encargo no admitido")
    spool = private_directory(home / "cola-cpu-v1")
    with (spool / "worker.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return {"estado": "ocupado"}
        work = private_directory(spool / job["id"])
        output = work / "muestra.mp4"
        cached = output.exists()
        if not cached:
            stage = Path(tempfile.mkdtemp(prefix="intento-", dir=work)) / "muestra.mp4"
            render("testsrc2=size=640x360:rate=24", stage, lock)
            probe(stage)
            with stage.open("rb") as stream:
                os.fsync(stream.fileno())
            # El enlace publica la muestra completa y falla si el destino ya existe.
            os.link(stage, output)
            fd = os.open(work, os.O_DIRECTORY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        else:
            probe(output)
        with output.open("rb") as stream:
            video = stream.read(MAX_VIDEO + 1)
        if not 0 < len(video) <= MAX_VIDEO:
            raise ValueError("Tamaño del video remoto inválido")
        return {"estado": "resultado", "id": job["id"], "reutilizado": cached,
                "sha256": hashlib.sha256(video).hexdigest(), "video": base64.b64encode(video).decode()}

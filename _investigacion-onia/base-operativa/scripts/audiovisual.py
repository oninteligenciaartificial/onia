"""Ingesta instrumental local. No descarga, decodifica completo ni percibe audio/video."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

import trabajo

MAX_BYTES = 256 * 1024 * 1024
ATTRIBUTES = ("guion", "imagen", "edicion_temporal", "tipografia", "voz",
              "prosodia", "musica", "efectos", "sincronia", "afirmaciones")


def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def public_identity(url):
    parsed = urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc not in {"www.instagram.com", "instagram.com"}
            or parsed.query or parsed.fragment):
        raise ValueError("Usar URL pública Instagram HTTPS sin credenciales, query ni fragmento.")
    match = re.fullmatch(r"/reel/([A-Za-z0-9_-]{1,64})/?", parsed.path)
    if not match:
        raise ValueError("Se requiere identidad pública /reel/ID/.")
    return {"plataforma": "instagram", "id": match[1],
            "url": "https://www.instagram.com/reel/" + match[1] + "/",
            "asociacion": "declarada_por_operador_no_verificada_en_red"}


def plain_directory(root):
    root = Path(os.path.abspath(root))
    for part in [root, *root.parents]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("La raíz contiene enlaces o reparse points.")
    if not root.is_dir():
        raise ValueError("Raíz de medios inexistente.")
    return root


def finite_number(value, label, *, positive=False):
    if isinstance(value, bool):
        raise ValueError("Número inválido: " + label)
    try:
        number = float(value)
    except (ValueError, TypeError):
        raise ValueError("Número inválido: " + label) from None
    if not math.isfinite(number) or (positive and number <= 0):
        raise ValueError("Número inválido: " + label)
    return number


def optional_number(value, label):
    return None if value in (None, "N/A") else finite_number(value, label)


def integer(value, label):
    if isinstance(value, bool) or not re.fullmatch(r"[0-9]+", str(value)):
        raise ValueError("Entero inválido: " + label)
    return int(value)


def sanitize_probe(raw, size):
    streams = raw.get("streams")
    if not isinstance(streams, list) or not 1 <= len(streams) <= 32:
        raise ValueError("Número de pistas inválido.")
    form = raw.get("format", {})
    if not isinstance(form, dict):
        raise ValueError("Formato ffprobe inválido.")
    duration = finite_number(form.get("duration"), "duración", positive=True)
    if integer(form.get("size"), "bytes") != size:
        raise ValueError("Tamaño de ffprobe distinto del original.")
    clean = []
    indexes = set()
    for stream in streams:
        if not isinstance(stream, dict):
            raise ValueError("Pista ffprobe inválida.")
        kind = stream.get("codec_type")
        if kind not in {"audio", "video"}:
            continue
        index = integer(stream.get("index"), "índice")
        codec = stream.get("codec_name")
        if index in indexes or not isinstance(codec, str) or not re.fullmatch(r"[a-z0-9_]{1,40}", codec):
            raise ValueError("Identidad de pista inválida.")
        indexes.add(index)
        entry = {"indice": index, "tipo": kind, "codec": codec,
                 "inicio_s": optional_number(stream.get("start_time"), "inicio de pista"),
                 "duracion_s": optional_number(stream.get("duration"), "duración de pista")}
        if entry["duracion_s"] is not None and entry["duracion_s"] < 0:
            raise ValueError("Duración de pista negativa.")
        for source, dest in (("width", "ancho"), ("height", "alto"),
                             ("sample_rate", "frecuencia_hz"), ("channels", "canales")):
            if source in stream:
                entry[dest] = integer(stream[source], source)
                if entry[dest] <= 0:
                    raise ValueError("Dimensión/frecuencia/canales no positivos.")
        for source in ("r_frame_rate", "avg_frame_rate"):
            value = stream.get(source)
            if kind == "video" and value is not None:
                if not isinstance(value, str) or not re.fullmatch(r"[0-9]+/[0-9]+", value):
                    raise ValueError("Fracción FPS inválida.")
                entry[source] = value
        clean.append(entry)
    if not any(s["tipo"] == "video" for s in clean):
        raise ValueError("El medio no contiene pista de video.")
    return {"duracion_contenedor_s": duration,
            "inicio_contenedor_s": optional_number(form.get("start_time"), "inicio"),
            "pistas": clean, "audio_presente": any(s["tipo"] == "audio" for s in clean),
            "pts_decodificados": False, "decodificacion_completa": False}


def ingest(root, relative, url, ffprobe="ffprobe", timeout=20):
    identity = public_identity(url)
    root = plain_directory(root)
    path = trabajo.safe_path(root, relative)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= MAX_BYTES:
        raise ValueError("Medio regular vacío o fuera del límite de 256 MiB.")
    suffix = path.suffix.lower()
    if suffix not in {".mp4", ".mov", ".webm"}:
        raise ValueError("Formatos permitidos: mp4, mov, webm.")
    timeout = finite_number(timeout, "timeout", positive=True)
    if timeout > 60:
        raise ValueError("Timeout máximo: 60 segundos.")
    before = hash_file(path)
    entries = ("stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,"
               "sample_rate,channels,duration,start_time:format=duration,start_time,size")
    args = [str(ffprobe), "-v", "error", "-max_alloc", "16777216", "-protocol_whitelist", "file",
            "-f", "matroska" if suffix == ".webm" else "mov", "-show_entries", entries,
            "-of", "json", str(path)]
    try:
        result = subprocess.run(args, stdin=subprocess.DEVNULL, capture_output=True,
                                timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise ValueError("ffprobe excedió el límite; no hay recibo de éxito.") from None
    except OSError:
        raise ValueError("ffprobe no disponible o no ejecutable.") from None
    if result.returncode != 0 or len(result.stdout) > 1024 * 1024:
        raise ValueError("ffprobe falló o produjo salida fuera del límite; stderr no se publica.")
    try:
        raw = json.loads(result.stdout)
        if not isinstance(raw, dict):
            raise ValueError()
    except (ValueError, UnicodeDecodeError):
        raise ValueError("Respuesta ffprobe inválida.") from None
    probe = sanitize_probe(raw, info.st_size)
    current = trabajo.safe_path(root, relative)
    after_info = current.stat()
    if (not stat.S_ISREG(after_info.st_mode) or after_info.st_size != info.st_size
            or after_info.st_mtime_ns != info.st_mtime_ns or hash_file(current) != before):
        raise ValueError("El medio cambió durante la ingesta; recibo rechazado.")
    return {"schema": 1, "tipo": "ingesta_instrumental", "fecha_utc": trabajo.now(),
            "fuente": identity, "original": {"sha256": before, "bytes": info.st_size},
            "metadata": probe,
            "capacidad_av_acreditada": False,
            "atributos": {name: {"estado": "pendiente", "observaciones": []} for name in ATTRIBUTES},
            "afirmaciones_contrastadas": [], "conocimiento_aceptado": [],
            "limites": ["Sólo hash y metadata de contenedor; no escucha ni interpretación temporal.",
                        "FPS nominal no son PTS; no hay muestreo ni cobertura perceptual acreditados.",
                        "La URL identifica la fuente declarada; no verifica procedencia en red.",
                        "No se copiaron originales ni metadata privada; no se ejecutó un backend AV."]}


def save_new(base, relative, receipt):
    path = trabajo.safe_path(base, relative)
    if path.suffix != ".json" or not path.parent.is_dir():
        raise ValueError("Elegir JSON nuevo en directorio existente.")
    data = (json.dumps(receipt, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode("utf-8")
    # Publicación atómica sin reemplazo: una escritura parcial queda sólo en el
    # temporal propio. link falla si otro escritor ocupó el nombre de destino.
    descriptor, temporary = tempfile.mkstemp(prefix=".av-ingesta-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
    finally:
        os.unlink(temporary)
    return path


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raiz-medios", type=Path, required=True)
    parser.add_argument("--archivo", required=True, help="Ruta relativa dentro de la raíz autorizada.")
    parser.add_argument("--url", required=True, help="URL pública del reel sin query.")
    parser.add_argument("--ffprobe", default="ffprobe")
    parser.add_argument("--raiz-salida", type=Path, required=True)
    parser.add_argument("--salida", required=True, help="JSON relativo nuevo; no sobrescribe.")
    args = parser.parse_args(argv)
    try:
        output_root = plain_directory(args.raiz_salida)
        output = trabajo.safe_path(output_root, args.salida)
        if os.path.lexists(output):
            raise ValueError("La salida ya existe; no se sobrescribió.")
        receipt = ingest(args.raiz_medios, args.archivo, args.url, args.ffprobe)
        save_new(output_root, args.salida, receipt)
        print(json.dumps({"resultado": "ingesta_instrumental", "capacidad_av_acreditada": False,
                          "sha256_original": receipt["original"]["sha256"]}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        # Errores de SO pueden contener rutas privadas; no exportarlas como evidencia.
        message = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        print(json.dumps({"error": message}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Edición local CPU a partir de decisiones explícitas."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import textwrap
import time

FPS = 30
MAX_SECONDS = 1800
MAX_PARTS = 40
BASE = Path(__file__).resolve().parent


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path):
    if not path.is_file() or path.stat().st_size > 8 * 1024 * 1024:
        raise ValueError("JSON ausente o mayor de 8 MiB.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError):
        raise ValueError("JSON inválido.") from None


def write_json(path, data):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write("\n")


def number(value):
    if type(value) not in (float, int) or not math.isfinite(value) or value < 0:
        raise ValueError("Tiempo inválido. Usar segundos finitos no negativos.")
    return float(value)


def keys(data, required, optional=()):
    if not isinstance(data, dict) or not set(required) <= data.keys():
        raise ValueError("Faltan campos obligatorios del esquema.")
    if data.keys() - set(required) - set(optional):
        raise ValueError("Campo desconocido en el plan.")


def local_file(root, value, media=False):
    if not isinstance(value, str) or not value.strip() or "://" in value:
        raise ValueError("Se requiere archivo local.")
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = root / path
    path = path.resolve(strict=True)
    if not path.is_file():
        raise ValueError("Entrada local ausente o no regular.")
    if media and path.suffix.lower() not in {".mp4", ".mov", ".webm"}:
        raise ValueError("Medios permitidos .mp4, .mov y .webm.")
    if media and re.search(r"(^|[\W_])vlog([\W_]|$)", path.stem, re.I):
        raise ValueError("Vlog excluido de esta cadena.")
    return path


def run(command, timeout=120, cwd=None):
    try:
        result = subprocess.run(command, stdin=subprocess.DEVNULL, capture_output=True,
                                cwd=cwd, timeout=timeout, check=False)
    except subprocess.TimeoutExpired:
        raise ValueError("Proceso excedió el límite CPU/tiempo configurado.") from None
    if result.returncode:
        # El stderr de FFmpeg puede contener rutas o metadata privada.
        raise ValueError("Proceso local falló. Verificar dependencias, pistas y formato.")
    return result.stdout


def probe(path):
    raw = json.loads(run(["ffprobe", "-v", "error", "-protocol_whitelist", "file",
                          "-show_streams", "-show_format", "-of", "json", str(path)], 30))
    duration = number(float(raw["format"]["duration"]))
    videos = [s for s in raw["streams"] if s["codec_type"] == "video"
              and not s.get("disposition", {}).get("attached_pic")]
    if not videos or not 0 < duration <= MAX_SECONDS:
        raise ValueError("Video ausente o duración fuera de 0–1800 segundos.")
    # Los timestamps del contrato son relativos al comienzo de cada pista.
    # Se rechazan desfases grandes para no perder sincronía silenciosamente.
    starts = [float(s.get("start_time", 0)) for s in raw["streams"]
              if s["codec_type"] in {"video", "audio"}]
    if max(starts) - min(starts) > 1 / FPS:
        raise ValueError("Pistas desfasadas más de un frame. Normalizar con revisión humana.")
    return {"duration": duration, "video_index": videos[0]["index"],
            "audio_index": next((s["index"] for s in raw["streams"]
                                 if s["codec_type"] == "audio"), None),
            "width": videos[0]["width"], "height": videos[0]["height"]}


def intervals(rows, duration):
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_PARTS:
        raise ValueError("Se requieren entre 1 y 40 intervalos.")
    result = []
    previous = 0
    offset = 0
    for row in rows:
        keys(row, ("start", "end"))
        start, end = number(row["start"]), number(row["end"])
        if start >= end or end > duration or start < previous:
            raise ValueError("Intervalo fuera de rango, desordenado o solapado.")
        first, last = round(start * FPS), round(end * FPS)
        if first >= last or last > math.floor(duration * FPS + 1e-6):
            raise ValueError("Intervalo vacío o fuera de rango al ajustar a 30 fps.")
        result.append({"requested": row, "start": first / FPS, "end": last / FPS,
                       "output_start": offset / FPS, "frames": last - first})
        offset += last - first
        previous = end
    return result


def load_plan(path):
    plan = read_json(path)
    keys(plan, ("version", "tipo", "entrada", "intervalos"), ("transcripcion", "broll"))
    if type(plan["version"]) is not int or plan["version"] != 1:
        raise ValueError("Versión de esquema no soportada.")
    if plan["tipo"] not in ("reel", "talking_head"):
        raise ValueError("Tipo excluido. Vlog fuera de esta cadena.")
    source = local_file(path.parent, plan["entrada"], media=True)
    info = probe(source)
    cuts = intervals(plan["intervalos"], info["duration"])
    duration = sum(c["frames"] for c in cuts) / FPS
    broll = plan.get("broll", [])
    if not isinstance(broll, list) or len(broll) > MAX_PARTS:
        raise ValueError("Manifest B-roll inválido o mayor de 40 elementos.")
    overlays = []
    previous = 0
    for row in broll:
        keys(row, ("archivo", "start", "end", "source_start"))
        start, end, source_start = (number(row[k]) for k in ("start", "end", "source_start"))
        if start < previous or start >= end or end > duration:
            raise ValueError("B-roll fuera de salida, desordenado o solapado.")
        if any(abs(t * FPS - round(t * FPS)) > 1e-5 for t in (start, end, source_start)):
            raise ValueError("Tiempos B-roll deben coincidir con la grilla de 30 fps.")
        media = local_file(path.parent, row["archivo"], media=True)
        metadata = probe(media)
        if source_start + end - start > metadata["duration"] + 1e-6:
            raise ValueError("B-roll más corto que el intervalo solicitado.")
        overlays.append({**row, "path": media, "info": metadata})
        previous = end
    transcript = None
    if "transcripcion" in plan:
        transcript = local_file(path.parent, plan["transcripcion"])
    return source, info, cuts, overlays, transcript


def segments(data, duration):
    if not isinstance(data, dict) or not isinstance(data.get("segments"), list):
        raise ValueError("Transcripción requiere segments del piloto ASR.")
    rows = data["segments"]
    if not rows or len(rows) > 20000:
        raise ValueError("Transcripción vacía o excesiva.")
    previous = 0
    for row in rows:
        if not isinstance(row, dict) or not {"start", "end", "text"} <= row.keys():
            raise ValueError("Segmento de transcripción inválido.")
        start, end = number(row["start"]), number(row["end"])
        if not start < end <= duration + 1 / FPS or start < previous:
            raise ValueError("Transcripción fuera de rango o solapada.")
        text = row["text"]
        if not isinstance(text, str) or not text.strip() or len(text) > 10000:
            raise ValueError("Texto de subtítulo vacío o excesivo.")
        # Alfabeto acotado para que el presupuesto geométrico sea verificable.
        if any((not (32 <= ord(c) <= 126 or 160 <= ord(c) <= 255) and c not in "\n\r\t–—…“”‘’€")
               or c in "{}\\" for c in text):
            raise ValueError("Subtítulo contiene caracteres fuera del alfabeto latino admitido.")
        for name in ("avg_logprob", "no_speech_prob"):
            if name in row and (type(row[name]) not in (int, float) or not math.isfinite(row[name])):
                raise ValueError("Confianza ASR inválida.")
        if "no_speech_prob" in row and not 0 <= row["no_speech_prob"] <= 1:
            raise ValueError("Probabilidad ASR fuera de rango.")
        previous = end
    return rows


def subtitle_cues(rows, cuts):
    cues = []
    doubts = []
    for cut in cuts:
        for row in rows:
            start, end = max(row["start"], cut["start"]), min(row["end"], cut["end"])
            if start >= end:
                continue
            if start > row["start"] + 0.001 or end < row["end"] - 0.001:
                # No repetir todas las palabras de una frase cortada sobre un fragmento.
                # Se exige un ajuste humano o una transcripción específica del fragmento.
                raise ValueError("Un corte atraviesa un segmento. Ajustar intervalos o transcripción.")
            lines = textwrap.wrap(" ".join(row["text"].split()), width=14,
                                  break_long_words=True, break_on_hyphens=False)
            groups = [lines[i:i + 2] for i in range(0, len(lines), 2)]
            span = end - start
            if len(groups) > 1:
                doubts.append({"tipo": "tiempo_interno_estimado", "start": start, "end": end})
            for index, group in enumerate(groups):
                first = start - cut["start"] + cut["output_start"] + span * index / len(groups)
                last = start - cut["start"] + cut["output_start"] + span * (index + 1) / len(groups)
                if last - first < 0.35:
                    doubts.append({"tipo": "subtitulo_rapido", "start": first, "end": last})
                if round(last * 100) <= round(first * 100):
                    raise ValueError("Subtítulos demasiado breves. Reducir texto o ampliar intervalo.")
                cues.append({"start": first, "end": last, "lines": group})
            if row.get("avg_logprob", 0) < -1 or row.get("no_speech_prob", 0) > 0.6:
                doubts.append({"tipo": "asr_incierto", "start": start, "end": end})
    if not cues:
        raise ValueError("Los intervalos seleccionados no contienen subtítulos.")
    return cues, doubts


def ass_time(seconds):
    value = round(seconds * 100)
    return f"{value // 360000}:{value // 6000 % 60:02}:{value // 100 % 60:02}.{value % 100:02}"


def write_ass(path, cues, formato="vertical"):
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,36,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,0,2,72,72,140,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    if formato == "horizontal":
        header = header.replace("PlayResX: 720", "PlayResX: 1280").replace("PlayResY: 1280", "PlayResY: 720")
        header = header.replace(",72,72,140,1", ",72,72,72,1")
    with path.open("x", encoding="utf-8") as stream:
        stream.write(header)
        for cue in cues:
            text = r"\N".join(cue["lines"])
            stream.write(f"Dialogue: 0,{ass_time(cue['start'])},{ass_time(cue['end'])},Default,,0,0,0,,{text}\n")


def dimensions(width, formato):
    if formato == "vertical" and width in (360, 720, 1080):
        return width, width * 16 // 9
    if formato == "horizontal" and width in (640, 1280, 1920):
        return width, width * 9 // 16
    raise ValueError("Ancho incompatible: vertical 360/720/1080; horizontal 640/1280/1920.")


def render(source, info, cuts, overlays, output, width, timeout, formato="vertical"):
    width, height = dimensions(width, formato)
    geometry = (f"scale=w='trunc(min({width},{height}*dar)/2)*2':"
                f"h='trunc(min({height},{width}/dar)/2)*2',"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black,setsar=1,fps={FPS}")
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
               "-filter_complex_threads", "1", "-threads", "1", "-protocol_whitelist", "file",
               "-i", str(source)]
    for overlay in overlays:
        command += ["-threads", "1", "-protocol_whitelist", "file", "-i", str(overlay["path"])]
    filters = []
    inputs = []
    for index, cut in enumerate(cuts):
        start, end = cut["start"], cut["end"]
        duration = cut["frames"] / FPS
        filters.append(f"[0:{info['video_index']}]setpts=PTS-STARTPTS,"
                       f"trim=start={start}:end={end},setpts=PTS-STARTPTS,"
                       f"{geometry},tpad=stop_mode=clone:stop_duration={duration},"
                       f"trim=end_frame={cut['frames']}[v{index}]")
        if info["audio_index"] is None:
            audio = "anullsrc=r=48000:cl=stereo,"
        else:
            audio = (f"[0:{info['audio_index']}]asetpts=PTS-STARTPTS,atrim=start={start}:end={end},"
                     "asetpts=PTS-STARTPTS,aresample=48000,")
        filters.append(audio + f"aformat=sample_fmts=fltp:channel_layouts=stereo,"
                       f"apad,atrim=duration={duration}[a{index}]")
        inputs.append(f"[v{index}][a{index}]")
    filters.append("".join(inputs) + f"concat=n={len(cuts)}:v=1:a=1[base][audio]")
    previous = "base"
    for index, overlay in enumerate(overlays):
        start, end = overlay["start"], overlay["end"]
        source_start = overlay["source_start"]
        filters.append(f"[{index + 1}:{overlay['info']['video_index']}]setpts=PTS-STARTPTS,"
                       f"trim=start={source_start}:end={source_start + end - start},"
                       f"setpts=PTS-STARTPTS,{geometry},setpts=PTS+{start}/TB[b{index}]")
        filters.append(f"[{previous}][b{index}]overlay=eof_action=pass:repeatlast=0:"
                       f"enable='gte(t,{start})*lt(t,{end})'[o{index}]")
        previous = f"o{index}"
    filters.append(f"[{previous}]ass=subtitulos.ass[out]")
    (output / "filtros.txt").write_text(";\n".join(filters), encoding="utf-8")
    frames = sum(cut["frames"] for cut in cuts)
    command += ["-filter_complex_script", "filtros.txt", "-map", "[out]", "-map", "[audio]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-threads:v", "1",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-threads:a", "1",
                "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
                "-map_metadata", "-1", "-map_chapters", "-1", "-movflags", "+faststart",
                "-t", str(frames / FPS), "pieza.mp4"]
    run(command, timeout=timeout, cwd=output)


def process(args):
    output = args.salida.absolute()
    # mkdir exclusivo reserva la ejecución incluso ante invocaciones concurrentes.
    output.mkdir(mode=0o700, parents=False, exist_ok=False)
    started = time.monotonic()
    receipt = {"version": 1, "resultado": "fallida", "fecha_utc": datetime.now(timezone.utc).isoformat(),
               "revision_humana": "pendiente", "capacidad_av_completa": False,
               "dudas": ["Cotejar palabras, sincronía, encuadre y sonido con el original.",
                         "Música, tono y eventos visuales requieren revisión humana."]}
    try:
        plan_path = args.plan.resolve(strict=True)
        source, info, cuts, overlays, transcript = load_plan(plan_path)
        paths = [plan_path, source] + [row["path"] for row in overlays]
        if transcript:
            paths.append(transcript)
        hashes = {path: digest(path) for path in paths}
        receipt["asr"] = "transcripcion_aportada" if transcript else "small_cpu_int8_offline"
        asr_started = time.monotonic()
        if transcript is None:
            if info["audio_index"] is None:
                raise ValueError("ASR requiere audio o una transcripción aportada.")
            transcript = output / "transcripcion.json"
            run([str(args.asr_python.expanduser()), str(BASE / "asr_offline.py"),
                 "--entrada", str(source), "--salida", str(transcript),
                 "--modelos", str(args.modelos.expanduser())], args.timeout)
        receipt["tiempo_asr_s"] = round(time.monotonic() - asr_started, 3)
        rows = segments(read_json(transcript), info["duration"])
        cues, doubts = subtitle_cues(rows, cuts)
        receipt["dudas"] += doubts
        if info["audio_index"] is None:
            receipt["dudas"].append("Fuente sin audio. La salida lleva silencio explícito.")
        receipt["intervalos"] = cuts
        receipt["broll"] = [{k: v for k, v in row.items() if k not in {"path", "info", "archivo"}}
                             for row in overlays]
        for row, overlay in zip(receipt["broll"], overlays):
            row["sha256"] = hashes[overlay["path"]]
        write_ass(output / "subtitulos.ass", cues, args.formato)
        write_json(output / "subtitulos.json", {"segments": cues})
        render_started = time.monotonic()
        render(source, info, cuts, overlays, output, args.ancho, args.timeout, args.formato)
        receipt["tiempo_render_s"] = round(time.monotonic() - render_started, 3)
        measured = probe(output / "pieza.mp4")
        expected = sum(cut["frames"] for cut in cuts) / FPS
        if abs(measured["duration"] - expected) > 1 / FPS + 0.005:
            raise ValueError("Duración renderizada difiere del plan más de un frame.")
        if (measured["width"], measured["height"]) != dimensions(args.ancho, args.formato):
            raise ValueError("La salida no tiene las dimensiones solicitadas.")
        if any(digest(path) != before for path, before in hashes.items()):
            raise ValueError("Una entrada cambió durante la ejecución.")
        receipt.update(resultado="renderizada_pendiente_revision", fps=FPS, formato=args.formato,
                       duracion_esperada_s=expected, salida=measured,
                       sha256_salida=digest(output / "pieza.mp4"),
                       entradas=[{"rol": "plan" if p == plan_path else "medio_o_transcripcion",
                                  "sha256": h} for p, h in hashes.items()])
    except (ValueError, OSError, KeyError, TypeError) as error:
        receipt["error"] = str(error) if isinstance(error, ValueError) else "Entrada o dependencia local inválida o ausente."
        raise ValueError(receipt["error"]) from None
    finally:
        receipt["tiempo_total_s"] = round(time.monotonic() - started, 3)
        write_json(output / "reporte.json", receipt)
    return receipt


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--salida", required=True, type=Path, help="Directorio nuevo con padre existente.")
    parser.add_argument("--formato", choices=("vertical", "horizontal"), default="vertical")
    parser.add_argument("--ancho", type=int, choices=(360, 640, 720, 1080, 1280, 1920))
    parser.add_argument("--timeout", type=int, choices=range(1, 3601), default=600, metavar="1..3600")
    parser.add_argument("--asr-python", type=Path, default=Path("~/asr/venv/bin/python"))
    parser.add_argument("--modelos", type=Path, default=Path("~/asr/modelos"))
    args = parser.parse_args(argv)
    if args.ancho is None:
        args.ancho = 720 if args.formato == "vertical" else 1280
    try:
        receipt = process(args)
        print(json.dumps({"resultado": receipt["resultado"], "sha256": receipt["sha256_salida"]}))
        return 0
    except (ValueError, OSError) as error:
        message = str(error) if isinstance(error, ValueError) else "Salida existente, padre ausente o acceso denegado."
        print(json.dumps({"resultado": "rechazada", "error": message}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

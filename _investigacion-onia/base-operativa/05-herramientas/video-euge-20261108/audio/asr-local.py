#!/usr/bin/env python3
"""Transcribe un archivo local con faster-whisper y pesos ya disponibles."""

import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import time

os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
from faster_whisper import WhisperModel
import numpy as np
import onnxruntime

onnxruntime.disable_telemetry_events()

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("media", type=Path)
parser.add_argument("model_dir", type=Path)
parser.add_argument("output", type=Path, help="JSON privado nuevo")
parser.add_argument("--language")
parser.add_argument("--beam-size", type=int, choices=(1, 5), default=5)
parser.add_argument("--pcm-cache", type=Path, help="Numpy PCM float32 mono a 16 kHz derivado del mismo WebM")
parser.add_argument("--clip", type=float, nargs=2, metavar=("INICIO", "FIN"), help="Ventana PCM, en segundos")
args = parser.parse_args()
media = args.media.resolve(strict=True)
model_dir = args.model_dir.resolve(strict=True)
if not media.is_file() or media.suffix.lower() not in (".webm", ".wav"):
    parser.error("Se necesita un archivo WebM o WAV local.")
if not all((model_dir / filename).is_file() for filename in ("model.bin", "tokenizer.json", "config.json")):
    parser.error("El modelo indicado debe incluir pesos, tokenizer y config locales.")
if args.output.exists():
    parser.error("El destino privado ya existe.")

os.umask(0o077)
started = time.monotonic()
with media.open("rb") as handle:
    sha256 = hashlib.file_digest(handle, "sha256").hexdigest()
if bool(args.pcm_cache) != bool(args.clip):
    parser.error("Indique juntos --pcm-cache y --clip.")
audio = str(media)
clip_start = 0.0
pcm_total = None
if args.pcm_cache:
    pcm = np.load(args.pcm_cache, mmap_mode="r", allow_pickle=False)
    if pcm.ndim != 1 or pcm.dtype != np.float32:
        parser.error("El PCM debe ser un vector float32 mono.")
    left, right = (round(value * 16000) for value in args.clip)
    if not (0 <= left < right <= len(pcm)):
        parser.error("Ventana fuera del PCM disponible.")
    audio = pcm[left:right]
    clip_start = left / 16000
    pcm_total = len(pcm) / 16000
model = WhisperModel(
    str(model_dir), local_files_only=True, device="cpu", compute_type="int8",
    cpu_threads=2, num_workers=1,
)
segments, info = model.transcribe(
    audio, task="transcribe", language=args.language, beam_size=args.beam_size, vad_filter=True,
)
rows = [
    {
        "start_s": round(segment.start + clip_start, 6), "end_s": round(segment.end + clip_start, 6), "text": segment.text.strip(),
        "avg_logprob": segment.avg_logprob, "no_speech_prob": segment.no_speech_prob,
    }
    for segment in segments
]
summary = {
    "source_sha256": sha256,
    "faster_whisper_version": version("faster-whisper"),
    "model_snapshot": model_dir.name,
    "device": "cpu int8, 2 threads",
    "vad": True,
    "beam_size": args.beam_size,
    "wall_s": round(time.monotonic() - started, 3),
    "audio_duration_s": pcm_total if pcm_total is not None else info.duration,
    "clip_pcm_s": [clip_start, round(clip_start + info.duration, 6)] if args.clip else None,
    "language": info.language,
    "language_forced": args.language is not None,
    "language_probability": info.language_probability,
    "segment_count": len(rows),
    "first_segment_s": rows[0]["start_s"] if rows else None,
    "last_segment_s": rows[-1]["end_s"] if rows else None,
    "time_reference": "audio decodificado del archivo local",
    "auditory_observation": False,
}
with args.output.open("x", encoding="utf-8") as handle:
    json.dump({**summary, "segments": rows}, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
print(json.dumps(summary, ensure_ascii=False, indent=2))

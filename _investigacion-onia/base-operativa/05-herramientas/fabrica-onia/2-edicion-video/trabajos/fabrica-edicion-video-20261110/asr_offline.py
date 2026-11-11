#!/usr/bin/env python3
"""Adaptación local del piloto asr-local, con caché de sólo lectura y sin descarga."""
import argparse
import json
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    parser.add_argument("--modelos", type=Path, required=True)
    args = parser.parse_args()
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    # Un directorio concreto evita la resolución/descarga por nombre de modelo.
    cached = args.modelos / "models--Systran--faster-whisper-small"
    reference = (cached / "refs" / "main").read_text().strip()
    if len(reference) != 40 or any(c not in "0123456789abcdef" for c in reference):
        raise ValueError("Referencia local small inválida.")
    snapshot = cached / "snapshots" / reference
    for name in ("model.bin", "config.json", "tokenizer.json", "vocabulary.txt"):
        if not (snapshot / name).is_file():
            raise ValueError("Modelo small local incompleto.")
    from faster_whisper import WhisperModel

    model = WhisperModel(str(snapshot), device="cpu", compute_type="int8", cpu_threads=2,
                         num_workers=1, local_files_only=True)
    found, meta = model.transcribe(str(args.entrada), language="es", beam_size=5,
                                  vad_filter=True, condition_on_previous_text=False)
    rows = [{"start": s.start, "end": s.end, "text": s.text.strip(),
             "avg_logprob": s.avg_logprob, "no_speech_prob": s.no_speech_prob}
            for s in found if s.text.strip()]
    if not rows:
        raise ValueError("ASR sin voz. Requiere material hablado y cotejo humano.")
    with args.salida.open("x", encoding="utf-8") as stream:
        json.dump({"language": meta.language, "segments": rows,
                   "motor": "faster-whisper/small/cpu/int8/2threads/beam5/vad/offline",
                   "cotejo_humano": "pendiente"}, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()

"""Prueba local reproducible: controles PCM, medidas y ASR offline (no escucha).

No instala, descarga, llama APIs ni identifica emociones/SFX por inferencia.
Los binarios se escriben sólo en --media; JSON de evidencia junto al script.
"""
import argparse
import hashlib
import json
import math
import subprocess
import time
from pathlib import Path

import numpy as np
from scipy.io import wavfile

OUT = Path(__file__).resolve().parent


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def fingerprint(path):
    return {"file": str(path), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def measure(path):
    sr, raw = wavfile.read(path)
    samples = raw.astype(np.float64) / (2 ** (raw.dtype.itemsize * 8 - 1))
    mono = samples.mean(axis=1) if samples.ndim == 2 else samples
    peak = float(np.max(np.abs(samples)))
    rms = float(np.sqrt(np.mean(samples ** 2)))
    spec = np.abs(np.fft.rfft(mono))
    freq = float(np.fft.rfftfreq(len(mono), 1 / sr)[np.argmax(spec)]) if peak else None
    return {**fingerprint(path), "sample_rate": sr, "frames": len(mono),
            "channels": 1 if samples.ndim == 1 else samples.shape[1],
            "duration_s": len(mono)/sr, "peak": peak, "rms": rms,
            "rms_dbfs": 20*math.log10(rms) if rms else None,
            "all_zero": bool(np.all(samples == 0)), "dominant_fft_hz": freq}


def prepare(media):
    sr = 16000
    t = np.arange(6*sr) / sr
    controls = {
        "control-silencio.wav": np.zeros(len(t)),
        "control-tono440.wav": 0.2 * np.sin(2*np.pi*440*t),
        "control-patron.wav": np.where((t >= 2) & (t < 4), 0.2*np.sin(2*np.pi*440*t), 0),
    }
    for name, data in controls.items():
        wavfile.write(media / name, sr, np.rint(data * 32767).astype(np.int16))
    results = {name: measure(media / name) for name in controls}
    assertions = {
        "silencio_todas_muestras_cero": results["control-silencio.wav"]["all_zero"],
        "tono_frecuencia_440": abs(results["control-tono440.wav"]["dominant_fft_hz"] - 440) < 1,
        "tono_rms_esperado": abs(results["control-tono440.wav"]["rms"] - 0.2 / math.sqrt(2)) < 0.001,
    }
    sr, pattern = wavfile.read(media / "control-patron.wav")
    assertions["patron_intervalos_exacto"] = bool(
        np.all(pattern[:2*sr] == 0) and np.any(pattern[2*sr:4*sr] != 0)
        and np.all(pattern[4*sr:] == 0))
    real = measure(media / "pedro-asr-16k.wav")
    original = measure(media / "pedro-original-pcm24.wav")
    # Five historical visual transitions, retaining 1s context each side.
    _, pcm = wavfile.read(media / "pedro-original-pcm24.wav")
    rate = original["sample_rate"]
    clips, selection = [], []
    for n, center in enumerate([3.3, 33.7, 46.5, 61.7, 74.0], 1):
        start, end = int(round((center-1)*rate)), int(round((center+1)*rate))
        part = pcm[start:end]
        dest = media / f"pedro-fragmento-{n:02d}.wav"
        # scipy writes int32 PCM; values from PCM24 retain original significance.
        wavfile.write(dest, rate, part)
        clips.append({**fingerprint(dest), "source_start_s": start/rate,
                      "source_end_s": end/rate, "selection_start_s": (n-1)*2.5,
                      "selection_end_s": (n-1)*2.5+2,
                      "source_pcm_equal": bool(np.array_equal(wavfile.read(dest)[1], part))})
        if selection:
            selection.append(np.zeros((int(rate*.5), pcm.shape[1]), dtype=pcm.dtype))
        selection.append(part)
    wavfile.write(media / "pedro-seleccion-12s.wav", rate, np.concatenate(selection))
    # Per 100ms energy: factual waveform measurements, never voice pause labels.
    sr, x = wavfile.read(media / "pedro-asr-16k.wav")
    x = x.astype(np.float64)/32768
    energy=[]
    for begin in range(0,len(x),sr//10):
        v=x[begin:begin+sr//10]
        rms=float(np.sqrt(np.mean(v*v)))
        energy.append({"start_s":begin/sr,"end_s":min(begin+sr//10,len(x))/sr,
                       "rms_dbfs":20*math.log10(rms) if rms else None,
                       "peak":float(np.max(np.abs(v)))})
    write_json("controles-y-medidas.json", {"scope":"PCM measurements, not listening",
               "expected":{"silence":"all PCM zero", "tone":"6s 440Hz amplitude .2", "pattern":"2s silence + 2s tone + 2s silence"},
               "controls":results,"assertions":assertions,"pass":all(assertions.values()),
               "real_asr":real,"original_pcm":original})
    write_json("fragmentos.json", {"source":original,"clips":clips,
               "selection":fingerprint(media/"pedro-seleccion-12s.wav"),
               "synthetic_separators":"0.5s between clips; selection is not continuous source",
               "question":"Son cinco fragmentos separados por medio segundo de silencio. ¿En cuáles distinguís un sonido breve añadido? Respondé por número; si no se distingue, indicá no se distingue."})
    write_json("energia-100ms.json",energy)
    print(json.dumps({"controls_pass":all(assertions.values()),"real_duration":real["duration_s"],"original_duration":original["duration_s"]}))


def asr(media, model_path, vad=False, input_name="pedro-asr-16k.wav", language="es"):
    required=["control-silencio.wav","control-tono440.wav","control-voz.wav",input_name]
    missing=[name for name in required if not (media/name).is_file()]
    if missing:
        raise ValueError("Faltan entradas; no se ejecutó ASR: " + ", ".join(missing))
    from faster_whisper import WhisperModel
    start = time.monotonic()
    model=WhisperModel(str(model_path),device="cpu",compute_type="int8",cpu_threads=4,
                       num_workers=1,local_files_only=True)
    files=[("control-silencio.wav","es"),("control-tono440.wav","es"),
           ("control-voz.wav","en"),(input_name,language)]
    result={"method":"faster-whisper small, CPU int8, 4 threads, cached weights only",
            "model_directory":str(model_path),"vad_filter":vad,
            "scope":"words from audio, not music/SFX/emotion/prosody validation", "files":[]}
    for filename,lang in files:
        before=time.monotonic()
        segments, info=model.transcribe(str(media/filename), language=lang,
              beam_size=5,vad_filter=vad,condition_on_previous_text=False,
              word_timestamps=True, temperature=0)
        rows=[]
        for s in segments:
            rows.append({"start":s.start,"end":s.end,"text":s.text,
                         "avg_logprob":s.avg_logprob,"no_speech_prob":s.no_speech_prob,
                         "words":[{"start":w.start,"end":w.end,"word":w.word,
                                   "probability":w.probability} for w in (s.words or [])]})
        item={**fingerprint(media/filename),"elapsed_s":round(time.monotonic()-before,3),
              "duration":info.duration,"duration_after_vad":info.duration_after_vad,
              "segments":rows,"text":"".join(x["text"] for x in rows)}
        result["files"].append(item)
        write_json("asr-vad-resultados.json" if vad else "asr-resultados.json",result)
        print(json.dumps({"file":filename,"seconds":item["elapsed_s"],"text":item["text"]},ensure_ascii=False),flush=True)
    result["total_elapsed_s"]=round(time.monotonic()-start,3)
    result["model_files"]=[fingerprint(p) for p in sorted(model_path.iterdir()) if p.is_file()]
    write_json("asr-vad-resultados.json" if vad else "asr-resultados.json",result)


if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=["prepare","asr"])
    p.add_argument("--media",type=Path,required=True)
    p.add_argument("--model",type=Path)
    p.add_argument("--vad",action="store_true")
    p.add_argument("--input",default="pedro-asr-16k.wav",help="WAV real dentro de --media, para reutilizar con otra referencia")
    p.add_argument("--language",default="es")
    p.add_argument("--report-dir",type=Path,help="Subcarpeta de evidencia para no reemplazar otra referencia")
    a=p.parse_args()
    if a.mode=="asr" and not a.model:
        p.error("asr requiere --model con una carpeta existente de pesos locales")
    if a.report_dir:
        candidate=a.report_dir.resolve()
        if not candidate.is_relative_to(OUT):
            p.error("--report-dir debe permanecer dentro de audio-tecnico")
        OUT=candidate
        OUT.mkdir(parents=True,exist_ok=True)
    if Path(a.input).name != a.input:
        p.error("--input debe ser sólo el nombre de archivo")
    if a.mode=="prepare": prepare(a.media.resolve())
    else: asr(a.media.resolve(),a.model.resolve(),a.vad,a.input,a.language)

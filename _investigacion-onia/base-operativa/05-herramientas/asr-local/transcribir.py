"""Public URL -> audio -> small/CPU/int8 -> timestamped Markdown. No cookies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
from datetime import datetime, timezone
os.environ.setdefault('HF_HOME', '/home/onia-codex-worker/asr/huggingface')
os.environ.setdefault('HF_XET_CACHE', '/home/onia-codex-worker/asr/huggingface/xet')
import av
import yt_dlp
from faster_whisper import WhisperModel

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('url')
p.add_argument('--max-seconds', type=float, default=1800, help='Reject longer media before downloading (default 30 minutes)')
a = p.parse_args()
root = Path(os.environ.get('ASR_ROOT', '/home/onia-codex-worker/asr'))
out = Path(os.environ.get('ASR_OUTPUT', '/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/03-referentes/asr'))
out.mkdir(parents=True, exist_ok=True)
cache = root / 'audio'
cache.mkdir(parents=True, exist_ok=True)
opts = {'format': 'bestaudio/best', 'noplaylist': True, 'socket_timeout': 25,
        'retries': 1, 'fragment_retries': 1, 'quiet': True,
        'outtmpl': str(cache / '%(extractor_key)s-%(id)s.%(ext)s')}
with yt_dlp.YoutubeDL(opts) as ydl:
    info = ydl.extract_info(a.url, download=False)
    if info.get('_type') in ('playlist', 'multi_video'):
        raise SystemExit('Se requiere una sola pieza, no una lista.')
    duration = info.get('duration')
    if duration is not None and duration > a.max_seconds:
        raise SystemExit(f'Duración desconocida o superior al límite {a.max_seconds}s: {duration}')
    ident = hashlib.sha256(a.url.encode()).hexdigest()[:12]
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    target = out / f'{ident}-{stamp}.md'
    downloaded = ydl.extract_info(a.url, download=True)
    audio = Path(ydl.prepare_filename(downloaded))
with av.open(str(audio)) as media:
    measured = media.duration / av.time_base if media.duration else None
if measured is None or measured > a.max_seconds:
    raise SystemExit(f'Duración descargada desconocida o excesiva: {measured}')
duration = measured
model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=2,
                     download_root=str(root / 'modelos'))
segments, meta = model.transcribe(str(audio), beam_size=5, vad_filter=True)
def ts(seconds):
    ms = round(seconds * 1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
rows = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
if not rows:
    raise SystemExit('Sin segmentos de voz: no se publica transcripción vacía.')
body = [f'# ASR: {info.get("title", info["id"])}', '', f'Fuente: {a.url}',
        f'Canal declarado: {info.get("uploader", "desconocido")}',
        f'Fecha UTC: {stamp}', f'Duración fuente: {duration} s',
        f'Idioma detectado: {meta.language}',
        'Motor: faster-whisper; modelo small; CPU; int8; VAD; beam_size=5.',
        f'SHA-256 audio: {hashlib.sha256(audio.read_bytes()).hexdigest()}',
        'Transcripción automática sin cotejo auditivo humano. Puede contener errores; no prueba edición, música ni resultados comerciales.', '']
body += [f'[{ts(r["start"])}–{ts(r["end"])}] {r["text"]}' for r in rows]
with target.open('x') as f:
    f.write('\n'.join(body) + '\n')
with target.with_suffix('.json').open('x') as f:
    json.dump({'url': a.url, 'duration': duration, 'language': meta.language, 'segments': rows}, f, ensure_ascii=False, indent=2)
print(target)

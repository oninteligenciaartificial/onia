"""ASR completo de la preview autorizada, pesos locales existentes, sin red."""
import hashlib
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
audio=BASE/'operacion/referentes-20261105/secundarios/erik/erik-hermes-asr-16k.wav'
weights=Path('C:/Users/PC/.cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120')
start=time.monotonic()
model=WhisperModel(str(weights),device='cpu',compute_type='int8',cpu_threads=4,num_workers=1,local_files_only=True)
segments,info=model.transcribe(str(audio),language='es',beam_size=5,vad_filter=True,
    condition_on_previous_text=False,word_timestamps=True,temperature=0)
rows=[]
for s in segments:
    rows.append({'start':s.start,'end':s.end,'text':s.text,'avg_logprob':s.avg_logprob,
                 'no_speech_prob':s.no_speech_prob,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in (s.words or [])]})
result={'source':str(audio),'sha256':hashlib.sha256(audio.read_bytes()).hexdigest(),
        'duration_input_s':info.duration,'duration_after_vad_s':info.duration_after_vad,
        'model':str(weights),'method':'faster-whisper 1.2.1 small CPU int8 four threads, VAD, no network',
        'elapsed_s':round(time.monotonic()-start,3),'segments':rows,
        'scope':'automatic words/timings only; not listened, not visually reviewed, not corrected by human'}
(OUT/'erik-asr.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'erik-asr.txt').write_text('\n'.join(f"[{s['start']:.2f}–{s['end']:.2f}] {s['text'].strip()}" for s in rows)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ['duration_input_s','duration_after_vad_s','elapsed_s']},ensure_ascii=False))

"""Consolida medidas y verifica artefactos existentes; no modelos ni red."""
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from scipy.io import wavfile

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'

def dump(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def read(name):
    return json.loads((OUT/name).read_text(encoding='utf-8'))

sr,pcm=wavfile.read(MEDIA/'pedro-original-pcm24.wav')
clips=read('fragmentos.json')
clip_checks=[]
for row in clips['clips']:
    rate,part=wavfile.read(row['file'])
    start,end=round(row['source_start_s']*sr),round(row['source_end_s']*sr)
    clip_checks.append(rate==sr and np.array_equal(part,pcm[start:end]))
asr=read('asr-vad-resultados.json')
raw=read('asr-resultados.json')
texts=[r['text'].strip() for r in asr['files']]
checks={
    'pcm_controls_pass':read('controles-y-medidas.json')['pass'],
    'five_clips_pcm_exact':all(clip_checks) and len(clip_checks)==5,
    'vad_silence_empty':texts[0]=='',
    'vad_tone_empty':texts[1]=='',
    'known_speech_matches_normalized':texts[2].lower().replace('7','seven')=='this is a controlled audio test. the number is seven.',
    'real_90s_passed_to_asr':asr['files'][-1]['duration']>90,
    'raw_tone_failure_preserved':raw['files'][1]['text'].strip()!='',
}
decode=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(MEDIA/'pedro-Dd6oC4EkRX1.mp4'),'-f','null','-'],capture_output=True,text=True)
checks['full_decode_exit0_no_errors']=decode.returncode==0 and not decode.stderr.strip()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(MEDIA/'pedro-Dd6oC4EkRX1.mp4')],text=True))
pcm_hash=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(MEDIA/'pedro-original-pcm24.wav'),'-c:a','pcm_s32le','-f','hash','-hash','sha256','-'],text=True).strip().split('=')[1]
sr,x=wavfile.read(MEDIA/'pedro-asr-16k.wav')
x=x.astype(np.float64)/32768
bounds=[0,3.2,33.5,46.3,61.7,73.8,len(x)/sr]
labels=['Promesa','Avatar/problema','Escasez real','Urgencia','Metodologia propia','Producto y bonos']
sections=[]
for label,a,b in zip(labels,bounds,bounds[1:]):
    v=x[round(a*sr):round(b*sr)]
    words=[w for s in asr['files'][-1]['segments'] for w in s['words'] if a <= w['start'] < b]
    sections.append({'visual_section_historical':label,'start_s':a,'end_s':b,
                     'mono16k_rms_dbfs':round(float(20*np.log10(np.sqrt(np.mean(v*v)))),2),
                     'asr_word_units':len(words),'asr_word_units_per_minute':round(len(words)*60/(b-a),1)})
dump('verificacion.json',{'scope':'technical extraction, controls and ASR only; no acoustic listening acceptance',
     'checks':checks,'technical_pass':all(checks.values()),'decode_stderr':decode.stderr,
     'acoustic_listening_complete':False,'native_audio_input_error':'audio content omitted because you do not support audio input'})
dump('tramos-medidos.json',{'source':'new public MP4 2026-11-05; historical visual chapter boundaries are approximate',
     'sections':sections,'scope':'energy + ASR words, not perceived pacing, prosody or verified lip sync'})
files=[]
for path in sorted(MEDIA.iterdir()):
    if path.is_file():
        files.append({'file':path.relative_to(BASE).as_posix(),'bytes':path.stat().st_size,
                      'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
dump('manifest.json',{'source_url':'https://www.instagram.com/pedrobuerbaum/reel/Dd6oC4EkRX1/',
     'retrieved_date':'2026-11-05 America/Caracas','repo_head_at_start':'1119f5e94b24eaa7d8448319d8b7f424612db27d',
     'provenance':'public download, no login/cookies; yt-dlp 2026.8.19; FFmpeg 8.1.1',
     'first_attempt':'sandbox DNS error resolving instagram.com',
     'second_attempt':'approved network execution, download and remux successful',
     'cloud_source_pcm_s32_sha256':'63a4d73004c08f970baf8bb0529c31782700a408c6f371c1d4d92b6e7495d726',
     'current_pcm_s32_sha256':pcm_hash,'same_pcm_as_historical':pcm_hash=='63a4d73004c08f970baf8bb0529c31782700a408c6f371c1d4d92b6e7495d726',
     'probe':probe,'files':files})
print(json.dumps({'checks':checks,'technical_pass':all(checks.values()),'media_files':len(files),'media_bytes':sum(f['bytes'] for f in files),'same_pcm_as_historical':False},indent=2))

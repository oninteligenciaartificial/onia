"""Controles sintéticos de click y melodía; no son una escucha humana."""
import hashlib
import json
from pathlib import Path
import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
sr=16000
t=np.arange(6*sr)/sr
click=np.zeros(6*sr,dtype=np.float32)
click[2*sr]=0.8
notes=[261.63,329.63,392.0,523.25,392.0,329.63]
melody=np.zeros_like(click)
for i,f in enumerate(notes):
    local=np.arange(sr)/sr
    env=np.minimum(1,local/.02)*np.minimum(1,(1-local)/.05)
    melody[i*sr:(i+1)*sr]=0.18*np.sin(2*np.pi*f*local)*env
sf.write(MEDIA/'control-click.wav',click,sr,subtype='PCM_16')
sf.write(MEDIA/'control-melodia.wav',melody,sr,subtype='PCM_16')
voice,voice_sr=sf.read(MEDIA/'control-voz-es.wav',dtype='float32')
voice=resample_poly(voice,320,441) if voice_sr==22050 else voice
mixed=melody*.35
mixed[:min(len(voice),len(mixed))]+=voice[:len(mixed)]*.5
sf.write(MEDIA/'control-mezcla.wav',mixed,sr,subtype='PCM_16')
files=[]
for name in ['control-voz-es.wav','control-click.wav','control-melodia.wav','control-mezcla.wav']:
    path=MEDIA/name
    info=sf.info(path)
    files.append({'name':name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                  'sample_rate':info.samplerate,'channels':info.channels,'duration_s':info.duration})
data={'scope':'controles conocidos para usar sólo después de superar básicos',
      'spanish_voice':'Windows OneCore Microsoft Helena es-ES; texto introducido: Hola, esta es una prueba de audio. El número es siete.',
      'click':'un pulso de 1 muestra a 2,0s sobre 6s de silencio',
      'melody':'6 notas senoidales sintetizadas de 1s, sin instrumentos reales',
      'mix':'voz sintética española y melodía sintética, sin VAD; ganancias .5 y .35',
      'files':files}
(OUT/'controles-adicionales.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(files,indent=2))

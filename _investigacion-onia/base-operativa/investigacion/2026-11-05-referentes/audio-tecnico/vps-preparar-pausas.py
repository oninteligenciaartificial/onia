import numpy as np,wave,json,hashlib
from faster_whisper import decode_audio
x=decode_audio('/work/input/control-voz-es.wav',sampling_rate=16000)
z=np.zeros(16000,dtype=np.float32); y=np.concatenate((z,x,z))
for n,gain in [('normal',1),('suave',.25)]:
 p='/work/input/voz-pausa-correcta-'+n+'.wav'; a=(np.clip(y*gain,-1,1)*32767).astype('<i2')
 with wave.open(p,'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(16000);f.writeframes(a.tobytes())
 print(n,hashlib.sha256(open(p,'rb').read()).hexdigest(),len(a)/16000)

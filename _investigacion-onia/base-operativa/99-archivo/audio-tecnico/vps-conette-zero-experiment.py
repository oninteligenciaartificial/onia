import hashlib,json,sys,wave
import numpy as np
p=sys.argv[1]
with open(p,'rb') as f:data=f.read()
h=hashlib.sha256(data).hexdigest()
with wave.open(p,'rb') as w:
 if (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getcomptype())!=(1,2,32000,'NONE') or not 32000 <= w.getnframes() <= 960000:raise ValueError('expected PCM16 mono 32000 Hz 1-30s uncompressed')
 raw=w.readframes(w.getnframes())
a=np.frombuffer(raw,dtype='<i2')
r={'input_sha256':h,'sample_range':[0,len(a)],'sample_rate':32000,'nonzero_samples':int(np.count_nonzero(a)),'model_sha256':'271b9f4409ebbceaa0d5fe5319069a3a56e269ab0b868616d7e23f5145cc0ce2'}
if not np.any(a):r.update(route='exact_digital_zero',result='sin se?al digital',caption=None)
else:
 import torch
 from conette import CoNeTTEConfig,CoNeTTEModel
 with open('/work/model/pytorch_model.bin','rb') as f:
  actual=hashlib.file_digest(f,'sha256').hexdigest() if hasattr(hashlib,'file_digest') else None
 if actual is None:
  h2=hashlib.sha256()
  with open('/work/model/pytorch_model.bin','rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h2.update(block)
  actual=h2.hexdigest()
 if actual!=r['model_sha256']:raise ValueError('model hash mismatch')
 torch.set_num_threads(1);torch.set_num_interop_threads(1)
 cfg=CoNeTTEConfig.from_pretrained('/work/model',local_files_only=True)
 model=CoNeTTEModel.from_pretrained('/work/model',config=cfg,device='cpu',offline=True,local_files_only=True).eval()
 with torch.inference_mode():out=model(torch.from_numpy(a.astype(np.float32)/32768).unsqueeze(0),sr=32000,task='audiocaps',beam_size=3,min_pred_size=3,max_pred_size=20)
 r.update(route='nonzero_to_conette',result='caption_raw',caption=out['cands'],task=out['tasks'])
print(json.dumps(r,ensure_ascii=False,default=str))

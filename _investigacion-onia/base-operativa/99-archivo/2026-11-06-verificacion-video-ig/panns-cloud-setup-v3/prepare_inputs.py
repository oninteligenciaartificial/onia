from pathlib import Path
import json,hashlib,wave,subprocess,uuid
O=Path(__file__).resolve().parent;R=O.parent
assert json.loads((O/'csv-installed.json').read_text())['complete']
inputs={}
for case,folder in [('zeros','negativo-v1'),('voice','positivo-v1')]:
 control=json.loads((R/folder/'control-manifest.json').read_text());chunks=[];sources=[]
 for x in control['files']:
  if x.get('modality')!='audio':continue
  p=Path(x['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
  with wave.open(str(p),'rb') as w:
   assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,16000,16000);chunks.append(w.readframes(16000))
  sources.append({'path':str(p),'sha256':x['sha256']})
 assert len(chunks)==2
 source=O/(uuid.uuid4().hex+'.wav');derived=O/(uuid.uuid4().hex+'.wav')
 with wave.open(str(source),'wb') as w:w.setparams((1,2,16000,0,'NONE','not compressed'));w.writeframes(b''.join(chunks))
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-filter_threads','1','-i',str(source),'-ar','32000','-ac','1','-c:a','pcm_s16le','-threads','1',str(derived)]
 subprocess.run(cmd,check=True)
 with wave.open(str(derived),'rb') as w:assert (w.getnchannels(),w.getsampwidth(),w.getframerate(),w.getnframes())==(1,2,32000,64000)
 inputs[case]={'path':str(derived),'sha256':hashlib.sha256(derived.read_bytes()).hexdigest(),'bytes':derived.stat().st_size,'samples':64000,'rate':32000,'duration':2,'source_chunks':sources,'command':cmd,'extra_padding':0,'voice_scope':'complete one two0.8639375s within original1s padded chunk, plus final1s silence' if case=='voice' else 'two seconds digital zeros'}
freeze={'inputs':inputs,'CSV':json.loads((O/'csv-installed.json').read_text()),'checkpoint':json.loads((R/'panns-setup-v3/preparation-receipt.json').read_text())['checkpoint'],'params':{'sample_rate':32000,'window_size':1024,'hop_size':320,'mel_bins':64,'fmin':50,'fmax':14000,'classes':527,'interpolate':'nearest','CPU':1,'workers':1,'batch':1,'AS_GiB':3,'CPU_wall_seconds':120,'reserve_GiB':6,'VAD':False},'criterion':{'known_controls_not_retained':True,'paired1':'max Speech frame score voice > max Speech frame score zeros','paired2':'mean Speech on[0,0.8639375) voice > mean Speech on[1,2) final silence','threshold':None,'scores_not_calibrated_event_probabilities':True,'truth':'generator, not human audition'},'adapter_sha256':hashlib.sha256((O/'infer.py').read_bytes()).hexdigest()}
(O/'input-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n');print('inputs/adapter/params/paired criteria frozen BEFORE first scores')

from pathlib import Path
import json,hashlib,wave,subprocess,uuid
O=Path(__file__).resolve().parent;R=O.parent
assert json.loads((O/'zeros-receipt.json').read_text())['complete'] and json.loads((O/'voice-receipt.json').read_text())['complete']
source=R/'cormac-transfer-v1/DfWLWspIruU-remux.mp4'
assert source.stat().st_size==10749773 and hashlib.sha256(source.read_bytes()).hexdigest()=='2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5'
full=O/(uuid.uuid4().hex+'.wav');cmd=['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-filter_threads','1','-i',str(source),'-map','0:a:0','-vn','-ar','32000','-ac','1','-c:a','pcm_s16le','-threads','1',str(full)]
subprocess.run(cmd,check=True)
with wave.open(str(full),'rb') as w:
 assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,32000)
 count=w.getnframes();raw=w.readframes(count)
target=1208960;assert count>=target,'decoded audio shorter than declared container: do not fabricate coverage or silence'
windows=[]
for i,(start,end) in enumerate([(0,320000),(320000,640000),(640000,960000),(960000,target)]):
 case=f'cormac{i}';path=O/(uuid.uuid4().hex+'.wav')
 with wave.open(str(path),'wb') as w:w.setparams((1,2,32000,0,'NONE','not compressed'));w.writeframes(raw[start*2:end*2])
 entry={'case':case,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'samples':end-start,'rate':32000,'duration':(end-start)/32000,'interval_source_seconds':[start/32000,end/32000],'padding':0}
 (O/(case+'-input.json')).write_text(json.dumps(entry,indent=2)+'\n');windows.append(entry)
(O/'cormac-input-freeze.json').write_text(json.dumps({'source':str(source),'source_sha256':'2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5','container_duration_seconds':37.78,'decoded_full_samples':count,'decoded_full_duration_seconds':count/32000,'beyond_container_samples_not_covered':count-target,'full_decoded_WAV':str(full),'full_decoded_WAV_sha256':hashlib.sha256(full.read_bytes()).hexdigest(),'command':cmd,'windows':windows,'coverage_audio_seconds':37.78,'coverage_visual_seconds':0,'threshold':None,'interpretation':'model candidates, not independent truth; no ASR/word/emotion/mix/synchrony claims','adapter_sha256':hashlib.sha256((O/'infer.py').read_bytes()).hexdigest(),'known_controls_not_retained':True},indent=2)+'\n')
print('Cormac source/4 nonoverlapping windows frozen BEFORE Cormac scores; no added padding')

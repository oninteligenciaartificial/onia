from pathlib import Path
import json,hashlib,wave,subprocess,uuid,math
O=Path(__file__).resolve().parent;R=O.parent
t=json.loads((O/'transfer-receipt.json').read_text());assert t['complete']
expected=['dd47543edc46efbf26fe6fdff2e2493323d3fcb689cdc4b4377b30a742f2dba6','43b8932a8e13ec8aeaa1fb3808d2ac8dece4c4ad4e9d55c4a762166e7b80053a']
actual=[x.split('=')[-1] for x in t['remux']['streamhash_output'].splitlines()];assert actual==expected
(O/'payload-comparison.json').write_text(json.dumps({'expected_PC_streamhashes':expected,'actual_remux_streamhashes':actual,'video_and_audio_payloads_match_PC':True,'container_file_hash_identical':t['remux']['file_hash_matches_original'],'comparison_scope':'ordered compressed stream payload hashes; not container bytes/timestamps equality'},indent=2)+'\n')
source=O/'DfaLyn7Rorf-remux.mp4';assert hashlib.sha256(source.read_bytes()).hexdigest()==t['remux']['sha256']
full=O/(uuid.uuid4().hex+'.wav');cmd=['ffmpeg','-hide_banner','-loglevel','error','-threads','1','-filter_threads','1','-i',str(source),'-map','0:a:0','-vn','-ar','32000','-ac','1','-c:a','pcm_s16le','-threads','1',str(full)]
subprocess.run(cmd,check=True)
with wave.open(str(full),'rb') as w:
 assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,32000)
 count=w.getnframes();raw=w.readframes(count)
assert abs(count/32000-37.545011)<1
windows=[]
for i,start in enumerate(range(0,count,320000)):
 end=min(start+320000,count);case=f'aidan{i}';path=O/(uuid.uuid4().hex+'.wav')
 with wave.open(str(path),'wb') as w:w.setparams((1,2,32000,0,'NONE','not compressed'));w.writeframes(raw[start*2:end*2])
 entry={'case':case,'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'samples':end-start,'rate':32000,'duration':(end-start)/32000,'interval_source_seconds':[start/32000,end/32000],'padding':0}
 (O/(case+'-input.json')).write_text(json.dumps(entry,indent=2)+'\n');windows.append(entry)
csvpath=R/'panns-setup-v3/runtime-home/panns_data/class_labels_indices.csv';assert hashlib.sha256(csvpath.read_bytes()).hexdigest()=='cdd1049833c4b86127c2773ac0d14a2754b6a6d0d1798002ed5c66e699708429'
freeze={'reel':'DfaLyn7Rorf','source_account':'murphmaxxing','source_person':'Aidan Murphy','source_remux_sha256':t['remux']['sha256'],'PC_payloads_match':True,'container_duration_seconds':float(t['remux']['probe']['format']['duration']),'decoded_samples':count,'decoded_duration_seconds':count/32000,'full_decoded_WAV':str(full),'full_decoded_WAV_sha256':hashlib.sha256(full.read_bytes()).hexdigest(),'command':cmd,'windows':windows,'inputs':{x['case']:x for x in windows},'CSV':{'installed_path':str(csvpath),'sha256':'cdd1049833c4b86127c2773ac0d14a2754b6a6d0d1798002ed5c66e699708429','Speech_index':0,'Music_index':137},'checkpoint_sha256':'dd3b4043a87d4ec13df8082c0fcfee3fb5084151808e47e060987a95eabdd142','adapter_sha256':hashlib.sha256((O/'infer.py').read_bytes()).hexdigest(),'params':{'CPU':1,'workers':1,'batch':1,'AS_GiB':3,'CPU_wall_seconds_per_entry':120,'reserve_GiB':6,'VAD':False,'rate':32000,'model':'Cnn14_DecisionLevelMax','interpolate':'nearest'},'coverage':'entire decoded audio sample range, no VAD/crop/padding; visual analysis0','interpretation':'auxiliary uncalibrated scores, no emotion/music-absence/validated-event or integral AV claims','ASR':'omitted: coordinator confirms PC small CPU+Silero already performed; no Cloud installation or ASR'}
(O/'input-manifest.json').write_text(json.dumps(freeze,indent=2)+'\n');(O/'input-freeze.json').write_text(json.dumps(freeze,indent=2)+'\n');print('payloads match PC; all PCM samples frozen before PANNs output',count,count/32000,len(windows))

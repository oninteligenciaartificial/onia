import hashlib, json, os, resource, sys, time
from faster_whisper import WhisperModel, decode_audio
from faster_whisper.vad import get_speech_timestamps
p=sys.argv[1]
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
t=time.monotonic(); m=WhisperModel('/work/model',device='cpu',compute_type='int8',cpu_threads=2,num_workers=1)
audio=decode_audio(p,sampling_rate=16000)
intervals=get_speech_timestamps(audio)
segments,info=m.transcribe(p,beam_size=5,vad_filter=True,language=sys.argv[2],word_timestamps=True)
segs=[{'start':s.start,'end':s.end,'text':s.text,'words':[{'word':w.word,'start':w.start,'end':w.end} for w in (s.words or [])]} for s in segments]
r={'input_sha256':sha(p),'language':info.language,'elapsed_seconds':round(time.monotonic()-t,3),'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'cpu_seconds':resource.getrusage(resource.RUSAGE_SELF).ru_utime+resource.getrusage(resource.RUSAGE_SELF).ru_stime,'vad':True,'speech_intervals_samples':intervals,'sample_rate':16000,'duration_seconds':len(audio)/16000,'text':''.join(s['text'] for s in segs).strip(),'segments':segs}
out='/work/output/'+os.path.basename(p)+'.vad.json'
with open(out,'x',encoding='utf-8') as f: json.dump(r,f,ensure_ascii=False,indent=2)
print(json.dumps(r,ensure_ascii=False))


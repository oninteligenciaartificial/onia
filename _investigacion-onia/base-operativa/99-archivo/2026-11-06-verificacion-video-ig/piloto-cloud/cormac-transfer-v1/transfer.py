from pathlib import Path
import json,hashlib,time,urllib.request,urllib.error,urllib.parse,subprocess,sys
O=Path('/workspace/onia-av-pilot-20261106/cormac-transfer-v1')
deadline=time.monotonic()+110;MAX=64*1024**2
def save(x):(O/'transfer-receipt.json').write_text(json.dumps(x,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
state={'piece':'DfWLWspIruU','anonymous':True,'automatic_retries':0,'tracks':[],'complete':False}
def run(cmd):
 t=deadline-time.monotonic()
 if t<=0:raise TimeoutError('deadline')
 return subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=t).stdout.decode()
try:
 for i,spec in enumerate(json.loads((O/'private-spec.json').read_text())):
  parsed=urllib.parse.urlsplit(spec['url']);queryless=urllib.parse.urlunsplit((parsed.scheme,parsed.netloc,parsed.path,'',''))
  entry={'format_id':spec['format_id'],'host':parsed.hostname,'url_without_query_sha256':hashlib.sha256(queryless.encode()).hexdigest(),'bytes':0,'complete':False}
  state['tracks'].append(entry);save(state)
  assert parsed.scheme=='https' and parsed.hostname=='scontent-lim1-1.cdninstagram.com'
  dest=O/f'track-{i}.mp4';headers=dict(spec['headers']);headers['Accept-Encoding']='identity'
  req=urllib.request.Request(spec['url'],headers=headers)
  with urllib.request.urlopen(req,timeout=min(20,max(.1,deadline-time.monotonic()))) as response:
   entry['http_status']=response.status;entry['content_length']=response.headers.get('Content-Length')
   if response.status!=200:raise ValueError('unexpected_status')
   if response.headers.get('Content-Encoding','identity').lower()!='identity':raise ValueError('encoding')
   if entry['content_length'] and int(entry['content_length'])>MAX:raise ValueError('oversize_header')
   with open(dest,'xb') as f:
    while True:
     if time.monotonic()>=deadline:raise TimeoutError('deadline')
     b=response.read(min(262144,MAX-entry['bytes']+1))
     if not b:break
     if entry['bytes']+len(b)>MAX:raise ValueError('oversize_body')
     f.write(b);entry['bytes']+=len(b)
   if entry['content_length'] and entry['bytes']!=int(entry['content_length']):raise ValueError('short_body')
  entry.update(sha256=sha(dest),closed_file_hash=True,complete=True);save(state)
 remux=O/'DfWLWspIruU-remux.mp4'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-threads','2','-i',str(O/'track-0.mp4'),'-i',str(O/'track-1.mp4'),'-map','0:v:0','-map','1:a:0','-c','copy',str(remux)]
 run(cmd)
 probe=json.loads(run(['ffprobe','-v','error','-count_packets','-show_entries','format=duration,size:stream=index,codec_type,codec_name,width,height,sample_rate,channels,duration,nb_read_packets','-of','json',str(remux)]))
 expected=['ae7c9a7097a0f7d3d262bcde444569bb10789b76a4afd5176f209e0ed505b403','681f83302315ebb9819b9b72b1a0ebaa1f3967a1afe615fdfdf982ded8c4ab49']
 hashes=run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(remux),'-map','0:v:0','-map','0:a:0','-c','copy','-f','streamhash','-hash','sha256','-'])
 actual=[line.strip().split('=')[-1] for line in hashes.splitlines() if '=SHA' in line]
 # ffmpeg emits e.g. 0,v,SHA256=<digest>; compare both ordered tracks.
 actual=[line.strip().split('=')[-1] for line in hashes.splitlines() if 'SHA256=' in line]
 state.update(complete=True,remux={'bytes':remux.stat().st_size,'sha256':sha(remux),'probe':probe,'streamhash_output':hashes,'expected_original_streamhashes':expected,'both_streams_match_original':actual==expected,'original_file_sha256':'9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e','file_hash_matches_original':sha(remux)=='9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e','container_variant':'local remux, not assumed byte-identical original','command':cmd})
except BaseException as exc:
 state.update(error_type=type(exc).__name__,http_error_status=getattr(exc,'code',None),safe_error='exception text suppressed to avoid signed URLs; no retry')
 for i,x in enumerate(state['tracks']):
  p=O/f'track-{i}.mp4'
  if p.exists():x.update(bytes=p.stat().st_size,sha256=sha(p),closed_file_hash=True)
save(state);print(json.dumps(state),flush=True)
sys.exit(0 if state['complete'] else 1)

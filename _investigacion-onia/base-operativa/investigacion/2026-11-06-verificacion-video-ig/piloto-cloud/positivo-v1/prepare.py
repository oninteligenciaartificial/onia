from pathlib import Path
import hashlib,json,subprocess,uuid,wave,sys
R=Path('/workspace/onia-av-pilot-20261106'); O=R/'positivo-v1'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
def save(n,x): (O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
prior=R/'resume-negativo-v1'; assert sha(prior/'manifest.json')=='578e54307938649f9362d5b711841f30305e6fefd80eb540c60d4a207f93a031'
assert json.loads((prior/'workspace-marker.json').read_text())['id']=='2f701954-b26e-43e7-9110-ca296ee87f09'
for x in json.loads((prior/'manifest.json').read_text())['files']:
 p=prior/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
freeze=json.loads((R/'review-v2/source-freeze.json').read_text())
for x in freeze['sources']:
 p=R/'runtime'/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
for x in json.loads((R/'negativo-v1/runtime-libraries.json').read_text())['own_elfs']:
 p=Path(x['real_path']);assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
for x in json.loads((prior/'weights-receipt.json').read_text())['verified']:
 p=R/'negativo-v1/weights'/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
sys.path.insert(0,str(R/'review-v2'));import supervisor
policy=supervisor.Policy(os_thread_cap=16,tree_bytes=16*1024**3)
snapshot=supervisor.snapshot(R);assert supervisor.guard(snapshot,policy) is None
save('continuity.json',{'prior_marker_verified':True,'manifest21_verified':True,'sources_libraries_weights_verified':True,'resources':snapshot})
commands=[]
def run(cmd,**kw):
 commands.append(cmd);return subprocess.run(cmd,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,**kw).stdout
voice=O/(uuid.uuid4().hex+'.wav')
run(['ffmpeg','-hide_banner','-loglevel','error','-filter_threads','2','-f','lavfi','-i','flite=text=one two:voice=kal16','-ar','16000','-ac','1','-c:a','pcm_s16le','-threads','2',str(voice)])
with wave.open(str(voice),'rb') as w:
 assert (w.getnchannels(),w.getsampwidth(),w.getframerate())==(1,2,16000)
 samples=w.getnframes();data=w.readframes(samples)
assert 0<samples<=32000, f'voice too long: {samples}/16000 seconds; no truncation'
blocks=(samples+15999)//16000;count=blocks+1
data+=bytes((count*16000-samples)*2)
opaque=uuid.uuid4().hex;signals=O/opaque;signals.mkdir();prefix=str(signals/(uuid.uuid4().hex+'_'));files=[]
for i in range(count):
 wav=Path(prefix+f'{i:04d}.wav')
 with wave.open(str(wav),'wb') as w:w.setparams((1,2,16000,0,'NONE','not compressed'));w.writeframes(data[i*32000:(i+1)*32000])
 rgb=bytearray([255])*(224*224*3)
 for y in range(224):
  for x in range(224):
   inside=(24<=x<96 and 76<=y<148) if i<blocks else ((x-160)**2+(y-112)**2<=36**2)
   if inside:rgb[(y*224+x)*3:(y*224+x)*3+3]=bytes((255,0,0) if i<blocks else (0,0,255))
 ppm=signals/(uuid.uuid4().hex+'.ppm');ppm.write_bytes(b'P6\n224 224\n255\n'+rgb)
 jpg=Path(prefix+f'{i:04d}.jpg')
 run(['ffmpeg','-hide_banner','-loglevel','error','-threads','2','-i',str(ppm),'-frames:v','1','-c:v','mjpeg','-pix_fmt','yuvj444p','-threads','2',str(jpg)])
 decoded=run(['ffmpeg','-hide_banner','-loglevel','error','-threads','2','-i',str(jpg),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-threads','2','pipe:1']);assert len(decoded)==224*224*3
 for p,mod in [(wav,'audio'),(jpg,'image'),(ppm,'generator-source')]:files.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p),'modality':mod,'pts':i,'duration':1})
save('control-manifest.json',{'opaque_id':opaque,'prefix':prefix,'chunks':count,'files':files,'voice_source':{'path':str(voice),'bytes':voice.stat().st_size,'sha256':sha(voice),'samples':samples,'duration':samples/16000},'commands':commands})
save('control-truth.json',{'authority':'generator truth, NOT human audition','speech':'one two','voice':'included flite kal16','voice_samples':samples,'voice_blocks':blocks,'first_blocks':'white image, red square left; complete speech then zero padding','last_chunk':'white image, blue circle right; exactly16000 zero samples','no_truncation':True,'not_passed_to_model':True})
print(json.dumps({'samples':samples,'duration':samples/16000,'chunks':count,'resources':snapshot}))

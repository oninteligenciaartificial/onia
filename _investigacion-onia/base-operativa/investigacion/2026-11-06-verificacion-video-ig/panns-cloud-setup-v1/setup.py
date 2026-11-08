"""One bounded official-binary closure, offline installation, explicit checkpoint."""
from pathlib import Path
import sys,json,time,urllib.request,urllib.parse,hashlib,zipfile,email,subprocess,os
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.version import Version
from pip._vendor.packaging.tags import sys_tags
from pip._vendor.packaging.utils import parse_wheel_filename,canonicalize_name
O=Path(__file__).resolve().parent;W=O/'wheels';W.mkdir();START=time.monotonic();LIMIT=1610612736
state={'stage':'official_metadata','network_start_monotonic':START,'download_bytes_total':0,'download_cap_bytes':LIMIT,'automatic_retries':0,'packages':{},'complete':False};tags=set(sys_tags())
def save():(O/'setup-receipt.json').write_text(json.dumps(state,indent=2)+'\n')
def remaining():
 t=295-(time.monotonic()-START)
 if t<=0:raise TimeoutError('global_preparation_deadline')
 return t
def fetch(url,dest=None,expected_size=None,expected_sha=None,expected_md5=None):
 assert urllib.parse.urlsplit(url).hostname in {'pypi.org','files.pythonhosted.org','download.pytorch.org','zenodo.org'}
 remaining();req=urllib.request.Request(url,headers={'Accept-Encoding':'identity'})
 h=hashlib.sha256();md=hashlib.md5();size=0;pieces=[];handle=open(dest,'xb') if dest else None
 try:
  with urllib.request.urlopen(req,timeout=min(20,remaining())) as response:
   if response.status!=200:raise ValueError('HTTP_status')
   if response.headers.get('Content-Encoding','identity')!='identity':raise ValueError('HTTP_encoding')
   announced=response.headers.get('Content-Length')
   if announced and int(announced)+state['download_bytes_total']>LIMIT:raise ValueError('aggregate_download_budget_header')
   while True:
    remaining();b=response.read(262144)
    if not b:break
    state['download_bytes_total']+=len(b);size+=len(b)
    if state['download_bytes_total']>LIMIT:raise ValueError('aggregate_download_budget')
    if expected_size and size>expected_size:raise ValueError('oversize_download')
    h.update(b);md.update(b)
    if handle:handle.write(b)
    else:
     if size>16*1024**2:raise ValueError('metadata_size')
     pieces.append(b)
   if announced and size!=int(announced):raise ValueError('short_HTTP_body')
 finally:
  if handle:handle.close()
 if expected_size and size!=expected_size:raise ValueError('expected_size_mismatch')
 if dest:
  h=hashlib.sha256();md=hashlib.md5()
  with open(dest,'rb') as f:
   while b:=f.read(1048576):h.update(b);md.update(b)
 if expected_sha and h.hexdigest()!=expected_sha:raise ValueError('SHA256_mismatch')
 if expected_md5 and md.hexdigest()!=expected_md5:raise ValueError('MD5_mismatch')
 save();return {'bytes':size,'sha256':h.hexdigest(),'md5':md.hexdigest(),'closed_file_hash':bool(dest)} if dest else b''.join(pieces)
def compatible(f):
 if not f['filename'].endswith('.whl') or f.get('yanked'):return False
 try:return bool(set(parse_wheel_filename(f['filename'])[3])&tags)
 except Exception:return False
pins={'torch':'2.5.1+cpu','numpy':'1.26.4','librosa':'0.10.2.post1','torchlibrosa':'0.1.0','panns-inference':'0.1.1'}
queue=[Requirement(n+'=='+v) for n,v in pins.items()];constraints={};selected={};requirements=[]
try:
 # First network action begins the sole preparation clock. Only official CPU index.
 import re,html
 index=fetch('https://download.pytorch.org/whl/cpu/torch/').decode()
 links=[html.unescape(x) for x in re.findall(r'href="([^"]+)"',index)]
 torch_link=next(x for x in links if 'torch-2.5.1%2Bcpu-cp312-cp312-linux_x86_64.whl' in x or 'torch-2.5.1+cpu-cp312-cp312-linux_x86_64.whl' in x)
 torch_url=urllib.parse.urljoin('https://download.pytorch.org/whl/cpu/torch/',torch_link);torch_sha=urllib.parse.parse_qs(urllib.parse.urlsplit(torch_url).fragment)['sha256'][0];torch_url=torch_url.split('#',1)[0]
 while queue:
  remaining();req=queue.pop(0)
  if req.marker and not req.marker.evaluate({'extra':''}):continue
  name=canonicalize_name(req.name);requirements.append(str(req));constraints.setdefault(name,[]).append(req.specifier)
  if name.startswith('nvidia-') or name in {'torchaudio','torchvision'}:raise ValueError('unexpected_extra_or_CUDA_dependency:'+name)
  if name in selected:
   if not all(Version(selected[name]['version']) in s for s in constraints[name]):raise ValueError('closure_conflict:'+name)
   continue
  if name=='torch':version=pins[name];url=torch_url;expected=torch_sha;size=None;filename=urllib.parse.unquote(url.rsplit('/',1)[1])
  else:
   j=json.loads(fetch('https://pypi.org/pypi/'+name+'/json'))
   versions=[pins[name]] if name in pins else sorted((v for v in j['releases'] if not Version(v).is_prerelease and all(Version(v) in s for s in constraints[name])),key=Version,reverse=True)
   found=None
   for version in versions:
    candidates=[f for f in j['releases'].get(version,[]) if compatible(f)]
    if candidates:found=candidates[0];break
   if not found:raise ValueError('no_compatible_official_binary:'+name)
   url=found['url'];filename=found['filename'];expected=found['digests']['sha256'];size=found['size']
  state['stage']='download_wheel:'+name;save()
  p=W/filename;facts=fetch(url,p,size,expected)
  with zipfile.ZipFile(p) as z:
   metadata=email.message_from_bytes(z.read(next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'))))
   assert canonicalize_name(metadata['Name'])==name and Version(metadata['Version'])==Version(version)
   requires=metadata.get_all('Requires-Dist',[])
   if name=='panns-inference':
    assert facts['sha256']=='97f6b56b6c9467cf00e21f041e1f88933188c65c1b5ca64eeb3c92e37fb27fc2'
    license_name=next(n for n in z.namelist() if n.endswith('LICENSE.MIT'));license_bytes=z.read(license_name)
    assert hashlib.sha256(license_bytes).hexdigest()=='ebf680a8816f15b367981f48d461369a9848a29c9ce644c249bbcbaa4831a01f'
    (O/'LICENSE.MIT').write_bytes(license_bytes);state['license_anomaly']='Original MIT file retains Google/Angular2010-2017 notice exactly; not corrected.'
  item={'version':version,'url':url,'filename':filename,'requires':requires,**facts};selected[name]=item;state['packages'][name]=item
  queue.extend(Requirement(s) for s in requires);save()
 state['stage']='closure_validate_offline';save()
 # Independent pip resolver checks METADATA using ONLY collected local binaries.
 cmd=[sys.executable,'-B','-m','pip','--isolated','install','--dry-run','--ignore-installed','--no-index','--only-binary=:all:','--find-links',str(W),'--report',str(O/'pip-closure.json')]+[n+'=='+v for n,v in pins.items()]
 subprocess.run(cmd,check=True,timeout=remaining())
 (O/'closure-lock.json').write_text(json.dumps({'direct_pins':pins,'selected':selected,'requirements_evaluated':requirements,'validated_before_install':True},indent=2)+'\n')
 state['stage']='create_isolated_venv';save();venv=O/'venv'
 subprocess.run([sys.executable,'-B','-m','venv','--without-pip',str(venv)],check=True,timeout=remaining())
 state['stage']='offline_install';save()
 subprocess.run([sys.executable,'-B','-m','pip','--isolated','--python',str(venv/'bin/python'),'install','--no-index','--no-deps','--no-compile']+[str(W/x['filename']) for x in selected.values()],check=True,timeout=remaining())
 state['stage']='checkpoint_download';save();path=O/'Cnn14_DecisionLevelMax_mAP=0.385.pth'
 state['checkpoint']=fetch('https://zenodo.org/records/3987831/files/Cnn14_DecisionLevelMax_mAP%3D0.385.pth?download=1',path,327428481,expected_md5='70539c43c18b6a289b3199c503a82c5a')
 state['checkpoint'].update(source='Zenodo3987831 version3',license='CC BY4.0',path=str(path));state['stage']='complete';state['complete']=True
except BaseException as exc:
 state.update(error_type=type(exc).__name__,safe_error=str(exc) if isinstance(exc,(ValueError,AssertionError)) else 'exception text suppressed; see stage and status',http_status=getattr(exc,'code',None))
finally:
 state['elapsed_seconds']=time.monotonic()-START;save();print('SETUP_RESULT '+json.dumps(state),flush=True)
sys.exit(0 if state['complete'] else 1)

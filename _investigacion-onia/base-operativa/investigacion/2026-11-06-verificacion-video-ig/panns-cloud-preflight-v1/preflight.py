"""Offline metadata-only preflight. No framework import, install or inference."""
from pathlib import Path
import datetime,hashlib,json,os,resource,shutil,subprocess,sys
R=Path('/workspace/onia-av-pilot-20261106');O=R/'panns-preflight-v1'
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  while b:=f.read(1048576):h.update(b)
 return h.hexdigest()
manifests={'positivo-v1':'51cabe47a664da9741ca62d229a185067cb424dc4854e164a6a480370d86bdec','resume-negativo-v1':'578e54307938649f9362d5b711841f30305e6fefd80eb540c60d4a207f93a031','positivo-v2':'436a1d14ced05f07c0b9dd3f0116e45630445aa7a265b252774b6622ee8f9ca1','cormac-transfer-v1':'ea9b35ddc2f005c896f16527497c11439745b73e3c99459bbd2f250464f529f5'}
checks=[]
for d,expected in manifests.items():
 p=R/d;assert sha(p/'manifest.json')==expected
 m=json.loads((p/'manifest.json').read_text())
 for x in m['files']:
  f=p/x['path'];assert f.stat().st_size==x['bytes'] and sha(f)==x['sha256']
 checks.append({'directory':d,'manifest_sha256':expected,'files_verified':len(m['files'])})
assert json.loads((R/'positivo-v2/workspace-marker.json').read_text())['id']=='580e4821-b090-49de-8f16-9995512ccfe3'
head=subprocess.check_output(['git','-C','/workspace/onia','rev-parse','HEAD'],text=True).strip()
status=subprocess.check_output(['git','-C','/workspace/onia','status','--porcelain'],text=True)
assert head=='e55812ce1bc8ef798fb370257ba887d07acccc53' and not status
save('continuity.json',{'marker':'580e4821-b090-49de-8f16-9995512ccfe3','manifests':checks,'onia_HEAD':head,'onia_status':status,'workspace':str(R),'minicpm_weights_or_runtime_not_opened':True})
fixtures=[]
for d in ['negativo-v1','positivo-v1']:
 c=json.loads((R/d/'control-manifest.json').read_text());truth=R/d/'control-truth.json'
 files=list(c['files'])
 if 'voice_source' in c:files.append(c['voice_source'])
 verified=[]
 for x in files:
  p=Path(x['path']);assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256']
  verified.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':x['sha256']})
 assert truth.is_file()
 fixtures.append({'fixture':d,'used_by':'positivo-v2' if d=='positivo-v1' else 'accepted negative','manifest_sha256':sha(R/d/'control-manifest.json'),'truth_sha256':sha(truth),'truth':json.loads(truth.read_text()),'files':verified,'regenerated':False,'human_audition':False})
save('fixtures.json',fixtures)
mem={}
for line in Path('/proc/meminfo').read_text().splitlines():
 k,v=line.split(':',1)
 if k in ['MemTotal','MemAvailable','SwapTotal','SwapFree']:mem[k+'_bytes']=int(v.split()[0])*1024
levels=[]
group=Path('/proc/self/cgroup').read_text().strip().split('0::',1)[1]
for line in Path('/proc/self/mountinfo').read_text().splitlines():
 before,after=line.split(' - ',1)
 if after.split()[0]!='cgroup2':continue
 f=before.split();mount_root,mount=f[3],Path(f[4]);leaf=mount/group[len(mount_root):].lstrip('/')
 while True:
  values={'path':str(leaf)}
  for name in ['memory.max','memory.current','memory.swap.max','memory.swap.current','cpu.max','cpuset.cpus','cpuset.cpus.effective','cpuset.mems.effective']:
   p=leaf/name
   try:values[name]=p.read_text().strip()
   except OSError:values[name]=None
  levels.append(values)
  if leaf==mount:break
  leaf=leaf.parent
 break
reserves=[mem['MemAvailable_bytes']];quotas=[]
for l in levels:
 if l['memory.max'] not in [None,'max']:reserves.append(max(0,int(l['memory.max'])-int(l['memory.current'])))
 if l['cpu.max'] and not l['cpu.max'].startswith('max'):a,b=l['cpu.max'].split();quotas.append(int(a)/int(b))
free=shutil.disk_usage(R).free;reserve=min(reserves)
own=[];other=0;uid=os.getuid()
for p in Path('/proc').glob('[0-9]*'):
 try:
  if p.stat().st_uid!=uid:other+=1;continue
  raw=p.joinpath('stat').read_text();v=raw.rsplit(')',1)[1].split();comm=raw.split('(',1)[1].rsplit(')',1)[0]
  own.append({'pid':int(p.name),'comm':comm,'state':v[0],'ppid':int(v[1]),'pgid':int(v[2]),'threads':int(v[17]),'rss_bytes':int(v[21])*os.sysconf('SC_PAGE_SIZE')})
 except (OSError,ValueError,IndexError):pass
pending=[p for p in own if p['pgid'] in [17437,17490,16953]]
resources={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'host_memory':mem,'cgroup_visible_levels':levels,'hidden_ancestors':'not observable; no claims about host ancestors beyond namespace','reserve_bytes':reserve,'required_reserve_bytes':6*1024**3,'reserve_pass':reserve>=6*1024**3,'cpu_logical_host':os.cpu_count(),'parent_affinity':sorted(os.sched_getaffinity(0)),'visible_cpu_quota_min_cores':min(quotas) if quotas else None,'disk_free_bytes':free,'parent_rlimit_as':resource.getrlimit(resource.RLIMIT_AS),'parent_rlimit_cpu':resource.getrlimit(resource.RLIMIT_CPU),'future_entry_policy':{'AS_virtual_bytes_per_process':3*1024**3,'cpu_seconds_per_entry':120,'wall_seconds_per_entry':120,'affinity_CPUs':1,'batch':1,'reserve_bytes':6*1024**3,'swap_addition':False,'policy_applied_now':False},'own_uid_process_metadata':own,'other_uid_process_count_only':other,'previous_groups_pending':pending,'no_process_signals_sent':True}
save('resources.json',resources)
assert resources['reserve_pass'] and levels and not pending and os.sched_getaffinity(0)
interpreters=[];seen=set()
candidates=[Path(sys.executable),Path('/usr/bin/python3'),Path('/usr/local/bin/python3')]
venvs=[]
for root in [Path('/workspace'),Path('/opt/codex/runtimes')]:
 for directory,dirs,files in os.walk(root,followlinks=False):
  dirs[:]=[d for d in dirs if d not in {'.git','.aws','.codex','.agents','node_modules','runtime','build-v2','cmake-local','weights','site-packages','__pycache__'}]
  if 'pyvenv.cfg' in files:
   v=Path(directory);venvs.append(str(v));candidates.append(v/'bin/python')
code="import importlib.metadata as m,json,sys; names=['torch','torchaudio','numpy','librosa','torchlibrosa','panns-inference']; out={};\nfor n in names:\n try:\n  d=m.distribution(n);out[n]={'version':d.version,'location':str(d.locate_file('')),'requires':d.requires}\n except m.PackageNotFoundError:out[n]=None\nprint(json.dumps({'executable':sys.executable,'version':sys.version.split()[0],'prefix':sys.prefix,'base_prefix':sys.base_prefix,'packages':out,'frameworks_imported':False}))"
for p in candidates:
 if not p.exists() or str(p.resolve()) in seen:continue
 seen.add(str(p.resolve()))
 try:
  result=subprocess.run([str(p),'-B','-c',code],check=True,capture_output=True,text=True,timeout=15)
  interpreters.append(json.loads(result.stdout))
 except Exception as e:interpreters.append({'path':str(p),'error_type':type(e).__name__})
save('versions.json',{'venv_search_roots':['/workspace','/opt/codex/runtimes'],'venvs_found':venvs,'interpreters':interpreters,'method':'stdlib importlib.metadata only; no framework import, pip or network','CPU_compatibility':'metadata only; CPU kernel availability/runtime ABI not executed or certified'})
save('receipt.json',{'phase':'PANNs phase1a preflight only','continuity':'four manifests and current marker verified','onia_HEAD':head,'git_clean':not status,'fixtures':'negative gray/silence and complete flite one two positive fixture hashes/bytes/truth verified; positive-v2 reuses positive-v1','reserve_bytes':reserve,'reserve_required_bytes':6*1024**3,'resource_preflight_pass':resources['reserve_pass'],'visible_cgroup_levels':len(levels),'disk_free_bytes':free,'previous_process_groups_pending':len(pending),'python_interpreters':len(interpreters),'details':['continuity.json','fixtures.json','resources.json','versions.json'],'not_performed':['framework import','package install/download','checkpoint download','inference','regeneration','runtime rebuild','signals to processes','ONIA/configuration/publication changes'],'limits_for_next_entry':'AS3GiB virtual per process, CPU/wall120s, CPU1,batch1,reserve>=6GiB; no swap added. Not applied to parent; no child inference started.','status':'metadata_preflight_complete_not_runtime_validation'})
print((O/'receipt.json').read_text())

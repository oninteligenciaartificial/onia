"""Own-group CPU1 supervisor; stdlib only; never changes parent limits."""
from pathlib import Path
import os,sys,time,json,resource,signal,subprocess,selectors,hashlib
R=Path('/workspace/onia-av-pilot-20261106');O=R/'panns-setup-v2';G=1024**3
def snapshot():
 mem=int(next(x.split()[1] for x in Path('/proc/meminfo').read_text().splitlines() if x.startswith('MemAvailable:')))*1024
 cg=Path('/sys/fs/cgroup');maximum=(cg/'memory.max').read_text().strip();current=int((cg/'memory.current').read_text())
 import shutil
 return {'mem_available':mem,'memory_max':maximum,'memory_current':current,'reserve':min(mem,int(maximum)-current) if maximum!='max' else mem,'disk_free':shutil.disk_usage(R).free}
def run(name,command,wall,cpu):
 assert 0<wall<=300 and type(cpu) is int and 0<cpu<=wall
 s=snapshot();assert s['reserve']>=6*G and s['disk_free']>=30*G
 dest=O/name;dest.mkdir();start=time.monotonic();affinity=[min(os.sched_getaffinity(0))]
 report={'command':command,'policy':{'AS_virtual_bytes_per_process':3*G,'CPU_seconds_per_process':cpu,'wall_seconds':wall,'affinity':affinity,'workers':1,'batch':1,'reserve_bytes':6*G,'swap_added':False,'log_bytes':262144,'output_cut_bytes':1048576},'before':s,'reason':None,'sampled_max_group_RSS':0,'sampled_max_threads':0,'output_bytes':0,'log_bytes':0,'parent_before':{'AS':resource.getrlimit(resource.RLIMIT_AS),'CPU':resource.getrlimit(resource.RLIMIT_CPU),'affinity':sorted(os.sched_getaffinity(0))},'RSS_scope':'sampled sum, not exact peak; shared pages may double count'}
 spec={'command':command,'cpu':cpu,'affinity':affinity};(dest/'spec.json').write_text(json.dumps(spec))
 p=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'child',str(dest/'spec.json')],start_new_session=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 report['pgid']=p.pid;interrupted=[];old=signal.getsignal(signal.SIGTERM)
 signal.signal(signal.SIGTERM,lambda n,f:interrupted.append(n))
 sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ);ticks=os.sysconf('SC_CLK_TCK');seen_cpu={}
 def members():
  out=[]
  for f in Path('/proc').glob('[0-9]*/stat'):
   try:
    v=f.read_text().rsplit(')',1)[1].split()
    if int(v[2])==p.pid:
     out.append({'pid':int(f.parent.name),'state':v[0],'rss':int(v[21])*os.sysconf('SC_PAGE_SIZE'),'threads':int(v[17])});seen_cpu[(f.parent.name,v[19])]=(int(v[11])+int(v[12]))/ticks
   except (OSError,ValueError,IndexError):pass
  return out
 try:
  with open(dest/'output.log','xb') as log:
   while True:
    for key,_ in sel.select(.1):
     b=os.read(key.fd,65536)
     if b:
      report['output_bytes']+=len(b);keep=b[:max(0,262144-report['log_bytes'])];log.write(keep);report['log_bytes']+=len(keep)
     else:sel.unregister(p.stdout)
    m=members();s=snapshot();report['last_resources']=s
    report['sampled_max_group_RSS']=max(report['sampled_max_group_RSS'],sum(x['rss'] for x in m))
    report['sampled_max_threads']=max(report['sampled_max_threads'],sum(x['threads'] for x in m))
    elapsed=time.monotonic()-start
    reason='SIGTERM' if interrupted else 'wall_timeout' if elapsed>=wall else 'reserve_guard' if s['reserve']<6*G else 'disk_guard' if s['disk_free']<30*G else 'output_limit' if report['output_bytes']>1048576 else None
    if reason:
     report['reason']=reason;break
    if p.poll() is not None and not sel.get_map():
     report['reason']='exited' if p.returncode==0 else 'child_failure';break
   live=[x for x in members() if x['state']!='Z']
   if live:
    if p.poll() is not None and report['reason']=='exited':report['reason']='incomplete_descendants'
    try:os.killpg(p.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    deadline=time.monotonic()+1
    while time.monotonic()<deadline and any(x['state']!='Z' for x in members()):time.sleep(.05)
    if any(x['state']!='Z' for x in members()):
     try:os.killpg(p.pid,signal.SIGKILL)
     except ProcessLookupError:pass
   p.wait(timeout=5)
 finally:
  signal.signal(signal.SIGTERM,old);sel.close();p.stdout.close()
  report.update(exit_code=p.poll(),wall_seconds=time.monotonic()-start,pending_live=[x for x in members() if x['state']!='Z'],pending_zombies=[x for x in members() if x['state']=='Z'],sampled_CPU_seconds=sum(seen_cpu.values()),CPU_scope='sampled process times; transient exited processes may be missed; all descendants constrained to same single CPU so global wall also bounds aggregate CPU',parent_after={'AS':resource.getrlimit(resource.RLIMIT_AS),'CPU':resource.getrlimit(resource.RLIMIT_CPU),'affinity':sorted(os.sched_getaffinity(0))},parent_SIGTERM_restored=signal.getsignal(signal.SIGTERM)==old)
  (dest/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 return report
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='child':
 spec=json.loads(Path(sys.argv[2]).read_text());resource.setrlimit(resource.RLIMIT_AS,(3*G,3*G));resource.setrlimit(resource.RLIMIT_CPU,(spec['cpu'],spec['cpu']));os.sched_setaffinity(0,spec['affinity'])
 for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[k]='1'
 os.environ['PYTHONDONTWRITEBYTECODE']='1'
 os.execv(spec['command'][0],spec['command'])

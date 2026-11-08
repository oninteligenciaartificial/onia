"""Linux/WSL single-stage runner: owned PGID, resource limits and receipts."""
import hashlib, json, os, resource, signal, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
name, *command = sys.argv[1:]
assert command and name.replace('-', '').replace('_', '').isalnum()
out = ROOT / 'stages' / name
out.mkdir(parents=True, exist_ok=False)
cpus = sorted(os.sched_getaffinity(0))[:2]
os.sched_setaffinity(0, cpus)
start = time.monotonic()
pid = os.fork()
if pid == 0:
    os.setsid()
    resource.setrlimit(resource.RLIMIT_AS, (3*1024**3, 3*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
    os.environ['OMP_THREAD_LIMIT'] = '2'
    os.environ['OMP_NUM_THREADS'] = '2'
    (out/'effective.json').write_text(json.dumps({'pid':os.getpid(),'pgid':os.getpgrp(),'affinity':sorted(os.sched_getaffinity(0)), 'AS':resource.getrlimit(resource.RLIMIT_AS),'CPU':resource.getrlimit(resource.RLIMIT_CPU)}))
    for fd, target in [(1,out/'stdout.log'),(2,out/'stderr.log')]:
        stream = os.open(target, os.O_CREAT|os.O_EXCL|os.O_WRONLY, 0o600)
        os.dup2(stream,fd); os.close(stream)
    os.chdir(ROOT)
    os.execvp(command[0], command)

def members():
    found=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdigit(): continue
        try:
            stat=(p/'stat').read_text(); fields=stat[stat.rindex(')')+2:].split()
            if int(fields[2]) == pid:
                found.append({'pid':int(p.name),'state':fields[0], 'rss':int(fields[21])*os.sysconf('SC_PAGE_SIZE')})
        except (OSError,ValueError,IndexError): pass
    return found

max_rss=0; reason='exited'; killed=[]
try:
    while True:
        max_rss=max(max_rss,sum(p['rss'] for p in members()))
        done,status,usage=os.wait4(pid,os.WNOHANG)
        if done: break
        if time.monotonic()-start > 120:
            reason='wall_timeout';killed=members();os.killpg(pid,signal.SIGKILL)
            _,status,usage=os.wait4(pid,0);break
        time.sleep(.1)
finally:
    live=[p for p in members() if p['state']!='Z']
    if live:
        os.killpg(pid,signal.SIGKILL)
        if reason=='exited': reason='incomplete_group_shutdown'
    report={'stage':name,'command':command,'exit_code':os.waitstatus_to_exitcode(status),'reason':reason,'wall_seconds':time.monotonic()-start,'cpu_seconds_leader':usage.ru_utime+usage.ru_stime,'max_rss_leader_kib':usage.ru_maxrss,'sampled_group_rss_bytes':max_rss,'affinity':cpus,'AS_bytes_per_process':3*1024**3,'CPU_seconds_per_process':120,'wall_limit_seconds':120,'limits_scope':'AS/CPU per process; group RSS sampled, not aggregate hard cap','killed':killed,'pending_live':[p for p in members() if p['state']!='Z']}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
sys.exit(0 if report['exit_code']==0 and reason=='exited' else 1)

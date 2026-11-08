import json,os,subprocess,sys,time,shutil
container=sys.argv[1]; command=sys.argv[2:]; start=time.monotonic(); minmem=10**12; mindisk=10**12; maxusage=0; reason=None
p=subprocess.Popen(['docker','exec',container,'timeout','120s']+command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
while p.poll() is None:
 with open('/proc/meminfo') as f: mem={a.split(':')[0]:int(a.split()[1])*1024 for a in f if ':' in a and len(a.split())>1 and a.split()[1].isdigit()}
 minmem=min(minmem,mem['MemAvailable']); mindisk=min(mindisk,shutil.disk_usage('/').free)
 try:
  val=subprocess.check_output(['docker','stats','--no-stream','--format','{{.MemUsage}}',container],text=True,timeout=4).strip()
 except Exception: val='unknown';reason='stats unavailable'
 if minmem<6*1024**3: reason='host available memory below 6GiB'
 if mindisk<30*1024**3: reason='host disk below 30GiB'
 if time.monotonic()-start>135:reason='supervisor timeout'
 if reason:
  subprocess.run(['docker','stop','--time','2',container],timeout=15);break
 time.sleep(1)
out,err=p.communicate(timeout=15)
r={'container':container,'exit':p.returncode,'reason':reason,'min_available_bytes':minmem,'min_disk_free_bytes':mindisk,'last_docker_memory':val,'elapsed':time.monotonic()-start,'stdout':out,'stderr':err}
print(json.dumps(r))

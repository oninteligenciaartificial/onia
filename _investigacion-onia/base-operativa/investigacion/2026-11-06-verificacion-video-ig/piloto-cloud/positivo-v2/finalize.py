from pathlib import Path
import json,hashlib,re,subprocess,uuid,shutil
R=Path('/workspace/onia-av-pilot-20261106');O=R/'positivo-v2'
def save(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((O/'model-report.json').read_text());log=(O/'model-output.log').read_text()
tele={}
for name in ['SAMPLER','BUDGET','CHUNK','RESULT','ERROR']:
 values=[]
 for match in re.finditer('PILOT_'+name+' ',log):
  values.append(json.JSONDecoder().raw_decode(log[match.end():])[0])
 tele[name.lower()]=values
save('model-telemetry.json',tele)
response=None
if '  Count:  2\n' in log:
 response=log.split('  Count:  2\n',1)[1].split('PILOT_CHUNK ',1)[0]
 (O/'model-response.txt').write_text(response)
for d,h in [('positivo-v1','51cabe47a664da9741ca62d229a185067cb424dc4854e164a6a480370d86bdec'),('resume-negativo-v1','578e54307938649f9362d5b711841f30305e6fefd80eb540c60d4a207f93a031')]:
 p=R/d;assert digest(p/'manifest.json')==h
 for x in json.loads((p/'manifest.json').read_text())['files']:
  f=p/x['path'];assert f.stat().st_size==x['bytes'] and digest(f)==x['sha256']
for x in json.loads((R/'review-v2/source-freeze.json').read_text())['sources']:
 p=R/'runtime'/x['path'];assert p.stat().st_size==x['bytes'] and digest(p)==x['sha256']
for x in json.loads((R/'negativo-v1/runtime-libraries.json').read_text())['own_elfs']:
 p=Path(x['real_path']);assert p.stat().st_size==x['bytes'] and digest(p)==x['sha256']
old=(R/'positivo-v1/model_driver.py').read_text();corrected=(O/'model_driver.py').read_text()
assert corrected==old.replace("prompt=(ROOT/'model-prompt.txt')","prompt=(ROOT/'negativo-v1/model-prompt.txt')")
assert not (R/'positivo-v1/model-invocation.json').exists()
save('result.json',{'status':report['reason'],'exit_code':report['exit_code'],'real_model_execs':1 if (O/'model-invocation.json').exists() else 0,'previous_real_positive_execs':0,'one_attempt_lock':True,'wall_seconds':report['elapsed_seconds'],'sampled_max_rss_bytes':report['sampled_max_group_rss_bytes'],'RSS_not_exact_peak':True,'actual_cpu_seconds':None,'sampled_max_os_threads':report['sampled_max_group_os_threads'],'response_literal':response,'telemetry':'model-telemetry.json','semantic_acceptance':'integration/reviewer decide; exit0 alone does not accept','old_cuts_sources_libraries_verified_unchanged':True,'prompt_only_source_change_verified':True,'fixture_reused_unchanged':True,'receipt_routing':'run_driver.py routes exclusive model-invocation.json write from old positive-v1 to positive-v2; no other I/O changes','cleanup_live':report['cleanup_pending_live'],'cleanup_zombies':report['cleanup_pending_zombies'],'parent_limits_restored':report['parent_limits_unchanged'],'onia_status':subprocess.check_output(['git','-C','/workspace/onia','status','--porcelain'],text=True),'next':'Stop; no Cormac execution, retries or further controls.'})
save('workspace-marker.json',{'id':str(uuid.uuid4()),'previous':'5e7d0227-88e7-4aa9-837f-ec2530d8e6ef','status':'one_real_positive_attempt_complete','durability':'observed only, verify manifests next turn'})
save('closing-resources.json',{'disk_free_bytes':shutil.disk_usage(R).free,'memory_cgroup':report['last_snapshot'],'limits':'unchanged; see model-report.json','actual_cpu_seconds':'not captured'})
print(json.dumps({'reason':report['reason'],'exit':report['exit_code'],'response':response,'telemetry':tele},ensure_ascii=False,indent=2))

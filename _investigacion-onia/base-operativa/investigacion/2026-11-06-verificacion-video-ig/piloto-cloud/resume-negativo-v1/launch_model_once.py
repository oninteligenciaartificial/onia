from pathlib import Path
import dataclasses,json,sys
ROOT=Path('/workspace/onia-av-pilot-20261106')
sys.path.insert(0,str(ROOT/'review-v2'))
import supervisor
OUT=ROOT/'resume-negativo-v1'
transfer=json.loads((ROOT/'run-resume-negative-transfer-v1/report.json').read_bytes())
assert transfer['reason']=='exited' and transfer['exit_code']==0 and not transfer['cleanup_pending_live']
assert json.loads((OUT/'range-receipt.json').read_bytes())['complete']
policy=dataclasses.replace(supervisor.Policy(),wall_seconds=600,os_thread_cap=16,tree_bytes=16*1024**3)
assert supervisor.guard(supervisor.snapshot(ROOT),policy) is None
report=supervisor.run([sys.executable,str(OUT/'run_existing_driver.py')],'resume-negative-model-v1',policy)
print(json.dumps(report,indent=2))
sys.exit(0 if report['reason']=='exited' else 1)

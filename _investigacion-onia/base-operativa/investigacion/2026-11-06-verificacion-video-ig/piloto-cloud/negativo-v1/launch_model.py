from pathlib import Path
import dataclasses
import json
import sys
ROOT=Path('/workspace/onia-av-pilot-20261106')
sys.path.insert(0,str(ROOT/'review-v2'))
import supervisor
p=dataclasses.replace(supervisor.Policy(),wall_seconds=600,os_thread_cap=16,tree_bytes=16*1024**3)
r=supervisor.run([sys.executable,str(ROOT/'negativo-v1/model_driver.py')],'negative-model-v1',p)
print(json.dumps(r,indent=2))
sys.exit(0 if r['reason']=='exited' else 1)

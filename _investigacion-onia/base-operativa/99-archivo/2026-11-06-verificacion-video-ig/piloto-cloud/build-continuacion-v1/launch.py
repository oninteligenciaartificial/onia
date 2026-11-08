"""One run ID, same frozen supervisor v2, explicit continuation budget."""
from pathlib import Path
import dataclasses
import json
import sys

ROOT=Path('/workspace/onia-av-pilot-20261106')
sys.path.insert(0,str(ROOT/'review-v2'))
import supervisor

policy=dataclasses.replace(supervisor.Policy(),wall_seconds=300,
                           tree_bytes=1024**3,os_thread_cap=16)
report=supervisor.run([sys.executable,str(ROOT/'build-continuacion-v1/driver.py')],
                      'build-continuacion-v1',policy)
print(json.dumps(report,indent=2))
sys.exit(0 if report['reason']=='exited' else 1)

"""Exactly one authorized incremental build; no configure, clean or target execution."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path('/workspace/onia-av-pilot-20261106')
OUT=ROOT/'build-continuacion-v1'
freeze=json.loads((ROOT/'review-v2/source-freeze.json').read_bytes())
def verify_sources():
    for item in freeze['sources']:
        data=(ROOT/'runtime'/item['path']).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
verify_sources()
command=[str(ROOT/'cmake-local/cmake/data/bin/cmake'),'--build',str(ROOT/'build-v2'),
         '--target','llama-omni-single-test-omni','-j2']
print('BUILD_COMMAND '+json.dumps(command),flush=True)
result=subprocess.run(command)
print('BUILD_EXIT '+str(result.returncode),flush=True)
verify_sources()
if result.returncode: sys.exit(result.returncode)
binary=ROOT/'build-v2/bin/llama-omni-single-test-omni'
receipt={'path':str(binary),'bytes':binary.stat().st_size,
         'sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
         'executed':False,'frozen_sources_verified_after_build':True}
(OUT/'binary.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('BUILD_ARTIFACT '+json.dumps(receipt),flush=True)

"""Authorized build only. Never executes the target or any model."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

ROOT=Path('/workspace/onia-av-pilot-20261106')
freeze=json.loads((ROOT/'review-v2/source-freeze.json').read_text())
for entry in freeze['sources']:
    assert hashlib.sha256((ROOT/'runtime'/entry['path']).read_bytes()).hexdigest()==entry['sha256']
cmake=ROOT/'cmake-local/cmake/data/bin/cmake'
commands=[
    [str(cmake),'--version'],
    [str(cmake),'-S',str(ROOT/'runtime'),'-B',str(ROOT/'build-v2'),
     '-DCMAKE_BUILD_TYPE=Release','-DGGML_CUDA=OFF','-DGGML_METAL=OFF',
     '-DENABLE_COREML=OFF','-DGGML_OPENMP=OFF','-DGGML_BLAS=OFF',
     '-DLLAMA_CURL=OFF','-DLLAMA_BUILD_TESTS=OFF','-DLLAMA_BUILD_SERVER=OFF'],
    [str(cmake),'--build',str(ROOT/'build-v2'),'--target','llama-omni-single-test-omni','-j2']
]
for cmd in commands:
    print('BUILD_COMMAND '+json.dumps(cmd),flush=True)
    result=subprocess.run(cmd)
    print('BUILD_EXIT '+str(result.returncode),flush=True)
    if result.returncode: sys.exit(result.returncode)
for entry in freeze['sources']:
    assert hashlib.sha256((ROOT/'runtime'/entry['path']).read_bytes()).hexdigest()==entry['sha256']
binary=ROOT/'build-v2/bin/llama-omni-single-test-omni'
print('BUILD_ARTIFACT '+json.dumps({'path':str(binary),'bytes':binary.stat().st_size,
      'sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'executed':False}),flush=True)

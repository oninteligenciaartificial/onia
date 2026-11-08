"""Descarga reproducible por rangos de dos pesos oficiales; verifica SHA-256."""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
DEST=BASE/'operacion/referentes-20261105/audio/eureka-preflight'
FILES={
 '1':('model-00001-of-00002.safetensors',4996447616,'3ab5beaaa05d67bed1afe2776a2e7623ccc0329c07c52a9745c98bdc50eda28a'),
 '2':('model-00002-of-00002.safetensors',1333409252,'b3a07bf63d4a4d87c988163cb2f095d98b5a14f86fc4de028051186510d3cb60')}
key=sys.argv[1]
name,total,expected=FILES[key]
partial=DEST/(name+'.partial')
chunk=DEST/(name+'.chunk')
progress=OUT/('eureka-descarga-'+key+'.json')
url='https://huggingface.co/cslys1999/Eureka-Audio-Instruct/resolve/219761da53c9c6c5900a84a723d88ccc29db66d3/'+name
step=64*1024*1024
done=partial.stat().st_size if partial.exists() else 0
if done>total or (done%step and done!=total): raise SystemExit('Archivo parcial con tamaño inesperado; no se modifica')
started=time.monotonic()
while done<total:
    end=min(done+step-1,total-1)
    run=subprocess.run(['curl.exe','--location','--fail','--silent','--show-error','--max-time','180',
        '--speed-limit','1024','--speed-time','30','--range',f'{done}-{end}',
        '--output',str(chunk),'--write-out','%{http_code} %{size_download}',url],
        capture_output=True,text=True)
    observed=chunk.stat().st_size if chunk.exists() else 0
    result={'file':name,'expected_bytes':total,'downloaded_before_chunk':done,'range':[done,end],
            'curl_exit':run.returncode,'http_and_bytes':run.stdout,'bytes_observed':observed,
            'elapsed_s':round(time.monotonic()-started,2),'completed':False}
    progress.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    if run.returncode or not run.stdout.startswith('206 ') or observed!=end-done+1:
        print(json.dumps({**result,'stderr':run.stderr},ensure_ascii=False),flush=True); sys.exit(1)
    with partial.open('ab') as dst,chunk.open('rb') as src:
        while True:
            b=src.read(1024*1024)
            if not b: break
            dst.write(b)
    done+=observed
    print(json.dumps({'file':name,'downloaded':done,'total':total,'elapsed_s':round(time.monotonic()-started,2)}),flush=True)
digest=hashlib.sha256()
with partial.open('rb') as source:
    for block in iter(lambda:source.read(1024*1024),b''): digest.update(block)
actual=digest.hexdigest()
if actual!=expected:
    progress.write_text(json.dumps({'file':name,'completed':False,'sha256':actual,'expected':expected,'error':'hash mismatch'},indent=2)+'\n',encoding='utf-8')
    raise SystemExit('SHA-256 no coincide; no se adopta el archivo')
os.replace(partial,DEST/name)
progress.write_text(json.dumps({'file':name,'bytes':total,'sha256':actual,'completed':True,'elapsed_s':round(time.monotonic()-started,2)},indent=2)+'\n',encoding='utf-8')

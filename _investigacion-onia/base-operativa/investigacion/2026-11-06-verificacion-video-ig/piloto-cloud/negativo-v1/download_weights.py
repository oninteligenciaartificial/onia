"""One streaming attempt per authorized fixed-revision artifact. Never load a model."""
from pathlib import Path
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

ROOT=Path('/workspace/onia-av-pilot-20261106/negativo-v1')
BASE='https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf/resolve/db25077c33951fe163b42986fba0132e279872a2/'
FILES=[
 ('MiniCPM-o-4_5-Q4_K_M.gguf',5026714400,'1237a97ee081b8abebc47aa7dad565701e8f5f904cdc92f6723ac4281bbc0932'),
 ('audio/MiniCPM-o-4_5-audio-F16.gguf',660167904,'d5b188ac7feaf98e17175c3f9bd14bf269301bfd187439fdaa3e3a494fc32ef7'),
 ('vision/MiniCPM-o-4_5-vision-F16.gguf',1095113184,'1453678cc4e4fe18de241952962e234f265cb8dda780773526103ab8ba82f421')]
receipts=[]
started=time.monotonic()
try:
    for name,expected,want in FILES:
        target=ROOT/'weights'/name
        target.parent.mkdir(parents=True,exist_ok=True)
        part=target.with_name(target.name+'.part')
        if target.exists() or part.exists(): raise FileExistsError('no overwrite or automatic resume')
        count=0
        print(json.dumps({'event':'begin','path':name,'expected_bytes':expected}),flush=True)
        # urllib follows official redirects; never persist/print the signed redirect URL.
        with urllib.request.urlopen(BASE+name,timeout=25) as response,open(part,'xb') as output:
            length=response.headers.get('Content-Length')
            if length is not None and int(length)!=expected: raise ValueError('header_size_mismatch')
            while True:
                if time.monotonic()-started>=590: raise TimeoutError('phase_deadline')
                chunk=response.read(min(1024*1024,expected-count+1))
                if not chunk: break
                if count+len(chunk)>expected: raise ValueError('size_maximum_exceeded')
                output.write(chunk); count+=len(chunk)
        if count!=expected or part.stat().st_size!=expected: raise ValueError('short_transfer')
        # Required second pass: hash the CLOSED file, bounded chunks; no read_bytes.
        digest=hashlib.sha256()
        with open(part,'rb') as closed_file:
            while chunk:=closed_file.read(1024*1024):
                if time.monotonic()-started>=590: raise TimeoutError('phase_deadline_during_hash')
                digest.update(chunk)
        got=digest.hexdigest()
        if got!=want: raise ValueError('sha256_mismatch')
        part.rename(target)  # same file, no full-file duplicate
        receipts.append({'path':name,'bytes':count,'sha256':got,'closed_file_hash_verified':True})
        (ROOT/'weights-receipt.json').write_text(json.dumps({'revision':'db25077c33951fe163b42986fba0132e279872a2','verified':receipts,'complete':len(receipts)==3},indent=2)+'\n')
        print(json.dumps({'event':'verified',**receipts[-1]}),flush=True)
except BaseException as exc:
    safe={'error_type':type(exc).__name__,'http_status':getattr(exc,'code',None),
          'verified_files':len(receipts),'automatic_retry':False,
          'detail':'transfer or integrity failed; signed URLs and exception text intentionally omitted'}
    (ROOT/'download-failure.json').write_text(json.dumps(safe,indent=2)+'\n')
    print(json.dumps(safe),flush=True)
    sys.exit(1)

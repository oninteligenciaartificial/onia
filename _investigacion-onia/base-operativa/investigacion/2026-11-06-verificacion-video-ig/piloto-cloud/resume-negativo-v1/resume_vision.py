"""ONE exact HTTP Range continuation; preserve historical receipts and prefix."""
from pathlib import Path
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT=Path('/workspace/onia-av-pilot-20261106')
OUT=ROOT/'resume-negativo-v1'
PART=ROOT/'negativo-v1/weights/vision/MiniCPM-o-4_5-vision-F16.gguf.part'
FINAL=PART.with_name(PART.name.removesuffix('.part'))
START=171966464
TOTAL=1095113184
PREFIX_SHA='fb749ab559817ef0a472e94104808e131f18f049fe7b22063f91c568aabfa8e0'
EXPECTED_SHA='1453678cc4e4fe18de241952962e234f265cb8dda780773526103ab8ba82f421'
URL='https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf/resolve/db25077c33951fe163b42986fba0132e279872a2/vision/MiniCPM-o-4_5-vision-F16.gguf'
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while b:=f.read(1024*1024):h.update(b)
    return h.hexdigest()
class ResumeError(Exception): pass
state={'start_bytes':START,'expected_total_bytes':TOTAL,'expected_prefix_sha256':PREFIX_SHA,
       'expected_final_sha256':EXPECTED_SHA,'bytes_added':0,'automatic_retries':0,
       'request_range':f'bytes={START}-{TOTAL-1}','request_accept_encoding':'identity',
       'stage':'precheck','complete':False}
try:
    if FINAL.exists() or PART.stat().st_size!=START or digest(PART)!=PREFIX_SHA:
        raise ResumeError('preexisting_partial_or_final_mismatch')
    original=PART.stat()
    state['prefix_verified_before']=True
    state['stage']='http_headers'
    request=urllib.request.Request(URL,headers={'Range':state['request_range'],'Accept-Encoding':'identity'})
    with urllib.request.urlopen(request,timeout=25) as response:
        state['http_status']=response.status
        state['content_range']=response.headers.get('Content-Range')
        state['content_length']=response.headers.get('Content-Length')
        state['content_encoding']=response.headers.get('Content-Encoding','identity')
        if response.status!=206: raise ResumeError('http_206_required_no_append')
        match=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',state['content_range'] or '')
        if not match or tuple(map(int,match.groups()))!=(START,TOTAL-1,TOTAL):
            raise ResumeError('invalid_content_range_no_append')
        if state['content_length']!=str(TOTAL-START): raise ResumeError('invalid_content_length_no_append')
        if state['content_encoding'].lower().strip()!='identity': raise ResumeError('compressed_response_no_append')
        state['headers_validated_before_append']=True
        state['stage']='append'
        with open(PART,'r+b') as f:
            now=os.fstat(f.fileno())
            if (now.st_dev,now.st_ino,now.st_size)!=(original.st_dev,original.st_ino,START):
                raise ResumeError('partial_changed_before_append')
            f.seek(0,os.SEEK_END)
            while True:
                remaining=TOTAL-START-state['bytes_added']
                b=response.read(min(1024*1024,remaining+1))
                if not b: break
                if len(b)>remaining: raise ResumeError('response_exceeds_exact_total')
                f.write(b);state['bytes_added']+=len(b)
        if PART.stat().st_size!=TOTAL or state['bytes_added']!=TOTAL-START:
            raise ResumeError('short_range_transfer')
    state['stage']='closed_file_final_hash'
    state['actual_final_sha256']=digest(PART)
    if state['actual_final_sha256']!=EXPECTED_SHA: raise ResumeError('final_sha256_mismatch')
    PART.rename(FINAL)
    state.update(stage='complete',complete=True,closed_file_hash_verified=True,final_bytes=FINAL.stat().st_size)
    historical=json.loads((ROOT/'negativo-v1/weights-receipt.json').read_bytes())
    assert len(historical['verified'])==2 and not historical['complete']
    combined={'revision':historical['revision'],'verified':historical['verified']+[
        {'path':'vision/MiniCPM-o-4_5-vision-F16.gguf','bytes':TOTAL,'sha256':EXPECTED_SHA,
         'closed_file_hash_verified':True}],'complete':True,
         'historical_receipt_preserved':'negativo-v1/weights-receipt.json'}
    (OUT/'weights-receipt.json').write_text(json.dumps(combined,indent=2)+'\n')
except BaseException as exc:
    state.update(error_type=type(exc).__name__,http_error_status=getattr(exc,'code',None),
                 safe_reason=str(exc) if isinstance(exc,ResumeError) else 'non_protocol_exception_text_suppressed',
                 retained_bytes=PART.stat().st_size if PART.exists() else (FINAL.stat().st_size if FINAL.exists() else None))
    (OUT/'range-receipt.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(state),flush=True);sys.exit(1)
(OUT/'range-receipt.json').write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps(state),flush=True)

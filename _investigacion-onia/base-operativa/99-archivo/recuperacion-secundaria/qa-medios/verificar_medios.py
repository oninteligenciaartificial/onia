"""QA read-only incremental de MP4: metadata, SHA y decode integral secuencial.
Sólo escribe en qa-medios; no altera medios ni subtítulos.
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[3]
MEDIA=BASE/'operacion/referentes-20261105/secundarios'
IDS=['anrAaNvbp4M','oFYznV9EYPg','4jWLq8Gn_4Y','SVHKZkD1r_A','c4S0EJAdL5I','oZ9UKXve3Dk']

def save(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def hash_file(path):
    h=hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()

def last_progress(path):
    blocks=[]; block={}
    for line in path.read_text(encoding='utf-8',errors='replace').splitlines():
        key,sep,value=line.partition('=')
        if sep:
            block[key]=value
            if key=='progress':
                blocks.append(block);block={}
    return blocks[-1] if blocks else block

summary={'scope':'metadata, hashes and full technical decode only; not viewing/listening',
         'date':'2026-11-05 America/Caracas',
         'execution':'sequential, one ffmpeg process; decoder/output/filter thread options all set to 1',
         'ffmpeg_version':subprocess.check_output(['ffmpeg','-version'],text=True).splitlines()[0],
         'results':[]}
existing_path=OUT/'resultados.json'
if existing_path.exists():
    summary=json.loads(existing_path.read_text(encoding='utf-8'))
existing_ids=[r['id'] for r in summary['results']]
if len(existing_ids)!=len(set(existing_ids)):
    raise ValueError('IDs duplicados en evidencia existente; no modificar.')
if any(not r['full_decode_completed'] for r in summary['results']):
    raise ValueError('Hay resultado previo fallido; requiere revisión, no repetir automáticamente.')
prior_elapsed=summary.get('elapsed_s',0)
prior_canonical=json.dumps(summary['results'],sort_keys=True,ensure_ascii=False).encode('utf-8')
preserved_digest=hashlib.sha256(prior_canonical).hexdigest()
pending=[ident for ident in IDS if ident not in existing_ids]
if not pending:
    print(json.dumps({'already_complete':True,'preserved_ids':existing_ids}),flush=True)
    raise SystemExit(0)
summary['last_run']={'preserved_ids':existing_ids,'preserved_records_canonical_sha256':preserved_digest,
                     'requested_ids':pending,'decoded_ids':[],'previous_elapsed_s':prior_elapsed}
started=time.monotonic()
for ident in IDS:
    if ident in existing_ids:
        continue
    path=MEDIA/ident/(ident+'.mp4')
    before_stat=path.stat()
    start=time.monotonic()
    digest=hash_file(path)
    probe_cmd=['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]
    probe=subprocess.run(probe_cmd,capture_output=True,text=True)
    if probe.returncode:
        raise RuntimeError(probe.stderr)
    meta=json.loads(probe.stdout)
    save(ident+'.ffprobe.json',meta)
    error_file=OUT/(ident+'.decode.stderr.txt')
    progress_file=OUT/(ident+'.decode.progress.txt')
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-xerror','-nostats',
         '-threads','1','-filter_threads','1','-filter_complex_threads','1',
         '-i',str(path),'-map','0:v:0?','-map','0:a:0?',
         '-fps_mode','passthrough','-threads','1','-progress','pipe:1','-f','null','-']
    print(json.dumps({'id':ident,'stage':'decode_started','bytes':before_stat.st_size}),flush=True)
    decode_start=time.monotonic()
    with progress_file.open('w',encoding='utf-8') as out, error_file.open('w',encoding='utf-8') as err:
        result=subprocess.run(cmd,stdout=out,stderr=err)
    decode_time=round(time.monotonic()-decode_start,3)
    stderr=error_file.read_text(encoding='utf-8',errors='replace')
    progress=last_progress(progress_file)
    after_stat=path.stat()
    record={'id':ident,'path':str(path),'bytes':before_stat.st_size,'sha256':digest,
            'source_stat_unchanged':before_stat.st_size==after_stat.st_size and before_stat.st_mtime_ns==after_stat.st_mtime_ns,
            'format_duration':meta['format'].get('duration'),
            'streams':[{k:s[k] for k in ['index','codec_type','codec_name','width','height','sample_rate','channels','start_time','duration','time_base','duration_ts','nb_frames','avg_frame_rate'] if k in s} for s in meta['streams']],
            'probe_exit_code':probe.returncode,'probe_stderr':probe.stderr,
            'decode_command':cmd,'decode_exit_code':result.returncode,'decode_stderr':stderr,
            'decode_elapsed_s':decode_time,'full_decode_completed':result.returncode==0 and not stderr.strip() and progress.get('progress')=='end',
            'last_progress':progress,'total_elapsed_s':round(time.monotonic()-start,3),
            'viewed':False,'listened':False}
    save(ident+'.qa.json',record)
    summary['results'].append(record)
    summary['last_run']['decoded_ids'].append(ident)
    summary['last_run']['elapsed_s']=round(time.monotonic()-started,3)
    summary['all_completed']=len(summary['results'])==len(IDS)
    summary['all_pass']=summary['all_completed'] and all(r['full_decode_completed'] and r['source_stat_unchanged'] for r in summary['results'])
    summary['elapsed_s']=round(prior_elapsed+time.monotonic()-started,3)
    save('resultados.json',summary)
    print(json.dumps({'id':ident,'decode_exit':result.returncode,'decode_s':decode_time,'decoded_frames':progress.get('frame'),'pass':record['full_decode_completed']}),flush=True)
print(json.dumps({'all_pass':summary['all_pass'],'elapsed_s':summary['elapsed_s']}),flush=True)

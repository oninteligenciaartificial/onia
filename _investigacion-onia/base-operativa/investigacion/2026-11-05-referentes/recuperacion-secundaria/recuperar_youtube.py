"""Recuperación pública acotada a seis IDs; sin config/cookies/credenciales.

metadata: registra datos y catálogo de subtítulos, sin URLs temporales de CDN.
download: máximo720p, subtítulos es/en originales/automáticos disponibles.
No instala ni carga modelos. Artefactos grandes sólo en carpeta ignorada.
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/secundarios'
IDS=['anrAaNvbp4M','oFYznV9EYPg','4jWLq8Gn_4Y','SVHKZkD1r_A','c4S0EJAdL5I','oZ9UKXve3Dk']
COMMON=['yt-dlp','--ignore-config','--no-cache-dir','--no-playlist','--socket-timeout','20','--retries','0','--no-progress','--js-runtimes','node','--no-remote-components']


def write(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def existing(name):
    path=OUT/name
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else []


def upsert(rows,row):
    return [r for r in rows if r['id']!=row['id']]+[row]


def metadata(ids):
    rows=existing('youtube-metadata.json')
    for vid in ids:
        start=time.monotonic()
        url='https://www.youtube.com/watch?v='+vid
        proc=subprocess.run(COMMON+['--skip-download','--dump-single-json',url],capture_output=True,text=True,encoding='utf-8',timeout=150)
        row={'id':vid,'url':url,'exit':proc.returncode,'elapsed_s':round(time.monotonic()-start,3),'stderr':proc.stderr}
        if proc.returncode==0:
            info=json.loads(proc.stdout)
            for key in ['title','duration','upload_date','channel','channel_url','description','chapters','availability','language','live_status']:
                row[key]=info.get(key)
            row['subtitles']={lang:[{'ext':f.get('ext'),'name':f.get('name')} for f in formats] for lang,formats in info.get('subtitles',{}).items()}
            row['automatic_captions_languages']=list(info.get('automatic_captions',{}))
            row['formats']=[{k:f.get(k) for k in ['format_id','ext','width','height','fps','vcodec','acodec','filesize','filesize_approx']} for f in info.get('formats',[])]
        rows=upsert(rows,row)
        write('youtube-metadata.json',rows)
        print(json.dumps({k:row.get(k) for k in ['id','exit','title','duration','stderr']},ensure_ascii=False),flush=True)


def download(ids,include_subtitles=True,subtitle_languages='es.*,en.*,-live_chat'):
    result_name='youtube-downloads.json' if include_subtitles else 'youtube-media-downloads.json'
    records=existing(result_name)
    for vid in ids:
        dest=MEDIA/vid
        dest.mkdir(parents=True,exist_ok=True)
        url='https://www.youtube.com/watch?v='+vid
        cmd=COMMON+['--no-overwrites','--format','bv*[height<=720][vcodec^=avc1]+ba/b[height<=720]/bv*[height<=720]+ba',
             '--merge-output-format','mp4']
        if include_subtitles:
            cmd+=['--write-subs','--write-auto-subs','--sub-langs',subtitle_languages,'--sub-format','vtt']
        cmd+=['-o',str(dest/(vid+'.%(ext)s')),url]
        start=time.monotonic()
        proc=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',timeout=900)
        suffix='download' if include_subtitles else 'media-download'
        (OUT/(vid+'-'+suffix+'.log')).write_text(proc.stdout+'\n'+proc.stderr,encoding='utf-8')
        record={'id':vid,'url':url,'exit':proc.returncode,'elapsed_s':round(time.monotonic()-start,3),
                'files':[p.name for p in dest.iterdir() if p.is_file()]}
        records=upsert(records,record)
        write(result_name,records)
        print(json.dumps(record,ensure_ascii=False),flush=True)


if __name__=='__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    p=argparse.ArgumentParser()
    p.add_argument('mode',choices=['metadata','download','media'])
    p.add_argument('--id',choices=IDS,action='append')
    p.add_argument('--sub-langs',default='es.*,en.*,-live_chat')
    a=p.parse_args()
    if a.mode=='metadata': metadata(a.id or IDS)
    else: download(a.id or IDS,a.mode=='download',a.sub_langs)

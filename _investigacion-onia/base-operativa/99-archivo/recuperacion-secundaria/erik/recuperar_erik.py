"""Recupera una muestra ya conservada y consulta sólo la preview pública.
No cookies, login, modelos, instalación ni servicios. No guarda tokens del HTML.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import subprocess
import urllib.request
import urllib.parse

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[3]
MEDIA=BASE/'operacion/referentes-20261105/secundarios/erik'
SOURCE=BASE/'operacion/referentes-20261105/marketing/erik/hermes-introduccion-61s.mp4'
PAGE='https://cursos.eriktaveras.com/c/hermes-basico/preview/'
IFRAME='https://iframe.mediadelivery.net/embed/748625/7e37ed34-f1ee-420a-9d08-42ec67256d7e'

def write(name, data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fixed_url(url):
    p=urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme,p.netloc,p.path,'',''))

class Tracks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tracks=[]
    def handle_starttag(self,tag,attrs):
        if tag=='track':
            self.tracks.append(dict(attrs))

def probe():
    result=[]
    for url in [PAGE,IFRAME]:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0','Referer':PAGE})
            with urllib.request.urlopen(req,timeout=30) as response:
                html=response.read().decode('utf-8',errors='replace')
                parser=Tracks(); parser.feed(html)
                candidates=sorted(set(re.findall(r'https?[^\s\"\x27<>]+\.(?:vtt|srt)(?:\?[^\s\"\x27<>]*)?',html,re.I)))
                visible=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',html)
                visible=re.sub(r'<[^>]+>',' ',visible)
                visible=' '.join(visible.split())
                result.append({'url':url,'http_status':response.status,'html_chars':len(html),
                    'visible_text_excerpt':visible[:100],
                    'tracks':[dict(t,src=fixed_url(t.get('src',''))) for t in parser.tracks],
                    'subtitle_url_paths':[fixed_url(u) for u in candidates],
                    'caption_keyword_count':len(re.findall(r'caption',html,re.I)),
                    'html_persisted':False,'temporary_url_queries_persisted':False})
        except Exception as e:
            result.append({'url':url,'error':type(e).__name__+': '+str(e)})
    write('web-metadata.json',{'queried_date':'2026-11-05 America/Caracas','requests':result,
         'limit':'No track/URL found does not prove captions are unavailable in every player configuration.'})
    print(json.dumps(result,ensure_ascii=False))

def recover():
    MEDIA.mkdir(parents=True,exist_ok=True)
    dest=MEDIA/'erik-hermes-preview.mp4'
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    if not dest.exists():
        shutil.copyfile(SOURCE,dest)
    if sha(SOURCE)!=sha(dest):
        raise ValueError('La copia no coincide; no sobrescribir archivo existente.')
    metadata=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)],text=True))
    decode=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(dest),'-f','null','-'],capture_output=True,text=True)
    if decode.returncode:
        raise RuntimeError(decode.stderr)
    audio=MEDIA/'erik-hermes-asr-16k.wav'
    if not audio.exists():
        subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(dest),'-map','0:a:0','-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(audio)],check=True)
    import wave
    with wave.open(str(audio),'rb') as wav:
        wav_info={'frames':wav.getnframes(),'rate':wav.getframerate(),'channels':wav.getnchannels(),'duration_s':wav.getnframes()/wav.getframerate()}
    manifest={'source_page':PAGE,'source_iframe':IFRAME,
        'media_url_documented_by_marketing':'https://vz-35b81d4f-cdb.b-cdn.net/7e37ed34-f1ee-420a-9d08-42ec67256d7e/play_720p.mp4',
        'acquisition':'Copied from already-preserved local public-preview artifact, not downloaded again',
        'local_source':str(SOURCE),'copy_sha256_equal':True,
        'files':[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)} for p in [dest,audio]],
        'ffprobe':metadata,'audio_pcm':wav_info,
        'full_decode':{'exit_code':decode.returncode,'stderr':decode.stderr},
        'embedded_subtitle_streams':[s for s in metadata['streams'] if s['codec_type']=='subtitle'],
        'asr_executed_here':False,'viewed':False,'listened':False}
    write('manifest.json',manifest)
    print(json.dumps({'mp4':str(dest),'audio':str(audio),'sha256':sha(dest),'audio_pcm':wav_info,'decode_exit':decode.returncode},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['recover','probe']);a=p.parse_args()
    recover() if a.action=='recover' else probe()

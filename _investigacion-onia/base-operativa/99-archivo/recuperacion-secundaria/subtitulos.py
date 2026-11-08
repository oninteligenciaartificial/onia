"""Conserva cues de VTT automático y mide cobertura temporal, sin interpretarla."""
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/secundarios'
metadata={r['id']:r for r in json.loads((OUT/'youtube-metadata.json').read_text(encoding='utf-8'))}
TIMING=re.compile(r'^(\d+:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d+:\d{2}:\d{2}\.\d{3})')

def seconds(text):
    h,m,s=text.split(':')
    return int(h)*3600+int(m)*60+float(s)

summaries=[]
for vid in ['anrAaNvbp4M','oFYznV9EYPg','4jWLq8Gn_4Y','SVHKZkD1r_A','c4S0EJAdL5I','oZ9UKXve3Dk']:
    lang='en-orig' if vid=='SVHKZkD1r_A' else 'es-orig'
    source=MEDIA/vid/f'{vid}.{lang}.vtt'
    if not source.exists():
        print(json.dumps({'id':vid,'status':'VTT not present yet'}))
        continue
    text=source.read_text(encoding='utf-8-sig')
    cues=[]
    for block in re.split(r'\n\s*\n',text):
        lines=block.splitlines()
        for i,line in enumerate(lines):
            match=TIMING.match(line)
            if match:
                content=' '.join(lines[i+1:])
                clean=html.unescape(re.sub(r'<[^>]*>','',content)).strip()
                cues.append({'start_s':seconds(match[1]),'end_s':seconds(match[2]),'text':clean})
                break
    merged=[]
    for cue in sorted(cues,key=lambda x:x['start_s']):
        a,b=cue['start_s'],cue['end_s']
        if b<a:
            raise ValueError(f'Invalid time interval {vid}')
        if merged and a<=merged[-1][1]: merged[-1][1]=max(merged[-1][1],b)
        else: merged.append([a,b])
    words=[]
    for cue in cues:
        new=cue['text'].split()
        overlap=0
        for n in range(min(80,len(words),len(new)),0,-1):
            if words[-n:]==new[:n]: overlap=n; break
        words.extend(new[overlap:])
    gaps=[]
    end=0
    duration=metadata[vid]['duration']
    actual_duration=None
    video=MEDIA/vid/f'{vid}.mp4'
    if video.exists():
        probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration','-of','json',str(video)],text=True))
        actual_duration=float(probe['streams'][0]['duration'])
        duration=actual_duration
    for a,b in merged:
        if a>end: gaps.append({'start_s':end,'end_s':a,'duration_s':round(a-end,3)})
        end=b
    if end<duration: gaps.append({'start_s':end,'end_s':duration,'duration_s':round(duration-end,3)})
    result={'id':vid,'source_vtt':source.relative_to(BASE).as_posix(),
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'language':lang,
        'type':'YouTube automatic captions, not human transcript',
        'video_duration_metadata_s':metadata[vid]['duration'],'video_duration_actual_s':actual_duration,'cue_count':len(cues),
        'first_cue_s':cues[0]['start_s'] if cues else None,
        'last_cue_s':max(c['end_s'] for c in cues) if cues else None,
        'cue_union_s':round(sum(b-a for a,b in merged),3),
        'cue_union_within_video_s':round(sum(max(0,min(b,duration)-max(a,0)) for a,b in merged),3),
        'last_cue_overrun_s':round(max(0,max(c['end_s'] for c in cues)-duration),3),
        'gaps':gaps,
        'scope':'timestamps measure caption presence, not completeness of spoken content or acoustic listening',
        'cues':cues}
    (OUT/f'{vid}-subtitulos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (OUT/f'{vid}-texto-derivado.txt').write_text('Texto derivado de VTT automático: se retira solapamiento de palabras; cotejar cues/raw antes de citar.\n\n'+' '.join(words)+'\n',encoding='utf-8')
    summaries.append({k:result[k] for k in ['id','source_vtt','source_sha256','language','video_duration_metadata_s','video_duration_actual_s','cue_count','first_cue_s','last_cue_s','cue_union_s','cue_union_within_video_s','last_cue_overrun_s']})
(OUT/'subtitulos-cobertura.json').write_text(json.dumps(summaries,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(summaries,indent=2,ensure_ascii=False))

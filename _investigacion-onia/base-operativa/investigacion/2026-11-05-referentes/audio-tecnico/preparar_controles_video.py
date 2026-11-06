"""Prepara controles locales para un analizador que sólo acepta video.

No sube archivos ni inicia análisis. Cada clip muestra el mismo gris sin texto;
la única variable es la pista. Los nombres no revelan la respuesta esperada.
"""
import hashlib
import json
import subprocess
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/audio'
cases=[('a','control-silencio.wav',0,'silencio: ninguna voz, música o efecto'),
       ('b','control-tono440.wav',0,'tono constante 440Hz: sin voz'),
       ('c','control-voz.wav',0,'voz sintética inglesa conocida; número seven; silencio al final'),
       ('d','pedro-original-pcm24.wav',2.3,'fragmento real Pedro 2.3–8.3; descripción acústica aún sin validar')]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(
        ['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

# Sólo se reemplazan estos cuatro derivados, nunca una fuente o un enlace.
media_root=MEDIA.resolve(strict=True)
targets={MEDIA/f'probe-{key}.mp4' for key,_,_,_ in cases}
for dest in targets:
    if dest.is_symlink() or dest.resolve().parent!=media_root:
        raise ValueError('Destino fuera de la carpeta de audio o enlazado: '+str(dest))
    if dest.parent.resolve()!=BASE.resolve()/'operacion'/'referentes-20261105'/'audio':
        raise ValueError('La carpeta de audio resuelve fuera de la base autorizada.')
untouched_before={p.name:sha(p) for p in MEDIA.iterdir() if p.is_file() and p not in targets}
records=[]
for key,source,offset,expected in cases:
    dest=MEDIA/f'probe-{key}.mp4'
    source_probe=probe(MEDIA/source)
    source_audio=next(s for s in source_probe['streams'] if s['codec_type']=='audio')
    if source_audio['channels'] not in (1,2):
        raise ValueError('El control sólo admite fuentes mono o estéreo.')
    # Mono se duplica a L/R con ganancia unitaria, sin sumar canales ni aplicar
    # el downmix/upmix automático. Estéreo conserva sus dos canales originales.
    filters=['aresample=48000']
    if source_audio['channels']==1:
        filters.append('pan=stereo|c0=c0|c1=c0')
    filters.append('apad')
    cmd=['ffmpeg','-nostdin','-y','-v','error','-f','lavfi','-i','color=c=gray:s=320x180:r=1:d=6',
         '-ss',str(offset),'-i',str(MEDIA/source),'-map','0:v:0','-map','1:a:0',
         '-af',','.join(filters),'-t','6','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','aac','-ar','48000','-ac','2','-b:a','128k','-map_metadata','-1',str(dest)]
    subprocess.run(cmd,check=True)
    output_probe=probe(dest)
    output_audio=next(s for s in output_probe['streams'] if s['codec_type']=='audio')
    visual_hash=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(dest),'-map','0:v:0','-f','hash','-hash','sha256','-'],text=True).strip()
    records.append({'file':dest.relative_to(BASE).as_posix(),'bytes':dest.stat().st_size,
                    'sha256':sha(dest),
                    'decoded_video_hash':visual_hash,'source_audio':source,'source_start_s':offset,
                    'source_audio_sha256':sha(MEDIA/source),
                    'nominal_duration_s':6,'expected':expected,
                    'audio_codec':output_audio['codec_name'],'sample_rate':int(output_audio['sample_rate']),
                    'channels':output_audio['channels'],'channel_layout':output_audio.get('channel_layout'),
                    'target_bitrate_bps':128000,'reported_bitrate_bps':int(output_audio['bit_rate']),
                    'audio_filter':','.join(filters),'command':cmd})
untouched_after={p.name:sha(p) for p in MEDIA.iterdir() if p.is_file() and p not in targets}
if untouched_before!=untouched_after:
    raise RuntimeError('Cambió un archivo de medios fuera de los cuatro probes.')
result={'status':'prepared only; not uploaded or submitted',
        'same_visual_all_cases':len({r['decoded_video_hash'] for r in records})==1,
        'unchanged_other_media':untouched_before==untouched_after,
        'unchanged_other_media_sha256':untouched_after,
        'purpose':'blind controls for candidate video analysis; image cannot reveal audio content',
        'source_conversion':'H264 gray 320x180 1fps + AAC 48000Hz stereo target128k; no normalization; mono duplicated L/R at unity gain; original stereo preserved; silence pad to 6s',
        'bitrate_note':'AAC target bitrate is identical; actual bitrate varies with signal complexity, especially digital silence.',
        'blind_submission_rule':'Submit only probe-a/b/c/d.mp4 with neutral questions; never source names, expected answers or this manifest.',
        'cases':records}
(OUT/'controles-video.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({'same_visual':result['same_visual_all_cases'],'files':len(records),'bytes':sum(r['bytes'] for r in records)}))

"""Índice/manifiesto de los siete medios autorizados; sin red, modelos ni decode."""
import hashlib
import json
import os
from pathlib import Path

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
MEDIA=BASE/'operacion/referentes-20261105/secundarios'
IDS=['anrAaNvbp4M','oFYznV9EYPg','4jWLq8Gn_4Y','SVHKZkD1r_A','c4S0EJAdL5I','oZ9UKXve3Dk']

def read(path):
    return json.loads((OUT/path).read_text(encoding='utf-8-sig'))

def link(path):
    return os.path.relpath(path,OUT).replace('\\','/')

metadata={r['id']:r for r in read('youtube-metadata.json')}
subs={r['id']:r for r in read('subtitulos-cobertura.json')}
qa={r['id']:r for r in read('qa-medios/resultados.json')['results']}
erik=read('erik/manifest.json')
asr=read('erik-asr.json')
records=[]
for folder in [MEDIA/'erik',*[MEDIA/i for i in IDS]]:
    for path in sorted(folder.iterdir()):
        if path.suffix.lower() in {'.mp4','.wav','.vtt'}:
            records.append({'file':path.relative_to(BASE).as_posix(),'bytes':path.stat().st_size,
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
files={r['file']:r for r in records}
checks={'seven_mp4':len([r for r in records if r['file'].endswith('.mp4')])==7,
        'six_original_vtt':len(subs)==6,
        'six_youtube_full_decode':all(i in qa and qa[i]['full_decode_completed'] and qa[i]['decode_exit_code']==0 and not qa[i]['decode_stderr'] for i in IDS),
        'youtube_hashes_match_qa':all(i in qa and files[(MEDIA/i/(i+'.mp4')).relative_to(BASE).as_posix()]['sha256']==qa[i]['sha256'] for i in IDS),
        'erik_full_decode':erik['full_decode']['exit_code']==0 and not erik['full_decode']['stderr'],
        'erik_hash_matches':files[(MEDIA/'erik/erik-hermes-preview.mp4').relative_to(BASE).as_posix()]['sha256']==erik['files'][0]['sha256'],
        'original_vtt_hashes_match':all(files[r['source_vtt']]['sha256']==r['source_sha256'] for r in subs.values()),
        'erik_asr_input_matches':files[(MEDIA/'erik/erik-hermes-asr-16k.wav').relative_to(BASE).as_posix()]['sha256']==asr['sha256']}
manifest={'scope':'seven assigned public references only; no viewing or listening claimed',
          'date':'2026-11-05 America/Caracas','files':records,'bytes_total':sum(r['bytes'] for r in records),
          'checks':checks,'pass':all(checks.values()),'viewed':False,'listened':False}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
state=['# REF-RECUPERACION-20261105 · entrega de medios', '',
       '**5/11/2026 · America/Caracas.** '+('Extracción y verificación técnica terminadas.' if all(checks.values()) else 'Medios recuperados; QA técnica aún en curso.'),
       'Siete referencias autorizadas; sin ampliar investigación comercial. No se acredita visionado ni escucha. Higgsfield conserva su espera de autorización.', '',
       '## Índice para Video/Aprendizaje', '',
       '| Pieza/canal observado | Medio recuperado | Video real (s) | Texto recuperado |',
       '|---|---|---:|---|',
       '| Erik · preview Hermes | [MP4]('+link(MEDIA/'erik/erik-hermes-preview.mp4')+') | 61,600 | [ASR local](erik-asr.txt), entrada61,674688s; [JSON](erik-asr.json) |']
for i in IDS:
    r=metadata[i]
    duration=subs[i]['video_duration_actual_s']
    channel=r['channel']
    if i=='c4S0EJAdL5I': channel+=' · Bastian Xu en título del episodio'
    state.append(f"| {channel} · `{i}` | [MP4]({link(MEDIA/i/(i+'.mp4'))}) | {duration:.6f} | [{subs[i]['language']} VTT]({link(BASE/subs[i]['source_vtt'])}); [cues]({i}-subtitulos.json), [texto derivado]({i}-texto-derivado.txt) |")
state += ['', 'Las identidades se cotejaron por metadata: Bastian figura como invitado en un episodio de **Creators Latam**, no como canal propietario; Álvaro corresponde al canal **Alvaro Risoglio**. No es identificación visual/por voz. [Títulos, canales y URLs fuente](youtube-metadata.json).', '',
          '**Pistas de audio:** el contenedor remuxado etiqueta las seis como `eng`; no se tomó como idioma real. Un cotejo público confirmó los mismos IDs de formato que los logs en 6/6: español original es-US para San, inglés original en-US para Nick y es para Bastian/Álvaro. [Selección](idiomas-pistas.json), sin redescargar ni modificar MP4. Es metadata, no escucha.', '',
          '## Cobertura exacta y límites', '',
          '| ID | Intervalo VTT bruto (s) | Presencia de cues dentro del video (s) | Límites |',
          '|---|---:|---:|---|']
for i in IDS:
    r=subs[i]
    limits=[]
    if r['first_cue_s']>0: limits.append(f"sin cue inicial hasta {r['first_cue_s']:.3f}")
    if r['last_cue_overrun_s']>0: limits.append(f"último cue excede video {r['last_cue_overrun_s']:.3f}s")
    if r['last_cue_s']<r['video_duration_actual_s']: limits.append(f"sin cue desde {r['last_cue_s']:.3f} hasta {r['video_duration_actual_s']:.6f}")
    state.append(f"| `{i}` | {r['first_cue_s']:.3f}–{r['last_cue_s']:.3f} | {r['cue_union_within_video_s']:.3f} | {'; '.join(limits) or 'ver datos'} |")
state += ['',
    'Todos los VTT recuperados son **automáticos**, no transcripciones humanas. La unión de cues mide presencia temporal de subtítulos; no prueba que incluyan cada palabra, sonidos o música. Se conservan los intervalos brutos incluso cuando exceden el final del MP4. No se interpreta ausencia de cue como silencio. El texto derivado elimina solapamientos de palabras para lectura; cotejar cues/VTT antes de citar.', '',
    f"**Erik:** no hay subtítulos embebidos; la preview pública no expuso tracks, y el iframe respondió cuerpo403 aunque HTTP200. No se declara ausencia universal de subtítulos. Se aplicó faster-whisper small existente, CPU/int8/cuatro hilos, VAD: entrada completa{asr['duration_input_s']:.6f}s, conservada por VAD{asr['duration_after_vad_s']:.3f}s, {len(asr['segments'])} segmentos verbales de{asr['segments'][0]['start']:.2f} a{asr['segments'][-1]['end']:.2f}s; {asr['elapsed_s']:.2f}s de proceso. Sin nuevo modelo/API; no certifica el contenido de los intervalos descartados ni prosodia/mezcla.", '',
    '## Evidencia y recuperación de fallos', '',
    f"[Manifest](manifest.json): {len(records)} archivos de medios/subtítulos, {manifest['bytes_total']:,} bytes; SHA-256 y ocho verificaciones integradas. [QA de seis YouTube](qa-medios/resultados.json), [Erik](erik/manifest.json), [cobertura VTT](subtitulos-cobertura.json). Decodificación completa técnica, sin confundirla con visionado. Las diferencias entre duración de metadata redondeada, streams y PCM se conservan sin inferir desfase.", '',
    '- Se reutilizó la copia pública de Erik preservada por Marketing: SHA idéntico, sin alterar el original. Los seis YouTube se descargaron hasta720p con video H.264; no se recurrió a cookies, credenciales ni servicios.',
    '- Las traducciones adicionales recibieron429: se conservaron es/es-orig de San, se separó el medio del fallo de subtítulos y se obtuvo en-orig de Nick por una consulta de pista original distinta. Para las dos candidatas finales se pidió sólo es-orig. Sin repetir la traducción fallida.',
    '- Una consola cp1252 falló al mostrar emojis del título de Bastian después de guardar metadata válida. Se corrigió stdout a UTF-8 y se continuó con Álvaro sin repetir la consulta de Bastian.',
    '- Scripts: [recuperación](recuperar_youtube.py), [cues/cobertura](subtitulos.py), [ASR Erik](asr_erik.py), [índice/manifiesto](cerrar_recuperacion.py). Logs de descarga y evidencia de versiones en esta carpeta; sólo binarios/HTML públicos en la carpeta ignorada de medios.', '',
    '**Siguiente acción:** Video/Aprendizaje inspeccionan estas siete copias y registran cobertura visual/verbal real por pieza, incluidos inicio/final sin cues. Aceptación de esta entrega: siete medios presentes y decodificados completos, textos y límites recuperables por ruta/hash. No significa aceptación audiovisual integral ni cambios comerciales. No se envían mensajes, preguntas humanas ni operaciones Higgsfield por esta entrega.']
(OUT/'ESTADO.md').write_text('\n'.join(state)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'pass':manifest['pass'],'files':len(records),'bytes':manifest['bytes_total']},indent=2))

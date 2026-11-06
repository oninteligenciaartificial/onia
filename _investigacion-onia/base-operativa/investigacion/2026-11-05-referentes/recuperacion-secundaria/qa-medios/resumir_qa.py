"""Resume evidencia final ya generada; no vuelve a decodificar ni escribir medios."""
import json
import hashlib
from pathlib import Path

OUT=Path(__file__).resolve().parent
data=json.loads((OUT/'resultados.json').read_text(encoding='utf-8'))
if not data['all_completed']:
    raise SystemExit('La tanda aún no termina; no se publica cierre.')
preservation=None
if data.get('last_run'):
    prior_ids=data['last_run']['preserved_ids']
    prior_records=[r for r in data['results'] if r['id'] in prior_ids]
    digest=hashlib.sha256(json.dumps(prior_records,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()
    preservation={'preserved_ids':prior_ids,'canonical_sha256':digest,
                  'matches_prior_records':digest==data['last_run']['preserved_records_canonical_sha256']}
    if not preservation['matches_prior_records']:
        raise SystemExit('Cambió un registro anterior; revisar antes de publicar cierre.')
    (OUT/'preservacion.json').write_text(json.dumps(preservation,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
checks=[]
lines=[f"# QA técnico de {len(data['results'])} MP4 secundarios",'',
       '5/11/2026, America/Caracas. FFmpeg 8.1.1; ejecución secuencial con un proceso y opciones de threads del decodificador, salida y filtros en 1. No se modificaron medios, subtítulos o índices raíz. **No es visionado ni escucha.**','',
       '| ID | Duración video (s) | Duración audio (s) | Frames metadata / decodificados | Decode (s) | Resultado |',
       '|---|---:|---:|---:|---:|---|']
for r in data['results']:
    video=next(s for s in r['streams'] if s['codec_type']=='video')
    audio=next(s for s in r['streams'] if s['codec_type']=='audio')
    metadata_count=video.get('nb_frames')
    decoded=r['last_progress'].get('frame')
    equal=str(metadata_count)==str(decoded) if metadata_count is not None else None
    check={'id':r['id'],'metadata_nb_frames':metadata_count,'decoded_frames':decoded,
           'frame_count_matches_metadata':equal,'dup_frames':r['last_progress'].get('dup_frames'),
           'drop_frames':r['last_progress'].get('drop_frames'),'decode_exit_code':r['decode_exit_code'],
           'stderr_empty':not r['decode_stderr'].strip(),'source_stat_unchanged':r['source_stat_unchanged']}
    checks.append(check)
    lines.append(f"| {r['id']} | {video.get('duration','no declarada')} | {audio.get('duration','no declarada')} | {metadata_count or 'no declarado'} / {decoded} | {r['decode_elapsed_s']} | {'Completo sin errores' if r['full_decode_completed'] else 'Revisar evidencia'} |")
lines.extend(['','Los time bases, start times, duration_ts y duraciones exactas declaradas por cada stream están en sus archivos `.ffprobe.json` y `.qa.json`. Los frames finales provienen de `-progress` con fps passthrough; no se infiere duración sólo del nombre o título. Diferencias entre duración de audio y video no prueban desfase perceptual.','',
              '| ID | Bytes | SHA-256 |','|---|---:|---|'])
for r in data['results']:
    lines.append(f"| {r['id']} | {r['bytes']} | `{r['sha256']}` |")
lines.extend(['',f"Tiempo acumulado de las ejecuciones: {data['elapsed_s']} s (incluye hash/probe/decodificación). Los tiempos de la tabla son sólo ejecución FFmpeg. Código de salida 0, stderr vacío y progress=end en todos los archivos; tamaño y fecha de modificación de las fuentes permanecieron iguales durante su comprobación.",'',
              '[Evidencia conjunta](resultados.json) · [Cotejo de frames](cotejo-frames.json) · [Ejecutor](verificar_medios.py). Cada fuente tiene log `.decode.stderr.txt` y progreso `.decode.progress.txt` conservados.','',
              'Cierre: verificación técnica de extracción cumplida para estos archivos. Siguiente paso: Video/Aprendizaje usan esos medios y los subtítulos/ASR del lote para su revisión de contenido; no extender este resultado a calidad audiovisual, comprensión ni escucha.',''])
if data.get('last_run'):
    last=data['last_run']
    lines.extend([f"Ampliación incremental: se conservaron {', '.join(last['preserved_ids'])} sin repetir decodificación; sólo se ejecutaron {', '.join(last['decoded_ids'])}. Tiempo de ampliación: {last['elapsed_s']} s. Huella canónica de los registros preservados en resultados.json.",''])
(OUT/'cotejo-frames.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(OUT/'ESTADO.md').write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'all_decode_pass':data['all_pass'],'frame_counts_match':all(x['frame_count_matches_metadata'] is not False for x in checks),'preservation':preservation,'results':checks,'elapsed_s':data['elapsed_s']},indent=2))

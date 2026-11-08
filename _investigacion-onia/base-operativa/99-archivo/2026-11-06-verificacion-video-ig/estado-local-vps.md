# Estado local/VPS y muestra recuperable

Fecha: 6/11/2026, America/Caracas. Auditoría de lectura, sin conexión remota, reproducción, escucha, transferencia, instalaciones ni inferencia nueva. Checkout HEAD `e55812ce1bc8ef798fb370257ba887d07acccc53`; había cambios ajenos, preservados.

## Fuentes y autoridad

Leídos: `reglas-comunes.md`, `ESTADO.md`, `ORQUESTACION.md`, `orquestacion.json`; apoyo canónico `compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md` sólo como guía de investigación. El encargo limita a lectura y prohíbe subdelegación. No se consultó ONIA-CENTRAL ni contexto personal.

Fuentes históricas del 5/11, bajo `investigacion/2026-11-05-referentes/`:
- `audio-tecnico/vps-repositorio-20261105.md`: captura de inventario, acceso y transferencia.
- `audio-tecnico/vps-faster-whisper.md`: controles ASR y reel completo Cormac.
- `audio-tecnico/vps-instrumental.md`: controles temporales/sincronía sintéticos y correcciones.
- `audio-tecnico/vps-conette.md` y `vps-conette-experimento.md`: fallos raw y lote modular.
- `audio-tecnico/vps-arquitectura.md`: diseño y reservas propuestas; distinguir propuestas de resultados posteriores.
- `audiovisual/ruta-integral-vps.md`: evaluación independiente, rechazo de semántica temporal.
- `registro-de-errores.md`, retrospectiva VPS y lecciones recuperación/percepción: no repetir negativos idénticos ni confundir ASR con escucha.

## Hardware y estado comprobado

| Entorno | Fuente/fecha | Hecho y límite |
|---|---|---|
| VPS | Inventario histórico 5/11 citado arriba | Ubuntu24.04.4/kernel6.8;4CPU lógicas;15GiB RAM/10GiB disponibles;swap8GiB/1,4 usados;raíz193GiB/79 libres inicialmente. No GPU acreditada; ausencia exhaustiva no probada. |
| VPS al cierre histórico | Mismo informe actualizado | 73.111MiB libres después de41archivos/2.949.254.316bytes verificados por hashes. Contenedores pilotos detenidos; producción activa. No revalidado hoy. |
| Local | CIM/PSDrive, lectura directa6/11 | Windows11Home10.0.26300;i5-11400H6núcleos/12hilos;RAM25.390.186.496bytes (~23,65GiB);libre7.676.040KiB (~7,32GiB);C:37.950.427.136bytes libres (~35,34GiB). |
| GPU local | Win32_VideoController6/11 | RTX3050Laptop, AdapterRAM4.293.918.720bytes (~4GiB), IntelUHD. Detección del dispositivo, sin prueba de CUDA/runtime ni inferencia nueva. |

VPS: n8n, Easypanel, plataforma/Supabase, Chatwoot y LiteLLM observados activos el5/11; runner reiniciándose antes del piloto. No atribuir causa ni estado actual. Límites históricos del worker:1CPU/3GiB/sin swap adicional en pruebas finales;reserva host6GiB,piso disco30GiB;presupuesto agregado revisado12GiB. Son condiciones del encargo histórico, no garantía de margen actual.

## Capacidad verdaderamente validada y fallos

- ASR CPU faster-whisper1.2.1/int8: raw rechazado al transcribir silencio como «You». Configuración diferente con SileroVAD pasó negativos sintéticos, frases EN/ES y muestra JFK. VAD puede omitir voz débil; marcas verbales aproximadas.
- Cormac completo37,753991s: ASR-VAD VPS ejecutado en25,136s;RSS proceso712.160KiB. Comparación automatizada con ASR local0,9935; no verdad humana ni verificación factual. Se conserva diferencia `halo`/`halos` y frase dudosa.
- Instrumental FFmpeg/OpenCV/librosa: tonos, mezcla sintética, orden/movimiento de figura, PTS y desfase0/+250ms comprobados en controles. No acredita interpretación de montaje, música, intención ni sincronía labial real.
- CoNeTTE raw inventó motor en silencio y fue rechazado. Sistema nuevo con puerta de ceros preservó8/8 entradas,ceros2/2,señal6/6;orden voz/pulsos0/2 aceptados y atribución «man» no respaldada. No habilitado para descripción temporal/corpus.
- Correcciones ya hechas: dependencia Python pura vs only-binary;supervisor interno/reservas;PTS reales en vez de inferencia por FPS;remuestreo explícito22050→16000Hz. No repetir el ensayo de pausas mal muestreado.
- No hay percepción audiovisual integral validada en VPS. Reproducir un MP4, transcribirlo, muestrear cuadros y comprender audio+movimiento son capacidades distintas. Este informe no afirma haber visto/escuchado los reels ni juzga fuentes tipográficas o verdad de afirmaciones.

## Reel breve listo para siguiente verificación

Raíz privada local: `C:\dev\proyectos\_investigacion-onia\base-operativa\operacion\`.

Cormac `DfWLWspIruU`, original local comprobado6/11:
- `reels-e-ideas\DfWLWspIruU\DfWLWspIruU.mp4`:10.749.782bytes;SHA256 `9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e`, coincide con informe histórico.
- ffprobe local, sólo metadata:VP9,1440×2560,60/1FPS nominal;duración video37,733333s;AAC estéreo44100Hz37,753991s;ambas pistas inicio0;contenedor37,753991s. FPS nominal no certifica PTS continuos.
- `reels-e-ideas\DfWLWspIruU\DfWLWspIruU.info.json`:metadata yt-dlp identifica Instagram y el ID;sin imprimir URLs de medios ni cabeceras.
- `reels-e-ideas\DfWLWspIruU\audio.wav`:1.209.048bytes;`asr.json`:1.979bytes;`contacto.jpg`/`cierre.jpg` existentes por inventario, no inspeccionados visualmente en esta auditoría.
- `referentes-20261105\audio\cormac-vps\cormac-asr.wav.vad.json`:17.839bytes;SHA256 `377474e5c270143831bd2fedc4f4a5923d2072fd42a13c852ab7d4ba9ec34133`, recotejado;supervisores ASR/extracción en misma carpeta.
- Ruta VPS histórica original:`/opt/onia-referentes-media/cormac-01/DfWLWspIruU.mp4`;WAV:`/opt/onia-asr-pilot-20261105/input/cormac-asr.wav`;salidas:`/opt/onia-asr-pilot-20261105/output/`.
- Fuente pública identificada por ID:`https://www.instagram.com/reel/DfWLWspIruU/`;no consultada en red en esta auditoría.

Alternativa Alex disponible localmente:`referentes-20261105\reel-identidad\DevcnJYNS7r.mp4`:4.969.230bytes, existencia/tamaño comprobados;metadata compartible:`investigacion/2026-11-05-referentes/reel-identidad/metadata.json`. No hash/reproducción ni validación VPS de este reel en esta tanda. Cormac tiene mejor trazabilidad ASR-VPS ya probada.

## SSH saneado y próximo paso propuesto

Leído sólo el config local6/11:alias `onia-codex`,usuario `onia-codex`,puerto22,IdentityFile `~/.ssh/onia_codex_ed25519`,StrictHostKeyChecking=yes. Identidad existe;no se leyó contenido. HostName omitido. El acceso histórico5/11 fue `root` con otra identidad existente;no prueba que este alias actual tenga los mismos permisos ni acceso funcional.

Propuesta para coordinador, NO ejecutada:

```powershell
ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 onia-codex 'id -un; uname -sr; nproc; free -b; df -B1 /; uptime; test -e /dev/nvidia0 && echo nvidia-device-present; docker ps -a --format "{{.Names}} {{.Status}}"; stat -c "%s %n" /opt/onia-referentes-media/cormac-01/DfWLWspIruU.mp4; sha256sum /opt/onia-referentes-media/cormac-01/DfWLWspIruU.mp4'
```

Sólo lectura, sin sudo/env/inspect/config dumps ni inicio de contenedores;puede devolver permiso denegado por usuario restringido. No sustituir identidad ni elevar automáticamente. Contraste independiente de huella de host seguía pendiente en la evidencia5/11;verificación estricta sólo coteja el host conocido local. Responsable de decidir/ejecutar este paso:coordinador actual. Después separar reproducción literal disponible de análisis del modelo y exigir controles del atributo faltante antes de instalar candidato alguno.

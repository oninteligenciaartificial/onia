# Erik · preview Hermes recuperada

5/11/2026, America/Caracas. Alcance exclusivo: [lección de muestra pública](https://cursos.eriktaveras.com/c/hermes-basico/preview/). **Medio completo recuperado y decodificado; no visionado ni escucha acreditados.**

La copia pública ya existía en `operacion/referentes-20261105/marketing/erik/hermes-introduccion-61s.mp4`. Se reutilizó sin nueva descarga ni modificar el original; copia SHA-256 idéntica. La ficha de Marketing identifica [iframe público](https://iframe.mediadelivery.net/embed/748625/7e37ed34-f1ee-420a-9d08-42ec67256d7e) y [MP4 720p](https://vz-35b81d4f-cdb.b-cdn.net/7e37ed34-f1ee-420a-9d08-42ec67256d7e/play_720p.mp4). No se heredó como prueba la reproducción anterior: esta tanda ejecutó su propia decodificación completa.

| Entregable | Ruta dentro de `operacion/referentes-20261105/secundarios/erik/` | Cobertura |
|---|---|---|
| Video y audio | `erik-hermes-preview.mp4` | H.264 1280×720, video 61,600 s; AAC estéreo 48 kHz, duración declarada 61,721333 s |
| Audio para ASR | `erik-hermes-asr-16k.wav` | PCM16 mono/16 kHz, 986.795 muestras, 61,6746875 s; extracción completa sin normalizar |

MP4: 11.628.703 bytes, SHA-256 `0d362046f3afaba52920f04c597d50060f29cf400f1079a2fcda1a22b62c2aef`. Hash del WAV, metadata completa y comando/verificación en [manifest.json](manifest.json). El decode integral terminó con código 0 y stderr vacío. Las distintas duraciones de contenedor/PCM no se interpretan como desfase audiovisual.

**Subtítulos:** no hay stream de subtítulos embebido. GET nuevo de la preview: HTTP 200, sin etiquetas track ni URLs VTT/SRT. El iframe respondió HTTP 200 pero el cuerpo visible es **403**; por eso su HTML no acredita acceso al reproductor ni ausencia de pistas externas. No se recuperó un subtítulo separado y no se copiaron tokens temporales ni cookies. [Consulta y limitaciones](web-metadata.json).

**Actualización posterior de Desarrollo:** ASR local con VAD terminado sobre la entrada completa de 61,6746875 s; 58,992 s conservados por VAD, 12 segmentos de texto de 0 a 58,40 s y 20,11 s de proceso. [Resultado JSON](../erik-asr.json) y [texto automático](../erik-asr.txt). El campo `asr_executed_here:false` del manifiesto original describe únicamente la fase de extracción de ese subagente. No se interpreta el intervalo sin texto como silencio ni se acredita revisión audiovisual. Video/Aprendizaje pueden inspeccionar el MP4 completo; alcance integrado en [índice principal](../ESTADO.md). [Script de extracción](recuperar_erik.py), sin instalación, servicios, API paga o VPS.

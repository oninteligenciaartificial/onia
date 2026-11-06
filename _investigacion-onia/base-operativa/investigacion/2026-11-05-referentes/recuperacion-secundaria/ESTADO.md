# REF-RECUPERACION-20261105 · entrega de medios

**5/11/2026 · America/Caracas.** Extracción y verificación técnica terminadas.
Siete referencias autorizadas; sin ampliar investigación comercial. No se acredita visionado ni escucha. Higgsfield conserva su espera de autorización.

## Índice para Video/Aprendizaje

| Pieza/canal observado | Medio recuperado | Video real (s) | Texto recuperado |
|---|---|---:|---|
| Erik · preview Hermes | [MP4](../../../operacion/referentes-20261105/secundarios/erik/erik-hermes-preview.mp4) | 61,600 | [ASR local](erik-asr.txt), entrada61,674688s; [JSON](erik-asr.json) |
| Santiago Munoz · `anrAaNvbp4M` | [MP4](../../../operacion/referentes-20261105/secundarios/anrAaNvbp4M/anrAaNvbp4M.mp4) | 1266.433333 | [es-orig VTT](../../../operacion/referentes-20261105/secundarios/anrAaNvbp4M/anrAaNvbp4M.es-orig.vtt); [cues](anrAaNvbp4M-subtitulos.json), [texto derivado](anrAaNvbp4M-texto-derivado.txt) |
| Santiago Munoz · `oFYznV9EYPg` | [MP4](../../../operacion/referentes-20261105/secundarios/oFYznV9EYPg/oFYznV9EYPg.mp4) | 1268.400000 | [es-orig VTT](../../../operacion/referentes-20261105/secundarios/oFYznV9EYPg/oFYznV9EYPg.es-orig.vtt); [cues](oFYznV9EYPg-subtitulos.json), [texto derivado](oFYznV9EYPg-texto-derivado.txt) |
| Santiago Munoz · `4jWLq8Gn_4Y` | [MP4](../../../operacion/referentes-20261105/secundarios/4jWLq8Gn_4Y/4jWLq8Gn_4Y.mp4) | 1525.166667 | [es-orig VTT](../../../operacion/referentes-20261105/secundarios/4jWLq8Gn_4Y/4jWLq8Gn_4Y.es-orig.vtt); [cues](4jWLq8Gn_4Y-subtitulos.json), [texto derivado](4jWLq8Gn_4Y-texto-derivado.txt) |
| Nick Bare · `SVHKZkD1r_A` | [MP4](../../../operacion/referentes-20261105/secundarios/SVHKZkD1r_A/SVHKZkD1r_A.mp4) | 1681.846833 | [en-orig VTT](../../../operacion/referentes-20261105/secundarios/SVHKZkD1r_A/SVHKZkD1r_A.en-orig.vtt); [cues](SVHKZkD1r_A-subtitulos.json), [texto derivado](SVHKZkD1r_A-texto-derivado.txt) |
| Creators Latam · Bastian Xu en título del episodio · `c4S0EJAdL5I` | [MP4](../../../operacion/referentes-20261105/secundarios/c4S0EJAdL5I/c4S0EJAdL5I.mp4) | 2040.271567 | [es-orig VTT](../../../operacion/referentes-20261105/secundarios/c4S0EJAdL5I/c4S0EJAdL5I.es-orig.vtt); [cues](c4S0EJAdL5I-subtitulos.json), [texto derivado](c4S0EJAdL5I-texto-derivado.txt) |
| Alvaro Risoglio · `oZ9UKXve3Dk` | [MP4](../../../operacion/referentes-20261105/secundarios/oZ9UKXve3Dk/oZ9UKXve3Dk.mp4) | 1380.233333 | [es-orig VTT](../../../operacion/referentes-20261105/secundarios/oZ9UKXve3Dk/oZ9UKXve3Dk.es-orig.vtt); [cues](oZ9UKXve3Dk-subtitulos.json), [texto derivado](oZ9UKXve3Dk-texto-derivado.txt) |

Las identidades se cotejaron por metadata: Bastian figura como invitado en un episodio de **Creators Latam**, no como canal propietario; Álvaro corresponde al canal **Alvaro Risoglio**. No es identificación visual/por voz. [Títulos, canales y URLs fuente](youtube-metadata.json).

**Pistas de audio:** el contenedor remuxado etiqueta las seis como `eng`; esa etiqueta no se tomó como idioma real. Un cotejo público de la selección confirmó los mismos IDs de formato que los logs de descarga en 6/6: español original `es-US` para San, inglés original `en-US` para Nick y `es` para Bastian/Álvaro. [Evidencia de selección](idiomas-pistas.json), sin redescargar ni modificar los MP4. Esto acredita metadata de la pista seleccionada, no escucha.

## Cobertura exacta y límites

| ID | Intervalo VTT bruto (s) | Presencia de cues dentro del video (s) | Límites |
|---|---:|---:|---|
| `anrAaNvbp4M` | 0.000–1268.305 | 1266.433 | último cue excede video 1.872s |
| `oFYznV9EYPg` | 0.240–1270.400 | 1268.160 | sin cue inicial hasta 0.240; último cue excede video 2.000s |
| `4jWLq8Gn_4Y` | 0.199–1526.720 | 1524.968 | sin cue inicial hasta 0.199; último cue excede video 1.553s |
| `SVHKZkD1r_A` | 3.670–1661.360 | 1657.690 | sin cue inicial hasta 3.670; sin cue desde 1661.360 hasta 1681.846833 |
| `c4S0EJAdL5I` | 0.000–2032.640 | 2032.640 | sin cue desde 2032.640 hasta 2040.271567 |
| `oZ9UKXve3Dk` | 0.760–1382.159 | 1379.473 | sin cue inicial hasta 0.760; último cue excede video 1.926s |

Todos los VTT recuperados son **automáticos**, no transcripciones humanas. La unión de cues mide presencia temporal de subtítulos; no prueba que incluyan cada palabra, sonidos o música. Se conservan los intervalos brutos incluso cuando exceden el final del MP4. No se interpreta ausencia de cue como silencio. El texto derivado elimina solapamientos de palabras para lectura; cotejar cues/VTT antes de citar.

**Erik:** no hay subtítulos embebidos; la preview pública no expuso tracks, y el iframe respondió cuerpo403 aunque HTTP200. No se declara ausencia universal de subtítulos. Se aplicó faster-whisper small existente, CPU/int8/cuatro hilos, VAD: entrada completa61.674687s, conservada por VAD58.992s, 12 segmentos verbales de0.00 a58.40s; 20.11s de proceso. Sin nuevo modelo/API; no certifica el contenido de los intervalos descartados ni prosodia/mezcla.

## Evidencia y recuperación de fallos

[Manifest](manifest.json): 17 archivos de medios/subtítulos, 790,029,097 bytes; SHA-256 y ocho verificaciones integradas. [QA de seis YouTube](qa-medios/resultados.json), [Erik](erik/manifest.json), [cobertura VTT](subtitulos-cobertura.json). Decodificación completa técnica, sin confundirla con visionado. Las diferencias entre duración de metadata redondeada, streams y PCM se conservan sin inferir desfase.

- Se reutilizó la copia pública de Erik preservada por Marketing: SHA idéntico, sin alterar el original. Los seis YouTube se descargaron hasta720p con video H.264; no se recurrió a cookies, credenciales ni servicios.
- Las traducciones adicionales recibieron429: se conservaron es/es-orig de San, se separó el medio del fallo de subtítulos y se obtuvo en-orig de Nick por una consulta de pista original distinta. Para las dos candidatas finales se pidió sólo es-orig. Sin repetir la traducción fallida.
- Una consola cp1252 falló al mostrar emojis del título de Bastian después de guardar metadata válida. Se corrigió stdout a UTF-8 y se continuó con Álvaro sin repetir la consulta de Bastian.
- Scripts: [recuperación](recuperar_youtube.py), [cues/cobertura](subtitulos.py), [ASR Erik](asr_erik.py), [índice/manifiesto](cerrar_recuperacion.py). Logs de descarga y evidencia de versiones en esta carpeta; sólo binarios/HTML públicos en la carpeta ignorada de medios.

**Siguiente acción:** Video/Aprendizaje inspeccionan estas siete copias y registran cobertura visual/verbal real por pieza, incluidos inicio/final sin cues. Aceptación de esta entrega: siete medios presentes y decodificados completos, textos y límites recuperables por ruta/hash. No significa aceptación audiovisual integral ni cambios comerciales. No se envían mensajes, preguntas humanas ni operaciones Higgsfield por esta entrega.

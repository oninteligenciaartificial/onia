# REF-VIDEO-20261105 · Jeff Nippard y Ali Abdaal

5/11/2026. Se recuperaron los dos candidatos exactos documentados en `criterio/nick-jeff-ali.md`, tras comprobar por ID y nombre de archivo que no figuraban ya descargados en investigación/operación. **Dos MP4 completos con audio; 143 imágenes inspeccionadas y texto normalizado completo de captions automáticos ingleses leído. Cero escucha y cero reproducción visual continua.** Son muestras seleccionadas por el equipo para referentes pedidos; no se atribuye a Sergio el envío de estas piezas.

## Identidad, corpus y cobertura

| Pieza exacta | Identidad de metadata / procedencia documental | Medio y cobertura visual |
|---|---|---|
| [Jeff · lu_BObG6dj8](https://www.youtube.com/watch?v=lu_BObG6dj8) | Uploader/canal Jeff Nippard, canal `UC68TLK0mAEzUyHx5x5k-S1Q`; asociado al [artículo propio de cinco niveles](https://jeffnippard.com/blogs/news/how-to-build-muscle-explained-in-5-levels) en la ficha de criterio | **21:54.554**, 854×480, 30000/1001 FPS; 88 muestras cada **15.015 s** (450 frames), 0–21:46.305, más último fotograma a PTS **21:54.5132**; 89 imágenes, contactos 01–08 |
| [Ali · T2M9hSswlIs](https://www.youtube.com/watch?v=T2M9hSswlIs) | Uploader/canal Ali Abdaal, canal `UCoOae5nYA7VqaXzerajD0lg`; enlazado por la [guía propia](https://aliabdaal.com/youtube/the-ultimate-guide-to-youtube/) en la ficha de criterio | **13:14.774**, 854×480, 25 FPS; 53 muestras cada **15 s** (375 frames), 0–13:00, más último fotograma a PTS **13:14.720**; 54 imágenes, contactos 01–05 |

Se inspeccionaron todos esos contactos y ambos fotogramas finales. Muestrear la duración completa no significa haber visto cada fotograma. Las divisiones temporales siguientes son aproximadas, apoyadas en imágenes, captions y capítulos publicados; no son un listado exacto de cortes.

## Jeff: complejidad creciente y apoyos concretos

| Tiempo aproximado | Comunicación observada |
|---|---|
| 0–0:30 | Promesa de cinco niveles, presentación de fuentes/experiencia y pregunta al público sobre hasta dónde sigue la explicación |
| 0:30–1:25 | Explicación básica con guitarra, alimentos y bloques físicos como analogías |
| 1:25–4:23 | Añade parámetros y ejemplos; comparación en cuatro columnas con semanas y resaltado de lo que cambia |
| 4:23–10:03 | Descompone variables; alterna presentador, gimnasio, listas, gráfica dibujada y capturas de artículos |
| 10:03–15:50 | Contrasta explicaciones causales con diagramas, bibliografía e intervenciones remotas; el texto explicita incertidumbres |
| 15:50–21:35 | Dominós y pizarra progresiva para relaciones más complejas; distingue hipótesis y posibles objeciones |
| 21:35–21:54.513 | Captions piden comentario sobre un nivel siguiente, like y suscripción. Último fotograma negro |

**Forma:** marcador lateral de nivel, colores por categoría, comparación simultánea y alternancia entre objetos concretos y esquemas. El texto aumenta complejidad sin cambiar de pregunta central. Las capturas de papers acreditan que se muestran referencias; aquí no se validaron sus conclusiones científicas. No se convierte la explicación en consejo de entrenamiento/nutrición ni se certifica el aprendizaje del espectador. Las etiquetas de música presentes en captions no equivalen a música escuchada.

## Ali: etapas, decisiones y oferta histórica

| Tiempo aproximado | Comunicación observada |
|---|---|
| 0–0:30 | Presenta un marco de tres etapas y experiencia propia; el gancho incluye una promesa económica no validada aquí |
| 0:30–3:00 | Primeros intentos y decisión de compromiso, explicados mediante analogía de relaciones y un diagrama sobre papel |
| 3:00–5:30 | Mejora de habilidades y decisión hobby/negocio; lista superpuesta, objetos de ejemplo y promoción intermedia de edición |
| 5:30–9:00 | Clic, tiempo visto y satisfacción; después público/valor. Presentador, rótulos y apoyos visuales |
| 9:00–11:30 | Diferenciación y sistemas; analogías de restaurante/operación y dibujos |
| 11:30–13:05 | Promoción de academia/cohorte, capturas de oferta y becas |
| 13:05–13:14.720 | Captions remiten a otro video para principiantes; último fotograma muestra saludo del presentador |

**Forma:** plano de mesa con micrófono, acercamientos, plano cenital del cuaderno con presentador en recuadro, B-roll, palabras destacadas y barra de progreso inferior. Los dibujos muestran elecciones y etapas; no son una demostración completa de un flujo editorial. El cierre combina oferta y continuidad hacia otro contenido.

**Discrepancia temporal preservada:** el título recuperado dice *If I Started a YouTube Channel in 2026, I'd Do This*. La guía lo rotula con 2025, y la ficha conserva una referencia histórica de 2023 al mismo ID. La nueva metadata tiene `upload_date: 20230214`; es el campo informado por la plataforma, no una fecha inferida del título. Además, los captions del cierre **11:36–13:05** mencionan explícitamente una última cohorte en vivo en **abril–mayo de 2023**, garantía de **60 días** y becas. Las capturas de oferta/becas aparecen en las muestras de 12:15 y 12:45. Esa promoción es **histórica dentro de esta pieza**: no constituye disponibilidad actual ni sustituye las condiciones vigentes investigadas por Marketing. No se comprobó el precio, la garantía ni los resultados de alumnos.

## Captions y límite auditivo

Se descargaron directamente captions **automáticos `en-orig`**, sin ASR/modelos nuevos. Se leyó todo el texto normalizado: 702 líneas de Jeff y 518 de Ali. `captions.py` elimina etiquetas y repeticiones de líneas móviles para lectura; los VTT originales se conservan. La normalización no es una transcripción corregida ni permite certificar cada palabra, repetición intencional o sincronía.

| Pieza | Cues originales | Extensión temporal declarada en VTT | Límite |
|---|---:|---|---|
| Jeff | 1.403 | 00:00.040–21:56.360 | El último cue excede el final del MP4; errores de reconocimiento en términos/nombres |
| Ali | 1.035 | 00:00.080–13:16.399 | El último cue excede el final del MP4; no usarlo para calcular duración |

Estas son extensiones del archivo de captions, no porcentajes de exactitud ni segundos escuchados. No se comprobó voz, prosodia, velocidad verbal, pausas, música/SFX, ambiente o mezcla. El audio está disponible para una revisión auditiva autorizada. Para certificar todos los cortes y animaciones también falta reproducción visual continua.

## Evidencia local

Base: `operacion/referentes-20261105/video/jeff-ali/`.

| MP4 | Bytes | SHA-256 |
|---|---:|---|
| `jeff-lu_BObG6dj8.mp4` | 53.025.605 | `e2b4837ec44d6c375524ed9ca6d1ba5ade3ca99a6c94c4bbc7fa8de8b809f2a6` |
| `ali-T2M9hSswlIs.mp4` | 37.426.850 | `a52c2b7fb191ef7bcef96299b63ef0c418cf9081d525d4924969d6718a212522` |

Ambos contienen video AV1 y audio Opus. `manifest.json` registra los archivos, hashes, FPS, muestreo y último PTS; carpetas homónimas contienen `ffprobe.json`, `metadata.json`, imágenes, contactos y `final-frame.jpg`. Metadata de plataforma en `*.info.json`; registro de descarga en `*-download.log`; captions originales en `*.en-orig.vtt`; derivados en `*-captions-normalized.json` y `*-captions-reading.txt`; cobertura/hashes de VTT en `captions-summary.json`. Descarga pública con yt-dlp existente, sin cookies/login; no se editaron otros documentos o medios.

**Resultado:** acceso a ambas piezas resuelto, estructura visual y textual revisada con límites trazables. Práctica propia posible: explicar una misma idea con complejidad progresiva (Jeff) o convertir etapas en decisiones visibles (Ali), comprobando comprensión con un caso nuevo. No se atribuye esa práctica ni aprendizaje a Sergio, ni se adoptan promesas comerciales o científicas como hechos.

# Evidencia · grupo B · ia-ensenanza

Encargo `cerebros-b-20261108`, recibido por stdin/chat. Inicio comprobado el 8/11/2026, UTC. Base Git `e286d4564127945cb007e7b3db69cf2208e6dad7`; rama `codex/ws-cerebros-b-20261108`; worktree limpio al inicio. Ruta exclusiva: esta carpeta. El registro y briefing canónicos permanecen en manos del coordinador.

## Lecturas y selección

Principal: `AGENTS.md`; `00-MAPA/ESTADO.md`; `04-operacion-agentes/reglas-comunes.md`, `boss-memoria.md`, `ORQUESTACION.md` y selección marketing de `orquestacion.json`; `01-negocio/preparar-oferta-y-embudo/SKILL.md`; apoyo `05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md`; `05-herramientas/2026-11-08-harness/00-decisiones.md` y `plan-workshop.md`; `03-referentes/cerebros/README.md` y las seis fichas previas asignadas. Se aplica investigación primaria del apoyo, con hijos nuevos secuenciales; la prohibición de nietos prevalece sobre delegar desde cada hijo.

La skill directora fue anunciada en el catálogo de esta sesión y su cuerpo canónico fue leído explícitamente. Esto no acredita una carga automática de cuerpos. Las decisiones actuales prevalecen sobre las propuestas históricas de las fichas: clase 1 con Claude; Bs50 grupal aprobado; VIP y condiciones sólo propuestos.

## Capacidades y límites

Disponibles: subagentes nativos, lector/búsqueda web, shell, HTTP GET público, `curl` y `yt-dlp` existente. No se instala ni se ejecuta ASR nuevo pesado. Captions/ASR heredados se cuentan sólo después de leer el archivo exacto; un informe secundario sin primario accesible no basta para una pieza completa. No se acredita escucha ni visión continua a partir de texto. Las piezas bloqueadas se conservan como candidatas y no suman al mínimo.

Modelo/esfuerzo solicitado a cada hijo: `gpt-6.1-sol` / `high`, mediante parámetros nativos explícitos y contexto fresco (`fork_turns=none`). El proveedor no expone en esta interfaz un recibo independiente del modelo efectivo ni un medidor de cuota; se registra lo solicitado y se conserva observado como no acreditado salvo dato adicional. No se usan claves ni créditos API. `codex login status` devolvió `Logged in using ChatGPT`; el arranque del CLI avisó que no pudo crear aliases PATH por filesystem de sólo lectura. No se cambió configuración. Ese comando de estado no lanzó chats ni agentes y no mide saldo/cuota. La autorización es cuota incluida mediante el runtime ya iniciado por el coordinador; no se inspeccionan secretos.

## Recuperación auxiliar del principal

- GET público acotado de `https://www.youtube.com/@cormachayden/shorts`: HTTP200, HTML con IDs `xHl_LA665Pk` y `A-GvBfZTo_k`. No captions ni contenido cotejado; no suma piezas. Sitio propio `https://www.cormac.so/` leído: enlaza ese canal, Oasis y Halos. Halos abierto públicamente; sin registro ni uso del producto.
- GET público acotado de `https://www.youtube.com/@soyenriquerocha/shorts`: HTTP200, listado con IDs históricos y adicionales. GET de `https://www.youtube.com/watch?v=LsOQDp76898`: `LOGIN_REQUIRED`, cero captionTracks; no se utilizó login ni cookies. Se informa a los hijos para evitar confundir listado con contenido.
- Alternativa Ali: `https://aliabdaal.com/podcast/cal-newport-the-secrets-of-slow-productivity` leído; enlaza transcripción pública en Notion, pero lector devuelve error400 en destino. Es pista de recuperación, no pieza completa.

- Historia Git local: consulta de patrones `*/T2M9hSswlIs*`, `*/LsOQDp76898*`, `*/ali-captions*` y `*/captions-normalized.json` sin commits recuperables. No demuestra ausencia universal, sí que esta vía concreta no recuperó esos primarios.

- Alternativa posterior del principal para Enrique (8/11, tras hallazgo de Cormac): GET `/shorts/LsOQDp76898` y `/shorts/t7J-xcXjBlA` sí devolvieron player `OK` con dos pistas; esto cambia la observación del endpoint, no la recuperación de contenido. En LsOQDp76898 las pistas ASR `en` y `es` respondieron HTTP200 con cero bytes; una solicitud Range limitada a64KiB al stream público anunciado devolvió403. No se guardaron medios ni URLs temporales. La cobertura de Enrique sigue en cero completas.

## Mapa de hijos

Primera entrega terminada: `/root/erik_taveras` → `erik-taveras.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 1 pieza completa. Verificado estado nativo `completed` antes de iniciar Enrique. Su P5/P6 son entrevistas de audio como alternativas auxiliares: no se incluyen en la selección audiovisual de la matriz ni en el mínimo. P1–P4: 1 completa de 4; las seis entradas de la ficha conservan los intentos de recuperación.

Segunda entrega terminada: `/root/enrique_rocha` → `enrique-rocha.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 0/6 completas. Estado nativo `completed` cotejado antes de iniciar Ali. Su ficha completa fue leída por el principal; seis bloques y enlaces locales comprobados. GET de seis watch bloqueados sin captions; timedtext200 vacío, Instagram429, cuatro guías propias sin etiquetas de medios ni linksMP4/VTT/SRT; búsquedas de entrevista sin alternativa identificada. C1 y S1 son landing/guía, sin sumarlas al mínimo.

Tercera entrega terminada: `/root/ali_abdaal` → `ali-abdaal.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 4/4 completas para las cinco preguntas mediante segmentos de transcripciones primarias. Estado nativo `completed` cotejado antes de iniciar San. El principal leyó la ficha completa y comprobó sus enlaces locales; reabrió las tres fuentes primarias de P1–P3 (títulos, atribuciones y transcripciones visibles) y cotejó identidad y comienzo/cierre de Pathless Path en la fuente del anfitrión. P3 usa edición republicada con introducción propia; P4 reloj del transcript distinto de capítulos/citas del video. Tiempos sustentados en esos transcripts, sin offsets ni sincronía audiovisual inventados. Ni escucha ni lectura íntegra de todos los transcripts acreditadas. Descartado episodio37 de Creator Science por Watch de otro video; Headspace truncado tampoco cuenta.

Cuarta entrega terminada: `/root/san_munoz` → `san-munoz.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 3/4 completas. Estado nativo `completed` cotejado antes de iniciar Cormac. Principal leyó ficha completa, comprobó enlaces y cotejó cues/fin/duración de los tres JSON: pequeñas sobreextensiones automáticas declaradas, sin duración adicional inventada. El hijo leyó tres textos derivados íntegros y cotejó rangos exactos. Vimeo config403/player401, Skool preview inaccesible y cuarta candidata YouTube bloqueada. P4tercero sin tiempos no cuenta; reels internos no suman piezas.

Quinta entrega terminada: `/root/cormac_hayden` → `cormac-hayden.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 3/6 completas. Estado nativo `completed` cotejado antes de iniciar Bastian. El principal leyó la ficha completa, comprobó enlaces y releyó ASR de P1. Inspeccionó seis hojas temporales de control de P2/P3 (tres por Short), incluyendo extremos; el hijo inspeccionó tres y cinco hojas respectivamente. Son muestras nativas1Hz/101x180px, no video continuo. Se excluyen celdas nominales posteriores a22/36s. Sin cifras de gráficos ni texto pequeño legibles inventados. P2/P3 montajes distintos del reel y entre sí. P4/P5 bloqueadas;P6sólo metadata. Producto Halos/Oasis separado; handle actual distinto del histórico, sin migración afirmada.

Sexta entrega terminada: `/root/bastian_xu` → `bastian-xu.md`, solicitado `gpt-6.1-sol/high`, observado `null/null`; 4/4 completas. El principal leyó la ficha final, cotejó cues de EP17 en tres rangos y abrió los tres contactos visuales completos. El hijo corrigió la última celda de cada Short al comparar `approxDurationMs`: se admiten 0–50, 0–53 y 0–65 s. La celda66 de P4 no acredita un CTA dentro de duración. Cuerpos de P2/P3 distintos aunque compartan cierre; no se mezclan voces de EP17 ni se afirma migración de handles. Puente primario del canal actual a Content Project comprobado por descripción y landing.

| Slug | ID nativo expuesto | Modelo solicitado | Esfuerzo solicitado | Modelo/esfuerzo observados | Archivo exclusivo | Completas/selección | Estado final |
|---|---|---|---|---|---|---:|---|
| erik-taveras | `/root/erik_taveras` | gpt-6.1-sol | high | null/null | [erik-taveras.md](erik-taveras.md) | 1/4 | completed |
| enrique-rocha | `/root/enrique_rocha` | gpt-6.1-sol | high | null/null | [enrique-rocha.md](enrique-rocha.md) | 0/6 | completed |
| ali-abdaal | `/root/ali_abdaal` | gpt-6.1-sol | high | null/null | [ali-abdaal.md](ali-abdaal.md) | 4/4 | completed |
| san-munoz | `/root/san_munoz` | gpt-6.1-sol | high | null/null | [san-munoz.md](san-munoz.md) | 3/4 | completed |
| cormac-hayden | `/root/cormac_hayden` | gpt-6.1-sol | high | null/null | [cormac-hayden.md](cormac-hayden.md) | 3/6 | completed |
| bastian-xu | `/root/bastian_xu` | gpt-6.1-sol | high | null/null | [bastian-xu.md](bastian-xu.md) | 4/4 | completed |

Se usó un hijo nuevo con contexto fresco por referente, en el orden asignado. Se comprobó `completed` antes de abrir el siguiente: nunca más de un hijo trabajando. Los seis terminaron; ningún hijo escritor sigue activo. La interfaz expone estos IDs canónicos y estados, sin operación explícita de borrar/cerrar agentes ni UUID adicional; la terminación liberó el cupo nativo. No hubo nietos, Git de hijos ni otro escritor de sus fichas. El principal sólo escribió el índice, matriz, esta evidencia y copió imágenes pequeñas.

## Evidencia visual preservada por el principal

Después de terminar el hijo de Cormac, el principal conservó ocho hojas JPEG nativas pequeñas,139.371 bytes en total,máximo22.319 bytes por archivo. Las copias fueron cotejadas byte a byte mediante SHA-256 con los temporales leídos. La frase de la ficha sobre no almacenar medios en el repo describe el trabajo del hijo; esta preservación posterior es del principal. No hay videos ni audio nuevos en la entrega.

- Cormac P2, fuente [Short oficial](https://www.youtube.com/shorts/xHl_LA665Pk): [M0](evidencias/cormac-xHl_LA665Pk-story0.jpg), [M1](evidencias/cormac-xHl_LA665Pk-story1.jpg), [M2](evidencias/cormac-xHl_LA665Pk-story2.jpg).
- Cormac P3, fuente [Short oficial](https://www.youtube.com/shorts/A-GvBfZTo_k): [M0](evidencias/cormac-A-GvBfZTo_k-story0.jpg), [M1](evidencias/cormac-A-GvBfZTo_k-story1.jpg), [M2](evidencias/cormac-A-GvBfZTo_k-story2.jpg), [M3](evidencias/cormac-A-GvBfZTo_k-story3.jpg), [M4](evidencias/cormac-A-GvBfZTo_k-story4.jpg).

Reloj nominal: `t=(9×M+posición de celda desde0)×1s`, lectura por filas,cuadrícula3×3,celdas101×180. P2 usa0–21s de22s; P3 usa0–35s de36s. Celdas22–23 y36–37 están preservadas para auditar la exclusión, sin basar conclusiones en ellas. No equivalen a reproducción continua. No se almacenan URLs temporales firmadas.

El principal preservó también 21 hojas nativas de Bastian (437.491 bytes), cotejadas por SHA-256 con sus temporales. Total del paquete: **29 JPEG, 576.862 bytes; máximo 29.562 bytes por archivo**. No se copiaron los manifiestos temporales con URLs firmadas ni los contactos ampliados.

| Fuente Bastian | Hojas nativas conservadas | Rango admitido |
|---|---|---|
| [P2](https://www.youtube.com/shorts/GvwKsszNf6g) | [M0](evidencias/bastian-GvwKsszNf6g-sb0.jpg), [M1](evidencias/bastian-GvwKsszNf6g-sb1.jpg), [M2](evidencias/bastian-GvwKsszNf6g-sb2.jpg), [M3](evidencias/bastian-GvwKsszNf6g-sb3.jpg), [M4](evidencias/bastian-GvwKsszNf6g-sb4.jpg), [M5](evidencias/bastian-GvwKsszNf6g-sb5.jpg) | 0–50 s; celda51 excluida |
| [P3](https://www.youtube.com/shorts/etwFdjwYT6U) | [M0](evidencias/bastian-etwFdjwYT6U-sb0.jpg), [M1](evidencias/bastian-etwFdjwYT6U-sb1.jpg), [M2](evidencias/bastian-etwFdjwYT6U-sb2.jpg), [M3](evidencias/bastian-etwFdjwYT6U-sb3.jpg), [M4](evidencias/bastian-etwFdjwYT6U-sb4.jpg), [M5](evidencias/bastian-etwFdjwYT6U-sb5.jpg), [M6](evidencias/bastian-etwFdjwYT6U-sb6.jpg) | 0–53 s; celda54 excluida |
| [P4](https://www.youtube.com/shorts/XxWuLNo5dOs) | [M0](evidencias/bastian-XxWuLNo5dOs-sb0.jpg), [M1](evidencias/bastian-XxWuLNo5dOs-sb1.jpg), [M2](evidencias/bastian-XxWuLNo5dOs-sb2.jpg), [M3](evidencias/bastian-XxWuLNo5dOs-sb3.jpg), [M4](evidencias/bastian-XxWuLNo5dOs-sb4.jpg), [M5](evidencias/bastian-XxWuLNo5dOs-sb5.jpg), [M6](evidencias/bastian-XxWuLNo5dOs-sb6.jpg), [M7](evidencias/bastian-XxWuLNo5dOs-sb7.jpg) | 0–65 s; celda66 excluida |

Reloj de Bastian: mismo índice nominal a 1 Hz y cuadrícula3×3. Metadata `approxDurationMs`: 50965/53589/65984 ms, respectivamente. Las últimas celdas exceden esos valores en35/411/16 ms; no se usan para sostener hechos dentro del medio. Se preservan para auditar esa exclusión.

## Comprobaciones y publicación

Precomprobación remota: `git ls-remote origin refs/heads/codex/ws-cerebros-b-20261108` terminó con código0 y sin referencia devuelta (21:26 UTC); `origin` respondió, rama aún no publicada. No se interpreta esto como prueba de push.

Erik: principal leyó la ficha completa y el ASR exacto de P1; SHA-256 coincidió (`f741042ca644c0900c330f90d82270a9eea710b3daa101e1495884d47df4423c`). Los enlaces locales de esa ficha existen, seis bloques P y cinco respuestas en cada bloque. P2–P6 no cuentan como completas.

Validación final ejecutada con Python estándar: JSON parseado y esquema requerido cotejado; seis slugs en orden, 28 audiovisuales seleccionados y 15 completos. Estados de la matriz contrastados con cada bloque P, cinco apartados presentes y fuente temporal exigida en cada pieza completa. Sin IDs audiovisuales duplicados en la selección. Las dos fuentes de audio de Erik quedaron excluidas expresamente.

Se comprobaron 249 enlaces Markdown: URLs con esquema/host válidos; destinos locales y fragmentos existentes. Esto verifica sintaxis y referencias internas, no disponibilidad universal de cada URL bloqueada. Fuentes temporales locales existentes y URLs de las fuentes de tiempos con sintaxis válida. No se atribuye éxito de acceso a una candidata bloqueada.

Paquete de 38 archivos: ocho Markdown, un JSON y 29 JPEG pequeños; integridad de copia y 576.862 bytes de evidencia visual comprobados. Se comparó el estado Git con la ruta exclusiva: ningún cambio fuera de `03-referentes/cerebros-profundos/b`. No se inventaron tests documentales: estos son controles de estructura, correspondencia y enlaces, más los cotejos manuales descritos arriba. La comprobación de whitespace y la publicación se completan sobre el índice/commit resultantes.

La entrega es parcial: Erik1, Enrique0, Ali4, San3, Cormac3 y Bastian4 piezas completas; no se declara aceptación global. Las fuentes auxiliares y bloqueadas no reemplazan el mínimo. No se escribieron clases ni síntesis entre A/B/C. No se tocaron tareas, briefing, memoria, reglas u otros grupos. No hubo compras, registros, mensajes a personas, producción, instalaciones, ASR nuevo, servicios ni configuraciones globales.

Publicación autorizada únicamente en `origin/codex/ws-cerebros-b-20261108`, sin force ni amend. El hash de esta entrega se informa al usuario y se coteja con la referencia remota después del push; no se embebe un hash autorreferencial. El cierre de harness, revisión independiente, aceptación e integración corresponden al coordinador. Esta entrega no declara integración en master.


## Retoma de la misma tarea · fuentes públicas y ASR corto

La primera entrega y sus comprobaciones anteriores corresponden al commit `03a965882d0b960534dbf31f4e03d411e5d904dc`, que se conserva íntegro en la historia. Esta sección registra la continuación autorizada; no reinterpreta el resultado parcial anterior como aceptación. Inicio desde esa misma rama/HEAD y worktree limpio. No se modifica el registro ni el briefing canónicos.

Se releyeron AGENTS, reglas comunes, boss-memoria, decisiones/plan del workshop y directora/apoyo research. Se reanudan los hijos originales, secuencialmente y con sus mismos archivos exclusivos: prioridad Erik, Enrique, San y Cormac. Ali y Bastian ya tenían cuatro piezas y no se reabren para inflar el corpus. Cada hijo conserva la primera versión mediante Git y sus propios auxiliares fuera del repo; el principal actualizará únicamente índice, cobertura y evidencia.

La instrucción actual permite ASR breve: pesos small ya existentes, offline, CPU/int8, dos hilos y un trabajador; máximo180s por nueva pieza, secuencial y con presupuesto acotado. Prevalece sobre la exclusión anterior de ASR nuevo de la primera entrega. No se instala ni descarga modelo. No se borra ningún archivo ni temporal; medios y transcripciones extensas se conservan fuera de Git. Detención de una fuente ante auth/403/429, sin cookies, proxies o bypass.

Metodología C: la carpeta no existe en este checkout ni en el master remoto consultado `e677c7cd804621ecdbd65138be25de39f800f23a`. Se leyó solamente la documentación pertinente EVIDENCIA y apartados técnicos de gonzalo-teba/beltran-briones desde el worktree C, sin escribir allí ni abrir sus metadatos Git. Método: embed público individual → metadata/propietario/medio público → audio mono16kHz con FFmpeg si hace falta → FFprobe → small offline. La limpieza de temporales mencionada en C no se hereda: la instrucción vigente prohíbe borrar.

El snapshot local comprobado está en `~/asr/modelos/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120`. No se usa el wrapper predeterminado que puede escribir fuera de la carpeta o descargar pesos; scripts auxiliares sólo en directorios temporales nuevos y salida declarada. Las rutas temporales son evidencia complementaria; la entrega conservará fuente pública, duración, método, huellas y ventanas interpretadas, sin transcripciones largas.

### Erik · hijo original reanudado y terminado

ID `/root/erik_taveras`, modelo/esfuerzo solicitado heredado `gpt-6.1-sol/high`, observado `null/null`. Estado nativo `completed` comprobado antes de reanudar Enrique. Corpus vigente cinco completas: preview previa y cuatro reels nuevos, con formatos/guiones distintos. El principal leyó la ficha vigente completa, los cuatro ASR íntegros y metadata de autor/medio; cotejó las cuatro huellas MP4 declaradas, configuración del script y dos láminas de tres imágenes. No inspeccionó video continuo ni afirma escucha.

273,589297s de material nuevo, 78 segmentos y88,356s de wall de transcripción; no coste facturado. DfIxCRDuvXU excede1,581s en su último cue: cierre limitado a78,179s y confirmado por muestra77,47s; no se alteró el JSON original. Novedades/planes/créditos se mantienen como dichos del autor, sin validación técnica ni acciones de cuenta. Primera versión íntegra dentro del bloque histórico cercado y en03a9658; sus candidatos no se cuentan de nuevo.

ASR conservados fueraGit bajo `/tmp/onia-erik-retoma-20261108-jzkgnwkt/`; SHA-256 cotejados por el principal:

| ID | SHA-256 JSON ASR | Duración medida(s) | Wall ASR(s) |
|---|---|---:|---:|
| DfcPRmlxlbr | `8005240064ba0450580dd37074243e79e8c2c4c97f99bcf3c5b6de15e8f9f0c6` | 59.625986 | 17.655 |
| DfZ-HLAuVAV | `24c1fb4aaab162178a62167140ad0558fce2cec4645c64241eb3b19d31198ecc` | 30.229524 | 10.265 |
| DfP6T1XJliW | `041b1f56e19437f74bde84fe70827d613c99321c4cd386ce915c4a69d767eabb` | 105.555057 | 35.503 |
| DfIxCRDuvXU | `da8070b151f194b05ab93e7958b4eece9124b953262bb9872d65e8ad933dc5e1` | 78.178730 | 24.933 |

### Enrique · hijo original reanudado y terminado

ID `/root/enrique_rocha`, solicitado heredado `gpt-6.1-sol/high`, observado `null/null`; `completed` cotejado antes de reanudar San. Cuatro nuevas piezas de @soyenriquerocha comprobadas por embed/medio200 y ASR íntegro, con guiones de edición, correo, recursos y contexto. Candidatas extra P5/P6 siguen incompletas y fuera del corpus vigente P1–P4; no se usan para afirmar el mínimo. Los shorts bloqueados de la primera entrega quedan en03a9658.

Principal leyó ficha completa, los67 segmentos y la hoja de16 imágenes; cotejó ocho huellas declaradas (cuatro MP4 y cuatro JSON ASR) y parámetros del script: offline/small/CPUint8/2hilos/1worker. 206,599727s de MP4; wall externo68,127s e internoASR66,492s son medidas diferentes, no gasto ni CPUfacturada. Las duraciones WAV son algo menores que los contenedores y no se infiere un offset de video. Últimos cues dentro deaudio. La afirmación antispam y el resto de prestaciones siguen atribuidas, sin probar entregabilidad ni ejecutar herramientas. C1 reabierta por el hijo.

Temporales conservados: `/tmp/onia-enrique-retoma-xhha7ogo/` (56archivos según entrega del hijo); sin borrar ni copiar transcripciones/medios alrepo. Error declarado: el auxiliar `fuente.json` se inició con fecha2026-11-09 y se corrigió explícitamente a2026-11-08 UTC dejando nota; no se presenta la fecha errónea como real ni se altera la evidencia canónica. Las ocho huellas de medios/ASR se conservaron y cotejaron.

### San · hijo original reanudado y terminado

ID `/root/san_munoz`, solicitado heredado `gpt-6.1-sol/high`, observado `null/null`; `completed` cotejado antes de reanudar Cormac. P1–P3 conservadas, nuevaP4 `Dfc2-y6IQF8` completa; la antigua candidata `5REPWhjX64A` quedaH1histórica y excluida. Guion de llamada/agendamiento contrastado con los tres textos de edición previos: no es otro extracto de esos ejemplos.

Principal leyó los36 segmentos del ASR evitando reproducir identificadores de ejemplo, comparó la ficha vigente contra la primera y abrió las muestras temporales explícitas y cuadros132/137. El rótulo identifica clínica de demo/datos de ejemplo; se separan agente, interlocutor y presentador. No se afirma reserva o envío real ni se copian nombres/teléfonos. CTA AGENTE a137s sustentado por frame, no por ausencia de texto ASR.

Modelo/script observado small offline CPUint8/2hilos/1worker, beam5VAD. Audio139,1121875s, MP4139,223991s, wallASR32,753s,36segmentos hasta134,6s; no metraje posterior inventado. Cinco huellas cotejadas y coincidentes: tres JSON captions previos, MP4 nuevo y ASR nuevo. JSONASR SHA-256 `e96ad834cf106b008408fe8b242b1b226d8d0193cee44b8460837d02903e60a2`; MP4 `a6ca78516e656a882cbf1e5958d876748e2055f74753f4f9c7f4faef1b719b2e`.

Temporales preservados en `/tmp/san-munoz-retoma-6uusdvc7/`. Corrección de método: la cuadrícula exploratoria con filtrofps no se usa para fijar tiempos; se extrajeron posiciones explícitas mediante-ss y se mantuvo la cuadrícula anterior sin borrarla. Aviso ONNX de identificador de telemetría no bloqueó el proceso; no se modificó configuración para resolverlo. Ningún medio ni transcript extenso nuevo se copió aGit.

### Cormac · hijo original reanudado y terminado

ID `/root/cormac_hayden`, solicitado heredado `gpt-6.1-sol/high`, observado `null/null`; `completed` cotejado antes de la aclaración final del hijo Enrique. P1–P3 conservadas y nuevaP4 `DfTCQtuIRPJ` completa. Owner78346194006/cormachdn coincide con el reelP1; no se inventa migración acormacbuilds. Un GraphVideo/post, no un conjunto de assets contados como piezas. Guion de rutina/botellas distinto del escritorio y dos montajes. Las candidatas antiguas C1–C3 siguen incompletas y no cuentan.

Principal leyó la ficha actualizada y los22 segmentos íntegros, abrió11muestras0/10/…/100s y cotejó cinco huellas declaradas (MP4,WAV,JSON,TXT,contacto). Modelo/scriptobservado smallofflineCPUint8/2hilos/1worker, beam5VAD; una ejecución33,109s dewall, fuente101,003946s, últimoASR100,80s. JSONASR SHA-256 `40172e4a7a9081062a7983bd4b1643a6340710407f1feda4405e8846953909d1`. El CTA aOasis pertenece al caption y no se presenta como frase hablada. Las propiedades/relaciones con salud se describen sólo como afirmaciones del emisor; no se validan ni recomiendan.

Temporales nuevos conservados en `/tmp/cormac-retoma-20261108-y_cijoug/`, sin borrar ni copiarmedios/transcriptsextensos aGit. Los CDN temporales quedan sólo fueraGit. Las tres candidatas sin contenido suficiente se preservan como tales y dejan de ser necesarias para el mínimo.

### Aclaración final de atribución y cierre de escritores

Se reanudó brevemente al mismo hijo `/root/enrique_rocha`, después de terminar las cuatro recuperaciones, sin nuevos ASR o fuentes: aclaró P3 como discurso publicado con roles anfitrión/invitado no determinados y sin asignar turnos individuales ni edición al propietario. P2 se distingue como exposición presencial. No cambió el corpus ni sus67segmentos/huellas. Todos los hijos originales terminaron sus turnos; no hubo nuevos ejecutores ni nietos, y nunca más de un hijo trabajando. Los cuatro escritores de ficha de la retoma conservaron sus archivos exclusivos.

La evidencia de la primera entrega se comprobó conservada byte a byte como prefijo de este documento, además de permanecer en03a9658. Ali y Bastian se cotejaron byte a byte contra03a9658 y están sin cambios. Los temporales nuevos y las29imágenes previas permanecen; no se eliminó ningún archivo. La matriz final selecciona sólo el corpus vigente completo: candidatos adicionales e históricos permanecen en las fichas o primera entrega y se excluyen del conteo.

### Resultado documental de la retoma

| Slug | Hijo original reanudado | Completas antes→ahora | Nuevos clips | Material MP4(s) | Wall ASR registrado(s) |
|---|---|---:|---:|---:|---:|
| erik-taveras | `/root/erik_taveras` | 1→5 | 4 | 273.589297 | 88.356 |
| enrique-rocha | `/root/enrique_rocha` | 0→4 | 4 | 206.599727 | 66.492 |
| san-munoz | `/root/san_munoz` | 3→4 | 1 | 139.223991 | 32.753 |
| cormac-hayden | `/root/cormac_hayden` | 3→4 | 1 | 101.003946 | 33.109 |

Ali4 y Bastian4 permanecen sin cambios: total vigente25completas, con mínimo4en cada uno de los seis. Se reutilizaron los hijos originales, heredando la solicitudSol6.1/high; modelo/esfuerzo conversacionales efectivos siguen no expuestos (`null/null`). No se lanzaron otros ejecutores, chats ni nietos. El último turno de aclaración de Enrique terminó en `completed`; no quedan hijos escribiendo.

Total de10 nuevos clips: 720.416961s de contenedores MP4, máximo individual139,223991s, todos bajo180s. Los campos internos wall de transcripción suman220.709s; sus alcances se declaran por hijo y no equivalen al tiempo global de VM ni CPU/gasto facturado. Se mantuvo un único ASR activo, offline/CPUint8/2hilos/1worker, sin instalaciones ni pesos nuevos. Se cotejaron los203 segmentos nuevos; en San se omitieron identificadores del ejemplo al reproducir la salida de control.

Las limitaciones restantes no se ocultan: ASR automático con léxico imperfecto; muestras visuales discontinuas; reloj editorial de Ali no sincronizado; sin escucha integral, compra, eficacia comercial o garantía técnica/médica acreditadas. Las candidatas excluidas siguen sin contenido suficiente y no se convierten en completas por alcanzar el mínimo con otras. Las propuestas ONIA siguen separadas de los hechos: Claude en clase1, Bs50 grupal aprobado y VIP sólo propuesto.

### Comprobaciones finales de esta ampliación

JSON parseado y esquema cotejado: seis slugs en orden, 25 piezas seleccionadas completas, 4–6 por referente, cinco apartados presentes y fuente temporal existente/URL válida por pieza. Diez JSON ASR nuevos leídos; para Enrique, cuya salida no repite los parámetros CPU, se cotejó directamente el script offline con 2hilos/1worker, sin modificar los resultados. Un primer pase del control esperaba esos campos en todos los JSON y se corrigió el control, no la fuente.

Se comprobaron 257 enlaces Markdown renderizables: URLs con sintaxis/host válidos, destinos locales y fragmentos existentes, incluidas las rutas temporales preservadas en este entorno. La disponibilidad global de las candidatas bloqueadas no se afirma. La validación distingue el corpus vigente del bloque histórico cercado de Erik y de las candidatas adicionales de otras fichas. Sin IDs seleccionados duplicados; el cotejo semántico/visual de guiones se describe por referente.

Paquete conservado de 38archivos: ocho Markdown, un JSON y29JPEG previos (576.862bytes), estos últimos cotejados byte a byte con03a9658. Ali/Bastian íntegros sin cambios y primera EVIDENCIA íntegra como prefijo. Siete archivos modificados, todos bajo la carpeta exclusiva B; cero archivos borrados y ningún archivo nuevo fuera de la asignación. Los medios/transcripts nuevos permanecen fueraGit. `git diff --check` pasó antes de preparar el índice. El control de índice/commit y publicación se realiza a continuación sobre esta entrega.

Revisión de contenido: los ASR nuevos y ventanas coinciden con las cinco respuestas; roles, muestras, condiciones, diferencias de duración y afirmaciones no comprobadas quedan declarados. Los tiempos que exceden medio no se convierten en metraje, los fotogramas exploratorios no fijan tiempos y las propiedades sanitarias/antispam no se adoptan como hechos probados. No se realizaron clases completas, síntesis entre A/B/C, registros, mensajes a personas, compras, API pagas ni activaciones. Estos son cotejos proporcionales de documentación/fuentes y Git, no una suite de tests documentales ni un veredicto independiente.

La primera entrega permanece en03a9658 y como prefijo íntegro de esta evidencia. Esta ampliación se publica mediante un nuevo commit descendiente en `origin/codex/ws-cerebros-b-20261108`, sin amend ni force; el hash se informa y coteja con remoto al terminar. No se modifica el registro/briefing canónico, otras carpetas ni master. Cierre del harness, revisión independiente, aceptación e integración corresponden al coordinador.

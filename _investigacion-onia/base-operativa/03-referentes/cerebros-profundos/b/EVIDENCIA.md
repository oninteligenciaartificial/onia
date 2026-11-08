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

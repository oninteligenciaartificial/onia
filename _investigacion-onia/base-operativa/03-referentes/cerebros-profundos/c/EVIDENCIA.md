# Evidencia del grupo C · contenido y marca

Encargo `cerebros-c-20261108`, consulta del 8 de noviembre de 2026. Entrega del ejecutor; la aceptación e integración corresponden al coordinador y a un revisor distinto. No incluye síntesis entre grupos.

## Arranque y alcance

- Checkout comprobado: `/home/onia-codex-worker/repos/onia-ws-cerebros-c-20261108`.
- Rama: `codex/ws-cerebros-c-20261108`; base inicial: `e286d4564127945cb007e7b3db69cf2208e6dad7`; estado inicial limpio.
- Git privado comprobado mediante `git rev-parse --git-dir`, bajo `operacion/git/cerebros-c-20261108.git`. Remoto comprobado: `oninteligenciaartificial/onia`.
- Briefing recibido en el chat/stdin; no se requiere su proyección en este checkout. No se modifica el registro canónico ni se ejecutan transiciones del harness.
- Única carpeta de escritura versionada: `03-referentes/cerebros-profundos/c`, relativa a base-operativa.
- Instrucciones ONIA recibidas explícitamente por el usuario; skills propias anunciadas en el catálogo de esta sesión. Sus cuerpos se leyeron por archivo. No se afirma ejecución automática de una instrucción Start.

## Lecturas del principal

Rutas relativas a `_investigacion-onia/base-operativa/`, salvo AGENTS:

- `AGENTS.md` de la raíz; `00-MAPA/ESTADO.md`.
- `04-operacion-agentes/reglas-comunes.md`, `boss-memoria.md`, `ORQUESTACION.md` y `orquestacion.json` (área marketing).
- `01-negocio/preparar-oferta-y-embudo/SKILL.md`, directora; `05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md`, apoyo de investigación primaria con contexto fresco.
- `05-herramientas/cloud/INICIO-SESION.md`, aplicado al checkout asignado sin operar otros checkouts.
- `05-herramientas/2026-11-08-harness/00-decisiones.md` y `plan-workshop.md`.
- `03-referentes/cerebros/README.md` y las siete fichas previas: Gonzalo, Beltrán, Toto, Nick, Jeff, Álvaro y Voltra.
- `03-referentes/fichas/marketing/gonzalo-beltran-toto.md`, `03-referentes/fichas/audiovisual/gonzalo-alternativa.md`, `gonzalo-beltran.md` y ASR `03-referentes/asr/complementario/gonzalo-alternativa.txt`.

Las lecturas posteriores para verificar las entregas se registran con cada referente. Las propuestas comerciales históricas de las fichas no sustituyen las decisiones actuales: Claude en clase 1, Bs50 grupal aprobado; VIP sólo propuesta.

## Delegación nativa

Un hijo nuevo por referente, secuencial, sin nietos. Cada hijo recibe una sola ficha; sólo el principal escribe índice, matriz y este archivo y hace Git. Contexto fresco solicitado con `fork_turns=none`, modelo `gpt-6.1-sol`, esfuerzo `high`, según autorización expresa. El recibo de creación identifica el task ID; modelo/esfuerzo son parámetros solicitados y aceptados por la herramienta, no una medición independiente de la inferencia subyacente. No se usan procesos `codex exec` alternativos.

| Slug | ID nativo | Modelo / esfuerzo solicitados | Archivo exclusivo | Cobertura entregada | Estado del hijo |
|---|---|---|---|---|---|
| gonzalo-teba | `/root/gonzalo_teba` | gpt-6.1-sol / high | `gonzalo-teba.md` | 4 completas (P1–P4), 2 incompletas | entrega final recibida; sin escritor activo |
| beltran-briones | `/root/beltran_briones` | gpt-6.1-sol / high | `beltran-briones.md` | 4 completas | entrega final recibida; sin escritor activo |
| toto-artuso | `/root/toto_artuso` | gpt-6.1-sol / high | `toto-artuso.md` | 4 completas | entrega final recibida; sin escritor activo |
| nick-bare | `/root/nick_bare` | gpt-6.1-sol / high | `nick-bare.md` | 4 completas, 2 complementarias fuera del mínimo | entrega final recibida; sin escritor activo |
| jeff-nippard | `/root/jeff_nippard` | gpt-6.1-sol / high | `jeff-nippard.md` | 4 completas | entrega final recibida; sin escritor activo |
| alvaro-risoglio | `/root/alvaro_risoglio` | gpt-6.1-sol / high | `alvaro-risoglio.md` | 4 completas, P4 con límite de atribución editorial | entrega final recibida; sin escritor activo |
| voltra | `/root/voltra` | gpt-6.1-sol / high | `voltra.md` | 4 completas | entrega final recibida; estado nativo completed |

Las herramientas expuestas permiten crear, consultar, enviar mensajes e interrumpir hijos; no exponen una operación de borrado/cierre. Se espera la entrega final y se comprueba su estado antes de crear el siguiente. No se mantienen dos hijos ejecutando a la vez.

## Criterio de cobertura

Una pieza sólo cuenta completa cuando se leyó contenido primario suficiente para las cinco respuestas y su apertura/desarrollo/cierre tienen tiempos sustentados. Un enlace, título, snippet, landing o análisis secundario no alcanza. La página comercial es independiente y no suma piezas. Los ASR/captions existentes se distinguen de escucha/visión integral; no se inventan música, cortes, sonido ni minutos. Una ficha parcial no satisface la aceptación de cuatro piezas completas.

## Cotejo de las fichas

### Gonzalo: cotejo del principal

Ficha completa leída. P1 contrastada con el ASR conservado en repo; P2–P4 contrastadas con todos los segmentos de los tres JSON nuevos en `/tmp` antes del cierre de esta unidad. Ventanas y paráfrasis de apertura, desarrollo y cierre coinciden. Las tres huellas SHA-256 de los JSON se recalcularon y coinciden con las citadas. La ficha conserva resúmenes temporizados, método, duración y huellas; no depende de mantener medios temporales ni copia transcripciones extensas. P5/P6 no suman piezas. Página comercial comprobada por el hijo; límite 404 del formulario preservado. No se asume que la oferta detallada o una inscripción se hayan comprobado. Tras recibir la respuesta final, `list_agents` dejó de listar al hijo Gonzalo y sólo mostró al principal y al nuevo hijo Beltrán.

Se reutilizó un ASR y se ejecutaron tres ASR breves con herramientas y modelo locales, CPU/int8, dos hilos/un trabajador. El hijo reporta unos 69,5 s de los tres procesos terminados; un arranque duplicado fue interrumpido y queda excluido de esa suma. No es coste facturado ni medida total de CPU. Los medios temporales propios se eliminaron; no hubo instalaciones, descarga de pesos ni transcripción larga. Un candidato bloqueado por copyright se conservó sin eludirlo; alternativas del mismo propietario permitieron completar el mínimo.

### Beltrán: cotejo del principal

Ficha íntegra leída: cuatro piezas distintas con cinco apartados y mapas temporales, comercial separado y tres aplicaciones vinculadas. El principal reabrió por GET los cuatro embeds individuales: HTTP 200 y propietario `beltran.real.estate`; reabrió el perfil `beltranbriones`: HTTP 200 y los cuatro identificadores presentes. Esto corrobora la vinculación editorial descrita, no la identidad vocal ni el contenido hablado. La ficha conserva esa diferencia y no identifica por apariencia. El hijo leyó cuatro ASR breves completos, refinó apertura/cierre donde el primer pase no bastaba y conservó ventanas, método, duración y huellas en la ficha. Medios y auxiliares temporales eliminados por el hijo; el principal no afirma haber releído los JSON ya eliminados. El mínimo se apoya en esa lectura primaria documentada, no en el VTT histórico ausente. Mercado Libre 403 se registra como límite actual, sin reutilizar precios anteriores como vigentes.

### Toto: cotejo del principal

Ficha íntegra leída. El principal leyó completos los dos ASR nuevos y el ASR histórico de LinkedIn; cotejó apertura, bloque explicativo y cierre del vlog con sus tramos exactos de ASR existente, sin volver a transcribirlo. Los cinco apartados y las cuatro estructuras tienen respaldo; la pieza cotidiana P4 se limita como tal, sin convertirla en un método comercial. Se recalcularon las cuatro huellas de JSON (dos existentes y dos nuevos), todas coincidentes con la ficha, y se comprobaron sus enlaces locales. La evidencia nueva es de 114,849 s de clips breves y no del vlog largo. Fechas exactas de publicación P2–P4, fragmentos automáticos defectuosos, escucha y conversión quedan separados de los requisitos cumplidos. El hijo documenta búsqueda acotada sin curso propio y comprobación de Marz/portfolio/precios/auth sin alta ni pago.

### Nick: cotejo del principal

Ficha íntegra leída y los tres ASR nuevos completos cotejados desde sus JSON temporales. El principal revisó también apertura, reflexión de prioridades y cierre de los captions primarios existentes. Las ventanas documentadas tienen respaldo. P2 distingue la lectura de un texto ajeno de una tesis original de Nick. P5 y P6 tienen guiones/estructuras diferenciados; su uso de archivo y posible solape visual breve quedan declarados. Los dos primeros candidatos visuales tenían poco desarrollo explicativo: el principal pidió alternativas habladas y el hijo recuperó dos, sin recurrir a transcripción larga. P3/P4 quedan expresamente fuera del mínimo (`completa=false`); ASR sin segmentos no se presenta como silencio. El mínimo conservador es P1/P2/P5/P6. La discrepancia de prueba/precio comercial y el checkout ilegible siguen abiertos.

### Jeff: cotejo del principal

Ficha íntegra y los cien segmentos de los cuatro ASR nuevos leídos por el principal. Los últimos cues excedían unas décimas varios contenedores; se pidió y comprobó la declaración del desfase y el límite del cierre al medio medido. Los tres videos de una serie son piezas y guiones distintos, pero la diversidad limitada se preserva como límite. El antiguo resumen de cinco niveles no suma como pieza primaria. Pure Bodybuilding/Essentials se comprobaron sin transacción. El principal localizó tres candidatos de respaldo en el índice público [Picmany](https://picmany.com/jeffnippard); no fueron necesarios ni contados. El hijo obtuvo los suyos mediante índice Boostcamp y después cotejó los cuatro embeds y medios primarios, diferenciando descubrimiento secundario de análisis primario.

Durante la tarea se añadió el catálogo vidIQ. Se inspeccionó su descripción de lectura de transcripción: declara consumo de créditos. No se llamó a sus herramientas ni se consultaron cuentas; la restricción del encargo mantiene sólo cuota incluida ChatGPT y recursos públicos/locales disponibles.

### Álvaro: cotejo del principal

Ficha íntegra y tres ASR nuevos completos leídos por el principal; apertura, invitación de multicuentas y cierre de captions del vlog cotejados en el archivo exacto. Se recalcularon las cuatro huellas de JSON (tres nuevos y captions existentes), coincidentes con la ficha; enlaces locales comprobados. Los tres primeros teasers se descartaron por escasez/duplicación, incluido uno que retomaba el vlog. Los reemplazos se contrastaron por contenido y escenas, no sólo URL/hash. La cifra de visitas compartida no demuestra identidad de pieza.

P4 tiene propietario empresarial `voltra.argentina` (nombre de perfil Voltra Reels) y figura en el feed personal asociado; la cadena de publicaciones compartidas conecta éste con el perfil enlazado por SWAP. No aparece `coauthor_producers`, por lo que no se acredita modalidad de colaboración, equivalencia societaria ni identidad vocal. Se cuenta su análisis como publicación editorial asociada, conservando esa reserva en ficha y matriz. La suficiencia de esa atribución queda expresamente a revisión independiente; una exigencia de subida exclusivamente personal requeriría sustituirla. La tienda se comprobó como empresa y la búsqueda sin landing personal se documentó por fuentes y consultas, sin afirmar ausencia universal.

### Voltra: cotejo del principal

Ficha íntegra y los tres ASR nuevos completos leídos por el principal, junto con TXT/JSON existente de P1 y palabras temporizadas del cierre. La distinción de cuatro creativos se apoya en guiones/acciones y procedencia del carrusel de tienda, no sólo hashes o resoluciones. El principal abrió el HTML público del producto HTTP 200 y localizó doce URLs MP4 únicas como entrada; el hijo cotejó los cuatro assets seleccionados. La apertura verbal no recuperada de P2 y el hueco de ASR de P3 se cubren con observaciones visuales por PTS, sin inventar frases ni silencio. Las primeras hojas exploratorias no respaldan tiempos; la ficha utiliza el muestreo por índice de frame y PTS. Claims comerciales permanecen atribuidos y no se convierten en prestaciones medidas. La página conserva contradicciones, sin compra ni checkout ejecutado.

## Verificación final y publicación

Las siete respuestas finales nativas fueron recibidas en orden, antes de abrir al siguiente hijo. La última consulta de `list_agents` mostró sólo al principal ejecutando y al hijo Voltra en estado `completed`: **cero hijos ejecutando, cero escritores vivos sobre fichas**. No hay herramienta expuesta de borrado del hijo; se acredita terminación, no una operación de cierre que el runtime no ofrece.

Los siete archivos fueron escritos exclusivamente por sus hijos; el principal sólo escribió README, EVIDENCIA y COBERTURA.

Comprobaciones ejecutadas sobre la entrega reunida:

- JSON válido, esquema requerido, grupo `c`, siete slugs en el orden asignado, nombres de archivo y tipos válidos.
- 32 entradas en inventario: **28 completas (4 por referente)** y 4 complementarias/incompletas excluidas. Tres teasers adicionales de Álvaro están sólo en su tabla de descartes. No se cuentan duplicados por resolución, alias de URL ni recortes conocidos.
- Presencia comprobada de los cinco apartados en las 32 entradas; la suficiencia del contenido y sus reservas se cotejaron leyendo las siete fichas y las fuentes detalladas arriba. El conteo de encabezados por sí solo no acredita calidad.
- **50 enlaces internos válidos**, incluido un anchor comprobado contra su encabezado; todos los archivos de matriz existen. Las URLs públicas se consultaron según la evidencia de cada ficha; esto no garantiza disponibilidad futura ni se presenta como un nuevo acceso a cada enlace durante el cierre.
- **10 archivos**, todos dentro de `03-referentes/cerebros-profundos/c`; cero diferencias versionadas fuera de esa carpeta respecto de la base. Sólo Markdown y JSON, ningún medio o dependencia nueva en la entrega.
- Huellas de los JSON y medios cotejados por el principal según cada apartado; en Voltra las tres huellas de medio declaradas por los ASR nuevos coinciden con la ficha.
- `git diff --check` y `git diff --cached --check` ejecutados sin errores. El diff preparado contiene diez archivos nuevos y únicamente rutas del grupo C; el segundo control incluye los archivos nuevos que la primera llamada no cubría.
- Cero hijos ejecutando tras las siete entregas finales; sin auxiliares ASR/FFmpeg pendientes según cierre de cada hijo. No hubo nietos, instalaciones, descargas de modelos, compras, cuentas nuevas, mensajes, operaciones de tienda ni producción.

Estas son comprobaciones documentales proporcionales y cotejo de fuentes, no una suite de tests inventada ni un veredicto de aceptación.

### Integridad de las fichas entregadas

| Archivo | SHA-256 al reunir la entrega |
|---|---|
| `gonzalo-teba.md` | `8e239472ff556d1ed518c0a076e55410181663e120f0773e03c7552e049db331` |
| `beltran-briones.md` | `15769c70160ba2b4bd2647a595ecd85ab2363c4b8213897432fea3f4c878318f` |
| `toto-artuso.md` | `507b92f83e9745ce44cdc6ccb4032b02729199dd331b40c68a41e514f622e6f5` |
| `nick-bare.md` | `8b63fc20cfd0253bdd263086d695f8a0db6b0a9fc1c3e597a66b1c65ab1b3417` |
| `jeff-nippard.md` | `cf178824926a3244c13c32a91f0a9dd643a24d6551746171cc21d6d49c06f472` |
| `alvaro-risoglio.md` | `1d52aa524a0115e4542aed8be873f58dc97d101c415e061bc73c27c3cd476d92` |
| `voltra.md` | `99095a5d4b2ce639ac4fe591ee6969870218c39c5be27ab1bed1e5e215f0d675` |

### Publicación autorizada y límites

Rama única de salida: `codex/ws-cerebros-c-20261108`. Procedimiento autorizado: commit y `git push origin HEAD:refs/heads/codex/ws-cerebros-c-20261108`, sin force, amend, cambios de otras ramas ni transiciones del registro canónico. Este informe se cierra antes de crear ese commit: el hash efectivo y su coincidencia con `git ls-remote origin refs/heads/codex/ws-cerebros-c-20261108` corresponden al recibo final del ejecutor. No se usa esta declaración previa como prueba de publicación.

La aceptación, cierre del harness, revisión independiente e integración a master corresponden al coordinador. No se midió cuota/saldo desde esta sesión ni se inspeccionaron claves; el perfil solicitado por el briefing y por cada creación nativa se distingue del modelo/esfuerzo no expuesto por separado como telemetría. Las reservas de atribución (especialmente P4 de Álvaro), ciencia/claims, percepción y checkout permanecen en fichas y matriz para su revisión.

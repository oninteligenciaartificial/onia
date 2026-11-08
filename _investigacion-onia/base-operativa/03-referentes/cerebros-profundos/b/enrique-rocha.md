# Enrique Rocha / tododeia · investigación profunda parcial

Consulta realizada el 8 de noviembre de 2026, UTC. `estado: PARCIAL`. `piezas_audiovisuales_completas: 0`. Se localizaron seis shorts distintos del canal oficial y se comprobaron sus barreras de recuperación. **Esta entrega no cumple la aceptación de cuatro a seis piezas audiovisuales con contenido primario y tiempos sustentados.** La lectura de una guía y de páginas comerciales se registra por separado.

## Identidad y procedencia

**HECHO REFERENTE.** La página propia atribuye el proyecto a Enrique Rocha y declara @soyenriquerocha en Instagram y YouTube. El listado público de shorts corresponde a Soy Enrique Rocha, canal `UCFNddu8E_6ITF72_6lvZa2Q`, y contiene los seis IDs de esta ficha. Esa cadena identifica al creador de tododeia. [Sobre tododeia](https://www.tododeia.com/about), [canal y listado primario](https://www.youtube.com/@soyenriquerocha/shorts).

Se releyeron la [ficha previa](../../cerebros/enrique-rocha.md), su [fuente comercial](../../fichas/marketing/enrique-rocha.md), el [informe audiovisual histórico](../../fichas/audiovisual/enrique-rocha.md) y las [decisiones vigentes](../../../05-herramientas/2026-11-08-harness/00-decisiones.md). La directora fue `preparar-oferta-y-embudo`, con apoyo de `research`. Se aplicó la restricción expresa de este encargo sobre delegación.

## Cobertura y método

Se leyó el JSON público `ytInitialData` de la pestaña de shorts mediante HTTP GET. Se extrajeron los IDs y títulos de `shortsLockupViewModel`, sin atribuirles contenido hablado. Para cada ID se leyó el estado del reproductor devuelto por la página pública `watch`. Los seis devolvieron `LOGIN_REQUIRED`, razón `Sign in to confirm you’re not a bot`, sin `captionTracks`. Se conservan las URLs de shorts como destinos canónicos de las piezas.

La ruta histórica `base-operativa/operacion/referentes-20261105/video/rocha/captions-normalized.json` no existe en este checkout. Tampoco se recuperó el MP4 histórico desde esa ruta. El informe del 5/11 cuenta 215 cuadros y 62 entradas de captions, pero esta sesión leyó el informe, sin acceso al texto crudo de esas entradas. Su cobertura permanece como antecedente documental. [Informe histórico](../../fichas/audiovisual/enrique-rocha.md).

Las alternativas públicas realizadas fueron las siguientes.

- El lector web intentó abrir los shorts P2 y P3 y devolvió `Cache miss` en ambos. Las búsquedas exactas de los IDs nuevos P4 y P5 no aportaron transcripción primaria.
- Los endpoints públicos `https://www.youtube.com/api/timedtext?v=LsOQDp76898&lang=es&kind=asr` y `https://www.youtube.com/api/timedtext?v=t7J-xcXjBlA&lang=es&kind=asr` respondieron HTTP 200 con cero bytes. Eso describe esas solicitudes concretas. Sin pistas anunciadas por el reproductor, esas respuestas no prueban inexistencia de subtítulos.
- El GET público a `https://www.instagram.com/soyenriquerocha/` devolvió HTTP 429. La búsqueda `"soyenriquerocha" site:instagram.com/reel/` no recuperó una pieza verificable. La búsqueda equivalente en YouTube tampoco aportó texto audiovisual.
- Se inspeccionó el HTML público de `/community`, `/community/crea-contenido-con-claude`, `/community/editor-pro-max` y `/community/videos-a-skills`. Las cuatro respuestas fueron HTTP 200 al usar un User-Agent de navegador. No se encontraron etiquetas `video`, `iframe` o `track`, ni enlaces MP4, VTT o SRT en esas respuestas. Sólo apareció el canal general y, en la guía sobre videos, una URL de ejemplo con un ID de marcador. El primer GET sin ese encabezado había recibido HTTP 403 en la guía. [Índice](https://www.tododeia.com/community), [guía de contenido](https://www.tododeia.com/community/crea-contenido-con-claude), [Editor Pro Max](https://www.tododeia.com/community/editor-pro-max), [Videos a skills](https://www.tododeia.com/community/videos-a-skills).
- Las búsquedas `"Enrique Rocha" "tododeia" "entrevista"` y `"soyenriquerocha" "podcast"` no localizaron una entrevista audiovisual primaria con la identidad comprobada y texto temporal accesible. Los resultados sobre herramientas de transcripción y personas homónimas quedaron fuera de la muestra.

Las respuestas HTTP y JSON se examinaron en la salida de herramientas. Esta ficha conserva sus resultados y las rutas de reproducción. No se crearon archivos de medios o transcripciones. No hubo escucha, visionado nuevo ni ASR en esta sesión.

## P1 · Claude Fable 5 + Codex

- URL exacta · https://www.youtube.com/shorts/LsOQDp76898
- Título del listado primario · *Claude Fable 5 + Codex: Step-by-Step Guide to Building With Both*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel` — short de YouTube. `completa: false`. `fuente_tiempos: null` para esta investigación primaria.
- Cobertura efectiva · ID y título del listado oficial, estado del reproductor y lectura íntegra del informe histórico. Captions y medio originales pendientes.

1. **Idea central. HECHO DOCUMENTAL HISTÓRICO.** El informe previo atribuye a la pieza separar planificación y ejecución entre herramientas para gestionar límites. Esta atribución procede del análisis anterior, cuya transcripción no se pudo releer. [Informe](../../fichas/audiovisual/enrique-rocha.md).
2. **Audiencia y problema. INFERENCIA LIMITADA.** El título y ese informe apuntan a usuarios que ya construyen con asistentes de código y encuentran límites de uso. El encaje con principiantes de un pequeño comercio queda por comprobar.
3. **Apertura, desarrollo y cierre.** El antecedente describe problema de consumo → reparto de tareas → inserto de interfaz → guía por comentario. Sus intervalos históricos son 0–10 s, 26–61 s, 62–71,5 s y 95–106,97 s respectivamente. Son tiempos del informe anterior, sin nuevo cotejo con captions o medio primario. No satisfacen `fuente_tiempos` en este encargo. [Secuencia histórica](../../fichas/audiovisual/enrique-rocha.md).
4. **Técnica de enseñanza y venta. HECHO DOCUMENTAL HISTÓRICO.** El informe describe ilustración del reparto, pantalla y CTA de recurso. Quedan pendientes lenguaje exacto, duración efectiva de cada argumento y relación entre comentario y entrega.
5. **Qué tomar para clase 1/2/3. PROPUESTA ONIA.** Evaluar la separación entre pedir un plan, revisarlo y ejecutarlo. Su prioridad sería clase 3. En clase 1 se conservaría una tarea simple con Claude. En clase 2, revisión humana del mensaje antes de usarlo. Esta adaptación está pendiente de corroborar P1.

**Faltante y alternativa intentada.** Recuperar captions originales o texto del autor vinculado a este ID. GET watch bloqueado, timedtext vacío y derivados locales ausentes. P4–P6 se probaron como alternativas genuinas del mismo canal.

## P2 · Manual y Skills personales

- URL exacta · https://www.youtube.com/shorts/T_V-GujTLXA
- Título del listado primario · *Claude Fable 5: manual y cómo usar Skills personales*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel`. `completa: false`. `fuente_tiempos: null`.
- Cobertura efectiva · ID y título del listado oficial, respuesta de reproductor y error del lector web. Cero texto hablado recuperado.

1. **Idea central.** El título anuncia un manual y Skills personales. El planteamiento real queda pendiente.
2. **Audiencia y problema. INFERENCIA DE SELECCIÓN.** Podría servir para estudiar cómo introduce instrucciones reutilizables a usuarios de Claude. El nivel de entrada y la necesidad concreta permanecen desconocidos.
3. **Apertura, desarrollo y cierre.** Pendientes los tres tramos y sus tiempos. El título no permite reconstruirlos.
4. **Técnica de enseñanza y venta.** Pendiente. No se acreditan demo, analogías, CTA ni venta.
5. **Qué tomar para clase 1/2/3. PROPUESTA CONDICIONAL.** Si una recuperación posterior demuestra una explicación accesible, evaluar instrucciones guardadas para ordenar tareas en clase 1, conservar tono comercial en clase 2 y repetir un procedimiento en clase 3. Son preguntas para revisar la pieza.

**Faltante y alternativa intentada.** Captions o guion temporal completo. GET watch dio `LOGIN_REQUIRED`; lector web del short dio `Cache miss`. Se contrastó con la guía escrita propia S1 como apoyo pedagógico separado.

## P3 · Conexión con información propia

- URL exacta · https://www.youtube.com/shorts/MHAD0IKofgc
- Título del listado primario · *Claude ahora se conecta a toda tu información y da miedo lo que puede hacer*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel`. `completa: false`. `fuente_tiempos: null`.
- Cobertura efectiva · ID, título y barreras. Cero texto hablado recuperado.

1. **Idea central.** El título anuncia conexión con información. Sistemas, permisos y resultado mostrado quedan pendientes.
2. **Audiencia y problema. INFERENCIA DE SELECCIÓN.** Candidata para estudiar cómo presenta información dispersa a usuarios de IA. La amplitud prometida por el titular requiere contrastar la pieza.
3. **Apertura, desarrollo y cierre.** Pendientes los tres tramos y sus tiempos.
4. **Técnica de enseñanza y venta.** El titular utiliza curiosidad y sorpresa. Es una observación del título, sin evidencia de cómo se sostiene el argumento audiovisual ni de su CTA.
5. **Qué tomar para clase 1/2/3. PROPUESTA CONDICIONAL.** Revisar si enseña a elegir el contexto necesario. Podría orientar información de tareas en clase 1, datos del producto en clase 2 y datos de entrada en clase 3. Esta posibilidad aún carece de ejemplo audiovisual leído.

**Faltante y alternativa intentada.** Transcripción y tiempos, además de comprobar el alcance de la demo. GET watch bloqueado y lector web `Cache miss`. El HTML de guías propias se examinó buscando un medio accesible alternativo.

## P4 · Prompts que funcionan a la primera

- URL exacta · https://www.youtube.com/shorts/t7J-xcXjBlA
- Título del listado primario · *How to write Claude prompts that work the first time*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel`. `completa: false`. `fuente_tiempos: null`.
- Cobertura efectiva · ID y título nuevos del listado oficial, estado del reproductor y respuesta timedtext vacía. El título inglés del listado no demuestra idioma hablado.

1. **Idea central.** El título promete mejorar prompts. La fórmula enseñada y los ejemplos permanecen pendientes.
2. **Audiencia y problema. INFERENCIA DE SELECCIÓN.** Posible pertinencia para personas que obtienen respuestas poco adecuadas. Falta identificar su público explícito.
3. **Apertura, desarrollo y cierre.** Pendientes los tres tramos y sus tiempos.
4. **Técnica de enseñanza y venta.** La promesa del título es observable. Queda pendiente si muestra contraste de entradas/salidas, práctica o recurso de cierre.
5. **Qué tomar para clase 1/2/3. PROPUESTA CONDICIONAL.** Evaluar cómo explica contexto, pedido y resultado. El uso prioritario sería clase 1 con una solicitud de organización. En clase 2 se examinaría un pedido comercial y en clase 3 una instrucción repetible, una vez recuperado el contenido.

**Faltante y alternativa intentada.** Captions o texto temporal autoral. GET watch bloqueado, timedtext HTTP 200 de cero bytes y búsqueda de ID sin transcripción. Se revisó S1 para obtener apoyo escrito verificable.

## P5 · Claude y Shopify

- URL exacta · https://www.youtube.com/shorts/bJGvavTY3j0
- Título del listado primario · *How to Connect Claude to Shopify to Manage Your Store*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel`. `completa: false`. `fuente_tiempos: null`.
- Cobertura efectiva · ID y título nuevos del listado oficial y estado del reproductor. Cero texto hablado recuperado.

1. **Idea central.** El título anuncia una conexión con Shopify para gestión de tienda. Funciones concretas, requisitos y resultado quedan pendientes.
2. **Audiencia y problema. INFERENCIA DE SELECCIÓN.** Podría dirigirse a comerciantes que ya usan esa plataforma. No hay base para asumir ese requisito entre asistentes de Santa Cruz.
3. **Apertura, desarrollo y cierre.** Pendientes los tres tramos y sus tiempos.
4. **Técnica de enseñanza y venta.** Pendiente observar interfaz, demostración, pasos y CTA. Nombrar una integración en el título no acredita su ejecución.
5. **Qué tomar para clase 1/2/3. PROPUESTA CONDICIONAL.** Candidata para estudiar una demostración de clase 3. Para clase 1/2 sólo se evaluaría cómo explica los datos de un negocio y su oferta. No se incorpora Shopify como requisito de ONIA.

**Faltante y alternativa intentada.** Contenido verbal temporal y comprobación del resultado mostrado. GET watch bloqueado y búsqueda del ID sin pieza textual recuperable. Se buscaron embeds en las guías propias y entrevistas con identidad verificable.

## P6 · Prompts y gasto

- URL exacta · https://www.youtube.com/shorts/4yVqeDu3O98
- Título del listado primario · *How to write great Claude prompts and stop wasting your money*.
- Autor · Soy Enrique Rocha / @soyenriquerocha.
- Consulta · 2026-11-08. `tipo: reel`. `completa: false`. `fuente_tiempos: null`.
- Cobertura efectiva · ID y título nuevos del listado oficial y estado del reproductor. Cero texto hablado recuperado.

1. **Idea central.** El título vincula calidad del prompt y gasto. Método y evidencia del ahorro quedan pendientes.
2. **Audiencia y problema. INFERENCIA DE SELECCIÓN.** Posible orientación a usuarios que pagan por IA. El plan o modelo aludido es desconocido.
3. **Apertura, desarrollo y cierre.** Pendientes los tres tramos y sus tiempos.
4. **Técnica de enseñanza y venta.** El titular usa un costo percibido para despertar interés. Quedan pendientes prueba, explicación y CTA.
5. **Qué tomar para clase 1/2/3. PROPUESTA CONDICIONAL.** Revisar si enseña a definir mejor un pedido antes de enviarlo. Podría ayudar en las tres clases, pero no se adopta promesa de ahorro monetario sin evidencia propia.

**Faltante y alternativa intentada.** Captions o texto temporal del autor y sustento de la afirmación económica. GET watch bloqueado. La alternativa documental S1 permite analizar un método escrito sin sumar una pieza al mínimo.

## C1 · Página comercial separada

**HECHO REFERENTE.** Se leyó la landing *WORKSHOP CLAUDE DE 0 A 100*, organizada por Enrique Rocha. Abre con la dificultad de aprender IA en español, describe resultados, público e inclusiones, ofrece plantillas y preguntas sobre casos individuales, y anuncia una oferta posterior. Al consultar muestra agotado. Anuncia 2 horas, 30 lugares y USD69. Son condiciones de esa página, sin prueba de venta, asistencia o disponibilidad actual. [Landing comercial completa](https://luma.com/5td5jr2y?locale=es).

**INFERENCIA.** La página permite analizar una secuencia comercial de problema → aprendizajes → público → materiales → precio/capacidad. La ejecución de la clase sigue pendiente de observación. El indicador de asistencia de Luma no verifica pagos.

**PROPUESTA ONIA.** Expresar el resultado de cada clase y requisitos de acceso antes de inscribir. El marco vigente es pequeños negocios de Santa Cruz, tres clases de ordenar, vender y automatizar, clase 1 con Claude y Bs50 grupal aprobado. VIP Bs150 y sus condiciones siguen como propuesta. [Decisiones de Sergio](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

Se reabrieron como fuentes exactas complementarias el [hub](https://www.tododeia.com/), el [libro Claude](https://www.tododeia.com/tienda/claude-de-cero-a-cien), [llamadas](https://www.tododeia.com/llamadas), [Marketing V6](https://luma.com/tcfid7z5), [claude-skill](https://github.com/Hainrixz/claude-skill) y [agente-pagokit](https://github.com/Hainrixz/agente-pagokit). Las lecturas comerciales aportan alcance y requisitos, sin consumo de productos. V15 `https://luma.com/kuabdl78` siguió inaccesible en el lector web. La evidencia útil para esta ficha se concentra en C1 y S1.

## S1 · Guía escrita auxiliar

**HECHO REFERENTE.** Se leyó el cuerpo de *Crea contenido con Claude · investigación, guiones, b-roll y portadas + 3 agentes que lo hacen por ti*, desde apertura hasta FAQ y cierre. Ordena siete etapas, aporta prompts y plantea conservar la participación humana al seleccionar ideas y grabar. Las secciones de guion usan trabajos anteriores para extraer una fórmula y proponen lectura en voz alta. La parte de agentes presenta reutilización de instrucciones y encadenamiento. Sus afirmaciones técnicas y de ahorro son declaraciones del autor. Es una guía escrita, sin tiempos audiovisuales. [S1, texto primario](https://www.tododeia.com/community/crea-contenido-con-claude).

## Patrón observado y límite de la muestra

**HECHO REFERENTE.** En la selección del listado oficial, cuatro títulos se centran en construcción, integración o acceso a información y dos en prompts. C1 explica público y resultados antes del precio. S1 avanza desde un mapa de etapas hacia tareas, ejemplos de instrucciones y reutilización. Estas son observaciones de títulos y texto primario escrito. [P1–P6, listado oficial](https://www.youtube.com/@soyenriquerocha/shorts), [C1](https://luma.com/5td5jr2y?locale=es), [S1](https://www.tododeia.com/community/crea-contenido-con-claude).

**INFERENCIA.** La muestra documental sugiere comunicación centrada en una tarea y un siguiente recurso. Con cero audiovisuales primarios recuperados no se puede establecer un patrón repetido de apertura hablada, ritmo, edición, voz o cierre entre piezas. La coincidencia temática entre títulos tampoco verifica el método enseñado.

## Tres aplicaciones concretas condicionadas por la evidencia

1. **PROPUESTA ONIA · clase 1, ordenar.** Usar una tarea cotidiana de un comercio y revisar si el pedido contiene contexto suficiente antes de aceptar la respuesta de Claude. Entregable futuro verificable, una lista priorizada que el dueño corrija. P4 se conserva como fuente candidata para estudiar cómo lo explica Rocha. El apoyo actualmente leído es S1, que hace explícitos audiencia, contexto y tarea en sus prompts. Esta aplicación tiene sustento escrito auxiliar y sigue pendiente de sustento audiovisual P4. [P4](https://www.youtube.com/shorts/t7J-xcXjBlA), [S1](https://www.tododeia.com/community/crea-contenido-con-claude).
2. **PROPUESTA ONIA · clase 2, vender.** Hacer que el dueño aporte un mensaje propio y corrija el borrador generado antes de usarlo. Entregable futuro verificable, un texto comercial que conserve datos reales y una revisión del dueño. S1 aporta el procedimiento escrito de partir de guiones propios y pulirlos en voz alta. P2 queda como candidata para comprobar cómo presenta instrucciones reutilizables. No se atribuye ese procedimiento a P2 mientras siga sin texto primario. [P2](https://www.youtube.com/shorts/T_V-GujTLXA), [S1](https://www.tododeia.com/community/crea-contenido-con-claude).
3. **PROPUESTA ONIA · clase 3, automatizar.** Mostrar un proceso acotado con entrada, resultado y revisión humana visibles. Entregable futuro verificable, que el asistente identifique qué información entra y qué salida debe comprobar. P1 es referencia documental histórica sobre reparto de tareas y P5 candidata temática para observar una demo de gestión de tienda. S1 sí permite examinar una cadena escrita de pasos. La selección concreta de automatización requiere una pieza audiovisual recuperada y el alcance aprobado de la clase. [P1](https://www.youtube.com/shorts/LsOQDp76898), [P5](https://www.youtube.com/shorts/bJGvavTY3j0), [S1](https://www.tododeia.com/community/crea-contenido-con-claude).

## Próximos pasos y comprobación

El coordinador puede retomar P1 recuperando el MP4 o `captions-normalized.json` del archivo original autorizado del 5/11 y cotejando ID, cobertura y tiempos. Para P2–P6 hace falta un medio público accesible o captions/texto temporal autoral ligado al ID. Conservar `completa: false` hasta leer el contenido y responder los cinco apartados con marcas sustentadas. Recuperar al menos cuatro piezas distintas antes de reevaluar la aceptación. Los fallos de esta sesión no justifican nuevos intentos idénticos de `watch` mientras no cambie la condición de acceso.

Comprobación documental realizada sobre esta entrega, seis IDs diferentes, seis estados incompletos, fuentes comerciales y guía separadas, ausencia de citas habladas inventadas y distinción entre antecedente, inferencia y propuesta. El archivo contiene investigación y aplicaciones propuestas, sin producción de clases ni síntesis entre grupos.

`modelo_observado: null`. `esfuerzo_observado: null`. Esta sesión hija carece de evidencia de runtime que permita acreditar esos valores.

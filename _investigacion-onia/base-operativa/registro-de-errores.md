# Registro de errores y correcciones — iniciado el 3 de noviembre de 2026

## Retrospectiva de la tanda VPS · cierre documental aceptado por Jefa

Pedido de Sergio: explicar demoras y conservar errores/soluciones para no repetirlos. Sólo causas observadas y correcciones comunicadas por Jefa; sin minutos inventados ni causa global de todos los fallos. Descarga de dependencias/modelos, transferencia autorizada de2.949.254.316bytes y prueba de negativos son trabajo necesario; el fallo legítimo de un modelo no es por sí solo un error de ejecución. Lote independiente8WAV terminado:integridad/rutas8/8, ceros2/2 y señal6/6; orden0/2 y atribución no respaldada impiden aceptar captioner en corpus. Jefa acepta propiedades/aciertos limitados, no percepción integral; sin tuning ni segunda pasada.

- **Dependencias:** `--only-binary` demasiado amplio excluyó torchoutil/ANTLR Python puro. Corrección: construir ruedas pequeñas para esas dependencias; CoNeTTE quedó instalado. [Evidencia](investigacion/2026-11-05-referentes/audio-tecnico/vps-conette.md). Resuelto ese empaquetado, no fiabilidad semántica. Caso cercano: preferir ruedas disponibles sigue siendo válido para dependencias compiladas; no habilita compilación arbitraria del sistema.
- **Supervisor:** primer timeout externo no supervisaba dentro del contenedor ni reservas periódicas del host. Se incorporó timeout interno y muestreo de memoria/disco, deteniendo sólo proceso/contenedor propio. [Supervisor e instrumental](investigacion/2026-11-05-referentes/audio-tecnico/vps-instrumental.md). Corrección comprobada en controles suplementarios; no medir un pico continuo exacto a partir de muestras. Un GET documental no exige un supervisor de inferencias.
- **Tiempo/PTS:** primer control infirió tiempos porFPS. Se corrigió conPTS decodificados y controles de0/+250ms. [Fuente](investigacion/2026-11-05-referentes/audio-tecnico/vps-instrumental.md). Aceptado sólo sintético; no sincronía labial/semántica. FPS nominal puede rotular una rejilla aproximada si no se presenta como medición exacta.
- **Frecuencia de voz:** se asumió16kHz para fuente22050Hz y se alteró duración. Remuestreo explícito/control de pausas y versión25% corrigieron el ensayo. [ASR](investigacion/2026-11-05-referentes/audio-tecnico/vps-faster-whisper.md). Texto/robustez acotados aceptados, palabras con tiempos aproximados; no segmentación fina. No remuestrear por costumbre una fuente cuyo formato ya está verificado y es compatible.
- **Presupuesto de disco:**2GiB por lote se trató como límite global. Jefa corrigió tras medir a12GiB agregados con piso30GiB libre; transferencia de41archivos autorizada, hash41/41 y laptop conservada. [Protocolo/transferencia](investigacion/2026-11-05-referentes/audiovisual/ruta-integral-vps.md). No convierte12GiB en política universal ni autoriza borrar originales o completar todo el disco.
- **Criterio raw/modular:** Whisper raw inventóYou y CoNeTTE raw motor en silencio; rechazos conservados. VAD pertenece a otra configuraciónASR; detector de ceros exactos es sistema modular nuevo congelado, con positivos no nulos retenidos y lote independiente. [Método](investigacion/2026-11-05-referentes/criterio/metodo-validacion-audiovisual.md), [ensayo](investigacion/2026-11-05-referentes/audio-tecnico/vps-conette-experimento.md). VAD/ASR aceptado acotadamente y Cormac completo procesado enVPS; modular aceptado sólo en propiedades, rechazado para descripción temporal fiable/corpus. Coincidencia entreASR no es verdad humana. Un rechazo raw no demuestra imposibilidad de todos los módulos; evitar silencio no rehabilita descripción de señal sin positivos correctos.

**Continuidad:** encabezados antiguos más un estado nuevo al final produjeron contradicciones. Se concilia la lectura principal con los estados de área; los cortes anteriores quedan fechados como historia. El caso existente de contexto/cuota se aplica también a consultas root que devolvieron contenido de venv: acotar rutas del propietario y excluir entornos/pesos/medios, sin nueva regla redundante. No es excusa para omitir una fuente pertinente. Esta corrección es documental; no demuestra ahorro cuantificado ni cierre perceptual. Jefa recibió resultados terminales; la selección documental quedó aceptada por Jefa para publicación; sin repetir controles ni registrar como éxito el tiempo necesario de descarga/copia.

## Lecciones del 5/11 · referentes, acceso y coordinación

Solicitud directa de Sergio comunicada por Jefa: registrar intención, fallo, motivo de corrección, prueba y pendiente para aplicar al iniciar tareas similares. Esta sección es la fuente de casos; no copia conversaciones ni datos personales. Las entradas anteriores son historia y no sustituyen el estado vigente. Verificación de esta actualización: revisión documental de los nueve casos y sus contraejemplos; no repetición de pruebas de modelos, conexión o despliegue. Reconsiderar una regla si amplía tareas irrelevantes: conservar el alcance y volver al caso concreto.

### Delegación y modelos

**Solicitud/intención:** Sergio pidió una Jefa coordinadora y ejecución con modelos inferiores. **Error y tipo:** Fallo de reparto: Jefa absorbía tareas de área o se heredaba Astra. **Evidencia:** [fuente](SESIONES.md). **Motivo del cambio:** Sergio delimitó Jefa como coordinadora y Astra sólo para ella; el cotejo de turn_context mostró que Sol/Terra ya ejecutaban los turnos de área. **Corrección y prueba:** Roles explicitados; Astra sólo Jefa, Sol/Terra por área. Jefa cotejó turn_context y fechas. **Estado/límite:** Resuelto en los turnos registrados; no garantiza configuración futura. **Regla operativa:** Jefa delega/revisa; cada área ejecuta y mantiene propiedad de sus archivos. **Caso donde no aplica:** No impide que Jefa lea evidencia para aceptar una entrega.

### Contexto, seguimiento y estado principal

**Solicitud/intención:** Sergio pidió continuidad útil y cuidar cuota. **Error y tipo:** Fallo de ejecución: consultas amplias, contexto excesivo, QA repetida y encabezados antiguos contradiciendo novedades. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/GOAL-REFERENTES.md). **Motivo del cambio:** las consultas extensas y QA repetidas consumían contexto, mientras encabezados viejos afirmaban un estado contrario a los resultados nuevos. **Corrección y prueba:** Reducir consulta al dato decisivo, entrega compacta; reconciliar encabezados/filas y conservar cortes como historia. **Estado/límite:** Parcial: comprobación documental de coherencia, no ahorro cuantificado ni eficacia futura. **Regla operativa:** Leer sólo fuentes necesarias; repetir QA al cambiar evidencia o aparecer un problema concreto. **Caso donde no aplica:** Ampliar una fuente si falta evidencia para decidir; no recortar silenciosamente el alcance.

### Recuperación frente a percepción

**Solicitud/intención:** Sergio pidió análisis integral de contenido, imagen y sonido. **Error y tipo:** Error de criterio: ASR, fotogramas o instalación se confundían con escucha/percepción. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audiovisual/pendientes-visuales-finitos.md). **Motivo del cambio:** los controles generativos inventaron sonido u omitieron voz; ASR y cuadros recuperan contenido sin probar escucha, ritmo ni sincronía. **Corrección y prueba:** Controles reales rechazaron MiDasheng/Eureka y Smol;16ASR recuperan texto, no calidad acústica. **Estado/límite:** Parcial: unidades documental/estática aceptadas;7grupos/40medios y39pistas conservan límites. **Regla operativa:** Aceptar sólo atributo e intervalo realmente comprobados; no equivaler texto o cuadros a percepción. **Caso donde no aplica:** Un documento escrito o animatic silencioso no exige una voz inventada.

### Control decisivo antes de ampliar

**Solicitud/intención:** Sergio quería una solución probada sin consumo inútil. **Error y tipo:** Fallo experimental: pruebas costosas antes del control excluyente de silencio. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audio-tecnico/ruta-abierta-20261105.md). **Motivo del cambio:** el silencio digital descartó rutas tras gasto de pruebas; ese control excluyente debía preceder a más inferencias y al corpus. **Corrección y prueba:** En audio generativo, comenzar por silencio neutral sin VAD que lo oculte; conservar fallo y detener esa ruta antes del corpus. **Estado/límite:** Corrección escrita y fallos documentados; no modelo fiable obtenido. **Regla operativa:** Tras superar silencio, positivos y controles del atributo antes del corpus; no repetir condición idéntica fallida. **Caso donde no aplica:** En ASR puro se mide transcripción/ausencia de alucinación; no exigirle identificar música que no promete.

### VPS y límites de tanda

**Solicitud/intención:** Sergio autorizó probar repositorios gratuitos en su VPS y quiere allí la app audiovisual con bases distintas por uso. **Error y tipo:** Criterio prematuro: concluir bloqueo sin comprobar VPS o convertir límite de una tanda en prohibición permanente. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audio-tecnico/vps-arquitectura.md). **Motivo del cambio:** Sergio autorizó probar repositorios abiertos gratuitos en VPS, superando el límite de aquella tanda, pero en aquel corte no se había comprobado acceso ni margen; el acceso y el inventario sólo lectura ya se verificaron tras la acción de Sergio. **Corrección y prueba:** Medir acceso/recursos/cargas y aislar antes de elegir; diseño de bases, roles y respaldos separados aceptado por Jefa como propuesta condicionada al inventario. **Estado/límite:** Diseño aceptado; acceso resuelto al identificar destino y usar clave local existente/host conocido con verificación estricta. Inventario sólo lectura aceptado por Jefa en [informe vigente](investigacion/2026-11-05-referentes/audio-tecnico/vps-repositorio-20261105.md). Contraste independiente de huella pendiente; ninguna instalación, inferencia o app audiovisual comprobada. **Regla operativa:** Reevaluar sólo al cambiar acceso/condición; medir reservas, aislar y ensayar controles, sin prometer éxito por hardware. **Caso donde no aplica:** No habilita migraciones de producción, gasto, puertos públicos o uso de claves contra un host supuesto.

### Superficie e interfaz Windows

**Solicitud/intención:** Sergio pidió aprovechar acceso disponible. **Error y tipo:** Diagnóstico incompleto: IAB/inventario vacío se trató como falta total de Computer Use. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audio-tecnico/vps-arquitectura.md). **Motivo del cambio:** @oai/sky pudo inicializar Windows y abrir Chrome aunque IAB faltaba; el guard de URL detuvo después la lectura. **Corrección y prueba:** Skill Windows con @oai/sky disponible y Chrome abierto; guard de URL después detuvo lectura, sin recuperación soportada. **Estado/límite:** Límite histórico de Windows/guard conservado: no se puenteó. Sergio abrió laptop/Hostinger y Desarrollo obtuvo acceso por SSH existente; eso no acredita recuperación del guard ni control universal del panel. **Regla operativa:** Distinguir inventario de una superficie de todas las capacidades; respetar guard y pedir sólo acción necesaria. **Caso donde no aplica:** No autoriza puentear guardrails ni suponer que una ventana abierta es controlable.

### Fuentes conocidas y conexión real

**Solicitud/intención:** Sergio quería resolver acceso aprovechando lo ya guardado. **Error y tipo:** Falta de acceso confundida con disponibilidad: archivos de claves no prueban conexión y API n8n no es SSH. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audio-tecnico/vps-repositorio-20261105.md). **Motivo del cambio:** las identidades locales no tenían vínculo verificado con el VPS y la página privada probó API de n8n, no SSH ni panel administrativo. **Corrección y prueba:** Consultar fuentes conocidas antes de pedir datos; lectura de entrega privada confirmó servicio n8n, no panel/SSH del VPS. **Estado/límite:** Acceso resuelto después de identificar destino y reutilizar identidad local existente y host conocido: Desarrollo logró hostname/id con verificación estricta. La lectura de API n8n anterior sigue sin equivaler a SSH; el nuevo ensayo sí acredita esa conexión. Inventario sólo lectura aceptado, sin secretos reproducidos. El límite sin servicios instalados corresponde a ese corte inicial; después hubo instalación aislada y pruebas, según [ESTADO](ESTADO.md), sin app audiovisual integral acreditada. **Regla operativa:** Comprobar destino/usuario/puerto/huella y mecanismo protegido; no pedir secretos por chat. **Caso donde no aplica:** Un GET autorizado de n8n acredita esa API, aunque no haya SSH; no descartar esa capacidad específica.

### Solicitudes y uso móvil

**Solicitud/intención:** Sergio pidió recibir solicitudes en Jefa y notificaciones móviles. **Error y tipo:** Fallo de coordinación: preguntas dispersas por áreas contradecían su uso móvil. **Evidencia:** [fuente](ORQUESTACION.md#solicitudes-a-sergio-y-canal-móvil). **Motivo del cambio:** Sergio indicó que las solicitudes llegaran al chat de Jefa por su uso mayoritario del móvil; las áreas estaban duplicando preguntas. **Corrección y prueba:** Centralización escrita; autorizaciones nativas pueden quedar en origen y no equivalen a respuesta textual; push sin configurar. **Estado/límite:** Parcial: procedimiento registrado; no notificaciones móviles configuradas ni calendario aprobado. **Regla operativa:** Jefa reúne preguntas con evidencia; preferencias/horarios se consultan sólo en privado cuando hagan falta. **Caso donde no aplica:** No autoriza aprobar botones por Sergio ni programar avisos a partir de horarios aproximados.

### Lectura del contador Erik

**Solicitud/intención:** El pedido era analizar lo realmente visible sin inventar contradicciones. **Error y tipo:** Error de observación:33 intermedio se trató como cifra final frente a56. **Evidencia:** [fuente](investigacion/2026-11-05-referentes/audiovisual/pendientes-visuales-finitos.md). **Motivo del cambio:** el cuadro nativo a59s mostró Beelink72/Lenovo56;33 era un estado intermedio de la animación, no la cifra final. **Corrección y prueba:** Video revisó cuadros55/59/63s y Jefa abrió erik-59.png:Beelink72/Lenovo56; se corrigió lectura final preservando antecedente. **Estado/límite:** Resuelto ese dato; diferencia170/171 y límites comerciales permanecen, sin rendimiento real auditado. **Regla operativa:** Antes de declarar contradicción en contador animado, comprobar estado estabilizado y marcas temporales. **Caso donde no aplica:** No borrar diferencias reales entre fuentes ni deducir ventas/rendimiento por una animación.


## Corrección del 5 de noviembre: audio sin solución, autoridad ignorada y contexto excesivo

**Caso y evidencia.** Sergio señaló que se repetía el límite acústico sin cerrar una solución. Las [revisiones locales](continuidad/2026-11-05/README.md) conservan la cobertura: muestreo visual, texto y etiquetas; Qwen alucinó sonidos sobre silencio, YAMNet/CLAP no confirmaron efectos ni prosodia. El [piloto D1](continuidad/2026-11-05/piloto-d1/reporte.md) sí produjo una prueba visual silenciosa, sin resolver el audio de referentes. Declarar el límite repetidamente fue insuficiente frente al pedido de resolverlo.

**Corrección autorizada.** Primera tarea de Jefa v2 tras commit/recepción: encargar a Video/Desarrollo [audio real con controles](continuidad/2026-11-05/HANDOFF-JEFA.md#primera-tarea-tras-la-recepción-audio-real), evaluar voz/música/SFX/silencios/sincronía y probar alternativas abiertas/autorizadas antes de pedir la intervención personal mínima. ASR no certifica prosodia. Sin Gemini ni API paga por defecto. La investigación no se ejecuta en este handoff y no se presenta como resuelta.

**Error de continuidad.** El reparto local, el alcance y los cierres vigentes quedaron sólo en `operacion/`, ignorado por Git, mientras las fuentes versionadas seguían indicando cloud o pausas anteriores. Se consolidan siete revisiones, brief/reporte D1 y bundle n8n con sus límites; ESTADO, PLAN, SESIONES y ORQUESTACION apuntan a una sola fuente en el repo. Notion es proyección; Pages conserva medios/procedencia. Medios y secretos permanecen fuera de Git, con referencias apropiadas. Preparar esta entrega no equivale a commit, recepción del relevo o archivo de la jefa anterior.

**Error de comunicación.** Lecturas extensas y repetidas trasladaron contexto innecesario entre áreas. La corrección mantiene cierres compactos: resultado, evidencia/enlace, prueba realizada, bloqueo con solución y siguiente acción. Se conserva la cobertura en la fuente enlazada; no se recorta silenciosamente el material del encargo.

**Comprobación y límite.** Revisión documental del caso: una fuente con sonido exige una prueba acústica y una salida viable; caso cercano: un animatic intencionalmente silencioso no requiere inventar locución para aceptar sólo su alcance visual. Validar enlaces y hashes comprueba recuperación e integridad, no escucha, runtime n8n ni eficacia futura de la regla. La recepción de Jefa v2 y su prueba quedan pendientes de ejecución verificable. Si el cierre compacto oculta evidencia necesaria, ampliar ese enlace/sección sin volver a importar historiales completos. No se cambian skills ni se entrenan modelos por esta corrección.

## Corrección del 4 de noviembre: cerrar video sin resolver el audio

Caso observado: la entrega del reel de Pedro Buerbaum declaró cerrada la prueba cloud, aunque sólo había revisión visual y el audio seguía sin escucharse. Se informó el límite, pero se dejó como pendiente sin pedir la capacidad concreta ni completar una vía de resolución en esa tanda. La recuperación de archivos sí funcionó; no completó el análisis audiovisual solicitado por Sergio.

Sergio ordenó explícitamente una regla nueva: analizar todo lo enviado y, ante una función ausente, pedirle la acción necesaria, recomendar alternativas y resolver lo autorizado en la misma tanda. Se incorporó en la sección «Análisis integral del material» de [reglas-comunes](reglas-comunes.md), fuente única; no se creó otra skill ni se duplicó la regla en cada proyecto.

Comprobación documental: un video con sonido exige imagen, guion, voz, música, efectos, ambiente, silencios, ritmo, sincronía y cierre; fotogramas, ASR o métricas de amplitud no acreditan escucha. Un PDF sin medios no necesita una evaluación de audio inventada. Si falta una capacidad, el agente obtiene primero lo que puede (por ejemplo, extraer la pista existente) y pide sólo el acceso o acto personal restante; no devuelve a Sergio una extracción que puede ejecutar por sí mismo. No se declara completa una revisión parcial.

Aplicación: Sergio eligió mantener sólo Codex y una alternativa abierta; Gemini quedó descartado y no recibió archivos ni prompts. En la VM cloud se extrajo la pista completa, se conservaron archivos y mediciones, y YAMNet procesó los 90,35 s en 188 ventanas. Reporta candidatos de voz/música; eso no acredita por sí solo identificación completa de efectos ni sincronía. El ensayo generativo Qwen7B ejecutó pero falló al inventar sonidos sobre silencio digital, incluso con prompt neutral; no se usaron sus etiquetas ni tiempos como hechos. La alternativa CLAP completó la pista y ventanas de comparación; no permitió confirmar efectos precisos. La corrección termina en evidencia útil y un pedido humano acotado sobre fragmentos ya preparados, sin declarar análisis auditivo integral. [Evidencia única de Video](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4). Sin compras, APIs pagas ni carga adicional en el VPS.

Sergio también corrigió la falta de una recomendación trabajada después del análisis. Su instrucción quedó incorporada en «Autonomía» de reglas-comunes: aprendizaje explícito → siguiente paso prioritario con evidencia, entregable, comprobación y responsable; ejecutar la parte autorizada. Aplicación concreta: síntesis de Hormozi, Gadzhi, Heras y Pedro; ensayo D1 en cloud de ficha → tres respuestas → contraste, registrado en [Pruebas propias](https://chatgpt.com/space/page_1d43cefbf3c48191924a32447e792e2e). La ejecución textual no valida alumnos, demanda ni ventas; su utilidad editorial necesita revisión separada. No basta preparar otro catálogo o prometer trabajo indefinido.

Estado: ambas instrucciones autorizadas y versionadas, aplicación documental revisada. La regla no agrega capacidad por sí sola ni entrena el modelo. Acotar su aplicación si induce revisión irrelevante fuera de los materiales y finalidad del encargo, manteniendo visibles los componentes que realmente faltan.

## Corrección del 4 de noviembre: diagnóstico sin salida operativa

Sergio volvió a señalar que el cierre describía un bloqueo sin resolver cómo operar. La investigación textual avanzaba, pero se repetían pruebas y se dejaba la corrección del navegador como trabajo futuro. Además, la documentación del repo seguía contradiciendo Notion y pruebas cloud posteriores.

Corrección ejecutada: aislar el problema de la base NSS de sólo lectura, conservar la misma CA oficial y TLS, reconstruir confianza en un directorio escribible por proceso y comprobar página, clic y reproducción real. El resultado y límites están en [evidencia del día](EVIDENCIA-2026-11-04.md) y [operación cloud](cloud/OPERAR.md). No hizo falta contratar infraestructura nueva. Las alternativas se compararon antes de decidir.

Sergio autorizó subir la información útil verificada. Se consolidaron las fichas, fuentes y estado, manteniendo propuestas como propuestas y Notion para lo cotidiano. El cambio corrige este caso; no agrega una skill, no entrena el modelo ni permite eludir bloqueos legítimos de terceros. El cierre exige commit remoto y aceptación cloud identificables, no sólo un documento escrito.

Solicitud de Sergio: «Una leida mas a todo lo que hablamos y anotas tu error».

Revisión: mensajes de Sergio disponibles en esta conversación y contraste con contexto, reglas, corrección de procedencia, catálogo y recorrido documentados. No se consultó ONIA-CENTRAL.

## Error principal

### Corrección del entorno cloud — 3 de noviembre de 2026

Elegí ONIA Platform para probar el harness porque era un entorno ejecutable existente. Sergio aclaró que requiere un entorno limpio llamado `onia` y un repositorio de esta carpeta. La disponibilidad de un entorno no justificaba usar el repositorio del producto como base del sistema de coordinación.

Se envió orden de detener la tarea 01a1a3e6-50ac-7052-9243-cafe9e8a200c. Confirmó detención, sin procesos activos, commits, push ni despliegue. La prueba stdlib aprobó cinco tests; instalar Chromium falló por 403 Domain forbidden. La evidencia queda como histórica y no valida `onia`.

Corrección: preparar repo privado desde la base vigente, excluir todos los proyectos y respaldos vecinos, vincularlo sólo al entorno `onia` y comprobar allí reglas, skills y continuidad. No volver a cargar trabajo del harness en el repositorio del producto.

Convertí repetidamente un encargo de construcción y acompañamiento en propuestas, catálogos y documentos. Sergio pidió empezar a armar su sistema de trabajo y comprobar qué funciona. Yo avancé en investigación y redacción, pero dejé la implementación del harness, la continuidad entre sesiones y el aprendizaje como pasos futuros. Esa diferencia es responsabilidad mía; una explicación extensa no la resuelve.

La meta de ingresos debe orientar el sistema. No me autoriza a sustituir el encargo inmediato de arquitectura, reglas y skills por otro plan comercial ni a exigir una oferta terminada para todo avance independiente.

## Errores concretos y evidencia

1. **Adopté una base equivocada.** La corrección de procedencia ya registra que mezclé propuestas con ONIA-CENTRAL. Sergio lo excluyó expresamente. Sus reglas, skills, versiones y permisos no son fuente del sistema nuevo. La propuesta anterior no se retoma.
2. **Recomendé antes de completar la comparación.** El primer catálogo distinguía cuatro repositorios leídos y 26 pendientes. Sergio tuvo que pedir que leyera todos. La revisión posterior amplió la cobertura, pero no borra ese error.
3. **No separé con suficiente claridad selección, adaptación y funcionamiento.** Un catálogo de 15 capacidades no son 15 skills creadas. Tres archivos con formato validado no prueban un harness operativo. Tampoco prueban trabajo cloud, una sesión que retoma correctamente ni un ciclo de aprendizaje.
4. **Dejé que mi preferencia por reducir herramientas desplazara parte del pedido.** Evitar contradicciones exige identificar comportamientos concretos, adaptar y probar. No basta postergar paquetes por ser grandes. Las decisiones actuales son recomendaciones documentales; no resultados de ensayos comparativos en ONIA.
5. **No consolidé suficientemente las correcciones de Sergio.** No hay dos semanas reservadas para diseñar reglas: se empieza ahora y el plazo comercial es el 14 de noviembre. HyperFrames y n8n son elecciones expresas; funnels, webinars, Meta, organización personal y desarrollo forman parte del alcance.
6. **La identificación y lectura tienen límites que deben mantenerse visibles.** Los nombres del reel no equivalen a 30 enlaces exactos confirmados por su autor. La correspondencia de Agent Skills sigue provisional. Se hizo lectura dirigida de repositorios, no auditoría de todo su código, ni se verificó íntegramente el video.
7. **El alcance original sigue teniendo pendientes.** Comparativa de LLM y límites efectivos, accesos/bóveda, inspección del VPS, distribución de reglas, sesiones y aprendizaje no están resueltos por haber terminado un catálogo. No debo presentar el conjunto como armado.

## Pedido que debo conservar

- Organizar la vida de Sergio y ONIA alrededor de su disponibilidad real, colegio, gimnasio, descanso y compromisos.
- Orientar el trabajo a la meta económica del 14 de noviembre sin consumir la etapa en diseño.
- Empezar a construir reglas comunes desde las decisiones de esta conversación, con contexto persistente y control de entradas, salidas, tareas y resultados.
- Aprovechar Codex y los servicios que Sergio reporta existentes; complementar Grok Bot cuando tenga cuota, sin presuponer planes superiores ni acceso API.
- Usar el código de ONIA Platform para el producto; no heredar autoridad del repositorio excluido.
- Evaluar las referencias aportadas, seleccionar capacidades compatibles y adaptar skills a tareas reales: video con HyperFrames, marketing, ventas/talleres, código, organización y n8n.
- Construir autonomía acotada y verificable; conservar las decisiones de Sergio y las autorizaciones ya dadas.

El detalle personal y económico permanece en privado/contexto.md; este registro no crea una segunda fuente de esos datos.

## Corrección operativa

Antes de actuar, identificar el resultado concreto solicitado en el turno y conservar el objetivo general. Completar el trabajo autorizado que no dependa de información faltante. No volver a entregar únicamente un plan cuando se pidió implementación.

Al informar, separar: propuesta, archivo creado, disponible en el entorno, probado y operativo. Vincular cada afirmación de funcionamiento a su evidencia. Una limitación puntual bloquea sólo el trabajo que depende de ella.

Cerrar cada unidad con el cambio realizado, comprobación, pendiente concreto y siguiente acción. Si algo no se incorpora, explicar qué necesidad queda cubierta y qué condición justificaría reconsiderarlo.

## Estado de esta corrección

Error registrado y enlazado desde el índice; criterio de cumplimiento incorporado a reglas-comunes.md. La eficacia de la corrección se comprobará en el próximo encargo mediante un resultado terminado y verificable. Este registro no significa que el autoaprendizaje, la distribución de reglas o el harness ya estén desplegados.

## Corrección de configuración y navegador — 3 de noviembre de 2026

Sergio pidió configurar accesos, corregir los scripts ausentes y avanzar con el harness. Volvió a señalar que se repetían explicaciones y que la interfaz sí mostraba un navegador.

| Error observado | Causa identificada | Corrección aplicada y evidencia |
|---|---|---|
| Afirmar categóricamente que no había navegador cloud. | Trasladar una limitación documental general a la interfaz de Sergio, sin inspeccionar antes su capacidad efectiva. | Captura de Sergio: pestaña de navegador junto al entorno. «Editar onia» comprobó Chromium 156.0.8078.4 en la VM con clic y captura; remote_desktop habilitado, estado unknown, sin herramienta de control interactivo expuesta. El control de esa pestaña y el login persistente quedan sin probar, no descartados. |
| Tratar los scripts como ausentes sin cerrar el diagnóstico de versión. | La preparación conservaba HEAD 4de11bb; GitHub ya incluía los scripts desde 66674eb. | Se leyó el chat «Editar onia» y ambos archivos de master; avance fast-forward a f81a5b9. install.sh y start.sh terminaron, doce tests Python y uno de navegador aprobaron. No hizo falta recrear archivos. |
| Alternar bóveda personal y secretos del entorno. | Presentar dos mecanismos válidos como pasos sucesivos, generando confusión y posible duplicación. | Ubicación elegida: N8N_API_KEY en Secretos de red del entorno onia. Sergio la cargó allí; el helper dio HTTP 200, diez flujos en la página y siete activos. Ningún valor o contenido de flujo se exportó. |
| Repetir comprobaciones de la tarea antigua y listas en vez de operar la preparación. | Usar su revisión 1 como si describiera el editor actual y no inspeccionar el chat de setup disponible. | Se continuó el chat correcto. La desconexión proxy/exec-server se informó como fallo de acceso; tras recuperarse se actualizó y probó el checkout real. Las partes independientes del harness avanzaron con subagentes. |

Fuente: chat de coordinación y «Editar onia» (`01a1a428-996b-77af-9f4d-cacf78486021`, turno de recuperación `01a1a443-92d1-72f3-8e88-82b108cfae03`). El resultado describe esa instancia de preparación; no acredita la aceptación de una tarea nueva ni la publicación de sus archivos actualizados.

Cambio de procedimiento: reglas-comunes exige comprobar evidencia real cuando contradice una afirmación; CONFIGURAR-ONIA ahora comprueba HEAD y rutas antes de ejecutar. El diagnóstico `harness.py doctor` detecta un script faltante, pero informa expresamente que presencia no equivale a runtime operativo. Su prueba cubre el archivo ausente y el caso cercano con archivos presentes, sin afirmar una conexión.

La instrucción no obliga a explorar todas las fuentes posibles ni convierte una captura en prueba de control. Si no existe herramienta o sesión habilitada, registrar ese límite concreto y continuar lo independiente. Revertir o acotar el procedimiento si deriva en revisiones repetidas sin evidencia nueva. Este cambio mejora instrucciones persistentes; no entrena los pesos del modelo.


## Alcance n8n contrastado con operaciones reales — 4 de noviembre de 2026

Se trató la observación histórica `workflow:list` como límite actual y se planteó otra key antes de comprobar el alcance efectivo. Coordinación confirmó discovery HTTP 200 con capacidades de workflow, credenciales, tablas y filas, y la creación de un workflow sintético inactivo con diez nodos. Corrección: no pedir otra clave para ese alcance ya disponible; ejecutar el encargo autorizado y reservar la intervención personal para accesos que realmente falten. [Accesos](accesos.md) conserva el resultado y la [evidencia privada](https://chatgpt.com/space/page_381ee668401481918e7e45c87921e82d) contiene el artefacto.

La comprobación documental distingue discovery, POST/GET reales y 14 tests de modelo. El cierre posterior, releído en la evidencia privada secuencia 2, sí acredita cinco casos ejecutados en n8n y persistencia secuencial de una fila por evento, con tabla/credencial reales; final inactivo y guardado de ejecuciones deshabilitado. No acredita concurrencia, timeout real ni Meta. No queda una acción de Sergio para cerrar ese ensayo sintético. No se amplían permisos por inferencia ni se declara autenticación permanente; un alcance anunciado sin operación probada sigue teniendo ese límite. Esta corrección específica no crea otra regla ni activa un scheduler.


## App, producto y login de Instagram — 4 de noviembre de 2026

Se indicó la app de Ads y sus scopes antes de inspeccionar los casos de uso reales. Coordinación comprobó en Chrome que ONIA Marketing API sólo ofrece dos casos de anuncios, mientras OnIA Social API ya dispone de mensajes/contenido Instagram. Corrección específica: revisar **producto + login + host** antes de pedir scopes; para el piloto propio se seleccionó Instagram Login existente y `graph.instagram.com`, con `instagram_business_basic`, `instagram_business_content_publish` e `instagram_business_manage_messages` listos para prueba en la UI. Ads queda separado en `graph.facebook.com`. No es una regla nueva ni autorización personal concedida.

Sólo se añadió el permiso de mensajería a la preparación existente. Cuentas anteriores y webhooks quedaron intactos; no se exportó el token visible en una captura. `@sergiourcullo` aún no conectado: Sergio completa Agregar cuenta, guarda el secreto por su mecanismo y publica onia; el ejecutor valida lectura cloud después. Evaluar Unified Login antes de producción, sin prometer permanencia o renovación automática. [Estado y alcance canónico](accesos.md#instagram-operativo-y-continuidad-de-autenticación).

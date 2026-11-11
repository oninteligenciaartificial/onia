# Cierre de fábrica para vender · 11 noviembre 2026 UTC

**Actualización del Q&A del 11-nov:** rigen las [confirmaciones directas de Sergio](DECISIONES-SERGIO-20261110.md#confirmaciones-directas-en-codex--11-nov-2026). Clases viernes 13 a las 20:00, sábado 14 a las 14:00 y lunes 16 a las 20:00, La Paz. Cobrador = QR y seguimiento con confirmación manual de Sergio. VSL confirmada. Los materiales y eventos con fechas anteriores deben corregirse antes de usarlos.

Sergio pidió terminar lo necesario para vender y ahora organizar panel, fábricas y sesiones. Se retoman las entregas existentes sin esperar al homelab. Este documento coordina requisitos y evidencia, no reemplaza estados del harness ni concede activación, envíos o cobros. El reparto de la intervención nocturna se conserva abajo como antecedente; la propuesta actual se detalla al final.

**Actualización del panel, 11-nov:** Sergio eligió Propuesta 1 y autorizó explícitamente «Sí, integrar ese panel». La entrega `94cca9bfaeba72ad6eee8bcf87db30d8c4d28083`, con revisión independiente favorable, quedó integrada y verificada en `origin/master` mediante `05b5d1e2ecf68dc9dda34742f107ad8dcd722084`. Se corrigió el guardado y se comprobó su persistencia y el recorrido en navegador. Esto no activa servicios, ejecución por horario ni canales comerciales. El flujo diario se construye aparte en `fabrica-automatizaciones-flujo-diario-20261111`; su estado vivo se consulta en el harness.

**Antecedente de la primera tanda:** el [dictamen de la coordinadora](../../04-operacion-agentes/evidencias/tanda-fabricas-20261111/REVISION-COORDINADORA-v1.md) conserva el fallo de guardado inicial del panel y las pruebas locales de guiones/WhatsApp. La sección final **Funcionamiento diario y siguiente tramo** describe la continuidad propuesta; sus pendientes deben cotejarse con el registro y las entregas posteriores, sin confundir construcción con recurrencia activada.

## Cadena que debe quedar completa

Contenido revisa guiones → Sergio ensaya y graba una tanda → Boss mueve a cola privada → script transcribe una vez y monta vertical/horizontal → Contenido y Sergio revisan → Sergio publica → consulta comercial → ficha y QR privado → Sergio verifica el movimiento → acceso a Meet → clase y soporte → medición de pagos reales.

La llamada a comentar NEGOCIO requiere un responsable o una automatización del canal comprobada. WhatsApp conectado por sí solo no responde comentarios ni DMs de Instagram/Facebook. No cambiar silenciosamente los CTAs. Propuesta para reducir dependencias si Sergio la elige: entrada directa a WhatsApp desde enlace de perfil; no aplicada ni publicada.

## Qué existe y qué bloquea uso real

| Requisito | Evidencia al arrancar | Próximo responsable / condición de cierre |
|---|---|---|
| Oferta única | DECISIONES-SERGIO: Claude de 0 a 100: tu negocio con IA; Bs50/Bs150; horario confirmado en Q&A del 11-nov | Cotejar todos los mensajes, guiones, bot y Calendar con esa fuente; corregir versiones vigentes, conservar evidencia histórica |
| Cinco guiones | Entrega 0a710ac, textos finales de Contenido; falta revisión del conjunto e incorporación al circuito de consulta | Codex integra técnicamente; Contenido/Sergio validan ensayo, duración y CTA |
| Montaje | Entrega 9c9a8a0; prueba sintética y ASR disponibles | Codex completa lote y formatos; Boss aporta crudo, Contenido/Sergio verifican resultado real |
| WhatsApp | fbc8747 es ensayo: QR/acceso ficticios, workflow manual sin webhook ni envíos; revisión formal cambios | Codex corrige BAJA/timeout y prepara adaptador; revisor distinto comprueba. No activar ese JSON de ensayo |
| Número Meta y credenciales | Estado actual desconocido; faltante documentado, sin prueba real | Sergio verifica número; Operaciones comprueba acceso y configuración privada. No pegar secretos en chat/Git |
| QR y Meet | No localizados en las entregas; búsqueda de Calendar por workshop sin resultados (no demuestra ausencia) | Sergio/Operaciones localizan y verifican medios privados, destino e importe |
| Comentarios/DMs IG y Facebook | Análisis documental, sin recepción/respuesta real demostrada | Boss/Operaciones identifican cuentas y permisos; prueba autorizada por canal. No declarar listo con una prueba de WhatsApp |
| Pago y acceso | Debe haber confirmación manual autenticada, referencia única y cupos VIP | Codex prueba lógica y persistencia; Sergio valida recorrido real con número de prueba y datos privados |
| Clase y entrega | Kit de primera práctica y primeros10min existentes; ensayo real de Claude pendiente | Sergio ensaya ejercicio, comprueba Meet/materiales y acceso a Claude; Contenido/Operaciones cierran soporte |
| Publicación/activación | Sin autorización nueva para acciones externas en este pedido de construcción | Entregar resultado concreto revisado y pedir sólo la activación/prueba externa necesaria |

## Coordinación de la intervención nocturna (antecedente)

Codex directo trabaja sobre código y documentación de integración. Un colaborador técnico tiene escritura exclusiva del paquete WhatsApp; Codex conserva edición, integración y comprobaciones. Boss no debe lanzar en paralelo otro ejecutor sobre estas rutas: puede reunir entradas privadas y revisión editorial con Operaciones/Contenido. La reserva de cuota90 está retirada; sigue máximo3 y >3 pendiente. Última muestra al arranque: 96% usado, 2026-11-11T01:55:50.291UTC; no implica saldo extra.

No se acepta una tarea antigua por incorporar sus archivos. Los registros anteriores conservan su revisión y dictamen; se publicará el commit y evidencia de las correcciones nuevas. Un test local no se etiqueta como prueba real de Meta, n8n o venta.

## Estructura de OnIA

Se conservan las seis fábricas y el panel existente. Venta del workshop y contenido son el frente inmediato. Meta Ads, venta de ONIA Platform y otros canales se mantienen identificados con sus requisitos; no forman un bloqueo artificial para corregir el circuito del workshop ni se presentan como construidos. No se crean nuevos bots, paneles o investigaciones de infraestructura.

La operación posterior al 14 exige también que Boss pueda ejecutar los programas fijos con su acceso restringido. Tener el script en Git no prueba ese permiso ni su ejecución desde Boss: comprobar ese paso antes de declarar operación sin Codex.

## Resultado de esta intervención

La tabla inicial es el diagnóstico de entrada. El cierre actual es:

| Entrega | Veredicto técnico | Pendiente operativo |
|---|---|---|
| Tanda T01–T05 v2 | Integrar: textos/hash cotejados, consulta en panel existente sin simular aprobación | Contenido/Sergio: ensayo, duración, CTA atendido, grabar y aprobar |
| Editor y lote VPS | Integrar: ASR, B-roll, subtítulos, vertical/horizontal; reutiliza transcripción; revisión independiente buena tras corregir dos fallos | Boss aporta material privado; Contenido/Sergio revisan encuadre y audio; probar mando desde puente sin Codex |
| WhatsApp | Integrar como preparado/deshabilitado: HMAC, persistencia, pagos manuales autenticados, referencias, VIP, BAJA, incertidumbre | Meta/número verificado; secretos/QR/media ID/Meet privados; HTTPS y WSGI; conectar n8n, aprobar textos/excepciones y probar de punta a punta |
| n8n de despacho | Plantilla inactiva manual revisada localmente, credencial separada del operador | Importación y compatibilidad con instancia real; luego despacho periódico autorizado, no declarado instalado |
| Coordinación Boss | Acuse publicado en 388043f del pedido de reunir entradas sin duplicar ejecutores | Boss debe completar esa coordinación en su chat principal; el acuse no acredita que ya encontró QR/número/Meet |

Evidencia y comandos: [revisión independiente](../../04-operacion-agentes/evidencias/cierre-venta-20261111/REVISION-INDEPENDIENTE.md), [contenido](../../04-operacion-agentes/evidencias/cierre-venta-20261111/PRUEBAS-CONTENIDO.md) y [adaptador](4-chatbot-whatsapp/trabajos/fabrica-chatbot-whatsapp-20261110/ADAPTADOR.md).

### Lo necesario para abrir la venta

1. Operaciones/Boss reúnen en privado número Meta verificado, acceso a la cuenta, QR correcto y tres enlaces Meet. Sergio informa qué está listo; no pegar claves ni QR en Git/chat.
2. Codex conecta la preparación al entorno autorizado con esos datos; primero una prueba limitada con el número propio de Sergio. Comprobar información → modalidad/QR → captura sin acceso → confirmación manual → enlace real, además de duplicado, BAJA y fallo de envío. Sin pagar dinero para simular una compra y sin contactar clientes durante el ensayo. No confundir este paso pendiente con los tests locales ya ejecutados.
3. Contenido/Sergio aprueban textos, tratamiento de pagos vencidos/VIP lleno y una pieza de venta; Sergio ensaya la práctica de Claude y graba. El CTA NEGOCIO necesita atención comprobada por su canal; la alternativa de enlace directo a WhatsApp sigue propuesta, no decisión tomada.
4. Con el recorrido concreto verificado, Sergio autoriza la activación, el despacho recurrente y la publicación comercial. No se da por abierta la venta antes de ese paso.

### Frentes que quedan abiertos, sin bloquear este cierre técnico

IG/Facebook comentarios y DMs, WhatsApp de ONIA Platform y Meta Ads no tienen prueba real en este cierre; sus ofertas/permisos/formatos siguen pendientes. Los tipos de anuncios y guiones son lista abierta; esta tanda no demuestra cobertura de todos ni contiene un relato real del día del founder. Homelab y más de3 sesiones siguen pendientes por decisión de Sergio. La continuidad automática tras el14 requiere comprobar ejecución de scripts desde Boss antes del corte; no es requisito para usar hoy el editor desde Codex.

No se han activado servicios/n8n ni enviado mensajes a clientes. La publicación de código/evidencia en GitHub y el aviso técnico a Boss no equivalen a publicación comercial.

## Plan de sesiones del Q&A del 11-nov — primera tanda ejecutada, siguientes propuestas

La primera tanda de este plan se autorizó y ejecutó después de redactarlo. Su cierre y sus límites están en el dictamen enlazado al principio. Las muestras de cuota y estado de esta sección son antecedentes fechados; no son el estado vivo. Las sesiones siguientes siguen propuestas.

### Método aprendido de los videos

Se releyó íntegramente el contenido hablado disponible de ambos videos, usando las transcripciones ya conservadas, sin repetir ASR ni extraer más fotogramas. No se acredita un nuevo visionado o escucha continua.

- [Video 1, desde 16:14](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=974s): atomizar hasta un resultado evaluable; definir qué hace bueno a cada resultado antes de producirlo. Desde 20:34: entrada, pasos, salida, medición y aprendizaje. Desde 24:08: sala de montaje con versiones, fallos visibles y correcciones.
- [Video 2, desde 8:06](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=486s): contexto pertinente y ejemplos; desde 14:04, herramientas/instrucciones/memoria persistente; desde 24:30, especialistas por paso y disparadores por archivo u horario.
- Aplicación: cerebro selecciona fuentes y criterios → tarea pequeña → resultado → revisión independiente → decisión humana cuando corresponda → evidencia y corrección reutilizable. Aprender significa conservar una corrección y comprobarla en otra pieza; no entrenar pesos ni convertir opiniones de personas simuladas en ventas reales.
- Reutilizar cerebro, panel, editor y harness de OnIA. Las máquinas, modelos y servicios pagados de Euge no son requisitos ni permisos para OnIA.

### Coordinación y contexto

Propuesto: Codex coordina este frente directamente con el harness; Boss puede reunir entradas privadas o aportar revisión editorial si está disponible. La bitácora nueva informa otros agentes usando onia-llm: eso no prueba que sus ejecuciones estén registradas en el harness. Antes de lanzar, comprobar actividad y asignaciones para evitar dos coordinaciones o consumos no contabilizados.

Cada sesión recibe objetivo, decisiones vigentes, fuentes seleccionadas del cerebro, entrega exacta, rutas exclusivas, dependencias y criterios de aceptación. Lee BITACORA-BOSS y DECISIONES primero; no carga indiscriminadamente todo el historial. El registro canónico del harness decide el estado, la bitácora da contexto y Git conserva entregas.

Consulta del registro canónico a 2026-11-11T12:12:15Z: ninguna sesión viva en esa base. No es una auditoría de procesos de todas las otras máquinas. Cuota informada por el proveedor: 1% usado a 12:11:58Z, ventana semanal y reinicio 18-nov 12:05:02Z. Sustituye para esta planificación la muestra anterior de 98%; causa del cambio y continuidad de la suscripción no comprobadas. Leer de nuevo antes de lanzar; no prometer gasto o capacidad futura con esa muestra.

### Primera tanda: tres resultados independientes

| Lugar | Sesión y reutilización | Escritura exclusiva | Entrega y prueba de aceptación |
|---|---|---|---|
| 1 | Panel operativo; retomar cerebro-panel-usable-20261109 después de actualizar su alcance | 05-herramientas/fabrica-contenido/20261109-lector-panel/ | Ampliar panel existente: fábricas, pasos, resultado, revisión, bloqueos y calendario. Primer recorrido reproducible con una tarea y una corrección persistida; distinguir datos de prueba del estado real. No anunciar producción ni conexión real antes de probarlas. |
| 2 | Guiones y calendario; nuevo resultado propuesto guiones-tanda-automatizada-20261111; reutilizar cerebro y tanda v2 | 05-herramientas/fabrica-onia/1-guiones-calendario/ | Generador/procedimiento con noticias fechadas y enlazadas, ideas filtradas y cinco guiones útiles, calendario, CTA atendible y marca personal. Versiones nuevas con horarios actuales; si falta noticia verificable, evergreen identificado. Ensayar una tanda diaria de cinco ideas/piezas con variantes horizontal y vertical; una corrección debe reflejarse en la siguiente salida sin perder el original. La recurrencia automática no queda probada con esa tanda local. |
| 3 | Cierre de venta; retomar fabrica-chatbot-whatsapp-20261110 con nueva entrega y revisión | 05-herramientas/fabrica-onia/4-chatbot-whatsapp/ | Reusar adaptador y pruebas. Corregir fechas y el límite temporal de configuración que dependía del sábado 14; preparar QR/seguimiento/confirmación manual/acceso. Verificar duplicados, BAJA, pago no confirmado y fallo incierto. La prueba real depende de datos privados y autorización concreta; los tests locales no la sustituyen. |

No son tareas registradas o sesiones en ejecución por aparecer en esta tabla. El coordinador reserva rutas en el registro antes de escribir y resuelve reservas antiguas sin aceptar entregas por accidente. Los documentos compartidos de decisiones y estado quedan con un único escritor: el coordinador. Los productores consumen un contrato de datos pequeño acordado antes del arranque; no se editan mutuamente los archivos.

Sol6.1 high para implementación y revisión técnica complejas; low para tandas de texto acotadas, inventarios y consultas. Sin hijos por defecto ni ultra nuevo. Cada lanzamiento declara modelo, esfuerzo y recibo observado; usar tres lugares no significa abrir otros agentes fuera del contador.

### Rotación y cierre de cada resultado

1. Consultar registro, permisos, cuota y dependencias; reutilizar el ID existente cuando sea el mismo objetivo. Preparar/actualizar briefing y asignar rutas. No usar dry-run sobre un ID que se vaya a lanzar después.
2. Lanzar o reanudar una ejecutora con revisión esperada vigente, modelo explícito y autenticación incluida; comandos y sintaxis en ORQUESTACION.md. Máximo tres sesiones principales vivas, contando revisores; la coordinadora de este chat también consume cuota aunque no sea una sesión CLI registrada.
3. Al terminar, verificar proceso, commit y rama remota. Una entrega no localizada no se etiqueta como fallida ni se relanza hasta conciliar el resultado.
4. Cerrar con conservación del worktree. El primer lugar liberado recibe un revisor distinto sobre el commit exacto; recoger mediante revisar --recoger --conservar-worktree. Fin de ejecutor y fin de revisor son eventos diferentes; no repetir cerrar al terminar el revisor.
5. Si pide cambios, retomar la misma tarea y revisar el commit nuevo. Sólo con dictamen bueno vigente y autoridad aplicable, aceptar e integrar de a una a master; comprobar el conjunto y el hash remoto. No equiparar aceptación técnica a autorización comercial.
6. Guardar siguiente acción concreta y desbloquear la siguiente sesión preparada. Durante esta operación el coordinador hace el despacho; no se acredita una cola automática o actividad entre turnos por escribir este plan.

Si un frente espera una credencial o una grabación, conserva el bloqueo visible y libera su lugar para trabajo independiente. Una pregunta de Sergio no cancela las tareas. No prometer que nunca faltará información: toda falta debe tener responsable, siguiente paso y prueba de cierre.

### Siguientes sesiones en lugares liberados

La enumeración no es una cola rígida. Tras la revisión pendiente, VSL, materiales del curso y conciliación de horarios tienen prioridad en el primer lugar compatible que se libere por su fecha de uso y el corte del 14; no esperan al homelab ni a terminar toda la sala de montaje. Codex coordina la comprobación de Calendar/Meet con acceso de lectura; Boss/Calendario pueden aportar los enlaces privados. Los cambios de eventos se aplican dentro de la autorización correspondiente y se releen después; no se da por corregido Calendar por corregir este archivo.

- **Sala de montaje:** retomar fabrica-edicion-video-20261110 para conectar lote existente al contrato del panel, comparar original/versión y registrar motivos. Autor de editor escribe sólo 2-edicion-video; autor de panel incorpora UI por separado. Probar una grabación real de la tanda de cinco guiones de Sergio: cinco piezas en horizontal y cinco en vertical, una sola transcripción de la tanda y una corrección solicitada. Distinguir esa aceptación de lote de la recurrencia diaria todavía no comprobada. El vlog queda excluido. Falta esa grabación y la validación perceptiva.
- **VSL, anuncios y curso/VIP:** derivar de oferta, cerebro y guiones actuales el video de venta, piezas y ejercicios/materiales de las clases. Sin promesas o testimonios inventados. Ensayar duración y demostración real; Sergio graba y decide publicación. Lista abierta de formatos, sin compra de Higgsfield o pauta implícita.
- **Instagram/Facebook y n8n:** reutilizar análisis existente, comprobar permisos de las cuentas y construir comentarios/DMs → conversación comercial como entregas por canal. Cada canal tiene prueba propia; WhatsApp no los valida. Configurar y activar lo real sólo con autorización aplicable.
- **Homelab:** mantener homelab-conexion-20261109. Cuando DESKTOP-0GGGNMF esté disponible, ejecutar el diagnóstico PE ya revisado una vez y seguir su resultado. Después probar usuario aislado, acceso y trabajo real. La PC apoyará procesamiento cuando esté comprobada; edición actual sigue en el VPS. Laptop excluida y ampliación sobre tres sesiones pendiente.

Meta Ads y WhatsApp de ONIA Platform siguen visibles en la estructura, con sus requisitos, y no se presentan como operativos ni bloquean vender este workshop. No confundir terminar una primera cadena de ingresos con automatizar toda la empresa.

### Lo que debe sobrevivir al 14

Preparar antes del corte guiones/procedimientos, VSL y materiales, clases y enlaces con horario correcto, scripts fijos y forma probada de ejecutarlos, y acceso/soporte para el lunes 16. Un programa fijo puede continuar sin Codex; investigar noticias nuevas, escribir con un LLM o decidir excepciones necesita un operador o modelo efectivamente disponible. No se presume sustituto pagado ni servicio autónomo por tener instrucciones guardadas.

## Funcionamiento diario y siguiente tramo — propuesta del 11-nov

Pedido de Sergio después del STOP: explicar si cada apartado es una sesión, cómo se actualiza cada día, cómo entra una noticia de Anthropic, dónde ve automatizaciones y chatbot, y continuar el plan siguiendo a Euge. No se ha autorizado por este texto una activación comercial ni otra tanda automática.

### Una fábrica es un proceso; una sesión hace un trabajo acotado

Se conservan las seis fábricas. Cada una tiene entradas, pasos, resultados comprobables, revisión y correcciones. Puede necesitar varias sesiones en distintos momentos, además de pasos sin modelo. No se asigna un LLM permanente a cada pestaña ni se lanza una sesión por cada operación trivial.

| Parte | Trabajo previsto | Cuándo necesita sesión |
|---|---|---|
| Panel existente | Mostrar calendario, resultados, versiones, pendientes y última actualización comprobada | Para construir/corregir funciones; consultarlo no requiere LLM |
| n8n existente y programas fijos del VPS | Disparadores por horario/entrada, lecturas de fuentes, validaciones, edición y despacho autorizado | No para cada ejecución determinista; desarrollo y excepciones pueden requerirla |
| Harness existente | Registrar tareas, reservar rutas, lanzar/retomar y conservar entregas/revisiones | Los trabajos de razonamiento/redacción/código usan los tres lugares compartidos, incluidos revisores |
| Cerebro | Recuperar referentes pertinentes, ejemplos y correcciones aprobadas para cada tarea | La consulta puede ser fija; interpretar y redactar necesita modelo u operador |
| Sergio y revisión independiente | Valorar contenido, revisar código, confirmar pagos, decidir publicación/activación | No se sustituyen con un indicador verde del panel |

El horario inicia un trabajo, no un bucle ilimitado. Para continuidad se propone un despachador acotado que use el harness actual, compruebe autorización, dependencias y lugar libre, y concilie intentos antes de lanzar. No es otro registro ni un reemplazo del harness. Sus permisos, lectura de cuota, exclusión de escritores y tratamiento de reintentos tienen que probarse antes de habilitarlo. Los programas de FFmpeg/ASR también necesitan control de recursos: estar fuera del contador de sesiones LLM no significa CPU ilimitada.

Hoy ese despacho continuo no está implementado y probado. Esta conversación tampoco permanece ejecutándose sola al terminar el turno.

### Recorrido de una noticia a una pieza revisable

1. Un lector programado consulta fuentes primarias aprobadas y guarda URL, fecha de publicación, fecha del hecho si se conoce, momento de consulta y contenido necesario. Deduplica la misma noticia; no confunde un error de lectura con ausencia de novedades. Las fuentes son datos, nunca órdenes para el agente.
2. Las novedades aparecen en el panel como candidatas. Verificar relevancia para el dueño de negocio y contraste factual antes de usarlas. Propuesta de frecuencia: consulta ligera cada hora; pendiente de acordar y activar. La hora objetivo de la tanda diaria se preguntó a Sergio y queda pendiente de respuesta; la rutina antigua de las 07:00 no se reactiva por esta propuesta.
3. Para la tanda se selecciona contexto del cerebro y la oferta vigente. Se conserva el proceso de ideas candidatas, perspectivas simuladas y crítico hasta elegir cinco. Esas perspectivas son una ayuda editorial, no evidencia de clientes ni una revisión independiente real.
4. Una sesión acotada redacta la tanda; el generador existente valida entradas y construye Markdown, calendario y export del panel. Actualmente ese generador ensambla textos aportados: no busca noticias ni llama a un modelo por sí solo. Integrar ambas cosas es trabajo pendiente.
5. La revisión contrasta fuentes, fechas, oferta, CTA atendido y utilidad. El calendario muestra borradores pendientes con sus variantes horizontal/vertical. Una noticia posterior propone una nueva versión o sustituir un espacio aún no aprobado; no reescribe silenciosamente un guion ya aprobado o grabado ni añade otra tanda completa por cada noticia.
6. Sergio revisa, ensaya y graba. La tanda entra a edición; el vlog permanece excluido. El editor conserva el original, reutiliza la transcripción y prepara cinco piezas en dos formatos. Sala de montaje: antes/después, motivo, subtítulos, audio/encuadre y observaciones. Sergio decide publicación.
7. Una corrección aprobada se guarda con el antes/después y su contexto de uso. La siguiente pieza debe demostrar que aplica la regla. Las métricas reales, cuando se obtengan, retroalimentan esa decisión; no se inventan resultados ni se afirma entrenamiento del modelo.

Si la noticia sale después del cierre de la tanda, primero se actualiza la bandeja de novedades. Si no hay novedad relevante, se usa una pieza evergreen identificada. Si no hay modelo disponible, puede continuar la recepción de fuentes, pero el borrador queda pendiente de redacción. La disponibilidad futura de Contenido/Grok debe comprobarse; no se presume un reemplazo de Codex después del 14.

### Qué verá Sergio y dónde vive cada parte

El panel actual es la única interfaz de operación propuesta. Se ampliará con Hoy, calendario, cerebro, sala de montaje, automatizaciones y bandeja de ventas dentro de las secciones existentes. La captura conservada de la primera tanda contiene material histórico y un ensayo rotulado; no se presenta como la interfaz final conectada.

- **Actualización del panel:** cada productor persiste su resultado y export validado; el panel lee una proyección y se refresca mientras está abierto. Se debe mostrar la fecha de la fuente y el último éxito, no cambiar la fecha para aparentar frescura. Una caída deja visible el último resultado y el error. La página cerrada no detiene los trabajos del VPS. Ese refresco y la reunión de los nuevos exports todavía faltan.
- **Automatizaciones:** el panel mostrará finalidad, disparador, estado comprobado, última ejecución, resultado, fallo y siguiente acción. El detalle técnico se abrirá en la instancia privada de n8n, cuyo historial permite inspeccionar ejecuciones. No hace falta otra pantalla de Codex para operar. La proyección debe omitir credenciales, payloads personales y enlaces autenticados.
- **Chatbot:** el cliente conversa por WhatsApp. Se propone alojar el adaptador existente como servicio del VPS, con almacenamiento privado persistente; sólo la recepción de Meta se expondrá por HTTPS. n8n despachará los mensajes autorizados. La bandeja de operador será privada dentro del panel, con pendientes, bajas, envíos inciertos y acción de confirmar un pago tras comprobarlo en el banco. Esa bandeja visual, alojamiento y conexión real siguen pendientes; los endpoints locales ya probados no los sustituyen.
- **Roles del bot:** preguntas previstas y QR pueden resolverse con la lógica fija existente, sin una sesión Codex por cliente. Una excepción queda para el operador. La captura no concede acceso; Sergio confirma el pago y el sistema entrega el enlace cuando la conexión esté probada y autorizada. El chatbot de WhatsApp no valida los comentarios/DMs de Instagram o Facebook.
- **Acceso y continuidad:** falta probar el acceso privado desde el teléfono/PC de Sergio y definir la ubicación persistente fuera de Git, respaldo y recuperación. No publicar el panel ni los endpoints de operador como una web abierta. No hay una URL de operación del panel confirmada en esta entrega.

Documentación primaria consultada el 11-nov: [Schedule Trigger de n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/) para horarios y zona del workflow; [historial de ejecuciones](https://docs.n8n.io/workflows/executions/all-executions/) para inspección. Debe cotejarse con la versión instalada; esta consulta no la verificó. Usar America/La_Paz explícitamente y probar el cambio de día. Publicar/activar un flujo sigue requiriendo el sí aplicable.

### Siguiente tramo con resultados y paradas de revisión

| Frente propuesto | Reutilización y responsable | Condición para darlo por listo |
|---|---|---|
| 1. Panel utilizable y conjunto integrado | Codex retoma cerebro-panel-usable-20261109; el revisor examina el commit nuevo. Una sola escritora del panel | Corregir el 403 al guardar sin relajar controles; usar guiones v3 y export WhatsApp actuales; observar una revisión conservada tras reinicio, recorrido escritorio/móvil y estados reales sin fixtures confundibles. Integrar sólo tras revisión válida |
| 2. Noticias y tanda recurrente | Codex, fábrica de automatizaciones y generador de guiones existentes; separar rutas de disparador y contenido | Una noticia nueva crea una candidata y un borrador trazable; repetir el evento no duplica; fallo de fuente queda visible; cambio de día crea otra tanda; sin modelo queda pendiente. Probar primero con datos controlados, luego una fuente real. La prueba de horario real viene al autorizar activación |
| 3. Venta completa del workshop | Codex retoma fabrica-chatbot-whatsapp-20261110; Sergio aporta decisiones/activos privados y confirma pagos | Preparación de servicio y bandeja de operador revisada; Calendar/Meet conciliados con 13/14/16; después prueba autorizada con Sergio: consulta, QR, captura sin acceso, confirmación manual, acceso, duplicado, BAJA y envío incierto. No usar dinero real para fingir una venta |
| 4. VSL, curso y sala de montaje | VSL/materiales en el primer lugar compatible libre; reutilizar editor actual para la grabación | Texto/ejercicio real ensayado, materiales de tres clases disponibles y enlaces correctos; cinco piezas en dos formatos revisadas con audio/imagen y una corrección aplicada. El curso del lunes 16 no depende de Codex |

Tres lugares como máximo, con rotación de ejecutores y revisores; un lugar esperando credenciales se libera para VSL/materiales. La persona que modifica el panel incorpora también la bandeja visual para no solapar escritores. No abrir más sesiones sólo por ocuparlas. Cada frente se entrega con resultado visible y se detiene en su revisión; el siguiente paso automático sólo se habilita si tiene permiso, entradas y criterio de aceptación cumplidos. No se ha registrado ni lanzado esta segunda tanda por documentarla.

IG/Facebook se prueba por canal y conserva el pendiente del CTA NEGOCIO. Si Sergio elige abrir primero por enlace directo a WhatsApp, se cambia de forma explícita la oferta/CTA y se prueba ese recorrido; no se da por hecho. Meta Ads y WhatsApp Platform quedan visibles como pendientes de su propio alcance. Homelab sigue como apoyo futuro cuando complete su diagnóstico; no aloja ahora el bot ni es condición para vender con el VPS. La ampliación de tres sesiones continúa pendiente.

**Demostración de cierre propuesta:** Sergio abre el panel, ve entrar una noticia identificada, revisa un guion, guarda una corrección y la encuentra tras reiniciar. Luego ve el montaje de su grabación y recorre el bot con su número de prueba. Cada resultado tiene versión, evidencia y responsable; los pasos pendientes no aparecen como completados. Antes de llamar al sistema diario o continuo, comprobar también un disparo real por horario y recuperación tras reinicio sin duplicar trabajo.

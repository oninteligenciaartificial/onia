# Cierre de fábrica para vender · 11 noviembre 2026 UTC

**Actualización del Q&A del 11-nov:** rigen las [confirmaciones directas de Sergio](DECISIONES-SERGIO-20261110.md#confirmaciones-directas-en-codex--11-nov-2026). Clases viernes 13 a las 20:00, sábado 14 a las 14:00 y lunes 16 a las 20:00, La Paz. Cobrador = QR y seguimiento con confirmación manual de Sergio. VSL confirmada. Los materiales y eventos con fechas anteriores deben corregirse antes de usarlos.

Sergio pidió terminar lo necesario para vender y ahora organizar panel, fábricas y sesiones. Se retoman las entregas existentes sin esperar al homelab. Este documento coordina requisitos y evidencia, no reemplaza estados del harness ni concede activación, envíos o cobros. El reparto de la intervención nocturna se conserva abajo como antecedente; la propuesta actual se detalla al final.

**Actualización del panel, 11-nov:** Sergio eligió Propuesta 1 y autorizó explícitamente «Sí, integrar ese panel». La entrega `94cca9bfaeba72ad6eee8bcf87db30d8c4d28083`, con revisión independiente favorable, quedó integrada y verificada en `origin/master` mediante `05b5d1e2ecf68dc9dda34742f107ad8dcd722084`. Se corrigió el guardado y se comprobó su persistencia y el recorrido en navegador. Esto no activa servicios, ejecución por horario ni canales comerciales. El flujo diario se construye aparte en `fabrica-automatizaciones-flujo-diario-20261111`; su estado vivo se consulta en el harness.

**Actualización del flujo diario, 11-nov:** primera cadena comprobada por la coordinadora con fuente y redacción reales, revisión independiente y panel; parada en revisión editorial, sin duplicados al repetir el tick. Producto del flujo `9a4639f`, dictamen bueno r41; tanda `3d50b82`, dictamen bueno r16. [Evidencia y límites](../../04-operacion-agentes/evidencias/flujo-diario-real-20261111/REVISION-COORDINADORA.md). Flujo/generador siguen en rama esperando aprobación de integración; horario pendiente y programación deshabilitada. Esto no acredita automatización comercial ni continuidad de un modelo después del 14.

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

## Plan completo para operar desde el 12-nov — PROPUESTO, 11-nov 15:45 La Paz

Pedido actual de Sergio: preparar el plan integral, estimar tiempos y trabajar mediante el harness sin pedirle un prompt por cada paso. Prioridades explícitas: cerebro corregible, guiones, anuncios Meta, contenido con IA, edición, WhatsApp y automatizaciones de Instagram/Facebook. Este pedido incorpora anuncios y contenido IA al desarrollo inmediato; sustituye su posición de espera en las propuestas anteriores. La publicación comercial y el gasto conservan sus permisos propios.

Este bloque es una propuesta revisable. No registra ni lanza tareas, no activa servicios y no amplía por sí solo permisos. Se presenta en el chat antes de publicar el plan acordado en master. Los IDs nuevos que aparecen abajo son propuestos; no se describen como tareas ya registradas.

### Punto de partida comprobado

- Master contrastado: `6d81c694dd37a3738ee4c0d756fc081d079f9654`. Panel Propuesta 1 integrado. Flujo `9a4639f`, generador `26c39e3` y WhatsApp `46944fb` tienen dictámenes buenos, pero sus integraciones pendientes deben resolverse como parte del siguiente lote autorizado.
- Cero sesiones vivas; cuota usada 18%, lectura `2026-11-11T19:39:04.466Z`. Muestra de VPS: 15.6 GiB RAM, 10.4 GiB disponibles; es una instantánea, no un ensayo de capacidad. No hay límite de seis altas ni reserva del 90%; siguen tres sesiones simultáneas, incluidos revisores.
- La cadena real de guiones ya alcanzó revisión editorial con un escritor y un revisor, sin duplicados. Su código contiene un controlador diario específico, deshabilitado. Un despachador general de desarrollo desatendido aún no está implementado ni probado.
- DESKTOP-0GGGNMF aparece online en el daemon Tailscale existente. Su usuario, aislamiento, conexión SSH y continuidad del worker no están aceptados. Falta ejecutar el diagnóstico PE revisado desde la PC y conciliar su resultado. La laptop queda excluida.
- El catálogo del cerebro existente contiene 19 referentes y 23 patrones seleccionados. Se reutilizan catálogo, fichas y fuentes. Los errores del historial no se convierten en decisiones vigentes por volver a cargarlos.

### Resultado que se construye y cómo se acepta

| Apartado | Entrega concreta | Prueba de aceptación |
|---|---|---|
| Hoy y operación | Un panel privado en el VPS accesible desde el teléfono, con trabajos en curso, resultados, bloqueos, siguiente acción y última actualización real | Abrir desde un cliente autorizado; autenticar; revisar un resultado; reiniciar el servicio y conservar datos. El acceso local del desarrollador no acredita el del teléfono |
| Cerebro | Buscador de decisiones, oferta, audiencia, voz de Sergio, referentes, procesos, ejemplos buenos/malos, fuentes y correcciones, con fecha y versión | Recuperar una decisión vigente, distinguirla de la sustituida y comprobar que el briefing de una tarea utiliza la versión correcta. Mostrar conocimiento documentado de OnIA, sin volcar secretos, conversaciones completas o instrucciones internas del proveedor |
| Corrección en cualquier sección | Botón común para indicar qué está mal, cambio deseado y alcance; guardar original, propuesta, resultado y revisión | Corregir guion, anuncio, montaje y respuesta del bot con la misma mecánica; generar versión nueva; un formulario o dictamen antiguo no puede aprobarla. Las correcciones no se quedan sólo en una nota |
| Guiones y calendario | Noticias primarias, ideas, cinco piezas diarias, variantes horizontal/vertical, locución, planos, CTA y calendario | Tanda real con fechas y oferta actuales; noticia repetida no duplica; fuente fallida se distingue de ausencia de novedades; revisión técnica y editorial separadas. El vlog diario no se edita |
| Anuncios Meta y VSL | Objetivo, audiencia, ángulo, oferta, textos, guion, piezas, formato y destino; vista previa y variantes; VSL del workshop | Un paquete completo coherente con precio/horarios/CTA y versiones; formatos ampliables. Se distinguen borrador local, pieza exportada, anuncio creado y campaña activa. Sin testimonios o métricas inventados |
| Contenido con IA | Cola de recursos, instrucciones, referencias, proveedor, crédito autorizado por pieza, resultado y procedencia; conexión con edición | Un recurso aprobado entra a la sala de montaje conservando origen e instrucciones. Preparación y generación real aparecen como etapas distintas. Higgsfield sólo se ejecuta con el sí vigente para esa pieza; no se presume que la suscripción incluya API o créditos ilimitados |
| Edición y sala de montaje | Entrada de grabación/B-roll, transcripción reutilizable, cortes, subtítulos, formatos, comparación antes/después y motivo de cada cambio | Una tanda real de Sergio produce cinco piezas horizontales y cinco verticales; revisión perceptiva; corrección de una pieza sin repetir la transcripción ni sobrescribir el original. Registrar resolución/fps y tiempos medidos antes de prometer rendimientos |
| WhatsApp del workshop | Conversación, ficha, QR privado, seguimiento permitido, pendientes de pago, confirmación manual de Sergio, acceso y soporte | Probar con interlocutor de ensayo autorizado: consulta, QR, captura que no concede acceso, confirmación, acceso, duplicado, BAJA, reinicio y envío incierto. Un envío incierto no se repite a ciegas |
| Instagram y Facebook | Comentarios/NEGOCIO, DMs, derivación, registro y control humano | Prueba separada de comentario y DM en cada cuenta/canal, con IDs de recepción y respuesta; demostrar la derivación a venta. Un webhook sintético o WhatsApp funcionando no acredita IG/Facebook |
| Métricas y continuidad | Piezas aprobadas/publicadas, consultas, pagos confirmados, pendientes y errores; materiales de clases y VIP | Contar sólo hechos registrados; reconciliar fechas de Calendar/Meet 13/14/16; materiales y acceso del lunes 16 disponibles sin depender de Codex |

Se amplía Propuesta 1. Una sola sesión escribe la interfaz y sus componentes compartidos; cada productor entrega un contrato de datos. Anuncios y contenido IA son vistas del trabajo correspondiente dentro de las seis fábricas existentes, no seis bots nuevos. La revisión visual incluye móvil, estados vacíos/error, carga, guardado y accesibilidad básica, además de capturas.

### Cómo se convierte una corrección en aprendizaje útil

1. La corrección autenticada identifica objeto, versión y alcance. Lo que Sergio corrige directamente autoriza ese cambio dentro de su alcance; una inferencia del agente queda como propuesta.
2. Se conserva el antes/después y se crea o retoma la tarea correspondiente con un ID estable. Se marcan los resultados dependientes que necesitan nueva revisión; una corrección de oferta no reescribe silenciosamente un video aprobado o publicado.
3. Una sesión acotada aplica el cambio, otra revisa cuando corresponde y el panel muestra la versión nueva y la prueba. Si falta un dato, muestra responsable y siguiente acción.
4. Una lección reutilizable actualiza la fuente existente de reglas/skills con ejemplo de aplicación y contraejemplo. Se comprueba el caso que falló y uno próximo donde la regla no debe aplicarse. No se agregan instrucciones a todas las sesiones ni se adopta una preferencia global por una corrección local.
5. El cerebro distingue corrección registrada, aplicada y comprobada en una salida posterior. Es mejora de contexto y procedimientos, no reentrenamiento del modelo ni garantía de ausencia de errores.

### Dos recorridos distintos en el mismo harness

**Desarrollo del lote:** tarea autorizada y elegible → ejecutor → pruebas → commit de rama → cierre comprobado → revisor distinto → correcciones si hacen falta → aceptación técnica autorizada → integración secuencial → comprobación conjunta → siguiente dependencia. La aprobación del lote debe permitir estas transiciones técnicas completas para evitar pedir un sí por cada commit. Sólo dictámenes buenos del commit exacto permiten avanzar.

**Operación diaria:** horario o entrada → fuente/cerebro → resultado → revisión → corrección → decisión editorial o comercial de Sergio. Estos recorridos persisten en el VPS; el chat no se promete como un proceso que continúa ejecutándose al terminar un turno.

El despachador se añade al harness existente y usa su registro canónico, asignaciones, revisión esperada e índice global. Un manifiesto del lote referencia IDs, dependencias, rutas, criterios y permisos; no duplica estados. Un lock y eventos persistidos impiden doble despacho. Antes de actuar coteja autor, commit, SID y permiso vigente; un evento incierto se concilia antes de repetir.

Propuesta de control: máximo tres sesiones globales; dos productores y un revisor rotativo. Si todavía no hay nada que revisar, el tercer lugar puede ejecutar una tarea corta independiente. No llenar los tres lugares con trabajos largos y dejar las revisiones esperando. Un único trabajo CPU pesado inicial; medir su impacto y no atribuir al homelab capacidad todavía no probada.

El loop toma sólo tareas del lote aprobado. No inventa objetivos, no cambia sus permisos, no modifica su propia política activa y no consume cuota sólo para consultar el estado. Sol low para pasos simples; high para diseño, integración o fallos complejos; sin hijos, sin ultra ni compras implícitas. Registra modelo solicitado y observado por separado, cuotas fechadas, SID, intentos y entregas.

Paradas propuestas: STOP o revocación, proveedor no disponible, cuota insuficiente/desconocida para un nuevo despacho, evidencia incierta, conflicto de rutas o necesidad de un permiso externo. Dos correcciones consecutivas sin progreso comprobable detienen sólo esa tarea y escalan el diagnóstico a la coordinadora; las otras siguen si son independientes. Esto no restaura topes diarios ni la reserva del 90%. Cambiar el ID no elude una parada.

Antes de dejarlo desatendido: probar tarea terminada pero no cerrada, fin de revisor, evento duplicado, corte antes/después de lanzar, commit distinto al revisado, reinicio, agotamiento del proveedor y STOP. Guardar recibo y demostrar un avance real a la siguiente dependencia. Hasta entonces la coordinadora puede trabajar activamente con el harness, pero no se declara autonomía entre turnos.

### Reparto de sesiones y rutas

| Orden / trabajo | ID y propiedad propuesta | Dependencia |
|---|---|---|
| Integrar lo ya revisado y preparar acceso privado | Retomar flujo diario, generador y WhatsApp existentes; coordinadora integra uno a uno | Sí de alcance al lote; revisar estado actual antes de aceptar |
| A: despachador de desarrollo | Nuevo propuesto `fabrica-codigo-continuidad-lote-20261111`; `05-herramientas/scripts/` y evidencia propia | Reutilizar diseño de carriles/recuperación; no reconstruir el harness |
| B: cerebro, correcciones y panel | Retomar `cerebro-panel-usable-20261109`; panel y catálogo/documentos de cerebro expresamente asignados | Contratos pequeños acordados con productores; sólo B modifica UI |
| C: revisión y trabajo editorial corto | Revisores distintos sobre cada entrega; mientras no haya entrega, VSL/anuncios/materiales en un encargo de marketing propuesto | Slots y rutas libres, sin escribir panel ni reglas comunes |
| Venta y canales | Retomar `fabrica-chatbot-whatsapp-20261110`; después nuevo propuesto `fabrica-automatizaciones-meta-canales-20261111` bajo su subruta de automatizaciones | Cuenta/número, credenciales privadas y permisos del canal; contrato del panel |
| Recursos IA y edición | Retomar `fabrica-edicion-video-20261110`; separar subrutas antes de delegar si hay más de un productor | Grabación/B-roll; generación Higgsfield por pieza autorizada |
| Homelab | Retomar `homelab-conexion-20261109`; exclusivamente documentación/instalador asignados y PC de casa autorizada | Diagnóstico PE, aislamiento y SSH comprobados antes de recibir trabajo |

Estos son trabajos lógicos, no siete sesiones concurrentes. Las tareas completadas liberan lugar para la siguiente elegible. Los bloqueos de Meta o una grabación no detienen cerebro, guiones, VSL o materiales. Antes del primer lanzamiento quedan registrados el ID, rutas exactas, herramientas/skills leídas, cuota actual, aceptación y comando real; no se inventa hoy un número de revisión futura.

### VPS, homelab y Boss

El VPS aloja el panel autenticado, datos privados, despacho y servicios de integración; los puntos de entrada externos se exponen con la autenticación/verificación correspondiente. El despliegue prepara recuperación y conserva originales. Se reutiliza el acceso existente si sirve, sin comprar dominio o hosting; comprobar la URL desde el teléfono es un requisito de entrega, no basta una captura del servidor.

Homelab: ejecutar una vez el diagnóstico revisado mientras está online, corregir la causa comprobada y probar host key fijada, usuario aislado, ausencia de acceso a archivos Windows y continuidad. Tras aceptar el worker, destinarlo inicialmente a ASR/render y pruebas que requieran CPU; los bots siguen en el VPS. Si la PC cae, conservar el trabajo y conciliar su último estado antes de reenviarlo. No sumar recursos físicos equivale a ampliar cuota de modelos. La medición de más de tres sesiones continúa pendiente.

Codex coordina este lote técnico. Boss puede reunir accesos y entradas mediante sus conectores autorizados; Contenido mantiene revisión editorial. No se crean bots nuevos y no se le entrega a cada ejecutor el historial entero: recibe el objetivo, decisiones vigentes, fuentes pertinentes y criterios de su tarea. Las tareas del VPS avanzan sin esperar a Boss cuando tienen sus entradas.

### Estimación de entrega y alcance de esta noche

Estimaciones de tiempo transcurrido desde la aprobación y el arranque, usando hasta tres lugares incluyendo revisión. No son tiempos sumables ni promesas de resultado; contemplan trabajo simultáneo y una ronda razonable de correcciones.

| Hito | Estimación | Qué debe poder usarse |
|---|---|---|
| H0 | 45–90 min | Integraciones revisadas, acceso privado preparado y primera prueba del panel en su alojamiento |
| H1 | 2–4 h | Despachador acotado probado, tanda/calendario y primera versión del cerebro con correcciones trazables |
| H2, objetivo de esta noche | 6–8 h | Panel de operación, guiones revisables, paquete de anuncios/VSL, cola IA/edición y bandeja de ventas; cada sección muestra su capacidad real y pendiente |
| H3 | 12–20 h de desarrollo/verificación transcurridos | Recorridos prioritarios completos con materiales reales y correcciones probadas, condicionado a entradas y accesos |

WhatsApp/IG/Facebook en producción requieren pruebas reales y autorizaciones; no se promete su disponibilidad esta noche ni una fecha de revisión de Meta. La PC requiere diagnóstico; no se descuenta tiempo del plan suponiéndola ya utilizable. Render real se estima después de medir un clip representativo. La espera externa no se oculta dentro de H3.

Si H2 se demora, se conserva como entrega útil el panel con cerebro/guiones y el circuito comercial que efectivamente haya pasado su prueba; los demás pasos quedan visibles con causa y responsable. No se cambian silenciosamente CTAs ni se afirma que la empresa está totalmente automatizada por tener todas las pestañas.

Antes del corte de Codex: dejar scripts fijos, instrucciones operativas, guiones/materiales y clases del 13/14/16 preparados. Después del 14 pueden seguir panel, validaciones y programas fijos; redacción nueva y razonamiento requieren Contenido o un proveedor disponible, con gasto sólo autorizado. No se convierte una suscripción de Grok o Higgsfield en una API disponible por suponerlo.

### Escalar hacia la operación de una persona

Cada fábrica declara entrada, pasos, responsable, contrato de salida, revisión y permisos. Agregar un canal o formato reutiliza ese contrato y los componentes de revisión; no requiere otro panel ni una sesión permanentemente encendida. Código y decisiones compartibles viven en master; medios, clientes, pagos y credenciales quedan en almacenamiento privado con exportaciones saneadas.

Primero se mide el recorrido de contenido a pago confirmado del workshop. Después se incorporan agenda/soporte, entrega de proyectos y seguimiento de clientes de OnIA Platform, y reportes de operación/finanzas a partir de datos reales. Esos frentes son la siguiente fase, no trabajo implícito dentro del lote de esta noche. Antes de aumentar concurrencia se mide VPS más worker aceptado; ese ensayo conserva su pendiente y no demora ventas.

El criterio de avance es reducir intervenciones repetitivas de Sergio con pruebas observables: una corrección se aplica, un resultado recibe revisión, un mensaje tiene recepción comprobada y un pago lo confirma su dueño. Cantidad de bots, pestañas o sesiones no es una medida de que la empresa opere sola.

### Una autorización de alcance y las entradas personales

La aprobación propuesta cubre desarrollar este lote mediante el harness, sus correcciones y revisiones, aceptar e integrar resultados técnicos buenos en master, mejorar las skills aplicables con evidencia y desplegar el panel privado y su despachador probado en el VPS. Incluye integrar flujo `9a4639f` y generador revisado; los cambios posteriores dentro del mismo alcance requieren su revisión, no otro prompt de Sergio. Se registra el alcance de esa aprobación una vez y se conserva en cada tarea.

Quedan como decisiones finales concretas: activar workflows/canales de n8n/Meta preparados, envíos de ensayo y operación con personas, publicaciones, presupuesto de anuncios y consumo Higgsfield por pieza. Se agrupan por canal con configuración y prueba concretas para que Sergio apruebe una vez el recorrido aplicable. No se solicita de nuevo autorización ya concedida dentro de su alcance.

Entradas pendientes: hora de **entrega** de la tanda desde mañana (preguntada; iniciar el proceso con margen medido), número del workshop verificado en Meta (preguntado), acceso privado a QR/Meet/cuentas y grabación/B-roll. La PC está online; su diagnóstico se coordina por el acceso ya autorizado y Sergio acepta las tarjetas administrativas que le correspondan. Las contraseñas y códigos los introduce él.

Criterio global de cierre: abrir desde el teléfono, corregir un dato del cerebro y ver su aplicación en una nueva pieza; revisar anuncio y recurso IA; procesar una grabación; completar un ensayo comercial por cada canal habilitado; reiniciar sin duplicados; mostrar evidencia, tareas pendientes y continuidad del día siguiente. Aprobar el plan no significa que estas comprobaciones ya pasaron.

Referencias: lecturas existentes de los dos videos de Euge (`EUGE-VIDEO-BOSS-20261109.md` y `EUGE-VIDEO2-BOSS-20261109.md`), ejemplos/criterios concretos, pasos pequeños y carpeta persistente. Consulta técnica primaria: [ejemplos oficiales de Meta para WhatsApp](https://github.com/fbsamples/whatsapp-api-examples). Las páginas oficiales de Private Replies, Cloud API y Generate Preview devolvieron HTTP 429 en esta consulta; permisos, versión y disponibilidad efectiva quedan sujetos a cotejo en la implementación. No se tomaron artículos de terceros como garantía de acceso.

## Autorización del lote y estrategias — 11 noviembre 2026

Sergio aprobó: «Ok, vamos con el plan ve desarrollando te dejo», y agregó un apartado que arme estrategias documentadas para la venta actual y futuros proyectos/ventas. Queda autorizado el lote técnico presentado, incluida integración revisada y despliegue privado; se mantienen aprobaciones comerciales y gasto. El bloque anterior deja de ser sólo propuesta para ese alcance. Hora diaria y verificación Meta siguen pendientes.

Estrategias: biblioteca versionada por proyecto con diagnóstico, evidencia/supuestos, audiencia, oferta, canal, recorrido de venta, acciones priorizadas, piezas, responsable, dependencias, métricas reales y revisión. Primera estrategia: workshop y objetivo de Bs 3000. Futuros proyectos quedan como propuestas evaluables, sin iniciar gastos ni desarrollar cada idea. Integrar su consulta/corrección al panel mediante contrato, con un solo escritor de UI.

## Auditoría de huecos del lote — 11 noviembre, ejecución autorizada

| Brecha observada | Responsable y siguiente paso | Evidencia de cierre requerida |
|---|---|---|
| Regla de cierre estaba en memoria de Boss pero no explícita para Codex | Coordinadora: incorporada en reglas-comunes | Regla publicada y aplicada a este lote |
| Flujo/generador revisados seguían sin integración | Cerrado técnico: merge a728a89, seis HTTP correctas; aceptaciones canónicas flujo r43/generador r17 | Publicado, estados saneados en master624529c |
| Loop general no existe probado | Sesión fabrica-codigo-continuidad-lote-20261111 ejecutándose | Dictamen y ensayo de avance/reinicio real |
| Estrategias aún sin entrega | Entrega67e8336 revisada buena; conciliación de fuentes en curso | Integración y export vigente |
| Cerebro/correcciones/panel y acceso teléfono incompletos | Retoma cerebro-panel-usable-20261109 ejecutándose r36, misma sesión y ruta exclusiva | Corrección aplicada, persistencia, acceso privado real |
| WhatsApp preparado sin ensayo comercial | Integrado7a9892a, aceptado r34;44Node+16Python correctas. Sergio completa acceso Meta/QR/Meet | Recorrido real autorizado, pago manual y acceso |
| IG/FB, anuncios/IA y montaje incompletos | Sesiones sucesivas del lote aprobado, rutas separadas | Pruebas por canal y material real; generación por pieza autorizada |
| Entrega diaria18:00 confirmada | Coordinadora: programar con margen medido; no restaurar07:00 | Disparador probado y entrega antes de18:00 |
| Homelab online sin worker aceptado | Diagnóstico PE local y validación SSH/aislamiento | Una ejecución segura en worker; no basta presencia Tailscale |
| Modelo después del14 sin continuidad garantizada | Preparar scripts/materiales y operación con Contenido | Proveedor disponible o procedimiento manual comprobado |

Esta tabla registra pendientes reales; anotarlos no equivale a resolverlos. El lote sigue abierto hasta sus comprobaciones, sin exigir otro prompt para trabajo técnico ya autorizado.

### Conciliación comprobada del cierre

Master remoto52fb1c8 comprobado; después integración WhatsApp7a9892a y publicación de estados624529c. Flujo/generador/WhatsApp aceptados técnicamente con sus revisores originales buenos y commits exactos. Rutas liberadas. Esto no activa programación ni canales ni aprueba piezas editoriales.

La primera liberación de ruta del flujo falló porque se usó actor coordinadora donde el harness exige el responsable asignado. La aceptación anterior sí había quedado guardada: se consultó el estado y se liberó con el responsable canónico, sin aceptar de nuevo ni eludir la comprobación. Lección: cada efecto se concilia antes de reintentar el paso siguiente.

Las brechas de producto son trabajo del lote en curso, no condiciones para volver a pedir aprobación del plan. Los bloqueos externos son concretos: hora diaria, acceso y prueba autorizada Meta, QR/Meet privados, grabación/B-roll y diagnóstico local del homelab. No se inventa que alguno llegó. La ampliación de más de tres sesiones permanece pospuesta por Sergio.

### Confirmaciones recibidas y avance

Sergio confirmó entrega diaria18:00LaPaz y número Meta verificado. Quedan por comprobar acceso API y ensayo real; no pedir de nuevo la hora ni la verificación al titular. La retoma del panel ya corre; el primer intento de iniciar fue rechazado sin lanzar por tener historial y se usó reanudar sobre el mismo ID. Estrategias recibió dictamen bueno67e8336; antes de su aceptación se concilian fuentes modificadas y estas nuevas confirmaciones, preservando prueba y versión anteriores. Meta-canales está preparado como fabrica-automatizaciones-meta-canales-20261111; no activo.

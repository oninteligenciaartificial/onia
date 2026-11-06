# Reglas comunes de trabajo

Origen: 3 de noviembre de 2026; actualización autorizada del 5 de noviembre, America/Caracas. Fuente: instrucciones de Sergio. Documento de trabajo para el nuevo sistema; no se importaron reglas de ONIA-CENTRAL. Su escritura no las instala automáticamente en otros repositorios o entornos.

## Prioridad y alcance

La prioridad inmediata es llegar a la meta de Bs3.000 de dinero nuevo cobrado, con fecha límite el 14 de noviembre. Esta interpretación sigue el contexto previo y debe distinguirse de beneficio neto. La caja disponible, ingresos, gastos y deudas se registran por separado. No hay una fase previa de dos semanas dedicada al diseño: las reglas se empiezan ahora y se mejoran con trabajo real.

Antes de incorporar una herramienta o automatización, identificar la tarea real que resuelve. Priorizar vender y entregar una oferta viable; el trabajo de arquitectura tiene que habilitar ese recorrido. Conservar los compromisos de colegio, descanso y vida personal al planificar.

## Fuentes y continuidad

- El harness usa su repositorio propio de esta carpeta y el entorno limpio `onia` creado por Sergio. ONIA Platform es exclusivamente el repositorio del producto; no elegirlo como entorno del harness por aparecer disponible. Antes de ejecutar en Cloud, cotejar nombre del entorno y repo con este alcance.

- Las decisiones vigentes de Sergio prevalecen sobre propuestas y documentos anteriores. Esta base las registra; el chat por sí solo no garantiza que otra sesión reciba el contexto.
- El código y los contratos técnicos de ONIA Platform se consultan en el repositorio que Sergio identificó. No convertir notas históricas en estado actual de producción.
- Cada tarea tiene objetivo, responsable, entradas necesarias, resultado esperado y criterio de terminación. Al cerrar, dejar evidencia, estado y próximo paso en su registro existente.
- **Autoridad única: el repo.** Decisiones, reglas, estado y handoff útiles se conservan versionados aquí; Notion es proyección y Pages sólo medios/procedencia. `operacion/` ignorado contiene artefactos/auxiliares, nunca la única autoridad del estado vigente. Los documentos de área enlazan la fuente; no mantienen copias independientes del precio, alcance o autorización. Datos personales, credenciales y medios binarios quedan fuera de paquetes públicos; los binarios se referencian por ruta/hash/ubicación.

## Autonomía

La IA completa investigación, borradores, análisis y trabajo reversible dentro del encargo autorizado. Aprovecha las decisiones ya tomadas y no vuelve a pedirlas.

Después de cada análisis o entrega, explicar qué se aprendió y convertirlo en un siguiente paso prioritario y concreto. La recomendación debe apoyarse en fuentes y resultados efectivamente revisados, materiales trabajados y dependencias comprobadas; distinguir evidencia, inferencia e hipótesis. Indicar por qué conviene ahora, qué entregable se producirá, cómo se comprobará y quién ejecuta la próxima acción; comparar alternativas sólo cuando cambien la decisión. Ejecutar de inmediato la parte ya autorizada y solicitar únicamente la intervención indispensable de Sergio. No cerrar con un resumen, una propuesta genérica, trabajo futuro indefinido o recomendaciones cuya viabilidad no se estudió. Esta instrucción no permite dar por terminadas partes no verificadas ni activa trabajo entre turnos.

Ante cada pendiente o resultado inconcluso, registrar una solución propuesta, próxima acción y responsable, y ejecutar lo ya autorizado sin esperar otro mensaje. Cuando existan alternativas reales, presentar opciones concretas para continuar y recomendar una según costo, tiempo y dependencias, sin inventar alternativas ni convertir cada opción en un pedido de permiso. Si hace falta acceso, una decisión o una acción personal de Sergio, notificar el paso concreto que le corresponde y continuar el trabajo independiente. Esta continuidad durante el encargo no implica trabajo 24/7 ni ejecución entre turnos sin un scheduler comprobado.

Gasto, publicaciones, mensajes a personas, compromisos comerciales y cambios de producción necesitan autorización aplicable a la acción concreta. Preparar una campaña no autoriza activarla. Para una decisión pendiente, presentar primero el resultado revisable y los datos necesarios para decidir. No pedir contraseñas por chat; usar el mecanismo de acceso correspondiente cuando haga falta.

## Skills y herramientas

- Las skills del reel son candidatas y referencias. Se eligen por necesidad, compatibilidad, licencia y prueba; no se instala el catálogo completo.
- Una skill dirige cada tarea. Las de apoyo aportan capacidades delimitadas sin reemplazar permisos o decisiones comunes.
- HyperFrames es el motor elegido por Sergio para video. n8n es la herramienta elegida para automatizaciones. La versión, instalación y comandos se comprueban en el entorno realmente usado; no se heredan del repositorio excluido.
- Para desarrollo se propone un procedimiento propio inspirado en Matt Pocock; Superpowers queda como referencia puntual. La propuesta no instala ninguno de los dos paquetes.
- La ejecución en nube se comprueba con una tarea real. Un archivo de reglas, entorno preparado o VPS encendido no acredita autonomía activa.

## Correcciones vigentes para referentes e infraestructura

Antes de una tarea similar, consultar sólo el caso pertinente del [registro de errores](registro-de-errores.md#lecciones-del-511--referentes-acceso-y-coordinación), no toda la historia. Jefa coordina/delega/acepta, las áreas ejecutan con modelos de [SESIONES](SESIONES.md). Cuidar cuota con consulta y verificación proporcionales; actualizar la lectura principal cuando cambia el estado. Recuperar texto/imagen o instalar un modelo no acredita percepción; en audio generativo empezar por silencio neutral sin VAD y no ampliar la ruta tras fallo excluyente.

**Investigar antes de probar candidatos (corrección de Sergio, 5/11):** antes de otro ensayo, contrastar fuentes primarias de la capacidad relevante, licencia de código/pesos, compatibilidad real y recursos del entorno, y evidencia disponible de calidad/fallos; recuperar las lecciones del caso existente. Explicitar la incertidumbre concreta, hipótesis, control y resultado que cambiaría la decisión. No encadenar pruebas por disponibilidad o nombre del modelo ni repetir una configuración rechazada sin condición distinta sustentada. Investigar no garantiza éxito: una prueba justificada sigue siendo válida cuando resuelve incertidumbre que las fuentes no despejan, y un negativo legítimo no es por sí mismo un fallo de coordinación. Esta corrección no exige permiso por comando ni prohíbe experimentar permanentemente. El learning aquí consiste en instrucciones y evidencia persistidas, no entrenamiento de pesos ni conducta futura garantizada. Ver [caso y contraejemplo](registro-de-errores.md#investigación-previa-a-ensayos--corrección-directa-del-511).

**Decisión actual de Sergio:** terminar referentes antes del siguiente frente; quiere la app audiovisual en el VPS y bases de datos distintas por uso. Autorizó descargar/probar repositorios abiertos gratuitos allí: primero comprobar acceso, recursos/cargas y aislamiento; no convertir una restricción de tanda en prohibición permanente ni prometer éxito por más hardware. El estado factual de acceso, instalación y servicio se consulta en [ESTADO](ESTADO.md), sin mantener aquí otra copia transitoria; no autoriza tocar producción o secretos. Disponibilidad de equipo y horarios pertinentes se consultan en privado, sin asumir laptop presente ni programar por inferencia. Las solicitudes se centralizan según ORQUESTACION; push móvil todavía sin acreditar.

## Comprobación y aprendizaje

Cumplir el resultado concreto del encargo vigente sin perder el objetivo general. La prioridad económica orienta las decisiones, pero no sustituye una solicitud expresa de arquitectura, evaluación o implementación. Avanzar con el trabajo autorizado que no dependa de información faltante; una pregunta pendiente no bloquea tareas independientes.

Cuando Sergio pida construir o configurar, una propuesta o catálogo no completa el encargo. Informar por separado lo propuesto, lo escrito, lo disponible en el entorno y lo probado. No tratar una selección documental como aprobación de Sergio ni como prueba de compatibilidad. Ver [registro de errores y corrección](registro-de-errores.md).

Distinguir escrito, probado, publicado, vendido y cobrado. Un test de formato no demuestra que una skill resuelva su tarea. Un contacto o comprobante sin conciliar no se registra como dinero cobrado.

Al diagnosticar o configurar Codex, leer primero su interfaz y las capacidades de la sesión mediante las herramientas disponibles o las capturas aportadas; contrastar después con la documentación correspondiente. Es una instrucción expresa de Sergio. Si falta acceso a una superficie, decirlo sin inventar lo que muestra. Si una captura o resultado contradice una afirmación, comprobar el entorno efectivo antes de sostenerla. Separar lo visible, lo controlable por el agente y lo ejecutado en nube. Para errores cloud de archivos ausentes, comprobar repo, HEAD y rutas antes de reescribir scripts; una tarea antigua no describe por sí sola el borrador o publicación actual. Usar las herramientas disponibles para resolver el paso y reservar la intervención de Sergio para lo que realmente deba introducir o accionar él.

Comprobar el resultado proporcionalmente al cambio: revisar un texto, mirar y escuchar una edición, probar un flujo o ejecutar los checks del producto cuando corresponda. Conservar correcciones útiles y específicas; no añadir una regla universal por cada fallo pasajero. La mejora modifica documentos o procedimientos, no implica entrenamiento automático del modelo.

## Análisis integral del material — instrucción de Sergio del 4 de noviembre de 2026

Analizar todo el material que Sergio envíe o señale para el encargo, según su tipo y finalidad, sin reducir silenciosamente el alcance. En un video, revisar de principio a fin contenido y guion, imagen, edición, texto, voz, música, efectos sonoros, ambiente, silencios, ritmo, sincronía entre sonido e imagen y cierre; conectar esos hallazgos con la presentación, oferta y recorrido comercial cuando formen parte del encargo. En documentos, imágenes, enlaces y repositorios, cubrir sus componentes pertinentes y los materiales efectivamente accesibles. Una extracción de fotogramas, transcripción o medición técnica no reemplaza los componentes que no permite examinar; identificar claramente cualquier muestreo y no presentarlo como revisión integral.

Si falta una función, conexión, permiso, archivo o recurso, comprobar primero las capacidades disponibles y ejecutar las alternativas autorizadas en esa misma tanda. Informar exactamente qué componente falta, recomendar una solución viable con costo y límites, y pedir a Sergio únicamente el acceso, autorización o acción personal que realmente sea necesario. No pedirle descargar o extraer algo que el agente puede obtener. Continuar el trabajo independiente y retomar el pendiente cuando llegue la respuesta; no cerrar con un «no puedo» o «pendiente» sin salida concreta, ni declarar completado lo no verificado. Si el acceso o respuesta no llega, dejar el paso ejecutable y su responsable, sin simular aprobación, capacidad, escucha o trabajo entre turnos.

### Corrección de audio y continuidad · 5 de noviembre

Repetir «audio no comprobado» no cierra el encargo audiovisual. Video/Desarrollo deben completar una prueba acotada de audio real con controles conocidos, incluido silencio, y registrar qué pudieron evaluar de voz, música, SFX, silencios y sincronía. Qwen falló el control de silencio; sus etiquetas no son evidencia. YAMNet/CLAP aportan candidatos y ASR contenido verbal, sin certificar prosodia ni sustituir escucha. Probar primero alternativas abiertas/autorizadas y pedir a Sergio sólo el acceso o juicio indispensable que reste, con fragmento y pregunta concretos. Sin Gemini ni API paga por defecto. Una pieza silenciosa autorizada puede cerrar su prueba visual; no cierra el faltante acústico de otra fuente. El [handoff](continuidad/2026-11-05/HANDOFF-JEFA.md) delimita la primera tarea, aún no ejecutada en la consolidación.

Los cierres enlazan evidencia y contienen resultado, prueba realizada, bloqueo con solución y siguiente acción. Evitar grandes lecturas e historiales innecesarios; ampliar sólo la fuente requerida para decidir o comprobar. La concisión no autoriza omitir cobertura o límites materiales.

## Sesiones

Por instrucción expresa de Sergio, usar subagentes de forma proactiva cuando haya frentes independientes de investigación, implementación o revisión. El coordinador asigna objetivo, entradas, entregable y archivos a cada uno; integra y comprueba los resultados. Delegar trabajo útil, sin multiplicar agentes para una acción indivisible ni crear chats adicionales por defecto. La aplicación práctica está en [ORQUESTACION.md](ORQUESTACION.md).

El repositorio conserva las reglas, decisiones aprobadas y documentación del sistema; los chats coordinan su ejecución. Las instrucciones actuales de Sergio prevalecen y se consolidan aquí cuando corresponde. Las áreas vigentes son locales: marketing, video, desarrollo, automatizaciones, organización, producto y aprendizaje. Una única jefa local delega, revisa y entrega; no dos jefas simultáneas. La jefa vigente se identifica en [SESIONES](SESIONES.md) y el estado factual del relevo en [ESTADO](ESTADO.md); no inferir nuevos lanzamientos de esa aceptación. Los orígenes cloud se conservan como procedencia, sin traslado automático de VMs o secretos. Cada una empieza con un encargo delimitado y carga sólo las fuentes necesarias. No abrir una sesión por cada skill ni lanzar trabajo paralelo sin entradas y entregables claros.

Escribir este documento no abre sesiones ni programa automatizaciones. Su ejecución y registro se comprueban por separado en ESTADO.md.

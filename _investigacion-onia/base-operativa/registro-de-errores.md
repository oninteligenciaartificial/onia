# Registro de error y corrección — 3 de noviembre de 2026

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

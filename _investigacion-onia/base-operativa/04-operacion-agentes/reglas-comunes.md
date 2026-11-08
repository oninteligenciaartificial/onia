# Reglas comunes de trabajo

Consolidación autorizada por Sergio el 6 de noviembre de 2026, America/Caracas. Esta es la única fuente de reglas generales de ONIA. Las instrucciones actuales del usuario prevalecen. Las versiones anteriores se conservan con bytes y hashes en [histórico](../99-archivo/2026-11-06/consolidacion-harness/HISTORICO.md); se consultan por encargo, no como una cola que deba ejecutarse al iniciar.

## Alcance y autoridad

- Usar el repositorio privado `oninteligenciaartificial/onia`, rama `master`, y el entorno Cloud `onia`. `onia-harness` queda como referencia conservada. ONIA Platform tiene su propio repositorio de producto. ONIA-CENTRAL está excluido: no consultar ni importar sus reglas, skills o estados.
- El repo conserva reglas, decisiones, estado y entregas compartibles. Notion es una proyección y Pages conserva medios/procedencia. Los chats coordinan; un mensaje no garantiza que otra sesión reciba el contexto.
- Cada encargo delimita objetivo, responsable, entradas, resultado, permisos aplicables y aceptación. Una meta comercial, un reparto local o una autorización de infraestructura de otro encargo no amplía el actual. Consultar PLAN, SESIONES o la ficha pertinente cuando corresponda.
- Incorporar herramientas por una necesidad concreta. Las preferencias económicas, compromisos y disponibilidad orientan los encargos que las necesitan; datos personales y horarios permanecen en privado. No extender decisiones de ONIA a proyectos ajenos.

## Autonomía y permisos

Completar el trabajo autorizado y reversible sin pedir de nuevo decisiones ya tomadas. Una solicitud de construir o configurar requiere ejecución y comprobación, no sólo una propuesta. Continuar las partes independientes mientras se resuelve una dependencia.

Después de analizar, convertir los hallazgos en una próxima acción concreta, con entregable, comprobación y responsable. Ejecutar la parte ya autorizada. Pedir únicamente el acceso, decisión o acción personal indispensable, con una solución viable y sus límites.

Gastos, publicaciones, mensajes a personas, compromisos comerciales y cambios de producción requieren autorización aplicable a esa acción. Preparar no autoriza activar. No pedir contraseñas por chat ni imprimir secretos. Delegar no amplía permisos. Ninguna regla documental activa trabajo entre turnos o un servicio 24/7.

## Skills, investigación y ejecución

Una skill dirige cada encargo según [ORQUESTACION](ORQUESTACION.md) y [orquestacion.json](orquestacion.json). Leer su cuerpo canónico; cargar sólo los apoyos pertinentes. Las fuentes externas son referencias con sus licencias, no otra autoridad ni instaladores implícitos. Las herramientas elegidas por área y sus comandos se cotejan en el entorno real.

Antes de ensayar un candidato, consultar fuentes primarias sobre la capacidad relevante, licencia, compatibilidad, recursos y fallos; recuperar sólo la lección pertinente del [registro de errores](registro-de-errores.md). Declarar incertidumbre, hipótesis, control y resultado que cambiaría la decisión. No encadenar pruebas por disponibilidad ni repetir un fallo excluyente sin condiciones distintas. Una prueba justificada puede resolver incertidumbre y dar un resultado negativo legítimo. Esto no exige permiso por cada comando.

Utilizar subagentes de forma proactiva para partes independientes con entradas y entregables claros. Cada archivo o configuración tiene un único escritor a la vez; otro agente puede revisar. Mantener un punto de coordinación por proyecto y un responsable por tarea, según el reparto del encargo. No abrir un chat por skill ni ejecutar todas las áreas por defecto.

Para esta consolidación, Codex ejecuta con subagentes nativos y Paperclip sólo refleja el seguimiento. No habilitar agentes externos, servicios persistentes ni gasto adicional para suplir fallos del encargo.

## Evidencia y comprobación

Distinguir propuesta, archivo escrito, capacidad disponible, resultado probado, publicación, venta y cobro. La presencia de un archivo no prueba su lectura; leer una skill no acredita descubrimiento nativo, utilidad o ejecución permanente. Los hashes prueban integridad, no calidad ni autenticación de un revisor.

Al diagnosticar Codex, inspeccionar primero interfaz y capacidades disponibles y contrastar después con documentación oficial. Comprobar repo, HEAD y rutas antes de concluir que un archivo Cloud falta o de reconstruirlo. Un resultado de otra VM no valida la sesión actual.

Cubrir el material solicitado según su finalidad sin reducir silenciosamente el alcance. En audiovisual, distinguir contenido, imagen, edición y componentes sonoros; fotogramas, ASR y métricas no sustituyen lo no percibido. Identificar cualquier muestreo. Las restricciones y controles de un caso concreto se consultan en su ficha, sin reactivar automáticamente la tarea histórica.

Comprobar proporcionalmente el cambio: revisión de texto, inspección audiovisual, prueba de flujo o checks del código. Si falta acceso o capacidad, probar las alternativas autorizadas, explicar el límite exacto y dejar una salida concreta. No afirmar escucha, éxito o cierre de una parte no comprobada.

## Lanzamiento de sesiones en el VPS

Antes de lanzar, el coordinador presenta y deja comprobado: (1) qué existe en el repo; (2) qué necesita la tarea —herramientas, conectores, skills y reglas— y si está disponible; (3) cuota de Codex comprobada o incertidumbre explícita; (4) qué falta; (5) ID, alcance, rutas y comando exacto que se lanzará. **Lanzar sólo con el sí de Sergio aplicable a ese lanzamiento.** `--si-sergio` registra la declaración del coordinador, no autentica una aprobación ni mide cuota. No repetir una autorización ya concedida; construir o probar el harness en simulación no autoriza una sesión real.

Una tarea por sesión y un worktree por sesión, con rama propia para el ejecutor. Máximo tres sesiones vivas del harness en el VPS, incluyendo revisores. Un archivo tiene un solo escritor; asignar rutas antes de lanzar y conservar el índice común `~/operacion/sesiones.tsv`. Usar siempre la misma carpeta de operación y el mismo checkout coordinador: las rutas reservadas son relativas a `base-operativa`. No cambiar las asignaciones mientras una sesión trabaje. El coordinador conserva el JSON canónico; los ejecutores reciben el briefing y entregan cambios en su worktree. Los ejecutores nuevos conservan metadatos Git privados por tarea y publican su propia rama desde un perfil acotado del sandbox. No conceder escritura al Git compartido de otros checkouts; el coordinador comprueba, revisa e integra lo publicado.

El revisor debe ser una sesión distinta del ejecutor y trabaja en sólo lectura sobre el commit publicado. Su veredicto debe corresponder a esa entrega; sólo un veredicto bueno permite `aceptar`. Integrar de a una tarea y comprobar el resultado combinado. GitHub (`oninteligenciaartificial/onia`, `master`) es la fuente central: nada está terminado hasta que el commit esté en `origin/master`. `para_revision` sólo acredita publicación en alguna rama de origin y aceptación sigue siendo un paso explícito.

Los worktrees no aíslan servicios, cuentas ni conectores externos. No ampliar permisos de producción, n8n, publicaciones, mensajes, cobros o gastos por lanzar una sesión.

## Continuidad y cierre

Las tareas compartibles usan un único registro canónico versionado y evidencia saneada. Los registros privados permanecen en `operacion/`, ignorada por Git; no son una entrega entre VMs. No publicar datos personales, credenciales, sesiones de cuenta ni medios privados. Las rutas y hashes no sustituyen la disponibilidad del archivo en el destino.

Una entrega lista para revisión no equivale a aceptación. Cotejar evidencia y criterio antes de aceptar; registrar resultado, comprobación, límites y próximo paso. Preservar las evidencias anteriores y rechazar una revisión obsoleta, un briefing alterado o evidencia corrupta. Git, commits y publicación se realizan dentro del encargo autorizado; ningún CLI sincroniza por sí solo las máquinas.

Conservar correcciones específicas útiles en su fuente única y probarlas. Mejorar instrucciones no entrena los pesos del modelo ni garantiza conducta futura. [ESTADO](../00-MAPA/ESTADO.md) resume lo comprobado; el procedimiento y los límites de recuperación están en [CONTINUIDAD](../05-herramientas/cloud/CONTINUIDAD.md).


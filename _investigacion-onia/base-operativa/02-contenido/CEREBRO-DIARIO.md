# Cerebro diario de ONIA

El cerebro es un registro compartido y un procedimiento de trabajo. Se ejecuta cuando Sergio da un encargo o un disparador comprobado lo inicia. No es un proceso permanente ni un modelo que se entrena solo.

## Fuentes

| Dato | Fuente única |
|---|---|
| Reglas, permisos y skills | [Reglas comunes](../04-operacion-agentes/reglas-comunes.md) y [manifiesto](../04-operacion-agentes/orquestacion.json) |
| Dirección, decisiones y planes por área | [PLAN.md](../01-negocio/PLAN.md), integrado por la coordinación local con planificación/síntesis de ONIA · Jefe cloud; [consolidación documental](../99-archivo/2026-11-04/README.md) para procedencia |
| Vida, publicaciones, ventas, actualidad y decisiones cotidianas | [Sergio · Hoy, Notion privado](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) |
| Contexto personal histórico todavía no consolidado | [Página privada anterior](https://chatgpt.com/space/page_9891b23df62081918a4bcf61eadb0fc4); recuperar sólo lo necesario y comprobar vigencia, sin mantener otra cola diaria |
| Investigación, entregas documentales y fuentes | [Índice en Git](../03-referentes/notas-2026-11-04/README.md) y [entregas consolidadas](../99-archivo/2026-11-04/README.md); biblioteca cloud como procedencia, historial y medios |
| Compromisos y horarios guardados | Google Calendar personal; leer el día solicitado antes de modificarlo |
| Ejecución y evidencia de cada área | Chat correspondiente de [SESIONES.md](../04-operacion-agentes/SESIONES.md) y sus artefactos accesibles |
| Capacidad comprobada del sistema | [ESTADO.md](../00-MAPA/ESTADO.md) |

Los registros privados se leen con el conector oficial correspondiente, Notion o ChatGPT Space. Sus IDs identifican recursos, no conceden acceso. **Git es la fuente oficial del plan, decisiones y documentación consolidada**; Pages conserva procedencia, medios y registros privados que no pertenecen al repositorio. No copiar perfil, finanzas, hábitos ni credenciales al código, paquetes de skills o evidencia pública. Consultar sólo las secciones pertinentes. Una consolidación documental no prueba migración total de datos personales ni sincronización automática.

## Entrada durante el día

Sergio puede enviar tareas y respuestas en cualquier momento libre. Los controles del calendario son recordatorios para revisar, no una restricción de horarios ni un disparador de Codex. Puede escribir normalmente; no necesita rellenar un formulario.

- **Plan de hoy:** leer agenda y encargos abiertos; elegir un resultado principal y hasta dos secundarios que quepan.
- **Tengo diez minutos:** ofrecer la siguiente acción personal realizable; las tareas cloud completas pueden continuar por su cuenta.
- **Hacé…:** recuperar las entradas, preparar un encargo y ejecutar lo autorizado en el área correspondiente.
- **Estado:** distinguir terminado, en ejecución, esperando entrada o decisión; mostrar sólo lo relevante.
- **Cambió mi día…:** conservar lo terminado y ajustar únicamente lo afectado.
- **Cierre:** registrar resultados y hábitos informados, pendientes y primera acción siguiente.

Como límite inicial de atención, mantener hasta dos encargos activos que requieran revisión de Sergio; él puede cambiarlo. La cola preparada no se confunde con trabajo ejecutándose. Comidas, colegio, descanso, traslados y compromisos personales se consideran antes de asignarle más tareas.

## Coordinación y registro

Aplicar hoy ORQUESTACION y el reparto del encargo en ESTADO. Los dos párrafos siguientes conservan antecedentes del 4/11; no fijan la coordinación de toda tarea nueva.

La **sesión local `01a1a29c-3a3d-7b50-aef6-41305ce5faae`** coordina prioridades, despacho y revisión de entregas; las áreas ejecutan en cloud. **ONIA · Jefe** conserva planificación/síntesis cloud, con [PLAN.md](../01-negocio/PLAN.md) como fuente documental vigente; no se le atribuye inicio de chats de área. **ONIA · Organización diaria** mantiene la operación cotidiana y es la escritora designada de Notion/Calendar. El repo mantiene las decisiones del sistema; cada chat carga la parte necesaria. El agente que recibe un pedido puede resolverlo dentro de su alcance; los cambios a cada registro compartido pasan por su responsable, con un único escritor a la vez. Los demás chats devuelven resultado y evidencia sin editar simultáneamente el tablero. La sesión Aprendizaje aporta fuentes y práctica, sin duplicar la agenda ni el registro diario.

El despacho local y la recuperación de una entrega de Desarrollo quedaron comprobados; en Jefe/Desarrollo cloud se observaron herramientas para leer/esperar chats, pero no para enviarles nuevas órdenes. [Alcance de la prueba](../99-archivo/2026-11-04/coordinacion-local-cloud.md). La coordinación local requiere la PC disponible para nuevas órdenes/revisiones. La ejecución remota se comprobó sin ensayar un apagado físico de la PC; no declarar continuidad permanente por esa prueba ni confundir subagentes internos con chats de área.

Cada encargo contiene ID estable, área, objetivo, entregable, criterio de aceptación, estado, referencia al chat/artefacto, resultado, comprobación y siguiente paso. Reutilizar los estados de `scripts/trabajo.py`:

| Estado | Condición |
|---|---|
| preparado | Encargo definido; todavía no comenzó su ejecución |
| en_curso | Lanzamiento o ejecución aceptados por la herramienta correspondiente |
| en_espera | Falta una entrada, una decisión o resolver un bloqueo; indicar responsable y próximo paso |
| para_revision | Entrega preparada con evidencia íntegra y comprobación declarada correcta |
| aceptado | Revisión explícita registrada después de cotejar el criterio |

El estado terminado sólo se conserva en registros históricos schema 1; no se infiere aceptación al migrarlo.

Antes de actualizar un registro, leer su versión actual: revisión Git para documentación, IDs y hashes en Space, IDs y propiedades reales en Notion. Comprobar recibo y releer el resultado. Las exportaciones de Pages son instantáneas fechadas de procedencia; una actualización posterior se concilia en el documento canónico, no crea un plan oficial paralelo. Ante conflicto, conciliar sin sobrescribir cambios ajenos. Consultar un resultado externo incierto antes de repetirlo.

El mismo CLI usa un único registro por ID: compartible bajo continuidad/tareas o local bajo operacion, según [CONTINUIDAD](../05-herramientas/cloud/CONTINUIDAD.md). La revisión esperada impide actualizar una versión vieja y el inventario de evidencia se conserva. Los registros de `operacion/` son apoyo local de la ejecución. El bloqueo de archivo de `trabajo.py` sólo protege esa VM; no coordina varias máquinas. No crear una segunda cola global allí ni atribuirle sincronización automática. Si se usa el CLI, conservar el mismo ID y reflejar únicamente el resultado comprobado en la página.

## Flujo de trabajo

1. Leer fuentes vigentes y la parte necesaria del registro privado. Si el acceso falla, informar la diferencia y continuar con trabajo independiente; no inventar memoria recuperada.
2. Elegir área y una skill directora mediante el manifiesto. Preparar entradas, resultado y comprobación. Delegar partes independientes conforme a [ORQUESTACION.md](../04-operacion-agentes/ORQUESTACION.md).
3. Ejecutar en el entorno autorizado para el encargo. Coordinar otros chats sólo con autorización y herramientas verificadas; confirmar el lanzamiento antes de registrar en_curso. La coordinación no requiere por definición un chat local.
4. Consultar la entrega, revisar la evidencia y actualizar el registro. Una prueba sintética no acredita una campaña, venta, publicación o hábito real.
5. Dejar siguiente paso y un resumen breve para Sergio. Reutilizar su autorización vigente; los documentos no amplían permisos para gastos, mensajes o producción.

El aprendizaje conserva una corrección concreta, su causa y una comprobación. Cambiar una regla o skill sólo cuando el fallo lo justifique, mediante `mejorar-sistema`; no transformar cada anécdota o contenido web en una regla universal.

## Continuidad comprobable

La prueba histórica del registro cotidiano exige que otro chat cloud recupere una entrada sintética desde la página, sin recibir sus valores en el prompt, y que una actualización posterior se relea desde otra sesión. Conservar el resultado en ESTADO.md, sin exportar el contenido privado.

La página no mueve archivos de video entre VMs. Calendar no inicia agentes por sí solo. Automatización recurrente, publicación social y entrega de medios requieren pruebas independientes; su estado real se consulta en ESTADO.md.

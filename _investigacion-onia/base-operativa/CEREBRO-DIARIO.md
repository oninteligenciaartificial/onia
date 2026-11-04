# Cerebro diario de ONIA

El cerebro es un registro compartido y un procedimiento de trabajo. Se ejecuta cuando Sergio da un encargo o un disparador comprobado lo inicia. No es un proceso permanente ni un modelo que se entrena solo.

## Fuentes

| Dato | Fuente única |
|---|---|
| Reglas, permisos y skills | [Reglas comunes](reglas-comunes.md) y [manifiesto](orquestacion.json) |
| Prioridades, contexto personal, encargos y siguiente paso | [ONIA · Cerebro diario, página privada](https://chatgpt.com/space/page_9891b23df62081918a4bcf61eadb0fc4) |
| Compromisos y horarios guardados | Google Calendar personal; leer el día solicitado antes de modificarlo |
| Ejecución y evidencia de cada área | Chat correspondiente de [SESIONES.md](SESIONES.md) y sus artefactos accesibles |
| Capacidad comprobada del sistema | [ESTADO.md](ESTADO.md) |

La página se lee con el conector oficial ChatGPT Space y no se comparte públicamente. Su ID identifica el recurso, no da acceso. El repositorio sólo conserva este enlace y el procedimiento; no copiar el perfil, finanzas, hábitos ni credenciales al código, paquetes de skills o evidencia pública. Consultar sólo las secciones pertinentes a cada encargo.

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

**ONIA · Organización diaria** coordina la operación cotidiana. Este chat de configuración mantiene las decisiones del sistema. El agente que recibe un pedido puede resolverlo dentro de su alcance; los cambios al registro compartido pasan por el coordinador designado, con un único escritor a la vez. Los demás chats devuelven resultado y evidencia sin editar simultáneamente el tablero.

Cada encargo contiene ID estable, área, objetivo, entregable, criterio de aceptación, estado, referencia al chat/artefacto, resultado, comprobación y siguiente paso. Reutilizar los estados de `scripts/trabajo.py`:

| Estado | Condición |
|---|---|
| preparado | Encargo definido; todavía no comenzó su ejecución |
| en_curso | Lanzamiento o ejecución aceptados por la herramienta correspondiente |
| en_espera | Falta una entrada, una decisión o resolver un bloqueo; indicar responsable y próximo paso |
| terminado | Resultado obtenido y comprobado, con evidencia accesible |

Antes de actualizar la página, leer su versión y el bloque actual. Usar ID y hash devueltos por esa lectura para una edición protegida; comprobar el recibo y releer el resultado. Ante conflicto, volver a leer y conciliar; no sobrescribir cambios ajenos. Un resultado externo incierto se consulta antes de repetir la acción.

Los registros de `operacion/` son apoyo local de la ejecución. El bloqueo de archivo de `trabajo.py` sólo protege esa VM; no coordina varias máquinas. No crear una segunda cola global allí ni atribuirle sincronización automática. Si se usa el CLI, conservar el mismo ID y reflejar únicamente el resultado comprobado en la página.

## Flujo de trabajo

1. Leer fuentes vigentes y la parte necesaria del registro privado. Si el acceso falla, informar la diferencia y continuar con trabajo independiente; no inventar memoria recuperada.
2. Elegir área y una skill directora mediante el manifiesto. Preparar entradas, resultado y comprobación. Delegar partes independientes conforme a [ORQUESTACION.md](ORQUESTACION.md).
3. Ejecutar en el entorno cloud vigente, o enviar al chat de área existente cuando la autorización del usuario abarque esa coordinación. Confirmar el lanzamiento antes de registrar `en_curso`.
4. Consultar la entrega, revisar la evidencia y actualizar el registro. Una prueba sintética no acredita una campaña, venta, publicación o hábito real.
5. Dejar siguiente paso y un resumen breve para Sergio. Reutilizar su autorización vigente; los documentos no amplían permisos para gastos, mensajes o producción.

El aprendizaje conserva una corrección concreta, su causa y una comprobación. Cambiar una regla o skill sólo cuando el fallo lo justifique, mediante `mejorar-sistema`; no transformar cada anécdota o contenido web en una regla universal.

## Continuidad comprobable

La prueba de aceptación exige que otro chat cloud recupere una entrada sintética desde la página, sin recibir sus valores en el prompt, y que una actualización posterior se relea desde otra sesión. Conservar el resultado en ESTADO.md, sin exportar el contenido privado.

La página no mueve archivos de video entre VMs. Calendar no inicia agentes por sí solo. Automatización recurrente, publicación social y entrega de medios requieren pruebas independientes; su estado real se consulta en ESTADO.md.

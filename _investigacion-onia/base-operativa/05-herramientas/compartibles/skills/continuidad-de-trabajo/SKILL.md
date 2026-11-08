---
name: continuidad-de-trabajo
description: Prepara o actualiza una entrega para documentar, retomar o traspasar trabajo entre agentes o sesiones cuando el usuario solicita esa continuidad. No se activa para cada tarea cotidiana ni convierte una propuesta en trabajo ejecutado.
---

# Continuidad de trabajo

Dejá una entrega breve que permita continuar el trabajo autorizado con su estado real. Si el pedido incluye retomarlo, usá la entrega como punto de partida y avanzá dentro del alcance vigente.

## Reconstruir el estado

Si el proyecto ya tiene un registro ejecutable de tareas, usalo como fuente del estado. Desde la raíz de ONIA, `python _investigacion-onia/base-operativa/05-herramientas/scripts/trabajo.py retomar ID` devuelve objetivo, resultado y siguiente acción, y falla si la evidencia vigente no conserva su integridad. En ese mismo directorio scripts, `harness.py retomar ID` recupera además el briefing comprobado. No dupliques ese estado en otra nota. En otros proyectos, no supongas que esos scripts existen.

Para una tarea ONIA compartible, consultá [el contrato de continuidad](../../../cloud/CONTINUIDAD.md): un registro por ID, revisión esperada al modificar y evidencia acumulativa en rutas nuevas por versión. No sobrescribas una evidencia registrada ni recalcules su hash para ocultar un fallo. Los registros schema 1 siguen legibles como historia y requieren migración explícita antes de editar; un `terminado` histórico no se convierte en aceptación. Una entrega `para_revision` requiere comprobación correcta y la aceptación es un paso separado.

- Localizá la nota de continuidad y las fuentes canónicas indicadas por el usuario o por el trabajo existente. Reutilizá el registro pertinente en vez de crear varias versiones paralelas del mismo estado.
- Conservá el objetivo, las restricciones y las autorizaciones vigentes que consten en el contexto accesible. No amplíes el alcance ni agregues una aprobación universal para pasos ya autorizados.
- Contrastá lo que pueda haber cambiado antes de depender de ello. Para código, esto puede incluir rama, revisión, cambios locales y comprobaciones relevantes; para otros trabajos, el documento, tarea o sistema que mantiene el estado actual. No inventes herramientas o accesos para hacer esa verificación.
- Separá hechos observados, decisiones, inferencias y propuestas. Marcá como completado sólo lo respaldado por un resultado accesible; una intención, comando preparado o nota anterior no prueba su ejecución.
- Si existe trabajo en curso, registrá dónde consultar su estado. Un identificador de proceso o de sesión en una nota no demuestra que siga activo ni sea reutilizable desde otro entorno.

## Preparar la entrega

Incluí sólo lo necesario para continuar:

- **Objetivo y alcance:** resultado buscado y restricciones que siguen aplicando.
- **Fuentes canónicas:** enlaces o rutas reales donde viven decisiones, archivos y estado. Identificá qué fuente prevalece si hay versiones contradictorias.
- **Estado observado:** qué terminó, qué sigue en curso y qué está pendiente, con evidencia y fecha de observación cuando el dato pueda quedar obsoleto.
- **Verificación:** comprobaciones realizadas y su resultado; separá las no ejecutadas. Añadí limitaciones que afecten la conclusión.
- **Próximo paso:** una acción concreta dentro del alcance vigente, sus dependencias y el criterio para saber que terminó.
- **Pendientes de decisión:** preguntas o bloqueos reales que requieren información externa, sin convertir toda incertidumbre en un bloqueo.

Al actualizar, reemplazá afirmaciones obsoletas y conservá las decisiones que todavía explican el estado. Referenciá la fuente de un hecho compartido en vez de duplicarlo en varios documentos. No incluyas credenciales ni datos ajenos a la continuidad solicitada.

## Retomar o traspasar

Antes de repetir una operación con efectos externos o continuar una ejecución incierta, verificá su estado para evitar duplicados. Si la evidencia no es accesible, expresá qué falta comprobar y elegí un siguiente paso que no dependa de darla por cierta.

Entregá la ubicación del registro actualizado y los cambios materiales de estado. No afirmes que otro agente recibió el traspaso o que una tarea quedó programada sin confirmación de la herramienta correspondiente. Una entrega escrita preserva contexto; por sí sola no inicia trabajo futuro.

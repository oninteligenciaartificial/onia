# Auditoría estática del pseudoflujo S1–S4

## Diagnóstico

La consulta por texto confunde identidad de evento con contenido: A y B son el mismo evento `e1`, mientras C (`e2`) es independiente aunque también diga PLAN. Además, la secuencia de consulta e inserción sin unicidad ni reserva atómica permite que A y B vean ausencia e inserten dos filas; S3 aporta ese historial como dato del caso, no como una ejecución observada hoy. Marcar `sent` después de enviar deja una ventana en la que el proveedor pudo aceptar el envío y la respuesta agotó el tiempo: reejecutar sin conciliación puede duplicarlo. El pseudoflujo tampoco persiste la baja STOP ni verifica la preferencia antes del seguimiento. La petición humana prevalece sobre cualquier seguimiento comercial.

El esquema `webhook(event_id,text)` no identifica al usuario, aunque D y E se refieren al mismo: hace falta un identificador estable de usuario para aplicar y consultar la baja. También falta el alcance concreto de la respuesta, el contrato del proveedor para identificación y consulta de envíos y el orden verificable de las peticiones. No se puede inferir que PLAN posterior reactive el consentimiento.

## Evento → estado y efecto esperado

| Entrada | Estado esperado | Efecto esperado |
|---|---|---|
| A: `e1`, PLAN | Registrar y reservar `e1` una sola vez; pasar por pendiente y, según evidencia, enviado o resultado incierto. | Como máximo un envío comercial autorizado para `e1`, sujeto a baja y petición humana. |
| B: `e1`, PLAN, concurrente | Reconocer el mismo `event_id`; no crear otra reserva ni procesar en paralelo. | Ningún envío adicional; devolver o consultar el estado existente. |
| C: `e2`, PLAN | Registrar como evento independiente, aunque el texto coincida. | Evaluar su propio efecto según el estado y preferencias de su usuario; el texto igual no lo suprime. |
| D: `e3`, STOP | Persistir la baja para el usuario identificado y cancelar o bloquear seguimientos comerciales pendientes. | No enviar seguimiento comercial; cualquier confirmación de baja requiere definición y autorización específica. |
| E: `e4`, PLAN, después de D, mismo usuario | Registrar evento independiente y conservar baja activa. | Bloquear seguimiento comercial; PLAN no revoca STOP por sí solo. |
| Reejecución de `e1` tras timeout | Mantener resultado incierto hasta consultar evidencia del proveedor. | Si se confirma aceptación, marcar enviado sin reenviar; si se confirma ausencia y sigue autorizado, permitir un reintento controlado; si no se puede determinar, dejar pendiente para revisión humana. |

## Corrección propuesta

1. Validar `event_id`, texto y un identificador estable de usuario; rechazar o aislar entradas incompletas antes de efectos. Definir la identidad y el orden desde la fuente de eventos; si un mismo ID llega con datos incompatibles, aislarlo para revisión en vez de tratarlo como un duplicado normal.
2. Registrar cada evento con unicidad garantizada por `event_id` y reservar de forma atómica su procesamiento y su efecto, usando una clave de efecto estable derivada del evento y tipo de operación. Los duplicados leen el estado ya registrado. Mantener estados explícitos: pendiente, reservado, enviado, incierto, bloqueado y error; registrar cambios y evidencia sin secretos ni datos personales completos.
3. Persistir la baja por usuario al recibir STOP y darle prioridad frente a seguimientos pendientes. Antes de despachar, volver a comprobar baja y petición humana; coordinar esa comprobación con la reserva/despacho para evitar que un trabajo pendiente ignore un STOP ya aceptado. Un envío ya entregado no se puede retirar; documentar y resolver explícitamente la carrera entre STOP y un envío en curso según las garantías reales del proveedor.
4. Enviar sólo con autorización aplicable y, si el proveedor lo admite, usar la clave estable como clave de idempotencia. Ante timeout, registrar incierto y consultar el estado remoto por esa clave antes de reintentar. La ausencia debe ser concluyente según el contrato del proveedor; si no existe consulta fiable ni idempotencia, escalar el caso sin reenvío automático. Registrar el resultado confirmado, no asumirlo por la respuesta local.
5. Conservar referencia a la versión anterior antes de cualquier cambio real. Preparar un mecanismo de desactivación que detenga nuevos despachos y deje las reservas e incertidumbres visibles para conciliación; revertir la configuración sólo tras revisar los efectos ya iniciados y preservar bajas. No activar ni enviar como parte de esta auditoría.

## Controles locales propuestos

| Control con datos sintéticos | Resultado esperado | Estado de comprobación |
|---|---|---|
| A y B simultáneos con `e1` | Una reserva y como máximo un efecto; el duplicado obtiene estado existente. | Inspección estática del requisito; concurrencia no ejecutada. |
| C con `e2` y texto PLAN | Nueva identidad; no se descarta por texto. | Inspección estática; no ejecutado. |
| D seguido de E para el mismo usuario | Baja persistente; E registrado y seguimiento bloqueado. | Inspección estática; no ejecutado. |
| Entrada sin ID de evento o usuario, o ID repetido con contenido incompatible | Rechazo o aislamiento sin efecto externo. | Propuesto; no ejecutado. |
| Envío aceptado con timeout y reejecución | Estado incierto, consulta y confirmación sin segundo envío. | Propuesto; no ejecutado. |
| Dependencia no disponible o resultado remoto indeterminado | Mantener incierto o error recuperable, alertar y no reenviar a ciegas. | Propuesto; no ejecutado. |
| STOP aceptado mientras existe seguimiento pendiente o en curso | Pendiente bloqueado; carrera con envío en curso visible y tratada conforme a garantías comprobadas. | Propuesto; no ejecutado. |

La evidencia disponible es exclusivamente el texto S1–S4. No se inspeccionaron instancia, versión ni contratos reales; no se construyó ni activó un flujo y no hay resultados de runtime. Próxima acción: la persona responsable de la integración debe precisar identidad de usuario, orden de eventos, tipo de respuesta y capacidades del proveedor; luego podrá validar el diseño en una copia de prueba con los controles anteriores antes de cualquier activación autorizada.
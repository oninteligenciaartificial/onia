# Auditoría del pseudoflujo S1–S4

## Diagnóstico estático

- Buscar por `text` confunde eventos independientes: C puede quedar suprimido por A aunque tenga otro `event_id`. El texto no es clave de identidad (S1, S2, S4).
- La comprobación y el INSERT separados, sin unicidad ni transacción, permiten que A y B pasen la consulta y creen dos filas para e1. Las dos filas son un antecedente declarado en S3, no una carrera reproducida en esta auditoría. El INSERT tampoco reserva el envío atómicamente.
- Enviar antes de marcar `sent` deja un intervalo ambiguo: el envío de e1 puede completarse y devolver timeout; repetirlo ciegamente puede duplicar el mensaje (S3). Marcar antes de enviar, por sí solo, también podría perderlo.
- No hay persistencia ni comprobación de STOP. E debe bloquearse aunque sea un evento nuevo. El esquema del webhook no identifica al usuario: falta una identidad estable y su vínculo autorizado con D y E para aplicar esa regla. No se puede inferir de `text` o `event_id`.
- La petición humana prevalece: STOP debe registrarse y prevalecer sobre seguimientos pendientes. La semántica de otras peticiones humanas y qué respuesta, si alguna, está permitida requieren definición; no se debe suponer autorización para mensajes.

## Evento → estado y efecto esperado

| Entrada | Estado esperado | Efecto esperado |
|---|---|---|
| A: e1, PLAN | Admitir e1 una sola vez; reservar el efecto si el usuario puede recibirlo. | Como máximo un envío autorizado; si hay timeout, estado incierto y conciliación. |
| B: e1, PLAN, concurrente | Duplicado de e1; reutilizar su estado, incluso si está en curso o incierto. | No crear otra reserva ni iniciar otro envío. |
| C: e2, PLAN | Evento independiente de e1; evaluar preferencias del usuario correspondiente. | Puede producir su propio efecto autorizado; no suprimir por compartir PLAN. |
| D: e3, STOP | Registrar evento y preferencia persistente de exclusión para el usuario identificado; cancelar o bloquear seguimiento pendiente. | Ningún seguimiento comercial; cualquier respuesta a STOP sólo si está específicamente permitida. |
| E: e4, PLAN, tras D del mismo usuario | Registrar evento independiente como bloqueado por STOP persistente. | Ningún seguimiento comercial, aunque tenga ID nuevo. |

La tabla presupone que se aporta una identidad estable y que la relación D–E es verificable. No se especifica el usuario de A–C ni el orden de C respecto de D; su elegibilidad depende del estado aplicable en el momento de decidir el efecto. Si STOP llega mientras un envío ya salió, no se puede garantizar retirarlo: registrar el resultado, impedir envíos posteriores y conciliar cualquier incertidumbre.

## Corrección propuesta

1. Validar `event_id`, texto y un identificador estable de usuario, con tipos y procedencia definidos; rechazar o poner en revisión entradas que carezcan de identidad necesaria. Tratar la reutilización del mismo ID con datos contradictorios como conflicto para revisión, sin nuevos efectos.
2. Registrar cada evento con unicidad por `event_id`. En una operación atómica, resolver duplicados y reservar a lo sumo un efecto por evento y tipo; guardar estados como recibido, reservado, enviando, enviado, incierto, bloqueado y error. La implementación concreta de transacción y unicidad queda por diseñar para el almacenamiento real.
3. Persistir STOP por usuario y hacer que la comprobación de consentimiento y la reserva del seguimiento se coordinen con su actualización. Antes del despacho, volver a comprobar el bloqueo y cancelar reservas aún no enviadas. Definir un punto de no retorno y serialización por usuario para gestionar carreras con STOP; no prometer revocar efectos ya despachados.
4. Usar una clave de idempotencia estable por efecto si el proveedor la admite. Tras timeout o resultado desconocido, conservar `incierto` y consultar el estado remoto por esa clave antes de decidir. Si no existe consulta fiable ni idempotencia, mantener en revisión humana sin reenvío automático; registrar evidencia y resolución. Un error confirmado previo al efecto puede reintentarse de manera controlada, previa comprobación de STOP.
5. Mantener credenciales fuera de ejemplos y registros; registrar sólo referencias y datos mínimos. La activación y cualquier envío necesitan autorización aplicable. El diseño no demuestra compatibilidad con una instancia ni con un proveedor concreto.

## Controles locales propuestos

| Control estático con datos sintéticos | Resultado esperado |
|---|---|
| A y B simultáneos | Una identidad e1 y una reserva como máximo; B observa el estado existente. |
| C con mismo texto y otro ID | e2 se evalúa independientemente, sin deduplicación por texto. |
| D seguido de E para el mismo usuario | STOP persiste; e4 queda bloqueado y no se despacha seguimiento. |
| STOP durante una reserva o despacho | Reserva aún no despachada bloqueada; despacho ya iniciado registrado y conciliado, sin garantizar revocación. |
| Timeout después de posible éxito | Estado incierto, consulta del proveedor y ningún reenvío ciego; si no hay consulta fiable, revisión humana. |
| ID ausente, identidad ausente o ID repetido con contenido contradictorio | Rechazo o revisión según el caso, sin efecto externo. |
| Dependencia no disponible o error confirmado | Estado y causa registrados; recuperación controlada sólo tras determinar que no hubo efecto y verificar STOP. |

Estos son controles derivados del texto, no pruebas ejecutadas: no se construyó ni activó un flujo, ni se comprobó runtime, versión, almacenamiento o proveedor. La siguiente acción concreta para la persona responsable de automatizaciones es especificar identidad de usuario, autorización de respuestas y capacidades de conciliación del proveedor; con esos datos podrá preparar una implementación de prueba y verificar los casos de la tabla antes de cualquier activación.

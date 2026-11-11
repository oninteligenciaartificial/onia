# Contrato local de estados y eventos

Este documento describe el motor de fixtures. El contrato de la retoma HTTP/SQLite está en [ADAPTADOR.md](ADAPTADOR.md).

Los estados pertenecen a clientes sintéticos, no al harness. `snapshot.version=1` conserva `clientes`, `referencias`, `vistos`, `salida`, `auditoria` y `reloj`. El llamador puede serializar y restaurar ese objeto para un ensayo; el workflow manual empieza vacío en cada ejecución. No hay persistencia entre ejecuciones de n8n implementada.

| Estado previo | Entrada | Resultado / salida preparada |
|---|---|---|
| Sin registro | NEGOCIO | `interesado`; ficha sin instrucciones de pago |
| Sin registro o interesado | GRUPAL / VIP | `pendiente`; importe, QR ficticio y aviso al operador |
| Pendiente | Imagen con o sin referencia ficticia | Sigue pendiente; acuse y aviso de revisión; cero accesos |
| Pendiente | Señal explícita completa del operador | `confirmado`; un acceso ficticio, si no venció y queda cupo |
| Pendiente | Importe/moneda/destino/movimiento incorrectos, referencia cambiada o compartida | `excepcion`; revisión humana, sin acceso ni instrucción de volver a pagar |
| Pendiente | Vencimiento de 24 h, comprobado por reloj, captura o confirmación tardía | `excepcion`, sin reintento automático |
| Confirmado | Señal repetida con igual referencia | `ya_confirmado`, sin otro acceso |
| Confirmado | Captura o inscripción posterior | No altera el pago; no genera otra inscripción |
| Excepción | Intento de confirmar | Rechazado; no se reabre automáticamente |
| Cualquiera | BAJA | `cese=true`, acuse único por evento y se detiene el contacto posterior |
| Cualquiera sin cese | AYUDA / entrada desconocida | Aviso local al operador / ayuda fija; no confirma nada |

El timeout de 24 h es una **propuesta técnica de ensayo**, no una condición comercial aprobada. El reloj es monotónico y lo aporta el llamador. La prueba usa milisegundos abstractos (1000, 2000…), sin datos personales. El límite exacto se considera vencido. Confirmado nunca se degrada por un vencimiento posterior. La reapertura de excepciones, correcciones y devoluciones quedan en manos humanas; no hay comando automático de recuperación comercial.

## Fronteras de confianza

`normalizarMeta(payload)` sólo acepta `ficticio=true`, recorre todos los `entry[].changes[].value.messages[]` y proyecta texto e imagen. Los `statuses` se ignoran. No descarga imágenes ni conserva el cuerpo crudo. `NEGOCIO`, `GRUPAL`, `VIP`, `AYUDA` y `BAJA` son los comandos fijos; el resto produce ayuda. Un comentario en Instagram no es una entrada WhatsApp: el puente desde el CTA sigue sin implementar. No se promete DM automático.

`recibirCliente(evento, ahora)` permite únicamente acciones del cliente. `confirmarOperador(evento, ahora)` es una API local separada. Exige `decision=confirmar`, `operador=operador-ficticio`, referencia, importe numérico exacto, `moneda=BOB`, `movimientoVerificado=true` y `destinoVerificado=true`. Estos campos **simulan una conciliación declarada; no autentican al operador ni comprueban un banco**. Ningún campo, texto o imagen de Meta puede seleccionar esta API. El canal `operador` del fixture es una entrada interna de confianza sólo para el ensayo; nunca se debe conectar a un webhook público.

En una integración futura, la entrada del operador debe autenticarse por un canal privado y autorizado por Sergio, vincularse a la inscripción/revisión vigente y auditar identidad, importe, moneda, destino y movimiento observado. Un ID de operador escrito por un cliente no puede cumplir esa condición. La firma HTTP de Meta, challenge GET y protección contra replays HTTP quedan pendientes: este motor no los implementa.

Todos los ID aceptados empiezan por `fixture-`; las referencias por `FICTICIO-`. Se rechazan entradas no ficticias y campos extra como `qr`, `qrPath`, `acceso` y `credentials`. El QR y el acceso son textos fijos no utilizables, sin imágenes ni enlaces. Para esta entrega no se leen archivos privados. No se agregan nombres, teléfonos o destinos reales.

## Idempotencia y pagos

La clave de transporte local es `canal:evento.id`. Un duplicado con idéntico objeto devuelve `duplicado` sin nueva salida; reutilizar ese ID con contenido distinto falla. El orden de las claves JSON no cambia la firma local. No es una firma criptográfica. Una segunda solicitud de inscripción con otro ID tampoco duplica QR ni cambia modalidad. La confirmación con otro ID y la misma referencia ya conciliada no duplica el acceso. Las referencias se normalizan a mayúsculas y se recortan en extremos; se reclaman al recibir la captura o al confirmar y no se liberan al vencer. Otro cliente que las use pasa a excepción.

Cada salida tiene un ID estable derivado del evento y su posición. Es una **intención local**, no un recibo de entrega. Las pruebas restauran el snapshot y vuelven a enviar la confirmación para verificar que no nace otro acceso. El límite VIP cuenta confirmaciones dentro del snapshot; no reserva cupo con una solicitud y no garantiza cupos bajo ejecuciones concurrentes.

Para uso real faltan una transacción durable que guarde deduplicación, unicidad de referencia, cupos y outbox atómicamente, y un adaptador de entrega con recibos privados. No usar el estado global del workflow como garantía de exclusión. Si falla una escritura, no enviar; si una entrega vence o su resultado es incierto, conservarla como indeterminada, conciliar su estado antes de reintentar y pedir revisión cuando no pueda resolverse. El ensayo no hace escrituras externas, no simula una entrega exitosa y no prueba concurrencia ni recuperación ante caída de un servicio.

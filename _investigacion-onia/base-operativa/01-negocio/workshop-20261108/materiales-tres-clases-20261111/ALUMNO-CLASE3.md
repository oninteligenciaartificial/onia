# Clase 3 · Describir y revisar una tarea repetida

Plantilla editable. Guardá una copia como `clase3-mi-practica.md` o trabajá en notas/papel. Negocio, personas, eventos, referencias y pagos de esta hoja son ficticios. La práctica se ejecuta leyendo y escribiendo un registro local.

ID anónimo ______. Fecha ______. Modo vivo / manual ______. Ayuda y paso ______.

## Resultado y preparación

Vas a guardar un procedimiento y probar qué pasa con una consulta repetida, una captura, una confirmación manual y una salida incierta. Tené la ficha, un registro vacío y una copia de la hoja. Podés pedir ayuda a Claude si tenés acceso verificado. El recorrido manual permite completar la revisión después del corte de Codex del 14.

## Caso ficticio Las Palmeras

La tienda recibe consultas sobre Canasta Mañana, Bs 35. En este ejercicio se registra una consulta, luego una solicitud de reserva con cantidad y franja de retiro. El dueño confirma disponibilidad y, si hay pago, lo coteja manualmente. El operador prepara una confirmación de retiro cuando están confirmados disponibilidad y pago. El envío se ensaya anotando un estado en la hoja.

Las claves y estados siguientes son una propuesta didáctica para probar a mano.

| Dato mínimo | Uso |
|---|---|
| ID de evento | Reconocer la repetición exacta de una entrada |
| ID de consulta | Vincular eventos nuevos de la misma consulta |
| Producto, cantidad y franja solicitada | Comprobar qué se pide |
| Disponibilidad y autor de confirmación | Conservar la decisión del dueño |
| Estado de pago y referencia ficticia | Separar captura recibida de pago confirmado |
| Estado de salida y referencia | Distinguir preparada, entregada o incierta |
| Última revisión y siguiente paso | Retomar después de una interrupción |

Estados de consulta propuestos, abierta → reserva por confirmar → reserva confirmada → retiro pendiente. Una incidencia agrega un pendiente de revisión en el mismo registro. BAJA detiene el seguimiento comercial y conserva lo necesario para atender una incidencia de compra.

## Ejercicio guiado

1. Escribí una frase que describa cuándo empieza y cuándo termina la tarea.
2. Completá el procedimiento antes de mirar el ejemplo.
3. Recorré los cinco eventos en orden, agregando una fila por revisión. Para E02, reconocé el evento repetido y conservá la consulta existente.
4. Al llegar a una salida incierta, escribí qué evidencia tendría que comprobar el operador antes de repetirla.
5. Cerrá la hoja y retomá desde la última fila. Guardá entrada, registro, procedimiento corregido y pendientes.

### Mi procedimiento

| Campo | Completar |
|---|---|
| Tarea pequeña y resultado esperado | ______ |
| Disparador de inicio | ______ |
| Datos mínimos | ______ |
| Dónde queda el registro local | ______ |
| Clave para entrada duplicada | ______ |
| Cómo vincular un evento nuevo a consulta existente | ______ |
| Paso 1 de recepción y revisión | ______ |
| Paso 2 de reserva y disponibilidad | ______ |
| Paso 3 de confirmación manual | ______ |
| Paso 4 de preparación y salida | ______ |
| Responsable de cada decisión | ______ |
| Qué hacer si falta un dato | ______ |
| Qué hacer con captura recibida | ______ |
| Qué hacer con envío incierto | ______ |
| Qué hacer ante BAJA | ______ |
| Cómo retomar tras corte | ______ |
| Evidencia que consideraría éxito | ______ |

### Pedido opcional para copiar

```text
Ayudame a revisar un procedimiento manual del caso ficticio Las Palmeras.
Recibimos consulta por Canasta Mañana, Bs 35. Pedimos cantidad y franja de
retiro. El dueño confirma disponibilidad y coteja manualmente cada pago.
El operador prepara la confirmación cuando disponibilidad y pago constan
confirmados. Usamos ID de evento para repetidos e ID de consulta para
vincular entradas nuevas. Una captura queda pendiente de revisión.
Una salida incierta requiere comprobar el historial antes de repetir.
BAJA detiene seguimiento comercial. Si falta cantidad o franja, pedir ese
dato. Escribí pasos, datos mínimos, responsable, control de duplicados,
tratamiento de fallos y evidencia de éxito. Dejá decisiones pendientes
visibles. Vamos a probarlo escribiendo cinco eventos en un registro local.
```

### Cinco eventos ficticios para recorrer

| Turno | Entrada de prueba | Lo que decidí y por qué |
|---|---|---|
| E01 | Evento EVT-F01, consulta CON-F01, una canasta para retiro 09:00–09:30. Dueño todavía pendiente | ______ |
| E02 | Llega otra vez EVT-F01 con exactamente los mismos datos | ______ |
| E03 | Evento EVT-F02 de CON-F01, llega captura por Bs 35. Dueño confirma disponibilidad, revisión de pago pendiente | ______ |
| E04 | Evento EVT-F03, dueño coteja manualmente Bs 35 y confirma pago con referencia ficticia PAG-F01 | ______ |
| E05 | Operador intenta confirmar retiro, registra salida SAL-F01, la recepción queda incierta | ______ |

### Mi registro vacío

Agregá filas según el recorrido. Conservá la versión anterior y la revisión más reciente de la misma consulta.

| Turno | Evento / consulta | Disponibilidad | Pago / referencia | Salida / referencia | Autor de revisión | Siguiente paso |
|---|---|---|---|---|---|---|
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |
| ______ | ______ | ______ | ______ | ______ | ______ | ______ |

### Pruebas adicionales de la extensión

Una entrada nueva pide reservar y omite cantidad. Decisión ______.

Otra entrada solicita BAJA del seguimiento. Decisión ______.

Una interrupción cierra la hoja después de E05. Antes de seguir, leería ______. Evidencia que buscaría para SAL-F01 ______.

## Referencia escrita · caso ficticio resuelto

Procedimiento docente propuesto para revisión manual.

1. Operador busca ID de evento en el registro. Si ya consta, anota repetición y conserva la misma consulta. Para un evento nuevo, usa el ID de consulta existente o abre una consulta si corresponde.
2. Verifica producto, cantidad y franja. Pide el dato mínimo faltante y espera. El dueño decide disponibilidad.
3. Registra captura como pendiente de revisión. El dueño coteja movimiento, importe y referencia y anota su confirmación. Una referencia de pago ya usada se concilia antes de asociarla a otra consulta.
4. Con disponibilidad y pago confirmados, el operador prepara una confirmación con cantidad/franja y un identificador de salida. Revisa si esa salida ya fue entregada o quedó incierta antes de ejecutar el siguiente paso.
5. Registra resultado. Si el resultado queda incierto, consulta historial y evidencia de recepción. Si se acredita entrega, la marca entregada. Si se acredita fallo, prepara un reintento controlado conservando la referencia previa. Mientras falte evidencia, mantiene revisión pendiente.
6. Ante corte, recupera la última versión y sus referencias. Ante BAJA, detiene seguimiento comercial y deja registrada la solicitud para el operador.

| Turno | Evento / consulta | Disponibilidad | Pago / referencia | Salida / referencia | Autor de revisión | Siguiente paso |
|---|---|---|---|---|---|---|
| E01 | EVT-F01 / CON-F01 | Pendiente | Pendiente | Pendiente | Operador ficticio | Pedir confirmación al dueño |
| E02 | Repetido EVT-F01 / CON-F01 | Pendiente | Pendiente | Pendiente | Operador ficticio | Mantener consulta única |
| E03 | EVT-F02 / CON-F01 | Confirmada por dueño | Captura, revisión pendiente | Pendiente | Dueño y operador ficticios | Cotejo manual del pago |
| E04 | EVT-F03 / CON-F01 | Confirmada | Confirmado por dueño / PAG-F01 | Preparada / SAL-F01 | Dueño y operador ficticios | Revisar e intentar salida una vez |
| E05 | Intento local / CON-F01 | Confirmada | Confirmado / PAG-F01 | Incierta / SAL-F01 | Operador ficticio | Comprobar historial/recepción antes de decidir |

En el recorrido hay una consulta única, tres IDs de evento de entrada, una referencia de pago y una de salida. E05 es el resultado del intento local. La entrega permanece pendiente de evidencia. En la extensión, falta cantidad → pedir cantidad. BAJA → detener seguimiento comercial. Reinicio → leer E05 y comprobar SAL-F01 antes de actuar.

## Autoevaluación y recuperación

| Criterio | Logrado / con ayuda / pendiente y evidencia |
|---|---|
| Identifiqué disparador, datos, pasos, responsable y salida | ______ |
| Reconocí EVT-F01 repetido y conservé consulta única | ______ |
| Captura quedó pendiente de confirmación manual | ______ |
| Confirmación identificó dueño y PAG-F01 | ______ |
| Envío incierto quedó pendiente de evidencia antes de reintento | ______ |
| Expliqué cómo retomar, pedir dato faltante y atender BAJA | ______ |
| Guardé y reabrí procedimiento, registro y pendientes | ______ |

Archivo o nota ______. Última fila recuperada ______. Próximo paso ______.

La práctica de revisión queda completa cuando podés justificar cada decisión con el registro. La implementación futura necesita conexión autorizada, datos privados y pruebas del canal real. La demostración real de OnIA elegida por Sergio sigue pendiente en este corte. [Capacidades documentadas y límites](FUENTES-Y-REUSO.md).

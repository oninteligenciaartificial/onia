# Decisiones de Sergio para armar la fábrica

Registro iniciado el 10-nov-2026, 07:58–08:00 America/La_Paz, en el chat de Boss. La tabla incorpora las confirmaciones directas posteriores de Sergio en Codex del 11-nov. Las entradas fechadas anteriores se conservan como historia; ante un conflicto rige la confirmación más reciente de Sergio.

| Tema | Decisión |
|---|---|
| Canal del chatbot | WhatsApp Cloud API (Meta) con n8n. Queda inactivo hasta el sí de Sergio. |
| Horarios del workshop (America/La_Paz) | Viernes 13 de noviembre a las 20:00; sábado 14 a las 14:00; lunes 16 a las 20:00. Confirmación directa en Codex el 11-nov; sustituye también la entrada de Boss de las 07:34. |
| Plataforma de las clases | Google Meet. |
| Cupos del grupo | Sin límite. |
| Precio del grupo | Bs 50. |
| VIP | Bs 150, 5 cupos, llamada de 30 minutos. Se ofrece esta semana. |
| QR de pago | Sergio se lo pasa directo a Codex en el VPS. Se guarda privado y nunca va a Git. |
| Higgsfield | Pieza por pieza, cada una con el sí de Sergio. |
| Autor de los 5 guiones diarios | Contenido. |
| Confirmación de pagos | Sergio, a mano. Una captura no basta para confirmar. |

Pendiente: la verificación del número en Meta, que es un paso humano de Sergio.

## Agregado 08:22: guiones y plan B

- **Hasta el viernes 13:** Codex escribe los 5 guiones diarios mediante el harness, Contenido los revisa como editor y Sergio los ve y aprueba en el panel.
- **Desde el sábado 14:** Contenido escribe los guiones con las reglas que deje Codex.
- **Plan B, si la venta no alcanza la meta:** se paga Claude, que reemplaza a Codex en los guiones y el trabajo pesado. El harness y el panel siguen iguales; sólo cambia el modelo ejecutor. El gasto lo aprueba Sergio con un sí explícito.

## Decisiones comerciales (10 nov 2026 16:08 La Paz)

- Quién atiende NEGOCIO: la automatización responde cuando alguien comenta la palabra clave (sin activar nada hasta su sí).
- VIP: llamada privada viendo el caso del negocio o personal de la persona.
- Política de devolución: cero devoluciones.
- Soporte: al terminar el workshop, grupos de WhatsApp (privados o públicos) más la comunidad pública, como flujo constante para que quien ya hizo un workshop vuelva a contratar.

## Nombre del workshop (10 nov 2026 16:20 La Paz)

Sergio eligió: «Tu negocio con IA: ordena, vende y automatiza». Se descarta «Automatiza tu vida y sé más saludable con IA». Los guiones T01–T05 de guiones-tanda-20261111 mantienen el enfoque negocio; aplicar los cambios de texto de Contenido.

## Nombre final del workshop (10 nov 2026 16:21 La Paz)

Reemplaza la entrada de las 16:20. Nombre final: «Claude de 0 a 100: tu negocio con IA». No usar el logo de Claude/Anthropic como propio; mencionar el nombre está bien. Aplicar en guiones-tanda-20261111 y materiales de venta.

## Alcance de anuncios, guiones y canales (10 nov 2026 17:31 La Paz)

- Los tipos de anuncio y de guion nombrados (artes, UGC, ugly ads, talking head; noticia IA, B-roll, personal, venta) son ejemplos, no una lista cerrada. El panel y cada encargo deben contemplar todos los tipos relevantes (p. ej. carrusel, testimonio, demo de pantalla, antes/después, oferta directa, retargeting, historias, lead ads, mensajes a WhatsApp) e incorporar los que Sergio vaya mencionando.
- Cada canal (Instagram, Facebook, TikTok, YouTube, X, WhatsApp, comunidad, Meta Ads) debe quedar documentado y probado de punta a punta (entrada, respuesta, derivación, pago, acceso, soporte y medición) antes de considerarse listo. Documentado o conectado no equivale a probado.

## Prioridad de ingresos y cuota · 10 nov 2026, noche de La Paz

Decisión directa de Sergio en Codex: «Quita el limite de 90% lo de las mas de 3 sesiones queda pendiente tenemos hasta el 14 de noviembre para los ingresos».

- Retirar la reserva interna del90% para trabajo ya autorizado; usar el saldo incluido disponible sin autorizar compras ni saldo extra. Aplicado en el VPS mediante política privada100; no es una ampliación de cuota del proveedor.
- Mantener máximo3 sesiones simultáneas. La medición para superar3 queda pendiente; no ejecutar ni programar el ensayo91→93.
- Prioridad hasta el14 de noviembre: ingresos. Retomar las entregas existentes útiles para vender y completar sus requisitos; no condicionar el trabajo independiente del VPS a terminar benchmarks o al homelab.
- Sustituye la secuencia anterior de cerrar toda la infraestructura antes de avanzar en ingresos. Homelab conserva su pendiente y no se presenta como listo. No cambia permisos de publicación, mensajes comerciales, cobro, gasto, n8n ni producción; ninguna entrega se acepta sin su evidencia y autoridad correspondientes.

## Horario definitivo del workshop · 11 nov 2026, 07:34 La Paz

**Sustituido por la confirmación directa en Codex al final de este documento.** Se conserva para explicar el desajuste con los eventos de Calendar informados por Boss.

Decisión directa de Sergio en chat con Boss: «Para que haya tiempo de vender movamos un día la clase, inicia el viernes, para agarrar más cupos». Antes había pedido bajar la hora a las 20:00.

- Clase 1 Ordenar: viernes 13 nov, 20:00–21:30 (America/La_Paz).
- Clase 2 Vender: sábado 14 nov, 20:00–21:30.
- Clase 3 Automatizar: domingo 15 nov, 14:00–15:30.
- Sustituye las fechas anteriores (jue 12 / vie 13 21:00, sáb 14 14:00) en oferta, guiones, textos del bot, calendario de contenido y n8n.
- Pendiente de Sergio: la clase 1 se pisa con su bloque «Novia» (vie 18:00–21:00).

## Reparto de trabajo con Codex · 11 nov 2026, 07:40 La Paz

Sergio: «Necesitamos que todos usen a Codex […] y tengo que tener el panel listo».

- Todos los agentes (Contenido, Infraestructura/Operaciones, Calendario, Boss Life) mandan el trabajo pesado a Codex con `onia-llm` en la computadora compartida y solo coordinan y revisan. Boss conserva el puente al VPS para repo grande y tareas con revisor.
- Todo el trabajo y el contexto deben quedar en este repo; nunca secretos, QR de pago, enlaces autenticados ni medios privados.
- Prioridad: panel listo (lista abierta de tipos, calendario con fechas nuevas, sala de montaje) y corrección de fechas. Propuesto por Boss; lanzamiento pendiente de confirmación de Sergio.

## Confirmaciones directas en Codex · 11 nov 2026

Fuente: Q&A de Sergio en esta conversación. Pidió comprender las fábricas de los dos videos de Euge y explicar cómo se usarán el harness y sus sesiones, por secciones.

- Fechas de las tres clases: viernes 13 a las 20:00; sábado 14 a las 14:00; lunes 16 a las 20:00, America/La_Paz. Respuesta literal sobre las horas: «Viernes 8pm / Sabado 2pm / Lunes 8pm». No se confirmó una hora de finalización nueva.
- Esta confirmación sustituye jueves/viernes/sábado y la interpretación viernes/sábado/domingo de Boss. Su bitácora informa eventos Meet con el horario sustituido: deben conciliarse con esta decisión. Actualizar este archivo no modifica Calendar, mensajes del bot ni guiones existentes.
- Cobrador: envío de QR y seguimiento; Sergio confirma cada pago. No detectar ni confirmar cobros automáticamente desde el banco; una captura no concede acceso.
- «BCL» significaba VSL, video de venta del curso.
- Meta inmediata: Bs 3.000. Prioridades pedidas: ampliar el panel existente con fábricas, cerebro, pasos y revisiones; automatizar ideas/noticias/guiones y calendario; cinco piezas diarias y salidas horizontal/vertical; sala de montaje con explicación de cambios; WhatsApp, Instagram/Facebook y n8n; curso, VIP y anuncios. Los formatos son lista abierta.
- El vlog diario sigue entero y fuera del editor de la fábrica. No interpretar horizontal/vertical como diez ideas ni como permiso para cortar el vlog.
- El límite de tres sesiones se conserva y medir más de tres sigue pendiente. No se restablecen las seis altas diarias ni la reserva interna del 90%.
- La suscripción se sigue planificando con corte el 14: la clase del lunes 16 necesita materiales y operación que no dependan de una sesión de Codex. No hay autorización de renovación, API de pago ni proveedor sustituto.
- El reparto detallado de sesiones está propuesto en CIERRE-VENTA-20261111.md. Este registro no acredita lanzamientos, cambios en rutinas de Grok ni configuración de ejecución automática.

## Primera tanda autorizada y punto de parada · 11 nov 2026

Sergio aprobó lanzar panel, guiones/calendario y WhatsApp del plan 2cb5050. Alcance y contrato compartido: 04-operacion-agentes/evidencias/tanda-fabricas-20261111/ALCANCE-v1.md. Al entregar, parar para revisión con la coordinadora/Sergio; no pasar a la siguiente tanda ni integrar/aceptar automáticamente estos productos. Esta autorización sustituye el estado aparcado y los topes históricos del encargo del panel. Conserva tres sesiones, sin hijos, y los permisos sensibles vigentes.

## Confirmaciones de operación — 11 noviembre 2026

- Sergio confirmó directamente en Codex que la tanda de cinco guiones debe estar lista a las **18:00 America/La_Paz**, desde el12nov. Es hora de entrega; el inicio necesita margen medido y no restaura la rutina histórica pausada de07:00.
- Sergio confirmó que el número del workshop **ya está verificado en Meta**. Es confirmación del titular; todavía no acredita acceso API, recepción de webhook, envío real ni recorrido de pago/acceso. Esas pruebas conservan sus permisos y evidencia propios.

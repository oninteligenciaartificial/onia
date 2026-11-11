# 4 · Chatbot de WhatsApp

## Estado vigente · 11 nov UTC

La vía elegida es Cloud API + n8n. Ya está el [adaptador local revisado](trabajos/fabrica-chatbot-whatsapp-20261110/ADAPTADOR.md), con persistencia, confirmación manual autenticada y pruebas locales. El workflow de despacho está inactivo y sin credencial; el workflow anterior de fixtures sigue siendo sólo ensayo. Faltan configuración privada, importación/conexión autorizadas y prueba real. Horarios/VIP/Meet están definidos en [DECISIONES-SERGIO](../DECISIONES-SERGIO-20261110.md); faltan los enlaces privados, no la decisión de plataforma.

El detalle de cierre está en [CIERRE-VENTA-20261111.md](../CIERRE-VENTA-20261111.md).

## Especificación original del 10 nov · histórica

Lo siguiente conserva la propuesta inicial. Sus pendientes y pedidos se cotejan con el estado vigente y las decisiones actuales; no se vuelven a lanzar ni se reutilizan sus textos comerciales anteriores.

Especificación del recorrido de venta: comentario NEGOCIO → información → inscripción pendiente → QR → Sergio verifica el pago a mano → acceso. Es el frente 1 del [plan al 13](../../../04-operacion-agentes/PLAN-LISTO-AL-13-20261110.md): sin este recorrido no hay ventas del workshop. Boss no configura WhatsApp ni n8n.

## Qué hace

Atiende a quien pide información del workshop y lo lleva hasta el pago y el acceso, con **respuestas fijas** (sin un modelo de IA). Así puede seguir funcionando después del 14. Una captura de pantalla no confirma el pago.

No se afirma que exista hoy una configuración activa de WhatsApp, del número de Meta ni de un bot respondiendo.

## Cómo lo hace Euge

Euge no muestra un chatbot de WhatsApp con QR en esos dos videos.

Lo más parecido, y lo que **no** copiamos:

- Video 1, [0:42–1:00](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=42s) y el cierre: presenta Clonify como plataforma de embudos, formularios y email marketing. Eso es su producto, no la infra de OnIA.
- Video 1, [27:12–28:14](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1632s): Leader Summaries apunta a una oferta y publica solo, sin revisión. Él mismo dice que tiene pocas visitas. En OnIA no se publica ni se cobra sin revisión.

La venta del workshop es un problema nuestro, no una receta suya.

## Cómo lo hacemos en OnIA

El pedido de Sergio de esta tanda fija el canal como **WhatsApp**. Siguen pendientes el número, si se usa la app de WhatsApp Business o la Cloud API, la imagen del QR (privada, fuera de Git), la hora del jueves 12 y los cupos.

Dos opciones técnicas, a decidir con Sergio:

1. **WhatsApp Business (la app) con respuestas rápidas o catálogo.** Cero código nuevo. Sergio o quien él designe pega los textos fijos. Es la vía mínima si hay que vender esta semana.
2. **WhatsApp Cloud API + n8n.** Requiere número y verificación de Meta. Codex, si hay sí, arma un workflow **nuevo e inactivo** con respuestas fijas. Se activa sólo con otro sí, después de una prueba con datos ficticios.

En ambos casos las respuestas son el texto aprobado por Contenido, no un modelo.

**Veredicto infra OnIA: parcial.** El recorrido comercial está escrito. La app de Business no necesita infra extra. La vía Cloud API + n8n es posible con el n8n del VPS, pero no está construida ni se afirma verificación de Meta.

## Entra / sale

| Entra | Dónde | Sale | Dónde |
|---|---|---|---|
| Comentario o mensaje NEGOCIO | Publicación de G01 (u otra pieza de venta) y el WhatsApp que Sergio confirme | Respuesta de información (borrador abajo) | El mismo chat |
| Nombre, contacto autorizado y a qué se dedica | Mensaje de la persona | Inscripción pendiente de pago, con ID interno privado | Registro privado fuera de Git |
| Imagen del QR | Archivo privado del VPS o del teléfono de Sergio; **nunca Git** | El QR se envía por el chat | WhatsApp |
| Captura o referencia de pago | El chat | Estado: confirmado, incierto o excepción, después de que Sergio mire su banco | Respuesta fija + acceso cuando corresponda |

Drive no es el canal de este chatbot. El repo guarda sólo textos y el contrato, no destinos ni el QR.

## Quién la hace

- **Contenido:** redacta y aprueba los textos fijos.
- **Codex:** si se elige n8n + Cloud API, implementa el flujo inactivo y los tests, hasta el 13.
- **Boss:** especifica y revisa el recorrido; no pega el QR ni confirma pagos.
- **Sergio:** confirma el canal operativo, guarda el QR en privado, verifica cada pago a mano, autoriza el alta y manda el acceso.
- **Operaciones:** puede llevar el registro privado y el soporte, si Sergio se lo pide.

## Criterio de «bueno»

- El interesado recibe la ficha (nombre, para quién es, tres clases, 12–14 de noviembre, Bs 50 grupal, clase 1 con Claude) sin instrucciones de pago en el primer mensaje.
- No se promete DM automático, plaza reservada, VIP ni hora del jueves mientras esté pendiente.
- Interesado, inscrito pendiente y pagado son estados distintos.
- La captura sola no confirma. Se contrastan importe, moneda y movimiento real.
- El acceso se manda sólo después del pago confirmado, a una cuenta propia de la persona, sin credenciales ajenas.
- Los textos siguen iguales sin un modelo: sirven el 14 y después.

## Cómo se mide

Al final, con datos reales y ventana: mensajes NEGOCIO únicos, personas que recibieron la ficha, inscripciones pendientes, pagos conciliados, accesos enviados, excepciones y pedidos de cese. No se pronostica conversión. Un gasto, una devolución y un cobro se anotan por separado.

## Borrador de mensajes fijos

Tomados o adaptados de [OFERTA-Y-RECORRIDO.md](../../../01-negocio/workshop-20261108/noche-20261109/OFERTA-Y-RECORRIDO.md). **Borrador para revisión de Contenido.** No se envían hasta su dictamen y el sí de Sergio.

**1 · Respuesta a NEGOCIO (información, sin pago)**

> Gracias por tu interés. El workshop Tu negocio con IA: ordena, vende y automatiza está dirigido a dueños de pequeños negocios de Santa Cruz. Son tres clases, el 12, 13 y 14 de noviembre, a Bs 50 grupal. La primera es práctica con Claude. Estamos completando horarios con zona, canal y requisitos de acceso antes de confirmar inscripciones.

**2 · Inscripción pendiente** (borrador OnIA; no está literal en la ficha)

> Si querés anotarte, decime tu nombre, un contacto y a qué te dedicás. Te dejo inscrito pendiente de pago. El lugar se confirma cuando Sergio verifique el pago.

**3 · Envío del QR** (sin imagen en Git)

> Acá está el código para el pago de Bs 50 grupal. Cuando pagues, enviá una captura. Eso no confirma el pago: Sergio lo verifica y te avisa.

**4 · Pago confirmado** (el enlace o el lugar de la clase lo completa Sergio; no inventarlo)

> Pago confirmado. Te mando el acceso a la clase por este mismo chat.

**5 · Pago no encontrado o referencia repetida**

> Todavía no vemos el pago con ese importe y esa referencia. Lo revisamos antes de pedirte que intentes de nuevo.

Pendientes que bloquean un texto publicable: imagen del QR y a nombre de quién; hora del jueves 12; cupos; lugar o plataforma de las clases; si el VIP entra o no (hoy queda fuera).

## Qué existe y qué falta

Ya está la ficha y el recorrido mínimo en [OFERTA-Y-RECORRIDO.md](../../../01-negocio/workshop-20261108/noche-20261109/OFERTA-Y-RECORRIDO.md), y el CTA de [G01](../../../01-negocio/workshop-20261108/noche-20261109/GUION-01-WORKSHOP.md). Hay piezas de Telegram y n8n inactivas ([20261109-telegram](../../fabrica-contenido/20261109-telegram/README.md)); no son este chatbot de WhatsApp.

Falta todo lo operativo de WhatsApp y la prueba de punta a punta con datos ficticios.

## Desde el 14 sin Codex

Funciona si las respuestas quedaron fijas (en la app de Business o en un workflow ya activado con sí). Si el flujo depende de un modelo, el 14 se corta la venta.

## Pedido para Codex

Frente 1. Prioridad máxima de implementación, después de que Sergio elija la opción técnica y deje el QR en privado. Boss no configura el número ni n8n.

- **ID sugerido:** `fabrica-chatbot-whatsapp-20261110`
- **Rutas exclusivas:** `05-herramientas/fabrica-onia/4-chatbot-whatsapp/` (un workflow n8n nuevo iría como archivo en esta carpeta; no editar los workflows ya inventariados).
- **Qué construir:**
  - Si Sergio elige la app de Business: un paquete de textos versionados y un checklist de carga manual. Sin API.
  - Si elige Cloud API + n8n: workflow nuevo e inactivo con los textos fijos, estados interesado / pendiente / pagado / excepción, y un gancho para que un humano marque «pago confirmado». El QR se lee de un archivo privado del VPS, fuera de Git.
- **Criterio de aceptación:** prueba con datos ficticios: mensaje de interés → ficha → pendiente → entrega de un QR de prueba (no el real en Git) → marca de pago confirmado → mensaje de acceso de prueba. Captura sola no pasa a «pagado».
- **Tests:** casos de duplicado, timeout de pago, referencia repetida y rechazo a guardar el QR en el repo. Sin envíos reales.
- **Qué no tocar:** workflows existentes de n8n, Telegram real, G01/G02 salvo lectura, el plan fijado, secretos, el QR verdadero, activar el flujo, publicar o cobrar.

## Decisión de Sergio, 10-nov-2026 07:58 America/La_Paz

**Canal: WhatsApp Cloud API de Meta, con n8n.** Queda descartada la app WhatsApp Business manual. Esto cambia el pedido de arriba:

- **Codex** primero comprueba qué existe: la app de Meta, el número, la verificación del webhook y la credencial en n8n. Hay rastros de una configuración previa de verificación de WhatsApp en el entorno de Boss, pero no se afirma que funcione. Después construye el flujo n8n con respuestas fijas: información, inscripción pendiente, QR y aviso a Sergio. El flujo queda **inactivo**.
- **El paso humano lo hace Sergio** en Meta: el número, la verificación del negocio si la pide y aceptar los permisos. Las contraseñas y tokens los escribe él, nunca en el chat ni en Git.
- **La activación** del flujo de n8n y del webhook de Meta necesita el sí de Sergio, después de una prueba con un número de prueba.
- **El pago** lo sigue confirmando Sergio a mano. El bot no da por pagado a nadie.
- **Riesgo de tiempo:** la verificación de Meta puede demorar. Si el jueves 12 no está aprobada, el plan B es que Sergio responda a mano con los mismos textos fijos.

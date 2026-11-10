# Plan: todo listo al viernes 13

Boss, 10-nov-2026 ~07:50 America/La_Paz. Organiza lo ya decidido; **no cambia el plan fijado** ([modelo único](ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md), 573b302/777fd23). Cada tarea de Codex va por el harness con su ID y una revisión distinta. Cuando la conexión esté lista, Boss la pide directamente; hasta entonces la pide Sergio.

## Restricciones que mandan

- **Workshop:** jueves 12 (hora pendiente), viernes 13 a las 21:00 y sábado 14 a las 14:00, todo America/La_Paz. Bs 50 grupal. **Sin chatbot con QR no hay ventas.**
- **Codex:** ~20 % de cuota (Sergio, 10-nov 07:39). La suscripción termina el 14 y no se renueva. Lo que deba seguir funcionando tiene que quedar el viernes 13 como script con tests, que corra sin modelo.
- **Infraestructura:** VPS sin GPU, FFmpeg, transcripción por CPU, Higgsfield (pago) para elementos de IA y Drive como sala de montaje. Gasto cero adicional. Publicar, cobrar, n8n y la PC necesitan el sí de Sergio.
- **Roles:** Contenido hace los guiones y la línea editorial. Boss coordina, revisa y mueve los archivos de Drive. Codex hace la implementación pesada hasta el 13. Sergio graba, aprueba y publica. El vlog no se corta.

## Cuatro frentes, en orden de prioridad

| # | Frente | Entra | Sale | Quién | Listo cuando | Funciona sin Codex desde el 14 |
|---|---|---|---|---|---|---|
| 1 | **Venta: NEGOCIO → QR → acceso** | G01, la ficha de oferta, el QR de Sergio y el canal elegido | Chatbot mínimo que responde la información y entrega el QR; registro privado de interesados; Sergio confirma cada pago a mano | Contenido (textos), Codex (flujo), Sergio (QR y verificación) | Prueba con datos ficticios: comentario → info → QR → "pago confirmado" → enlace de la clase | Sí, si es un flujo fijo sin modelo. Respuestas fijas, no IA. |
| 2 | **G01 publicable** | G01 y su revisión | Versión aprobada por Sergio con un solo CTA | Contenido propone, Boss revisa, Sergio aprueba | Dictámenes en `revision-boss-g01-20261110` y sí de Sergio | Sí (es trabajo editorial). |
| 3 | **Edición en el VPS** | Grabación de la tanda en Drive `1 Entrada`; clips en `2 B-roll` | Por guion: corte 9:16 con subtítulos, en `3 Sala de montaje` | Boss mueve los archivos; el script de Codex corta y renderiza; Sergio revisa | Una pieza real (G01) pasa la lista de comprobación: frases sin cortar, subtítulos correctos, legible en móvil, sonido revisado | Sí: el script fijo corre con un comando. Las decisiones de corte dudosas las marca para revisión humana. |
| 4 | **Conexión Boss–Codex** | `conexion-boss-codex-20261110` | Adaptador mínimo, llave restringida, aviso por webhook | Codex; Boss prueba; Sergio copia la URL y la clave una vez | Tarea de juguete de punta a punta y petición repetida con un solo intento | Parcial: el registro y el SSH siguen; no quedan ejecutoras Codex. |

Cuota: el frente 4 ya está empezado y debe quedar **mínimo**. El frente 3 es el que más cuota consume. Si la cuota no alcanza, se recorta el 3 antes que el 1: el 1 trae la plata.

## Día por día

**Martes 10**
- Codex: frente 4, versión mínima. Boss lo prueba apenas lo suba.
- Contenido y Boss: revisión de G01 y del recorrido de venta (frente 2), con dictámenes en el repo.
- **Sergio:** responde las preguntas de abajo, sobre todo el canal del chatbot y el QR.

**Miércoles 11**
- Codex: frente 1. Es el flujo del chatbot. Si se usa n8n, se crea inactivo y se activa sólo con el sí de Sergio.
- Sergio: graba la primera tanda (G01 y los demás guiones del día) y la sube a `1 Entrada`.
- Codex: empieza el frente 3 con esa grabación real.
- Sergio publica G01 aprobado, editado a mano si el script todavía no está.

**Jueves 12 (clase 1)**
- Prueba del chatbot de punta a punta. Si pasa y Sergio da su sí, se activa.
- Codex cierra el frente 3: el script con tests y el manual de uso.
- Boss corre la tanda del día con el script y la deja en `3 Sala de montaje`.

**Viernes 13 (clase 2, 21:00): entrega para funcionar sin Codex**
- Codex deja: el manual de operación sin Codex (comandos, qué hacer si falla), el estado de cada tarea en el harness y el registro de errores al día. Nada queda a medias en ramas.
- Boss verifica que puede correr la edición y el chatbot sin Codex, y te da el reporte.

**Desde el sábado 14:** Contenido escribe los guiones, Sergio graba, Boss mueve los archivos y corre el script, Sergio revisa y publica. La mejora del estilo queda como reglas escritas en el repo a partir de los ejemplos antes/después; eso va al final.

## Preguntas para Sergio (sólo lo que bloquea)

1. **Canal del chatbot:** ¿WhatsApp, Telegram, o DM de Instagram/TikTok? (En el VPS ya hay piezas de Telegram y n8n.)
2. **QR:** ¿dónde está la imagen y a nombre de quién? No va a Git: se guarda privada en el VPS.
3. **¿Quién confirma los pagos?** ¿Vos, mirando tu banco?
4. **Hora de la clase del jueves 12**, el lugar o plataforma de las clases y el cupo máximo.
5. **VIP:** ¿20 o 30 minutos? ¿O lo dejamos fuera esta semana?
6. ¿Cuántos créditos de Higgsfield podemos usar por día?

## Qué no se hace esta semana

No hay bots nuevos. Tampoco publicación automática, anuncios pagos, más análisis de Euge, el despachador B ni subir el límite de 3 sesiones. La rutina diaria de las 07:00 sigue pausada hasta que pasen los frentes 1 y 3.

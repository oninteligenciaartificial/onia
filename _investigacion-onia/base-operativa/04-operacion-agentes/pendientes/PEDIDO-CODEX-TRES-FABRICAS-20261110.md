# PEDIDO a Codex: registrar tres tareas de fábrica (sin lanzar)

Estado: **PROPUESTO por Boss, 10-nov-2026 13:00 America/La_Paz. No autorizado para ejecutar.**
Este pedido no amplía la autorización de Sergio (regla 1). Registrar y habilitar cada ID requiere su sí aplicable; lanzar requiere otra orden.

## Comprobado hoy (fuente y hora)
- Puente `consultar`, 12:57 La Paz: los tres IDs devuelven `id_no_habilitado`. No hay registro en `04-operacion-agentes/tareas/`.
- Cuota semanal compartida: 80 % a las 12:42 La Paz (RECIBO-CIERRE-v1.json, muestra 16:42 UTC), saldo extra 0.
- Fichas existentes: `05-herramientas/fabrica-onia/4-chatbot-whatsapp/README.md`, `2-edicion-video/README.md`, `1-guiones-calendario/README.md` y tabla 5 de `DICTAMEN-HARNESS-Y-SESIONES-BOSS-v1.md`.

## Límites comunes propuestos
Modelo `gpt-6.1-sol`, 0 hijos, máximo 1 ejecutora + 1 revisora distinta por ID, máximo 2 intentos por ID. Parar si la cuota supera el 90 % o si falta una entrada. En ese caso, conservar el trabajo y reportar. Activar `avisos_fin_ids` para cada ID. Sin n8n activo, sin publicar, sin secretos en Git.

## 1. `fabrica-chatbot-whatsapp-20261110`
- Objetivo: flujo n8n nuevo **inactivo** para WhatsApp Cloud API con textos fijos y estados interesado / pendiente / pagado / excepción. El pago se marca a mano.
- Entradas: decisiones de Sergio (07:58 y 08:00), textos de venta, QR privado en el VPS fuera de Git.
- Rutas exclusivas: `05-herramientas/fabrica-onia/4-chatbot-whatsapp/`.
- Aceptación: prueba ficticia de interés → ficha → pendiente → QR de prueba → pago marcado a mano → acceso de prueba. Una captura sola no pasa a pagado. Tests de duplicado, timeout, referencia repetida y rechazo del QR en el repo.
- Esfuerzo: `high`. Responsable: Codex. Revisor: sesión distinta, `high`.
- Falta comprobar: si el QR ya está en el VPS, y si existen la app de Meta y el número.

## 2. `guiones-tanda-20261111`
- Decisión de Sergio, 10-nov-2026 12:59 La Paz: **hasta el 13, Codex redacta los 5 guiones y Contenido los revisa como editor**. Sergio aprueba en el panel. Desde el 14 los escribe Contenido. Es una excepción acotada a la regla 5.
- No reutilizar `fabrica-guiones-paquete-20261110`: es el comprobador sin modelo y queda propuesto aparte, con prioridad baja.
- Objetivo: cinco paquetes para grabar el 11 (venta, marca, noticia o evergreen, segunda venta o marca, reel de prueba), siguiendo el cerebro, G01/G02 y `CALENDARIO-SEMANA-20261110-14.md`.
- Rutas exclusivas: `05-herramientas/fabrica-onia/1-guiones-calendario/salida/`. Esfuerzo `low`.
- Aceptación: un solo CTA por pieza, hora y precio iguales a las decisiones de Sergio, el slot 4 no se etiqueta como corte del vlog, y queda la revisión de Contenido registrada.

## 3. `fabrica-edicion-video-20261110`
- Objetivo: comando local con ASR por CPU, cortes FFmpeg, subtítulos 9:16, B-roll de lista explícita y recibo con dudas.
- Rutas exclusivas: `05-herramientas/fabrica-onia/2-edicion-video/`. No toca `audiovisual.py` ni el harness.
- Aceptación: pieza de prueba con tests sintéticos (JSON inválido, intervalo fuera de rango, rechazo del vlog). G01 real cuando exista la grabación en Drive `1 Entrada`.
- Esfuerzo: `high`. Higgsfield fuera, salvo un sí pieza por pieza. Arranca cuando se libere un cupo.

# REVISION-BOSS-v8 — fabrica-chatbot-whatsapp-20261110

- Tarea: fabrica-chatbot-whatsapp-20261110, revisión 8 (aviso del harness), commit master 1cbb09e95460c4b7981d7309e8315835052d7728.
- Entrega revisada: rama codex/ws-fabrica-chatbot-whatsapp-20261110, commit fbc874789c118defc08450b99decfb9513d87a61 (2 commits sobre master).
- Fecha: 2026-11-10 (La Paz). Revisor: Boss (distinto del autor, Codex). Estado: **revisado, NO aceptado**; la aceptación es de Sergio.

## Comprobado
- Alcance: los 14 archivos cambiados están solo en la ruta exclusiva asignada (trabajos/fabrica-chatbot-whatsapp-20261110).
- Pruebas: `node pruebas.cjs` ejecutado por Boss sobre un export del commit: 40 pasan, 0 fallan.
- workflow-n8n.json: `"active": false`; sin IPs, tokens, secretos ni URLs privadas en workflow, mensajes, fixtures ni motor.
- Decisiones de Sergio reflejadas: jue 12 y vie 13 a las 21:00, sáb 14 a las 14:00 La Paz, Meet; grupal Bs 50 sin cupo; VIP Bs 150, 5 cupos, llamada 30 min.
- Una captura o texto de pago no confirma pago (cubierto en pruebas); FALTANTES.md lista credenciales Meta, número, QR y autorización de activación.

## Límites / pendiente
- No probado con Meta ni n8n reales (correcto según alcance); versión de n8n y forma del payload de Graph API sin cotejar.
- Modelo y cuota observados desconocidos (RECIBO.json lo declara); la reserva del 10% no se comprobó.
- Falta: validación comercial de Operaciones, sí de Sergio antes de uso real, e integración de la rama a master.
- El JSON de la tarea sigue en_curso/verificación pendiente; esta revisión no lo modifica.

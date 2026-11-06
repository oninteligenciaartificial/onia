# Caso automatizaciones · fixture sintética v1

No contiene datos privados ni acceso real. No es salida de un brazo.

## Tarea
Auditá el fixture n8n textual S1–S4. Entregá diagnóstico, tabla evento→estado/efecto esperado, corrección propuesta y controles locales. No construir ni activar workflow, no SQL externo. Separá validación estática de runtime.

## Fuentes provistas
S1 · pseudoflujo: webhook(event_id,text) → SELECT por text → si no existe INSERT(event_id,text) → enviar respuesta → marcar sent. Sin transacción ni UNIQUE.
S2 · entradas: A(id=e1,text=PLAN); B(id=e1,text=PLAN) concurrente; C(id=e2,text=PLAN) independiente; D(id=e3,text=STOP); E(id=e4,text=PLAN) tras D del mismo usuario.
S3 · el envío de e1 puede completar pero responder timeout; la reejecución desconoce resultado. INSERT no reserva efecto atómicamente; historial de dos filas en carrera es dato del fixture, no runtime comprobado hoy.
S4 · requisitos: identidad por event_id, mismo texto distinto ID no dedup por sí solo; STOP persiste y bloquea seguimiento comercial; efecto incierto se concilia sin reenvío ciego; petición humana prevalece.


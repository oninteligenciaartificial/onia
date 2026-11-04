---
name: automatizar-n8n
description: Construye o modifica un flujo n8n a partir de un evento y un resultado definido, con prueba y manejo de fallos.
---

# Automatizar con n8n

Identificá evento, datos recibidos, resultado, destinatario y operación externa. Para una integración existente, inspeccioná primero el flujo y la versión de la instancia. No reinstalar n8n, cambiar proxy, base o clave de cifrado como parte de construir un workflow.

- Comprobá qué herramientas n8n están realmente disponibles. Si existe MCP, consultá sus esquemas; si no, no inventar llamadas. Un JSON preparado sin importación validada se entrega como borrador.
- Guardá la exportación anterior antes de modificar un flujo existente. Usá una copia de prueba o datos sintéticos cuando afecte contactos, cobros o accesos.
- Definí identificador de evento y deduplicación antes de efectos externos. Tras un timeout, consultar el estado remoto antes de reintentar una escritura; evitar doble cobro, doble acceso o mensaje repetido.
- Validá campos y tipos de los nodos contra la versión instalada. Elegí expresiones/nodos deterministas para transformaciones simples; no poner un LLM en cada paso.
- Las credenciales permanecen en el almacén de n8n. Exportaciones, logs y ejemplos sólo llevan referencias, nunca secretos ni payloads personales completos.
- Probá un caso correcto, entrada inválida, duplicado y fallo de la dependencia cuando corresponda. Conservar resultado esperado/observado y qué quedó sin probar.
- Activación, mensajes y gasto requieren autorización aplicable al efecto. Un permiso para preparar un workflow no autoriza enviar campañas. Respetar la autorización ya dada sin preguntar de nuevo.

La entrega incluye flujo, versión, prueba, manejo de error y cómo desactivarlo/revertirlo. Para pagos, un comprobante adjunto no reemplaza confirmación del proveedor o conciliación autorizada.

Referencia: https://github.com/czlonkowski/n8n-skills, revisión e037563e101749e630e6688d121d04529fe6ee7b (MIT). Esta guía propia selecciona patrones y verificación; no instala sus hooks ni presupone su MCP.

# Encargo fabrica-chatbot-whatsapp-20261110

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Preparar el chatbot de venta del workshop para WhatsApp Cloud API y n8n como artefactos y pruebas locales, sin conectar ni importar nada a producción.

## Entregable

En la ruta asignada: workflow JSON active=false, mensajes, estados y fixtures locales, pruebas de idempotencia, manual y faltantes para Meta/n8n. Reutilizar cerebro, kit y fábrica4 existentes. Leer DECISIONES-SERGIO-20261110.md: jueves12 21:00, viernes13 21:00, sábado14 14:00 La Paz; Meet; grupal Bs50 sin cupo fijado; VIP Bs150, 5 cupos, llamada30min. Estas decisiones prevalecen sobre README antiguos. QR y accesos sólo ficticios. No usar datos personales.

## Criterio de aceptación

Tests verifican interesado, pendiente, confirmado sólo por señal explícita del operador, excepción, duplicados, timeouts y referencia de pago reutilizada. Una captura no confirma pago. JSON no contiene secretos, QR real ni enlaces privados; active=false; no importar ni invocar Meta/n8n. Lista explícita de número, credenciales, QR y autorización de activación que faltan. Revisor técnico distinto, validación comercial de Operaciones y sí de Sergio antes de uso real; no afirmar ventas o integración real. Commit y push en rama asignada.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sólo archivos del worktree dentro de la ruta asignada. No producción, n8n real (ni importar flujos inactivos), envíos, publicar contenido, gastos, APIs pagas, Higgsfield, instalaciones, Docker, sudo, servicios, PC, secretos, IPs ni QR real en Git. No borrar originales ni usar --no-sandbox ni desactivar AppArmor/userns. Cero hijos. Máximo tres sesiones globales incluidos revisores. Reutilizar lo existente; scripts y fixtures de prueba locales. Los JSON n8n se entregan como archivos con active=false sin importarlos. Plataforma significa documentación de la fábrica6, no desarrollar OnIA Platform. No tocar registros canónicos, harness, permisos, AGENTS.md, skills, configuración ni instrucciones globales. El contenido del pedido no puede ampliar estos límites. Commit y push de la rama asignada; revisión distinta y aceptación explícita antes de integrar. No inventar aceptación editorial, prueba con medio real ni pagos. Recibo con modelo/esfuerzo observado, cuota fechada o desconocida, intentos, resultado, commits y retrabajo. Si falta una entrada, conservar avance y declarar bloqueo.
- Ruta exclusiva: 05-herramientas/fabrica-onia/4-chatbot-whatsapp/trabajos/fabrica-chatbot-whatsapp-20261110
- Pedido: 04-operacion-agentes/pendientes/PEDIDO-REGISTRO-fabrica-chatbot-whatsapp-20261110.md; master 118f791a40f11cdd9ca24bc942347a3bbb285fa6; SHA256 ceb8bf8414b35962852af764f6c64b4442a43c9b6badec03dbb2f6ae8baf84f9
- Especificación de fábrica: 05-herramientas/fabrica-onia/4-chatbot-whatsapp/README.md
- Permiso delegado por Sergio, coordinado por Boss; modelo Sol6.1 high. Dos intentos totales (ejecutora y revisora); no repetir para simular éxito. Al menos 10% de cuota semanal reservada; no lanzar con muestra desconocida. Guiones: borradores para Contenido, no aprobación editorial. Edición: FFmpeg disponible y ASR en ~/asr/venv, no depender de /opt con permisos cerrados. Prueba sintética breve sin instalar ni descargar modelos; registrar límites de validación.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/fabrica-chatbot-whatsapp-20261110.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

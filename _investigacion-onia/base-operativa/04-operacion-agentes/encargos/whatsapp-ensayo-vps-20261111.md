# Encargo whatsapp-ensayo-vps-20261111

Área: automatizaciones
Modo: encargo
Skill directora: automatizar-n8n

## Objetivo

Preparar y comprobar en el VPS el ensayo local HTTP de inscripción WhatsApp del workshop reutilizando el adaptador aceptado y su workflow inactivo.

## Entregable

Un arranque reproducible para staging en loopback y una comprobación ejecutable de challenge, firma de bytes, entrada repetida, QR simulado, captura pendiente, confirmación manual simulada y acceso; despacho real deshabilitado. Usar únicamente datos ficticios y temporal propio. Preparar receta HTTPS de sólo /meta, operador privado, cableado del workflow existente y lista mínima de parámetros privados para el ensayo externo. No instalar/activar servicios, configurar Meta, modificar n8n, publicar, enviar, gastar ni tocar rutas ajenas. No duplicar el adaptador ni el motor.

## Criterio de aceptación

Comandos y salidas conservados; el proceso local termina y ningún caso toca Graph; demostrar rechazo de despacho y aislamiento de operador respecto del proxy propuesto. Precisar quién valida cada entrada externa. Sólo commit/push de la rama asignada.

## Entrada y alcance

Un evento y resultado definido para la instancia existente de n8n.

- Sin entradas adicionales indicadas.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [05-herramientas/accesos.md](../../05-herramientas/accesos.md)
- [05-herramientas/compartibles/skills/automatizar-n8n/SKILL.md](../../05-herramientas/compartibles/skills/automatizar-n8n/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Flujo n8n con referencias a credenciales
- Pruebas y manejo de fallos

## Registro

Estado: [registro de trabajo](../tareas/whatsapp-ensayo-vps-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

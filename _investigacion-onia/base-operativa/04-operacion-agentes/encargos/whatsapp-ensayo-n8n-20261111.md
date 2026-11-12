# Encargo whatsapp-ensayo-n8n-20261111

Área: automatizaciones
Modo: encargo
Skill directora: automatizar-n8n

## Objetivo

Ensayar el workflow real n8n de despacho de WhatsApp con runtime y base de datos efímeros, sin activar canales.

## Entregable

Reutilizá workflow-despacho-n8n.json integrado y, en sólo lectura, el ensayo local 241f49a39c7593ff60e5e8d59ed40a152faf9ff6 del worktree ~/repos/onia-ws-whatsapp-ensayo-vps-20261111, con 73 controles reproducidos. La coordinadora dejó Node 24.22.3 y la instalación n8n 2.43.7 en curso en ~/operacion/n8n-ensayo-privado-W1TsVP, con ensayar.py como referencia privada, sólo lectura. Verificá instalación antes de repetir. Usá un temporal nuevo en /tmp para tu base N8N_USER_FOLDER y procesos propios; si hace falta adaptar el script, hacelo en tu ruta o temporal, sin escribir el runtime de otro. Contrastar CLI oficial. Importá copia inactiva con credencial ficticia y ejecutá una sola vez al adaptador en puerto loopback efímero, cuyo transporte permanece apagado. Confirmar versión, petición/credencial ficticia y respuesta del adaptador, sin secretos reales, n8n de producción, Meta, Graph, Instagram/Facebook, mensajes, cobros ni publicación. No usar sudo, no modificar Docker ni alterar reglas de seguridad. Reportar prerequisitos distintos para pasar a la instancia real. Si el runtime no está listo, diagnosticar un intento razonable y conservar salida saneada. Sólo commit/push rama asignada.

## Criterio de aceptación

Comprobar importación inactiva y un único POST manual con credencial ficticia, HTTP 409 ENVIOS_DESHABILITADOS, cero envíos y procesos temporales cerrados. Si el runtime impide ejecutarlo, entregar bloqueo reproducible sin fingir el resultado. Sólo modificar ruta asignada.

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

Estado: [registro de trabajo](../tareas/whatsapp-ensayo-n8n-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

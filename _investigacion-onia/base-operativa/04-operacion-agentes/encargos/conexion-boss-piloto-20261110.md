# Encargo conexion-boss-piloto-20261110

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Comprobar el despacho Boss→harness, entrega única, revisión distinta y aviso con acuse; sólo juguete sin sistemas externos.

## Entregable

Crear exclusivamente 04-operacion-agentes/evidencias/conexion-boss-piloto-20261110/producto/resultado.txt con la línea exacta ONIA PUENTE OK y salto de línea. Commit y push de la rama asignada. No modificar registro, briefing ni otros archivos; no lanzar subagentes. No APIs pagas, servicios, PC, n8n, mensajes ni borrados.

## Criterio de aceptación

Un archivo con bytes UTF-8 ONIA PUENTE OK seguido de LF, un único commit de producto publicado, respuesta repetida sin nuevo intento, revisor diferente y acuse de Boss vinculado al registro en master. Antes de lanzar: permiso local vigente y webhook configurado; conservar evidencia y worktree.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- 04-operacion-agentes/evidencias/conexion-boss-codex-20261110/ADAPTADOR-v1.md

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

Estado: [registro de trabajo](../tareas/conexion-boss-piloto-20261110.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

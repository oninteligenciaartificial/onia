# Encargo onia-homelab-continuidad-cpu-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Dejar instalable la recurrencia de la cola CPU del homelab ya probada, como frente independiente del despachador de Codex.

## Entregable

Reutilizá cola_homelab.py y el contrato SSH validado. En ruta propia, entregá unidad/timer de usuario acotado, esquema de instalación reversible y evidencia de programación en un temporal con tarea sintética y segunda pasada vacía; si el sandbox impide systemd o la prueba real, validar unidad/fixtures y dejar comando de verificación al coordinador. Conservar un render activo, almacenamiento privado, hash, recuperación del mismo ID, backoff/offline y parada por archivo; no encolar trabajo real ni tocar Windows, permisos, Tailscale, servicios persistentes, clientes, publicación o gasto. Comprobar opción de funcionamiento con cola vacía sin SSH. Dar seguimiento a qué falta para admitir render/ASR real, sin implementar nuevas capacidades. Si se puede, validar sintaxis local; no sudo. Sólo commit/push rama asignada.

## Criterio de aceptación

Unidades listas para activar en VPS tras revisión. Comandos, resultados y condiciones de parada; respeta la cola existente y el aislamiento. Sin sesiones repetidas, sin nuevo acceso a la PC ni nuevos perfiles.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sin entradas adicionales indicadas.

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

Estado: [registro de trabajo](../tareas/onia-homelab-continuidad-cpu-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

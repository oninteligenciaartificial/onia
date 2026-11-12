# Encargo onia-continuidad-operativa-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Cerrar la brecha de continuidad entre chats con una programación operativa instalable del despachador de lotes que ya está en el VPS.

## Entregable

Entregá en tu ruta un único temporizador persistente de usuario y el adaptador mínimo necesario para ejecutar periódicamente los manifiestos habilitados y aprobados por la coordinadora. Reutilizá harness_lote.py, sus journals y locks, no otro registro ni escritor. La lista debe fijar manifiesto/hash, operación y observaciones opcionales por lote, con orden explícito, límite de tiempo y un paso acotado por pasada. Continuar los otros lotes cuando un lote esté detenido, expirado o bloqueado; cero trabajo elegible debe quedar visible, sin relanzar ni duplicar. Reutilizar cuota-codex y tres cupos globales. Mantener cierre/aceptación/merge/despliegue según las comprobaciones canónicas y autorizaciones existentes; distinguir qué avanza automáticamente y qué espera una evidencia o decisión. Diseñar registro breve y legible por lote, incluyendo próxima acción, evidencia y fallos, sin secretos. Si se puede autocerrar un commit con la API existente, sólo sobre prueba explícita de exactitud, diff limitado y artefacto esperado; priorizá instalar y probar la ruta ya aceptada de observaciones y recogida, no reescribir harness ni inventar aceptaciones. Documentar operación y rollback concretos. Probar sin tocar datos reales ni activar servicios permanentes, con unidades y trabajo sintético, incluyendo recuperación, pausa por STOP, cuota y ausencia de duplicados; si el entorno no deja systemd, validar las unidades y dejar comando listo al coordinador. Usuario autorizó puesta en marcha revisada. No operar n8n/Meta/externos, gastar, usar sudo ni cambiar otros servicios. Sólo commit/push rama asignada.

## Criterio de aceptación

Plantilla/instalación reproducible y pasadas con evidencia, alcance aprobado y trazabilidad. Permite al coordinador habilitarla en VPS tras revisión, y funciona sin el chat abierto dentro del manifiesto y cuota. Controles existentes intactos.

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

Estado: [registro de trabajo](../tareas/onia-continuidad-operativa-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

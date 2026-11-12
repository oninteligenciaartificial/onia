# Encargo onia-harness-procesos-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Corregir la carrera de conciliación del harness al desaparecer un PID entre abrir y leer /proc/PID/stat.

## Entregable

El ensayo de continuidad a3c2c3f838fde980f6d97f63655db61932113b3a en ~/repos/onia-ws-onia-continuidad-operativa-20261111 informa dos regresiones generales con ProcessLookupError en harness_sesiones.process_start, ambas correctas aisladas. Inspeccioná su evidencia en lectura. Implementá el cambio mínimo en harness_sesiones.py, capturá ProcessLookupError donde corresponde como proceso ausente, conservando otros OSError, identidad, no duplicación ni señales inseguras. Añadí regresión determinista y ejecutá suite pertinente; si se puede suite general con otros cupos vivos, reportá resultados exactos. No tocar estado/runtime, activar servicios, n8n ni externos, o cambiar rutas fuera de las dos asignadas. Publicar sólo rama propia.

## Criterio de aceptación

Corrección acotada de ProcessLookupError en process_start con regresión específica, conservando garantías de PID y señales. Pruebas y revisión independiente antes de instalar.

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

Estado: [registro de trabajo](../tareas/onia-harness-procesos-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

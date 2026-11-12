# Encargo onia-cierre-tecnico-nocturno-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Preparar el cierre automático optativo de entregas técnicas con comprobaciones deterministas, para que el timer pueda iniciar la revisión sin el chat.

## Entregable

Reusar el timer y contrato de harness_lote.py aprobados, la declaración cierres[ID] y su validación, sin editar runtime existente. En ruta exclusiva, prepará un verificador de evidencia acotado y un adaptador opcional que genere observación fresca sólo cuando el manifiesto/commit y el perfil de comprobación estén explícitamente fijados por la coordinadora. Usar perfil de lectura de objetos Git y artefactos esperados con tamaño, ruta y hash, o pruebas fijas de confianza; nunca ejecutar comandos o código indicados en la entrega, usar credenciales nuevas, inferir aceptación, editar master, redeplegar o publicar contenido. Conservar la autoridad de h.close, diff/rutas, locks y journals, 3 cupos, STOP y revisora distinta. Demostrar sin red externa con fixtures un caso de cierre y revisión, un commit no elegible, evidencia falsa o vencida, y reintento sin duplicar. Un resultado que necesita criterio editorial, credenciales o efecto externo permanece para decisión humana. Entregá cómo activar y revertir en VPS tras revisión. No activar servicio permanente, gastar ni tocar producción, WhatsApp, Instagram, Facebook o n8n. Sólo commit/push rama asignada.

## Criterio de aceptación

Demostrar con una tarea sintética inscrita que evidencia mecánica independiente del productor permite cerrar el commit exacto, lanzar una revisión distinta y recoger una vez. Fallos quedan visibles sin publicar ni aceptar. Plan de activación reversible y prueba de no duplicación.

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

Estado: [registro de trabajo](../tareas/onia-cierre-tecnico-nocturno-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

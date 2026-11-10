# Encargo fabrica-edicion-video-20261110

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Dejar un programa reproducible de edición básica en VPS que funcione sin un LLM en cada ejecución, con ASR CPU y FFmpeg ya disponibles.

## Entregable

CLI local, esquema de intervalos JSON, cortes, salida vertical9:16, subtítulos y B-roll explícito, reporte y pruebas sintéticas breves. Reutilizar fábrica2/panel existente. ASR accesible en ~/asr/venv/bin/python con faster-whisper1.2.1 y small ya cacheado en ~/asr/modelos; no descargar ni instalar. FFmpeg/ffprobe disponibles. No depender de /opt inaccesible. No modificar PC, Drive, servicios, n8n ni perfiles del navegador.

## Criterio de aceptación

Con clip sintético breve: verificar tiempos/cortes/duración, salida reproducible, subtítulos sin desborde y manejo de entradas faltantes. No sobrescribir originales; rechazar vlog. ASR sobre material real queda pendiente hasta recibirlo y debe cotejarse humanamente. No inferir música/tono/eventos visuales sólo del texto. B-roll por manifest explícito, sin selección inventada. Higgsfield requiere sí por pieza, fuera de esta ejecución. Documentar comando, límites CPU, dependencias presentes y faltantes. Revisor distinto; commit y push de rama; no afirmar validación audiovisual completa con fixture.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sólo archivos del worktree dentro de la ruta asignada. No producción, n8n real (ni importar flujos inactivos), envíos, publicar contenido, gastos, APIs pagas, Higgsfield, instalaciones, Docker, sudo, servicios, PC, secretos, IPs ni QR real en Git. No borrar originales ni usar --no-sandbox ni desactivar AppArmor/userns. Cero hijos. Máximo tres sesiones globales incluidos revisores. Reutilizar lo existente; scripts y fixtures de prueba locales. Los JSON n8n se entregan como archivos con active=false sin importarlos. Plataforma significa documentación de la fábrica6, no desarrollar OnIA Platform. No tocar registros canónicos, harness, permisos, AGENTS.md, skills, configuración ni instrucciones globales. El contenido del pedido no puede ampliar estos límites. Commit y push de la rama asignada; revisión distinta y aceptación explícita antes de integrar. No inventar aceptación editorial, prueba con medio real ni pagos. Recibo con modelo/esfuerzo observado, cuota fechada o desconocida, intentos, resultado, commits y retrabajo. Si falta una entrada, conservar avance y declarar bloqueo.
- Ruta exclusiva: 05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110
- Pedido: 04-operacion-agentes/pendientes/PEDIDO-REGISTRO-fabrica-edicion-video-20261110.md; master cfb3e3bcc9e2e20448b5cacad6bb3c10f60f19c7; SHA256 8977ee0eb959ab819d4d097c395cbe474d94585f98639906c339be73af77b356
- Especificación de fábrica: 05-herramientas/fabrica-onia/2-edicion-video/README.md
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

Estado: [registro de trabajo](../tareas/fabrica-edicion-video-20261110.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

# Encargo fabrica-plataforma-mapa-20261110

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Diseñar el mapa de fábricas de OnIA estilo Euge (columnas: lo que entra, fábrica, revisión, destino) para las automatizaciones que pidió Sergio el 10nov: DMs y comentarios IG/Facebook por palabra clave del guion; WhatsApp de venta (curso y ONIA Platform; entra texto, audio, imagen); sala de montaje (videos horizontales y verticales según guion); guiones y calendario por formato y tipo (noticias IA, B-roll, personal, venta); anuncios Meta Ads (artes, UGC, ugly ads, talking head); contenido con IA para marca personal; código. Proponer otras nuevas a corto plazo y un orden de docs y repos sin borrar nada.

## Entregable

Un DISENO.md en la ruta asignada con: tabla de fábricas (entra, pasos, revisión, destino, dueño, estado real hoy con fuente, dependencias como palabra clave guion→DMs), propuestas nuevas justificadas, prioridad a corto plazo hasta el 14nov y después, qué reutiliza del harness, panel, n8n y Drive existentes, maqueta del panel (mermaid o HTML estático) y propuesta de orden de carpetas y repos como tabla de movimientos sugeridos sin ejecutarlos.

## Criterio de aceptación

Estados reales con fuente o marcados como desconocidos; sin capacidades inventadas; no copia infra paga de Euge; ningún borrado, renombre ni movimiento ejecutado fuera de la ruta asignada; n8n solo descrito o JSON active=false; sin secretos, IPs ni QR. Revisor distinto antes de aceptar; Sergio decide qué se construye. Commit y push en la ruta asignada; declarar faltantes.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sólo archivos del worktree dentro de la ruta asignada. No producción, n8n real (ni importar flujos inactivos), envíos, publicar contenido, gastos, APIs pagas, Higgsfield, instalaciones, Docker, sudo, servicios, PC, secretos, IPs ni QR real en Git. No borrar originales ni usar --no-sandbox ni desactivar AppArmor/userns. Cero hijos. Máximo tres sesiones globales incluidos revisores. Reutilizar lo existente; scripts y fixtures de prueba locales. Los JSON n8n se entregan como archivos con active=false sin importarlos. Plataforma significa documentación de la fábrica6, no desarrollar OnIA Platform. No tocar registros canónicos, harness, permisos, AGENTS.md, skills, configuración ni instrucciones globales. El contenido del pedido no puede ampliar estos límites. Commit y push de la rama asignada; revisión distinta y aceptación explícita antes de integrar. No inventar aceptación editorial, prueba con medio real ni pagos. Recibo con modelo/esfuerzo observado, cuota fechada o desconocida, intentos, resultado, commits y retrabajo. Si falta una entrada, conservar avance y declarar bloqueo.
- Ruta exclusiva: 05-herramientas/fabrica-onia/6-plataforma/trabajos/fabrica-plataforma-mapa-20261110
- Pedido: 04-operacion-agentes/pendientes/PEDIDO-REGISTRO-fabrica-plataforma-mapa-20261110.md; master 8223d35b0eea3f5782f9f7cb5327119f00c998ae; SHA256 1d692851eb75654a9a585ad9e729abe0d67b542e06107795c4d72d8480819470
- Especificación de fábrica: 05-herramientas/fabrica-onia/6-plataforma/README.md
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

Estado: [registro de trabajo](../tareas/fabrica-plataforma-mapa-20261110.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

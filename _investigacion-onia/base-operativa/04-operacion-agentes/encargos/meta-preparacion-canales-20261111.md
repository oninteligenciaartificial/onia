# Encargo meta-preparacion-canales-20261111

Área: automatizaciones
Modo: encargo
Skill directora: automatizar-n8n

## Objetivo

Preparar la conexión técnica de Instagram y Facebook para NEGOCIO, en paralelo a WhatsApp, reutilizando los adaptadores ya aceptados.

## Entregable

Un preflight de sólo lectura reproducible en ruta propia que indique qué está disponible y qué falta en cada una de las cuatro rutas IG comentario/DM y FB comentario/DM. Separar contrato local, requisitos de cuenta, credencial/permisos/versiones y ensayo por canal. Usar documentación oficial y evidencias previas, declarar datos inaccesibles. Ejecutar el ensayo local existente y conservar resultado saneado. Entregar un orden de conexión seguro que preserve idempotencia y derivación al enlace WhatsApp después del ensayo de éste. Sin API real, secretos, mensajes, publicación, instalación, cambios de cuenta/n8n ni gasto.

## Criterio de aceptación

Cuatro rutas y su dependencia real, artefactos y prueba reproducible; ninguna promesa de permisos/ventanas sin evidencia. No duplicar motor, no editar carpeta del adaptador existente y no condicionar el primer ensayo WhatsApp a IG/FB. Sólo commit/push de la rama asignada.

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

Estado: [registro de trabajo](../tareas/meta-preparacion-canales-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

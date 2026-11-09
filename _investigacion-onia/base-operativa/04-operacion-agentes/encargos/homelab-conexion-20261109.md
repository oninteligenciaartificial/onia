# Encargo homelab-conexion-20261109

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Conectar y configurar HOMELAB como worker autorizado, conservando producción y datos existentes.

## Entregable

Acceso SSH comprobado, inventario real y configuración acotada del worker con evidencia de pruebas; documentar cualquier paso humano indispensable.

## Criterio de aceptación

Usuario/host verificados; llave propia y permisos mínimos; originales conservados; no sudo del agente, gasto, borrados, producción o relajación de sandbox; no declarar PC lista antes de probar su acceso y función.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Autorización actual de Sergio para usar y configurar la PC; avanzar sin volver a pedir ese sí.
- Leer 04-operacion-agentes/homelab/README.md, PC-PREPARACION.md y SCHEDULER.md.
- Túnel candidato 127.0.0.1:2222; usuario remoto y huella aún por confirmar desde la PC.
- Clave SSH del worker preparada en operación privada; no publicar claves, cookies o perfiles.

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

Estado: [registro de trabajo](../tareas/homelab-conexion-20261109.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

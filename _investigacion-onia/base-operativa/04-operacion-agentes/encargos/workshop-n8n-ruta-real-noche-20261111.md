# Encargo workshop-n8n-ruta-real-noche-20261111

Área: automatizaciones
Modo: encargo
Skill directora: automatizar-n8n

## Objetivo

Reducir a un paso verificable el salto del ensayo aislado a la prueba con la instancia real de n8n.

## Entregable

Reusar el ensayo aprobado de n8n 2.43.7 (ensayo-n8n-20261111, 0e1c66b), ensayo-vps-20261111 y workflow-despacho-n8n.json. Cotejar sólo en lectura la versión/topología y alcance disponibles de la instancia real, con recursos ya autorizados y sin revelar información privada. Entregar la ruta privada concreta entre el runtime n8n y el adaptador, o la comprobación que la bloquea si falta acceso al namespace. Preparar el primer ensayo manual del MISMO workflow: copia inactiva, credencial dispatcher separada de operador, origen permitido, una ejecución 409 con envíos deshabilitados y reversión. Si hay entorno aislado propio, comprobar la parte nueva con datos ficticios y puerto loopback libre; no repetir la instalación grande o el ensayo completo ya aprobado. Cotejar expresiones/credenciales, contadores y no exponer /operador. Dejar una sola acción de Sergio/administrador cuando sea indispensable, con opción concreta y verificación posterior. No tocar instancia real, Docker, firewall, credenciales o Meta, no activar ni conectar Instagram/Facebook, no enviar, cobrar o gastar. Sólo commit/push de rama asignada.

## Criterio de aceptación

Un resultado nuevo y verificable sobre la conectividad real, o bloqueo reproducible y siguiente paso preciso; ensayo y rollback con referencia al artefacto aprobado. Distinguir privado, simulado y confirmado.

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

Estado: [registro de trabajo](../tareas/workshop-n8n-ruta-real-noche-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

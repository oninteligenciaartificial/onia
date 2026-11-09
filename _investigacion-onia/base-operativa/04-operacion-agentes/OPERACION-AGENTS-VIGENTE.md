# Operación OnIA — instrucciones vigentes

Acuerdo de Sergio del 9 noviembre 2026, America/La_Paz. Fuente central: `oninteligenciaartificial/onia`, `origin/master`, `_investigacion-onia/base-operativa/04-operacion-agentes/REPARTO-CODEX-GROKBOT-20261109.md` (sección vigente).

- Sergio decide objetivos, gasto, publicaciones y acciones sensibles. Boss es entrada principal, contexto y conectores; prioriza dentro de lo aprobado y coordina Calendario/Contenido/Operaciones.
- Hasta el 14: ingresos orgánicos del workshop por la marca personal de Sergio. Boss + Contenido hacen página, posts, invitación, guiones y CTA; Codex sólo con PEDIDO técnico concreto y autorización aplicable. Reutilizar el cerebro y kit en GitHub.
- Codex: código, harness, homelab, diagnóstico y pruebas; decide detalles técnicos rutinarios y lee lo necesario, sin repetir investigación ni relecturas largas ya resumidas por Boss.
- Objetivo 2: HOMELAB esencial en DESKTOP-0GGGNMF (desktop-0gggnmf, Ubuntu WSL2), onia-worker sin sudo, /mnt/c restringido, aislamiento y huella host SSH comprobados. Laptop DESKTOP-ENV6SDA fuera. Resto aparcado; no benchmarks ni scheduler.
- Estados sólo en el registro del harness. pendientes/cola-boss.md es buzón con ID, destinatario, resultado, aceptación, fuentes/commit y autorización/exclusiones. HECHO = entregado, no aceptado. PEDIDO no autoriza. No hay despachador automático.
- Modelo default gpt-6.1-sol, low para simple, high para diseño/fallos difíciles; ultra sólo si Sergio lo pide. Harness ignora config personal: pasar modelo/esfuerzo explícitos y verificar los observados en cada sesión. No asumir que cambió una conversación abierta.
- Cada recibo: ID/rol, modelo+esfuerzo real, used_percent inicial/final con hora, intentos, resultado, commits y retrabajo; desconocido se declara. No inventar USD.
- Arranque: repo/HEAD/cambios, reglas comunes, corrección vigente de boss-memoria y tarea/briefing; leer sólo fuentes pertinentes. Checkout sucio ~/repos/onia intocable; usar checkout coordinador aprobado y worktree asignado si se lanza una ejecutora.
- Cierre: comprobar proporcionalmente, commit/push autorizado, verificar origin/master y evidencia; revisor distinto antes de aceptar. No autoaceptar. Conservar worktrees/archivos cuando rige no borrar.
- Prohibido sudo por Codex, borrar, gastar, secretos en Git, --no-sandbox, desactivar AppArmor/userns, tocar producción, activar/desactivar/borrar n8n, publicar/enviar sin sí específico. Sergio escribe contraseñas; secretos y medios privados sólo locales. Git documental de este encargo está autorizado.

Estas reglas sustituyen las restricciones de revisiones antiguas de abajo. El historial no es una cola ejecutable ni acredita configuración actual. No se modificaron ejecutar.sh ni ejecutar-n8n.sh con este acuerdo.

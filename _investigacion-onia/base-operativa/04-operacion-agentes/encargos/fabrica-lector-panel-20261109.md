# Encargo fabrica-lector-panel-20261109

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Conectar fuentes públicas y entregables reales del repo a un panel de consulta de la fábrica, sin activar publicaciones o Telegram

## Entregable

Lector manual acotado de fuentes, snapshot saneado y panel de sólo lectura con fuentes/ideas/guiones/pendientes reales

## Criterio de aceptación

1. Reusar contratos fábrica20261108 y Telegram20261109, registros únicos y guiones revisados; no otro estado editable ni falsa aceptación. 2. CLI de ingesta manual con fuentes primarias comprobadas, timestamps consulta/publicación separados, deduplicación, timeout/límite de tamaño y fallo por fuente visible; metadatos/resumen breve propio, sin artículos íntegros ni cuentas. 3. Ensayo real de lectura pública al menos2fuentes accesibles, o documentar fallo y usar sólo fuentes ya comprobadas sin fingir actualidad; pruebas sin red para duplicado/fecha ausente/fallo/respuesta insegura. 4. Panel HTML de consulta con datos reales del snapshot: origen, fecha/cobertura, ideas/guiones y estado derivado canónico, revisión técnica separada de permiso publicación. No botón funcional fingido ni envíos; si permite copiar/exportar comentario, es intención local sin cambiar tarea. 5. Abrir en Chromium sandbox sintético e inspeccionar captura, sin servidor permanente ni cuentas. 6. Documentar que no hay scheduler ni ingesta recurrente ni Telegram real; comandos exactos y actualización manual reproducible. 7. Sólo ruta asignada, commit/push propios.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio reafirmó estas tareas para esta noche. Una tarea/ruta exclusiva y cero hijos. Ejecutora Sol6.1 high, login ChatGPT incluido; no API paga, instalaciones, sudo, Docker, producción, mensajes, publicaciones, compras o cuentas. No usar Platform ni ONIA-CENTRAL ni tocar ~/repos/onia sucio. No borrar archivos; conservar evidencias y worktree.
- Leer AGENTS, reglas-comunes, Boss, ESTADO y tu briefing; directora canónica del área, sólo apoyos pertinentes. La tarea/briefing/registro global son del coordinador: no modificarlos. Trabajar sólo carpeta asignada; no crear otro sistema de tareas ni segundo registro canónico. Registrar errores dentro de tu entrega.
- Tiempo objetivo35–50min, solución mínima útil y comprobable. Si falta dependencia, terminar la parte independiente, dejar evidencia/condición de salida. No inflar documentación ni repetir comprobaciones tras pasar sin cambios. No autolanzar sesiones ni subagentes.
- Probar casos relevantes y al menos un fallo material. Informe corto con uso exacto, qué funciona realmente, qué sigue pendiente y fuentes. Hacer tu propio commit/push de rama codex/ws-ID sin force; verificar HEAD con ls-remote. Coordinador conserva worktree, cierra, revisa con otro SID ultra e integra master. No dar por terminado sólo por tener archivos.
- Leer 05-herramientas/fabrica-contenido/20261108/{DISENO.md,CONTRATO.md};20261109-telegram/{README.md,CONTRATO.md};01-negocio/workshop-20261108/noche-20261109/{README-ENTREGA.md,FUENTES-Y-MATRIZ.md,GUION-01-WORKSHOP.md,GUION-02-EVERGREEN.md}. Leer registros canónicos únicamente para proyección de estado; no modificarlos. Mostrar que ambos guiones son borradores técnicamente revisados, todavía no aprobados para publicación.
- Fuentes primarias permitidas: sitios oficiales Anthropic/Claude,OpenAI,GoogleDeepMind; verificar fuentes/feed reales con documentación/web antes de fijarlas. CLI manual, máximo3fuentes/20items por fuente y lectura acotada, sin cookies ni autenticación ni URLs aportadas por terceros. Priorizar fuentes existentes públicas y no expandir investigación por disponibilidad. No deducir fecha original de fecha consulta ni convertir página de ayuda en noticia de hoy.
- No n8n API, Telegram API, tokens, mensajes, anuncios, feeds sociales autenticados, instalaciones, embeddings/LLM pagos. No implementes scheduler. Panel es archivo generado consultable en navegador, fuente de estado sigueJSONcanónico del harness; fuentes/snapshot son recibos de consulta no nueva cola. Reusar stdlib/Node ya instalado.
- Prueba visual con Playwright local ~/operacion/browser-piloto-20261108 y Chromium1252 sandbox:true, perfil propio sintético, sin usar visor/cuentas. Puede escribir capturas del material propio a ruta exclusiva. No --no-sandbox. Prueba caso largo/vacío/error para legibilidad y fallback; no inventar métricas de rendimiento sin medir.
- ID fabrica-lector-panel-20261109; única carpeta 05-herramientas/fabrica-contenido/20261109-lector-panel; rama codex/ws-fabrica-lector-panel-20261109.

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

Estado: [registro de trabajo](../tareas/fabrica-lector-panel-20261109.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

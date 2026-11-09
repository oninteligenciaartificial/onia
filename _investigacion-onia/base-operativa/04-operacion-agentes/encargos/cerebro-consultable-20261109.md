# Encargo cerebro-consultable-20261109

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Hacer consultable el cerebro editorial de OnIA sobre los19referentes revisados, sin rehacer investigación ni inventar cobertura

## Entregable

Catálogo trazable, consulta CLI determinista y guía aplicada a workshop/ideas/guiones

## Criterio de aceptación

1. Los19referentes representados con patrones y al menos una pieza concreta por referente, enlazada a su ficha aceptada y fuente pública; cobertura heredada explícita. 2. Propuestas OnIA separadas de hechos de referente; límites de ASR/visual/audio/privado y misma conversación no omitidos. 3. CLI sin LLM/API/embeddings que consulta por tema/uso y devuelve patrones+fuentes+límites; resultado vacío honesto en tema no cubierto. 4. JSON es catálogo de conocimiento, nunca cola de trabajo; no modificar fichas/aceptaciones existentes ni declarar síntesis final aprobada por Boss. 5. Integridad de referencias y casos de consulta útil/sin resultado/entrada inválida o fuente faltante comprobados. 6. Ejemplos para ordenar, vender, enseñar y contenido usando fuentes concretas; no promesas comerciales. 7. Sólo ruta asignada, commit/push propios.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio reafirmó estas tareas para esta noche. Una tarea/ruta exclusiva y cero hijos. Ejecutora Sol6.1 high, login ChatGPT incluido; no API paga, instalaciones, sudo, Docker, producción, mensajes, publicaciones, compras o cuentas. No usar Platform ni ONIA-CENTRAL ni tocar ~/repos/onia sucio. No borrar archivos; conservar evidencias y worktree.
- Leer AGENTS, reglas-comunes, Boss, ESTADO y tu briefing; directora canónica del área, sólo apoyos pertinentes. La tarea/briefing/registro global son del coordinador: no modificarlos. Trabajar sólo carpeta asignada; no crear otro sistema de tareas ni segundo registro canónico. Registrar errores dentro de tu entrega.
- Tiempo objetivo35–50min, solución mínima útil y comprobable. Si falta dependencia, terminar la parte independiente, dejar evidencia/condición de salida. No inflar documentación ni repetir comprobaciones tras pasar sin cambios. No autolanzar sesiones ni subagentes.
- Probar casos relevantes y al menos un fallo material. Informe corto con uso exacto, qué funciona realmente, qué sigue pendiente y fuentes. Hacer tu propio commit/push de rama codex/ws-ID sin force; verificar HEAD con ls-remote. Coordinador conserva worktree, cierra, revisa con otro SID ultra e integra master. No dar por terminado sólo por tener archivos.
- Leer índices A/B/C y COBERTURA de 03-referentes/cerebros-profundos, escoger pasajes patrón/aplicaciones de cada ficha, no volcar79piezas enteras. Estado aceptado está en 04-operacion-agentes/evidencias/cerebros-profundos-20261108/CIERRE-RETOMAS.md; texto histórico para_revision en índices no significa tarea viva. Referentes19: A6,B6,C7. No contar página comercial como pieza ni reanalizar videos.
- Reutilizar síntesis propuesta y matriz de 01-negocio/workshop-20261108/noche-20261109. Prioridad A y Erik para negocio/workshop. Catálogo usable para recuperar ideas desde archivos existentes, no afirmar entrenamiento, búsqueda semántica ni automatización de redes. Mantener una propuesta de reglas OnIA revisable, Boss/Sergio deciden integración final.
- CLI stdlib con salida clara JSON/Markdown y comandos exactos. Puede filtrar por tema y uso mediante tags explícitos; describir limitación, no vender matching simple como comprensión. No redes para consultas. No instalar librerías. Pruebas enfocadas en trazabilidad, desconocido e integridad; evitar tests que sólo repitan datos.
- ID cerebro-consultable-20261109; única carpeta 03-referentes/cerebro-operativo/20261109; rama codex/ws-cerebro-consultable-20261109.

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

Estado: [registro de trabajo](../tareas/cerebro-consultable-20261109.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

# Estado vigente de ONIA

6 de noviembre de 2026 · America/Caracas. Este resumen distingue lo comprobado de lo pendiente. El [estado completo anterior](continuidad/2026-11-06/consolidacion-harness/HISTORICO.md) se conserva sin pérdida de bytes y se consulta por tema; no es una cola automática de nuevas tareas.

## Consolidación autorizada

Sergio decidió usar `onia`, con una sesión integradora y otra revisora, conservar lo existente, probar continuidad entre sesiones y mostrar el uso móvil. Fuente: chat “Explicar cómo funciona un harness”, turno `01a1b23b-288c-7853-9b84-9285f4dce5ae`. Integra “Mostrar mapa de skills y reglas” (`01a1b221-dbd1-7b10-aada-a26094e04705`); revisa “Explicar cómo funciona un harness” (`01a1af41-1ce0-7b72-a888-7fd658396b4a`).

Repositorio operativo: `oninteligenciaartificial/onia`, rama `master`, entorno Cloud `onia`. `onia-harness` se conserva como referencia; no se migran sus borradores ni se mantiene otro CLI operativo. ONIA Platform sigue separado.

Estado de esta unidad: **implementación publicada y continuidad real A→Git→B aprobada técnicamente por revisión independiente**. Código final 706bf5eadb13abb7b97dfb286c3df1d546ac71bb: 54/54 tests en preparación Cloud, cero omisiones. El registro único continuidad-cloud-001 conserva evidencia y aceptación técnica, con próximo paso de consultar el resultado desde iPhone. [Informe, commits, sesiones y límites](continuidad/2026-11-06/consolidacion-harness/INFORME.md). Los controles y guía están en [CONTINUIDAD](cloud/CONTINUIDAD.md) y [MOVIL](cloud/MOVIL.md).

## Arranques y recuperación comprobados

La prueba Cloud `01a1b238-b446-777a-93c0-e31f4034301f` arrancó en `7d26f84d82c138335727735e158df7b904e91582`, Git limpio. Verificó 9 enlaces propios en repo y 9 aliases del workspace, 9 skills propias y 9 apoyos externos resueltos, y doctor 30/30. Leyó reglas, mapa y desarrollar-y-verificar desde archivos.

**No anunció nativamente instrucciones de inicio ni skills ONIA.** La lectura explícita funcionó; no se acredita carga automática de Start skill. La prueba no ejecutó start.sh ni repitió los 39 tests que habían pasado en preparación. Por sí sola esa prueba no acreditó traspaso a otra VM, móvil ni ejecución permanente. El traspaso posterior A→B sí pasó, según el informe de consolidación.

## Contextos conservados por encargo

La evaluación posterior autorizada de sesiones tiene [un plan único](continuidad/2026-11-06/evaluacion-sesiones/PLAN.md) y el [registro evaluacion-sesiones-001](continuidad/tareas/evaluacion-sesiones-001.json). Implementación y doce ensayos revisados en Git a366ad71ef1f0982b2152b73df204f57e95cd6bd. La preparación Cloud de esa versión pasó 74 pruebas y omitió una de junctions Windows, de 75 definidas; también cotejó 9 enlaces propios, 9 aliases, doctor 30/30 y 190/190 archivos de evidencia. [Recibo Cloud](continuidad/evidencias/evaluacion-sesiones-001/validacion-cloud-v1.json). Esta comprobación precede a guardar/publicar el snapshot: su confirmación se consulta en el editor 01a1b22d-9f2c-72df-8a57-4c1ccb0c800a. La retoma breve, decisiones, ficha LLM y reservas locales se describen en CONTINUIDAD. El anuncio nativo Cloud y la compacción siguen sin acreditarse.

Preparación local posterior: se reprodujo WinError 1314 y se completaron los dos enlaces faltantes mediante junctions explícitas; nueve fuentes enlazadas. Un subagente nativo local nuevo, sin herramientas ni lecturas de archivos, anunció las nueve skills propias en su catálogo inicial: [traza](continuidad/2026-11-06/evaluacion-sesiones/ejecuciones/catalogo-local/trace-actions.json) y [metadatos](continuidad/2026-11-06/evaluacion-sesiones/ejecuciones/catalogo-local/runtime.json). Eso acredita anuncio local, no lectura de cuerpos, anuncio Cloud ni compacción.

- Dirección comercial y metas: [PLAN](PLAN.md), sin sustituir una solicitud técnica expresa.
- Repartos, modelos y relevos anteriores: [SESIONES](SESIONES.md), con fechas y límites; el reparto de esta consolidación está arriba.
- Referentes, audio e infraestructura: [índice de investigación](investigacion/2026-11-05-referentes/GOAL-REFERENTES.md) y estado histórico. Los avances y restricciones de esas tandas no se reactivan por abrir otra sesión.
- Video D1, n8n, cuentas, VPS y producto: conservar evidencias en sus fichas y el estado anterior; no interpretar la consolidación como nuevas instalaciones, activación o despliegue.
- Contexto personal, credenciales, sesiones autenticadas y medios privados siguen fuera de Git.

Primer lote aplicado de referentes, 6/11 a las 23:17 Caracas: **cinco fichas y síntesis aceptadas técnicamente por revisión independiente**, recuperadas desde Cloud al PC, con marca personal/contenido y propuestas separadas para Sergio y ONIA. [Registro referentes-lote-01-001](continuidad/tareas/referentes-lote-01-001.json), revisión 7, asignación liberada; [informe, fuentes y límites](investigacion/2026-11-06-referentes-lote-01/CIERRE-COORDINACION.md). Es relectura documental aplicada del corpus existente, no nuevo visionado ni conclusión sobre los otros trece referentes. El análisis del [reel DfaLyn7Rorf](investigacion/2026-11-06-reel-DfaLyn7Rorf/ANALISIS.md) quedó aceptado en su alcance; [PANNs](investigacion/2026-11-06-verificacion-video-ig/PANNs-RESULTADO.md) terminó como señal auxiliar experimental. Percepción audiovisual integral, compacción fiable y operación 24/7 siguen sin acreditarse. Las entregas de este lote son locales; no se afirma publicación Git de estos cambios.

No hay scheduler distribuido ni actividad 24/7 acreditados. Paperclip es un tablero de seguimiento; su configuración y estado efectivo se comprueban al actualizar la tarea correspondiente.

7 de noviembre, prueba `panel-cloud-001`. **Dos áreas ejecutaron en espacios Cloud separados, con 42 segundos de solape y recuperación del mismo paquete reciente por Git.** Organización verificó lectura del panel y actualización de una tarjeta sintética en Notion. El paquete probado está en la rama privada `codex/panel-cloud-20261107`. Quedan por comprobar arranque de este paquete en chat nuevo, actualización de vistas reales y uso móvil. [Informe y evidencia](continuidad/evidencias/panel-cloud-001/INFORME.md) · [Registro único](continuidad/tareas/panel-cloud-001.json)

7 de noviembre, prueba `seis-areas-cloud-001`. **Las seis áreas ejecutaron comprobaciones reales en Cloud en una ráfaga sincronizada, con unos 386 ms de solape nominal según los relojes de los ejecutores.** El ensayo de operación sostenida y el checkout completo de Platform en Cloud quedan fuera de esta comprobación. La revisión y el paquete de recibos están en la base local. [Informe de seis áreas](continuidad/evidencias/seis-areas-cloud-001/INFORME.md) · [Registro único](continuidad/tareas/seis-areas-cloud-001.json)

7 de noviembre, `arranque-diario-001`. **Panel privado de ONIA disponible desde Hoy en Notion y retoma del paquete diario comprobada en un chat Cloud nuevo.** Organización verificó una actualización en la página real. La rutina se inicia por encargo y el pendiente de Sergio es la toma de la primera pieza. Apertura móvil y recurrencia quedan por comprobar. [Panel diario](https://app.notion.com/p/4112eb20bdfd81c1a339e23eb82afa9d) · [Informe](continuidad/evidencias/arranque-diario-001/INFORME.md) · [Registro único](continuidad/tareas/arranque-diario-001.json)

B (01a1b251-c3f8-7781-9fcf-1874844c401f) arrancó desde el snapshot 9cf3e40 y recuperó por Git la entrega c3ac631; continuó de revisión 2 a 3 con siete controles aislados. Persistió el límite de anuncio nativo, aunque leyó las fuentes y aplicó la directora. La entrega B está publicada en 955e981; el cierre de aquella consolidación se publicó con 99da0bf a las 15:43 Caracas. La evaluación posterior se distingue arriba. Uso real de iPhone y ejecución permanente siguen sin acreditar.

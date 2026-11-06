# Estado vigente de ONIA

6 de noviembre de 2026 · America/Caracas. Este resumen distingue lo comprobado de lo pendiente. El [estado completo anterior](continuidad/2026-11-06/consolidacion-harness/HISTORICO.md) se conserva sin pérdida de bytes y se consulta por tema; no es una cola automática de nuevas tareas.

## Consolidación autorizada

Sergio decidió usar `onia`, con una sesión integradora y otra revisora, conservar lo existente, probar continuidad entre sesiones y mostrar el uso móvil. Fuente: chat “Explicar cómo funciona un harness”, turno `01a1b23b-288c-7853-9b84-9285f4dce5ae`. Integra “Mostrar mapa de skills y reglas” (`01a1b221-dbd1-7b10-aada-a26094e04705`); revisa “Explicar cómo funciona un harness” (`01a1af41-1ce0-7b72-a888-7fd658396b4a`).

Repositorio operativo: `oninteligenciaartificial/onia`, rama `master`, entorno Cloud `onia`. `onia-harness` se conserva como referencia; no se migran sus borradores ni se mantiene otro CLI operativo. ONIA Platform sigue separado.

Estado de esta unidad: **implementación local en revisión; todavía sin publicar ni acreditar continuidad A→B del código nuevo**. Los controles nuevos y la guía se describen en [CONTINUIDAD](cloud/CONTINUIDAD.md) y [MOVIL](cloud/MOVIL.md). La evidencia final debe actualizar este párrafo después de revisión y prueba reales.

## Último arranque comprobado

La prueba Cloud `01a1b238-b446-777a-93c0-e31f4034301f` arrancó en `7d26f84d82c138335727735e158df7b904e91582`, Git limpio. Verificó 9 enlaces propios en repo y 9 aliases del workspace, 9 skills propias y 9 apoyos externos resueltos, y doctor 30/30. Leyó reglas, mapa y desarrollar-y-verificar desde archivos.

**No anunció nativamente instrucciones de inicio ni skills ONIA.** La lectura explícita funcionó; no se acredita carga automática de Start skill. La prueba no ejecutó start.sh ni repitió los 39 tests que habían pasado en preparación. Tampoco acreditó traspaso a otra VM, móvil ni ejecución permanente.

## Contextos conservados por encargo

- Dirección comercial y metas: [PLAN](PLAN.md), sin sustituir una solicitud técnica expresa.
- Repartos, modelos y relevos anteriores: [SESIONES](SESIONES.md), con fechas y límites; el reparto de esta consolidación está arriba.
- Referentes, audio e infraestructura: [índice de investigación](investigacion/2026-11-05-referentes/GOAL-REFERENTES.md) y estado histórico. Los avances y restricciones de esas tandas no se reactivan por abrir otra sesión.
- Video D1, n8n, cuentas, VPS y producto: conservar evidencias en sus fichas y el estado anterior; no interpretar la consolidación como nuevas instalaciones, activación o despliegue.
- Contexto personal, credenciales, sesiones autenticadas y medios privados siguen fuera de Git.

No hay scheduler distribuido ni actividad 24/7 acreditados. Paperclip es un tablero de seguimiento; su configuración y estado efectivo se comprueban al actualizar la tarea correspondiente.

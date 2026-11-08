# Entrega técnica: evaluación de sesiones

6 de noviembre de 2026. Integradora: chat 01a1b221-dbd1-7b10-aada-a26094e04705. Base de comparación: 99da0bff96f289dc01fc10a20f745dc146f77427. El estado operativo se mantiene en [el registro único](../../tareas/evaluacion-sesiones-001.json); este informe conserva la evidencia técnica previa a publicar la nueva versión Cloud.

Se implementaron retoma breve con integridad previa, consulta completa e histórica, decisiones con procedencia y sustitución explícita, ficha de modelo recomendado/solicitado/observado y reserva local de rutas con revisión esperada. La lectura conserva los registros v1/v2 sin migrarlos. El texto del briefing queda una sola vez en tarea.briefing.contenido; se retiró deliberadamente el alias de texto duplicado de la respuesta de harness. Preparar conserva su respuesta de ruta.

Se reprodujo el fallo de privilegios de symlink en Windows y se añadieron junctions explícitas como alternativa local. Sólo se crearon los dos enlaces faltantes. Una sesión nativa nueva anunció las nueve skills propias sin herramientas ni lectura de cuerpos. Eso acredita el catálogo local de esa sesión, no el anuncio nativo en Cloud.

## Comprobaciones y revisión

- 75 pruebas definidas después de la última corrección: Windows, salida 0, 67 ejecutadas y 8 omitidas por privilegios de symlink; WSL/Linux local, salida 0, 74 ejecutadas y 1 omitida por corresponder a junctions Windows. Cobertura complementaria, no 75 ejecuciones por plataforma. [Registro de validación](../../../99-archivo/2026-11-06/evaluacion-sesiones/mediciones-cli/validacion-v1.json).
- La revisión independiente detectó y se corrigieron tres fallos: ID de decisión no canónico, espacios en el nombre del revisor y autorreferencia del JSON como evidencia. Las regresiones conservan el archivo previo y permiten retomarlo después del rechazo.
- Doce ensayos nativos en copias aisladas: cuatro de código, cuatro de extracción y cuatro de recuperación; todos cumplieron sus rúbricas congeladas. Las cuatro recuperaciones conservaron decisiones y restricciones, terminaron el caso completo para revisión y dejaron el dato indispensable ausente como una pregunta concreta. No hubo autoaceptación. [Comparativa y trazas](../../../99-archivo/2026-11-06/evaluacion-sesiones/comparativa-llm.md).
- Una prueba decimal suplementaria encontró InvalidOperation en r02 con un valor grande válido. Se conserva como fallo fuera de la rúbrica original, sin modificar la entrega ni repetir corridas LLM. No acredita corrección universal ni ganador general.
- Las mediciones CLI conservaron sus doce salidas exactas. Con 60 revisiones redundantes, la respuesta inicial pasó de 21 284 a 1 536 bytes; con consulta histórica adicional sumó 2 027. Con una revisión, breve más consulta suma 2 148 frente a 1 640 anteriores. Son bytes de fixtures, no tokens, contexto total ni dinero ahorrado.
- [Dictamen independiente favorable](../../../99-archivo/2026-11-06/evaluacion-sesiones/revision.md). La revisora comprobó 36 referencias de recuperación y 24 archivos ajenos intactos. La integradora comprobó los 190 archivos autorizados del manifiesto por ruta, bytes y SHA-256 antes de incorporarlos.

## Identificación reproducible

| Fuente | SHA-256 |
|---|---|
| scripts/trabajo.py | 6333fb5e5acf8ee7ba7000214316750056733d466e0d6124178d762c81d1768f |
| scripts/harness.py | cc08834debf81c792b55b3823bbb148a8c5cae51f5b0cd3b93d240f4b3127486 |
| casos/congelacion.json | df959a85f2a89ec55398bc110aecc3f7cd94e93bc2fd564bb797ec649383d5b0 |
| ejecuciones/manifiesto-evidencia.json | 4d328c966172866f979fd0ddee494c67d513b28533ceb9224c5ad17c9b5ac7be |
| comparativa-llm.md | a032f18600e68b3cdd1188189eb35c9bdaff2790d6f62b641b10dee449514b3b |

## Límites y continuación

La reserva coordina un checkout, no editores externos ni otros clones. Los nombres de actores y revisores son declaraciones, no autenticación. Una recomendación no selecciona el modelo efectivo; los metadatos observados tampoco prueban la procedencia interna del backend. No hubo compacción nativa observada, nueva prueba de catálogo nativo Cloud ni recorrido real desde iPhone. No se habilitaron servicios, agentes externos ni actividad permanente.

El [plan único](../../../99-archivo/2026-11-06/evaluacion-sesiones/PLAN.md) conserva criterios, responsables y la regla para usar recomendaciones provisionales sólo en tareas equivalentes. La siguiente etapa autorizada es integrar y publicar Git, comprobar esta versión en la preparación Cloud existente y guardar/publicar el snapshot de onia. Su confirmación debe registrarse aparte; este informe no la anticipa.

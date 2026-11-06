# Revisión independiente de la evaluación de sesiones

6 de noviembre de 2026 · America/Caracas. Revisora: chat `01a1af41-1ce0-7b72-a888-7fd658396b4a`. Base examinada: `99da0bff96f289dc01fc10a20f745dc146f77427`. La integradora conserva la escritura de fuentes; la coordinación conserva los ensayos. Esta revisión sólo escribe este documento.

**Dictamen favorable para integrar la implementación y la evidencia, dentro del alcance comprobado abajo.** Se revisaron el plan antes de los ensayos, los cambios, las rúbricas, los artefactos y las trazas públicas. No se lanzaron ensayos LLM duplicados ni se modificaron sus resultados para obtener aprobación. Un auxiliar nativo revisó compatibilidad y todas las trazas públicas; la revisora cotejó directamente código, evaluadores, artefactos, hashes, metadatos y salidas de las suites.

## Código y contratos

Runtime cotejado después de las correcciones:

- `trabajo.py`: SHA-256 `6333fb5e5acf8ee7ba7000214316750056733d466e0d6124178d762c81d1768f`.
- `harness.py`: SHA-256 `cc08834debf81c792b55b3823bbb148a8c5cae51f5b0cd3b93d240f4b3127486`.

La vista breve se construye después de comprobar la integridad. Conserva el estado actual y las restricciones del briefing; omite historia operativa y decisiones sustituidas. La consulta completa conserva el registro íntegro y la consulta histórica permite seleccionar una revisión. Leer no migra ni escribe registros v1/v2.

La forma de respuesta cambia deliberadamente: desaparece el alias raíz de texto `briefing`; el texto queda en `tarea.briefing.contenido`. Los consumidores examinados se adaptaron. `preparar` conserva su respuesta de ruta. Compatibilidad de datos no significa conservar la forma antigua de la respuesta.

Se detectaron y corrigieron antes de liberar el runtime conductual:

1. Un ID de decisión con espacios podía sobrevivir como vigente después de su sustitución. Ahora se rechaza el ID no canónico, también al validar un registro importado.
2. Espacios en el revisor podían eludir la comparación con el ejecutor declarado. La comparación ahora usa el nombre normalizado; no se reescribieron aceptaciones históricas.
3. Usar el propio JSON como evidencia o fuente de decisión/modelo invalidaba su hash al guardar. La comprobación común rechaza esa autorreferencia antes de escribir y conserva el registro anterior.

Las regresiones cubren rechazo, conservación y retoma posterior. La reserva de rutas serializa asignaciones dentro de un checkout y rechaza solapamientos; no intercepta editores externos ni coordina clones. Los nombres de actor y revisor son declaraciones de coherencia, no identidades autenticadas.

## Evidencia aceptada

| Unidad | Resultado observado |
|---|---|
| Suites posteriores al último cambio de runtime | 75 pruebas definidas. Windows: salida 0, 8 omisiones por symlinks, 9.454 s. WSL/Linux local: salida 0, 1 omisión de junction Windows, 12.043 s. Cobertura complementaria; no son pruebas Cloud de esta versión. |
| Congelación | Manifiesto v1 SHA-256 `df959a85f2a89ec55398bc110aecc3f7cd94e93bc2fd564bb797ec649383d5b0`; 11/11 archivos cotejados antes de evaluar. Rúbricas fuera de las copias ejecutoras. |
| Código r01–r04 | Las cuatro entregas cumplen los ocho casos congelados, conservan entradas protegidas y superan el cotejo independiente de no mutación. Se revisaron sus implementaciones y las verificaciones ejecutadas. |
| Extracción r05–r08 | Las cuatro conservan las tres tareas, nombres, orden, fecha absoluta y valores nulos requeridos. El cambio de mayúscula inicial de r08 es compatible con la equivalencia admitida por la rúbrica. |
| Recuperación r09–r12 | Las cuatro recuperan la proyección ausente, aplican `decision-v2`, excluyen anulados y obtienen `37.00` y 5 unidades. El principal queda `para_revision`; el secundario queda `en_espera`, moneda nula y una pregunta concreta guardada. No hay autoaceptación. |
| Integridad de recuperación | 36 referencias de evidencia, procedencia y briefing cotejadas por bytes/hash. Objetivo, briefing canónico, decisiones, asignación e historia previa se conservaron en las cuatro copias. |
| Modelos | Los metadatos observados de los doce ensayos coinciden con modelo/esfuerzo solicitados. Las recomendaciones del manifiesto no configuran por sí mismas el runtime. |
| Catálogo local | Un subagente local nuevo anunció las nueve skills, con cero llamadas a herramientas. Acredita ese anuncio local; no acredita lectura de cuerpos, Cloud ni compacción. |

En las llamadas públicas examinadas no aparecen red, lectura de rúbricas, otras ejecuciones ni modificaciones explícitas fuera de los workspaces autorizados. r04 recuperó un fallo inicial de parche. Algunas llamadas conservaron sólo stdout y no el código de salida nativo; las comprobaciones finales y los artefactos se cotejaron igualmente. El payload de un mensaje interno de r02 está omitido y no se usa como evidencia textual.

## Límites que cambian la interpretación

**Doce aprobaciones de la rúbrica no prueban corrección ilimitada.** La lectura de r02 identificó una insuficiencia de precisión decimal. Una comprobación suplementaria sobre las mismas cuatro entregas, sin nuevas corridas LLM, confirmó `InvalidOperation` en r02 para un precio grande válido; las otras tres respondieron correctamente. Se conservó el fallo separado y no se alteraron rúbrica ni resultados originales. Ver [evidencia suplementaria](ejecuciones/limite-precision-suplementario.json).

Las [mediciones CLI](mediciones-cli/v1/resultados.json) conservan doce salidas exactas, todas cotejadas. Con 60 revisiones redundantes, la salida inicial pasó de 21 284 a 1 536 bytes; vista breve más consulta histórica sumó 2 027. Con una revisión, esa consulta adicional suma 2 148 bytes frente a 1 640 anteriores. Son bytes de fixtures y respuestas, no tokens, coste facturado ni contexto total del LLM. Tampoco prueban selección semántica de historia necesaria.

Las métricas de ejecución separan primer uso, serie y uso final, entrada acumulada, caché y salida. La entrada acumulada incluye relecturas; no es una única ventana de contexto. Dos repeticiones por candidato son un diagnóstico. No se aprueba declarar un ganador general ni ahorro universal con estos datos.

No se observó compacción nativa. El anuncio nativo en Cloud y el recorrido real desde iPhone siguen fuera de esta evidencia. El reparto de rutas y la revisión esperada local no constituyen un bloqueo distribuido. Los perfiles LLM son candidatos declarativos; el modelo efectivo debe seguir comprobándose por ejecución.

## Conservación y cierre

Se cotejó también el informe final [comparativa-llm.md](comparativa-llm.md), SHA-256 `a032f18600e68b3cdd1188189eb35c9bdaff2790d6f62b641b10dee449514b3b`: sus conclusiones conservan los límites anteriores y su tabla coincide con las doce métricas registradas. El [manifiesto de evidencia](ejecuciones/manifiesto-evidencia.json), SHA-256 `4d328c966172866f979fd0ddee494c67d513b28533ceb9224c5ad17c9b5ac7be`, verifica 190/190 archivos y 754 555 bytes, sin discrepancias. No incluye su propio archivo ni este dictamen.

La revisora cotejó 24/24 archivos ajenos contra los hashes tomados al iniciar esta unidad: intactos. También comprobó que ninguno aparecía en los 45 archivos preparados por la integradora al revisar el índice. La protección de bytes de casos, ejecuciones y mediciones es explícita en `.gitattributes`; no se normalizaron datos congelados para hacer coincidir sus hashes.

Se aprueban técnicamente las unidades descritas y su incorporación bajo el [plan acordado](PLAN.md). El estado y el siguiente paso operativo se mantienen únicamente en [evaluacion-sesiones-001](../../tareas/evaluacion-sesiones-001.json). Este dictamen no certifica por sí mismo commit, push ni publicación de un snapshot Cloud posterior: la integradora debe registrar esas confirmaciones al efectuarlas y conservar estos límites en la entrega.

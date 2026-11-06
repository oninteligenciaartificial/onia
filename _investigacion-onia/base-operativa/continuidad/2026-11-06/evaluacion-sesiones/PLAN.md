# Evaluación de sesiones ONIA

Autorización de Sergio: «Solucionemoslo de una vez y lancemos todas las pruebas necesarias, y hacemos el plan de trabajo», chat 01a1b245-bfe7-70f1-a4a1-a8c6eed15b4a, turno 01a1b29e-d8c4-7610-aab8-d4b94f8c8580. Base inicial 99da0bff96f289dc01fc10a20f745dc146f77427.

## Estado único y responsabilidades

El estado operativo, resultado, evidencia y siguiente paso están únicamente en [evaluacion-sesiones-001](../../tareas/evaluacion-sesiones-001.json). Consultar con trabajo.py retomar evaluacion-sesiones-001. Este plan define alcance y criterios; no duplica su progreso.

- Integradora 01a1b221-dbd1-7b10-aada-a26094e04705: única escritora de scripts, tests, manifiesto, documentos operativos, este plan, casos/ y mediciones-cli/. Integra después de revisión; no incorpora archivos ajenos.
- Coordinación 01a1b245-bfe7-70f1-a4a1-a8c6eed15b4a: única escritora de ejecuciones/ y comparativa-llm.md; ejecuta las comparaciones nativas en copias aisladas.
- Revisora 01a1af41-1ce0-7b72-a888-7fd658396b4a: única escritora de revision.md; revisa fuentes, rúbrica y evidencia sin editar implementación.
- No nuevos chats, servicios, agentes externos ni gasto adicional. ONIA-CENTRAL y contexto personal excluidos. No n8n, producto ni móvil salvo dependencia concreta.

## Unidades y aceptación

| Unidad | Entregable y criterio | Evidencia prevista |
|---|---|---|
| Recuperación | Vista breve predeterminada, briefing una sola vez, decisiones vigentes y restricciones conservadas; historial y registro completo explícitos. Verificar antes de proyectar; no modificar el JSON al leer. | Tests de compatibilidad e integridad; mediciones-cli/ compara salida inicial y consultas posteriores por separado. |
| Decisiones | Procedencia con hash y sustitución explícita de una decisión vigente; ninguna eliminación de historia ni aceptación automática. | Caso recuperacion y tests de reemplazo válido/inválido. |
| Ejecución | Recomendado, solicitado y observado separados; null significa desconocido. Una recomendación no cambia el runtime. Observado requiere fuente; identidad y calidad no se infieren del hash. | Ficha canónica, trazas de coordinación y comparativa-llm.md. |
| Escritura | Responsable declarado, rutas normalizadas, revisión esperada y reserva local serializada contra solapamientos. Reasignar/liberar explícitamente. No bloquea editores externos ni otros clones. | Tests con procesos, rutas idénticas/anidadas/vecinas y actor incorrecto; revisión de límites. |
| Skills | Corregir preparación incompleta demostrable y separar enlaces, fuente leída y catálogo anunciado. No certificar descubrimiento ni compacción por inferencia. | Chequeo de enlaces y recibo observado; límites si faltan capacidades. |

## Contrato de recuperación

trabajo.resume(base, id, complete=False) y harness.resume(base, id, complete=False) devuelven tarea con estado vigente. El briefing aparece una sola vez en tarea.briefing.contenido. Se elimina el alias duplicado de texto en la raíz de la respuesta de harness; sus consumidores se actualizan explícitamente. preparar conserva briefing como ruta y no cambia ese contrato.

- retomar ID: omite historial y decisiones sustituidas, informa contadores y consultas disponibles.
- retomar ID --completo: registro canónico íntegro, sin escrituras.
- historial ID [--revision N]: historia operativa explícita, sin confundirla con autorización vigente.
- decidir, ejecucion y asignar: requieren revisión esperada; no cambian estado del runtime. actualizar/recuperar requieren actor si hay asignación; aceptar requiere revisor distinto del ejecutor declarado.
- Los campos nuevos son opcionales en schema 2. Schema 1 conserva lectura histórica y migración explícita. La integridad del briefing/evidencia vigente se comprueba también en vistas breves e históricas.

## Casos congelados y comparación

Los datos, prompts y rúbrica están en casos/. Preparar cada copia con casos/preparar.py; sólo copia entrada/ y prompt, nunca rubrica.json. El manifiesto congelacion.json fija SHA-256 antes de cualquier ejecución evaluada. Una corrección posterior requiere nueva versión, razón y no mezcla resultados incompatibles.

Máximo inicial: 12 ejecuciones, tres casos por dos candidatos por dos repeticiones, en contextos frescos. Recuperación y código: Sol 6.1/medium frente a Terra 6.1/medium. Extracción: Luna 6/high frente a Sol 6.1/high. La coordinación conserva identificador, prompt exacto, hashes de entrada/runtime, modelo y esfuerzo solicitados y observados, herramientas, acciones, resultado, preguntas, tiempo y uso disponibles. No inferir USD, tokens o modelo efectivo si no están expuestos.

La rúbrica se fija antes de evaluar. Dos repeticiones son diagnóstico, no garantía estadística. Comparar sólo ejecuciones con capacidades equivalentes; falta de herramienta es incompatibilidad, no prueba de menor inteligencia. Elegir menor uso entre candidatos que cumplen todos los criterios; no declarar ganador cuando la evidencia no distingue.

Los perfiles generales de orquestacion.json son candidatos iniciales. Para trabajos equivalentes a los ensayos del 6/11, consultar la tabla fechada de [comparativa-llm.md](comparativa-llm.md): Sol 6.1/medium es la recomendación provisional para código decimal y recuperación evaluados. Registrar en la ficha el criterio y cualquier diferencia respecto del candidato general, sin cambiar automáticamente el runtime. La extracción no demuestra ahorro monetario de Luna. Doce ensayos no justifican reemplazar los perfiles por una regla universal.

El caso conductual incluye un escenario completo con fallo recuperable y otro con moneda indispensable sin determinar. Termina para_revision o en_espera según corresponda, sin autoaceptarse. La consulta indispensable se registra en la copia, sin pedir un dato ficticio al usuario real. Compacción nativa sólo se acredita con un evento observado; un relevo, resumen manual o copia no la prueba.

## Medición y cierre

Medir por separado bytes UTF-8/caracteres del archivo canónico, respuesta inicial serializada y respuestas consultadas después; tokens sólo si hay contador fiable. Comparar historia corta/larga con la misma información necesaria. La rúbrica identifica decisiones críticas y material irrelevante antes de ver resultados. Menor tamaño sin conservación de decisiones no aprueba.

Después del último cambio de código, ejecutar suites pertinentes, presentar diff/evidencia al revisor y registrar resultado en la tarea única. Preparar Git/publicación tras dictamen; no publicar fuentes ajenas ni describir pruebas locales como Cloud. La aceptación de una unidad no acredita 24/7, compacción nativa ni descubrimiento automático.

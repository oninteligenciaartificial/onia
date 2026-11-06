# Comparación de LLM y recuperación de sesiones ONIA

Fecha: 2026-11-06. Responsable de esta evidencia: coordinación 01a1b245-bfe7-70f1-a4a1-a8c6eed15b4a.

Los doce ensayos cumplieron la rúbrica congelada. Una comprobación adicional encontró un fallo real de precisión decimal en r02; se conserva separado y sin reparar la entrega evaluada. Estos resultados permiten elegir candidatos para tareas similares, pero no garantizan cumplimiento universal, compacción nativa ni funcionamiento continuo.

## Diseño y reproducibilidad

[PLAN.md](PLAN.md) fija alcance, responsabilidades y aceptación. El estado operativo vive únicamente en [evaluacion-sesiones-001](../../tareas/evaluacion-sesiones-001.json); este documento registra un experimento fechado.

- Tres casos, dos candidatos por caso y dos repeticiones: 12 subagentes nativos con contexto fresco, sin heredar este chat. Sin red, delegación ni lectura del repositorio anfitrión, rúbricas u otras ejecuciones.
- Mismo prompt de lanzamiento salvo ruta de la copia. Una semilla por caso y copias byte a byte mantienen iguales los datos y fechas iniciales. Cada solicitud conserva hashes de entrada y prompt normalizado.
- [Congelación](casos/congelacion.json): SHA-256 `df959a85f2a89ec55398bc110aecc3f7cd94e93bc2fd564bb797ec649383d5b0`. Once archivos fijados antes de las ejecuciones; el generador nunca copia la rúbrica al agente.
- Runtime copiado de recuperación: `trabajo.py=6333fb5e5acf8ee7ba7000214316750056733d466e0d6124178d762c81d1768f`; `harness.py=cc08834debf81c792b55b3823bbb148a8c5cae51f5b0cd3b93d240f4b3127486`.
- Modelo y esfuerzo solicitados coinciden con la metadata nativa `turn_context` observada en las doce ejecuciones. Es observación de configuración, no una auditoría independiente del backend.
- Hay dos observaciones por configuración. Herramientas e instrucciones de plataforma pueden variar entre modelos aunque la tarea y sus archivos sean idénticos; no es una comparación estadística aislada del modelo.

Cada carpeta [ejecuciones/r01](ejecuciones/r01) a [r12](ejecuciones/r12) contiene solicitud, prompt, copia de trabajo, evaluación funcional, runtime, acciones y resultados públicos de herramientas. No se guardó contenido de razonamiento. El payload opaco de un mensaje interno en r02 está redactado, manteniendo metadatos de la llamada. [recopilar_runtime.py](ejecuciones/recopilar_runtime.py) documenta la extracción y [evaluar_funcional.py](ejecuciones/evaluar_funcional.py) la verificación.

## Resultado por tarea

| Tarea y ejecuciones | Sol 6.1 | Segundo candidato | Resultado observado |
|---|---|---|---|
| Código decimal: r01–r04, medium | 2/2 | Terra 6.1: 2/2 | Ocho entradas congeladas correctas, sin mutación de datos; alcance y archivos protegidos conservados. |
| Extracción: r05–r08, high | 2/2 | Luna 6: 2/2 | Tres tareas en orden, responsables y fecha explícita correctos; datos ausentes/fecha relativa como null; comentario excluido. |
| Recuperación: r09–r12, medium | 2/2 | Terra 6.1: 2/2 | Recuperaron el briefing ausente y aplicaron decision-v2. Pedido completo: 37.00, cinco unidades, USD, para_revision. Pedido incompleto: mismo total, moneda null, en_espera y una pregunta concreta. |

La evaluación independiente hace 19 comprobaciones por entrega de código, 12 por extracción y 41 por recuperación. Son comprobaciones sobre doce escenarios, no 288 experimentos independientes. Recuperación conserva objetivo, briefing, decisiones, asignación e historia previa; verifica integridad y registro de evidencia. Ningún agente se autoaceptó. La revisión de trazas públicas contrasta acciones reales con el autorreporte; el [dictamen independiente](revision.md) detalla su alcance.

Proactividad observada: terminar lo resoluble, recuperarse de un archivo de briefing ausente y detener sólo la parte que requiere una moneda no proporcionada. Esto prueba conducta en una tarea activa. No acredita un scheduler, vigilancia continua ni autonomía 24/7.

## Fallo adicional que cambia la interpretación

La revisora detectó que r02 dependía de la precisión global predeterminada de Decimal. La entrada válida `1234567890123456789012345678.995`, una unidad activa, debe producir `1234567890123456789012345679.00`.

Se ejecutó ese límite sobre las cuatro entregas existentes, sin nuevas corridas LLM ni cambio de rúbrica: r01, r03 y r04 pasan; r02 produce `InvalidOperation`. Ninguna muta la entrada. La evidencia está en [limite-precision-suplementario.json](ejecuciones/limite-precision-suplementario.json).

Por eso “12/12 con rúbrica inicial” no significa “12 soluciones correctas para cualquier entrada”. El fallo es de una entrega sintética, no del runtime ONIA; no se arregló retroactivamente para mejorar la nota. En futuras tareas de importes con magnitud no acotada, incluir esta frontera antes de aceptar la solución.

## Tiempo y uso observados

Los valores siguientes provienen de runtime.json y se consolidan en [metricas-r01-r12.json](ejecuciones/metricas-r01-r12.json). Entrada inicial es la primera llamada registrada. Entrada y caché acumuladas suman llamadas, con texto repetido: no equivalen al contexto ocupado de una sola llamada. Salida ya incluye el razonamiento cuando la telemetría así lo indica; no se suma de nuevo. Duración incluye arranque y herramientas en un equipo compartido. No se midieron dólares ni cuota facturada.

| Run | Configuración | Segundos | Entrada inicial | Entrada acumulada | Caché acumulada | Salida acumulada |
|---|---|---:|---:|---:|---:|---:|
| r01 | Sol 6.1 medium | 50.56 | 20170 | 83974 | 75776 | 1630 |
| r02 | Terra 6.1 medium | 36.41 | 20106 | 104090 | 81664 | 1222 |
| r03 | Sol 6.1 medium | 55.19 | 20170 | 84143 | 74240 | 1892 |
| r04 | Terra 6.1 medium | 49.74 | 20106 | 105922 | 101376 | 2080 |
| r05 | Luna 6 high | 26.29 | 19479 | 80182 | 71552 | 1051 |
| r06 | Sol 6.1 high | 33.28 | 20296 | 83740 | 75520 | 961 |
| r07 | Luna 6 high | 34.62 | 19605 | 101663 | 92288 | 1304 |
| r08 | Sol 6.1 high | 32.69 | 20296 | 83675 | 72960 | 975 |
| r09 | Sol 6.1 medium | 78.65 | 20296 | 203486 | 192512 | 2401 |
| r10 | Terra 6.1 medium | 55.56 | 20232 | 247891 | 216064 | 1819 |
| r11 | Sol 6.1 medium | 67.50 | 20296 | 174044 | 163456 | 2070 |
| r12 | Terra 6.1 medium | 63.67 | 20232 | 246625 | 224768 | 2063 |

## Elección provisional para ONIA

| Trabajo similar al ensayado | Candidato inicial según esta muestra | Condición para usarlo |
|---|---|---|
| Cambios acotados con aritmética decimal | Sol 6.1 / medium | Dos entregas pasan también la frontera adicional; mantener pruebas de magnitud y revisión. Terra sigue siendo candidato, pero esta muestra no justifica preferirlo por calidad. |
| Recuperación y ejecución desde registro canónico | Sol 6.1 / medium | Ambos modelos cumplen; Sol usó menos entrada acumulada en las dos repeticiones. Terra fue más rápido aquí. No hay ganador en todos los ejes. |
| Extracción estructurada como la probada | Sol 6.1 / high, con Luna 6 / high como alternativa validada | Ambos cumplen. Sol tuvo menor promedio de entrada y salida acumuladas; Luna fue algo más rápido en promedio. No hay evidencia de ahorro monetario ni de que high sea necesario. |
| Arquitectura o decisión compleja fuera de estos casos | Sin ganador experimental | Elegir por dificultad/herramientas y validar con criterio propio de la tarea. Astra no fue comparado aquí. |

La documentación oficial ofrece orientación por carga de trabajo; este experimento agrega evidencia local limitada, sin sustituirla por una clasificación universal. Referencias consultadas: [modelos](https://learn.chatgpt.com/docs/models), [selección de modelos](https://learn.chatgpt.com/docs/model-selection) y [guía de evaluación/selección](https://developers.openai.com/api/docs/guides/model-selection).

El manifiesto sugiere candidatos. La orquestación debe solicitar explícitamente el modelo/esfuerzo compatible y registrar lo observado. Guardar una recomendación no cambia el modelo del chat. Escalar por un fallo identificado o mayor dificultad, sin confundir falta de herramienta, cuota o credenciales con falta de capacidad. No se contrataron servicios ni planes adicionales; las ejecuciones nativas consumen el uso disponible.

## Contexto: qué disminuye y qué queda por medir

La medición CLI separada de la integradora compara el mismo objetivo, restricciones y próximo paso con historia redundante de 1, 6 y 60 revisiones. A 60 revisiones, la respuesta inicial pasa de 21284 a 1536 bytes UTF-8 (92.8% menos); vista breve más una consulta histórica suma 2027 bytes. El archivo canónico conserva 18535 bytes y las lecturas no lo alteran. [Resultados y salidas exactas](mediciones-cli/v1/resultados.json).

Esto mide bytes serializados, no tokens ni todo el contexto del modelo. Los ensayos conductuales arrancaron desde cuatro revisiones; no prueban conducta con 60 revisiones. La entrada nativa inicial ya ronda 19–20 mil tokens antes de leer la tarea: existe coste de instrucciones/herramientas de plataforma fuera de la respuesta CLI. No observamos eventos de compacción nativa en ninguna corrida y no los simulamos llenando el contexto.

Después de reparar los enlaces locales, un subagente fresco anunció las nueve skills ONIA desde su catálogo inicial, con cero herramientas y cero lecturas de archivos: [evidencia de catálogo local](ejecuciones/catalogo-local/runtime.json) y [respuesta pública](ejecuciones/catalogo-local/trace-actions.json). Acredita anuncio local; no acredita lectura automática del cuerpo de cada skill ni descubrimiento en Cloud.

## Rutina de trabajo y siguientes comprobaciones

1. Una tarea canónica con objetivo, restricciones, responsable, rutas, evidencia y siguiente paso. Cada sesión retoma por ID y commit usando la vista breve; consulta detalle sólo ante una necesidad.
2. Elegir candidato/esfuerzo según trabajo y herramientas. Registrar recomendado, solicitado y observado por separado; null cuando no se puede observar.
3. Avanzar en pasos autorizados y verificables. Si falta un dato imprescindible, guardar el parcial y una pregunta concreta; continuar las partes independientes.
4. Un escritor por archivo y revisión esperada para mutaciones. La reserva local no protege otros clones ni editores externos: coordinar repositorio, revisión y responsables.
5. Verificar y someter a revisión distinta del ejecutor antes de aceptar. La próxima sesión carga estado y decisiones vigentes desde archivos, no todo el chat.
6. Comprobar el arranque nativo Cloud tras publicar el runtime actual; conservar como pendiente cualquier catálogo no anunciado. Si se necesita garantía específica tras compacción, hacer un ensayo con evento real observable y criterios fijados previamente. No repetir la batería actual sin cambios o incertidumbre concreta.

[PLAN.md](PLAN.md) contiene el contrato de trabajo; [revision.md](revision.md) registra la revisión independiente. El estado de integración y los pendientes operativos se consultan en la tarea única, no se infieren de este informe.


# Harness de agentes: investigación y auditoría de OnIA

Fecha: 8 de noviembre de 2026. Estado: propuesta entregada para revisión; sin implementación ni publicación en GitHub.

## 1. Qué es un harness en 10 líneas

1. El modelo es quien razona; el harness es el sistema que le permite trabajar. [F1]
2. Su bucle envía contexto al modelo, recibe acciones, ejecuta herramientas y devuelve resultados. [F1]
3. Las herramientas conectan ese razonamiento con archivos, comandos y otros sistemas. [F3]
4. Las instrucciones del proyecto, como AGENTS.md, conservan reglas entre sesiones. [F4]
5. El estado persistente guarda qué se hizo y desde dónde continuar. [F5]
6. El sandbox y los permisos limitan lo que el agente puede hacer realmente. [F3, F6]
7. Una capa de coordinación puede repartir tareas entre sesiones; no es obligatoria para un agente único. [F3; recomendación de diseño]
8. Las pruebas comprueban el resultado; un mensaje de “terminado” no basta. [F2]
9. Los registros y entregas de relevo permiten investigar fallos y continuar después. [F2, F6]
10. OnIA ya tiene varias de estas piezas; falta conectar mejor su ejecución local y su cierre verificable.

## 2. Fuentes y conclusiones de la investigación

Fuentes consultadas en la web en esta revisión. Las afirmaciones técnicas se apoyan en fuentes primarias; las conversaciones comunitarias son contraste, no garantías. No se instaló ni ejecutó software externo.

| ID | Fuente real | Qué respalda |
|---|---|---|
| F1 | [OpenAI: Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | El bucle del agente conecta inferencia, contexto y herramientas. |
| F2 | [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) | Trabajo incremental, registro de progreso y comprobación para continuar entre ventanas de contexto. |
| F3 | [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) | Herramientas, bucle, contexto, sesiones, hooks, subagentes y permisos. Se estudia como referencia; no se propone usar Claude en OnIA. |
| F4 | [OpenAI: Iterating Development Workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) | AGENTS.md como guía persistente y desarrollo organizado en fases con criterios. |
| F5 | [LangGraph: Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Checkpoints por hilo para recuperar estado. Persistir estado no equivale a garantizar que una acción externa se haga una sola vez. |
| F6 | [Codex: modo no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode) | codex exec, eventos JSONL, salida estructurada y reanudación por ID. |
| F7 | [Git: git-worktree](https://git-scm.com/docs/git-worktree) | Varios árboles de trabajo asociados a un repositorio y ramas separadas. |
| F8 | [GitHub: openai/codex](https://github.com/openai/codex) | Implementación pública de Codex CLI; permite inspeccionar el runtime, distinto de los scripts de OnIA. |
| F9 | [Anthropic: Managed Agents](https://www.anthropic.com/research/managed-agents) | Distingue sesión, harness y sandbox; separar esas responsabilidades facilita evolucionar el sistema. |
| C1 | [Hacker News: discusión del artículo de Anthropic](https://news.ycombinator.com/item?id=46081704) | Debate sobre tickets, contexto recuperable y límites de reglas escritas. Opiniones comunitarias. |
| C2 | [Reddit: experiencia construyendo y abandonando un harness](https://www.reddit.com/r/ClaudeAI/comments/1w8jhfp/i_spent_883_commits_and_8_months_building_an_llm/) | Experiencia anecdótica sobre complejidad y trazabilidad. No prueba rendimiento ni fiabilidad. |
| C3 | [X: publicación enlazada desde una discusión sobre harnesses](https://x.com/Jeremy069626792/status/2047957927030669420) | Se intentó abrir; devolvió 403. No se usa como evidencia de contenido ni se atribuyen afirmaciones a su autor. |

**Lectura práctica.** El bucle básico ya lo proporciona Codex. OnIA debe aportar el contrato de tarea, contexto pertinente, permisos, seguimiento, comprobaciones y relevo. Añadir otro framework no es un requisito de la definición. Esta es una recomendación arquitectónica derivada de F1, F3 y F9.

**Memoria.** Hay tres cosas distintas: reglas estables, estado de una tarea y conversación de una sesión. AGENTS.md ayuda con la primera; los registros de OnIA con la segunda; reanudar Codex con la tercera. Ninguna sustituye automáticamente a las demás. [F4, F5, F6]

**Cola y fallos.** Para varias tareas conviene registrar dependencias, responsable, intento y motivo de parada fuera del texto libre del modelo. Es una propuesta para OnIA, no una capacidad que toda herramienta citada prometa. Los checkpoints de F5 y el progreso de F2 ofrecen patrones reutilizables.

### Cómo lanzar Codex en paralelo

Patrón propuesto, **no ejecutado aquí**: Boss separa dos tareas independientes; cada proceso Codex trabaja en su rama y worktree, guarda sus eventos y entrega evidencia; después se integra una por una. Git proporciona los worktrees [F7] y Codex la ejecución no interactiva y JSONL [F6]. El paralelismo siguiente lo aporta el shell, no un scheduler implícito de codex exec.

```bash
# Ejemplo para una futura fase autorizada, desde un checkout de integración.
# No usar el master que otra sesión está editando.
git worktree add -b codex/tarea-a ../onia-tarea-a <COMMIT_BASE>
git worktree add -b codex/tarea-b ../onia-tarea-b <COMMIT_BASE>

codex exec -C ../onia-tarea-a --sandbox workspace-write --json \
  'Ejecuta únicamente la tarea A y sus comprobaciones autorizadas' > tarea-a.jsonl 2>&1 &
pid_a=$!
codex exec -C ../onia-tarea-b --sandbox workspace-write --json \
  'Ejecuta únicamente la tarea B y sus comprobaciones autorizadas' > tarea-b.jsonl 2>&1 &
pid_b=$!
wait "$pid_a"; rc_a=$?
wait "$pid_b"; rc_b=$?
```

El futuro lanzador debe conservar ambos códigos, el commit base, IDs y rutas. Reanudar con `codex exec resume <SESSION_ID>` evita elegir accidentalmente otra sesión mediante `--last`. [F6] Antes de usar el ejemplo hay que revisar permisos y versión instalada. Los worktrees separan archivos de trabajo; no aíslan cuentas, servicios ni efectos externos. No copiar secretos como parte de la preparación.

## 3. Estado del harness de OnIA

### Alcance y evidencia de esta auditoría

Se leyeron `LEEME.md`, `registro.tsv`, ambos runners y los documentos/código indicados del repo. Se consultaron además `00-MAPA/ESTADO.md` y las instrucciones de entrada. Las lecturas extensas tuvieron salidas truncadas en algunos bloques: el análisis del archivo histórico y los tests es documental y parcial, con recuperación dirigida de funciones y nombres de casos; no se presenta como revisión exhaustiva de cada línea histórica.

`./ejecutar.sh --comprobar` terminó con rc=0: estructura válida y lock exclusivo. No invocó Codex ni movió tareas. No se ejecutaron tests, doctor, scripts del repo, Git, Docker, n8n ni servicios. No se consultaron credenciales. Sólo se escribió esta entrega en `operacion/resultados/`. El comprobador abre el archivo de lock local como parte de su operación prevista.

La lectura del repo y la investigación web siguen el encargo actual, que amplía esas dos restricciones del texto inicial. El permiso de escritura se limita a resultados: por eso inicio, fin y estado se conservan aquí, sin modificar `registro.tsv` ni `tareas/`.

Otra sesión escribe en el repo: **no hay snapshot atómico ni HEAD actual verificado en esta auditoría**. Los commits y resultados históricos citados abajo son declaraciones de los documentos leídos, no una nueva comprobación remota. La disponibilidad de push mediante deploy key es información aportada por Sergio; no se probó ni se inspeccionó la clave.

### Lo que ya existe

| Pieza | Evidencia local | Valor y límite |
|---|---|---|
| Entrada y memoria de reglas | `AGENTS.md`, `04-operacion-agentes/reglas-comunes.md` | Hay fuente canónica y carga selectiva. No toda la memoria de Boss está formalizada con las reglas exactas del encargo actual. |
| Selección de trabajo | `ORQUESTACION.md`, `orquestacion.json`, `harness.py:prepare` | Seleccionan área, directora, apoyos y briefing. Los perfiles de modelo son recomendaciones, no configuración efectiva. |
| Estado y continuidad | `trabajo.py:create`, `mutate`, `resume`, `recover` | JSON canónico, revisión esperada, historial, evidencia con hashes y briefing recuperable. Ya hay memoria persistente útil. |
| Concurrencia local | `trabajo.py:locked`, `assign` | Locks y reservas de rutas en un checkout. No bloquean editores externos ni coordinan clones/worktrees distintos. |
| Entrega y revisión | `trabajo.py:validate`, `accept` | Exige evidencia y verificación correcta para entregar. Si existe asignación, impide aceptar con el mismo nombre del responsable; los nombres siguen siendo declaraciones. |
| Tests | `test_harness.py`, `test_trabajo.py` | Hay casos para corrupción, revisión obsoleta, interrupciones, rutas privadas, concurrencia y asignación. Leídos parcialmente; no ejecutados hoy. |
| Errores y aprendizaje | `registro-de-errores.md` | Conserva casos y correcciones. La lectura de lecciones sigue dependiendo del procedimiento; no es un motor de recuperación automática. |
| Traspaso entre sesiones | `99-archivo/2026-11-06/consolidacion-harness/INFORME.md` | Documenta A→Git→B aceptado técnicamente. No hay que reconstruirlo desde cero ni confundirlo con trabajo continuo. |
| Paralelismo Cloud | `00-MAPA/ESTADO.md` | Documenta dos áreas con 42 s de solape y otro ensayo de seis áreas con solape nominal de unos 386 ms. No acredita operación sostenida ni lanzador local. |
| Lanzamiento local | `ejecutar.sh` | Cola de carpetas, lock global, timeout 300 s, read-only, logs y rc. Es un runner manual de análisis acotado. |
| Variante n8n | `ejecutar-n8n.sh` | Mismo lock, 900 s, workspace-write y configuración de red habilitada; antepone reglas. No se ejecutó ni se comprobó su acceso efectivo. |

**Diagnóstico:** OnIA tiene un harness compuesto: Codex aporta el motor; el repo aporta reglas, preparación, estado y revisión; los runners aportan una ejecución manual limitada. Falta un supervisor local conectado a esos registros. `harness.py` y `trabajo.py` dicen expresamente que no lanzan agentes ni usan red.

El runner de 300 s sí sirve para tareas cortas de lectura. No permite implementar código en ese modo, y corta tareas que excedan cinco minutos. Cambiarlo a escritura no soluciona por sí solo continuidad, coordinación o publicación. `-a on-request` tampoco demuestra que haya aprobación humana disponible en ejecución headless; no debe usarse como garantía.

La auditoría del 6 de noviembre en `2026-11-06-agentes-harness/auditoria-onia.md` es un antecedente valioso, pero varios pendientes avanzaron después según ESTADO e INFORME. No trasladar sin cotejo sus carencias antiguas al diagnóstico actual.

## 4. Correcciones propuestas

Rutas del repo relativas a `_investigacion-onia/base-operativa/`, salvo indicación. **P0:** antes de habilitar escritura/paralelismo. **P1:** mínimo operativo siguiente. **P2:** mejora después del piloto. Toda fila es propuesta, no permiso para ejecutarla.

| Prioridad | Hueco y por qué importa | Archivo y cambio concreto propuesto | Comprobación de aceptación |
|---|---|---|---|
| P0 | Reglas de Sergio repartidas entre chat, repo y operación local: una sesión puede arrancar con una política anterior. | `04-operacion-agentes/reglas-comunes.md`: incorporar Codex ejecuta todo, Boss coordina, proponer antes de escribir, cobrar/gastar y activar n8n sólo con su sí; cerrar sólo con evidencia en GitHub. `AGENTS.md` enlaza esa fuente, sin duplicarla. | Sesión nueva recupera las reglas y distingue propuesta, permiso y capacidad. |
| P0 | La lectura de reglas no está garantizada por generar enlaces en el briefing. | Nuevo `05-herramientas/scripts/ejecutor.py`: construir entrada mínima con reglas canónicas, tarea y permisos; guardar rutas/hashes del contexto suministrado y versión de política. | Una regla de prueba aparece en la entrada; si falta el archivo, el lanzamiento se bloquea. El hash no se presenta como prueba de obediencia. |
| P0 | No hay cierre remoto obligatorio en `accept`; éxito local puede confundirse con entrega final. | `trabajo.py` y `test_trabajo.py`: separar aceptación técnica de publicación; añadir recibo con repo, rama, commit de entrega y evidencia de verificación remota. Evitar guardar dentro del commit su propio hash: recibo posterior. | Sin recibo no se declara cierre final; aceptación técnica local sigue siendo posible y explícita. |
| P0 | El runner n8n amplía escritura/red; sus límites dependen de reglas y entorno. | `operacion/ejecutar-n8n.sh` y reglas asociadas: política explícita de acciones, destino y autorización por operación; separar edición de activación. Mantener cobros/gastos y activación bloqueados sin sí aplicable. | En un doble de prueba, una activación sin autorización se rechaza antes de salir al servicio. No probar en n8n real ahora. |
| P1 | Timeout fijo de 300 s sin protocolo de checkpoint: una tarea larga se pierde a mitad. | Conservar `operacion/ejecutar.sh` para lectura; nuevo `ejecutor.py` con límite por tarea acotado, parada explícita y checkpoint persistido durante el trabajo. | Interrumpir una tarea sintética y recuperar su siguiente paso sin repetir efectos. No eliminar todos los límites. |
| P1 | Preparación y runner usan registros distintos: JSON del repo frente a carpetas/TSV local. | `ejecutor.py` referencia ID y revisión de `trabajo.py`; añadir intento, sesión, inicio/fin, rc y motivo de parada. Los logs privados quedan fuera del repo; exportar resumen saneado. | Una tarea permite seguir preparación→ejecución→verificación sin dos estados contradictorios. |
| P1 | No hay lanzador local paralelo en los archivos auditados. | Nuevo `05-herramientas/scripts/sesiones.py`: crear worktree/rama por tarea desde commit base aprobado; lanzar procesos Codex con máximo de concurrencia explícito y guardar IDs. | Dos tareas sintéticas independientes se solapan y cada una conserva su rc, rama, archivos y logs. Sin editar el master activo. |
| P1 | Reservas de rutas sólo locales: en worktrees distintos cada una puede aprobar un escritor incompatible. | `sesiones.py`: registro central del coordinador para reservas y dependencias; integración secuencial. Mantener el límite local de `trabajo.py:assign` documentado. | Dos tareas que reservan la misma ruta no se lanzan a la vez desde el coordinador; probar también directorio frente a archivo. |
| P1 | No hay cola ejecutable con dependencias y recuperación de proceso. | `ejecutor.py`: cola manual inicial con tarea lista/bloqueada y estado de intento ejecutando/fallido/interrumpido; cero reintentos automáticos por defecto. | Caída del proceso deja estado recuperable y requiere revisión antes de repetir. No hace falta activar n8n. |
| P1 | Logs de texto no ofrecen un contrato estable para retomar la sesión exacta. | Runners futuros: `codex exec --json`, salida final separada y extracción validada de session/thread ID; reanudar por ID, no `--last`. | Fallo o ID ausente se registra sin inventar sesión; no se mezcla la tarea A con B. [F6] |
| P1 | QA actual protege registros, pero no prueba el recorrido del nuevo supervisor. | Nuevos tests del ejecutor/sesiones con procesos falsos: timeout, interrupción, colisión, revisión vieja, entrega sin prueba y push fallido. | Ningún rc=0 falso llega a cierre final; un fallo remoto conserva la entrega local pendiente. |
| P1 | Documentación de rutas desfasada respecto al código. | `ORQUESTACION.md`, preparación: reemplazar destinos nuevos `continuidad/tareas` y `continuidad/encargos` por `04-operacion-agentes/tareas` y `encargos`; explicar lectura heredada. Revisar textos restantes de `harness.py`. | Cada ejemplo coincide con `PUBLIC_TASKS`/`PUBLIC_BRIEFS` y se conserva compatibilidad histórica. |
| P2 | Nombre del revisor no autentica identidad y no siempre existe asignación. | `trabajo.py:accept`: registrar responsable/ejecutor y vincular revisión al intento/evidencia; exigir asignación al nuevo flujo. Mantener explícita la limitación de identidad. | Rechazo de autoaceptación por actor declarado; revisión obsoleta bloqueada. No venderlo como autenticación fuerte. |
| P2 | Falta resumen operativo único y comprobable de Boss. | `00-MAPA/ESTADO.md` enlaza tareas abiertas, decisiones activas y siguiente paso; vista breve generada desde registros, sin copiar chats completos. | Sesión nueva continúa una tarea con ID, commit, límites y evidencia, sin depender del chat anterior. |
| P2 | Hay registro de errores, pero no conexión estructurada entre cada intento fallido y su lección. | `registro-de-errores.md` más metadatos del intento: enlazar causa, evidencia y condición para volver a probar. | Un fallo genera referencia recuperable; no dispara otro intento automáticamente. |

## 5. Plan de implementación en pasos

1. **Boss revisa esta propuesta.** Elegir el primer lote y autorizar sus archivos y permisos. No aplicar cambios sobre el master que otra sesión está escribiendo.
2. **Codex alinea reglas y rutas.** Formalizar las reglas exactas de Sergio en la fuente única y corregir el ejemplo de continuidad. Entregar diff para revisión.
3. **Codex conecta una tarea manual al ejecutor.** Primero lectura: ID, revisión, contexto, eventos JSONL, sesión, motivo de parada y evidencia. Conservar el runner actual como modo acotado.
4. **Codex prueba interrupción y retoma.** Proceso falso primero; después una tarea inocua autorizada. Reanudar por sesión exacta o por registro explícito si la sesión no puede recuperarse.
5. **Codex añade dos sesiones aisladas.** Worktrees desde un commit base acordado, reservas centrales, límite dos, integración de una entrega por vez. Boss reparte e integra decisiones; Codex hace el trabajo.
6. **Codex verifica y prepara publicación.** Tests proporcionales y revisión de evidencia. Tras autorización aplicable, publicar mediante el acceso legítimo ya disponible y conservar recibo remoto. Si falla push, estado pendiente de publicación, nunca terminado.
7. **Boss evalúa el piloto antes de ampliar.** Medir tareas aceptadas, fallos, duración y recuperación. Scheduler, gastos, cobros o activación n8n quedan fuera hasta el sí específico de Sergio.

### Registro de esta tarea y límites de cierre

Inicio: encargo recibido el 2026-11-08; arranque local leído y comprobador rc=0. Fin: informe guardado el 2026-11-08. Estado: investigación/auditoría documental entregada para revisión, con lectura parcial declarada de bloques extensos. No es certificación de runtime ni ejecución de tests.

No se modificó el repo ni se hicieron commits/push. Esta entrega permanece sólo en resultados por instrucción expresa; por la regla de Sergio no se declara cierre final en GitHub. No hay reintento automático ni siguiente tarea activada.

# Cómo funcionan los harnesses de agentes hoy, y qué cambiar en el de OnIA

Investigación independiente de Grok Bot (Boss), 8 de noviembre de 2026. No reutiliza el reporte anterior de Codex. Cada link de la sección 6 se comprobó el 8/11/2026. Del repo se leyó solo `origin/master`, en modo lectura, y además `~/operacion/ejecutar.sh` en el VPS.

---

## 1. Qué es un harness, en la práctica

**Un harness es todo lo que rodea al modelo y que no es el modelo:** el bucle que lo hace trabajar, las herramientas que usa, el contexto que recibe, sus permisos, cómo se comprueba que terminó y cómo se pasa el trabajo de una sesión a la siguiente.

- Anthropic presenta el Claude Agent SDK como "un harness de agente de uso general". Lo que agrega encima son las piezas de continuidad: un agente inicializador, un archivo de progreso, la lista de funciones y git ([Anthropic, long-running](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- OpenAI lo explica desde el rol del humano: "Humans steer. Agents execute." Cuando el agente falla, la solución casi nunca es pedirle que se esfuerce más. La pregunta es qué capacidad le falta y cómo hacerla legible y obligatoria ([OpenAI, Harness engineering](https://openai.com/index/harness-engineering/)).
- En la comunidad la fórmula que circula es **agente = modelo + harness**. Varios repiten que cambiar solo el harness movió un agente del puesto 30 al top 5 en Terminal Bench. Es una afirmación de un post de Reddit y no la verifiqué ([r/ai_coder](https://www.reddit.com/r/ai_coder/comments/1uimtgw/agent_harness_engineering/)). Arize lo resume en una frase: el modelo elige el camino, y el runtime controla el contrato, los permisos, la prueba de que terminó y la recuperación ([Arize](https://arize.com/resources/harness-engineering/)).

Para OnIA, el harness tiene tres partes: lo que Codex lee (AGENTS.md y las reglas), lo que lo lanza y lo vigila (`ejecutar.sh`, que hoy está muy limitado) y lo que demuestra que terminó (un commit en GitHub y los tests).

---

## 2. Los patrones que se repiten en los mejores harnesses

### 2.1 El bucle del agente
El modelo recibe contexto, llama una herramienta, ve el resultado y repite. Termina cuando cumple el objetivo o cuando llega a un límite de pasos. Lo importante es que en cada paso obtenga la "verdad del entorno": la salida del comando o el resultado del test, no lo que él supone ([Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). Anthropic recomienda empezar simple y sumar complejidad solo cuando mejora resultados medibles.

En Codex ese bucle ya existe: es `codex exec`. Su salida se puede leer en JSON Lines con `--json`, con eventos como `thread.started` y `turn.completed`. La respuesta final se guarda con `-o`, y una sesión se retoma con `codex exec resume <ID>` ([OpenAI, non-interactive](https://developers.openai.com/codex/noninteractive)).

### 2.2 Contexto y memoria
- **AGENTS.md es un mapa, no una enciclopedia.** OpenAI probó un AGENTS.md gigante y le falló: tapa la tarea, envejece rápido y no se puede verificar. Lo que usa ahora es un AGENTS.md de unas 100 líneas que apunta a `docs/`, con planes activos y completados versionados en el repo ([OpenAI](https://openai.com/index/harness-engineering/); estándar en [agents.md](https://agents.md/); cómo lo carga Codex en [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md)).
- **Lo que no está en el repo no existe para el agente.** Las conversaciones de chat y lo que alguien tiene en la cabeza son invisibles para él ([OpenAI](https://openai.com/index/harness-engineering/)).
- **La compactación sola no alcanza.** Anthropic vio que, aun compactando, la sesión siguiente arrancaba sin saber qué había pasado. Lo resolvió con un archivo de progreso (`claude-progress.txt`), el historial de git y una lista de funciones en JSON, todas marcadas `passes:false` al inicio. Eligió JSON porque el modelo lo pisa menos que un Markdown ([Anthropic, long-running](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents); ver también [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **Cada subagente trabaja con su propio contexto** y devuelve solo un resumen, para no ensuciar la conversación principal ([Claude Code, subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)).

### 2.3 Permisos y sandbox
- `codex exec` corre por defecto en **solo lectura**. Para escribir hay que pasarle `--sandbox workspace-write`, y `danger-full-access` queda solo para entornos aislados ([OpenAI](https://developers.openai.com/codex/noninteractive)).
- Claude Code permite elegir, por subagente, qué herramientas usa (`tools` y `disallowedTools`), su modo de permisos y hooks `PreToolUse` que bloquean comandos peligrosos antes de que corran ([subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents), [hooks](https://code.claude.com/docs/en/hooks)).
- **Un worktree no es un sandbox.** Separa los archivos, pero no la red, los puertos, las bases de datos ni las credenciales ([5sigmas](https://5sigmas.com/en/series/coding-agents-agent-harnesses/02-contexto-workspace-sandboxing-aislamiento/), [git-worktree](https://git-scm.com/docs/git-worktree)).

### 2.4 Pruebas y verificación
- El fallo más común es que el agente declare "listo" sin haber probado el resultado de punta a punta. La solución es darle herramientas para verificar, como un navegador o tests, y marcar algo como hecho solo después de esa prueba ([Anthropic, long-running](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
- OpenAI pasa las reglas a **linters y tests estructurales** con mensajes que le dicen al agente cómo arreglar el problema. Además corre agentes de limpieza periódicos, que llama "garbage collection" ([OpenAI](https://openai.com/index/harness-engineering/)).
- Un dato para tareas sin supervisión: en un ranking de harnesses citado en X, el mejor resuelve el 51,4 % de las tareas por intento, pero solo el 33 % siempre. Por eso conviene prever reintentos y controles ([post](https://x.com/chaumberx/status/2119447602391605754); es un dato de un tercero y no lo verifiqué).

### 2.5 Relevos entre sesiones
La sesión nueva arranca así: `pwd`, lee el progreso y `git log`, corre una prueba básica y recién entonces elige una sola tarea pendiente. Al cerrar, deja un commit con un mensaje descriptivo y actualiza el progreso ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)). LangGraph hace lo mismo con *checkpoints* persistentes por hilo, que permiten retomar después de una caída ([LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)). En Reddit lo dicen claro: guardar la transcripción no alcanza. Al retomar hay que comparar el estado real (HEAD, archivos y procesos) con lo que dice el registro ([r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1ta71n5/how_are_you_actually_running_claude_code_at_scale/)).

### 2.6 Lanzamiento en paralelo
- **Un worktree por tarea.** Pasados 2 o 3 agentes en paralelo, es obligatorio ([r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1ta71n5/how_are_you_actually_running_claude_code_at_scale/)). Claude Code lo trae de fábrica con `isolation: worktree` por subagente, admite hasta 20 subagentes simultáneos y 3 niveles de anidación ([subagents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)). Las herramientas de la comunidad (orca, omux, WorktreeWise) hacen lo mismo con Claude Code y Codex: un worktree por sesión y la revisión de cambios en un panel ([orca](https://x.com/git_bored/status/2119402161096339586), [omux](https://x.com/omuxapp/status/2119431788082630699), [WorktreeWise](https://x.com/WorktreeWise_/status/2119429847189442987)).
- **Los tres tipos de choque** ([5sigmas](https://5sigmas.com/en/series/coding-agents-agent-harnesses/02-contexto-workspace-sandboxing-aislamiento/)):
  1. Archivos y git: se resuelve con un worktree por tarea.
  2. Recursos compartidos (puertos, base de datos, `/tmp`): cada tarea necesita los suyos.
  3. Integración: dos cambios pueden estar bien por separado y romper juntos. Se resuelve integrando de a uno y volviendo a correr las pruebas sobre el resultado.
- **El cuello de botella pasa a ser la revisión humana.** Addy Osmani: *"Your coding agents made you a manager"* ([post](https://x.com/addyosmani/status/2119332146485891501)). Otros: "escalá la revisión antes de escalar agentes" ([post](https://x.com/NinumaK87152/status/2119418460795007109)), y es mejor "dos agentes con worktrees limpios y comprobantes que seis 'ayudando'" ([r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1ta71n5/how_are_you_actually_running_claude_code_at_scale/)).
- **Un caso real de lo que sale mal:** alguien lanzó 5 sesiones con prompts de una línea y recibió un solo merge conflict con cinco autores ([post](https://x.com/Novlyx/status/2119459935801291069)).
- **Patrón orquestador y trabajadores:** un coordinador divide la tarea, delega y junta los resultados ([Anthropic](https://www.anthropic.com/engineering/building-effective-agents), [multi-agent research](https://www.anthropic.com/engineering/multi-agent-research-system)).

### 2.7 Colas y logs
Lo que hay que registrar de cada corrida es qué agente corrió, en qué worktree y rama, con qué herramientas, cómo terminó (bien, con error o esperando aprobación), qué archivos cambió, quién lo verificó y cómo retomarlo ([r/ClaudeCode](https://www.reddit.com/r/ClaudeCode/comments/1ta71n5/how_are_you_actually_running_claude_code_at_scale/)). Las fases deben ser estados tipados con aprobación obligatoria antes de pasar a la siguiente, no simples sugerencias (mismo hilo). Codex ya entrega todo esto en `--json`: el `thread_id`, los comandos, los cambios de archivos y el uso de tokens.

### Referencia: los repos más conocidos
- **[openai/codex](https://github.com/openai/codex):** CLI con `exec`, `resume`, sandbox, MCP ([Codex MCP](https://developers.openai.com/codex/mcp)) y AGENTS.md.
- **[anthropics/claude-code](https://github.com/anthropics/claude-code):** subagentes, hooks, worktrees y memoria por subagente.
- **[Aider](https://github.com/Aider-AI/aider):** un solo agente que hace un commit de git por cambio, así que la historia sirve como registro.
- **[SWE-agent](https://github.com/SWE-agent/SWE-agent):** muestra que la interfaz entre el agente y la computadora (las herramientas) importa tanto como el prompt.
- **[OpenHands](https://github.com/All-Hands-AI/OpenHands):** agente con sandbox en contenedor.
- **[LangGraph](https://github.com/langchain-ai/langgraph):** grafos con estado y checkpoints.
- **[CrewAI](https://github.com/crewAIInc/crewAI):** roles y equipos de agentes.

---

## 3. Errores comunes de los harnesses caseros
1. **Prompts de una línea en paralelo**, sin archivos asignados: terminan en conflictos y en trabajo duplicado.
2. **Varias sesiones en la misma carpeta** o editando el mismo archivo.
3. **Confundir worktree con sandbox:** se aíslan los archivos, pero quedan compartidos la red, los secretos y los puertos.
4. **Aceptar "terminado" sin evidencia.** El agente lo declara antes de tiempo o la sesión siguiente cree que ya estaba hecho ([Anthropic](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)).
5. **Un AGENTS.md o unas reglas gigantes** que se pudren y se contradicen.
6. **Reglas que viven en el chat o en la memoria de un asistente** y no en el repo.
7. **Reglas solo en texto, sin un test o un script que las haga cumplir.**
8. **Timeouts cortos sin checkpoint ni reanudación:** la tarea se corta y se pierde.
9. **No guardar el ID de sesión** y no poder retomarla.
10. **Escalar agentes antes que la revisión:** el humano se convierte en el cuello de botella.
11. **Reintentar igual después de un fallo**, sin cambiar las condiciones.
12. **Dar permisos amplios "para que funcione"** (`danger-full-access` o root) en lugar de dar solo los que hacen falta.

---

## 4. Cómo está el harness de OnIA hoy

Revisé `origin/master` y el VPS.

**Lo que ya está bien:**
- `AGENTS.md` es corto (10 líneas), como recomienda OpenAI.
- `reglas-comunes.md` (47 líneas) es una fuente única de reglas.
- `ORQUESTACION.md` ya pide un escritor único por archivo, worktrees para tareas paralelas e integración en secuencia. También dice que un "terminado" no reemplaza la evidencia.
- `harness.py` y `trabajo.py` llevan las tareas en JSON como fuente de verdad, con su vista en Markdown, revisión esperada y estados `para_revision` y `aceptar`, y tienen tests. Es la misma idea que el JSON de funciones de Anthropic.
- `registro-de-errores.md` (194 líneas) sigue el "ratchet": cada error queda como lección permanente.
- `ejecutar.sh` es muy seguro: usa `flock`, rechaza symlinks, mueve cada tarea por carpetas de estado y lleva `registro.tsv`.

**Lo que falta, que es justo la pieza central del harness:**
1. `ejecutar.sh` corta a los **300 s**, trabaja en **`--sandbox read-only`**, sin red y sin push. Además usa **un lock global**, así que hay una sola tarea a la vez. No guarda el `thread_id` (no usa `--json`), así que no hay manera de retomar con `resume`. Corre con `--skip-git-repo-check` y no tiene directorio de trabajo (`-C`) ni worktree.
2. `harness.py` dice explícitamente que "no crea agentes ni ejecuta". No existe el puente entre un encargo preparado y una sesión lanzada.
3. **No hay archivo de progreso ni lista de entregables con `passes`** por objetivo grande, como el workshop. El estado global está en `ESTADO.md`, que es texto libre.
4. **Codex no tiene MCP:** `~/.codex/config.toml` existe, pero no tiene `mcp_servers`. Ya está anotado como pendiente en `pendientes/codex-conectores.md`.
5. **Las skills no se enlazan** en `.agents/skills`, así que Codex no las descubre solo.
6. **La regla "cerrado = commit en GitHub" está escrita, pero nada la hace cumplir.**

---

## 5. Qué aplicar ya al repo (en orden de prioridad)

| # | Archivo | Cambio | Cómo se prueba |
|---|---|---|---|
| 1 | `05-herramientas/scripts/lanzar.sh` (nuevo; en el VPS se copia a `~/operacion/`) | Un lanzador que por cada tarea: (a) crea `git worktree add -b codex/<id> ~/wt/<id> origin/master`; (b) corre `codex exec -C ~/wt/<id> --sandbox workspace-write --json -o final.md` con timeout configurable (por ejemplo 45 min) y red solo si la tarea la pide; (c) guarda el PID, la rama, el `thread_id` (sacado del evento `thread.started`) y el estado en `~/operacion/sesiones.tsv`; (d) usa un lock **por tarea**, no global; (e) permite como máximo 3 sesiones a la vez. `ejecutar.sh` se deja como está, para tareas de solo lectura. | Lanzar 2 tareas de prueba que escriban archivos distintos. Las dos terminan, cada una en su rama, `sesiones.tsv` tiene 2 `thread_id`, y `codex exec resume <id>` funciona. |
| 2 | `05-herramientas/scripts/cerrar.sh` (nuevo) | Antes de marcar una tarea como hecha, comprueba que la rama exista en `origin` (`git ls-remote`) y que tenga commits nuevos. Recién entonces mueve la tarea a `hechas` y anota el hash. Si no, la deja `para_revision`. Así la regla "cerrado = commit en GitHub" deja de ser solo texto. | Un test en `test_trabajo.py`: una tarea sin push no se puede cerrar y una con push sí. |
| 3 | `04-operacion-agentes/reglas-comunes.md` | Agregar 5 líneas: una tarea por sesión; un worktree por sesión; archivos asignados en el encargo; no se integra a master sin pasar los tests; y "integrar de a una por vez y volver a correr las pruebas después del merge". Las correcciones de hoy van a `registro-de-errores.md`. | Revisión de Sergio. `harness.py doctor` sigue en verde. |
| 4 | `04-operacion-agentes/objetivos/workshop.json` + `progreso-workshop.md` (nuevos) | Lista de entregables del workshop (clase 1, 2, 3 y venta), cada uno con pasos de comprobación y `"passes": false`. Cada sesión lee el progreso y `git log` al empezar, toma un solo entregable y al cerrar actualiza solo `passes` y el progreso. | Una sesión nueva puede decir qué falta leyendo solo esos dos archivos. |
| 5 | `harness.py` | Un subcomando `lanzar ID` que lea el encargo JSON y llame a `lanzar.sh` con su objetivo, sus archivos asignados y su aceptación. Así se unen "preparar" y "ejecutar". | Un test con un `codex` simulado (fake) que compruebe que llega el prompt correcto y que se guarda el `thread_id`. |
| 6 | `AGENTS.md` | Agregar la secuencia de arranque de cada sesión: `pwd`; leer el progreso del objetivo y `git log -20`; correr los tests; elegir una sola tarea. Y al cerrar: commit, push y actualizar el progreso. | Lanzar una sesión y revisar en su JSONL que hizo esos pasos. |
| 7 | `.agents/skills` | Crear los enlaces según `orquestacion.json`. Ya existe `instalar-skills-locales.ps1`; falta su equivalente en bash para el VPS. | `codex` lista las skills de OnIA en una sesión nueva. |
| 8 | `~/.codex/config.toml` en el VPS + `pendientes/codex-conectores.md` | Primer conector: el MCP de n8n, que ya corre en el VPS, solo con herramientas de lectura. La activación sigue bloqueada sin el sí de Sergio. Codex admite MCP por configuración ([docs](https://developers.openai.com/codex/mcp)). X, Notion y Drive quedan para después, por API o con un puente. | `codex mcp list` muestra n8n y una sesión puede listar los workflows sin modificarlos. |
| 9 | Proceso (sin archivo) | Tener como máximo 2 o 3 sesiones en paralelo hasta que la revisión de Sergio no sea el cuello de botella. | Ninguna rama queda más de 1 día sin revisar. |

**Lo primero que haría:** el 1 y el 2 (lanzador y cierre con prueba de commit) y el 4 (progreso del workshop). Con eso, el prompt del workshop que ya tiene Sergio deja de depender de la disciplina del modelo y pasa a depender de scripts.

---

## 6. Fuentes (todas comprobadas el 8/11/2026)

**Documentación oficial y artículos**
- Anthropic, Effective harnesses for long-running agents: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic, Building effective agents: https://www.anthropic.com/engineering/building-effective-agents
- Anthropic, Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic, Multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Claude Code, subagents: https://docs.anthropic.com/en/docs/claude-code/sub-agents
- Claude Code, hooks: https://code.claude.com/docs/en/hooks
- OpenAI, Harness engineering: https://openai.com/index/harness-engineering/
- OpenAI Codex, non-interactive (`codex exec`): https://developers.openai.com/codex/noninteractive
- OpenAI Codex, MCP: https://developers.openai.com/codex/mcp
- OpenAI Codex, AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Estándar AGENTS.md: https://agents.md/
- git-worktree: https://git-scm.com/docs/git-worktree
- LangGraph persistence: https://docs.langchain.com/oss/python/langgraph/persistence

**GitHub**
- https://github.com/openai/codex
- https://github.com/anthropics/claude-code
- https://github.com/Aider-AI/aider
- https://github.com/SWE-agent/SWE-agent
- https://github.com/All-Hands-AI/OpenHands
- https://github.com/langchain-ai/langgraph
- https://github.com/crewAIInc/crewAI

**Foros y análisis**
- Reddit, r/ClaudeCode: https://www.reddit.com/r/ClaudeCode/comments/1ta71n5/how_are_you_actually_running_claude_code_at_scale/
- Reddit, r/ai_coder: https://www.reddit.com/r/ai_coder/comments/1uimtgw/agent_harness_engineering/
- Hacker News, Show HN agent-harness-kit: https://news.ycombinator.com/item?id=48047826
- 5sigmas, aislamiento y worktrees: https://5sigmas.com/en/series/coding-agents-agent-harnesses/02-contexto-workspace-sandboxing-aislamiento/
- Arize, Harness engineering: https://arize.com/resources/harness-engineering/

**X (posts del 7 y 8 de noviembre de 2026)**
- Addy Osmani, "Your coding agents made you a manager": https://x.com/addyosmani/status/2119332146485891501
- 5 agentes en paralelo y un solo merge conflict: https://x.com/Novlyx/status/2119459935801291069
- Escalar la revisión antes que los agentes: https://x.com/NinumaK87152/status/2119418460795007109
- orca (un worktree por agente): https://x.com/git_bored/status/2119402161096339586
- omux: https://x.com/omuxapp/status/2119431788082630699
- WorktreeWise: https://x.com/WorktreeWise_/status/2119429847189442987
- Ranking de harnesses (51,4 % por intento frente a 33 % siempre): https://x.com/chaumberx/status/2119447602391605754
- Orquestación: comunicación, estado compartido, recuperación y verificación: https://x.com/noahseidman/status/2119454649207894523
- Harness, loop y graph: https://x.com/0xWhitemon/status/2119430401701621865

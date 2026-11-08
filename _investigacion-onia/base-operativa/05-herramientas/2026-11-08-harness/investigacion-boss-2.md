# Investigación 2: ¿el harness de OnIA es la forma correcta? (8 nov 2026)

## Veredicto
**Sí, el diseño es correcto y coincide con lo que hacen Anthropic, OpenAI, Cognition y los practicantes.** No hace falta rediseñar nada. Faltan 5 ajustes chicos y baratos, y ninguno obliga a rehacer lo que Codex está construyendo.

## Qué coincide con las prácticas recomendadas
| Pieza del diseño | Lo respalda |
|---|---|
| Coordinadora que reparte y sintetiza (orquestador y trabajadores) | Anthropic «Building effective agents» y el sistema multiagente de Research; Cognition 2026: «manager split, children execute, manager synthesizes» |
| Tarea en JSON con `passes:false` | Anthropic cwc-long-running-agents: «Default-FAIL contract, every criterion starts false» |
| Progreso + git + AGENTS.md al arrancar y cerrar | Anthropic «Effective harnesses»: progress file + git history + commit por sesión; AGENTS.md es el estándar de Codex |
| Una tarea por sesión | Anthropic: «work on only one feature at a time… critical» |
| Worktree + rama por sesión | Claude Code best practices, claude-squad, Conductor, docs de Codex worktrees, r/codex |
| Revisor de solo lectura distinto del ejecutor | cwc-long-running-agents («fresh-context evaluator, no Write/Edit tools»); Cognition: revisor sin contexto compartido encuentra más bugs |
| Máximo 3 en paralelo | Addy Osmani: su techo es «3 a 4 hilos»; Simon Willison: el cuello de botella es cuánto revisa el humano |
| `codex exec --json` en background + `resume <id>` | Docs oficiales de Codex non-interactive: JSONL con `thread.started` y `resume <SESSION_ID>`; dev.to y crowsnest recomiendan retomar por id, no `--last` |
| Merge de a una | r/codex y SyncStaff: el worktree evita pisarse, pero el choque aparece en el merge |
| Brief claro antes de lanzar | Anthropic Research: «objetivo, formato, herramientas, límites»; Osmani: el brief claro te deja alejarte |

## Qué falta o está mal (riesgo concreto)
1. **El revisor de contenido no tiene un test que correr.** A, B, C y D son guiones y textos, no código. Sin una rúbrica escrita, el revisor aprueba cualquier cosa. Riesgo: `passes:true` con clases flojas.
2. **El session id se puede perder.** Si `resume` usa `--last` en lugar del `thread_id` del primer evento JSONL, retoma la sesión equivocada (doc de Codex, dev.to). En openai/codex #11435 se reportó que varios `codex exec` en paralelo se mezclaban la sesión. Está cerrado como «no reproducible» tras reescribir exec, pero muestra el riesgo.
3. **Archivos compartidos entre sesiones.** `workshop.json`, `progreso`, `ESTADO.md` y `registro-de-errores.md` los tocarían A, B y C a la vez: van a chocar en el merge. Issue #60065 (abierto, 7 nov 2026): sesiones que leen archivos de plan compartidos se desvían de su tarea.
4. **Demasiadas sesiones para la decisión humana.** Son 8 sesiones. La coordinadora como sesión de Codex aparte suma costo y contexto sin aportar nada (Cognition: «unstructured swarms are a distraction»). Además Sergio está cansado (Osmani: el límite real es la persona).
5. **Coherencia entre clases.** Las tres clases en paralelo toman decisiones implícitas distintas de tono, nombres y precios (Cognition: «actions carry implicit decisions»). La integradora lo arregla tarde.

## 5 cambios priorizados y baratos
1. **Rúbrica en cada tarea:** agregar `aceptacion` con 4 a 6 criterios verificables (duración ≤ 1,5 h, ejercicio con herramienta gratis, fuente por cada referente, precio Bs 50/150 exacto, sin gimnasio). El revisor los marca uno por uno con evidencia (archivo:línea).
2. **Guardar `thread_id`:** `lanzar` lee el `thread.started` del JSONL y lo escribe en sesiones.tsv. `retomar` usa siempre ese id, nunca `--last`. Agregar `--output-last-message <id>.md` para tener el resumen final.
3. **Un solo escritor de lo compartido:** las sesiones A, B y C escriben solo en su carpeta. `workshop.json`, el progreso, ESTADO.md y el registro de errores los actualiza solo la coordinadora en el cierre. Es una línea en reglas-comunes.md y en el brief.
4. **Coordinadora = Boss (Grok Bot), no una sesión de Codex.** Se elimina la sesión 1, quedan 7 y Sergio sigue hablando con un solo chat.
5. **Hoja de estilo común antes de lanzar A, B y C:** un `00-decisiones.md` corto (público, tono, precios, fechas, nombres) que todas leen. Evita la incoherencia sin cambiar el paralelismo.

Nota: el harness que Codex arma ahora ya sirve. Los cambios 1 a 3 se pueden pedir en el prompt de la coordinadora o como un parche chico; no hace falta relanzar la fase 1.

## Fuentes
(✔ = abierta y leída; ○ = vista en el resultado de búsqueda con su contenido)
1. ✔ https://www.anthropic.com/research/claude-code-best-practices: escritor y revisor separados, 3 o 4 checkouts o worktrees, fan-out headless.
2. ○ https://www.anthropic.com/research/effective-harnesses-for-long-running-agents: inicializador, archivo de progreso, una función por sesión, commit.
3. ○ https://github.com/anthropics/cwc-long-running-agents: contrato Default-FAIL, evaluador de contexto limpio sin escritura, handoff.
4. ○ https://www.anthropic.com/research/harness-design-long-running-apps: planificador, generador y evaluador con umbrales duros.
5. ○ https://www.anthropic.com/research/multi-agent-research-system: orquestador y trabajadores; cómo delegar (objetivo, formato, límites).
6. ○ https://www.anthropic.com/research/building-effective-agents: patrones orchestrator-workers y evaluator-optimizer.
7. ○ https://code.claude.com/docs/en/worktrees: sesiones paralelas con worktrees (doc oficial).
8. ○ https://learn.chatgpt.com/docs/non-interactive-mode: `codex exec --json`, eventos JSONL y `resume <SESSION_ID>`.
9. ○ https://learn.chatgpt.com/docs/developer-commands.md?surface=cli: `exec resume`, `--last`, `--output-last-message` y sandbox workspace-write.
10. ○ https://learn.chatgpt.com/docs/environments/git-worktrees: worktrees gestionados por Codex.
11. ○ https://github.com/openai/agents.md/: estándar AGENTS.md.
12. ✔ https://github.com/openai/codex/issues/11435: varios `codex exec` en paralelo mezclaban sesiones (cerrado, no reproducible tras reescribir exec).
13. ✔ https://github.com/openai/codex/issues/60065: sesiones en el mismo directorio se desvían; la recomendación es worktree e integrador único.
14. ○ https://github.com/openai/codex/issues/8570: pedido de worktrees para agentes paralelos.
15. ○ http://github.com/smtg-ai/claude-squad: tmux + worktree por agente (soporta Codex).
16. ○ https://www.conductor.build/docs/guides/parallel-agents/run-multiple-claude-code-sessions: un workspace (worktree) por tarea, con un prompt acotado.
17. ○ https://www.syncstaff.ai/blog/claude-squad-and-conductor: el aislamiento no evita el choque en el merge (test con Codex).
18. ○ https://gitta.io/guides/parallel-coding-agent-tools: comparación de Conductor, Claude Squad, Vibe Kanban y Container Use.
19. ○ https://dev.to/vibeidedev/codex-exec-execute-codex-non-interactively-in-scripts-and-ci-4g50: retomar por `thread_id`, no `--last`; AGENTS.md.
20. ○ https://crowsnest.app/cli/codex/exec-resume/: guardar el UUID de la sesión y retomar explícito.
21. ✔ https://addyosmani.com/blog/cognitive-parallel-agents/: techo humano de 3 a 4 hilos, sesiones con tiempo fijo y brief con aceptación.
22. ○ https://addyosmani.com/blog/code-agent-orchestra/: qué hace funcionar el multiagente de código.
23. ○ https://simonwillison.net/2025/Oct/5/parallel-coding-agents/: el cuello de botella es la revisión; specs claras.
24. ○ https://news.ycombinator.com/item?id=45489884: hilo de HN sobre agentes paralelos.
25. ○ https://cognition.com/blog/dont-build-multi-agents: las acciones llevan decisiones implícitas.
26. ✔ https://cognition.com/blog/multi-agents-working: la escritura en un solo hilo, un revisor de contexto limpio y el patrón manager map-reduce funcionan; los enjambres no.
27. ○ https://www.reddit.com/r/codex/comments/1uvuh8l/how_do_you_handle_parallel_work_on_the_same/: worktree por tarea, merge en orden y archivos compartidos como fuente de choques.
28. ○ https://help.openai.com/en/articles/20001516-managing-usage-with-gpt-6-astra-in-work-and-codex: ventana de 5 h más límite semanal; revisar `/status`.
29. ○ https://x.com/0xwhrrari/status/2118327478250840140: post en X sobre harness, loop y grafo («el modelo no es lo roto»).

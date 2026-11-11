# Investigación: harness, VPS y homelab para que OnIA opere como empresa de una persona

Fecha: 11 de noviembre de 2026, 19:00 America/La_Paz. Autor: Boss (Grok Bot), por pedido directo de Sergio: «hacé una investigación intensiva sobre cómo trabajan en los harness y que la operación de one man company se haga y que se aproveche el VPS, el harness y el homelab, y desarrollar a toda velocidad y desempeño».

**Qué es y qué no es este documento.** Es investigación y propuesta. No cambia estados del harness, ni reglas, ni el tope de 3 sesiones; no lanza sesiones ni toca el VPS o el homelab. Cada afirmación sobre OnIA va marcada como **observado** (lo vi en el repo en master `f4479eb`), **inferido** (deducción mía) o **propuesto** (requiere decisión o autorización). Todas las fuentes externas se abrieron el 11-nov-2026; los enlaces respondieron al chequeo de ese día.

---

## Resumen para Sergio (leer esto si no leés nada más)

1. **Tu cuello de botella no es la CPU del VPS: es la cuota de Codex y tu atención para aprobar.** Lo dicen OpenAI y Anthropic, y lo confirman nuestras propias mediciones: con 3 sesiones el VPS quedó con unos 9 GiB de RAM libres.
2. **La cuota que no uses antes del 14 se pierde.** La última lectura registrada fue de 18 % usado (11-nov, 15:39 La Paz), con reinicio semanal el 18-nov. Tu plan termina antes de ese reinicio. Conviene que los 3 cupos trabajen sin parar, también de noche, en el lote ya aprobado.
3. **El primer paso que falta es el piloto real del despachador** (`fabrica-codigo-continuidad-lote-20261111`, aceptado con 34 pruebas, pero nunca corrido con sesiones reales). Sin él, alguien tiene que mover cada tarea a mano, y esa persona coordinadora también gasta cuota. Aunque el piloto salga bien, cerrar, aceptar e integrar siguen en manos de la coordinadora. Dejar los cupos trabajando de noche requiere además una coordinadora asignada a esas comprobaciones.
4. **Elegir el modelo correcto multiplica el trabajo.** Según la tabla oficial, Luna rinde unos 20 veces más mensajes que Sol, y Astra unas 3 veces menos. Hoy `onia-llm --nivel pesado` usa Astra (**observado**). Propuesto: Sol para lo pesado, Luna para lo mecánico. En el despachador eso necesita un cambio de código con tests, porque hoy impone Sol.
5. **Hay un agujero de control.** Los agentes de Grok que usan `onia-llm` pueden abrir hasta 3 trabajos *cada uno*, fuera del contador del harness, y es probable que gasten la misma cuenta (**inferido**). Hay que ponerles un tope global y registrarlo.
6. **El homelab sirve para CPU, no para conseguir más Codex.** Úsalo para ASR, FFmpeg, renders, tests y como depósito de crudos. Debe tomar trabajos de una cola del VPS, con límites de CPU y RAM. No es condición para vender.
7. **Pasar de 3 sesiones** se decide con datos: piloto del despachador, cola de revisión al día, cuota medida y, **con tu sí previo**, un ensayo corto de 4 sesiones con paradas automáticas. Después, otro sí para operar con 4, siempre de a una sesión más por vez.
8. **Después del 14:** Codex sigue incluido en los planes Free y Go según la ayuda oficial, con límites sin publicar. El plan es pasar a scripts deterministas, guardar Codex Free para cosas chicas y aceptar Claude pago sólo con tu sí y con plata del workshop.

---

## 1. Qué hace la industria (con fuentes)

### 1.1 Harness = el entorno, no el modelo

- **OpenAI, «Harness engineering» (11-feb-2026).** Tres ingenieros generaron alrededor de un millón de líneas en cinco meses, unos 1.500 PR (3,5 PR por persona por día), sin escribir código a mano. Sus lecciones:
  - El recurso escaso es «el tiempo y la atención humana».
  - Cuando algo falla, se pregunta qué capacidad le falta al agente, no se le pide «esforzate más».
  - El repo es el sistema de registro: un `AGENTS.md` corto (unas 100 líneas) funciona como **mapa**, no como manual, y apunta a `docs/` con planes de ejecución versionados. El «AGENTS.md gigante» fracasó porque desplaza la tarea, se pudre y no se puede verificar.
  - Las reglas se imponen con linters y tests estructurales, cuyos mensajes de error ya traen la instrucción de arreglo.
  - Los revisores son agentes que trabajan en bucle hasta quedar satisfechos («Ralph Wiggum Loop»).
  - Hay una tarea periódica de «recolección de basura» que busca desvíos y abre PR de limpieza chicos.
  - Hay corridas únicas de más de 6 horas, mientras los humanos duermen.
  - https://openai.com/index/harness-engineering/
- **OpenAI, «Unrolling the Codex agent loop» (23-ene-2026).**
  - El harness arma el prompt con instrucciones, herramientas y `AGENTS.md`, que tiene un límite de 32 KiB por defecto.
  - La **caché de prompt** sólo funciona si el comienzo del prompt es idéntico. Cambiar de modelo, de herramientas o MCP, de sandbox o de directorio a mitad de sesión rompe la caché.
  - La compactación automática ocurre al superar un umbral.
  - Con `--oss`, Codex puede usar un modelo local vía Ollama.
  - https://openai.com/index/unrolling-the-codex-agent-loop/
- **Anthropic, «Effective harnesses for long-running agents» (26-nov-2025).** Cada sesión empieza sin memoria. La solución que proponen:
  - Un agente inicializador escribe `init.sh`, un archivo de progreso y una **lista de funciones en JSON, todas en `passes: false`**. Eligen JSON porque el modelo lo sobrescribe menos que Markdown.
  - Cada sesión siguiente avanza **una sola función**, prueba de punta a punta como un usuario (con navegador), hace commit y deja una nota de progreso.
  - Los fallos típicos son declarar victoria antes de tiempo, dejar el entorno roto y marcar como hecho sin probar.
  - https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- **Anthropic, «Harness design for long-running application development» (24-mar-2026).**
  - Usan tres agentes: planificador, generador y **evaluador separado**, que prueba la app con Playwright y criterios explícitos.
  - Un *reset* de contexto con traspaso estructurado evita la «ansiedad de contexto». A medida que el modelo mejora, se quitan piezas del harness.
  - https://www.anthropic.com/research/harness-design-long-running-apps
  - El repo oficial resume tres primitivas: **contrato por defecto FAIL**, **evaluador en contexto limpio sin permiso de escritura** y **traspaso mantenido por el agente** en git. https://github.com/anthropics/cwc-long-running-agents
- **Anthropic, «How we built our multi-agent research system».** Un agente usa unas 4 veces más tokens que un chat, y un sistema multiagente unas 15 veces más. El uso de tokens explica el 80 % de la variación de rendimiento. Lo multiagente conviene sólo cuando el valor de la tarea paga ese gasto. https://www.anthropic.com/engineering/multi-agent-research-system
- **Anthropic, «Effective context engineering for AI agents».** Hay tres técnicas para horizontes largos: compactación, **notas estructuradas** fuera del contexto y arquitecturas multiagente. También recomienda leer archivos «justo a tiempo» (con glob o grep) en vez de cargar todo de entrada. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- **Anthropic, «Building effective agents».** Recomienda preferir flujos simples y deterministas, y agregar autonomía sólo donde mejora el resultado. https://www.anthropic.com/engineering/building-effective-agents
- **Geoffrey Huntley, «Ralph».** Es un bucle de bash que relanza al agente con contexto limpio. Cada vuelta hace una tarea, actualiza el plan compartido, hace commit y sale. https://ghuntley.com/ralph/

### 1.2 Paralelo sin chocar: worktrees, subagentes y revisor

- **Claude Code.**
  - Una sesión por *git worktree* aísla las ediciones; los subagentes pueden llevar `isolation: worktree`. https://code.claude.com/docs/en/worktrees
  - Los subagentes gastan **los mismos límites de uso** que la sesión principal. https://code.claude.com/docs/en/sub-agents
  - Si las tareas tocan los mismos archivos, van en serie; si no, se reparten con un dueño por conjunto de archivos. https://code.claude.com/docs/en/agents
- **Claude Academy (playbook SDLC).** Recomienda empezar con 2 o 3 sesiones: «el techo práctico es cuántas corrientes puede revisar bien una persona; agregá sesiones sólo mientras la revisión acompaña». https://academy.claude.com/courses/ai-native-sdlc-playbook/parallel-sessions-and-subagents
- **Patrón escritor/revisor.** Una sesión escribe y otra, en contexto limpio, revisa sin ver la conversación del escritor. https://code.claude.com/docs/en/best-practices
- **Codex.**
  - `codex exec` corre sin interfaz, en sandbox de sólo lectura por defecto; con `--sandbox workspace-write` puede editar. https://learn.chatgpt.com/docs/non-interactive-mode
  - `--worktree` crea un worktree administrado. https://learn.chatgpt.com/docs/developer-commands
  - Los subagentes vienen activados por defecto y «consumen más tokens que una corrida de un solo agente». https://learn.chatgpt.com/docs/agent-configuration/subagents
  - Base técnica: `git worktree`. https://git-scm.com/docs/git-worktree

### 1.3 Rendir más con la misma cuota

- **Tabla oficial de Codex (Plus), mensajes locales por cada 5 horas:**
  - GPT-6 Astra: 5–45
  - GPT-6.1 Sol: 15–160
  - GPT-6.1 Terra: 35–285
  - GPT-6 Luna: 350–3.000
- **Créditos por millón de tokens de entrada:** Astra 250, Sol 50, Luna 2,5. La entrada en caché cuesta 10 a 20 veces menos.
- **Otros datos de la misma página:**
  - Fast consume 2,5 veces y Ultrafast 8 veces.
  - Puede haber además un límite semanal, cuya cifra no se publica.
  - Para que la cuota dure, recomiendan prompts precisos, menos material fuente, un `AGENTS.md` más chico (o anidado) y menos servidores MCP.
  - https://learn.chatgpt.com/docs/pricing
- **Ayuda oficial.** «Codex is included across ChatGPT plans, including Free and Go», con límites según el plan. Codex Cloud no está incluido en Free ni en Go. Si Codex queda trabado compactando, conviene abrir un chat nuevo con un resumen corto. https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- **Lo que ya no sirve:** el nivel gratis de Gemini CLI para cuentas personales terminó en 2026. No contar con él. https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals
- **Modelo local:** `codex --oss` con Ollama necesita una ventana de contexto de al menos 64k. Por defecto usa `gpt-oss:20b`. https://docs.ollama.com/integrations/codex

### 1.4 VPS más PC de casa: workers remotos seguros

- **Tailscale.**
  - Las etiquetas (*tags*) identifican servidores y las *grants* dicen quién llega a qué puerto. https://tailscale.com/docs/features/tags · https://tailscale.com/docs/reference/syntax/grants
  - Tailscale SSH tiene modo `check` (reautenticación periódica), pero un origen etiquetado no puede usar `check`. https://tailscale.com/docs/features/tailscale-ssh
  - **Serve** publica sólo dentro de la tailnet; **Funnel** publica a Internet. https://tailscale.com/kb/1312/serve
- **Límites de recursos en Linux.** `systemd-run --scope -p CPUQuota=… -p MemoryMax=…` corre un trabajo dentro de un cgroup con tope. `CPUQuota=200%` equivale a 2 núcleos, y `MemoryMax` es un tope duro. https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html · https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html
- **WSL.** `.wslconfig` fija `memory` y `processors` de la VM (por defecto 50 % de la RAM y todos los procesadores), además de `vmIdleTimeout` y `autoMemoryReclaim`. https://learn.microsoft.com/en-us/windows/wsl/wsl-config

### 1.5 Empresas de una persona con IA: qué muestran los casos reales

- **Base44 (Maor Shlomo).** Nació como proyecto de una persona, sin inversión. Llegó a unos 250.000 usuarios y USD 189.000 de ganancia en mayo de 2025, y se vendió a Wix por USD 80 M en efectivo a los 6 meses. **No era 100 % solo:** tenía 8 empleados al vender, casi todos sumados en el último mes. https://techcrunch.com/2025/06/18/6-month-old-solo-owned-vibe-coder-base44-sells-to-wix-for-80m-cash/
- Shlomo dice que pasaba **20–30 % de su tiempo automatizando el negocio en vez de escribir código**, y que en la etapa temprana conviene que una sola persona decida. https://www.calcalistech.com/ctechnews/article/rkogikc9le
- **La lección para OnIA (inferido):** la empresa de una persona funciona cuando el fundador decide y vende, y las máquinas producen y verifican. Crecer en número de bots no es la métrica. Coincide con lo que ya dice CIERRE-VENTA: «Cantidad de bots, pestañas o sesiones no es una medida de que la empresa opere sola».

---

## 2. Diagnóstico del harness de OnIA frente a la industria

### 2.1 Fortalezas (ya estamos donde la industria recomienda)

| Práctica de la industria | En OnIA | Marca |
|---|---|---|
| El repo como sistema de registro; planes versionados | `origin/master` es la verdad; el registro canónico vive en `tareas/*.json` con revisión; los briefings están en `encargos/` | observado |
| Contrato por defecto FAIL; no declarar victoria | Reglas 4 y 5 («NO DEJAR HUECOS»; propuesto ≠ probado ≠ aceptado); «un código de salida cero no prueba entrega» | observado |
| Evaluador independiente en contexto limpio | Un revisor distinto revisa el commit exacto, en un worktree desprendido, sin hijos; veredicto `bueno`/`cambios` | observado |
| Worktree por tarea y rama propia | `codex/ws-<id>`, `../onia-ws-<id>`, un bare por ID (DICTAMEN §3) | observado |
| Traspaso estructurado entre sesiones | Briefing por ID, recibos y evidencias; retoma por SID | observado |
| Bucle finito con lock y diario | El despachador `harness_lote.py` hace un tick finito, con lock, diario de intención y efecto, conciliación por SID y commit, STOP y revocación; 34 pruebas | observado (estado `aceptado`, r38) |
| Medir antes de escalar | Hay una medición de 3 sesiones del 9-nov y un protocolo F1 escrito con paradas por CPU, RAM, PSI y swap | observado |
| Seguridad del worker | Instalador del homelab revisado y endurecido: usuario aislado, sin `/mnt/c`, huella fijada; nunca Funnel | observado |

### 2.2 Huecos

1. **El despachador está aceptado, pero nunca corrió con sesiones reales.** Su `proximo_paso` dice: «Coordinadora ejecuta piloto real… antes de activar recurrencia». Hasta que corra, cada transición la hace a mano una sesión coordinadora, que además gasta cuota (**observado**). Por eso los cupos quedan ociosos de noche o mientras nadie mira (**inferido**).
2. **Hay seis tareas en `para_revision` desde el 10-nov, sin aceptación:** `euge-dos-videos`, `fabrica-automatizaciones-redes-funnels`, `fabrica-edicion-video`, `fabrica-plataforma-mapa`, `guiones-tanda-20261111` y `-v2` (**observado** en `tareas/`). Al menos `guiones-tanda-20261111` ya tiene un dictamen formal `cambios`; las demás hay que revisarlas una por una. La industria limita el paralelo a lo que se alcanza a revisar. Si la cola de revisión crece, subir de 3 no suma (**inferido**). Algunas pueden ya estar superadas por entregas posteriores, y conviene cerrarlas explícitamente (**propuesto**).
3. **`onia-llm` corre fuera del harness.**
   - El nivel `pesado` usa `gpt-6-astra`, el modelo más caro de la tabla.
   - El tope es de 3 trabajos en paralelo **por agente**, no global.
   - No lee ni registra la cuota.
   - (Todo esto **observado** en `onia-llm --help`.)
   - Si comparte la cuenta ChatGPT del VPS, cinco agentes podrían abrir hasta 15 trabajos que no cuentan en el tope de 3 (**inferido**; falta comprobar qué cuenta usa la caja).
4. **El contexto es largo y está disperso.**
   - Tamaños: CIERRE-VENTA ≈ 56 KB, boss-memoria ≈ 26 KB, REGLAS-BOSS ≈ 18 KB, DICTAMEN ≈ 17 KB, reglas-comunes ≈ 12 KB (**observado**).
   - El `AGENTS.md` raíz es corto, de 4 KB (**observado**, bien).
   - OpenAI y Anthropic recomiendan un mapa corto con lectura justo a tiempo. Los documentos largos gastan entrada y caché en cada sesión y mezclan antecedentes con lo vigente (**inferido**).
5. **El registro canónico tiene varios escritores.** Hay commits como «Conserva estado concurrente del harness antes de integrar el lote» y «Conserva estados del harness antes de cerrar visual» (**observado**). Funcionan, pero cada conciliación cuesta tiempo y cuota. Lo recomendado es un único escritor de transiciones, que es lo que ya prevé el despachador (**inferido**).
6. **La cuota se observa a mano.** El despachador exige una observación de menos de 120 segundos, que escribe la coordinadora (**observado**, README del despachador). Sin un lector automático y sin costo de modelo de `/status` o del panel de uso, el bucle se frena por falta de dato (**inferido**).
7. **El homelab todavía no recibe trabajo.**
   - El diagnóstico PE dio `control_pe.ok=true`.
   - La retoma v3 falló en `mounts_safe` por un submontaje de módulos del kernel.
   - La retoma v4 está definida (`f4479eb`), pero falta ejecutarla en la PC, más SSH remoto y la persistencia (**observado**).
   - El 11-nov a las 07:35 la PC figuraba desconectada (**observado** por Boss; puede haber cambiado).
8. **Las pruebas de punta a punta están desparejas.** El panel se probó en navegador, pero falta el acceso desde el teléfono. El WhatsApp real con Meta y el número de Sergio tampoco está probado (**observado** en CIERRE-VENTA). Anthropic remarca que sin herramientas de prueba como usuario (navegador) los agentes marcan como hecho lo que no funciona.
9. **No hay «recolección de basura» periódica.** No existe una tarea chica que revise docs vencidas, fechas viejas (16 archivos con fechas viejas, según Boss) o estados huérfanos (**observado** que falta; **propuesto** crearla).
10. **La atención de Sergio es el recurso más escaso** (**inferido**): ventas, grabaciones y aprobaciones pasan todas por él. Cada pregunta que el sistema le hace sin necesidad le resta velocidad a la empresa.

### 2.3 La capacidad física no es el límite (por ahora)

Medición del 9-nov con 3 ejecutoras en el VPS (**observado**, ESCALADO-CARRILES):
- CPU mediana 43,6 %, pico 90,3 %.
- `MemAvailable` mínimo 9,09 GiB de 15,6.
- Dos de las tres sesiones usaban unos 400 MiB y alrededor de 1 % de CPU; la tercera, que corría herramientas, unos 2,7 GiB y 20 %.

La muestra del 11-nov tenía 10,4 GiB disponibles. **Inferido:** una sesión Codex típica espera al modelo y casi no usa CPU. El VPS probablemente aguanta 4 o 5 sesiones de texto y código. Lo que satura son los trabajos de herramientas (ASR, FFmpeg, npm, builds), y eso es lo que conviene mandar al homelab. Esto **no** autoriza subir el tope: es una hipótesis que hay que medir (§3.5).

---

## 3. Arquitectura recomendada (propuesto)

### 3.1 Qué corre dónde

| Lugar | Rol | Corre | No corre |
|---|---|---|---|
| **VPS (coordinador)** | Cerebro operativo, siempre encendido | Registro canónico y único escritor de transiciones; despachador (tick finito); hasta 3 sesiones Codex (ejecutoras y revisora); panel privado; adaptador de WhatsApp; n8n (inactivo hasta tu sí); lector de cuota | Renders largos ni ASR pesado en paralelo con 3 sesiones |
| **Homelab DESKTOP-0GGGNMF (worker de CPU)** | Músculo, cuando esté aceptado | ASR (faster-whisper int8), FFmpeg, renders, tests y builds pesados; depósito de crudos fuera de Git; más adelante, pruebas de modelo local | Bots, secretos de producción, registro canónico, sesiones que cuenten como «más Codex» |
| **Caja de Grok (Boss y agentes)** | Coordinación, ventas, calendario, conectores | Boss coordina y revisa; Contenido edita; Calendario agenda; `onia-llm` para textos cortos, con tope global | Repo grande, tareas con revisor (eso va por el puente) |
| **Teléfono de Sergio** | Decisiones | Panel privado: aprobar, corregir, mirar bloqueos | Copiar mensajes entre agentes |

### 3.2 Carriles paralelos sin tocar los mismos archivos

Cada carril tiene un **dueño exclusivo de rutas**. Las rutas exactas se fijan en la asignación de cada ID en el registro; esta tabla sólo orienta. Un carril puede tener varias tareas en el tiempo, pero sólo una ejecutora viva por vez.

| Carril | Rutas (dueño exclusivo) | Ejemplos de tareas |
|---|---|---|
| A · Venta y contenido | `05-herramientas/fabrica-onia/1-guiones-calendario/salida/`, `01-negocio/workshop-*` (textos) | Guiones de las 18:00, corrección de fechas, materiales de las clases |
| B · Panel y cerebro | rutas del panel y del cerebro asignadas en `cerebro-panel-usable-20261109` (sólo B modifica la interfaz); `05-herramientas/fabrica-onia/6-plataforma/` si se asigna. No `06-plataforma/`, que es del producto separado | Acceso desde el teléfono, bandeja de operador |
| C · Chatbot y automatizaciones | `05-herramientas/fabrica-onia/3-automatizaciones/`, `05-herramientas/fabrica-onia/4-chatbot-whatsapp/` | Ensayo real de WhatsApp, Meta |
| D · Harness | `05-herramientas/scripts/`, `05-herramientas/fabrica-onia/5-codigo/` | Piloto del despachador, lector de cuota, tope global de `onia-llm` |
| E · Homelab | `04-operacion-agentes/homelab/` | Retoma v4, SSH, cola de CPU |
| — · Documentos compartidos | DECISIONES, BITACORA, ESTADO | **Un solo escritor:** la coordinadora (Boss para sus notas) |

Reglas de los carriles:
- Una tarea no toca rutas de otro carril. Si hace falta, se parte en dos tareas con dependencia.
- El despachador ya valida que el diff completo caiga dentro de las rutas asignadas (**observado**, README).

### 3.3 Revisor y composición de los 3 cupos

- La composición preferida es **2 productoras + 1 revisora rotativa**, como ya proponen ESCALADO-CARRILES y CIERRE-VENTA.
- **La revisión tiene prioridad:** no se lanza una productora nueva si hay una entrega esperando revisor y un cupo libre.
- **Revisor barato cuando alcanza.** Si los tests hablan solos, la revisión va con Sol low o Luna. Si toca secretos, n8n, dinero o seguridad, con Sol high. Nunca Astra ni Ultrafast sin tu sí.
- **Contrato FAIL por tarea**, al estilo Anthropic. La aceptación es una lista de criterios verificables, todos `false` hasta que haya evidencia. El revisor no tiene escritura.

### 3.4 Despachador y cuota: la palanca de velocidad

Pasos en orden:

1. **Piloto real ya** (D): dos IDs del lote aprobado con rutas distintas, siguiendo `ENSAYO-COORDINADORA.md`. El criterio para pasar es cero lanzamientos duplicados, rutas respetadas y trazabilidad hasta `origin/master`.
2. **Coordinadora asignada a cierres.** El piloto no automatiza cerrar, aceptar ni integrar (README del despachador, «acciones de coordinadora»). Para avanzar de noche, una sesión coordinadora tiene que hacer esas comprobaciones, o las entregas quedan esperando hasta la mañana sin bloquear lo independiente.
3. **Lector de cuota sin modelo** (D): un script que escribe la observación privada (fecha, % restante, proveedor) leyendo el estado del CLI o del panel de uso, sin abrir un chat. Si no se puede leer, el despachador frena, como ya está diseñado.
4. **Tick recurrente acotado**, como `systemd` timer en el VPS y no como rutina de sondeo de Grok. Corre cada pocos minutos con retroceso, sólo dentro de la vigencia del manifiesto, y se detiene al vaciarse el lote. **Requiere tu sí explícito** (regla 12 y DICTAMEN).
5. **Ruteo por modelo** (requiere un cambio de código en `harness_lote.py` con tests y revisión, porque hoy el perfil impone `gpt-6.1-sol` low/high):
   - Luna para lo mecánico: fechas, enlaces, formatos, verificaciones.
   - Sol low para lo normal.
   - Sol high para diseño o fallos difíciles.
   - Cero hijos.
   - Mantener prompts estables (mismo modelo, mismas herramientas y MCP durante la sesión) para aprovechar la caché.
6. **Tope global de `onia-llm`** (es un script de la caja compartida de Grok, fuera del repo; lo cambia Boss con tu sí, no el carril D): un semáforo único para todos los agentes de la caja (por ejemplo, 2 trabajos), con cuota registrada en cada trabajo y `pesado` → Sol high en vez de Astra.
7. **Métricas en el panel:**
   - Entregas aceptadas por punto de cuota.
   - Minutos que pasan entre que se libera un cupo y se despacha la siguiente tarea.
   - Tareas que vuelven con `cambios`.
   - Tamaño de la cola de revisión.

### 3.5 Cómo subir de 3 sesiones midiendo (propuesto, requiere tu sí)

Compuertas, en orden. Si una falla, se queda en 3.
1. El despachador pasó el piloto real.
2. La cola de revisión tiene como mucho 1 entrega pendiente durante 24 horas: la revisión acompaña.
3. Hay cuota medida que alcanza para el lote más una reserva de revisión (dato fresco, no estimado).
4. **Tu sí para el ensayo**, que es una autorización específica distinta de operar con 4. Primero se repite una medición comparable con 3 sesiones y después un ensayo corto en el VPS: **4 sesiones durante 20 minutos**, usando las paradas ya escritas en F1 (CPU media de 60 s > 75 %, RAM disponible < 20 %, PSI, swap con presión, OOM). Muestras cada 5 s y recibo publicado.
5. Otro sí tuyo para operar. Se sube **+1** (a 4), se opera un día y recién después se evalúa 5.

El homelab aporta CPU para que los trabajos de herramientas no le roben al VPS. No aporta cuota.

### 3.6 El homelab como worker (propuesto, cuando esté aceptado)

- **Modelo «pull».** El VPS deja trabajos de CPU en una cola (archivo o directorio de trabajos con lock). El worker los toma por la ruta SSH vía Tailscale ya diseñada, los corre y devuelve resultados y recibos. Si la PC se apaga, el trabajo vuelve a la cola tras conciliar, sin rehacer lo publicado.
- **Aislamiento.**
  - Usuario `onia-worker` sin `/mnt/c`, con huella fijada, como ya hace el instalador.
  - Etiqueta Tailscale para el worker y una *grant* que sólo permita al VPS llegar a su puerto SSH.
  - Serve sí, Funnel nunca.
- **Límites.**
  - `.wslconfig` con `memory` de unos 10 GB y `processors` en 8, para que Windows siga usable.
  - Cada trabajo corre con `systemd-run --scope -p CPUQuota=600% -p MemoryMax=6G` y `nice`.
  - Un solo trabajo pesado por vez al principio; se mide antes de sumar otro.
  - Sin `--no-sandbox` ni cambios de AppArmor o userns (regla 10).
- **Prioridad:** no bloquea la venta. La edición sigue en el VPS hasta aceptar el worker.

---

## 4. Plan priorizado

### 4.1 Próximas 48 horas, hasta el sábado 14 (venta primero)

Horarios en America/La_Paz. Las clases son las de la confirmación más reciente en `DECISIONES-SERGIO-20261110.md`: **vie 13 20:00, sáb 14 14:00, lun 16 20:00**. Los eventos de Meet en Calendar todavía muestran el horario anterior (**observado** por Boss) y hay que alinearlos.

| Cuándo | Qué | Quién | Por qué primero |
|---|---|---|---|
| Mié 11, noche | NEGOCIO ya está decidido: responde la automatización (DECISIONES, 10-nov). Falta tu sí para activarla y probarla, resolver el choque de agenda del viernes, alinear Calendar y dar el sí para abrir la venta | Sergio (5 min) + Boss/Calendario | Sin esto no se vende; no gasta Codex |
| Mié 11, noche | **Piloto real del despachador** con dos IDs del lote. Si pasa, dejar los cupos trabajando de noche en el lote aprobado, con la coordinadora haciendo cierres, aceptación e integración | Codex coordinadora (D) | Convierte la cuota que se pierde el 14 en entregas |
| Mié 11, noche | Corregir las fechas viejas de los 16 archivos (Luna o Sol low) y los textos de reembolso cero, VIP lleno y pago vencido | Carril A + revisión de Contenido | Riesgo comercial directo |
| Jue 12, mañana | Tope global y modelo de `onia-llm` (Astra → Sol), en la caja; lector de cuota, en el repo | Boss (caja) + carril D (Sol low) | Evita quemar cuota a ciegas |
| Jue 12, mañana | Revisar o cerrar las 6 tareas en `para_revision` (aceptar, pedir cambios o marcar superada con evidencia) | Revisora rotativa + coordinadora | Libera la cola; requisito para escalar |
| Jue 12 | Ensayo real de WhatsApp sólo con el número de Sergio; acceso al panel desde el teléfono | Carriles C y B; Sergio prueba | «Conectado no es listo» |
| Jue 12, 18:00 | Tanda de 5 guiones lista (hora confirmada) | Carril A | Contenido diario |
| Jue 12–vie 13 | **VSL (video de venta)**, anuncios y materiales de las clases 1, 2 y 3; ensayo de la clase 1. Sin promesas ni testimonios inventados; Sergio graba y decide qué se publica | Carril A / encargo de marketing (C de CIERRE-VENTA) + Contenido + Sergio | Prioridad en el primer cupo libre (CIERRE-VENTA); la clase del lunes 16 no puede depender de Codex |
| Cuando la PC esté online y la guía v4 esté publicada y revisada | Retoma v4 del homelab. Hoy existe sólo el encargo (`ENCARGO-RETOMA-MONTAJE-v4`); la guía, el archivo y el hash los entrega Codex. Se corre con tus tarjetas | Codex (guía) → Boss + Sergio (ejecución) | Independiente de la venta |
| Vie 13–sáb 14 | **Paquete de continuidad** (§4.2): scripts sin modelo con tests, estado de cada ID, registro de errores, `AGENTS.md` como mapa | Carril D + coordinadora | Lo que sobrevive al 14 |
| Sáb 14 | Última lectura de cuota y cierre ordenado: nada queda «ejecutándose» sin dueño | Coordinadora | Evita trabajo huérfano |

### 4.2 Continuidad después del 14 sin Codex pago (propuesto)

1. **Primero lo determinista.** Todo lo que se repite pasa a scripts, n8n o al despachador sin modelo: guiones con plantilla, recordatorios, el panel, ASR y FFmpeg en el VPS u homelab. Es la recomendación de «Building effective agents» y la de CIERRE-VENTA: «Lo que debe sobrevivir al 14».
2. **Codex Free o Go.** La ayuda oficial dice que Codex está incluido en esos planes, con límites que no se publican y sin Codex Cloud (**observado** en la fuente). El 15-nov hay que medir con `/status` qué queda y qué modelos aparecen; no prometer capacidad antes de medirla. Si queda algo, usarlo sólo para revisión y arreglos chicos, con el harness igual y el tope en 1.
3. **Grok (Boss y Contenido) como productores de texto.** Contenido escribe los guiones desde el 14 (decidido por Sergio). Boss coordina y revisa con el mismo protocolo.
4. **Modelo local en el homelab, sólo para pruebas.** `codex --oss` con Ollama pide al menos 64k de contexto y usa `gpt-oss:20b` por defecto (fuente arriba). Con 16 GiB de RAM, sin GPU útil y WSL, un modelo así probablemente es lento o no entra (**inferido**). Sirve, como mucho, para clasificar o resumir con modelos chicos, de noche. Hay que medirlo antes de contar con él.
5. **Claude pago (plan B ya decidido)** sólo con tu sí explícito. Regla propuesta: que lo pague el ingreso del workshop, no deuda. El harness y el panel no cambian; sólo cambia el ejecutor.
6. **No contar con Gemini CLI gratis:** ese nivel terminó (fuente arriba).

---

## 5. Riesgos

| Riesgo | Señal | Mitigación |
|---|---|---|
| Se agota la cuota semanal antes del 14 (el límite semanal no se publica) | `restante` baja rápido en las lecturas | Luna para lo mecánico, revisores baratos, nada de Astra o Fast; el despachador frena sin dato fresco |
| La cuota sobra y se pierde el 14 | Cupos ociosos de noche | Piloto del despachador hoy; lote aprobado listo para encolar |
| Doble despacho o estados pisados en el JSON | Commits de «conservar estado concurrente» | Un único escritor (despachador); `onia-llm` no toca el repo canónico |
| La revisión se atrasa y el paralelo sólo acumula | Más de 1 entrega esperando revisor | Prioridad de revisión; no subir de 3 |
| Agentes de Grok gastan Codex sin control | Trabajos de `onia-llm` en varios agentes | Semáforo global y registro de cuota por trabajo |
| Fuga de secretos, IPs, QR o medios en Git | Diff con rutas privadas | Regla 9; revisor lo chequea; datos privados en el VPS y en el disco del homelab |
| El homelab expone Windows o se abre a Internet | Funnel activo o `/mnt/c` visible | Serve sí y Funnel nunca, *grants* por etiqueta, el CHECK del instalador; no aceptar sin probar el aislamiento |
| La PC se apaga a mitad de un trabajo | Trabajo sin recibo | Cola «pull» con conciliación; nada crítico de la venta depende de la PC |
| Contexto inflado: sesiones caras y desorientadas | Docs de más de 20 KB leídos completos | `AGENTS.md` como mapa; leer por secciones; separar lo vigente de los antecedentes |
| Calendar y decisiones desalineados | Meet con horario viejo | Calendario corrige con tu sí y relee el evento |
| Sobrecarga de Sergio | Preguntas repetidas | Pedir sólo decisiones imprescindibles, agrupadas, desde el panel |
| «Conectado» presentado como «listo» | Afirmaciones sin recibo | Reglas 5 y 11: evidencia por entorno |
| Después del 14 no hay modelo fuerte | Sin cuota el 15 | Paquete de continuidad, Free medido, plan B con tu sí |

---

## Fuentes (abiertas el 11-nov-2026)

- OpenAI · Harness engineering — https://openai.com/index/harness-engineering/
- OpenAI · Unrolling the Codex agent loop — https://openai.com/index/unrolling-the-codex-agent-loop/
- OpenAI · Codex pricing y límites — https://learn.chatgpt.com/docs/pricing
- OpenAI · Using Codex with your ChatGPT plan — https://help.openai.com/en/articles/11369540-using-codex-with-your-chatgpt-plan
- OpenAI · Non-interactive mode — https://learn.chatgpt.com/docs/non-interactive-mode
- OpenAI · Developer commands (worktree) — https://learn.chatgpt.com/docs/developer-commands
- OpenAI · Subagents — https://learn.chatgpt.com/docs/agent-configuration/subagents
- Anthropic · Effective harnesses for long-running agents — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Anthropic · Harness design for long-running application development — https://www.anthropic.com/research/harness-design-long-running-apps
- Anthropic · cwc-long-running-agents — https://github.com/anthropics/cwc-long-running-agents
- Anthropic · Multi-agent research system — https://www.anthropic.com/engineering/multi-agent-research-system
- Anthropic · Effective context engineering — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic · Building effective agents — https://www.anthropic.com/engineering/building-effective-agents
- Claude Code · Worktrees — https://code.claude.com/docs/en/worktrees
- Claude Code · Subagents — https://code.claude.com/docs/en/sub-agents
- Claude Code · Run agents in parallel — https://code.claude.com/docs/en/agents
- Claude Code · Best practices — https://code.claude.com/docs/en/best-practices
- Claude Academy · Parallel sessions and subagents — https://academy.claude.com/courses/ai-native-sdlc-playbook/parallel-sessions-and-subagents
- Geoffrey Huntley · Ralph — https://ghuntley.com/ralph/
- Git · git-worktree — https://git-scm.com/docs/git-worktree
- Ollama · Codex CLI — https://docs.ollama.com/integrations/codex
- Tailscale · Tags — https://tailscale.com/docs/features/tags
- Tailscale · Grants — https://tailscale.com/docs/reference/syntax/grants
- Tailscale · SSH — https://tailscale.com/docs/features/tailscale-ssh
- Tailscale · Serve — https://tailscale.com/kb/1312/serve
- systemd · resource-control — https://www.freedesktop.org/software/systemd/man/latest/systemd.resource-control.html
- systemd · systemd-run — https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html
- Microsoft · WSL config — https://learn.microsoft.com/en-us/windows/wsl/wsl-config
- Google · Gemini Code Assist consumer accounts (fin del nivel gratis) — https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals
- TechCrunch · Base44 vendida a Wix — https://techcrunch.com/2025/06/18/6-month-old-solo-owned-vibe-coder-base44-sells-to-wix-for-80m-cash/
- Calcalist · Shlomo sobre el camino solo — https://www.calcalistech.com/ctechnews/article/rkogikc9le

## Fuentes internas leídas (master `f4479eb`)

REGLAS-BOSS.md, reglas-comunes.md, boss-memoria.md, DICTAMEN-HARNESS-Y-SESIONES-BOSS-v1.md, `05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md`, `DECISIONES-SERGIO-20261110.md`, `homelab/RETOMA-PE-20261111.md`, `homelab/ENCARGO-RETOMA-MONTAJE-v4-20261111.md`, `homelab/F1-MEDICION.md`, `05-herramientas/2026-11-08-harness/ESCALADO-CARRILES-PROPUESTA.md`, `05-herramientas/fabrica-onia/5-codigo/continuidad-lote-20261111/{README,ENSAYO-COORDINADORA}.md`, `tareas/*.json` (sólo lectura de estados) y `encargos/fabrica-codigo-continuidad-lote-20261111.md`.

## Revisión de este documento

Revisión independiente de sólo lectura, hecha con `onia-llm --motor codex --nivel liviano` (Sol) el 11-nov-2026, alrededor de las 19:20 La Paz. Aportó 9 observaciones y las 9 se corrigieron:
- Una de las tareas en `para_revision` ya tenía dictamen `cambios`.
- NEGOCIO ya estaba decidido.
- Faltaba decir que la coordinadora sigue haciendo cierres e integración.
- Luna exige cambiar el código del despachador.
- El ensayo de 4 sesiones requiere un sí previo.
- Había rutas de carril inexactas.
- La guía v4 todavía no existe.
- Había datos personales de más.
- Faltaba el VSL en el plan.

Cuota consumida por esa revisión: no medida (unknown). Este documento no es un veredicto del harness ni una aceptación.

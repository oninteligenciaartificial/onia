# Propuesta: ¿hace falta un Jefe de Codex?

9 noviembre 2026 · ~17:00 America/La_Paz · investigación pedida por Sergio. Solo lectura y documentación. Sin secretos, IPs, claves ni cookies. No se crearon agentes, rutinas ni archivos de handoff.

Autor: Boss (Grok Bot), a pedido de Sergio: investigar la documentación de Grok Bot y definir si, para manejar a Codex, hace falta «un jefe más» o «un agente más», porque percibe que Boss entiende peor las cosas y no tiene contexto suficiente. También pidió cómo dividir el trabajo de Boss, cómo usar la cuota de Grok y para qué, tomando a Euge Oller como una forma de ver las cosas, no como fuente final.

## Veredicto corto

**No conviene crear ahora un agente nuevo llamado «Jefe de Codex».** El problema que señalás (que Boss entiende peor y le falta contexto) no se arregla con otro Grok Bot:

1. **Un agente extra no elige un modelo más capaz.** La documentación oficial dice que no hay selector de modelo: Grok Bot elige el backend por tarea y el usuario no puede enrutar hacia ni lejos de un modelo concreto. Crear «Jefe» no le da a OnIA un LLM distinto del de Boss.
2. **Lo que sí falta es contexto escrito y un puente operativo**, no un tercer capataz. Eso se arregla con archivos en GitHub (un estado corto + la cola de pedidos ya propuesta) y con el coordinador del harness, que ya gestiona las sesiones de Codex.
3. **Sumar un agente gasta cuota.** Cada respuesta de un Bot cuenta, también las de un group chat y los mensajes entre Bots.

La forma que encaja con Euge, con las docs de Grok Bot y con Anthropic/OpenAI es esta: **vos hablás con un solo capataz (Boss)**; Boss reparte a los compañeros que ya existen; **Codex + el harness + el HOMELAB son las fábricas**; GitHub es la memoria compartida. Si un día se acaba la cuota de Grok, Codex sigue solo con lo ya escrito en el repo.

## Cómo se investigó

| Fuente | Qué se leyó | Estado |
| --- | --- | --- |
| Documentación local del box | `/home/box/reference/app-ui.md` y `debugging-the-box.md` (únicos archivos en esa carpeta) | Verificado |
| Docs oficiales de Grok Bot | [Overview](https://docs.x.ai/grok-bot/overview), [How Grok Bot works](https://docs.x.ai/grok-bot/how-grok-bot-works), [Create and manage Bots](https://docs.x.ai/grok-bot/bots), [Message and collaborate](https://docs.x.ai/grok-bot/chat-and-collaboration), [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations), [FAQ](https://docs.x.ai/grok-bot/faq), [cursor.com/docs/grok-bot](https://cursor.com/docs/grok-bot), [Grok Bot on The X Subscription](https://docs.x.ai/x-subscription/grok-bot), [Pricing](https://docs.x.ai/x-subscription/pricing), [Usage limits](https://docs.x.ai/x-subscription/usage-limits) | Verificado (páginas públicas, 9 nov 2026) |
| Uso de esta cuenta | Informe de uso de esta semana, leído en este turno | Verificado en el momento de la lectura; los porcentajes cambian |
| Videos de Euge | Notas ya publicadas [EUGE-VIDEO-BOSS-20261109.md](EUGE-VIDEO-BOSS-20261109.md) y [EUGE-VIDEO2-BOSS-20261109.md](EUGE-VIDEO2-BOSS-20261109.md); cotejo puntual de subtítulos automáticos `es-orig` (no se republica la transcripción) | El contenido hablado sale de subtítulos automáticos: tiempos y nombres pueden deformarse |
| Prácticas externas | [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (Anthropic, 19 dic 2024), [When to use multi-agent systems](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them), [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) (OpenAI), [Iterating development workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex) | Verificado |
| Repo `oninteligenciaartificial/onia` master | [ORQUESTACION.md](ORQUESTACION.md), [boss-memoria.md](boss-memoria.md), [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md), [pendientes/codex-conectores.md](pendientes/codex-conectores.md), [AUDITORIA-ORQUESTACION-20261109.md](AUDITORIA-ORQUESTACION-20261109.md) | Verificado al leer master |

No se tocó el VPS ni la PC. No se crearon agentes, rutinas, `CONTEXTO-BOSS.md` ni `cola-boss.md`.

## Qué dice Grok Bot de sí mismo (verificado vs no)

### Verificado en docs oficiales o en la app

- **Bot primario frente a Bots con un trabajo.** El Bot primario es el punto de contacto y **coordina a los demás**. La guía es empezar el trabajo nuevo ahí. Conviene dar un Bot propio cuando el pedido se repite y tiene **fuentes, reglas o calendario propios**. Un Bot con un solo trabajo acumula mejor memoria para ese trabajo. Fuentes: [How Grok Bot works](https://docs.x.ai/grok-bot/how-grok-bot-works), [Create and manage Bots](https://docs.x.ai/grok-bot/bots).
- **Memoria por Bot, no compartida entera.** Cada Bot guarda preferencias, reglas y un registro de su trabajo. Lo compartido entre todos es poco (nombre y zona horaria). Los archivos, las sesiones del navegador y los handoffs sí mueven contexto. La memoria **no es fuente de verdad** para números que cambian: hay que consultar la fuente. Fuente: [What a Bot remembers](https://docs.x.ai/grok-bot/bots#what-a-bot-remembers).
- **Un solo ordenador compartido.** Todos los Bots de la cuenta usan el mismo ordenador en la nube (archivos, sesiones, terminal). Cada Bot tiene su propia pantalla. No sirven como frontera de seguridad entre sí. El box local de referencia (`app-ui.md`) coincide: Settings → Computer habla de las máquinas registradas y de recuperar **el** ordenador del Bot, no uno por agente.
- **Handoffs y group chats.** Un Bot puede mandar un mensaje asíncrono a otro; el receptor se despierta, trabaja y puede responder después. Un group chat admite de dos a seis Bots. Sirve cuando hay un resultado compartido y hay que ver los pases. Hay que nombrar **un dueño por etapa**. Las peticiones de aprobación, secretos y borradores de correo/Slack **no aparecen en un group chat**. Fuente: [Message and collaborate](https://docs.x.ai/grok-bot/chat-and-collaboration).
- **Cada respuesta gasta uso.** «Every Bot reply counts toward your usage, including replies in a group and messages between Bots, so fewer Bots in a group means fewer replies.» Fuente: la misma página.
- **Skills y routines.** Una skill describe cómo hacer una tarea y se comparte entre tus Bots (biblioteca privada). Una routine le dice a **un** Bot cuándo correrla (horario o evento: Slack, GitHub, correo del Bot, webhook, etc.). El consejo oficial es: hacer la tarea una vez, volverla skill y recién después automatizarla. Cada corrida gasta uso; un horario muy frecuente o un trigger amplio «can use a week of usage in a day». Un Bot puede tener hasta 50 routines. Fuente: [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations).
- **No se elige el modelo.** «Can I pick the model? No. Grok Bot picks the model for each task, and there is no model picker.» Puede ser un modelo de primer partido o de un proveedor de la lista de subencargados, y puede cambiar de un pedido a otro. Las vistas de uso lo anotan como uso de Grok Bot, no por modelo. «How fast you use your usage depends on the kind of work you give Grok Bot and how much effort each task takes.» Fuente: [FAQ](https://docs.x.ai/grok-bot/faq). En la interfaz local (`app-ui.md`) el panel de un agente permite nombre, título, descripción y notificaciones; no hay selector de modelo.
- **Trabajo de código a Cloud Agents.** La página [How Grok Bot works](https://docs.x.ai/grok-bot/how-grok-bot-works) dice que los Bots pueden pasar trabajo de código a Cursor Cloud Agents y adjuntar el resultado. Eso no sustituye a Codex en el VPS ni en el HOMELAB: esas máquinas y esa cuota son el circuito que OnIA ya eligió para fábricas.
- **Plan y cuota.** El informe de uso de este turno muestra plan **Premium**. La lista oficial de [Pricing](https://docs.x.ai/x-subscription/pricing) pone Premium en USD 30 al mes (precio de lista) y dice que Grok Bot está incluido en Premium, Super y Ultra. El uso de Grok Bot sale de la **piscina semanal compartida** con las otras apps del plan (Grok y Cursor), no de un pozo aparte. Super y Ultra tienen un multiplicador de uso incluido más alto (la tabla oficial: Premium 4x, Super 15x, Ultra 50x; no se inventan tokens absolutos). Fuente también: [Grok Bot on The X Subscription](https://docs.x.ai/x-subscription/grok-bot).
- **Qué pasa si se acaba la cuota semanal.** El FAQ: si se termina el límite semanal, el uso extra sigue solo si hay créditos adicionales / on-demand habilitado y no se alcanzó el tope mensual; si está apagado o en el tope, Grok Bot no puede responder, correr routines ni empezar trabajo en su ordenador hasta el reset. El tope no detiene una corrida a mitad: una tarea en curso puede pasarse un poco. Fuente: [FAQ](https://docs.x.ai/grok-bot/faq) («How do I stop charges after my weekly usage runs out?»).

### No verificado / no afirmar

- Qué modelo concreto atendió un mensaje de Boss o de un compañero (la app no lo muestra).
- Cuánto gastaría, en porcentaje, un agente «Jefe de Codex» o una routine concreta: el informe de uso no predice ahorros ni costos futuros.
- Que Boss «tenga un LLM peor» que Codex como hecho técnico. Lo que sí está documentado es que Codex corre en otra suscripción, con selector de modelo propio, y que Grok Bot no deja elegir el suyo.
- Capacidades que no figuren en las páginas citadas o en `/home/box/reference/`.

## Qué enseña Euge (y qué no)

Fuente primaria: subtítulos `es-orig` y las notas ya publicadas. Euge no es la autoridad final; coincide en varios puntos con las docs oficiales y con Anthropic/OpenAI.

Del primer video ([Así Utilizo los Agentes de IA a Diario](https://www.youtube.com/watch?v=JuAQILH7dkQ), ~[12:46–13:16](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=766s)):

- Trabaja con Grok Bot.
- El diseño que le parece correcto es **un agente capataz que dirige subagentes**. Lo que más sentido tiene, dice, es **hablar solamente con un agente**.
- Ese capataz tiene conectores, routines y un ordenador virtual ligero.
- Grok, detrás de Grok Bot, «aún no es suficientemente buena» para algunas tareas (él pone la edición como ejemplo). Para eso monta **fábricas en otro ordenador persistente**, con otros modelos.
- Hay que pedirle **al propio Grok Bot** que ayude a montar esas fábricas (~[19:20–19:27](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1160s)).
- En la fábrica de código, el PR «pone que lo reviso yo, pero en el fondo» Grok Bot le ayuda a revisarlo (~[23:52–24:05](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1432s)).
- Las fábricas existen sobre todo para los flujos que Grok Bot todavía no hace bien, porque hacen falta otros modelos (~[28:41–28:52](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1721s)).

Del segundo video ([Dame 25 minutos…](https://youtu.be/xPJbP9yZE1I)):

- Hablarle al modelo no lo reentrena; si «se acuerda», es contexto inyectado.
- La palanca ya no es el prompt perfecto, sino el **contexto** (ejemplos que sí funcionaron, criterio, historial). Cargar documentos que no tienen que ver solo hincha el contexto.
- El **arnés** es esa capa de memorias, instrucciones, herramientas y, si hace falta, recuperación. Conviene que sea **simple**. Hay que guardarlo en una carpeta persistente, no solo en la memoria del chat.
- La IA escribe mucho y **es mala revisando lo que hizo**: hace falta otro revisor y prueba humana.
- El razonamiento máximo no siempre conviene: gasta más y no hace falta para un email o una explicación sencilla.
- Un agente = modelo + contexto + herramientas + objetivo.
- Las fábricas agénticas encadenan varios pasos o modelos (entrada → pasos → salida).

Aplicado a la pregunta del «jefe más»: Euge no propone un segundo Grok Bot cuyo único trabajo sea manejar al modelo fuerte. El capataz **es** Grok Bot. El modelo fuerte vive en la fábrica (en OnIA: Codex en el VPS y el HOMELAB). Un «Jefe de Codex» en Grok Bot sería un capataz extra entre vos y el capataz, justo lo contrario de «hablar solamente con un agente».

## Qué dicen Anthropic y OpenAI

- Anthropic, [Building effective agents](https://www.anthropic.com/research/building-effective-agents): buscar la solución más simple y sumar complejidad solo cuando hace falta. El patrón **orchestrator-workers** es un LLM central que parte el trabajo, lo delega y sintetiza. Tres principios: simplicidad, transparencia del plan, y una buena interfaz agente-herramientas. Los sistemas agénticos suelen canjear latencia y costo por mejor resultado.
- Anthropic, [When to use multi-agent systems](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them): han visto equipos invertir meses en arquitecturas multiagente y luego lograr lo mismo con mejor prompting en un solo agente. Los multiagente suelen usar **de 3 a 10 veces más tokens** que un solo agente para la misma tarea (contexto duplicado, mensajes de coordinación, resúmenes de handoff). Valen la pena en tres casos: contaminación de contexto, trabajo realmente paralelo, o especialización que mejora las herramientas o el foco. **Fuera de esos casos, el costo de coordinar suele superar el beneficio.**
- El mismo artículo advierte contra partir por *tipo de trabajo* (un agente planea, otro implementa, otro revisa, otro itera): se pierde contexto en cada pase (el «teléfono descompuesto») y en un experimento así los subagentes gastaron más tokens coordinando que trabajando. Conviene partir por **límites de contexto** (trabajos que se pueden aislar de verdad), no por el organigrama. Un «Jefe de Codex» + Codex + el coordinador del harness es exactamente partir por rol (planificar / ejecutar / lanzar sesiones).
- La excepción que sí funciona bien, según ese artículo, es un **verificador** que comprueba con criterios concretos y no necesita toda la historia. OnIA ya tiene eso en el harness: revisor distinto y de solo lectura ([ORQUESTACION.md](ORQUESTACION.md), [AUDITORIA-ORQUESTACION-20261109.md](AUDITORIA-ORQUESTACION-20261109.md)).
- OpenAI, [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration): empezar con **un** agente. Sumar especialistas solo cuando mejoran de verdad el aislamiento de capacidades, de política, la claridad del prompt o el rastro. «Splitting too early creates more prompts, more traces, and more approval surfaces.» Si el manager debe quedarse con la respuesta final, los especialistas se invocan como herramientas acotadas; el handoff total solo cuando el especialista debe dueñar la conversación.
- OpenAI / Codex, [context files](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex): el contexto que tiene que sobrevivir se guarda en archivos de fase (decisiones, no-objetivos, supuestos, evidencia, preguntas abiertas), no en la transcripción. Actualizarlos al cerrar una fase y pasar solo ese archivo a la siguiente. Eso ataca «Boss no tiene contexto» mejor que sumar un agente.

## Estado actual en el repo (el piso de OnIA)

Hechos ya documentados, no redescubiertos:

- [boss-memoria.md](boss-memoria.md) dice a la vez «Boss solo planifica; Codex hace todo el trabajo» y «mientras tanto las tareas de conectores pasan por Boss». También dice **«No crear más bots de Grok hasta que haya ingresos»**. Esa contradicción empuja a Codex a quedarse con investigación, docs y análisis que Grok Bot ya puede hacer.
- [pendientes/codex-conectores.md](pendientes/codex-conectores.md): el MCP global de Codex en el VPS sigue vacío; el harness usa `--ignore-user-config`. Mientras tanto, Notion, Drive, X y n8n los hace Boss u otro agente con conectores. Una de las opciones anotadas es un puente que deje datos en archivos. **Eso todavía no está implementado como cola.**
- [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md): no hay canal de handoff operativo; el puente de hoy es que Sergio (o Boss) pega prompts en el chat de Codex. `cola-boss.md` está propuesto y **aún no creado** (espera sí). `operacion/AGENTS.md` (7 nov) excluye a Grok y le dice a Codex que no delegue. [ORQUESTACION.md](ORQUESTACION.md) describe el harness Codex↔Codex (lanzar, tope de 3, revisor distinto) y no nombra a los compañeros de Grok Bot.
- El harness **ya es** un jefe de sesiones de Codex: prepara, lanza, retoma, cierra, revisa y acepta, con `--si-sergio` y cierre solo si el commit está en `origin`. La auditoría del 9 nov concluyó: está bien diseñado; no reconstruirlo.
- Los compañeros que ya existen: **Calendario** (agenda), **Contenido** (copy y piezas), **Operaciones** (Hostinger y n8n en lectura, salvo un sí), **Binance** (lectura/consulta cuando Sergio lo pida; no operar ni gastar sin sí). Ninguno tiene como trabajo manejar a Codex.
- Dos cuotas distintas, no mezclarlas:
  - **Codex** (documentado en el reparto de esta tarde): 67% usado a ~14:54 America/La_Paz; plan prolite; créditos extra 0; reset viernes 13 nov 22:47 America/La_Paz.
  - **Grok Bot / piscina semanal del plan** (informe de este turno): ver la sección siguiente.

## Uso de la cuota de Grok, leído en este turno

Informe de uso de la cuenta, leído el 9 nov 2026 ~16:57 America/La_Paz. No se inventan otros números. Este informe no predice cuánto gastará una tarea futura.

- Plan: **Premium**.
- Límite semanal de uso: **7,8% usado**. Ese límite se comparte con las otras apps del plan; no es solo de Grok Bot.
- De ese 7,8%, Grok Bot usó 7,8% (en esta lectura, la parte usada de la piscina semanal aparece atribuida a Grok Bot).
- El límite semanal se renueva el **sábado 14 nov a las 10:00 America/La_Paz**.
- El uso extra viene de créditos de uso adicional. El saldo de esos créditos y el tope mensual no vinieron en este informe; se ven en [Uso y facturación](grokbot://app/v1/settings?id=usage).
- Cómo se repartió el uso de Grok Bot en esta semana (7–9 nov, UTC), como **porcentaje del uso de Grok Bot en ese período**, no del límite semanal:
  - **Boss: 59%**, casi todo fuera de routines (las routines borradas y los check-ins propios de Grok Bot, cada uno <1%).
  - **Bots borrados, group chats y bots de otras personas: 38%.**
  - **Binance: 2%.**
  - **Calendario: 1%** (la routine «Revisión importante de calendario» <1%, unas 6 corridas por semana).
  - **Contenido: <1%.**
  - **Operaciones: <1%.**

Lectura útil, sin extrapolar un ahorro:

- Esta semana la piscina de Grok **no está justa** (7,8% al 9 nov). La cuota que sí está alta es la de Codex (67%, reset el viernes 13). El miedo de que Grok «se acabe rápido» es razonable en un plan Premium (multiplicador oficial 4x frente a Super 15x o Ultra 50x), pero el agujero visible hoy no es Boss hablando con Sergio: es el 38% que se fue a bots borrados, group chats y bots ajenos.
- Contenido y Operaciones casi no gastan. Si el workshop manda hasta el 14, conviene usar Contenido para piezas, no Codex.
- No se recomienda una routine que vigile el uso: cada chequeo también gasta. La app ya avisa cuando el límite se acerca.

## (a) ¿Vale un «Jefe de Codex» frente a las alternativas?

| Opción | Qué ganás | Qué perdés / riesgo | ¿Ahora? |
| --- | --- | --- | --- |
| **1. Agente nuevo «Jefe de Codex»** | Un chat con memoria propia dedicado a armar paquetes para Codex; Sergio o Boss le hablarían de ese tema | No cambia el modelo (no hay selector). Parte el contexto: Boss ya no acumula el estado de Codex, y el nuevo Bot empieza de cero. Cada ida y vuelta (Boss→Jefe→respuesta, o un group chat) gasta uso. Sergio pasaría a hablar con dos capataces, contra Euge y contra «empezar en el Bot primario». Quedaría un tercer jefe encima del coordinador del harness. Choca con la regla vigente de no crear más bots de Grok hasta que haya ingresos. El 38% del uso de esta semana ya se fue a bots/group chats que no son Boss | **No** |
| **2. Encargárselo a Operaciones** | No se crea un Bot nuevo | Operaciones ya tiene oficio (Hostinger, n8n). Las docs piden un trabajo por Bot, con fuentes propias. Mezclar hosting con «manejar Codex» contamina las dos memorias | **No** |
| **3. Skill + (más adelante) routine + archivo de handoff** | La skill se comparte entre Bots y no abre otro chat. El archivo vive en GitHub, lo leen Boss y Codex aunque Grok esté en cero. Una routine que mire la cola puede venir después, con sí, y solo cuando la skill ya funcione a mano | Una routine frecuente gasta uso en cada corrida. Hasta que exista la cola, Sergio sigue reenviando el bloque (un minuto) | **Sí, como siguiente paso barato** (la skill y la cola esperan sí; este commit no las crea) |
| **4. El coordinador del harness como jefe de sesiones, Boss como portero** | Ya existe: lanza, retoma, cierra y revisa con tope de 3 y `--si-sergio`. Boss (o Sergio) escribe el pedido claro, da el sí y no entra al VPS. Si Grok se queda sin cuota, el harness sigue con lo ya aprobado | Boss no «maneja» a Codex en caliente dentro del VPS; el puente sigue siendo GitHub + el texto que Sergio pega, hasta que haya cola | **Sí: es el diseño actual, hay que usarlo en vez de sumar un agente** |

**Recomendación:** la opción 4 ahora, más la 3 en cuanto des el sí (archivos `CONTEXTO-BOSS.md` y `cola-boss.md`, y una skill de «armar/leer pedido a Codex»). Un agente «Jefe de Codex» solo se volvería a discutir **después** de probar esos archivos y **después** de tener ingresos, y solo si manejar a Codex se volviera un trabajo diario con horario propio que le ensucie a Boss el contexto de negocio. Hoy no se cumple el criterio oficial («fuentes, reglas o calendario propios» que Boss no pueda leer) ni el de Anthropic (aislar contexto de verdad, no clonar el organigrama).

Los ejecutores internos de Boss (investigar, leer docs, redactar este tipo de nota) ya cubren el papel de «subagente del capataz» que muestra Euge. No hace falta bautizar a otro compañero para eso.

## (b) Cómo dividir el trabajo de Boss y de los compañeros

Ajuste fino del reparto ya escrito en [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md) y del mapa de [EUGE-VIDEO-BOSS-20261109.md](EUGE-VIDEO-BOSS-20261109.md). No cambia máquinas: HOMELAB = PC de casa; la laptop sigue fuera.

| Quién | Qué hace | Qué no hace |
| --- | --- | --- |
| **Sergio** | Objetivos, criterios, contraseñas, sí de gasto, n8n, publicación y revisión editorial. Pega en Codex solo lo ya empaquetado, o confirma el paquete | No tiene que ser el router de calendario, copy o lecturas de Drive/Notion |
| **Boss (Bot primario / capataz)** | Único chat cotidiano. Parte el trabajo, pide el sí, documenta en GitHub, delega a compañeros, arma o revisa el paquete para Codex, lee el estado corto, hace síntesis y las tareas de conectores que no tengan dueño más claro | No entra al shell del VPS ni configura WSL. No relanza investigación que ya está en Git. No inventa MCP para Codex |
| **Calendario** | Agenda, solapes, preparación de reuniones, recordatorios | Código, VPS, copy largo |
| **Contenido** | Ideas, guiones, piezas del workshop, marca en X/Notion/Drive | Shell, n8n de producción, Codex |
| **Operaciones** | Hostinger y n8n en lectura (activar/desactivar/borrar solo con sí); chequeos | Convertirse en jefe de Codex |
| **Binance** | Consultas cuando lo pidas, más adelante; sin operar ni gastar sin sí | Análisis de caja completo ni trabajo de harness |
| **Ejecutores de Boss** | Lecturas largas, investigación con fuentes, commits de documentación | Sustituir a Codex dentro del VPS o de WSL |
| **Codex + harness + HOMELAB** | Código, tests, harness, Tailscale/WSL/`onia-worker`, commits desde el VPS, Chromium local, lo que Grok Bot no puede o no debe hacer en esas máquinas | Calendario, Notion/Drive/Gmail/X, copy, releer docs ya en Git, monitoreo Hostinger/n8n, síntesis de negocio |
| **Coordinador del harness** | Lanzar, retomar, cerrar y revisar sesiones de Codex, con tope de 3 y `--si-sergio` | Decidir gasto, publicación o n8n |

Regla práctica para Boss, pensada para la cuota:

1. Si el pedido se resuelve con un conector o con docs ya en Git → lo hace Boss o el compañero del área.
2. Si necesita VPS, PC de casa, código o harness → Boss (o Sergio) escribe un `## PEDIDO` y para esa parte. Codex no re-investiga el paquete.
3. Si Codex se encuentra una subtarea de conectores o de sola lectura → escribe el mismo tipo de bloque y para, en vez de improvisar MCP.
4. Trabajo pesado de máquina → Codex. Trabajo pesado de lectura o de criterio de negocio → Boss/compañeros, no Codex en ultra.

## (c) En qué gastar la cuota de Grok y en qué no

Prioridad, de más a menos. No se calcula un ahorro futuro.

**Gastar (en este orden):**

1. **Hablar con vos y coordinar decisiones.** Ya es el 59% del uso de Grok Bot esta semana, y es el trabajo del Bot primario. Pedidos cortos, con el resultado que esperás y el límite de aprobación, gastan menos esfuerzo que una investigación abierta.
2. **Lo que Codex no puede hacer hoy:** Calendar, Notion, Drive, Gmail, X, n8n y Hostinger por conector; revisar un entregable no técnico; armar el paquete para que Codex no vuelva a leer todo.
3. **El workshop, con Contenido.** Hasta el 14 manda vender. Contenido usó <1% esta semana: está subutilizado frente a Codex al 67%.
4. **Leer el repo y los documentos que ya existen**, en vez de pedirle a Codex que los relea con un subagente caro.
5. **Delegar a un compañero solo cuando ese compañero es dueño de la fuente** (Calendario para un solape, Operaciones para un chequeo de hosting). Un dueño por etapa, no un group chat de cuatro Bots para una pregunta.

**No gastar / ahorrar:**

1. **No crear más Bots ni group chats** hasta que haya ingresos y un trabajo recurrente con fuentes propias. El 38% del uso de Grok Bot de esta semana se fue a bots borrados, group chats y bots ajenos.
2. **No armar routines frecuentes** (cada hora, o un trigger amplio de Slack/GitHub). La doc oficial advierte que eso puede comerse una semana de uso en un día. Calendario ya tiene una routine ~6 veces por semana; no sumar otra de vigilancia.
3. **No releer videos ni docs que ya tienen nota en Git** (los dos de Euge, esta propuesta, el reparto, la auditoría).
4. **No usar Grok Bot para shell del VPS, WSL o código de fábrica.** Eso es Codex. Tampoco usar Codex para agenda o copy.
5. **No hinchar el contexto** con material que no cambia la decisión (Euge, segundo video). Un estado de dos pantallas le sirve más a Boss que otro agente.
6. **No intentar elegir «un modelo más barato» para Boss.** No hay selector; lo que cambia el ritmo de uso es el tipo de trabajo y el esfuerzo de cada pedido.
7. **No subir de plan ni encender gasto extra** sin un sí tuyo. El informe menciona créditos adicionales: el tope mensual lo ves y lo cambiás vos en [Uso y facturación](grokbot://app/v1/settings?id=usage).

La cuota cara **esta semana** es la de Codex, no la de Grok. Tiene sentido que Grok haga lecturas y paquetes para que Codex no queme el 33% que le queda antes del viernes 13 a las 22:47 America/La_Paz.

## (d) Cómo arreglar «Boss no tiene contexto»

No es (solo) un tema de modelo. El contexto está partido y a veces se contradice:

- `boss-memoria.md` es un diario largo, no un estado actual de una página.
- La regla «Codex hace todo» pelea con «los conectores pasan por Boss».
- `ORQUESTACION.md` no ve a los compañeros de Grok Bot.
- `operacion/AGENTS.md` le dice a Codex que no delegue.
- No existe todavía un archivo corto que Codex actualice y Boss lea al arrancar un turno operativo.
- El único puente vivo es el copia y pega humano.

Arreglo propuesto, **sin crearlo en este commit** (espera tu sí):

1. **`CONTEXTO-BOSS.md`** en esta misma carpeta. Corto a propósito (Euge: no hinchar). Codex lo actualiza al cerrar un bloque de trabajo; Boss lo lee cuando hay que decidir o armar un pedido. Contenido típico:
   - fecha de actualización (America/La_Paz);
   - prioridad vigente (hoy: workshop hasta el 14; de homelab, solo lo esencial);
   - máquinas (PC de casa = HOMELAB; laptop fuera);
   - estado de una línea: harness, Tailscale, `onia-worker`, `/mnt/c`, WSL siempre encendido;
   - cuota de Codex y de Grok, con fecha de la lectura (sin inventar);
   - decisiones que esperan tu sí;
   - próximo paso de Codex y qué no hacer;
   - enlaces a los docs canónicos, no una copia de todos ellos.
2. **`pendientes/cola-boss.md`**, como ya está propuesto en el reparto: bloques `## PEDIDO` / `## HECHO`, con objetivo, rutas, aceptación y qué no hacer. Sin secretos.
3. **Alinear `boss-memoria.md`:** Boss planifica **y** hace conectores, docs, contenido y el armado de paquetes; Codex hace VPS, PC, código y harness. Dejar de decir «Codex hace todo el trabajo».
4. **Alinear `operacion/AGENTS.md`** con el reparto (no borrar; marcar lo viejo como obsoleto). Eso ya está en el prompt de auditoría que espera tu sí.
5. **Más adelante, con otro sí:** una skill compartida «pedido a Codex / leer cola-boss» (las skills se comparten entre Bots y no abren otro chat). Recién cuando eso funcione a mano, una routine que mire `cola-boss.md` en `origin/master`. No crearla ahora.
6. **Los prompts para Codex los puede redactar Codex o Boss; los revisa Boss** antes de que los pegues. Eso sigue la regla de Euge: la IA escribe, otro mira, vos das el sí sensible.

La memoria automática del Bot sigue siendo útil para preferencias estables («hablame en voseo», «no gastes sin sí»). El estado que cambia día a día vive en GitHub, que es la carpeta persistente del segundo video de Euge.

## (e) Qué pasa si se acaba la cuota de Grok

Diseño de respaldo, sin gasto extra:

1. Codex no depende de que Boss esté despierto. El harness lee GitHub y sigue con lo que ya tenga tu sí.
2. Los archivos `boss-memoria.md`, el futuro `CONTEXTO-BOSS.md` y `cola-boss.md` son el relevo: Codex puede trabajar sin pedirle nada a Grok.
3. Vos le hablás directo a Codex con el último paquete escrito, o con el prompt que ya esté en el repo.
4. Calendario, Contenido, Operaciones y las routines también se detienen si Grok no puede responder. Por eso las fábricas no pueden vivir solo dentro de Grok Bot.
5. Si el límite semanal se termina y no querés gastar créditos adicionales, dejá el tope en [Uso y facturación](grokbot://app/v1/settings?id=usage) y esperá el reset del sábado 14 nov a las 10:00 America/La_Paz. No se propone subir de plan.

Esto es lo que ya se buscaba al copiar reglas a `boss-memoria.md`: «para que Codex pueda seguir solo si se acaba la cuota de Grok». Falta el estado corto; el diario solo no alcanza.

## (f) Tres decisiones para Sergio

1. **¿Aceptás no crear un «Jefe de Codex» ahora?** El diseño quedaría: Boss = único capataz con el que hablás; el coordinador del harness = jefe de las sesiones de Codex; GitHub = punto de encuentro. Un agente nuevo se vuelve a discutir solo después de probar los archivos y después de tener ingresos.
2. **¿Con un sí aparte (no en este commit) creamos `CONTEXTO-BOSS.md` y `pendientes/cola-boss.md`, y alineamos la frase contradictoria de `boss-memoria.md` («Codex hace todo el trabajo»)?** También seguiría pendiente el prompt ya redactado para que Codex baje su default a Sol high y deje de excluir a Grok en `operacion/AGENTS.md`.
3. **¿Hasta el 14 nov, la cuota de Grok se usa para hablar con vos, el workshop (Contenido), los conectores y los paquetes para Codex — y no para más Bots, group chats ni routines frecuentes?** La cuota que hay que cuidar de cerca esta semana es la de Codex (67%, reset viernes 13 nov 22:47 America/La_Paz).

## Qué no se hizo aquí

No se creó ningún agente ni routine. No se creó `CONTEXTO-BOSS.md` ni `cola-boss.md`. No se cambió el harness, n8n, el VPS ni la PC. No se pegó nada a Codex.

## Fuentes

- Local: `/home/box/reference/app-ui.md`, `/home/box/reference/debugging-the-box.md`
- [Grok Bot overview](https://docs.x.ai/grok-bot/overview)
- [How Grok Bot works](https://docs.x.ai/grok-bot/how-grok-bot-works)
- [Create and manage Bots](https://docs.x.ai/grok-bot/bots)
- [Message and collaborate](https://docs.x.ai/grok-bot/chat-and-collaboration)
- [Skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)
- [Grok Bot FAQ](https://docs.x.ai/grok-bot/faq)
- [Grok Bot (cursor.com)](https://cursor.com/docs/grok-bot)
- [Grok Bot on The X Subscription](https://docs.x.ai/x-subscription/grok-bot)
- [Pricing](https://docs.x.ai/x-subscription/pricing)
- [Usage limits](https://docs.x.ai/x-subscription/usage-limits)
- Informe de uso de esta cuenta, 9 nov 2026 ~16:57 America/La_Paz
- [EUGE-VIDEO-BOSS-20261109.md](EUGE-VIDEO-BOSS-20261109.md) y [EUGE-VIDEO2-BOSS-20261109.md](EUGE-VIDEO2-BOSS-20261109.md); videos [JuAQILH7dkQ](https://www.youtube.com/watch?v=JuAQILH7dkQ) y [xPJbP9yZE1I](https://youtu.be/xPJbP9yZE1I)
- [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (Anthropic)
- [When to use multi-agent systems](https://claude.com/resources/articles/building-multi-agent-systems-when-and-how-to-use-them) (Anthropic)
- [Orchestration and handoffs](https://developers.openai.com/api/docs/guides/agents/orchestration) (OpenAI)
- [Iterating development workflows with Codex](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)
- Repo: [ORQUESTACION.md](ORQUESTACION.md), [boss-memoria.md](boss-memoria.md), [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md), [pendientes/codex-conectores.md](pendientes/codex-conectores.md), [AUDITORIA-ORQUESTACION-20261109.md](AUDITORIA-ORQUESTACION-20261109.md)

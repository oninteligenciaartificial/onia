# Dictamen: harness, sesiones y homelab

Boss · 10 noviembre 2026, 12:32 America/La_Paz. Lectura del repo en `67be8b7` y consulta del puente (sólo `consultar`). No se cambió el harness, no se lanzó Codex y no se tocó la PC.

Sergio lee esto en el celular: el veredicto va primero; el resto es el criterio para organizar desde hoy hasta el viernes 13.

## 1. Veredicto

**Sí, con condiciones.** El harness es correcto para que Boss empiece a organizar y lanzar tareas. No hay que reconstruirlo. Faltan dos avisos chicos y el piloto formal todavía no está aceptado.

### Lo que está bien

- El puente SSH está acotado: JSON `onia-harness-v1`, sin shell, con permisos por tarea y nonce idempotente (`harness_boss.py` L18–21, L95–110, L211–218). La entrada forzada es `entrada-boss.sh`.
- Como máximo 3 sesiones vivas, incluyendo revisores; se rechaza una cuarta y un segundo vivo del mismo ID (`harness_sesiones.py` L217–227; `ORQUESTACION.md` L183; `reglas-comunes.md` L51–56).
- Un escritor por archivo: `check_capacity` y `trabajo.overlapping` (L591–594) impiden dos ejecutoras sobre rutas que se pisan.
- Cada ejecutor trabaja en su worktree `../onia-ws-<id>`, rama `codex/ws-<id>` y Git bare privado (`harness_sesiones.py` L410–433). El revisor usa otro worktree, detached y de sólo lectura, con actor distinto (L387–390, L418–422, L477–492).
- `cerrar` exige commit nuevo publicado en la rama de origin (L688–748). `aceptar` no pasa si el veredicto no es `bueno` (L796).
- El retorno publica a `master` en fast-forward y avisa por HTTPS (`harness_retorno.py` L38–114, L146–187). El piloto real recorrió ejecutar → repetición sin segundo intento → cierre → aviso: [ACUSE-BOSS-v1](evidencias/conexion-boss-piloto-20261110/ACUSE-BOSS-v1.md).

### Huecos concretos

1. **El harness no avisa cuando termina una sesión.** El supervisor marca `finalizada` o `fallida` (`harness_sesiones.py` L602–607) y se calla. `harness_boss.invoke` sólo llama al webhook en `cerrar` y `notificar` (L181–183). Por eso Boss tuvo que consultar a mano la revisión del piloto.
2. **`recoger` guarda el veredicto en el VPS y no lo publica solo.** `collect_review` (L751–796) no llama a `publish` ni a `deliver`. El r14 del piloto llegó a master porque Codex lo publicó a mano (`67be8b7`).
3. **El piloto no está aceptado.** Consulta del puente, 10-nov 12:32 America/La_Paz: `conexion-boss-piloto-20261110` revisión 14, `para_revision`, sesión 2 finalizada, no viva. El revisor distinto (`01a1c637-…`, Sol low) dijo **`cambios`**: le faltó, en el snapshot que vio, la prueba de la solicitud repetida, el acuse de Boss en master, el webhook listo antes del lanzamiento y la identidad distinta del revisor ([revision-2-402790d0.json](evidencias/conexion-boss-piloto-20261110/revision-2-402790d0.json)). Esas pruebas ya están en el acuse y en los commits posteriores; no justifican otra ronda cara de Codex esta semana. `conexion-boss-codex-20261110` sigue `en_espera` r9.

Condición extra, no es un fallo: el puente de Boss sólo puede pedir `gpt-6.1-sol` con esfuerzo `low` o `high` y **cero** subagentes (`harness_boss.py` L151–152 y L173). `ultra`, Astra/Terra y hijos nativos no salen por esta llave.

## 2. Comparación

El harness es un **workflow con código**, no un agente que se despacha solo. Eso coincide con el consejo de Anthropic de empezar por lo simple y no armar un grafo si el camino ya se conoce ([Building effective agents](https://www.anthropic.com/research/building-effective-agents)).

| Patrón | Qué hace | Qué hace OnIA |
|---|---|---|
| Anthropic orchestrator-workers | Un coordinador parte el trabajo y junta resultados. | Boss es el capataz; cada sesión de Codex es un obrero con ID, rutas y techo de 3. El reparto lo decide Boss, no el modelo en caliente. |
| Anthropic evaluator-optimizer | Uno genera y otro evalúa en un bucle. | `lanzar` → `cerrar` → `revisar` (otro actor, sólo lectura) → `recoger` → `aceptar` sólo si el veredicto es `bueno`. El bucle existe; no se acepta en automático. |
| Claude Code: worktrees y subagentes | Sesiones o hijos aislados en worktrees para no pisarse ([docs](https://code.claude.com/docs/en/worktrees)). | Ya está: worktree + bare privado + rutas exclusivas. Los hijos nativos del CLI son 0–2 y los revisores van en 0 (`harness_sesiones.py` L301–308, L352–355). |
| Codex CLI (`codex exec` / `resume`) | Sesión no interactiva y retoma por `session_id` ([docs](https://learn.chatgpt.com/docs/non-interactive-mode)). | El harness lo envuelve: permiso, modelo explícito, `--ignore-user-config`, cierre comprobado y registro en Git. No usamos `resume --last`. |
| LangGraph / CrewAI supervisor | Un grafo o un manager LLM despacha solo. | A propósito **no hay despachador** ([REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md)). El JSON del harness es el estado; la [cola-boss](pendientes/cola-boss.md) es sólo el buzón. |
| Euge: capataz + fábricas | Entrada, pasos, criterio, antes/después y revisión ([ANALISIS](evidencias/euge-dos-videos-20261110/ANALISIS.md)). | Lo tomamos como organización, no como su infra paga. Las 6 fábricas ya están especificadas en `05-herramientas/fabrica-onia/`. |

Veredicto por paso, sin mezclar infra: no se copia el servidor cloud, Opus, Clonify ni ElevenLabs de Euge. OnIA sigue con Boss, Codex en el VPS hasta el 13, FFmpeg, ASR por CPU y n8n inactivo hasta tu sí.

## 3. Cómo organizar las sesiones

### Criterio para partir el trabajo

1. **Una fábrica, un árbol de archivos.** Si dos tareas se pisan, van en serie. Chatbot y guiones sí pueden ir juntos: no comparten rutas.
2. **Un resultado que se pueda cerrar y revisar solo.** No pedir «armá toda la empresa» en una sesión.
3. **La dependencia manda.** No se lanza B si necesita el commit de A en `origin/master`.
4. **El revisor es otra sesión** y cuenta en el tope de 3.

### Repo y ramas

- La verdad está en `origin/master` del repo privado `oninteligenciaartificial/onia`. Nada está terminado hasta el push.
- Coordinador: checkout limpio `~/repos/onia-coordinador`.
- Ejecutor: rama `codex/ws-<id>`, worktree `../onia-ws-<id>`, bare `~/operacion/git/<id>.git`. El ejecutor hace commit y push **sólo** a esa rama.
- Revisor: worktree `../onia-ws-<id>-revision-<n>`, detached en el commit de entrega.
- Boss escribe sus notas (`boss-memoria.md`, `cola-boss.md` y dictámenes propios). Codex escribe el resto técnico. Un ID no mezcla `--dry-run` y operación real: eso ya trabó un lanzamiento el 9-nov ([cola-boss](pendientes/cola-boss.md)).

### Subagentes: cuándo sí y cuándo no

Hasta el 13, **no**. El puente los fija en 0 y la cuota compartida estaba en torno al 78–80 % (Sergio ~07:39 y Codex ~08:16 America/La_Paz, 10-nov; **no se volvió a medir en este turno**). Un hijo consume la misma cuenta y no entra en el tope de 3, o sea que puede gastar más de lo que se ve.

Después, como máximo 1 hijo y sólo si el trabajo se parte en archivos que no se tocan. El revisor nunca lleva hijos. El plan B (Claude, con tu sí si no se llega a la meta) puede usar subagentes de Claude en un trabajo pesado; no es para esta semana.

### Modelo y esfuerzo

Rige el [reparto](REPARTO-CODEX-GROKBOT-20261109.md): predeterminado `gpt-6.1-sol`. `low` para lo simple; `high` para diseño o un fallo difícil. `ultra` sólo si lo pedís vos. No hay salto automático a Astra/Terra/Luna. El chat coordinador del VPS se vio con `gpt-6-astra` / `xhigh`; eso no es lo que lanza Boss.

| Tipo de trabajo | Modelo | Esfuerzo | Revisión |
|---|---|---|---|
| Chatbot n8n + Cloud API (inactivo) | `gpt-6.1-sol` | `high` | Codex distinto, `high` (toca n8n y secretos; no activar) |
| Cinco guiones del día | `gpt-6.1-sol` | `low` | Contenido de editor; vos en el panel. Sin revisor Codex, para no gastar cuota en texto |
| Script de edición (FFmpeg + ASR CPU) | `gpt-6.1-sol` | `high` | Codex distinto, `low` si los tests hablan solos; `high` si hay dudas de corte |
| Arreglo chico del puente (aviso al terminar / publicar veredicto) | `gpt-6.1-sol` | `low` | Codex distinto, `low` |
| Coordinación, venta, mover Drive | Boss (Grok Bot) | — | No gasta Codex |
| Plan B, si la venta no alcanza y das el sí | Claude reemplaza a Codex; el harness y el panel no se cambian | El gasto es otro sí tuyo | Misma revisión distinta |

### Revisión y paralelo

- Actor distinto, veredicto `bueno` o `cambios`, commit exacto de la entrega.
- Esta semana: **1 ejecutora + como mucho 1 revisor** (2 de 3). El tercer cupo queda libre por si hay que retomar o revisar ya.
- No lanzar 3 ejecutoras. Integrar de a una a `master`.

## 4. Homelab

La idea de Euge (un lugar persistente para las fábricas) es correcta. La adaptación nuestra es VPS coordinador + PC de casa como worker. **Hoy no está listo:** aporta capacidad futura, no un segundo Codex gratis.

### Comprobado

- Identidad: sólo `DESKTOP-0GGGNMF`, nodo Tailscale `desktop-0gggnmf`, WSL2 Ubuntu. La laptop `DESKTOP-ENV6SDA` queda fuera ([homelab/README.md](homelab/README.md)).
- Hardware informado por Sergio: i5-12400F, 12 hilos, 15,8 GiB RAM, GT 730 sin CUDA útil, ~885 GB libres, ASR por CPU int8.
- En WSL, Boss vio `bwrap`, `ssh` activo y la huella del host. Tailscale del VPS en userspace, nodo `onia-vps-worker` Running; la PC figura online. Eso prueba membresía de la red, no SSH al worker.
- El instalador `alta-onia-worker.py` está escrito, hasheado y pasó revisión distinta. Aislamiento probado con fixture en el VPS.

### Sólo planeado (no aplicado)

- Crear `onia-worker`, recortar `/mnt/c`, SSH VPS→WSL por el 2224 y Tailscale Serve TCP. El puerto de la PC no respondió en el contraste remoto ([ALTA-ONIA-WORKER.md](homelab/ALTA-ONIA-WORKER.md), [CONEXION-EN-CURSO.md](homelab/CONEXION-EN-CURSO.md)).
- Persistencia de WSL, scheduler F3, medición F1 y LLM local F4. `homelab-conexion-20261109` está `en_espera` r8: el próximo paso humano es tu bloque de PowerShell. El puente no tiene ese ID habilitado (`id_no_habilitado` al consultar).

La PC **no suma cuota de Codex**: es la misma cuenta de ChatGPT ([README del homelab](homelab/README.md) L42). Suma CPU, disco y un sitio donde dejar grabaciones fuera de Git.

### Qué debería correr ahí, y veredicto de infra OnIA

| Paso | Veredicto OnIA | Nota |
|---|---|---|
| Vos corrés el PowerShell de alta sólo en la PC de casa | Sí, infra nuestra; ya está preparado | No se toca la laptop |
| Loopback 2224 y Tailscale Serve TCP (nunca Funnel) | Sí, después de `alta_local: OK` | Codex contrasta la huella antes de entrar |
| ASR CPU y FFmpeg pesado en la PC | Sí, cuando el worker esté probado | Esta semana la edición sigue en el VPS, como dice la [fábrica 2](../05-herramientas/fabrica-onia/2-edicion-video/README.md) |
| Guardar crudos y renders en el disco de la PC / Drive | Sí | Nada de eso entra a Git; Drive ya es la sala de montaje |
| Más sesiones Codex en la PC para subir el tope de 3 | No esta semana | No agrega cuota; subir el tope necesita tu sí y una medición que está aparcada |
| Copiar el Hetzner, Clonify, Opus o ElevenLabs de Euge | No | Se mezcla infra paga ajena con la nuestra de gasto cero |

Siguiente paso humano: el bloque de [ALTA-ONIA-WORKER.md](homelab/ALTA-ONIA-WORKER.md). Mandá sólo `alta_local: OK` o `ALTA DETENIDA`. No bloquea el chatbot ni los guiones de esta semana.

## 5. Cola hasta el viernes 13

Prioridad: la plata primero. Las clases son jueves 12 a las 21:00, viernes 13 a las 21:00 y sábado 14 a las 14:00 (America/La_Paz), Meet, Bs 50 grupal sin cupo y VIP Bs 150 / 5 lugares / 30 min ([DECISIONES-SERGIO-20261110](../05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md)). Esas decisiones ganan al [plan al 13](PLAN-LISTO-AL-13-20261110.md) donde aún decía «hora pendiente» o «Contenido escribe los guiones». Hasta el 13 los escribe Codex, Contenido los edita y vos los aprobás en el panel.

| Orden | ID | Sesión | Modelo | Rutas | Depende de |
|---|---|---|---|---|---|
| 1 | `fabrica-chatbot-whatsapp-20261110` | Ejecutora nueva | Sol `high`, 0 hijos | `05-herramientas/fabrica-onia/4-chatbot-whatsapp/` | Decisiones ya tomadas. QR privado en el VPS (dijiste que se lo pasás a Codex; **no comprobé en este turno si ya está**). El flujo nace inactivo. Vos verificás el número en Meta. Plan B humano: los mismos textos a mano si Meta no llega para el jueves. |
| 1b | (mismo ID, después del cierre) | Revisor distinto | Sol `high`, 0 hijos | las mismas, sólo lectura | Entrega publicada. No activar n8n. |
| 2 | `guiones-tanda-20261111` (ID nuevo; no usar el validador `fabrica-guiones-paquete-20261110`) | Ejecutora en paralelo con el chatbot | Sol `low`, 0 hijos | `05-herramientas/fabrica-onia/1-guiones-calendario/salida/` | Cerebro, G01/G02 y el calendario de la semana. Cinco paquetes para grabar el 11: venta, marca, noticia o evergreen, segunda venta o marca, reel de prueba. Contenido revisa; vos aprobás. |
| 3 | `fabrica-edicion-video-20261110` | Cuando se libere un cupo | Sol `high`, 0 hijos | `05-herramientas/fabrica-onia/2-edicion-video/` | Puede empezar con tests sintéticos (no toca `audiovisual.py` ni el harness). La prueba con G01 real espera tu tanda en Drive `1 Entrada`. Higgsfield, pieza por pieza con tu sí. |
| 4 | `conexion-boss-codex-20261110` (seguir este ID) | Arreglos chicos, Sol `low` | `05-herramientas/scripts/` (`harness_sesiones.py`, `harness_boss.py`, `harness_retorno.py` y tests) | Cuando haya un cupo libre. Pedidos de la sección 6; no reconstruir. |
| — | Venta del taller (textos, Meet, CTA) | Boss + Contenido | — | `01-negocio/workshop-20261108/` y borradores de la fábrica 4 | Actualizar horarios, Meet y VIP. Los borradores viejos todavía hablan de hora pendiente. |
| — | `revision-boss-g01-20261110` | Boss + Contenido | — | su carpeta de evidencias | El paquete está; **no encontré** `REVISION-BOSS-v1.md` ni `REVISION-CONTENIDO-v1.md`. Sin G01 aprobado no se publica la pieza de venta. |
| — | Homelab | Tu PowerShell; Codex después | — | `04-operacion-agentes/homelab/` | No entra en el paralelo de esta semana. |

Tope de paralelo hoy: chatbot (1) + guiones (2). El tercero queda libre. Edición y puente entran cuando termine una de las dos.

El viernes 13 Codex deja scripts con tests que corran sin modelo, el estado de cada ID y el registro de errores al día. Desde el sábado 14 Contenido escribe los guiones. Si no se llega a la meta, el plan B es pagar Claude con tu sí explícito.

## 6. Pedidos chicos al harness (no reconstruir)

### Pedido A — aviso cuando termina la sesión

ID: seguir `conexion-boss-codex-20261110` (o el que Codex reserve con rutas sólo de scripts). Sol `low`, 0 hijos.

Cuando el supervisor pasa la sesión a `finalizada` o `fallida` (`harness_sesiones.py` L602–607), mandar **un** POST chico a Boss: `id`, revisión, estado de la tarea, intento, rol, `viva: false`. Sin logs, prompts, rutas del disco ni secretos. Una sola vez por intento; si falla, `incierto` y no reintentar solo (igual que el retorno actual). No sustituye a `cerrar` ni a `recoger`.

Aceptación: test que no pega a la red real; el POST se dispara al terminar, no al lanzar; `cerrar` / `notificar` siguen igual.

### Pedido B — publicar el veredicto al recoger

Después de `collect_review`, publicar el registro y `evidencias_revision` a `master` (reutilizar `harness_retorno.publish`) y avisar a Boss. `deliver` ya exige `cierre`, que existe en ese momento, y usa una clave por `id`+revisión: al recoger la revisión cambia, así que no pisa el aviso del cierre. Hoy eso se hizo a mano en `67be8b7`.

Aceptación: un recoger de prueba deja el JSON del veredicto en `origin/master` y un evento de retorno de esa revisión; no se acepta la tarea en automático.

### Qué no pedir ahora

No subir el tope de 3, no armar scheduler, no hacer que un `--dry-run` deje de bloquear un ID real (ya hay [PROPUESTA-DRY-RUN](evidencias/flujo-boss-codex-v2-20261109/PROPUESTA-DRY-RUN.md), no es de esta semana), no abrir el puente a otros modelos hasta el plan B.

## Qué sigue, en una línea

El harness está bien para trabajar. Lo primero que hay que lanzar es el chatbot inactivo y, en paralelo, los cinco guiones de mañana.

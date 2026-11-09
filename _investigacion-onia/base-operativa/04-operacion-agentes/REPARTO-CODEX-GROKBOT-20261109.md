# Reparto aprobado Boss ↔ Codex

## Acuerdo vigente aprobado por Sergio · 9 noviembre 2026 · America/La_Paz

Esta sección sustituye las propuestas históricas de abajo. Fuente: mensaje de Sergio «VERSIÓN FINAL (con mi sí)», seguido del pedido de confirmación y cambio de modelo. Es autorización para aplicar este reparto y documentarlo en GitHub; no es autorización general para publicar contenido, gastar o activar producción.

**Objetivo 1 hasta el 14: INGRESOS orgánicos.** Vender «Tu negocio con IA» con la marca personal de Sergio, único canal de clientes actual: jueves 12 (hora no indicada en esta aprobación), viernes 13 a las 21:00 y sábado 14 a las 14:00, America/La_Paz; Bs 50 grupal. Sin publicidad paga. Boss + Contenido preparan página, posts, invitación, guiones y CTA; Sergio aprueba y publica. Codex sólo interviene ante un PEDIDO técnico concreto y con autorización aplicable. No se reabre investigación ya aceptada ni se crea una oferta VIP por inferencia.

**Cerebro:** contexto en GitHub: reglas, decisiones, `03-referentes/cerebros*` y `01-negocio/workshop-20261108`. Recuperar el material pertinente, no releer ni investigar todo de nuevo. El panel nuevo, Platform, benchmarks, scheduler y el «Jefe de Codex» propuesto quedan aparcados.

| Responsable | Trabajo y límite |
| --- | --- |
| Sergio | Objetivos, gastos, publicaciones y acciones sensibles; aprobación del contenido final. |
| Boss (Grok Bot) | Entrada principal, contexto de negocio, conectores y prioridades dentro de lo aprobado; coordina Calendario, Contenido y Operaciones. |
| Contenido | Guiones, selección de cortes, copies y CTA usando el cerebro. |
| Codex / HOMELAB | Código, harness, diagnóstico, pruebas y pasos técnicos pesados por ID; decide detalles rutinarios y lee las fuentes necesarias para su tarea. |
| Revisor distinto | Coteja entrega y aceptación antes de aceptar. Entregar no equivale a aprobar. |

**Fábrica:** idea o video crudo de Sergio → Boss + Contenido → PEDIDO técnico cuando haga falta → Codex/HOMELAB → revisión distinta → Sergio aprueba y publica. Conectores y cuentas disponibles no conceden permiso de envío/publicación.

### Preparación técnica mínima para esta semana

Reutilizar FFmpeg y faster-whisper donde estén disponibles; no instalar ni iniciar procesamientos por la mera existencia de esta lista. Completar primero el aislamiento del HOMELAB. No repetir investigación de referentes ni implementar una fábrica automática.

| Paso técnico | Entrada necesaria del PEDIDO | Entrega y comprobación |
| --- | --- | --- |
| Transcripción ASR CPU | Archivo autorizado y finalidad; ID y ruta privada accesible. | Texto con tiempos y SRT/VTT si se solicita; señalar palabras dudosas, cotejar pasajes usados como citas con el audio. No deducir música o tono del ASR. |
| Cortes y render con FFmpeg | Lista de intervalos aprobada por Contenido, formato/dimensiones y texto final de subtítulos. | MP4 de borrador, duración, sincronía, audio y encuadre comprobados. No decidir la propuesta comercial ni publicar. |
| Corrección técnica de la página | Sólo si Boss identifica un fallo concreto: reproducción y criterio de aceptación. | Cambio de código probado; publicación/despliegue requiere el sí específico. |

Los medios originales, perfiles y cuentas quedan fuera de Git. GitHub conserva código, instrucciones y evidencia saneada. No se promete ejecución autónoma nocturna ni disponibilidad del worker antes de las pruebas.

### Un registro y un buzón

El JSON del harness es la **única fuente de estados**. [cola-boss.md](pendientes/cola-boss.md) sólo intercambia pedidos/entregas vinculados a ese ID, con destinatario, resultado esperado, aceptación, fuentes/commit, autorización y exclusiones. «HECHO» significa entregado, no aceptado. Un PEDIDO no es autorización de Sergio. El estado se consulta con `harness.py retomar ID`, no se mantiene otra cola de estados en Markdown.

**El despachador automático no existe.** El harness lanza/reanuda una tarea cuando se lo invoca; no sigue despachando solo cuando Boss agota cuota. No se implementa un loop por este acuerdo. Se conservan los tres cupos actuales, revisores incluidos.

### Modelo y evidencia de cada lanzamiento

Predeterminado `gpt-6.1-sol`; esfuerzo `low` para lo simple, `high` para diseño/fallos difíciles. `ultra` únicamente ante pedido explícito de Sergio, también para revisiones. No hay escalamiento automático a Astra/Terra/Luna. Los perfiles de `orquestacion.json` son recomendaciones, no un cambio de runtime.

`~/.codex/config.toml` quedó aplicado con `model = "gpt-6.1-sol"` y `model_reasoning_effort = "low"`; los demás campos se conservaron. El harness usa `--ignore-user-config`: en cada lanzamiento o retoma autorizado indicar `--modelo gpt-6.1-sol --esfuerzo low` (o `high` justificado), además de los demás argumentos. La retoma no debe heredar accidentalmente un modelo/esfuerzo anterior. No lanzar tareas sin su autorización aplicable.

Guardar por intento ID de tarea y sesión, modelo/esfuerzo solicitado y **observado** en metadatos `turn_context` de esa misma sesión. Revisar hijos si los hay; no confundir configuración/recomendación con observación. Sin evidencia, observado queda `null`; si no coincide, detener nuevos pasos de esa tarea y corregir dentro del alcance autorizado. No publicar prompts completos ni logs privados. Cambiar el default no cambia el modelo de una conversación abierta.

Recibo de ejecutor y revisor: ID, rol, modelo+esfuerzo real, `used_percent` inicial/final y hora, saldo extra observado, intentos, commits, retrabajo y resultado. Si aún no hay veredicto, decir «pendiente de revisión»; al resolverlo registrar aceptada/rechazada/fallida según corresponda. La cuota es compartida: una diferencia de puntos no es consumo exclusivo demostrado de una sesión, ni USD.

### Objetivo 2 y límites

HOMELAB esencial: `onia-worker` sin sudo, acceso Windows `/mnt/c` restringido, pruebas de aislamiento y huella host SSH verificada por canal confiable; continuidad WSL dentro de lo ya pedido. Sólo `DESKTOP-0GGGNMF`, nodo `desktop-0gggnmf`, Ubuntu WSL2. Laptop `DESKTOP-ENV6SDA` excluida. Boss ya informó bwrap presente y ssh activo: no pedir de nuevo ese inventario. Falta alta administrativa local y verificación real de acceso/aislamiento; nodo online no acredita worker listo.

Prohibido borrar archivos, gastar, `--no-sandbox`, desactivar AppArmor/userns, secretos en Git, activar/borrar n8n o tocar producción. Publicaciones/envíos requieren autorización específica. El push documental a este repositorio privado está autorizado por este encargo.

### Aplicación y reversión

Se conserva respaldo privado del config original y del AGENTS local. Se cambian sólo modelo/esfuerzo, recomendaciones declarativas y documentos; no runner, permisos del sandbox, servicios o scheduler. Revertir con una nueva edición/commit que restaure esos campos o recomendaciones, tras cotejar cambios posteriores; no restaurar ciegamente un config completo ni borrar historia. AGENTS conserva abajo el texto anterior como obsoleto.

Fuente técnica: [configuración oficial de Codex](https://learn.chatgpt.com/docs/config-file/config-basic), CLI y `harness_sesiones.command` locales. La disponibilidad en catálogo no prueba un lanzamiento real. Evidencia: [entrega técnica](evidencias/reparto-final-20261109/ENTREGA-v1.md).

---

## HISTÓRICO OBSOLETO COMO INSTRUCCIÓN — propuesta anterior, conservada íntegra

Las afirmaciones sobre defaults, rol «Codex hace todo», prioridades, permisos o aprobaciones pendientes que siguen describen su fecha; no prevalecen sobre el acuerdo de arriba.

# Reparto Codex ↔ Grok Bot · 9 noviembre 2026

America/La_Paz. Lectura solo (VPS y repo). Sin secretos ni IPs. Autor: Boss (Grok Bot) tras pedido de Sergio.

Archivo canónico de dos partes: (1) revisión de lo que dijo Codex y (2) por qué no aprovecha a Grok Bot, con división de trabajo, handoff `cola-boss` y prompts copy-paste. **No crear aún** `pendientes/cola-boss.md` (lo crea Codex tras el sí).

---

## Parte 1 — Qué dijo Codex, si es correcto y cómo seguir

### Estado de la sesión

Sesión principal `01a1bc0b-65c1-7e13-afef-88fc1482896a` quieta desde **14:54 America/La_Paz** (18:54 UTC). Sin actividad nueva al momento de la lectura (~16:30 America/La_Paz).

**Cuota Codex observada:** **67%** usado al cierre de esa ventana (último evento de rate limit ~14:54 America/La_Paz / 18:54 UTC), plan **prolite**, créditos extra **0**, reset **viernes 13 nov 22:47 America/La_Paz**.

### Qué hizo Codex (últimas ~3 h)

1. Publicó plan HOMELAB F0 y docs (`88f40eb`).
2. Intentó el túnel local `127.0.0.1:2222`; Sergio aclaró que solo hay PC→VPS; Codex lo descartó bien.
3. Instaló Tailscale en userspace en el VPS; Sergio autorizó el nodo `onia-vps-worker`.
4. Documentó máquinas: PC de casa = HOMELAB, laptop excluida (`304d71c`).
5. Prioridad workshop + plan cerebro/panel (tope propuesto 2 puntos de cuota) → **sigue esperando sí**.
6. Explicó por qué HOMELAB no está listo: solo red; faltan `onia-worker`, restricción de `/mnt/c` y WSL siempre encendido.
7. Preguntó por esta consulta en PowerShell (PC de casa):

```powershell
wsl.exe -d Ubuntu -- sh -lc 'command -v bwrap; systemctl is-active ssh; ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub'
```

8. Relató el video de Euge: HOMELAB = entorno persistente de “fábricas”, no solo CPU; doc en GitHub (`a2c161e`). Usó un subagente Sol 6.1 ultra de solo lectura.

**El prompt de auditoría** (cambiar default a `gpt-6.1-sol` + `high`, marcar `operacion/AGENTS.md`, inventariar worktrees, etc.) **NO se pegó** a Codex. Sigue pendiente del sí de Sergio, igual que el prompt de reparto de esta nota.

### Resultado WSL (Boss en DESKTOP-0GGGNMF, ~16:33 America/La_Paz)

Consulta pedida por Codex, ejecutada por Boss en la PC de casa:

| Chequeo | Resultado |
|---|---|
| `bwrap` | Presente en `/usr/bin/bwrap` |
| `ssh` (servicio) | **active** |
| Host key ed25519 | Presente (huella pública omitida aquí a propósito) |

Listo para que Codex prepare el alta de `onia-worker` (sin sudo, `/mnt/c` restringido, pruebas). Pegar este resumen a Codex o el prompt de la Parte 1 abajo.

### Verificado vs no

| Afirmación | Estado |
|---|---|
| Tailscale VPS + PC online | **Sí** — ping al nodo de la PC OK vía DERP (sin ruta directa aún) |
| Laptop no tocada | **Sí** — README la excluye |
| Commits en `origin/master` (ventana del análisis) | **Sí** — HEAD coordinador = `a2c161e` al leer |
| `onia-coordinador` al día con origin/master | **Sí** |
| `~/repos/onia` viejo | **Sí** — ~108 commits atrás (no borrar) |
| `~/.codex/config.toml` default | **Sigue `gpt-6-astra` + `ultra`** (auditoría no aplicada) |
| `onia-worker` / `/mnt/c` / WSL always-on | **No hechos** (Codex lo admite) |
| Cuota | **67%** a ~14:54 America/La_Paz; prolite; créditos 0 |
| `--no-sandbox` / AppArmor / cookies / n8n prod / borrar | **No violado** — solo aparece como prohibición |
| ~14 worktrees detached de revisión | **Siguen** |

### Riesgos

- Quema cuota en análisis (Euge/ultra) mientras el workshop vende primero.
- Diseño de aislamiento menciona probar `--disable-userns` como “fallo cerrado”; cuidado de no interpretarlo como desactivar userns.
- Listener local 2222 en el VPS sigue sin identificar.
- Tailscale aún por DERP, no directo.

### ¿Espera algo de Sergio?

1. Confirmar/pegar a Codex el resultado WSL de arriba (o el prompt de desbloqueo).
2. **Sí o no** al plan cerebro+panel (tope ~2 puntos).
3. **Sí o no** al prompt de auditoría y al de reparto Codex↔Grok Bot (ambos esperan sí).

### Cómo seguir (recomendado)

1. Entregar a Codex el resultado WSL → alta de `onia-worker`.
2. Decidir cerebro+panel (tope chico) o usar lo ya aceptado sin gastar más.
3. Con sí: pegar auditoría y/o prompt de reparto (abajo).

### Prompt copy-paste · desbloquear HOMELAB (WSL)

```
En la PC de casa (DESKTOP-0GGGNMF / Ubuntu WSL2), la consulta que pediste dio (~16:33 America/La_Paz, Boss):

- bwrap: /usr/bin/bwrap
- systemctl is-active ssh: active
- ssh_host_ed25519_key.pub: presente (huella ya vista en la PC; no la repitas en chat)

Con eso:
1) Preparate el alta concreta de onia-worker SIN sudo, llave dedicada, /mnt/c restringido y pruebas de aislamiento. Mostrame el script/pasos para que yo ejecute lo administrativo local; no toques la laptop DESKTOP-ENV6SDA.
2) No benchmarks, no scheduler, no n8n, no --no-sandbox, no desactivar AppArmor/userns, no borrar, no secretos en git.
3) Documentá en GitHub (homelab/) y pará cuando quede listo el plan de alta + pruebas. Esperá mi sí antes de pedir más pasos.
```

---

## Parte 2 — Por qué Codex no aprovecha a Grok Bot (cuidando cuota, sin gastar más)

### Hallazgo corto

**Hay regla escrita de que Boss haga lo de conectores, pero no hay canal de handoff operativo.** En la práctica Codex se queda con casi todo (investigación, docs, relecturas, análisis de video, propuestas) y quema cuota semanal compartida. Grok Bot (Boss + teammates Calendario / Contenido / Operaciones) ya tiene Notion, Gmail, Drive, Calendar, X, n8n MCP, GitHub, Hostinger, TikTok, Meta, Higgsfield — y **casi no se usa como ejecutor de esas lecturas**.

Grok Bot también tiene límites de uso; **no inventar números**. Hay que repartir, no volcar todo a Boss.

### Qué dice el repo (verificado, solo lectura)

| Fuente | Qué dice | Efecto real |
|---|---|---|
| `pendientes/codex-conectores.md` | MCP de Codex en VPS vacío; opciones MCP/API/**puente Boss→archivos**; **mientras tanto esas tareas las hace Boss** | Correcto en papel; **no hay cola de pedidos Boss←Codex** |
| Análisis conectores 20261108 | Opción C recomendada: **paquete/puente** sin credenciales en el hijo CLI; cero compra | Propuesto, **no implementado como rutina** |
| `boss-memoria.md` | “Boss solo planifica; **Codex hace todo el trabajo**” + “conectores pendientes → pasan por Boss” | **Contradicción**: empuja todo a Codex y a la vez dice que conectores van a Boss |
| `operacion/AGENTS.md` (7 nov) | “Único ejecutor: Codex… **Claude, Grok y otros excluidos**. No delegar” | Codex se auto-aísla de Grok Bot |
| `ORQUESTACION.md` | Harness Codex↔Codex (lanzar/cerrar/revisar). Sin rol “Grok Bot / teammates” | Codex no ve a Boss como herramienta |
| `orquestacion.json` | Áreas marketing/video/desarrollo/… (skills), no bots Calendario/Contenido/Operaciones | Teammates Grok **no están en el mapa de Codex** |
| Skill `onia-llm` (Boss box) | Cola **Grok → Claude/Codex** para trabajo pesado | Dirección **inversa** a lo que hace falta ahora (ahorrar Codex) |
| Sesión Codex del 9 nov (tarde) | 0 menciones “pedir a Boss” / “Grok Bot” | No pide handoff aunque falten conectores |

**Puente existente hoy:** Sergio (o Boss) pega prompts en el chat de Codex y Codex pushea a GitHub. **No hay** cola GitHub automática, webhook n8n Boss↔Codex, ni carpeta compartida que Boss lea por rutina. `onia-llm cola` vive en el box de Boss, no en el VPS de Codex.

### Por qué pasa (causas)

1. **Regla dominante mal calibrada:** “Codex hace todo” + `operacion/AGENTS.md` excluye Grok → Codex no ofrece “esto lo hace Boss”.
2. **Conectores de Codex rotos/ausentes** (`--ignore-user-config`, MCP global vacío) → debería caer a Boss, pero cae a “inventar con archivos locales / gastar más Codex”.
3. **Handoff solo humano:** sin archivo-cola, depende de que Sergio recuerde partir el trabajo.
4. **onia-llm empuja carga hacia Codex**, no la saca.
5. **Grok también tiene límites** → repartir con criterio, no volcar todo.

### Qué está quemando Codex y podría ir a Grok Bot

| Trabajo reciente / típico | ¿Quién debería? | Por qué |
|---|---|---|
| Releer video Euge / docs largos ya en repo | **Boss** (lectura) | No necesita shell VPS |
| Calendario (clase vie 21:00, solapes) | **Calendario** | Tiene Google Calendar |
| Notion / Drive / Gmail / X lecturas | **Boss / Contenido / Operaciones** | Conectores ya listos |
| Borradores de contenido, guiones, copy workshop | **Contenido** (Boss revisa) | Ahorra Codex; Codex solo si hay código/panel |
| Monitoreo Hostinger / n8n estado (sin activar) | **Operaciones** | MCP Hostinger/n8n en Grok |
| Alta `onia-worker`, Tailscale VPS, harness, commits VPS | **Codex** | Solo él está en el VPS/PC |
| Código, worktrees, pruebas en repo, Chromium VPS | **Codex** | Ejecución local |
| Push/verificación `origin/master` desde VPS | **Codex** (o Boss via GitHub si es solo docs) | Docs simples → Boss con GitHub |

### División concreta (cero costo extra)

- **Codex (VPS/PC):** shell, Git en VPS, harness, Tailscale/WSL/`onia-worker`, código, tests, Chromium VPS, n8n *solo diseño* (activar/desactivar/borrar con sí de Sergio).
- **Boss (Grok Bot):** priorizar, preflight, síntesis, docs, investigación web/repo, armar paquetes de contexto para Codex.
- **Calendario:** agenda, recordatorios, choques de horario.
- **Contenido:** borradores, guiones, X/Notion/Drive de marca.
- **Operaciones:** Hostinger, n8n lectura, chequeos, tickets internos.

### Handoff cero-costo propuesto: `cola-boss.md`

1. Archivo en GitHub (aún **no creado**; lo crea Codex tras el sí):  
   `_investigacion-onia/base-operativa/04-operacion-agentes/pendientes/cola-boss.md`
2. Codex escribe bloques `## PEDIDO` (qué, fuentes, aceptación, deadline).
3. Boss (o Sergio) responde `## HECHO` con resumen + rutas y, si hace falta, un **paquete** en `evidencias/paquetes-boss/ID/` (texto saneado, sin secretos).
4. Mientras no haya rutina: **Sergio reenvía** el bloque PEDIDO a Boss / teammate (~1 minuto).
5. Codex **no** re-investiga lo que ya está en el paquete; solo ejecuta.

Más adelante (sigue sin gasto): rutina Boss “leer `cola-boss.md` en origin/master”. No hace falta n8n ni MCP nuevo en Codex para empezar.

### Prompt copy-paste · reparto / ahorro de cuota (espera sí de Sergio)

```
REGLA DE AHORRO (America/La_Paz) — sin gasto extra:
1) Vos (Codex) SOLO: VPS/PC, shell, harness, Tailscale/WSL/onia-worker, código, tests, commits desde el VPS, Chromium local. Modelo default preferido: gpt-6.1-sol high; ultra solo si lo pido.
2) NO hagas vos: calendario, Notion/Drive/Gmail/X, copy/guiones, reseñas largas de docs ya en Git, monitoreo Hostinger/n8n, síntesis de negocio. Eso es Grok Bot (Boss / Calendario / Contenido / Operaciones).
3) Si una subtarea necesita conectores o es solo lectura/docs: creá pendientes/cola-boss.md si no existe y escribí un bloque PEDIDO (objetivo, rutas, aceptación, qué NO hacer) y PARÁ esa subtarea. No la reescribas vos. No inventes acceso MCP.
4) Homelab: seguí solo lo esencial ya autorizado; usá el resultado WSL (bwrap presente, ssh active, host key presente). Laptop DESKTOP-ENV6SDA prohibida.
5) Documentá en GitHub. Prohibido: --no-sandbox, desactivar AppArmor/userns, secretos en git, n8n activar/borrar, borrar archivos, compras.
Confirmá que entendiste y listá 3 tareas abiertas tuyas que deberías devolver a Boss.
```

### Prompt de auditoría (sigue esperando sí; no pegado aún)

```
Con mi sí:
1) En ~/.codex/config.toml cambiá el default a gpt-6.1-sol + model_reasoning_effort="high". Ultra solo si lo pido o para la revisión final crítica. Mostrame el diff antes y después (sin claves).
2) Usá solo ~/repos/onia-coordinador al día con origin/master; no trabajes desde ~/repos/onia (commits atrás). No lo borres.
3) Marcá operacion/AGENTS.md como obsoleto o alinealo con ORQUESTACION.md (no borrar).
4) Inventariá sin borrar las copias de revisión sin rama y el Chromium del piloto abierto; proponeme qué cerrar y esperá mi sí.
5) Terminá solo lo esencial del homelab (onia-worker sin sudo, /mnt/c bloqueado y probado, WSL siempre encendido) y pará. Hasta el 14 nada de investigación ni lotes paralelos nuevos.
Documentá todo en GitHub.
```

### Conclusión

Codex **no está mal de intención** en Homelab/Tailscale, pero **sí está mal de reparto**: la orquestación actual lo deja solo y la regla “Codex hace todo” + AGENTS local que excluye Grok lo empuja a gastar cuota en trabajo que Boss/teammates ya pueden hacer con conectores **sin pagar más**. El arreglo barato no es otro MCP en el VPS ahora: es **cola de pedidos en GitHub + Sergio/Boss como relay**, y que Codex deje de rehacer investigación/docs.

Pendiente del sí de Sergio: (a) prompt auditoría, (b) prompt reparto, (c) cerebro+panel si aún aplica.
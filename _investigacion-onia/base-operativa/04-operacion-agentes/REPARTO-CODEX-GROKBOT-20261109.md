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
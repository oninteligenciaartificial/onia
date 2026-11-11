# Investigación en X, panel actual y contras · 11 nov 2026

Autor: Boss, a pedido de Sergio (11-nov-2026, 19:05 y 19:14 America/La_Paz). Complementa `INVESTIGACION-HARNESS-ONE-MAN-COMPANY-20261111.md` (commit 9be3b7e), que usó fuentes web y docs oficiales. Esta parte suma X, el estado visual del panel y las contras. Etiquetas: **observado** (visto en fuente o repo), **inferido**, **propuesto**.

## 1. Posts de X (2025–2026, lecturas públicas)

Elegidos por métricas públicas reales (`public_metrics`) devueltas por la API de X. Fechas en America/La_Paz.

| # | Autor | Post | Qué dice (observado) | Qué aplicamos (inferido) |
|---|---|---|---|---|
| 1 | @elonmusk | [post](https://x.com/elonmusk/status/2090078663312347334) · 19 ago 2026 · 7,02 M impresiones | «Make an instant one-person company with @Grok @Bot» | Confirma el modelo una persona + bots; no muestra panel |
| 2 | @rohit4verse | [post](https://x.com/rohit4verse/status/2053085351648891048) · 9 may 2026 · 1,03 M | Tesis de empresa de una persona de USD 1.000 M en 2026 (cita a Dario Amodei) | El cuello es cuota, revisión y el sí de Sergio, no pantallas |
| 3 | @itsolelehmann | [post](https://x.com/itsolelehmann/status/2113673555179364610) · 23 oct 2026 · 208 k | Línea de tiempo: empresa de USD 1.000 M con un empleado | Misma tesis |
| 4 | @cgtwts | [post](https://x.com/cgtwts/status/2043693751420469354) · 13 abr 2026 · 116 k | Video de Sam Altman sobre empresas de una persona | Contexto, no diseño |
| 5 | @shushant_l | [post](https://x.com/shushant_l/status/2056359292522168812) · 18 may 2026 · 31 k | «AI second brain»: Claude Code + Obsidian, capturas diarias, PARA, memory files, agentes | Los «Life OS» de X son bóveda + agentes, no panel de venta |
| 6 | @0xwhrrari | [post](https://x.com/0xwhrrari/status/2118327478250840140) · 5 nov 2026 · 1,70 M | «Harness, Loop and Graph»: si pasa tests pero el issue sigue abierto, el problema no es el prompt | Invertir en el loop del harness (cola, revisor), no en otro modelo |
| 7 | @sammy_capital | [post](https://x.com/sammy_capital/status/2120207132410908995) · 10 nov 2026 · 16 k | Lecturas: OpenAI Harness Engineering, Mitchell Hashimoto, harnesses de Anthropic | Mismas fuentes que la investigación 9be3b7e |
| 8 | @dexhorthy | [post](https://x.com/dexhorthy/status/2027478374520865174) · 27 feb 2026 · 36 k | Harness = el agente (Codex, Claude Code); «apparatus» = lo que se construye alrededor | Nuestro harness del VPS es el apparatus alrededor de Codex |
| 9 | @ArchiveExplorer | [post](https://x.com/ArchiveExplorer/status/2074094594556359045), cita [artículo](https://x.com/ArchiveExplorer/status/2071192832455430283) · 2,72 M | Playbook público de Anthropic: 277 skills, 67 agents, 34 rules, 15 hooks para 6 h de Claude Code | Ya usamos skills, reglas, hooks y revisor; no hacen falta 67 agentes |
| 10 | @RodmanAi | [post](https://x.com/RodmanAi/status/2037238354455195910) · 26 mar 2026 · 14 k | Carpeta `.claude/agents/` con 30+ agentes por área | Nuestro reparto Boss/Contenido/Operaciones/Calendario/Boss Life es ese patrón |
| 11 | @JoshARosen | [post](https://x.com/JoshARosen/status/2098422309644054594) · 11 sep 2026 · 23 k | ¿Conviene un harness propio si los labs controlan modelo y harness? | No rehacer Codex; sí el apparatus (cola, revisión, VPS + homelab) |
| 12 | @techdevnotes | [post](https://x.com/techdevnotes/status/2066531302283583684) · 15 jun 2026 · 3,5 k | «Grok Build now has Agent Dashboard» (captura) | Visor de sesiones ≠ panel de fábrica |

Imágenes públicas de dashboards (en `evidencias/x-paneles-20261111/`):
- `01-techdevnotes-grok-agent-dashboard.jpg`: dashboard de agentes de Grok Build (post 12).
- `02/03-pardnchiu-agenvoy-agente-personal-*.jpg`: agente personal self-hosted ([post](https://x.com/pardnchiu/status/2114306743417385046), casi sin interacciones; se usa sólo por la foto).
- `04-chasing-next-dashboard-calendario-todos.jpg`: «Life OS» con agenda, checklist y notas sobre Claude Code + Obsidian ([post](https://x.com/chasing_next/status/2030660561986560226)).

Conclusión (inferido): X coincide con la investigación web. Lo que acelera es el loop de revisión y cuota del harness, no sumar pantallas ni agentes.

## 2. Panel actual de Codex (observado)

Fuente: `cerebro-panel-usable-20261109`, código `diseno.py` y `cerebro.py` (`SECTIONS`), HTML servido localmente en master 9be3b7e, y capturas de evidencia de Codex del 11-nov (hechas con sandbox de Chromium activo):
- Propuesta 1: `evidencias/.../diseno-20261111/host-final-02` (13:25 La Paz).
- Cerebro y estrategias: `correccion-cerebro-20261111/host-final-04` (17:57 La Paz, commit a9067cd).
- Flujo diario: `04-operacion-agentes/evidencias/flujo-diario-real-20261111`.

Secciones hoy: Hoy, Fábricas (6), Calendario, Cerebro, Sala de montaje, Estrategias, Anuncios y canales, Correcciones; además Guiones, Fuentes, Ideas, Entregas y bloqueos y el bloque Flujo diario.

- «Calendario» es sólo el del workshop (Vie 13 20:00, Sáb 14 14:00, Lun 16 20:00, America/La_Paz).
- «Hoy» es la preparación del workshop.
- **No hay vida personal**: 0 apariciones de novia, gimnasio, hábito, estudios, vida personal, Boss Life o Google Calendar en el código del panel, el HTML ni `CIERRE-VENTA-20261111.md`.
- Lo personal sigue en Google Calendar y los agentes Calendario y Boss Life.

Boss no pudo sacar capturas nuevas en su computadora sin `--no-sandbox` (prohibido por la regla 10); usó las de evidencia de Codex.

## 3. Contras y riesgos

**Del enfoque one-man company con agentes**
- La tesis de X (empresa de una persona de USD 1.000 M) es marketing de labs e influencers, no evidencia de que OnIA pueda operar sola. Casos reales como Base44 tenían producto validado antes.
- Más agentes y pantallas no reducen trabajo si la revisión no da abasto: hoy hay 6 tareas en `para_revision` desde el 10-nov.
- La coordinación entre agentes ya falló hoy: Sergio dejó de usar a Boss por eso, y hubo dos horarios distintos del workshop (Boss: Vie/Sáb/Dom; Codex: Vie/Sáb/Lun). Los eventos de Calendar siguen con el horario sustituido.

**Del harness y la cuota**
- La cuota de Codex se pierde el 14; después no hay plan pago ni proveedor garantizado. Free/Go tienen límites no publicados.
- El despachador tiene 34 pruebas pero nunca corrió con sesiones reales. Llamarlo autónomo hoy sería falso.
- `onia-llm` corre fuera del harness, con tope de 3 por agente (no global) y sin registro de cuota; puede saltarse el tope de 3 sesiones (no comprobado si usa la misma cuenta).
- `onia-llm --nivel pesado` usa Astra, que según la tabla oficial rinde unas 3 veces menos mensajes que Sol.
- Subir de 3 sesiones sin medir cuota y revisión aumenta el gasto sin aumentar lo aceptado.

**Del homelab y el VPS**
- El homelab no suma Codex; sólo CPU (transcripción, FFmpeg, tests). Sigue sin worker aceptado ni diagnóstico PE corrido, y se desconecta cuando la PC se apaga.
- Exponer servicios por Tailscale Funnel o abrir puertos sería un riesgo; sólo Serve/SSH con tags.
- El VPS es punto único de falla para el panel y el registro.

**Del panel**
- Es un tablero de fábrica, no un Life OS como los posts que Sergio ve. Mezclar vida personal rompería el reparto de agentes y pondría datos privados junto a la operación.
- Falta el acceso privado real desde el teléfono; lo local no lo acredita.
- Mucho texto y muchas secciones para un uso rápido desde el celular (inferido de las capturas).

**De las fuentes**
- Métricas de X ≠ calidad; varios posts son opinión. Las fuentes oficiales (OpenAI, Anthropic) describen sus productos y conviene cotejar límites reales con `/status`.

## 4. Propuesto (requiere sí de Sergio)
1. Alinear los eventos Meet de Calendar al horario Vie 13 20:00, Sáb 14 14:00, Lun 16 20:00 y resolver el choque del viernes.
2. Piloto real del despachador esta noche con dos tareas del lote ya aprobado.
3. Tope global en `onia-llm` y pasar de Astra a Sol.
4. Un Life OS personal (Google Calendar + Boss Life + Calendario) como proyecto aparte, después del 14.

# Auditoría de orquestación — 2026-11-09

Boss (America/La_Paz). Sin secretos, IPs ni claves. Fuentes al final.

## Veredicto

El harness está **bien diseñado** respecto a las prácticas de Anthropic y OpenAI:

- Orquestador + workers (no un solo agente monolítico).
- Worktrees separados por sesión.
- Revisor distinto y de solo lectura.
- Tope de 3 sesiones concurrentes.
- Gates humanos (`--si-sergio`, cierre solo con commit en `origin`).
- Memoria durable en GitHub.

En ~7 días: **19 tareas / 56 intentos / 1 fallida**. Produce bien. **No reconstruir el harness.**

## Top 5 riesgos

1. **Defaults de la app interactiva.** `~/.codex/config.toml` deja `gpt-6-astra` + `ultra` por defecto. OpenAI recomienda `gpt-6.1-sol`. El harness queda protegido con `--ignore-user-config`; la app interactiva no.
2. **App interactiva fuera del tope de 3.** Comparte la cuota semanal y puede gastar sin pasar por el harness.
3. **Checkout principal desfasado.** `~/repos/onia` ~102 commits detrás de `origin/master`. `operacion/AGENTS.md` (7 nov) contradice el harness actual.
4. **Residuos.** ~14 worktrees de revisión detached + piloto Chromium vivo ~6h20.
5. **Sin recibo de cuota por tarea.** Solo se ve el `%` semanal; no hay costo por tarea (modelo, intentos, resultado).

## Top 5 mejoras

1. Bajar el default de la app a **Sol high** (necesita el sí de Sergio).
2. Hasta el **14 nov**: no abrir orquestación nueva, investigación larga ni etapas de homelab más allá de lo esencial.
3. Una sola fuente de verdad: `onia-coordinador` alineado a `origin/master`.
4. Después del 14: recibo obligatorio por tarea (id, modelo+esfuerzo, `used_percent` inicio/fin, intentos, resultado, commits, retrabajo).
5. Inventario de higiene de leftovers (worktrees/procesos) **sin borrar** hasta el sí.

## Qué no cambiar

- Ejecutor ≠ revisor.
- Tope de 3 sesiones.
- Worktrees por sesión.
- `--ignore-user-config`.
- `--si-sergio`.
- Cierre solo con commit en `origin`.
- Memoria en GitHub.

## Notas operativas (homelab / VPS)

- `127.0.0.1:2222` sigue sin identificar (escucha como SSH; no usarlo hasta verificar en solo lectura).
- `tailscaled` en modo userspace corriendo en el VPS (nodo `onia-vps-worker` ya en la tailnet, autorizado por Sergio).

## Fuentes

- https://www.anthropic.com/research/building-effective-agents
- https://www.anthropic.com/research/multi-agent-research-system
- https://learn.chatgpt.com/guides/best-practices
- https://learn.chatgpt.com/docs/agent-configuration/subagents
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://code.claude.com/docs/en/worktrees
- X: https://x.com/0xKAVI01/status/2116550768840921512
- X: https://x.com/buildwithhassan/status/2025150504024645766
- X: https://x.com/0xAndros/status/2048831902401085853
- X: https://x.com/rdsaltbo/status/2037533072141189255

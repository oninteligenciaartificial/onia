# Qué hizo Codex (VPS `onia-codex-worker`)

Fuente: `~/operacion/registro.tsv`, `~/operacion/tareas/{hechas,error}/`, `~/operacion/resultados/*-estado.json`, `~/operacion/LEEME.md`. **`~/operacion` NO está en el repo** (fuera de git); estas rutas son del VPS. Horas del registro en UTC; abajo se pasan a hora de Caracas (UTC-4). Todo ocurrió el **7 nov 2026**.

Ejecutor: Codex CLI, ChatGPT plan "prolite", modelo `gpt-6.1-sol`. Runner `~/operacion/ejecutar.sh` (solo lectura) y `ejecutar-n8n.sh` (workspace-write, para n8n).

| Tarea | Hora (Caracas) | Qué era | Estado | Resultado (en `~/operacion/`) |
|---|---|---|---|---|
| PRUEBA-RUNNER | 7 nov | Prueba inocua del runner | Hecha | `resultados/PRUEBA-RUNNER.txt.CSzv8N` |
| T001 | 12:34 | Diagnóstico comercial provisional | Hecha (documental) | `resultados/T001.md` |
| REVISION | 12:35 | Verificación local del runner | Hecha, 5 pruebas OK | `VERIFICACION.md` |
| T002 | — | Acceso GitHub del usuario worker | **Bloqueada** (marcada hecha, no ejecutar) | `resultados/T002.md` |
| T003-CICLO-REAL | 7 nov tarde | Ciclo repo→entregable→revisión→continuidad; inventario workshop | Aceptada técnicamente y retomada | `resultados/INVENTARIO-WORKSHOP-20261107.md`, `CONTINUIDAD-T003-20261107.md`, `T003-estado.json` |
| T003-RETOMA-01 | 7 nov | Reanudar misma sesión | Hecha | `resultados/T003-RETOMA-01.Qs44xF` |
| T004-REVISION-REAL | 7 nov | Revisión independiente de T003 | Hecha | `resultados/REVISION-T003-20261107.md` |
| T005-RECONCILIACION | 7 nov | Reconciliar operación completa (6 áreas) y prioridades | Hecha rc0, ~105k tokens | `resultados/RECONCILIACION-ONIA-20261107.md` |
| T006-REVISION-RECONCILIACION | 7 nov | Revisión independiente de T005 | Hecha rc0, ~63k tokens | `resultados/REVISION-RECONCILIACION-ONIA-20261107.md`, `RELEVO-RECONCILIACION-20261107.md` |
| T007-PAQUETE-OFERTA | 13:44–13:47 | Paquete de oferta tangible del workshop (meta 3.000 Bs) | **Pausada sin revisión** (~61k tokens) | `resultados/PAUSADO-T007-PAQUETE-OFERTA.md`, `T007-PAQUETE-OFERTA.txt.egO3Ah` |
| T008-PANEL-CONTENIDO | 13:48–13:50 | Panel diario + primera pieza grabable + anuncio pausado + mapa de bots | Hecha, solo autorrevisada (~43k tokens) | `diario/2026-11-07/`, `T008-PANEL-CONTENIDO.txt.jUO95x` |
| T009-PANEL-APRENDIZAJES | 13:54–13:55 | Ordenar panel (Notion) + parche documental | Hecha; parche **no aplicado** | `resultados/panel-aprendizajes-20261107/`, `ESTADO-LOCAL.json` |
| T010-N8N-CONTENIDO | 14:17–14:18 | Revisión solo lectura del frente de contenido n8n | Hecha | `resultados/T010-N8N-CONTENIDO.txt.YzWBNn` |
| T011-N8N | 14:26–14:27 | Auditoría Radar YT + preparar Radar IA | **Error rc2** (falló el comprobador, API sin consultar) | `resultados/T011-N8N-bloqueo.md`, `tareas/error/T011-N8N.txt` |
| T011B-N8N | 14:27–14:29 | Reintento de T011 | Hecha | `resultados/T011B-N8N.txt.13EPzB`, `resultados/T011-N8N/` |
| T012-TRIAGE-N8N | 14:30–14:34 | Triage de todos los workflows n8n (solo GET) | Hecha | `resultados/TRIAGE-N8N-20261107.md`, `T012-evidencia-n8n-20261107.json`, `backups-n8n/` |

Otros resultados en `~/operacion/resultados/`: `MANUAL-SERGIO-VPS-20261107.md`, `ANEXO-MANUAL-20261107.md`, `PLAN-RECUPERADO-20261107(-v2).md`, `REVISION-PLAN-20261107.md`, `LECCIONES-OPERACION.md`, `PRUEBAS-OPERACION-MANUAL-20261107.md`, `ACCESO-WINDOWS-WORKER-20261107.md`, `LEEME-PROPUESTO-20261107.md`.

## Cuota
Sesiones de `~/.codex/sessions/2026/11/07/` (18 archivos): `primary.used_percent` = **6 %** en todas, ventana 10.080 min (semanal), reinicio **vie 13 nov 2026 22:47 (Caracas)**, plan prolite, créditos extra 0. No hay sesiones después del 7 nov.

## Antes del VPS (repo, 3–6 nov)
Los 55 commits del repo (autor `oninteligenciaartificial` / `OnIA`) los hicieron agentes (Codex Windows / cloud, "Jefa", "Video", "Marketing", "Desarrollo") con la cuenta de Sergio; git no permite separar autoría humana. Hitos: 3 nov harness y cloud; 4 nov investigación Pedro, audio, n8n sintético; 5 nov referentes (17 personas + Voltra), VPS y faster-whisper; 6 nov continuidad, pilotos cloud, skills. Ver `git log`.

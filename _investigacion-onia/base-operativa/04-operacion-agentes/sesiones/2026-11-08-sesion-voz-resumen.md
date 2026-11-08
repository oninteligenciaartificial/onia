# Resumen de sesión de voz · 8 nov 2026

## 1. Errores de Boss y corrección
- Actué sin revisar: lancé Codex sin chequear su entorno y respondí sin leer el repo.
- No verifiqué conectores, skills ni reglas de Codex.
- Acordado: checklist fijo antes de cada encargo (qué existe en el repo; herramientas, conectores, skills y reglas que necesita Codex; cuota; qué falta; qué se lanza) y lanzar solo con el sí de Sergio.

## 2. Arquitectura
- Codex en el VPS es el ejecutor directo de todo el trabajo.
- Boss coordina y solo hace tareas puntuales.

## 3. Sesiones de Codex
- Corren en el VPS con el usuario `onia-codex-worker`; no aparecen en la app de Codex de la PC.
- Se ven y retoman por SSH con `codex resume`.

## 4. Sesión de cerebros
- Terminó a las 12:04 (America/Caracas), modelo `gpt-6.1-sol`.
- 19 cerebros (18 personas + Voltra) en `03-referentes/cerebros/`, commit `da7d5d0`.
- faster-whisper instalado sin root; transcripciones de Pedro, Cormac y Justin.
- Todos marcados parciales: YouTube bloqueó varias descargas.

## 5. Investigación del harness
- Reporte: `~/operacion/resultados/harness-auditoria-2026-11-08.md` (VPS).
- Harness = sistema alrededor del modelo: contexto, reglas, estado, permisos, pruebas y relevos.
- OnIA ya tiene reglas, preparación (`harness.py`), estado (`trabajo.py`), registro de errores y tests.
- Falta lanzador con sesiones en paralelo; `ejecutar.sh` corta a 5 min y es solo lectura.
- Recomendaciones: reglas actuales en `reglas-comunes.md`; cerrar tareas solo con commit en GitHub; bloquear activación de n8n sin sí; lanzador nuevo con `git worktree` por sesión.

## 6. Guía para usar Codex directo
1. SSH al VPS como `onia-codex-worker`.
2. `cd ~/repos/onia` y `git pull`.
3. `codex` para sesión interactiva.
4. `codex exec "pedido"` para paralelo, cada sesión con su copia: `git worktree add ../onia-tarea-b`.
5. `codex resume` para ver y retomar sesiones.
6. Subir con `git push` (deploy key del VPS).
- Límites: cuota se renueva el viernes 13; acceso a Codex vence el 14; sin conectores (X, n8n, Notion, Drive) ni root.

## 7. Pendiente
- Lanzador nuevo con sesiones paralelas.

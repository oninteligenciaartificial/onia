# Interrupción real y retoma — 8 de noviembre de 2026

**Prueba aprobada y tarea aceptada:** una sesión de juguete recibió SIGTERM externo, conservó sus cambios y se retomó dos veces con el mismo ID. La ejecutora publicó exactamente un commit. Un revisor nuevo de sólo lectura dio veredicto bueno antes de aceptar.

La prueba acredita este recorrido con supervisión del coordinador. Se observó un límite real: quedaron tres procesos residuales del comando lector, que el coordinador dejó terminar mediante su señal de salida antes de retomar. El harness todavía no detecta ni recupera automáticamente todos los procesos huérfanos.

## Resultado comprobado

| Etapa | Evidencia y resultado |
|---|---|
| Antes del corte | `checkpoint.json` staged, `nota.txt` untracked, cero commits nuevos y rama aún sin publicar. |
| Interrupción | SIGTERM dirigido por `pidfd_send_signal` al PID Codex 538534 revalidado, sin señalar el supervisor ni grupos. rc=-15; tarea `en_espera`. |
| Conservación | Mismos bytes SHA-256, índice Git completo, entradas staged, estado, HEAD y ausencia de publicación antes/después. |
| Procesos auxiliares | Tres residuales del lector drenados abriendo su barrera; cero descendientes capturados activos antes de reanudar. |
| Primera retoma | Mismo SID, worktree, Git privado y rama. Crea resultado/verificador y realiza su propio add, commit y push, rc=0. |
| Segunda retoma | Mismo SID; verifica y sale con `RETOMA_IDEMPOTENTE_OK`. Cero add/commit/push. HEAD local/remoto, cuatro archivos e índice conservados; contador sigue en uno. |
| Cierre/revisión | Commit comprobado en origin, worktree limpio retirado, revisor distinto read-only, veredicto bueno, aceptación y reserva liberada. |

Los tres eventos reales `thread.started`, leídos por segmento y offset del log, contienen `01a1bcce-7a6a-7922-aa16-e17371c1dbf8`. El revisor usa `01a1bcd1-d0de-70d1-8b21-de75ca48043c`.

Commit autónomo único: **`c77d03a0047e82d9b7f4ab627f4f18a628d44926`**. Rama: `codex/ws-harness-interrupcion-real-20261108`. Base real: `307f6d30ab71df58854cd8157bce5887e3803f90`. El coordinador integró el commit original por avance rápido; no lo recreó ni publicó por la ejecutora.

El checkpoint conserva SHA-256 `ab0a32d8c67d70450bd6d29dbae11f10aef561917223f49e4b289ce79d28f483`. El juguete comprueba valores `[6,9,12]`, total `27`, la nota exacta y ese hash. Sólo agrega los cuatro archivos previstos. El verificador usa stdlib, lee desde su propia carpeta y no escribe. La ejecutora probó cinco discrepancias en memoria; el revisor, seis. Ambos obtuvieron `RETOMA_OK` para el caso correcto y rechazo para las discrepancias.

## Pruebas y revisión

- Suite completa: **126 casos, 125 aprobados, uno omitido por Windows, cero fallos**, 27,158 s. Incluye el recorrido dry-run y los controles previos de cupos/colisiones.
- Nueva regresión sintética: SIGTERM, staging y archivo sin seguimiento conservados, mismo SID, primera publicación única y segunda retoma sin otro commit. El fake no tiene hijos lectores: esa limitación se observó en el piloto real.
- `doctor`: 30/30 archivos presentes; no equivale a validar servicios o conexiones. `bash -n`: instalador local de skills y los dos scripts `~/operacion/ejecutar*.sh`; no se ejecutaron esos scripts.
- Revisor real: seis criterios cotejados con la entrega y los recibos suministrados por stdin; veredicto **bueno** para el commit exacto. No editó ni aceptó por sí mismo.
- Verificador sobre el árbol integrado: `RETOMA_OK`. Evidencia canónica íntegra y `git diff --check` correcto antes de publicar.
- Los 40 archivos previos con cambios en `~/repos/onia` conservaron hashes y el mismo conjunto de cambios. Cero sesiones del piloto vivas al terminar. Worktrees ejecutor/revisor retirados limpios; ramas y Git privado conservados.

Se mantuvo el runtime existente; se agregó la regresión y se documentó el procedimiento de retoma con sus límites. Los commits concurrentes `b15200c` y `307f6d3`, relativos al plan/memoria, se conservaron. No se reemplazó el trabajo de otros chats.

## Uso y comandos

Los comandos aplicados sobre la tarea preparada fueron los siguientes. Los números de revisión pertenecen a este ensayo ya aceptado; para otro ID se usa su revisión vigente. El corte externo se realizó con el [procedimiento preservado](../../04-operacion-agentes/evidencias/harness-interrupcion-real-20261108/procedimiento-ejecutado.txt), después de verificar el checkpoint, la identidad de proceso y la espera sin escrituras. No repetir su PID histórico.

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
ID=harness-interrupcion-real-20261108
python3 "$H" lanzar "$ID" --revision-esperada 3 --actor interrupcion-ejecutor --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
# Tras SIGTERM y comprobación de conservación/cero hijos activos:
python3 "$H" reanudar "$ID" --revision-esperada 8 --actor interrupcion-ejecutor --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
# Después de la primera publicación, antes de cerrar:
python3 "$H" reanudar "$ID" --revision-esperada 13 --actor interrupcion-ejecutor --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
```

Tras adjuntar las evidencias mediante `trabajo.update`, el coordinador llamó a las funciones existentes `close` (revisión 20), `launch(reviewer='interrupcion-revisor')` (21), `collect_review` (26), `accept` (27) y `assign(release=True)` (28). No se creó otro sistema de tareas. [Comandos CLI equivalentes de cierre y revisión](../../04-operacion-agentes/ORQUESTACION.md).

Consultas actuales, sin relanzar la tarea aceptada:

```bash
cd ~/repos/onia-coordinador
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py estado
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py retomar harness-interrupcion-real-20261108
python3 _investigacion-onia/base-operativa/05-herramientas/2026-11-08-harness/piloto-interrupcion/verificar.py
python3 -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p 'test_*.py'
```

## Evidencia, alcance y pendientes

[Tarea canónica aceptada](../../04-operacion-agentes/tareas/harness-interrupcion-real-20261108.json) · [Recibos saneados](../../04-operacion-agentes/evidencias/harness-interrupcion-real-20261108/) · [Lecciones](../../04-operacion-agentes/registro-de-errores.md#interrupción-real-y-retoma-idempotente--8-de-noviembre-de-2026).

Los recibos conservan timestamps UTC y su conversión explícita a America/Caracas; las horas operativas del informe son Caracas. La señal se produjo a las **16:17:26**. El JSONL crudo permanece privado en `~/operacion/logs/`; se versionan extractos pertinentes, hashes y offsets, sin credenciales.

Sólo cuota incluida del login ChatGPT: Sol/low, permisos `never`, Git privado en ejecutora y read-only en revisor. Cuota semanal observada de 14% antes a 16% al terminar, saldo adicional cero. Es una cuota compartida con otras sesiones; no mide aisladamente el consumo del piloto. Sin API keys, compras, producción, Docker, n8n, app-server ni servicios intervenidos.

Pendientes fuera de este ensayo: detección/limpieza automática de huérfanos, validación automática estricta de cada `thread.started` contra el SID solicitado e idempotencia genérica de las tareas. El coordinador debe comprobar esos puntos antes de retomar. No se probó SIGKILL, caída del VPS ni interrupción durante escritura Git. La prueba de tres sesiones y rechazo de cuarta/solapamiento está registrada en el [ensayo paralelo anterior](PARALELO-REAL-2026-11-08.md); no se presenta como repetida aquí.

Sólo se ejecutó el juguete autorizado. El siguiente paso solicitado por Sergio es definir las tareas, rutas y aceptación del lote que se analizará de punta a punta y lanzar con su autorización aplicable. El hash final de publicación en `origin/master` se añade al recibo externo en `~/operacion/resultados/harness-interrupcion-real-2026-11-08.md`.

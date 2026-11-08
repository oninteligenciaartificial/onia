# Publicación autónoma desde sandbox — 8 de noviembre de 2026

**Resuelto y probado: la propia ejecutora hizo commit y push desde el sandbox; el revisor distinto dio veredicto bueno y la tarea quedó aceptada.** El coordinador preparó el entorno, comprobó el cierre y realizó la integración posterior, sin hacer el commit ni el push de la entrega de juguete.

## Cambio del harness

Se extiende `harness_sesiones.py` y el registro existente de `trabajo.py`. Cada tarea nueva conserva un repositorio bare privado en `~/operacion/git/ID.git` y un worktree `../onia-ws-ID`, rama `codex/ws-ID`, creado desde `origin/master`. Git copia sus objetos por fetch; no usa alternates ni índices/referencias compartidos con el checkout principal.

El perfil `harness-git` extiende `:workspace`, habilita red y concede escritura explícita sólo al bare y al gitdir privados. El runtime observado lo registra como `workspace-write`; `approval_policy` fue `never`. Se mantienen las protecciones del pointer `.git`, `.agents`, `.codex` y demás rutas del perfil base. No hay acceso irrestricto, sudo ni cambios de configuración global. Los revisores conservan `read-only` sin estas concesiones.

El lanzador ignora configuración de usuario para evitar que opciones legacy anulen el perfil; modelo, esfuerzo y autenticación se fijan por intento. Las variables heredadas `GIT_*` se eliminan en operaciones Git y en el hijo para evitar redirecciones de índice/objetos/configuración. Se valida el dueño antes de lanzar, retomar y cerrar; enlaces o alternates bloquean. La identidad técnica local es `OnIA Codex <onia-codex-worker@localhost>`.

La retoma reutiliza dueño, rama e ID; los registros anteriores conservan su modo original. El cierre busca el commit en el dueño privado, lo recupera desde origin al coordinador, exige presencia remota y retira sólo el worktree limpio desde su dueño correcto. Conserva bare y rama. No se creó otro sistema de tareas.

Fuentes contrastadas con CLI 0.167.0: [perfiles oficiales](https://learn.chatgpt.com/docs/permissions), [protección de rutas Git](https://learn.chatgpt.com/docs/agent-approvals-security). La sintaxis de perfiles fue probada sin modelo antes del lanzamiento real.

## Piloto real y revisión

- [Tarea canónica](../../04-operacion-agentes/tareas/harness-autopush-real-20261108.json): `harness-autopush-real-20261108`, aceptada, revisión 19 y reserva liberada.
- Ejecutora: `01a1bca0-e275-7de1-a776-2942f4b7a72c`; revisor distinto: `01a1bca3-33b4-7902-92a2-df7d76b3165f`.
- Entrega publicada por la ejecutora: **`01654543409365cb5adb28f942b2a6f2939dd743`**, en `codex/ws-harness-autopush-real-20261108`.
- Diff: sólo `piloto-autopush/resultado.json` y `piloto-autopush/verificar.py`, en esta carpeta. Valores `[4,1,7]`, ordenados `[1,4,7]`, suma 12 y cuadrados `[16,1,49]`.
- Comprobación: `AUTOPUSH_OK`, rc=0; la ejecutora rechazó siete discrepancias en memoria. El revisor cotejó ocho y verificó que el comprobador no escribe archivos.
- La traza del ejecutor acredita su comando `git add … && git commit … && git push origin HEAD:refs/heads/codex/ws-harness-autopush-real-20261108` con rc=0, seguido de HEAD/`git ls-remote` coincidentes. El coordinador hizo sólo lecturas sobre esa entrega antes de cerrar.
- El cierre confirmó el commit en origin. El revisor de sólo lectura cotejó los seis criterios, el diff y la evidencia suministrada de publicación; emitió **bueno**. El harness recogió el veredicto, aceptó y liberó rutas.
- Cero procesos del piloto vivos; worktrees ejecutor y revisor retirados. Bare privado y rama conservados.

[Evidencia saneada y recibos](../../04-operacion-agentes/evidencias/harness-autopush-real-20261108/): preflight, prueba del sandbox sin modelo, comandos autónomos con salida/código, runtime observado, recibo de cierre, veredicto, aceptación, tests, doctor y conservación. Los logs completos siguen privados en `~/operacion/logs/`; no se publican credenciales ni transcripciones completas.

## Pruebas

- Suite completa: **125 casos; 124 aprobados, uno omitido por Windows y cero fallos**, 27.698 s.
- Nueve pruebas nuevas cubren dueños independientes, ejecutor falso que publica, invariancia del índice/referencias del coordinador, cierre/importación, retoma, enlaces, metadatos inválidos, entorno Git saneado, permisos por rol y compatibilidad de sesiones anteriores.
- Sandbox real sin modelo: commit propio permitido; escritura en índice de otra fixture, archivo ajeno y pointer `.git` denegada. Los tres SHA-256 se conservaron.
- `doctor`: 30/30; `bash -n`: seis scripts; `git diff --check`: correcto. Juguete verificado de nuevo al integrar: `AUTOPUSH_OK`.
- Los 40 archivos con cambios anteriores de `~/repos/onia` conservaron sus bytes y el mismo conjunto de cambios. Se trabajó en el coordinador separado; no se tocaron producción, Docker, n8n, app-server ni servicios.

## Comandos

No hay un subcomando nuevo: `lanzar` aplica automáticamente el aislamiento a tareas nuevas. Los comandos usados, con sus revisiones de aquel momento, fueron:

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
python3 "$H" lanzar harness-autopush-real-20261108 --revision-esperada 3 --actor autopush-ejecutor --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
python3 "$H" cerrar harness-autopush-real-20261108 --revision-esperada 9 --actor autopush-ejecutor --resultado "Juguete publicado por su ejecutora" --comprobacion "AUTOPUSH_OK; commit y push propios rc=0; HEAD coincide con origin"
python3 "$H" revisar harness-autopush-real-20261108 --revision-esperada 10 --actor autopush-ejecutor --revisor autopush-revisor --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
python3 "$H" revisar harness-autopush-real-20261108 --recoger --revision-esperada 16
python3 "$H" aceptar harness-autopush-real-20261108 --revision-esperada 17 --revisor autopush-revisor --criterio "Seis criterios cotejados por sesión independiente"
```

La tarea ya está aceptada: no repetir esos lanzamientos. Para un encargo nuevo, preparar otro ID, asignarlo, comprobar su revisión y autorización. El [procedimiento completo](../../04-operacion-agentes/ORQUESTACION.md) conserva preparar/asignar y retoma. Consultas seguras actuales:

```bash
cd ~/repos/onia-coordinador
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py retomar harness-autopush-real-20261108
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py estado
python3 _investigacion-onia/base-operativa/05-herramientas/2026-11-08-harness/piloto-autopush/verificar.py
```

Consultar PID/estado desde el host coordinador: el `/proc` del sandbox exterior de una herramienta puede no ver los PID del host. La ausencia allí no acredita una caída; se cotejó estado del host y eventos antes de actuar.

## Cuota y límites

Ambos roles usaron el login ChatGPT existente, `gpt-6.1-sol`/`low`, sin API keys, compras ni créditos adicionales. Antes se observó 10% de cuota semanal usada; el dato final del revisor fue 11.0% y saldo adicional 0. La cuota es compartida con esta coordinación: no atribuir todo el cambio exclusivamente al juguete ni convertirlo en un importe monetario.

La publicación autónoma solicitada quedó comprobada. No se probaron tres sesiones reales simultáneas ni recuperación de una caída en este piloto. La retoma conserva tests de regresión y el piloto anterior. El perfil limita archivos locales, **no restringe por sí mismo las ramas remotas accesibles por la credencial GitHub**; los ejecutores deben publicar sólo su rama, sin force. Los registros legacy no se migran automáticamente y los bare privados no se borran automáticamente.

Se publican arreglo, juguete y evidencia en `origin/master`; el hash final verificado se guarda en el recibo externo `~/operacion/resultados/harness-publicacion-autonoma-2026-11-08.md`, para no intentar insertar en un commit su propio hash. [Errores y prevención](../../04-operacion-agentes/registro-de-errores.md#publicación-autónoma-desde-sandbox--8-de-noviembre-de-2026).

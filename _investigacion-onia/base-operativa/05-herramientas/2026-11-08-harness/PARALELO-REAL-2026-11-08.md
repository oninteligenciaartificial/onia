# Tres tareas reales en paralelo — 8 de noviembre de 2026

**Resultado: tres juguetes ejecutados en paralelo, commit/push autónomos y tres revisores distintos con veredicto bueno. Las tres tareas quedaron aceptadas.** Se comprobaron por separado el rechazo de una cuarta sesión y el de rutas solapadas. No fue necesario cambiar el código del harness.

## Qué se probó

Se usó el harness publicado en `a2f64edd6ffc9394d2022c7fa8303f5813793717`, con el mismo coordinador y `~/operacion/sesiones.tsv`. Durante el ensayo master avanzó a `26c332ac5bb49f9581229c4d469ba3cf57a0bfab` con dos documentos de otra tarea. El fetch de las tres ejecutoras tomó ese commit como base real; se conservaron esos cambios al integrar. Los scripts del harness no cambiaron entre esas bases ni durante este ensayo.

Sergio autorizó expresamente esta prueba en el chat. Cada ejecutora tuvo un Git privado, su worktree y dos archivos nuevos exclusivos bajo `piloto-paralelo/a`, `/b` o `/c`, en esta carpeta. No se tocó producción, Docker, n8n, app-server ni otros servicios. Los 40 archivos con cambios previos en `~/repos/onia` conservaron sus bytes y el mismo conjunto de cambios.

| Juguete | Valores | Resultado | Verificación integrada |
|---|---|---|---|
| A | `[2,4,6]` | suma 12, máximo 6 | `PARALELO_A_OK` |
| B | `[3,5,7]` | suma 15, máximo 7 | `PARALELO_B_OK` |
| C | `[11,13,17]` | suma 41, máximo 17 | `PARALELO_C_OK` |

Cada entrega agrega sólo `resultado.json` y `verificar.py` respecto de su base. El comprobador lee desde su propia carpeta, usa stdlib, no escribe archivos y rechaza objetos discrepantes, incluidos floats y booleanos en lugar de enteros. Los revisores comprobaron respectivamente 9, 11 y 18 discrepancias en memoria.

## Concurrencia y rechazos

Las ejecutoras leyeron sus instrucciones y esperaron una señal acotada antes de crear sus entregas. La barrera permitió conservar cupos reales mientras se probaban los controles; después se liberó y las tres continuaron creando, verificando y publicando sus archivos.

- Con sólo A viva se rechazó una reserva local para `a/resultado.json`: rc=2, `Colisión de rutas`.
- También con A viva se intentó lanzar un candidato desde otra base usando el **mismo** directorio de operación: rc=2, `Colisión de rutas con sesión viva`. Esa base era una fixture sin históricos, para evitar duplicar registros canónicos en el TSV.
- Con A/B/C vivas se rechazó una cuarta sesión: rc=2, `Máximo 3 sesiones vivas`.
- En cada rechazo, el JSON del candidato conservó su hash y no se creó sesión, log, briefing efectivo, supervisor log, Git privado ni worktree del candidato. La conciliación del índice de sesiones existentes sí es una operación normal del comando.
- Dos snapshots host con barrera cerrada y otro posterior a liberarla comprobaron tres PID reales vivos, identidades de arranque y SID distintos, cada proceso en su worktree correcto.

Solape mínimo acreditado por los snapshots: **15,405 segundos**, del 19:52:56 al 19:53:11 UTC; incluye una observación unos cinco segundos después de liberar. Intersección de los intervalos registrados de ejecución: **66,600 segundos**, desde el inicio de C hasta el fin de A. Son tiempos de sesiones/procesos, **no de CPU ni de carga intensiva**. No se afirma un benchmark de rendimiento ni operación continua.

El candidato de cuarta sesión quedó `en_espera`, sin reserva ni sesiones, con “no lanzar: control negativo concluido” como siguiente paso. La fixture de colisión tiene el mismo propósito documental; ninguno es una entrega ejecutada o aceptada. Se conserva su snapshot como evidencia y la fixture completa en `~/operacion/controles/paralelo-20261108/base-control`. El worktree de control se retiró después de cotejar los 27 archivos preservados y confirmar que su base no estaba referenciada en el TSV; la rama se conserva.

## Publicación, revisión y aceptación

Los eventos de cada ejecutora acreditan sus propios `git add`, `git commit` y `git push`, rc=0. Se contrastó HEAD con `git ls-remote` y se exigió el commit en origin mediante `cerrar`. El coordinador hizo esas comprobaciones, los cierres y la integración posterior; no publicó las entregas por las ejecutoras.

| Tarea | Commit autónomo | Session ID ejecutor | Session ID revisor | Resultado |
|---|---|---|---|---|
| A | `46cad1ad0518432feabcbb9e3602ba48dece35d9` | `01a1bcb8-1064-7bd2-8f99-71dcfab73181` | `01a1bcbb-07c8-7a53-9c28-baa2437fab3e` | bueno / aceptado |
| B | `df775d2eadb70d9db2efe1eb8562f366b6ea0e9c` | `01a1bcb8-4e59-7e53-97a4-72520c2ccfff` | `01a1bcbb-0f45-7693-91a9-4fe35ed41a30` | bueno / aceptado |
| C | `85bc563fe2b96ed54b7b0748a9973f2a8d50ac94` | `01a1bcb8-4ee7-7c01-945c-9f0abd7e6263` | `01a1bcbb-1713-7101-99ac-47a434dd8dd2` | bueno / aceptado |

Los seis SID son distintos. Las tres ejecutoras usaron `workspace-write` con escritura adicional limitada a sus metadatos Git privados; los tres revisores usaron `read-only`. Todos registraron `approval_policy=never`, `gpt-6.1-sol`, esfuerzo `low` y login ChatGPT exigido. Cada revisor cotejó los seis criterios, la entrega y la evidencia de concurrencia/rechazos; después se recogió su veredicto bueno, se aceptó y se liberó la reserva.

Los worktrees de las seis sesiones se retiraron limpios; ramas y repositorios Git privados se conservaron. Cero procesos del piloto vivos al terminar. Los commits originales se integraron secuencialmente, sin reescribirlos: avance rápido de A y merges de B/C. Los tres verificadores dieron OK sobre el árbol combinado.

Registros canónicos: [A](../../04-operacion-agentes/tareas/harness-paralelo-a-20261108.json), [B](../../04-operacion-agentes/tareas/harness-paralelo-b-20261108.json), [C](../../04-operacion-agentes/tareas/harness-paralelo-c-20261108.json). [Control de cuarta sesión](../../04-operacion-agentes/tareas/harness-paralelo-cuarta-20261108.json).

## Evidencia y pruebas

[Evidencia común](../../04-operacion-agentes/evidencias/harness-paralelo-20261108/): preflight/cuota, snapshots host y reloj monotónico, los tres rechazos, procedimiento puntual ejecutado, snapshots de la fixture, entregas, aceptaciones, conservación y comprobaciones. Evidencia por entrega: [A](../../04-operacion-agentes/evidencias/harness-paralelo-a-20261108/), [B](../../04-operacion-agentes/evidencias/harness-paralelo-b-20261108/), [C](../../04-operacion-agentes/evidencias/harness-paralelo-c-20261108/). Incluye extractos de comandos/salidas, runtime observado, recibo de cierre, veredicto y aceptación; los logs completos permanecen privados en `~/operacion/logs/`.

- Suite del harness previa al ensayo: **125 casos; 124 aprobados, uno omitido por Windows y cero fallos**, 27,531 s. El código del harness se conservó sin cambios.
- `doctor`: 30/30; `bash -n`: seis scripts; `git diff --check`: correcto.
- Prueba real: tres publicaciones propias, tres veredictos buenos, seis SID diferentes, tres controles negativos correctos y tres verificadores correctos sobre el árbol integrado.
- Ningún comando de las seis sesiones terminó con código distinto de cero. Los rechazos rc=2 pertenecen a los controles deliberados del coordinador.

## Comandos y consulta

Los lanzamientos realizados usaron el CLI existente; el procedimiento intercaló los controles y la barrera:

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
for letra in a b c; do
  python3 "$H" lanzar "harness-paralelo-${letra}-20261108" --revision-esperada 3 \
    --actor "paralelo-ejecutor-${letra}" --si-sergio \
    --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt
done
```

Para cada ID se ejecutó cierre con su revisión vigente, luego `revisar --actor paralelo-ejecutor-LETRA --revisor paralelo-revisor-LETRA --si-sergio --modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt`, recogida del veredicto y aceptación. El [procedimiento del ensayo](../../04-operacion-agentes/evidencias/harness-paralelo-20261108/procedimiento-ejecutado.txt) conserva los comandos exactos de los rechazos; es evidencia de una ejecución puntual, no otro lanzador ni una instrucción para repetir estos IDs aceptados.

Consultas actuales:

```bash
cd ~/repos/onia-coordinador
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py estado
for letra in a b c; do
  python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py retomar "harness-paralelo-${letra}-20261108"
  python3 "_investigacion-onia/base-operativa/05-herramientas/2026-11-08-harness/piloto-paralelo/${letra}/verificar.py"
done
```

## Cuota y límites

Sólo se usó la cuota incluida del login ChatGPT existente, sin API keys, compras ni créditos adicionales. La observación previa era 12% de cuota semanal usada; los últimos datos de los tres revisores muestran 13% y saldo adicional cero. Es una cuota compartida con coordinación y otras sesiones: ese cambio no mide aisladamente el coste del piloto ni representa un importe monetario.

Quedó comprobado el alcance solicitado. La prueba no mide cargas intensivas, fallos del VPS ni operación 24/7. El aislamiento de archivos no impone una ACL sobre las ramas remotas permitidas por la credencial GitHub. No se activó un servicio ni una cola nueva.

Arreglo existente, juguetes y resultados quedan en `origin/master`. El hash final verificado se incluye en el recibo externo `~/operacion/resultados/harness-paralelo-real-2026-11-08.md`. [Lecciones y controles](../../04-operacion-agentes/registro-de-errores.md#tres-sesiones-paralelas-reales--8-de-noviembre-de-2026).

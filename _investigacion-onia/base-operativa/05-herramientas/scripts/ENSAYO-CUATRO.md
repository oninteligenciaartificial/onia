# Control temporal de cuatro sesiones

Entrega técnica para revisión independiente del commit publicado. El ensayo real queda pendiente de esa revisión y de la coordinación del operador. Los comandos siguientes corresponden a esa etapa posterior.

`harness_ensayo.py` extiende la admisión de `harness_sesiones.py`. El registro canónico y el índice global existentes conservan su función. La política vive en `OPERACION/ensayo-cuatro/`, con su directorio privado 0700, archivos 0600, dueño actual y rechazo de enlaces simbólicos y duros en los documentos de control. La carpeta de operación debe pertenecer al usuario actual, permitir escritura sólo a su dueño y ser la única utilizada por todas las entradas del host.

## Contrato

- El límite habitual es tres. La presencia de `ensayo-cuatro` exige una política íntegra y vigente, un monitor vivo identificado por PID e inicio Linux y recibos íntegros. Una carpeta incompleta, STOP o una comprobación fallida bloquea la admisión.
- El permiso comprende una sola base absoluta y una lista explícita de IDs distintos. La preparación requiere el registro global libre para vincular todos los intentos del lote al permiso. Ejecutoras, revisores y reservas de preguntas comparten los cuatro lugares. Una quinta solicitud, un ID duplicado o una colisión de escritura se rechazan.
- Cada intento de sesión queda vinculado a la huella de la política. Sol high, login ChatGPT y cero hijos son obligatorios para lanzar o reanudar ejecutoras y revisores. Las preguntas conservan su contrato existente de Sol low y herramientas deshabilitadas, con la misma comprobación global y pertenencia al lote.
- La vigencia máxima es 1.800 segundos desde la preparación. Recursos y latido vencen a los 15 segundos, la cuota vence a los 60 segundos. Se rechazan muestras futuras, no finitas, incompletas y cambios de ventana de cuota. El monitor toma muestras aproximadamente cada cinco segundos y termina ante caducidad o STOP.
- El presupuesto es dos puntos porcentuales desde la lectura fresca inicial, en la ventana primaria y también la secundaria cuando el proveedor la entrega. Se detiene al observar un incremento de dos puntos, agotamiento, retroceso o cambio de ventana. Una secundaria ausente o null no se inventa; cualquier cambio del conjunto de ventanas durante el ensayo bloquea. El proveedor entrega porcentajes muestreados y el consumo en curso puede avanzar entre lecturas. Los recibos permiten comprobar el consumo observado. Esta entrega deja pendiente medir ese comportamiento durante el ensayo autorizado.
- Los umbrales iniciales elegidos para esta implementación son CPU menor que 85 %, RAM disponible al menos 20 %, PSI `some avg10` de CPU menor que 20 y de memoria e I/O menor que 10, swap utilizado hasta 25 % y actividad de swap menor que 256 páginas por segundo. Son decisiones conservadoras para revisión. CPU y swap se calculan con diferencias de contadores durante 0,2 segundos. Una plataforma que carezca de esos contadores queda bloqueada.
- La lectura de cuota utiliza `initialize` y `account/rateLimits/read` del app-server local, con el contrato cotejado en `/tmp/onia-read-quota-rpc.py`. El código incorpora la lectura acotada y la limpieza con PID verificado y SIGTERM. La respuesta privada se proyecta a porcentajes, duración y reinicio de ventanas y se guarda en los recibos privados.

La integridad se coteja mediante huellas entre preparación, política, estado, recibos e inventario. Estos controles detectan alteraciones de documentos y permisos. El propietario del usuario del sistema administra esa confianza. Todos los coordinadores y el puente deben ejecutar esta misma versión del código y compartir operación para que el límite global se aplique.

## Despliegue en un checkout separado

Después del veredicto independiente favorable sobre la entrega exacta, recuperar la rama publicada y crear un checkout limpio. Sustituir las rutas de ejemplo por las del host. El comando `worktree add` debe fallar si el destino ya existe.

```bash
REPO="$HOME/repos/onia"
CODIGO="$HOME/repos/onia-control-cuatro-revisado"
git -C "$REPO" fetch origin refs/heads/codex/ws-ensayo-cuatro-control-20261112
COMMIT_ENTREGA="$(git -C "$REPO" rev-parse FETCH_HEAD)"
git -C "$REPO" worktree add --detach "$CODIGO" "$COMMIT_ENTREGA"
git -C "$CODIGO" status --short
git -C "$CODIGO" rev-parse HEAD
```

Cotejar `COMMIT_ENTREGA` con el hash aprobado. Los archivos y el índice de trabajo del checkout de origen se conservan. El código del CLI y del puente debe apuntar al checkout revisado. Su `--base` y la configuración privada del puente siguen apuntando al registro canónico del coordinador. Conservar su configuración de Git y el mismo directorio de operación. Evitar aplicar estos archivos parcialmente sobre un checkout con cambios.

```bash
SCRIPTS="$CODIGO/_investigacion-onia/base-operativa/05-herramientas/scripts"
H="$SCRIPTS/harness.py"
E="$SCRIPTS/harness_ensayo.py"
BASE_CANONICA="$HOME/repos/onia-coordinador/_investigacion-onia/base-operativa"
OPERACION="$HOME/operacion"
python3 -m unittest discover -s "$SCRIPTS" -p 'test_harness_*.py'
python3 "$H" --base "$BASE_CANONICA" --operacion "$OPERACION" estado
```

Conciliar cualquier ocupación o registro desconocido antes de preparar. Reemplazar `ensayo-a` a `ensayo-d` por los IDs autorizados concretos. Para una pregunta se autoriza su `id_pregunta`. La base autorizada debe coincidir exactamente con la base del puente y de las sesiones.

## Preparación

```bash
python3 "$E" --operacion "$OPERACION" preparar \
  --base "$BASE_CANONICA" --segundos 1800 \
  --id ensayo-a --id ensayo-b --id ensayo-c --id ensayo-d
```

La salida `preparado` exige iniciar el monitor para poder admitir trabajo. Una lectura de cuota o recursos fallida devuelve `bloqueado`. Se conserva una carpeta creada parcialmente con STOP para su diagnóstico. Una preparación repetida conserva los documentos anteriores y falla.

## Monitor y admisión

Mantener el monitor en primer plano en la terminal del operador durante todo el ensayo.

```bash
python3 "$E" --operacion "$OPERACION" monitor
```

En otra terminal, repetir las variables anteriores y comprobar el control.

```bash
python3 "$E" --operacion "$OPERACION" estado
```

`listo` acredita las comprobaciones de ese instante. El lanzamiento continúa mediante el harness habitual, usando la revisión actual y el actor asignado. Ejemplo para un ID ya preparado y autorizado en el registro canónico, sustituyendo `REVISION_ACTUAL` y `ACTOR_ASIGNADO`.

```bash
python3 "$H" --base "$BASE_CANONICA" --operacion "$OPERACION" retomar ensayo-a
python3 "$H" --base "$BASE_CANONICA" --operacion "$OPERACION" lanzar ensayo-a \
  --revision-esperada REVISION_ACTUAL --actor ACTOR_ASIGNADO --si-sergio \
  --modelo gpt-6.1-sol --esfuerzo high --auth-chatgpt --subagentes-maximos 0
```

`reanudar` y `revisar` usan los mismos controles. Se comprueba otra vez el permiso después de Git y antes de abrir la compuerta del proceso. Las preguntas revalidan antes de abrir su proceso y antes de ejecutar el CLI. El monitor devuelve `parado` o `bloqueado` al detenerse. Un monitor muerto o un RPC lento hacen caducar la admisión.

## Fin y conservación

```bash
python3 "$E" --operacion "$OPERACION" fin
```

`fin` escribe STOP bajo el lock global antes de enviar señales. Selecciona los intentos vinculados al permiso, sus descendientes observados con ascendencia comprobada y el inventario ligado al estado. Abre un pidfd, vuelve a verificar propietario y PID con inicio, y envía SIGTERM por ese descriptor. Un PID reciclado se omite. Conserva logs, worktrees, ramas y recibos. Espera hasta cinco segundos y comunica los procesos o reservas pendientes. Los supervisores del harness pueden terminar de persistir su resultado durante esa espera.

Si el inventario o la pertenencia no pueden comprobarse, la salida es `bloqueado` y STOP conserva cerrada la admisión. Los auxiliares que se hayan desprendido antes de poder observar su ascendencia requieren conciliación por el operador con identidades verificadas. Ante procesos persistentes, conservar el bloqueo y sus recibos. La parada automática actúa sobre los procesos cuya identidad y pertenencia pudo comprobar.

Esperar la salida del monitor, repetir `fin` si quedan supervisores finalizando y comprobar `estado` del harness. Después de obtener `parado`, cero procesos/reservas del lote y monitor terminado, archivar la carpeta completa para volver al límite habitual de tres. Conservar su contenido privado.

```bash
ARCHIVO_ENSAYO="$OPERACION/ensayo-cuatro-cerrado-$(date -u +%Y%m%dT%H%M%SZ)"
test ! -e "$ARCHIVO_ENSAYO"
mv --no-clobber "$OPERACION/ensayo-cuatro" "$ARCHIVO_ENSAYO"
```

## Evidencia local reproducible

```bash
python3 -m unittest discover -s "$SCRIPTS" -p 'test_harness_ensayo.py'
python3 -m unittest discover -s "$SCRIPTS" -p 'test_harness_sesiones.py'
python3 -m unittest discover -s "$SCRIPTS" -p 'test_harness_preguntas.py'
```

Las pruebas usan directorios privados temporales, Git local, cuota sintética y procesos sintéticos. Cubren tres por defecto, cuarta, quinta, preguntas y revisores, autorizaciones, duración, recursos/cuota caducos, alteraciones, permisos, enlaces, colisiones, PID reciclado y parada SIGTERM con conservación. La validación sobre Windows/WSL, los umbrales bajo carga y el consumo real del ensayo quedan pendientes del operador y la revisión independiente. Los comandos de esta guía permiten preparar esa comprobación posterior.

Verificación local del 12 de noviembre de 2026 en Linux mediante la suite completa de `scripts/test_*.py`, 270 casos ejecutados, 269 correctos y uno omitido porque las junctions requieren Windows. Sintaxis de los seis archivos Python modificados y `git diff --check` comprobados. El ciclo de monitor CLI también pasó con RPC y recursos sintéticos y SIGTERM. La revisión independiente corresponde al coordinador sobre el commit publicado.

Corrección de coordinadora posterior a esa suite: la cuenta real entrega `secondary=null`. Se admite primaria obligatoria y secundaria opcional, conservando presupuesto y rechazo si cambia el conjunto de ventanas. Suite específica actual: 29/29. RPC real de sólo lectura en el VPS el 12-nov UTC: primaria disponible, 42 % usado, presupuesto validado contra la misma muestra; ninguna política activada. La suite completa anterior no acredita esta corrección; los casos nuevos comprueban RPC sintético con secundaria null, agotamiento de dos puntos, aparición/desaparición de ventanas y datos malformados.

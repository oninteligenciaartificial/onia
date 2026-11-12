# Continuidad operativa de lotes

Un único `onia-continuidad.timer` de usuario invoca `continuidad.py` cada minuto. La coordinadora instala esta entrega después de su revisión; esta sesión no habilita el temporizador. El adaptador recorre una lista privada ordenada y ejecuta **un tick como máximo por lote y por pasada**. El estado sigue en `trabajo.py`; las intenciones, recuperaciones y efectos siguen en `harness_lote.py`. La lista es configuración aprobada, no otro registro de tareas.

Se reutilizan sin modificaciones el [despachador y su contrato](../continuidad-lote-20261111/README.md), sus journals y locks, `--cuota-codex`, las API canónicas y los tres cupos globales. El adaptador no acepta, integra ni despliega. No lanza otras tareas ni crea IDs. Una excepción de API puede dejar una intención pendiente: el siguiente tick recupera el efecto reconocido o pide conciliación, según las comprobaciones existentes.

## Configuración privada

Copiar `lista-deshabilitada.json` fuera de Git, sustituir los ejemplos y mantener permisos `0600`, directorio `0700`. También es válida una lista vacía: `{"schema":1,"lotes":[]}`. No usar datos reales en los tests.

| Campo por lote | Contrato |
| --- | --- |
| `id` | Identidad exacta del manifiesto; única en la lista |
| `orden` | Entero >=0 único; menor primero, independiente de la posición en JSON |
| `habilitado` | Booleano; además el manifiesto debe estar habilitado, aprobado y vigente |
| `manifiesto` | Ruta absoluta al manifiesto privado ya aprobado |
| `manifiesto_sha256` | Hash canónico aprobado obtenido con `harness_lote.py … hash`; **no** el `sha256sum` del archivo JSON |
| `operacion` | La misma ruta absoluta `HOME del usuario coordinador/operacion` en todos los lotes; no admite otro registro para eludir cupos |
| `observaciones` | `null` o ruta absoluta a las declaraciones canónicas de la coordinadora |
| `limite_segundos` | Entero entre 5 y 120; plazo de un tick, no plazo del trabajo Codex supervisado |

Máximo 16 entradas y suma de límites <=480 segundos, con hasta 5 segundos adicionales de terminación por entrada. El servicio tiene un límite externo de 10 minutos. El plazo de cada lote asegura que un bloqueo no monopolice la pasada. Se rechazan IDs, órdenes y rutas de manifiesto duplicados. Los lotes que compartan tareas siguen sujetos al estado y a los cupos canónicos; la coordinadora debe mantener un solo dueño del despacho y evitar incluir el mismo trabajo en varios lotes.

Toda la lista se valida antes de operar: estructura inválida bloquea la pasada completa. Un manifiesto ausente, inválido, alterado, expirado, detenido o con otra operación bloquea únicamente su entrada; los demás continúan. El worker compara el hash de la lista con el de la pasada antes de actuar; una sustitución concurrente queda para la siguiente pasada. El manifiesto y las observaciones se revalidan en el despachador antes del efecto. Cambiar una aprobación exige revisar de nuevo su alcance; el adaptador nunca recalcula una aprobación para seguir.

Las observaciones conservan su contrato original: hash del manifiesto y fecha reciente (hasta 120 segundos). Con cuota directa, una declaración antigua se ignora, sin refrescar su fecha ni convertirla en evidencia nueva. Si se configuró una ruta ausente, ilegible, futura o perteneciente a otro manifiesto, se bloquea ese lote. Escribir mediante reemplazo atómico, nunca modificar el archivo mientras se lee. La cuota se obtiene del proveedor sólo para lanzar/reanudar/revisar; cerrar y recoger pueden avanzar con cuota agotada.

## Qué avanza y qué espera

| Paso | Condición y responsable |
| --- | --- |
| Lanzar/reanudar/revisar | Automático sólo con cobertura explícita en manifiesto, cuota incluida vigente, presupuesto y cupo. La retoma requiere el mismo SID y conciliación de auxiliares; no relanza desde cero. |
| Recuperar tras caída | Automático si journal y registro acreditan exactamente el efecto. Una intención incierta espera evidencia de la coordinadora mediante `conciliar-sin-efecto`; no se borra ni se repite a ciegas. |
| Cerrar | Automático únicamente tras declaración explícita reciente de la coordinadora sobre el commit exacto (`cierres[ID]`, `verificacion=correcta`, resultado y comprobación). Ella debe cotejar antes el artefacto esperado, su contenido/hash y pruebas contra el criterio. La API comprueba diff limitado a rutas, publicación, identidad, HEAD y limpieza. No se genera una declaración desde `rc=0`, un mensaje del agente o la mera existencia de un archivo. |
| Recoger | Automático al terminar la revisión, con las comprobaciones existentes de sesión distinta, commit, digest y recibo. Una revisión recogida impide duplicar la revisión. |
| Reabrir tras cambios | Coordinadora: diagnosticar, reabrir por API existente y aprobar la retoma del mismo SID. |
| Aceptar/integrar/desplegar | Coordinadora, con veredicto bueno vigente del commit exacto y autorización aplicable. Integrar secuencialmente, comprobar y verificar `origin/master`; desplegar sólo con sus controles y permisos. Estar en el manifiesto no ejecuta estos pasos. |

Se conserva la ruta aceptada de observaciones y recogida. No se añadió un verificador que invente pruebas, aceptaciones o evidencia de artefactos. Los controles de entrada del harness siguen siendo la autoridad. Un tick puede conciliar una intención previa y hacer una transición nueva; no se repite el efecto recuperado.

## Preparación e instalación reproducible

Ejecutar **en el checkout coordinador estable**, después de integrar y comprobar el commit revisado. No apuntar la unidad al worktree ejecutor que `cerrar` retirará. No trasladar los registros al worktree.

```bash
cd "$HOME/repos/onia-coordinador"
CONT_REPO="$PWD"
CONT_DIR="$CONT_REPO/_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/continuidad-operativa-20261111"
CONT_LISTA="$HOME/operacion/continuidad-lista.json"
CONT_LOTE="$CONT_REPO/_investigacion-onia/base-operativa/05-herramientas/scripts/harness_lote.py"

# Preparar privadamente lista y manifiestos, cotejar cada sí y hash, sin copiar secretos a Git.
python3 -B "$CONT_DIR/continuidad.py" --repo "$CONT_REPO" --lista "$CONT_LISTA" --validar
command -v codex
# Sustituir ~/.local/bin si command -v muestra otra carpeta del CLI autenticado.
python3 -B "$CONT_DIR/instalar.py" --repo "$CONT_REPO" --lista "$CONT_LISTA" --codex-bin "$HOME/.local/bin"
systemd-analyze --user verify "$HOME/.config/systemd/user/onia-continuidad.service" "$HOME/.config/systemd/user/onia-continuidad.timer"
```

El instalador sólo escribe esas dos unidades; no llama a `systemctl`, no habilita servicios y rechaza sobrescribir unidades diferentes o enlaces. Repetir con las mismas entradas produce los mismos bytes. Se puede preparar y validar en un directorio temporal con `--destino /tmp/onia-unidades-revisadas`. Las rutas de las unidades admiten letras ASCII, números, `/`, `.`, `_` y `-`; si contienen espacios o caracteres especiales, preparar una ruta estable compatible. No se crea un alias ni enlace automáticamente.

Antes de activar, revisar que no quede habilitado un timer anterior por lote que despache el mismo trabajo. Inventariar con `systemctl --user list-timers --all`; sólo detener una instancia anterior cuando se haya identificado como parte de esta sustitución y esté cubierta por la revisión. Conservar sus unidades y sus journals. Esta entrega no cambia otros servicios.

Comprobar `loginctl show-user "$(id -un)" -p Linger`: para arrancar tras reinicio sin login debe estar `Linger=yes`. El entorno de prueba devolvió `yes`. Si falta en el VPS definitivo, la coordinadora deja ese requisito al administrador; este instalador no usa sudo ni cambia linger. Una vez que corre el gestor de usuario, el timer y los supervisores no necesitan el chat abierto. Según [systemd.timer](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html), `Persistent=true` conserva el último disparo y recupera una activación perdida; no reproduce cada minuto perdido ni duplica una unidad ya activa.

## Puesta en marcha revisada — coordinadora

La autorización de puesta en marcha del briefing se reutiliza dentro de su alcance. Falta la revisión independiente de esta entrega y el cotejo de la lista concreta, no otro permiso general.

```bash
# Registrar HEAD, hashes aprobados, hora y usuario antes del primer disparo.
git rev-parse HEAD
systemctl --user daemon-reload
# Primera pasada acotada; revisar estado canónico, logs y supervivencia de su supervisor.
systemctl --user start onia-continuidad.service
journalctl --user -u onia-continuidad.service -n 30 --no-pager -o cat
# Tras comprobar esa pasada, habilitar el único temporizador.
systemctl --user enable --now onia-continuidad.timer
systemctl --user list-timers onia-continuidad.timer --all
systemctl --user status onia-continuidad.service onia-continuidad.timer --no-pager
```

`KillMode=process` sigue el patrón del disparador aceptado: permite que el supervisor canónico siga trabajando después de terminar la pasada. El padre termina sólo su worker al vencer el plazo o recibir SIGTERM, con gracia de hasta 5 segundos y luego SIGKILL sólo a ese PID. Nunca señala grupos de trabajo del harness. La consulta de cuota tiene su propia limpieza. Si se fuerza SIGKILL, puede quedar un auxiliar previo al efecto: conservar evidencia y comprobar procesos antes de declarar `sin_efecto`. No repetir intentos por esa incertidumbre. La semántica de señales procede de [systemd.kill](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html); la supervivencia se probó con una unidad transitoria sintética, no con Codex real.

## Registro y diagnóstico

El único historial de efectos continúa en `~/operacion/lotes/ID/journal.jsonl` con su cadena de hashes y en los registros canónicos. El adaptador imprime una línea JSON breve por lote a journald: ID/orden, hash aprobado, fecha, resultado, avances (`id`, operación, clave, revisión), próxima acción por tarea y digest/cantidad de eventos del journal. La línea final muestra `avanzados=0` cuando nada avanzó; una lista vacía muestra `sin_lotes`. No se relanza para fabricar actividad. Este log es una vista, no se utiliza para decidir ni recuperar estado.

No se copian mensajes arbitrarios, criterios, comprobaciones, stderr, URLs ni salidas de Codex/Git al log. Los bloqueos se agrupan en códigos como `cuota_o_autenticacion`, `tres_cupos_ocupados`, `evidencia_coordinadora`, `conciliar_journal_sid`, `diagnosticar_intentos`, `reserva_de_rutas` y `control_canonico`. Un error fuera del contrato devuelve `worker_fallido`; inspeccionar las entradas privadas y el plan existente. El proceso padre continúa con los otros lotes. Un servicio que terminó correctamente puede contener lotes bloqueados: mirar las líneas, no sólo el código de salida.

```bash
journalctl --user -u onia-continuidad.service --since today --no-pager -o cat
# Para el lote afectado, usar su ruta privada real:
python3 -B "$CONT_LOTE" --manifiesto "$HOME/operacion/lote-aprobado.json" plan
# El estado de procesos y las revisiones siempre se cotejan con el harness existente:
python3 -B "$CONT_REPO/_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py" estado
```

## Pausa, recuperación y rollback

Pausa global reversible, sin revocar los lotes: `systemctl --user disable --now onia-continuidad.timer`. Esto evita nuevos disparos y permite terminar la pasada ya admitida. Si también debe interrumpirse esa pasada: `systemctl --user stop onia-continuidad.service`; no detiene los trabajos ya supervisados. Retomar con `enable --now` sólo tras conciliar la evidencia y la vigencia de los manifiestos.

STOP de un lote, sin frenar los demás:

```bash
python3 -B "$CONT_LOTE" --manifiesto "$HOME/operacion/lote-aprobado.json" revocar --motivo 'STOP de la coordinadora'
```

Conservar `STOP.json`, journal, SID y registros. Una operación admitida concurrentemente puede terminar de registrarse. La reactivación requiere conciliación y autoridad explícita; no se borra STOP automáticamente. Para una intención sin efecto comprobado, usar el comando canónico `conciliar-sin-efecto` documentado en el despachador, con la misma clave/revisión y evidencia concreta de procesos, worktree y logs. Nunca truncar/rehashear el journal para continuar.

Rollback del paquete: deshabilitar el timer y detener el servicio como arriba; conservar copia privada de ambas unidades instaladas. Si sustituyó unidades anteriores de estos mismos nombres, restaurar esos dos archivos desde la copia comprobada y ejecutar `systemctl --user daemon-reload`. Si eran nuevos, retirar sólo `onia-continuidad.service` y `onia-continuidad.timer` de `~/.config/systemd/user` después de conservarlos, y ejecutar `daemon-reload`. No ejecutar `systemctl clean`, no borrar journals/STOP/registro ni cancelar sesiones vigentes para desinstalar el disparador. No revertir master ni otros servicios. La retirada no deshace entregas canónicas ya registradas.

## Verificación reproducible

Desde la raíz del checkout:

```bash
python3 -B -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/continuidad-operativa-20261111 -p 'test_*.py' -v
python3 -B -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p 'test_*.py'
git diff --check
```

La suite del adaptador usa dobles, Git local y ejecutor/revisor sintéticos; prueba orden, plazo, reanudación del journal tras caída sin duplicación, STOP, caducidad, hash, evidencia fresca/caducada, cuota, cupos, cierre y recogida única. La instalación se ejecuta dos veces en temporal y valida unidades con `systemd-analyze --user verify`. Si hay gestor de usuario accesible, crea una única unidad transitoria de prueba, conserva al supervisor sintético y la retira; si no lo hay, informa la omisión y conserva la validación estática. No habilita el timer entregado, no llama a Codex real ni mide cuota real. Evidencia y límites observados: [EVIDENCIA.md](EVIDENCIA.md).

# Recurrencia instalable de la cola CPU

Entrega del encargo `onia-homelab-continuidad-cpu-20261111`. Reutiliza sin cambios [cola_homelab.py](../cola_homelab.py), [worker_render.py](../worker_render.py) y su [contrato comprobado](../COLA-CPU.md). No depende del despachador, Codex, su cuota ni nuevas sesiones. Sólo admite `render-sintetico-v1`, el perfil existente. Preparado para revisión; no se instaló ni activó una recurrencia permanente.

`pasada.py` llama a `Queue.tick`: a lo sumo un intento por invocación, los mismos registros y MP4, lock local y lock remoto heredado por FFmpeg. En instalación se copia la versión exacta de ambos módulos y se registra su SHA-256; no mantener un fork ni modificar la cola canónica. Los medios y estados quedan privados en el VPS. El paquete no contiene claves ni medios.

La unidad usa `Type=oneshot`, `TimeoutStartSec=80s`, parada local de hasta 10 s, `KillMode=control-group`, prioridad 10, cuota CPU de 25 % de un núcleo, 256 MiB y 16 tareas. Esos límites afectan al cliente VPS; los límites del render remoto siguen en el worker original. Sin reinicio automático del servicio. El timer espera 15 s al arrancar y 60 s después de finalizar cada pasada, con precisión de 1 s. No recupera disparos históricos (`Persistent=false`). La elección de tiempo relativo y timeout sigue [systemd.timer](https://www.freedesktop.org/software/systemd/man/256/systemd.timer.html) y [systemd.service](https://freedesktop.org/software/systemd/man/latest/systemd.service.html); la sintaxis se contrastó además en systemd 255 local.

## Estados y parada

| Condición | Resultado y siguiente paso |
|---|---|
| Existe `continuidad-cpu-v1/STOP` (incluso enlace roto) | `detenido`, código 0; no abre la cola. Se vuelve a comprobar antes de transportar. El timer puede seguir despertando sin ejecutar trabajo. |
| Cola vacía, todos entregados o reintentos aún no vencidos | `sin_trabajo`, código 0, sin construir el comando SSH ni leer configuración de SSH. |
| `ONIA_HOMELAB_SSH=0` o argumento `--sin-ssh`, con pendiente | No conecta; deja `reintento` con motivo `ssh_deshabilitado`. Consume un intento, conserva el ID y el backoff. |
| Lock de cola ocupado | `ocupado`, sin otro intento. |
| Worker ocupado, SSH offline/255 o respuesta perdida/timeout | Reintento del mismo ID con espera creciente de 2 a 300 s, respetada por ticks posteriores. El reloj de 60 s puede demorar más la retoma. |
| Hash/ID/respuesta inválidos o error del worker | `bloqueado`, código 1; no entregar bytes corruptos. Ese ID queda excluido hasta inspección; el timer no se desactiva solo. |
| Error local, JSON corrupto, directorio no privado o configuración inválida | `fallo_local`, código 1; journal saneado, sin imprimir rutas o respuestas privadas. |
| Cliente terminado entre `en_curso` y guardado del recibo | Otra pasada recupera el mismo ID desde `en_curso`; si el worker publicó salida, la reutiliza. Un intento parcial anterior puede renderizarse de nuevo. |

`STOP` es cooperativo: no aborta un SSH/render que ya empezó. Para una parada controlada, crear `STOP`, detener el timer y dejar finalizar la pasada (hasta 80 s). Una parada inmediata del servicio termina el grupo local, sin prometer cancelar el render remoto; éste conserva su lock y la siguiente recuperación usa el mismo ID. No eliminar registros ni cambiar IDs para reintentar. No hay límite global de intentos offline: para una indisponibilidad prolongada, usar `STOP`.

## Comprobar sin instalar

Desde esta carpeta, con Python 3.10+ en Linux:

```bash
python3 -B -m unittest -v test_continuidad
(cd .. && python3 -B -m unittest -v test_cola_homelab)
systemd-analyze --user verify systemd/onia-homelab-cpu.service systemd/onia-homelab-cpu.timer
```

Si `verify` avisa que su socket privado está ocupado por el gestor del usuario, verificar con un runtime temporal propio:

```bash
python3 -I -B - <<'PY'
import os, subprocess, tempfile
with tempfile.TemporaryDirectory(prefix="onia-systemd-verify-") as runtime:
    subprocess.run(["systemd-analyze", "--user", "verify",
                    "systemd/onia-homelab-cpu.service", "systemd/onia-homelab-cpu.timer"],
                   env={**os.environ, "XDG_RUNTIME_DIR": runtime}, check=True)
PY
```

Prueba real de programación **local y temporal**, sin conexión a la PC, con FFmpeg/FFprobe disponibles en VPS:

```bash
T=$(mktemp -d /tmp/onia-cola-timer.XXXXXX)
python3 -I -B ensayo_timer.py --dest "$T/ensayo"
```

El fixture usa un paquete nuevo, el worker original en un home temporal, un ID sintético y un timer transitorio exclusivo. Reproduce los límites del servicio, comprime el intervalo a 2 s y cambia sólo el transporte por una llamada local a `worker.execute`; las funciones SSH fallan si se invocan. Exige `entregado` → `sin_trabajo`, un único intento de render, SHA idéntico en ambos extremos y parada por archivo; detiene únicamente sus dos unidades al salir y verifica que no queden activas. Conserva el temporal privado para inspección. No prueba el transporte SSH ni el intervalo de 60 s en producción. Si systemd no está disponible, conservar el fallo y repetir este comando desde el VPS coordinador; las pruebas de fixtures y `verify` siguen siendo reproducibles sin acceso a la PC.

Para comprobar el CLI sobre una cola vacía sin SSH (sin preparar claves):

```bash
T=$(mktemp -d /tmp/onia-cola-vacia.XXXXXX)
python3 -I -B pasada.py --root "$T/cola" --stop "$T/STOP" --sin-ssh
```

Debe imprimir `{"estado": "sin_trabajo"}`. Las pruebas también comprueban cola vacía con SSH habilitado y funciones de SSH/procesos prohibidas.

## Instalación después de revisión

Ejecutar como el usuario VPS que ya tiene `~/operacion/homelab`, nunca con sudo. `preparar.py` no ejecuta systemctl: crea un destino nuevo 0700, archivos 0600, `STOP`, `config.env` con SSH deshabilitado y `SHA256SUMS`. Si existe el destino, falla sin sobrescribirlo. No cambia permisos de rutas existentes ni crea otra cola. El servicio apunta a la cola privada original `~/operacion/homelab/cola-cpu-v1`.

Comandos para el coordinador, desde esta carpeta, sólo tras revisar la entrega:

```bash
set -e
D="$PWD"
P="$HOME/operacion/homelab/continuidad-cpu-v1"
U="$HOME/.config/systemd/user"
test -d "$HOME/operacion/homelab"
test ! -e "$P"
test ! -L "$P"
test ! -e "$U/onia-homelab-cpu.service"
test ! -L "$U/onia-homelab-cpu.service"
test ! -e "$U/onia-homelab-cpu.timer"
test ! -L "$U/onia-homelab-cpu.timer"
python3 -I -B "$D/preparar.py" --dest "$P"
(cd "$P" && sha256sum -c SHA256SUMS)
mkdir -p "$U"
install -m 600 "$P/systemd/onia-homelab-cpu.service" "$U/onia-homelab-cpu.service"
install -m 600 "$P/systemd/onia-homelab-cpu.timer" "$U/onia-homelab-cpu.timer"
systemd-analyze --user verify "$U/onia-homelab-cpu.service" "$U/onia-homelab-cpu.timer"
systemctl --user daemon-reload
```

Revisar la cola existente antes de retirar STOP: los pendientes previos también son elegibles. No encolar trabajo nuevo por instalar. El paquete congela sus módulos; nuevas versiones requieren otra revisión y un paquete nuevo, conservando el anterior.

Activación acotada sin SSH: conservar `ONIA_HOMELAB_SSH=0`, archivar `STOP` como `STOP.inicial` y activar **sólo** este timer:

```bash
mv "$P/STOP" "$P/STOP.inicial"
systemctl --user enable --now onia-homelab-cpu.timer
systemctl --user list-timers onia-homelab-cpu.timer --all
journalctl --user -u onia-homelab-cpu.service --since '5 minutes ago' --no-pager
```

En cola vacía debe dar `sin_trabajo`; con pendientes, modo sin SSH deja reintentos como indica la tabla. Para usar SSH tras la revisión y autorización aplicables al trabajo en cola, detener el timer, crear `STOP`, cambiar **únicamente** `config.env` a `ONIA_HOMELAB_SSH=1`, conservar su modo privado y verificar el contrato existente sin crear nuevas claves, perfiles o accesos. Después archivar STOP con un nombre nuevo y arrancar el timer. `--sin-ssh` prevalece sobre la variable. Un valor distinto de 0 o 1 falla cerrado. La huella fijada, alias, usuario, puerto, llave y ProxyCommand son exactamente los de `cola_homelab.py`.

`enable` no garantiza supervivencia del gestor de usuario al cerrar sesión ni al reiniciar. Consultar `loginctl show-user "$USER" -p Linger` y probar un disparo sin terminal, con los permisos correspondientes, antes de afirmar continuidad. Si el gestor no sobrevive, queda pendiente resolverlo por el coordinador; esta entrega no modifica linger, logon, Windows, Tailscale ni servicios de terceros.

## Reversión conservando estados y bytes

Con las variables `P` y `U` anteriores:

```bash
touch "$P/STOP"
systemctl --user disable --now onia-homelab-cpu.timer
systemctl --user show onia-homelab-cpu.service -p ActiveState -p SubState
```

Esperar que el servicio quede inactivo. Si es indispensable interrumpirlo: `systemctl --user stop onia-homelab-cpu.service`; conservar `en_curso` para recuperar el mismo ID. Archivar, sin sobreescribir archivos anteriores:

```bash
A=$(mktemp -d "$P/retiro.XXXXXX")
mv "$U/onia-homelab-cpu.service" "$A/"
mv "$U/onia-homelab-cpu.timer" "$A/"
systemctl --user daemon-reload
systemctl --user list-timers onia-homelab-cpu.timer --all
```

Conservar paquete, cola original y salidas remotas privadas. No borrar registros/MP4 ni detener Tailscale, SSH u otras unidades. Reinstalar las unidades archivadas no reinicia los IDs.

## Brechas para material real

| Brecha y estado | Responsable / próxima acción | Condición de cierre |
|---|---|---|
| Recurrencia permanente preparada; prueba sólo transitoria | Coordinador: revisar commit, instalar con STOP, verificar timer y journal vacío; después activar dentro del alcance autorizado | Disparos del servicio instalado y supervivencia del gestor de usuario comprobados. |
| SSH heredado, sin nuevo acceso en este encargo | Coordinador: cotejar contrato y evidencia previa; prueba autorizada con mismo ID si hace falta | Recuperación y hash por SSH acreditados para la versión instalada, sin nuevos perfiles. |
| Render de clientes no admitido | Contenido + coordinador: definir entrada privada inmutable, hash, perfil, límites de duración/tamaño y transferencia | Encargo específico con permisos, validación del resultado y recuperación; no reutilizar el sintético como render real. |
| ASR no admitido por esta cola | Coordinador: definir contrato ASR CPU, modelo local/licencia/recursos, entrada y salida privadas | Otro encargo y prueba con audio autorizado, hash e idempotencia. No se añaden tipos a esta cola. |
| Reinicio/suspensión de Windows y persistencia WSL no probados aquí | Sergio + coordinador: resolver en el frente de continuidad existente | Ensayo autorizado después de reinicio/suspensión, sin duplicar el render ni cambiar de ID. |

Evidencia de esta entrega: [EVIDENCIA.md](EVIDENCIA.md), recibos y hashes en `evidencia/`. No hay aceptación independiente ni integración a master por parte de esta ejecutora.

# Preparación de continuidad de Tailscale · 12 noviembre 2026

**Entrega preparada, no habilitada. La persistencia y la equivalencia con el daemon real siguen sin certificar.** No usar la plantilla directamente. No se ha instalado una unidad ni se ha detenido, reiniciado o iniciado ningún servicio.

## Evidencia local y límite

- Checkout inicial limpio, rama asignada, HEAD `da755793568cb03eab82fbbd6c4954f8776a981d`.
- `loginctl show-user <UID actual> -p Linger`: `Linger=yes`.
- systemd local 255. Las unidades de usuario `onia-panel.service` y `onia-panel-serve.service` están enabled/active/running. La segunda ejecuta nginx y Requires/After el panel; **su nombre no acredita que supervise Tailscale**. Ninguna declara dependencia del daemon.
- No se encontró unidad con `tailscaled` en los archivos legibles de `~/.config/systemd/user`, `/etc/systemd/user` y `/etc/systemd/system`. No es inventario exhaustivo de generadores, cron, unidades transitorias, otras rutas ni otros usuarios. La consulta de unidades del manager de sistema y `crontab -l` devolvieron rc=1; no permite concluir ausencia.
- El directorio runtime esperado tiene estado regular y socket Unix, ambos del UID actual. Sólo se consultó stat; no se abrió su contenido. **Eso no prueba propiedad ni actividad del proceso.**
- `/proc/1/comm` es `codex`; ninguno de los MainPID no nulos que el manager informa para el panel existe en este `/proc`. No aparece el daemon en la vista del sandbox. No se intentó salir del aislamiento. Por ello no se conocen argv, cwd, usuario/cgroup ni supervisión real del daemon. El antecedente `../CONEXION-EN-CURSO.md` registra arranque manual, no sustituye el cotejo actual.
- La cola (`../cola_homelab.py`, `ssh_command`) usa exactamente el socket previsto bajo el home y `tailscale nc`; reintenta fallos de transporte con backoff. No se ejecutó la cola, SSH ni conexión externa. Su disponibilidad real queda pendiente.
- Sólo se leyeron metadatos/argumentos necesarios; no se leyó estado Tailscale, identidad, IPs, configuración Serve, secretos, claves ni logs. No se tocó Windows, sudo, red, ACL o Serve.

## Archivos y contrato

`preparar.py` recibe un PID **ya identificado privadamente en el host** y un directorio privado nuevo fuera del repo. No busca credenciales, no llama a Tailscale ni instala nada. Rechaza una vista de procesos incompleta, otro propietario, otro ejecutable, rutas de estado/socket diferentes, modo distinto, flags desconocidos y duplicados. Conserva el orden y valores de los argumentos admitidos, incluidos puerto y formato `--flag valor` o `--flag=valor`. Si el daemon usa flags adicionales, detener preparación y revisarlos por separado: nunca descartarlos para conseguir que pase.

Produce una unidad privada y copia del guard. La plantilla `onia-tailscaled.service.in` sólo se vuelve válida tras generación. No incluye un usuario inventado: una unidad de usuario corre con el UID de su manager. Usa cwd observado, binario/estado/socket existentes; no crea runtime, estado ni login. `Type=exec` supervisa el proceso en primer plano, `Restart=on-failure` acota reintentos con límite de frecuencia. No configura disponibilidad de red ni readiness de la tailnet. No se añaden dependencias al panel/cola ni a un `network-online.target` de usuario que no garantiza la red del sistema.

`ExecCondition` ejecuta `no_duplicar.py`: bloquea ante cualquier `tailscaled` visible o socket que acepte conexión, permite un socket inexistente o que rechace conexión sin borrarlo, y falla ante dudas. La prueba de socket no envía solicitudes. No lee estado. Requiere host con PID1 systemd. No es un cerrojo contra un lanzamiento manual concurrente: antes de habilitar hay que retirar/conciliar todos los lanzadores competidores. No adopta el proceso manual ni borra sockets. stdout/stderr del daemon se descartan para evitar nuevos logs de identidad; los errores del manager deben consultarse sólo en privado. Esta decisión reduce diagnóstico, no cambia Serve.

## Procedimiento posterior: preparación privada sin interrumpir

Responsable: operador/coordinador con ejecución autorizada en el host y UID del daemon. Este encargo **no ejecutó** los pasos siguientes.

1. En el host, identificar todos los procesos `tailscaled` mediante comm/exe y cotejar propietario, argv necesarios, cwd, cgroup/ancestros y metadatos de estado/socket. Mantener PID y argumentos sólo en un recibo privado 0700/0600 fuera de Git. No usar `ps aux`, journals crudos ni imprimir entorno. Cotejar privadamente si variables de entorno del lanzador afectan al daemon; el generador no copia entorno. Si necesita alguna, resolver su equivalencia antes de habilitar, sin volcar secretos.
2. Inventariar systemd de usuario/sistema (incluidas unidades transitorias y generadas), timers, cron accesible, scripts de login/arranque y supervisor del proceso. Si ya hay persistencia, conservarla y descartar esta migración. Si no puede certificarse su ausencia, no habilitar un segundo lanzador.
3. Confirmar un único daemon del UID actual con las rutas esperadas. Ejecutar desde el directorio de esta entrega, usando valores privados para PID y salida: `python3 -B preparar.py --pid "$DAEMON_PID" --salida "$PREPARACION_PRIVADA"`. El padre de la salida debe existir; la salida debe ser nueva y fuera de Git. Revisar allí la unidad generada contra el recibo privado. Ningún flag puede perderse. Guardar también el comando original de arranque para rollback, sin copiar contenido del estado.
4. Ejecutar `systemd-analyze --user verify "$PREPARACION_PRIVADA/onia-tailscaled.service"` en privado; distinguir advertencias del entorno de errores de sintaxis. Volver a cotejar Linger, dueño de runtime/binario/estado/socket y hash del binario contra el recibo; no leer el estado. Conservar la carpeta privada y guard en ubicación estable: la unidad referencia esa ruta absoluta.
5. Capturar antes, sólo en privado: huella del recibo de argv/cwd, metadatos del proceso y socket, propiedades seleccionadas de unidades panel/cola, prueba HTTP local del panel sin publicar cuerpo/URL autenticada. Verificar SSH desde el cliente autorizado con known_hosts fijado, BatchMode y timeout; sólo cuando exista autorización de conexión externa. No se ha hecho aquí. Si no puede comprobarse panel/SSH, no declarar migración validada.
6. Para preparar **sólo el próximo arranque**, tras revisión/permiso de instalación: comprobar que `onia-tailscaled.service` no exista ya (archivo, enlace o unidad cargada); conservar evidencia y no sobrescribir. Copiar exclusivamente la unidad a `~/.config/systemd/user/onia-tailscaled.service` con 0600. `systemctl --user daemon-reload` y `systemctl --user enable onia-tailscaled.service` **sin `--now`**. Cotejar `is-enabled`, `show -p ActiveState -p MainPID -p FragmentPath` y que el daemon original conserva PID/argv/socket. Enable no adopta ni debe iniciar el proceso actual. No ejecutar start/restart/stop para probar. Si Linger dejó de ser yes, parar: no usar sudo ni habilitar Linger por inferencia.
7. Si hay un lanzador manual recurrente, conciliar su próximo arranque antes de enable, sin detener el proceso vivo. Conservar sus bytes y reversión. Si no está autorizado o no se entiende, parar. No modificar panel/cola para forzar ordering: sus sondas de disponibilidad y reintentos siguen siendo necesarios.

## Handoff tras un reinicio o ventana autorizada posterior

No reiniciar ahora. La unidad no puede adoptar de forma segura el daemon actual. Una transición en caliente requeriría ventana, acceso alternativo y permiso específico para interrupción; queda fuera del encargo.

Después de un reinicio autorizado por separado: cotejar privadamente un solo daemon, UID/argv/cwd/exe y socket/estado iguales, cgroup de `onia-tailscaled.service`, MainPID coherente, unidad enabled/active y Linger yes. Conservar comparación antes/después con valores privados, publicando sólo coincidencia o diferencia. No comparar hash del estado: puede cambiar legítimamente; nunca abrirlo para esta tarea. Comprobar panel local y desde el acceso autorizado, y SSH con identidad/known_hosts existentes; revisar cola sin despachar trabajos nuevos. Active no prueba tailnet lista. No cambiar Serve/ACL, ejecutar up/login ni resetear estado para reparar un fallo. Si hubo skip por instancia existente, localizar el lanzador competidor antes de cualquier nuevo start. El guard comprueba PID1; no necesita que el panel esté iniciado.

## Rollback reproducible

Antes del próximo arranque y con daemon manual intacto: `systemctl --user disable onia-tailscaled.service` **sin `--now`**. Conservar la unidad y carpeta privada como evidencia; retirar sólo la copia instalada por esta operación si no existía antes y tras cotejar sus bytes. `daemon-reload`; comprobar daemon original sin cambios, panel y acceso. No deshabilitar Linger ni tocar las unidades existentes.

Después de que la nueva unidad supervise el daemon: rollback interrumpe Tailscale y requiere ventana/autorización y acceso alternativo. Deshabilitar sólo esta unidad, detenerla de forma controlada, verificar que ya no existe daemon ni socket activo, y recuperar **el comando original privado** con mismo UID/cwd/binario/argv/estado/socket y su lanzador previo. No arrancar ambos. No borrar estado/socket ni crear autenticación nueva. Verificar panel/SSH y cola otra vez. Conservar los fallos y el recibo; sin autorización de corte, no ejecutar este rollback.

## Pruebas realizadas

`python3 -B -m unittest discover -s <esta-carpeta> -p 'test_*.py' -v`: 7/7 OK. Casos: conservación de argumentos, rechazo de flags extra/estado alternativo, socket ausente/activo/stale, vista de procesos incompleta, permiso denegado, escaping y parser real `systemd-analyze --user verify` con ejecutable inocuo. No se lanzó ninguna unidad ni daemon sintético. El parser detectó inicialmente comillas inválidas en WorkingDirectory; se corrigió a ruta absoluta restringida y se repitieron los siete casos con éxito.

Cotejo final local: panel y nginx siguen active, Linger sigue yes, estado y socket conservan tipo y propietario esperado. El generador rechazó la vista actual con rc=2 y no creó su salida privada; el guard rechazó con rc=255. No se pudo comparar PID/argv reales antes/después ni probar HTTP/SSH desde este alcance.

La prueba sintética acredita la sintaxis renderizada y controles acotados, no el arranque real ni equivalencia de parámetros todavía inaccesibles. Modelo/esfuerzo y cuota inicial/final efectivos: desconocidos desde esta sesión; no se inventan. Una sesión, sin hijos. Commit/push sólo de la rama asignada; revisión independiente, instalación, habilitación y prueba posterior siguen a cargo del coordinador/operador.

Fuentes primarias consultadas: [systemd.service](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) para Type=exec/ExecCondition/restart y [loginctl](https://www.freedesktop.org/software/systemd/man/latest/loginctl.html) para Linger. Documentación online actual; sintaxis cotejada con systemd 255 instalado. La consulta a la ruta web de userspace de Tailscale falló; no se atribuye verificación nueva a esa fuente.

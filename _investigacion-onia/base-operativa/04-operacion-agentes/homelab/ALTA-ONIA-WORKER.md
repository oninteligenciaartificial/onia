# Alta esencial de onia-worker

> **Entrada vigente para el estado dejado por v3:** [retoma v4 del corte de montaje](RETOMA-MONTAJE-v4-20261111.md). Pendiente revisión independiente y aplicación local. Los bloques de alta inicial y retomas anteriores que siguen son historia; no ejecutarlos sobre la cuenta existente.

> Siguiente paso del corte PE: [diagnóstico y retoma v3](RETOMA-PE-20261111.md). Primero diagnóstico; no repetir v2 ni dar la PC por conectada.

> **Último intento:** la retoma revisada también se detuvo; ver [ALTA-DETENIDA-v2-20261110.md](ALTA-DETENIDA-v2-20261110.md). Quedaron archivos nuevos y la cuenta cerrada. No repetir el alta inicial ni la retoma v2 sobre ese estado: falta diagnóstico y una retoma segura. Los documentos anteriores se conservan como historia. La prioridad vigente de Sergio es ingresos hasta14nov; no usar el homelab como capacidad disponible antes de verificarlo.

9 noviembre 2026 · America/La_Paz. Preparación revisada para que Sergio la aplique **sólo en DESKTOP-0GGGNMF / Ubuntu WSL2**. No aplicada todavía. Estado canónico: [homelab-conexion-20261109](../tareas/homelab-conexion-20261109.json). Laptop DESKTOP-ENV6SDA excluida.

## Qué se comprobó

Huella pública recibida de Sergio, obtenida localmente por Boss: `SHA256:4ClsP1NH8JWxBWUNjW2DP7Egn4UcHcqMUYBUu3sL1Gk` (ED25519). Tailscale VPS Running y PC online. El puerto22 de la PC no respondió durante el intercambio de banner; no se hizo autenticación ni se verificó todavía esa huella remotamente. No se utilizó el listener desconocido2222 del VPS.

[Instalador](alta-onia-worker.py), SHA256 `3b74ec2402b6ff99b641580523f730f9181fc71fd516e5c1b92dfeb13e195d78`. [Pruebas](test_alta_onia_worker.py): 9 OK, con Bubblewrap/seccomp real, persistencia entre procesos, rechazo de fuentes enlazadas/montajes y parseo del SSH dedicado con llave sintética. Harness/trabajo: 57 OK después de añadir el contexto de la fábrica. No se ejecutó `--apply`, no se ejecutó PE en Windows y no hay prueba remota WSL aún.

Cuatro pasadas del revisor distinto Sol6.1 high; tres pidieron correcciones. Veredicto final: apto para intento local controlado, **no aceptación de HOMELAB**. No se usa ultra. Evidencia y recibos en `evidencias/homelab-conexion-20261109/`.

## Paso de Sergio, ahora

1. Abrir [alta-onia-worker.py](alta-onia-worker.py) en GitHub con la cuenta que tiene acceso al repo privado y usar **Download raw file**. Guardar en Descargas con ese nombre. No copiar el instalador de una revisión anterior.
2. En **PowerShell de la PC de casa**, ejecutar este bloque. Comprueba hash y pasa la ruta al Python de Ubuntu; el instalador comprueba también nombre de máquina y huella. El uso de root local es necesario para crear la cuenta y sus controles; Codex no recibe acceso root ni contraseña.

```powershell
$oniaSetup = Join-Path $env:USERPROFILE 'Downloads\alta-onia-worker.py'
if ((Get-FileHash -Algorithm SHA256 $oniaSetup).Hash.ToLower() -ne '3b74ec2402b6ff99b641580523f730f9181fc71fd516e5c1b92dfeb13e195d78') { throw 'El archivo no coincide con el revisado' }
$oniaLinuxScript = (wsl.exe -d Ubuntu -- wslpath -u $oniaSetup).Trim()
if ($LASTEXITCODE -ne 0) { throw 'No se pudo localizar el archivo en Ubuntu' }
wsl.exe -d Ubuntu -u root -- python3 $oniaLinuxScript --apply
```

3. Compartir sólo la salida final `alta_local: OK` o el mensaje `ALTA DETENIDA`. No mandar respaldos, shadow, contraseñas o claves privadas. Ante fallo, conservar lo creado y diagnosticar; no repetir ni cambiar protecciones a ciegas.

## Qué cambia exactamente

| Elemento | Cambio |
| --- | --- |
| Cuenta | Crea onia-worker, grupo propio, password sin hash utilizable y home de login controlado por root. Consulta la política sudo y rechaza permisos para esa cuenta. |
| Datos | `/var/lib/onia-worker/work` es el único almacenamiento de trabajo escribible que se monta dentro de la sesión. `/var/lib/onia-worker/etc` contiene sólo el contexto mínimo. No monta /mnt, otros homes o /run del host. |
| Entrada | `/usr/local/libexec/onia-worker-shell`, root0755, Python aislado, entorno fijo, descriptores ajenos cerrados. Namespace de usuario/PID/red y NoNewPrivs/capacidades comprobados. |
| Canales WSL | Seccomp admite únicamente sockets AF_UNIX; bloquea AF_VSOCK, Hyper-V, INET e io_uring_setup. No desactiva AppArmor ni userns del sistema. Un PE sintético propio que sólo retorna cero se prueba fuera y dentro; si el control no funciona o la ejecución interna tiene éxito, el alta se detiene. |
| SSH | Nueva configuración `/etc/ssh/onia-worker/sshd_config`, sin PAM, Include, Match, entorno de cliente o CA. Sólo usuario worker, llave dedicada y `127.0.0.1:2224`; sin TTY/forwarding. No modifica ni recarga el SSH personal. Rechaza configuraciones personales de autenticación que no pueda descartar con seguridad. |
| Servicio WSL | Crea y habilita `onia-worker-sshd.service`. Verifica que el listener pertenezca al MainPID y exponga la huella esperada antes de publicar la llave. No crea servicios VPS ni toca producción. |
| Runtime | Helper `/usr/local/libexec/onia-worker-runtime` crea /run/sshd sólo si falta y valida cualquier existente; la unidad no se apropia de su ciclo de vida. |
| Originales | Copias privadas de las bases de cuentas/config SSH en `/root/onia-worker-originales-<fecha>`, modo0700. Nunca a Git ni al chat. No sobrescribe cuentas/rutas ya existentes. |

La shell sigue `nologin` y no hay llave autorizada hasta superar las pruebas locales y comprobar el servidor. No hay rollback destructivo si falla: puede quedar una cuenta o archivos parciales, cerrados. La presencia de libseccomp/bwrap y la política AppArmor real de WSL se validan al intentar, no se dan por ciertas por las pruebas VPS. No se descargan paquetes ni modelos.

## Después de alta_local OK: acceso Tailscale

Comprobar en PowerShell:

```powershell
Test-NetConnection 127.0.0.1 -Port 2224 -InformationLevel Quiet
```

Debe dar `True`. Si da `False`, pasar el resultado y el modo de red de WSL a Codex, sin abrir el firewall global ni reiniciar WSL. No aplicar cambios de `.wslconfig` por este documento.

Con loopback funcionando, el puente mínimo propuesto es **Tailscale Serve TCP**, exclusivamente dentro de la tailnet, al servidor2224. No es Funnel ni una publicación web. Antes de aplicarlo cotejar `tailscale serve status --json` local y conservar copia privada: si2224 ya está ocupado por otra configuración, no reemplazarla. El comando específico, cuando ese preflight esté comprobado, es:

```powershell
tailscale serve --bg --tcp=2224 tcp://127.0.0.1:2224
```

No se ha ejecutado. Reutiliza Tailscale de Windows; no instala otro en WSL, no configura router ni compra servicios. El acceso de tailnet conserva sus ACL; además SSH exige la llave dedicada. Mantener WSL en ejecución durante el primer ensayo; systemd por sí solo no acredita WSL siempre vivo.

Codex deberá obtener la host key sin autenticarse, comparar su hash con el proporcionado por Sergio y sólo entonces fijarla en un known_hosts exclusivo. Las conexiones posteriores usarán `StrictHostKeyChecking=yes`, `IdentitiesOnly=yes`, llave dedicada y `tailscale nc desktop-0gggnmf 2224` como ProxyCommand. Nunca confiar automáticamente en una huella distinta.

Pruebas remotas pendientes: comando por SSH con UID y grupos correctos, denegación de forwarding/TTY, ambiente y FDs, lectura directa/enlace/proc a Windows y host rechazada, archivo de trabajo conservado entre conexiones, rechazo de privilegios y huella efectiva. Se repetirá el chequeo local desde el punto de entrada SSH. Hasta esas pruebas, no aceptar el HOMELAB. Persistencia al cerrar terminal/reiniciar sigue siendo una comprobación posterior separada, no se reinicia la PC por sorpresa.

## Reversión conservando archivos

Sólo si se aplicó esta alta, Sergio puede detener **el servicio nuevo** y bloquear la shell desde su Ubuntu root; no afecta al ssh personal:

```powershell
wsl.exe -d Ubuntu -u root -- systemctl disable --now onia-worker-sshd.service
wsl.exe -d Ubuntu -u root -- usermod --shell /usr/sbin/nologin onia-worker
```

Conservar cuenta, workspace, scripts y respaldos. Para revocar también la llave, renombrar `authorized_keys` a un nombre nuevo fechado bajo `/etc/ssh/onia-worker/` después de comprobar que el destino no existe. No eliminarla ni copiar las bases completas passwd/shadow hacia atrás: podrían haber cambiado otros usuarios.

Si se habilitó **sólo este** forward de Tailscale, apagarlo con `tailscale serve --bg --tcp=2224 off`; nunca `serve reset`, que afectaría otros forwards. Conservar antes la configuración privada. No detener Tailscale ni servicios VPS.

## Primer PEDIDO técnico de la fábrica

El modelo editorial vive exclusivamente en [ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md](../ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md), confirmado por Sergio desde573b302. No se reescribe aquí. Para ejecutar:

- ID existente del harness, autorización aplicable, responsable y ruta del video privado accesible al worker (o transferencia autorizada); original fuera de Git.
- Idioma, duración y salida de transcripción: texto con tiempos, SRT/VTT si se solicita; nombres propios a comprobar y criterio de aceptación.
- Contenido entrega intervalos inicio/fin para cada corte, formato/resolución, subtítulos/CTA ya aprobados y destino privado del borrador.
- Si los intervalos todavía no existen: primera entrega de ASR → Contenido elige → cortes. Codex no decide los momentos editoriales para cumplir la meta de cinco.
- Revisor distinto; revisión y aprobación de Sergio antes de publicar. No subir originales, render privados o transcripciones completas a Git sin permiso de redistribución. No inferir música/tono a partir de ASR.

ASR y FFmpeg no se ejecutaron en este encargo. La red dentro del worker está cerrada: modelos y archivos tendrán que estar disponibles mediante transferencia autorizada antes del primer trabajo; no descargar pesos a ciegas ni copiar cuentas. No hay scheduler.

Fuentes técnicas primarias: [Bubblewrap](https://raw.githubusercontent.com/containers/bubblewrap/main/bwrap.xml), [OpenSSH](https://man.openbsd.org/sshd.8), [libseccomp](https://raw.githubusercontent.com/seccomp/libseccomp/main/include/seccomp.h.in), [formato PE](https://learn.microsoft.com/en-us/windows/win32/debug/pe-format), [Tailscale Serve](https://tailscale.com/docs/reference/tailscale-cli/serve). Las pruebas acotan el resultado; no prueban aislamiento absoluto ante vulnerabilidades del kernel o cambios administrativos posteriores.


## Retoma tras el corte del 10 noviembre

Para la cuenta parcialmente creada del informe ALTA-DETENIDA, usar [RETOMA-REVISADA-20261110](RETOMA-REVISADA-20261110.md): nuevo hash, validación de sudo-rs y `--resume-backup` explícito. El bloque anterior se conserva como antecedente de alta inicial y no debe repetirse sobre la cuenta existente.

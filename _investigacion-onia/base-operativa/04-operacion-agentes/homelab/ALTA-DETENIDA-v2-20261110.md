# Retoma de onia-worker DETENIDA (v2) · 10 nov 2026, 20:14 La Paz

Estado: **ejecutado parcialmente y detenido por el propio instalador**. No es aceptación ni rollback. Aplicó Boss en DESKTOP-0GGGNMF, Ubuntu 26.04 LTS sobre WSL2 (kernel 6.18.33.2-microsoft-standard-WSL2). Autorización: el sí de Sergio de las 13:29 (ver ALTA-DETENIDA-20261110.md), para retomar el mismo alcance. La ejecución como root la aprobó Sergio en su tarjeta local.

## Antes (sólo lectura, 20:08)
Usuario `onia-worker` uid y gid 1001, sin otros grupos, shell nologin. No existían `/var/lib/onia-worker` ni `/etc/ssh/onia-worker`, y el puerto 2224 estaba cerrado. Coincide con el corte documentado.

## Ejecución
El instalador se copió desde master (`04-operacion-agentes/homelab/alta-onia-worker.py`) como `Downloads\alta-onia-worker-v2.py`. Su SHA256 `0521e2f4…e871` se comprobó en el box y en la PC antes de correr. Se usó el comando exacto de RETOMA-REVISADA-20261110.md, con `--resume-backup` sobre el respaldo ORIGINAL.

```
ALTA DETENIDA: No funciona el control PE inocuo fuera del sandbox; conservar cuenta cerrada
Conservar lo creado; no desactivar protecciones ni repetir a ciegas. Avisar a Codex.
EXIT=1
```

## Qué quedó (sólo lectura, después)
- Pasó la consulta de sudo con sudo-rs: el instalador llegó hasta la línea ~489.
- Se creó `/var/lib/onia-worker` (root, 755, 00:14 UTC) con `login`, `work` y `etc`. Por el código, también `host-only` y `interop-canary.exe`.
- Lo que falló es la ejecución del canario PE fuera del sandbox (`run([ROOT/'interop-canary.exe'], timeout=5)`). Boss no vio la excepción subyacente.
- No existe `/etc/ssh/onia-worker`, no hay unidad ni llave, y la cuenta sigue cerrada. Hay `bwrap` en `/usr/bin/bwrap`. No existe el sysctl `apparmor_restrict_unprivileged_userns` en este kernel.
- No se borró, revirtió ni desactivó nada. No se repitió.

## Inferido (sin comprobar)
Probablemente la interop de WSL, que ejecuta .exe de Windows desde Linux, no funciona en ese contexto: sesión `-u root`, `wsl.conf`, binfmt o un timeout de 5 s en el primer arranque, con la distro en Stopped. Diagnosticarlo le corresponde a Codex.

## PEDIDO a Codex (homelab-conexion-20261109)
1. Diagnosticar por qué falla el canario PE. Dar un comando de sólo lectura que Boss pueda correr en la PC para capturar la excepción (interop habilitada, binfmt WSLInterop, wsl.conf) sin alterar nada.
2. Si hace falta, ajustar la retoma para que acepte el estado nuevo: `/var/lib/onia-worker` creado por este intento. Que no falle en `ROOT.mkdir` ni en `write_new`, sin relajar ninguna prueba.
3. Hacer pasar el test a otra sesión revisora y publicar el SHA256 nuevo.

La PC quedó desconectada de la app a las 20:15.

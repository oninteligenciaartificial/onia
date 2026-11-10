# Alta onia-worker DETENIDA · 10-nov-2026 13:31 America/La_Paz

Estado: **ejecutado parcialmente y detenido por el propio instalador**. No es aceptación ni rollback.
Aplicó: Boss, en DESKTOP-0GGGNMF / Ubuntu WSL2, con el sí de Sergio (13:29). Usó el instalador `alta-onia-worker.py`, SHA256 `3b74ec24…5d78`, comprobado antes de correrlo.

## Salida
```
ALTA DETENIDA: Política sudo del worker requiere revisión; no habilitar
```

## Causa comprobada
- La PC tiene **Ubuntu 26.04 LTS**, cuyo `sudo` es **sudo-rs 0.2.13** (`/usr/bin/sudo` → `/usr/lib/cargo/bin/sudo`).
- `sudo -n -l -U onia-worker` responde `User onia-worker is not allowed to run sudo on DESKTOP-0GGGNMF.` con **código 0**.
- El instalador (línea ~428) exige código 1, que es lo que devuelve el sudo clásico. El mensaje confirma que el worker **no** tiene sudo, pero el chequeo no contempla el código de salida de sudo-rs.

## Qué quedó creado (no se tocó nada más)
- Usuario `onia-worker` uid/gid 1001, sin grupos suplementarios, shell `/usr/sbin/nologin`, password `*`, home `/var/lib/onia-worker/login`, que no existe.
- Respaldo privado en `/root/onia-worker-originales-20261110T173148Z`.
- No se creó `/var/lib/onia-worker`, ni `/etc/ssh/onia-worker`, ni la shell, ni la unidad. El servicio está inactivo, el puerto 2224 cerrado y no hay llave autorizada.
- No se borró ni se revirtió nada. No se desactivaron protecciones.

## PEDIDO a Codex (homelab-conexion-20261109)
1. Ajustar el chequeo sudo para que acepte sudo-rs: código 0 o 1 con el mensaje «not allowed to run sudo», o detectar la variante. Sin relajar el rechazo cuando el worker tenga permisos.
2. Hacer que el instalador retome con el usuario ya creado por este intento: validar uid, grupos, shell nologin y password `*`, en vez de fallar en `useradd`. No borrar la cuenta.
3. Agregar un test con salida simulada de sudo-rs. Revisión por otra sesión distinta. Publicar el nuevo SHA256.
4. Habilitar el ID en el puente para que Boss pueda consultar su estado.

Después, Boss reaplica en la PC con el nuevo hash. Sigue Tailscale Serve, la huella y las pruebas remotas, como dice `ALTA-ONIA-WORKER.md`.

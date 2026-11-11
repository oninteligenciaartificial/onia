# Alta local v4 confirmada por salida de Sergio

Fuente: salida de PowerShell pegada por Sergio; no observación remota de Codex. PC DESKTOP-0GGGNMF, Ubuntu WSL. Hash v4 comprobado sin error: `0f6ca971dd570d8e783061ee1f4f58c7517f165dbf2fdb3452a9dc4140282cc1`.

Comando ejecutado: Python aislado con `--apply --resume-backup` del respaldo original y `--resume-mount-control`. Creada la habilitación de `onia-worker-sshd.service`. Resultado `alta_local=OK`, sin error final del bloque PowerShell.

Pruebas locales informadas como correctas: UID no root, sin capacidades, no_new_privs, namespaces PID/red aislados, Windows y host no expuestos, etc sólo lectura, sudo rechazado, módulos ocultos y sólo lectura. Se creó una marca de persistencia en el workspace; esto no acredita supervivencia a reinicio ni SSH entre conexiones. Se conserva el respaldo privado nuevo, sin publicarlo.

Huella informada coincide con la esperada en el instalador. Aún debe cotejarse la huella presentada por la conexión remota antes de autenticar.

## Próximo paso

Sergio comprueba desde Windows que el puerto local dedicado 2224 es accesible y consulta el estado actual de Tailscale Serve. Sólo después de verificar que no se sustituye otra configuración se prepara el forward privado. Codex prueba SSH con huella fijada y llave dedicada, aislamiento y persistencia entre conexiones. No repetir el instalador.

Pendientes: acceso remoto, inventario efectivo, persistencia WSL, trabajo útil remoto y ensayo de orquestación. No se acepta todavía el homelab ni se amplía el tope de tres sesiones. La limpieza de antecedentes del registro publicable continúa como mantenimiento separado.

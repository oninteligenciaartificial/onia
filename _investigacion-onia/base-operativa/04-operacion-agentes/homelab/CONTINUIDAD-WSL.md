# Continuidad WSL sin terminal abierta

Preparación, no instalación comprobada: ejecutar CONTINUIDAD-WSL.ps1 una vez desde PowerShell del usuario Windows dueño de Ubuntu, en DESKTOP-0GGGNMF. El acceso remoto del worker está aislado de Windows; Codex no puede registrar esta tarea por ese canal. No se pide contraseña ni se eleva a SYSTEM/root. La tarea corre con token interactivo limitado y utiliza onia-worker sólo para sleep, sin shell libre.

Nombre exclusivo OnIA-Ubuntu-Continuidad; se detiene si ya existe. Arranque al logon del usuario actual, ejecución inmediata, una instancia, sin límite de duración, tres reintentos ante fallo. PowerShell oculto espera a wsl.exe ejecutando sleep infinity. No cambia red, firewall, suspensión, WSL config ni otros trabajos. No elimina archivos. No habilita orquestación.

La tarea mantiene una sesión WSL real; systemd por sí solo no la sostiene. Cubre cierre de terminal con Windows conectado. No cubre apagado, suspensión ni logout. Tras reiniciar Windows requiere iniciar sesión. No se debe ensayar reinicio sin ventana acordada.

Validación pendiente en Windows: tarea Running, cerrar solamente las terminales Ubuntu, dejar Windows conectado y PC despierta; tras al menos 90 segundos comprobar SSH desde VPS sin ejecutar comandos wsl desde Windows que oculten una caída. Registrar dos conexiones y disponibilidad del archivo previo. Si falla, conservar tarea y consultar estado/LastTaskResult, no repetir registro ni instalar otra tarea.

Reversión conservadora: Stop-ScheduledTask -TaskName OnIA-Ubuntu-Continuidad; Disable-ScheduledTask -TaskName OnIA-Ubuntu-Continuidad. No borra configuración. Detenerla puede permitir que WSL salga cuando no quede actividad; primero drenar trabajos.

Verificación aquí: revisión estática PowerShell5.1; no hay PowerShell/Windows local para afirmar ejecución real. No requiere bypass de ExecutionPolicy: se puede pegar su contenido en la consola. Controles y resultado reales se registrarán después.

Fuentes: https://learn.microsoft.com/en-us/windows/wsl/systemd y https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal .

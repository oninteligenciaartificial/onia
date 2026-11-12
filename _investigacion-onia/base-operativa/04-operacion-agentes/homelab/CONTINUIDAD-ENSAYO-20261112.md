# Ensayo tras cerrar terminales: no aprobado

Sergio informó terminales cerradas. Codex esperó 90 segundos (dos ventanas de 45) sin iniciar conexiones al worker durante el intervalo y ejecutó la prueba SSH existente desde VPS. Resultado rc255, conexión cerrada antes de obtener la salida del worker. No se prueba persistencia ni disponibilidad con ese resultado.

Consulta posterior del estado Tailscale: VPS Running; PC DESKTOP-0GGGNMF online. No se publican direcciones ni estado de autenticación. Esto no distingue caída de Ubuntu, servicio, forward o tarea Windows.

No se recibió aún evidencia de registro/Running de OnIA-Ubuntu-Continuidad. No afirmar que la tarea fue instalada o que falló; próximo paso de Sergio: consultar Get-ScheduledTask, Get-ScheduledTaskInfo y wsl --list --running, sin arrancar la distro. Conservar lo instalado. No repetir alta, cambiar protecciones ni iniciar orquestación hasta diagnosticar continuidad.

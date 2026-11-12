# Ensayo tras cerrar terminales: no aprobado

Sergio informó terminales cerradas. Codex esperó 90 segundos (dos ventanas de 45) sin iniciar conexiones al worker durante el intervalo y ejecutó la prueba SSH existente desde VPS. Resultado rc255, conexión cerrada antes de obtener la salida del worker. No se prueba persistencia ni disponibilidad con ese resultado.

Consulta posterior del estado Tailscale: VPS Running; PC DESKTOP-0GGGNMF online. No se publican direcciones ni estado de autenticación. Esto no distingue caída de Ubuntu, servicio, forward o tarea Windows.

No se recibió aún evidencia de registro/Running de OnIA-Ubuntu-Continuidad. No afirmar que la tarea fue instalada o que falló; próximo paso de Sergio: consultar Get-ScheduledTask, Get-ScheduledTaskInfo y wsl --list --running, sin arrancar la distro. Conservar lo instalado. No repetir alta, cambiar protecciones ni iniciar orquestación hasta diagnosticar continuidad.

## Estado Windows recibido después

Sergio confirma tarea OnIA-Ubuntu-Continuidad existente, Ready; LastTaskResult 3221225786 (0xC000013A, STATUS_CONTROL_C_EXIT), última ejecución informada 11/11/2026 20:00:13. No hay distribuciones WSL ejecutándose. Esto acredita terminación, no identifica quién o qué envió el evento de control; no atribuir a una acción de Sergio. La hipótesis de cierre de consola debe contrastarse con acción/configuración real.

Fuente del significado: https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-erref/596a1078-e883-4972-9bbc-49e60bebca55 . Siguiente: inspeccionar acción, tipo de logon y reinicio configurado; no sustituir la tarea ni elevar privilegios por conjetura.

# SSH remoto v4 comprobado desde VPS

Después del alta local, Sergio informó Windows localhost accesible y Tailscale Serve TCP dedicado iniciado. Antes de eso WSL estaba apagado; al iniciarlo el servicio volvió activo/running y su puerto respondió dentro de Ubuntu. No inferir disponibilidad permanente.

Codex obtuvo la clave ED25519 sin autenticación a través de Tailscale, comprobó la huella esperada y sólo después la fijó en known_hosts privado. Las dos conexiones usaron StrictHostKeyChecking=yes, IdentitiesOnly=yes, BatchMode=yes y llave dedicada. No se usó el puerto ajeno 2222 ni la laptop. Direcciones privadas y credenciales no se incluyen.

[Prueba repetible](PRUEBA-SSH-v4-20261111.py): requiere el known_hosts privado ya verificado y las herramientas/llave existentes. Ejecutada en el VPS con Python3, rc0. Escribe una marca única en el workspace del worker y la conserva. [Salida saneada](SSH-REMOTO-v4-20261111.json).

Resultado: UID1001, único grupo1001; sin capacidades, no_new_privs y seccomp activos; Windows y root del host ausentes de las rutas comprobadas; sin entorno WSLInterop; módulos vacíos y escritura rechazada tanto allí como en etc; socket INET rechazado. Python, FFmpeg y Git encontrados (disponibilidad no implica pruebas funcionales de todos). Segunda conexión comprobó el contenido de la marca.

No es una prueba exhaustiva de escapes: siguen pendientes rechazo de forwarding/TTY y demás accesos alternativos previstos. No se ejecutó ASR, benchmark, reinicio ni orquestación distribuida. Tampoco se probó supervivencia de WSL sin terminal ni arranque tras reinicio. El homelab completo no se declara aceptado y el tope sigue en tres. Próximo cierre: pruebas remotas restantes, continuidad WSL y un trabajo útil acotado; después medir orquestación con recursos y cuota observados.

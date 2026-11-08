# Acceso de Sergio al navegador del VPS

**Estado al 8 de noviembre de 2026, 22:14 UTC.** Inspección de solo lectura en `srv1360183` como `onia-codex-worker`. El directorio de datos ya está reservado y el acceso gráfico sigue pendiente de prueba. La cuenta `onia.investigacion@gmail.com` aún no se creó y Google todavía no confirmó la disponibilidad del nombre.

## Qué está disponible

- El informe `~/operacion/browser-piloto-20261108/REPORTE.md` y su `package.json` documentan Playwright MCP 0.0.84 y Chromium 1252. Se verificó que el binario completo `~/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome` es ejecutable. El piloto MCP headless se comprueba en otro encargo. Su eventual prueba de navegación, DOM y capturas sería evidencia de automatización.
- `~/operacion/cuentas/analisis-onia/browser-profile` está vacío, pertenece a `onia-codex-worker` y tiene modo `0700`. Los perfiles que Chromium cree dentro guardarán cookies y otros datos de sesión. Chromium admite una ruta dedicada mediante `--user-data-dir` y requiere que una sola instancia use ese directorio a la vez. [Documentación de Chromium](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/user_data_dir.md)
- Están instalados `ssh`, `sshd`, `xauth`, `xdpyinfo` y `Xvfb`. El archivo principal de OpenSSH declara `X11Forwarding yes` e incluye archivos adicionales. Uno de ellos no es legible con el permiso actual. Se validó el análisis de opciones del cliente con `ssh -G -F /dev/null -X -o ForwardX11Trusted=no localhost`, que no abre conexión. La política efectiva para el acceso de Sergio, incluidas las restricciones de su autenticación, sigue por probar. [Manual del servidor OpenSSH](https://man.openbsd.org/sshd_config)
- La sesión inspeccionada carece de `DISPLAY` y `WAYLAND_DISPLAY`. La revisión de PATH, paquetes y rutas habituales no encontró componentes de VNC, RDP, noVNC ni websockify. La herramienta de inventario de sockets TCP quedó bloqueada por permisos de netlink. El catálogo de esta sesión carece de un control de escritorio verificable para este host. Abrir un panel de navegador en Codex no acredita dónde se ejecuta su navegador.

**Bloqueo para el alta.** Falta un canal gráfico autenticado de extremo a extremo para que Sergio vea y maneje Chromium en este VPS. La disponibilidad de Chromium, el reenvío declarado por OpenSSH y la prueba independiente de MCP son comprobaciones distintas de ese canal.

## Primera vía, OpenSSH con reenvío X11

Es la vía que aprovecha lo instalado sin compras ni cambios de servidor, condicionada a que Sergio ya tenga acceso SSH autorizado y un entorno X compatible en el dispositivo desde el que se conecta. El equipo cliente aporta la pantalla, el teclado y el ratón. Chromium, las peticiones a Google y su directorio de datos quedan en el VPS. El acceso funciona con una conexión nueva que permita el reenvío. [Manual de OpenSSH](https://man.openbsd.org/ssh#X11_FORWARDING)

1. Desde su cliente SSH, Sergio sustituye `ALIAS_SSH_DEL_VPS` por el destino autorizado que ya usa. Debe tener iniciada su pantalla X local antes de conectar. El alias y su autenticación no se recopilaron en esta inspección.

   ```sh
   ssh -X -o ForwardX11Trusted=no ALIAS_SSH_DEL_VPS
   ```

2. Dentro de esa conexión, comprueba el destino y la pantalla reenviada. Debe obtener `srv1360183`, `onia-codex-worker` y salida exitosa de `xdpyinfo`. Si la pantalla queda sin asignar, se rechaza el reenvío o falla la prueba, usar la vía de visor web una vez preparada.

   ```sh
   hostname
   id -un
   test -n "${DISPLAY:-}" && xdpyinfo >/dev/null
   ```

3. Antes del alta, valida ventana, teclado, ratón y navegación pública con un directorio temporal que pertenezca a esta prueba. Ejecuta el ejemplo en esa misma conexión para abrir `example.com` en Chromium del VPS.

   ```sh
   navegador="$HOME/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome"
   perfil_prueba=$(mktemp -d) &&
     "$navegador" --user-data-dir="$perfil_prueba" https://example.com
   ```

4. Cierra esa ventana. En la conexión de Sergio, una vez validada la ruta, abre Chromium con el directorio dedicado. En `chrome://version` comprueba que **Profile Path** queda debajo de `~/operacion/cuentas/analisis-onia/browser-profile`. Usa una sola instancia con ese directorio y conserva activo el aislamiento de Chromium. [Documentación de Chromium](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/user_data_dir.md)

   ```sh
   "$navegador" --user-data-dir="$HOME/operacion/cuentas/analisis-onia/browser-profile"
   ```

5. Dentro de esa ventana, Sergio abre la página oficial de Google y elige **Crear cuenta**. Prueba el nombre solicitado y decide qué hacer si Google lo rechaza. Ingresa personalmente sus datos, contraseña, recuperación y código o desafío de verificación si aparece. Los comparte únicamente con la interfaz oficial. Mantener la sesión fuera de automatización, capturas y registros. Puede informar al coordinador el resultado del alta sin compartir datos de acceso. [Crear una cuenta para Gmail](https://support.google.com/mail/answer/56256?hl=es) · [Verificación de cuenta](https://support.google.com/accounts/answer/114129?hl=es)

## Vía de visor web si el cliente no tiene X

Preparación posterior en el VPS, si la vía anterior no sirve. La opción libre es usar el `Xvfb` existente con un display privado con autorización X, un servidor `x11vnc` autenticado y noVNC con websockify. Los componentes adicionales deben prepararse y probarse en el VPS bajo el usuario de operación. El visor de Sergio se abre en un navegador que ya tenga, con su cliente SSH como transporte. Los puertos VNC y WebSocket se ligan únicamente a loopback y la sesión vive durante la intervención. La autenticación del servidor VNC debe permanecer activa, ya que otros procesos del host pueden alcanzar puertos de loopback. [x11vnc](https://github.com/LibVNC/x11vnc) · [noVNC](https://github.com/novnc/noVNC#quick-start) · [websockify](https://github.com/novnc/websockify)

1. El ejecutor futuro comprueba dependencias y opciones de instalación privada sin root, elige display y puertos libres, y levanta temporalmente el display y el puente con acceso restringido. Verifica desde el VPS que los listeners quedaron ligados a loopback.
2. Sergio crea el túnel con su destino SSH existente. Los puertos se sustituyen por los valores que el ejecutor haya verificado. La opción `ExitOnForwardFailure` detecta fallos al establecer el reenvío. La disponibilidad del puente remoto se valida al abrir el visor. [Reenvío local de OpenSSH](https://man.openbsd.org/ssh#L)

   ```sh
   ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:PUERTO_LOCAL:127.0.0.1:PUERTO_WEB_VPS ALIAS_SSH_DEL_VPS
   ```

3. Sergio abre la dirección de loopback que entregue el ejecutor tras la prueba. Primero prueba el control en una página pública con un perfil descartable. Después usa el directorio dedicado y completa personalmente el mismo flujo de Google. Al terminar, cierra Chromium, el visor y el túnel. El ejecutor detiene únicamente los procesos temporales de esa sesión y comprueba que cesaron los listeners.

## Pendientes

La primera prueba corresponde a una conexión real de Sergio desde un cliente autorizado, con control de una página pública y confirmación del perfil. Si esa prueba falla, queda pendiente preparar y probar el visor web en el VPS. Esta inspección no ejecutó conexiones SSH nuevas, navegador, MCP ni servicios. La implementación del acceso y el alta siguen separadas del informe.

La investigación de fuentes públicas puede avanzar con navegación sin sesión cuando la fuente lo permita. Cada fuente restringida requiere comprobar su acceso por separado. Crear Gmail no acredita por sí solo acceso a un video, curso ni extracción de su contenido.

## Decisión posterior de Sergio

Después de esta preparación, Sergio pidió terminar la evaluación audiovisual y hacer STOP. Alta de cuenta, prueba de acceso gráfico, navegador persistente e instalaciones del visor quedan para el siguiente encargo explícito. No hay enlace de acceso operativo que entregar todavía.

## Actualización posterior: preparación autorizada y bloqueo AppArmor

Sergio autorizó preparar el navegador y luego pidió la corrección mínima de AppArmor para revisión previa. [Propuesta, comandos, impacto, reversión y pruebas pendientes](APROBACION-APPARMOR.md). La etiqueta efectiva del Chromium instalado es `unconfined`; falla con `No usable sandbox`. Visor preparado y prueba sintética cerrada; todavía no hay navegador operativo ni cuenta creada. No se cargó ningún perfil del sistema.

# Chromium del VPS: corrección preparada, pendiente de aprobación

8 de noviembre de 2026, America/Caracas. Tarea `cuentas-secundarias-20261108`.

## Diagnóstico confirmado

El ejecutable instalado es `/home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome`. Su SHA-256 es `e44893f0eb826ba2e9c0e44e182f910e8d8473ce00b9eb7ae7a652512f02cd78`, pertenece al UID1004 (`onia-codex-worker`) y tiene modo0755. No se reinstaló ni modificó.

En la prueba de las18:46:22 Caracas se leyó `/proc/PID/exe` y, sólo después de confirmar que era ese ejecutable, `/proc/PID/attr/current`: **`unconfined`**. El arranque terminó con SIGABRT (`returncode=-6`) y `No usable sandbox!`. AppArmor está activo (`Y`) y `kernel.apparmor_restrict_unprivileged_userns=1`. La lista global de perfiles cargados no es legible para este usuario; no se presenta como inspeccionada. La etiqueta del proceso sí fue observada.

El archivo existente `/etc/apparmor.d/chrome` define una coincidencia para `/opt/google/chrome/chrome`, no para el ejecutable de Playwright. No fue modificado. No existe todavía `/etc/apparmor.d/onia-chromium-1252`.

Esto coincide con el diagnóstico de la [documentación oficial de Chromium](https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md): los builds descargados fuera de las rutas cubiertas pueden no obtener los user namespaces necesarios para su sandbox. [Ubuntu explica la aplicación de perfiles por programa](https://documentation.ubuntu.com/security/security-features/privilege-restriction/apparmor/).

## Cambio mínimo propuesto

Crear **un archivo nuevo**, `/etc/apparmor.d/onia-chromium-1252`, propietario `root:root`, permisos `0644`, con el contenido de [onia-chromium-1252.apparmor](onia-chromium-1252.apparmor):

```text
abi <abi/4.0>,
include <tunables/global>

profile onia-chromium-1252 /home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome flags=(unconfined) {
  userns,
}
```

La coincidencia es la ruta exacta, sin comodines. No incluye headless-shell, otros Chromium, Codex, Docker ni servicios. El perfil permite a este ejecutable crear namespaces de usuario; Chromium mantiene sus controles internos. `flags=(unconfined)` sigue el patrón oficial para esta excepción: **no es una política que aísle todos los archivos del navegador**. El proceso ya tenía esa etiqueta genérica; se añade la autorización de userns para su ruta.

Impacto y límite: aumenta para ese ejecutable el acceso a una interfaz del kernel restringida por Ubuntu. Como el archivo pertenece al usuario de operación, ese usuario puede reemplazar su contenido; el perfil se vincula a la ruta, no a su hash. El administrador debe revisar ese riesgo y la huella antes de aplicarlo. Fijar el binario en una ruta propiedad de root sería otra opción, con un cambio mayor, que no se aplica en esta propuesta mínima.

No se cambia sysctl, no se desactiva AppArmor, no se usa `--no-sandbox`, no se instala un helper SUID, no se reinicia ningún servicio y no se toca el perfil existente de Chrome. Cada actualización de ruta/binario requiere comprobar de nuevo compatibilidad y alcance.

## Comandos administrativos, NO ejecutados

Requieren **aprobación de Sergio y una consola administrativa del VPS**. El ejecutor actual es `onia-codex-worker`; aprobar la propuesta no le otorga privilegios root. No se usa sudo desde esta sesión.

Primero revisar el archivo versionado y su hash, publicado junto con la evidencia. El administrador ejecutaría:

```bash
bash /home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/aplicar-apparmor-admin.sh --aprobado-por-sergio
```

El script exige UID0, verifica la huella del ejecutable y del perfil, rechaza cualquier archivo de destino preexistente, crea el archivo root:root0644, compila sin cargar primero y carga **sólo ese perfil** con `apparmor_parser --add --skip-cache`. No inicia Chromium, visor ni cuenta. Si un paso falla, conserva el archivo/evidencia y no continúa a la navegación.

Las operaciones administrativas sustantivas son:

```bash
install -o root -g root -m 0644 "$origen_verificado" /etc/apparmor.d/onia-chromium-1252
apparmor_parser --skip-kernel-load --skip-cache /etc/apparmor.d/onia-chromium-1252
apparmor_parser --add --skip-cache /etc/apparmor.d/onia-chromium-1252
```

Usar el script completo para conservar sus precondiciones; los tres comandos no sustituyen la verificación anterior. La opción `--skip-kernel-load` ya pasó con la propuesta; **la carga no se ejecutó**.

## Reversión conservando originales

Primero cerrar de forma controlada sólo nuestro navegador y visor. El administrador comprueba que el perfil del archivo coincide con el aprobado, crea un directorio nuevo de respaldo y ejecuta:

```bash
respaldo=$(mktemp -d /var/backups/onia-apparmor.XXXXXX)
cp -a /etc/apparmor.d/onia-chromium-1252 "$respaldo/perfil-cargado"
apparmor_parser --remove /etc/apparmor.d/onia-chromium-1252
mv /etc/apparmor.d/onia-chromium-1252 "$respaldo/perfil-inactivo"
```

Se retira únicamente el perfil añadido de la memoria del kernel y del directorio de carga; sus bytes quedan conservados en el respaldo. No se borra ni restaura ningún archivo original del sistema porque no fue modificado. La restricción global sigue en1. Nuevos arranques vuelven a quedar sin esa excepción; después se comprueba el estado. Si alguien modificó el archivo desde la aprobación, detenerse y conciliar antes de revertir.

## Pruebas separadas después de aprobar y aplicar

1. **Chromium y sandbox.** Primero un perfil de prueba sin cuentas: arranque exitoso, DOM público y etiqueta `onia-chromium-1252`. Inspeccionar `chrome://sandbox` y los procesos renderer: namespaces/Seccomp efectivos, además de ausencia de flags que desactiven aislamiento. Arrancar no basta para afirmar todas las capas del sandbox.
2. **Visor.** Comprobar autenticación VNC (rechaza clave incorrecta, acepta la correcta), HTTP/WebSocket, listeners sólo127.0.0.1:5908 y127.0.0.1:6088, autorización X y acceso por túnel SSH de Sergio. No publicar la clave ni usarla en la URL. Los datos privados quedan0700/0600 fuera del repo.
3. **Control humano.** Sergio ve una página pública, escribe un texto de prueba, usa ratón y vuelve a abrir una página. La prueba desde VPS no acredita por sí sola el túnel desde Windows. Todavía no ingresar cuentas.
4. **MCP.** En prueba separada y con autorización de lanzamiento aplicable, usar el wrapper acotado del encargo AV y comprobar navigate/snapshot/captura/close; conservar el bloqueo anterior de aprobación como evidencia. La corrección AppArmor no demuestra que la política MCP se haya resuelto.

El alta de `onia.investigacion` y su disponibilidad siguen pendientes. El login lo hará Sergio directamente en Google, sin compartir contraseña/códigos ni capturar la pantalla durante esa parte. [Ayuda oficial de Gmail](https://support.google.com/mail/answer/56256?hl=es).

## Visor preparado y alcance de lo probado hoy

Se reutilizan Chromium1252, Playwright MCP0.0.84 y Xvfb existentes. Se prepararon bajo `~/operacion/cuentas/analisis-onia/runtime-20261108/` noVNC1.7.0 (`63107bd06d9e1f6136ff21aeda8cd62cbf0d433e`), websockify0.13.0 (`e81894751365afc19fe64fc9d0e5c6fc52655c36`) y paquetes Ubuntu extraídos, sin instalar globalmente: x11vnc0.9.16-10 y libvncserver/client0.9.14+dfsg-1ubuntu0.2. Bibliotecas de x11vnc resueltas. noVNC tiene núcleoMPL2.0 y recursos con otras licencias; websockifyLGPLv3; x11vncGPLv2+ y LibVNCServerGPLv2+. Avisos y fuentes se conservan en sus carpetas privadas; no se redistribuyen sus binarios en Git.

[browser-vps.py](browser-vps.py) es un lanzador preparado. En modo `prueba-visor` arrancaron Xvfb autenticado, xmessage sintético, x11vnc y websockify; detectó sus puertos de loopback. Eso **no prueba todavía** intercambio autenticado RFB, renderizado en el PC, teclado/ratón ni navegación. Tras la instrucción de revisar primero AppArmor, se cerraron sólo esos cuatro procesos por PID e identidad de arranque, y `ss` confirmó que5908/6088 no escuchan. No quedaron servicios nuevos activos. Los archivos de prueba se conservaron.

El directorio privado tenía modo0775; la precondición del script rechazó iniciar. Se corrigió a0700 antes de crear la clave0600. El primer intento de consultar `websockify/run` lo invocó erróneamente con Python; se corrigió al ejecutar su entrada shell. Ambos resultados se registran, sin tomarlos por pruebas exitosas de navegador.

Después de desbloquear y validar Chromium, el comando preparado —todavía no ejecutado con Chromium; abre example.com— será:

```bash
python3 ~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py iniciar
```

El usuario podrá reutilizar su SSH autorizado para reenviar el visor:

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:6088:127.0.0.1:6088 onia-codex-worker@DIRECCION_DEL_VPS
```

Y abrir `http://127.0.0.1:6088/vnc.html?autoconnect=1&resize=scale`. La URL **no funciona ahora** porque el visor está detenido. La autenticación SSH de Windows todavía no está comprobada. Chromium y su perfil corren en el VPS; Windows sólo presenta el visor. La clave del visor se consulta exclusivamente en la terminal SSH privada, nunca por chat; no es la contraseña de Google.

Estado del encargo: **en espera de aprobación administrativa; no terminado ni aceptado**. La investigación de referentes no fue interrumpida.

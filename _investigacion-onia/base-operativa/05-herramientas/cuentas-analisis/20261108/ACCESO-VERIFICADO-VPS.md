# Navegador operativo en el VPS; control humano confirmado

**Actualización 2026-11-08T22:07:54-04:00:** Sergio confirmó en el chat: «Sí, veo el navegador y puedo manejarlo», en respuesta a la prueba de visualización, ratón y teclado. El acceso humano que figura pendiente en la comprobación anterior queda confirmado por el usuario. El alta de Google/Instagram y la disponibilidad de `onia.investigacion` aún no están confirmadas. [Recibo de la confirmación](../../../04-operacion-agentes/evidencias/cuentas-secundarias-20261108/control-humano-confirmado-v1.json).

La comprobación técnica anterior se conserva a continuación con su fecha original.

8nov2026,aproximadamente21:55America/Caracas (9novUTC). Sergio aplicó el perfil preparado desde su acceso SSH. Se comprobó el archivo root:root0644 y su hash aprobado; restricción global AppArmor userns=1 conservada.

## Qué pasó las pruebas

1. **Chromium con sandbox:** chrome://sandbox informa namespaces PID/red y Seccomp-BPF activos. Procesos renderer observados con Seccomp2 y NoNewPrivs1; etiqueta AppArmor onia-chromium-1252. No flags de desactivación de sandbox. El proceso browser principal conserva Seccomp0/NoNewPrivs0; no se afirma que todos los tipos de proceso tengan las mismas capas. Página pública HTTP200, título y texto leídos, captura conservada.
2. **Visor privado:** Xvfb autenticado y x11vnc/websockify operativos. `ss` confirma sólo127.0.0.1:5908 y127.0.0.1:6088. Clave incorrecta rechazada y correcta aceptada a través de noVNC/WebSocket. Carpeta/perfil0700, clave0600. No hay autenticación Google ni Instagram todavía.
3. **Teclado y ratón desde un cliente de prueba en el VPS:** formulario sintético, clic para enfocar, escritura `onia123`, cambio de título comprobado en la ventana X y botón accionado con ratón. Página pública restablecida. **Falta el control desde Windows por Sergio**, que además valida el túnel externo.
4. **MCP nativo en Codex:** retoma del mismo SID01a1bd30-efe1-7f90-b6e0-811def9bf063. Las cuatro llamadas navigate/snapshot/screenshot/close completaron sin el bloqueo anterior de aprobación. Sol6.1high observado, cero hijos. Captura abierta por la ejecutora. Informe publicado en su rama en ec24b88b5511009dc3eac3e63f3fea007fe3dacd; la tarea AV completa aún espera revisión independiente. [Informe de la ejecutora](https://github.com/oninteligenciaartificial/onia/blob/ec24b88b5511009dc3eac3e63f3fea007fe3dacd/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/PRUEBA-MCP-RETOMA.md).

No se usan cookies o perfil de Sergio para MCP: esa prueba fue aislada. El visor humano usa `~/operacion/cuentas/analisis-onia/browser-profile`, sin endpoint de depuración remota. El wrapper corregido autoriza sólo cuatro herramientas por proceso; no se cambió aprobación global. AppArmor fue aplicado por Sergio, no por la ejecutora.

## Abrir desde Windows

Si la terminal muestra `PS C:\Users\PC>`, está en Windows. Ejecutar el comando completo desde esa ventana de PowerShell para consultar la clave privada en el VPS:

```powershell
ssh root@187.77.16.63 "cat /home/onia-codex-worker/operacion/cuentas/analisis-onia/clave-visor.txt"
```

El `cat /home/...` sin `ssh` sólo corresponde a una consola que ya está dentro del VPS; en PowerShell buscaría una ruta de Windows inexistente.

No pegarla en el chat ni ponerla en URLs. Es una clave del visor, distinta de cualquier contraseña de cuenta.

En **otra ventana de PowerShell**, mantener abierto el túnel:

```powershell
ssh -N -o ExitOnForwardFailure=yes -L 127.0.0.1:6088:127.0.0.1:6088 root@187.77.16.63
```

Conservar el usuario, puerto y opciones de identidad del SSH que ya funciona si difieren del ejemplo root/22. Este comando no abre una consola remota: queda esperando mientras transporta el visor. No concede nuevos permisos ni cambia SSH del servidor. Si6088 está ocupado en Windows, usar6089 sólo en el primer puerto y abrir el visor en6089.

Abrir en el navegador de Windows:

```text
http://127.0.0.1:6088/vnc.html?autoconnect=1&resize=scale
```

`localhost` y `127.0.0.1` señalan el equipo donde está abierto el visor. El túnel transporta la conexión al VPS; no mueve Chromium ni su perfil a Windows. Si la aplicación ofrece otra dirección local con un puerto distinto, no asumir que coincide con 6088: comprobar el canal antes de cambiar la dirección.

Ingresar la clave del visor. Debe verse Chromium del VPS con la página pública. Probar teclado/ratón antes del alta. Chromium, red, archivos y perfil permanecen en el VPS; Windows sólo presenta el visor. No se comprobó aún la autenticación/túnel desde ese equipo.

Cuando el control funcione, Sergio puede crear personalmente el correo elegido en la interfaz oficial de Google y después la cuenta secundaria de Instagram. `onia.investigacion` es el nombre elegido, no una disponibilidad confirmada. Contraseña, recuperación y verificaciones se ingresan sólo en las interfaces oficiales; no capturar ni automatizar esa fase. No se ha creado cuenta ni iniciado sesión por el agente.

## Estado y cierre del acceso

El navegador y visor quedan abiertos temporalmente para la intervención autorizada; no se instaló servicio de arranque ni scheduler. Consultar o detener sólo este conjunto mediante:

```bash
python3 ~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py estado
python3 ~/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/cuentas-analisis/20261108/browser-vps.py detener
```

Detener conserva perfil y archivos. Para reabrir, usar `iniciar` cuando no haya instancia viva. La tarea queda `en_espera` del control humano; eso no apaga este visor preparado para Sergio. No se declara aceptación completa del encargo.

Cuota antes de retomar MCP:35% semanal usado a21:44:43Caracas, saldo adicional0; compartida por la cuenta. Sin compras ni API paga.

## Diagnósticos conservados

- El HTML actual de example.com no tiene el h1 antiguo: el primer control falló por esa expectativa, aunque la página respondía200 y tenía título/cuerpo válidos. Se cambió a contenido realmente observado; no era un fallo de red.
- Chromium reescribe `/proc/PID/cmdline` como una cadena con espacios. El primer recolector que esperaba cada argumento separado por NUL no encontraba procesos. Se corrigió y se conservaron las pruebas anteriores.
- La automatización de un dataURL largo por la barra de direcciones perdió prefijos en varios intentos y produjo búsquedas públicas del HTML sintético, sin secretos. No se determinó la causa exacta de esos atajos. Se separó la prueba de entrada usando un archivo sintético abierto por la instancia ya existente y se enfocó explícitamente el campo con el ratón; esa prueba y el clic pasaron. El control de Sergio desde Windows sigue siendo una verificación necesaria.
- Todas las capturas de pruebas se conservan fuera de Git. Los archivos antiguos y errores MCP anteriores permanecen intactos. No se tocó producción, n8n, Docker, servicios existentes ni el checkout original sucio.

Recibos saneados: [sandbox](../../../04-operacion-agentes/evidencias/cuentas-secundarias-20261108/sandbox-activo-v1.json) y [visor/MCP](../../../04-operacion-agentes/evidencias/cuentas-secundarias-20261108/visor-y-mcp-verificados-v1.json).

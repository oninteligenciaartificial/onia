# Retoma v4 del corte de montaje WSL

Preparada para el encargo `homelab-conexion-20261109`, desde `f4479eb301c0b5364021fbbed0183d99c4685d13`. **Pendiente revisión independiente del commit de entrega y publicación de la coordinadora en master. No aplicada en la PC. HOMELAB sigue sin aceptación.** La autorización existente permite continuar esta misma alta; no se necesita otro permiso general. La ejecución administrativa local corresponde a Sergio.

El [encargo v4](ENCARGO-RETOMA-MONTAJE-v4-20261111.md) sustituye el briefing histórico: no conectar ni modificar la PC desde esta sesión. Puerto2222 ajeno y excluido. Sólo DESKTOP-0GGGNMF / Ubuntu WSL2; laptop excluida. El registro canónico y el briefing del coordinador no se modificaron.

## Cambio y estado que admite

v3 rechazaba el montaje observado `/usr/lib/modules/6.18.33.2-microsoft-standard-WSL2`, tipo `overlay`, antes de entrar en bwrap. El fixture conservado reproduce ese rechazo. v4 sólo admite exactamente ese montaje, único, con directorios canónicos controlados por root y sin escritura de grupo/otros. Rechaza otro kernel, filesystem, duplicados, enlaces y descendientes montados. Después del bind de `/usr/lib`, crea un tmpfs vacío sobre `/usr/lib/modules` y lo vuelve de sólo lectura. CHECK exige que esté vacío y que escribir allí falle. Los demás controles de montaje, usuario, Windows, namespaces, seccomp, sudo, SSH y huella se conservan.

La opción nueva `--resume-mount-control` requiere `--apply` y el respaldo ORIGINAL. Comprueba identidad cerrada UID/GID1001, grupo exclusivo, password bloqueado, shell nologin y respaldo previo sin la cuenta, además de:

- Árbol exacto de v3: `login` y `work` vacíos, configuración mínima, canarios y CHECK anterior; metadatos exactos, sin enlaces ni montajes extra.
- Wrapper v3 SHA256 `15bb695532d1d433ee6a8bf5e94e296b7f813328214039a24045d3279f8a41bd` y CHECK v3 `a5b29f52275be780ac5bbbfedf5633325a9a6fb56c3a81cfdff54b10c54e5ed2`. Fixtures extraídos del instalador v3 `3e6406591fa37c8518c42f5a4cc3e7e83885285e5836621988911b66d1e656be`; no se acepta un wrapper arbitrario.
- Runtime y configuración SSH con sus bytes revisados. Por el orden real de v3, ya debe existir el directorio SSH con **sólo** `sshd_config`; la inferencia anterior de ausencia del directorio en ALTA-DETENIDA-v3 no acredita el estado real. Si falta o difiere, esta retoma se detiene.
- `ld.so.cache` y `localtime` cotejados byte por byte con fuentes actuales seguras del host. Sólo se admite el enlace de zona horaria bajo `/usr/share/zoneinfo`. Una actualización o diferencia requiere diagnóstico; no se adopta contenido desconocido.
- Sin llave, archivo pending, recibo de alta ni unidad publicada; puerto2224 libre. No modifica el SSH personal.

Primero repite el control PE obligatorio, valida SSH y ejecuta la candidata como worker mediante Python aislado, sin instalarla. Ese CHECK previo comprueba aislamiento sin escribir la prueba de persistencia. Si falla, no sustituye archivos v3 ni publica acceso.

Tras pasar, conserva copias con metadatos y manifiesto SHA256 en el nuevo respaldo privado `/root/onia-worker-originales-<fecha>/estado-v3/`, con sincronización a disco antes de sustituir. Conserva runtime, configuración y CHECK v3 en su sitio; guarda CHECK v4 aparte y sustituye atómicamente sólo el wrapper autenticado. Un marcador `retoma-v4.json` impide repetir una retoma parcialmente aplicada. El CHECK del wrapper instalado prueba también escritura en el workspace. Sólo después se conserva el orden anterior de recibo, servicio dedicado, listener/huella y publicación de llave.

No hay rollback automático ni eliminación de originales. Si ocurre un corte después de guardar el marcador, quedan respaldos y cuenta cerrada hasta los pasos de habilitación; si falla durante esos últimos pasos puede quedar el servicio local iniciado. **Conservar y diagnosticar, sin repetir.** El marcador no acredita un alta exitosa.

## Un único archivo para Sergio

Después de revisión favorable del commit exacto y publicación en master, abrir el [instalador único alta-onia-worker.py](alta-onia-worker.py) con la cuenta que tiene acceso al repo privado y usar **Download raw file**. Guardarlo como `Downloads\alta-onia-worker-v4.py`, conservando v1/v2/v3. No hace falta descargar fixtures ni tests. El ejecutor no publica master ni puede afirmar que ya lo revisó otra sesión.

SHA256 v4: `0f6ca971dd570d8e783061ee1f4f58c7517f165dbf2fdb3452a9dc4140282cc1`.

En **PowerShell de DESKTOP-0GGGNMF**, una vez:

```powershell
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ne 'DESKTOP-0GGGNMF') { throw 'Solo la PC de casa autorizada' }
$oniaSetupV4 = Join-Path $env:USERPROFILE 'Downloads\alta-onia-worker-v4.py'
if (-not (Test-Path -LiteralPath $oniaSetupV4 -PathType Leaf)) { throw 'Falta el instalador v4 descargado' }
$oniaHashV4 = (Get-FileHash -LiteralPath $oniaSetupV4 -Algorithm SHA256).Hash.ToLowerInvariant()
if ($oniaHashV4 -ne '0f6ca971dd570d8e783061ee1f4f58c7517f165dbf2fdb3452a9dc4140282cc1') { throw 'Hash distinto: detenerse' }
$oniaPathV4 = @(wsl.exe --distribution Ubuntu --exec /usr/bin/wslpath -u $oniaSetupV4)
if ($LASTEXITCODE -ne 0 -or $oniaPathV4.Count -ne 1) { throw 'No se pudo localizar el archivo en Ubuntu' }
$oniaLinuxV4 = ([string]$oniaPathV4[0]).Trim()
if (-not $oniaLinuxV4.StartsWith('/')) { throw 'Ruta WSL no valida' }
wsl.exe --distribution Ubuntu --user root --exec /usr/bin/python3 -I -B $oniaLinuxV4 --apply --resume-backup /root/onia-worker-originales-20261110T173148Z --resume-mount-control
$oniaExitV4 = $LASTEXITCODE
if ($oniaExitV4 -ne 0) { throw 'ALTA DETENIDA: conservar salida y archivos; no repetir ni cambiar protecciones' }
```

Este bloque usa sintaxis de Windows PowerShell5.1: sin `&&`, operador ternario ni variables reservadas. `--exec` conserva la ruta como argumento, incluso con espacios; se valida salida y código de `wslpath` antes de invocar Python. WSL selecciona explícitamente distro y usuario; `-I -B` evita módulos del directorio de descarga y bytecode. **No ejecutado en PowerShell/WSL en esta sesión**; compatibilidad revisada estáticamente, no demostrada en Windows.

Si el hash falla, no ejecutar. Si aparece `ALTA DETENIDA`, guardar únicamente ese diagnóstico saneado y el hash usado, conservar todos los archivos y parar. CHECK informa código, tamaños, hash de stderr e indicios fijos, sin volcar stderr, entorno o salida arbitraria. No intentar otro flag, elegir otro backup, abrir firewalls ni desactivar protecciones para continuar. No publicar shadow, claves privadas, respaldos o perfiles. `alta_local=OK` sólo acredita el resultado local informado.

## Evidencia y brechas

[Recibo de pruebas de esta entrega](VERIFICACION-v4-20261111.json). Suite final: 33 pruebas, 32 correctas y una integración omitida por defecto. Se cubren el fallo v3, excepción exacta de montaje y máscara, tipos/rutas/descendientes, estados alterados, respaldos, preservación ante fallo de CHECK o copia, repetición, permisos/enlaces, fuentes del host y diagnóstico saneado. Las propiedades root y mountinfo de los casos WSL están simuladas; no constituyen un alta real.

La integración se intentó explícitamente y falló en la guarda de fuente sobre montaje separado del sandbox. Un bwrap mínimo real confirmó además `No permissions to create new namespace`, rc1. No se relajaron montajes ni namespaces para pasar. No se instaló el worker ni un servicio en el VPS; no se accedió a la PC, puerto2222, producción o credenciales privadas.

| Pendiente | Responsable y próxima acción | Criterio de cierre |
| --- | --- | --- |
| Revisión/integración | Coordinadora: repetir checks, revisor distinto del commit exacto, publicar master | Veredicto bueno vigente y hash remoto comprobado |
| Alta real | Sergio: descargar ese instalador y ejecutar el bloque una vez | `alta_local=OK`, CHECK de módulos y aislamiento, listener/huella |
| SSH remoto | Ejecutor autorizado posterior: ruta Tailscale y llave dedicada, según [ALTA-ONIA-WORKER](ALTA-ONIA-WORKER.md#después-de-alta_local-ok-acceso-tailscale) | Host key confiable fijada antes de autenticar; UID/grupos, aislamiento, persistencia entre conexiones y rechazo de acceso no autorizado comprobados |
| WSL persistente | Sergio y ejecución autorizada posterior: ventana para cierre/logout/reinicio | Acceso y función sobreviven las condiciones realmente probadas; no basta systemd activo |
| Orquestación | Coordinadora, después de esas comprobaciones y alcance propio | Ensayo acotado, lease/fencing/recuperación conforme a SCHEDULER; no se implementó ni lanzó aquí |

Modelo/esfuerzo efectivos y cuota inicial/final no expuestos a esta ejecutora: desconocidos. Se documenta esta intervención desde el commit base; no se inventa número total de intentos del harness ni consumo monetario. No se abrieron hijos ni otras sesiones.

Fuentes primarias contrastadas: [Bubblewrap, operaciones de montaje](https://github.com/containers/bubblewrap/blob/main/bwrap.xml) documenta que `--tmpfs` crea un filesystem nuevo y `--remount-ro` lo hace de sólo lectura; [Microsoft WSL](https://learn.microsoft.com/en-us/windows/wsl/basic-commands#run-a-specific-linux-distribution-from-powershell-or-cmd) documenta la selección explícita de distribución y usuario. Esas opciones no sustituyen el CHECK real pendiente.

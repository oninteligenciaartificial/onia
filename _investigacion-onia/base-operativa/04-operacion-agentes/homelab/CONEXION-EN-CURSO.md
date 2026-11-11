# HOMELAB: conexión esencial en curso

> Siguiente paso del corte PE: [diagnóstico y retoma v3](RETOMA-PE-20261111.md). Primero diagnóstico; no repetir v2 ni dar la PC por conectada.

> **Último intento:** la retoma revisada también se detuvo; ver [ALTA-DETENIDA-v2-20261110.md](ALTA-DETENIDA-v2-20261110.md). Quedaron archivos nuevos y la cuenta cerrada. No repetir el alta inicial ni la retoma v2 sobre ese estado: falta diagnóstico y una retoma segura. Los documentos anteriores se conservan como historia. La prioridad vigente de Sergio es ingresos hasta14nov; no usar el homelab como capacidad disponible antes de verificarlo.

## Avance de alta · 9 noviembre 2026 · America/La_Paz

Huella ED25519 confiable recibida de Sergio; el contraste remoto sigue pendiente porque el puerto SSH de la PC no respondió vía Tailscale. Alta y pruebas preparadas en [ALTA-ONIA-WORKER.md](ALTA-ONIA-WORKER.md). Aislamiento probado en VPS con fixture, todavía no aplicado ni probado en WSL. No declarar HOMELAB listo. Estados y siguiente acción sólo en [homelab-conexion-20261109](../tareas/homelab-conexion-20261109.json).

9 noviembre 2026 · America/La_Paz. La autorización actual cubre Tailscale, usuario `onia-worker` sin sudo, restricción de archivos Windows y WSL siempre encendido. No cubre benchmarks/mediciones largas ni scheduler. [Tarea canónica](../tareas/homelab-conexion-20261109.json).

## Estado comprobado

- Sergio corrigió el sentido del acceso: **la PC entra al VPS**, no existe todavía una cuenta VPS→WSL configurada. La distro informada por Sergio es `Ubuntu`, `Running`, WSL2.
- Tailscale **1.104.5** instalado en el VPS en `~/operacion/homelab/tailscale`, sin sudo, desde el tar oficial amd64. SHA256 `720cbbccbfc03d8b55df72afc19e5a72e31b0f65934700aa6fa38074d4ad7bf7` cotejado con la suma oficial. Binarios/datos privados; nada de estado de autenticación en Git.
- Daemon propio en modo `--tun=userspace-networking`, puerto UDP dinámico, sin aceptar DNS/rutas ni Tailscale SSH. No modifica red/firewall/servicios existentes. Arranque manual, persistencia después de reinicio todavía no comprobada.
- Sergio autorizó el login. Estado observado **Running**, nodo `onia-vps-worker` online; el par Windows `DESKTOP-0GGGNMF` figura online. Eso acredita membresía/presencia, no SSH a WSL ni aislamiento del usuario.
- Llave ED25519 dedicada preparada, privada0600 y directorio0700. Huella pública `SHA256:nabZ8igwtpOiGoATEYzhl/F5m8DLts4+hhXD1PuS0/g`. No se reutiliza la llave GitHub.

## Puerto ajeno 2222: excluido

Se observó antes de la corrección un listener SSH en `127.0.0.1:2222`; no se hizo login ni se confió su host key. **No hay evidencia de que sea HOMELAB.** Una inspección local posterior identificó UID0 e inode274038124; PID/ejecutable no visibles con UID1004. Identificar el dueño completo requiere que un administrador consulte `ss -ltnp 'sport = :2222'` o `lsof -nP -iTCP:2222 -sTCP:LISTEN`. El agente no usó sudo, no lo detuvo ni lo volvió a usar. El preflight-v1 y el briefing originales se conservan como historia, corregidos por este estado vigente y preflight-v2.

## Qué falta y quién lo hace

1. **Codex:** preparar alta mínima y prueba de aislamiento en WSL, conservando archivos originales. Un usuario Linux sin sudo no basta si conserva `/mnt/c`, interop Windows o una shell que eluda el aislamiento. La sesión debe fallar cerrada si faltan sus controles; nunca `--no-sandbox` ni desactivar AppArmor/userns.
2. **Sergio:** ejecutar una vez el paso administrativo local en la distro `Ubuntu` y cotejar la huella pública del servidor. Es necesario porque todavía no hay usuario/llave remotos; no mandar contraseñas por chat. Sólo se pedirá ejecutar el comando después de preparar y explicar exactamente sus cambios.
3. **Codex:** comprobar SSH por Tailscale con host key fijada, usuario sin privilegios y rechazo real de `/mnt/c`, interop y rutas alternativas. No habilitar acceso general a la cuenta personal de WSL.
4. **Sergio + Codex:** configurar continuidad WSL con tarea al iniciar sesión y proceso de vida acotado, conservación/reversión; verificar cierre de terminal sin detener WSL. No ejecutar `wsl --shutdown` ni cambiar suspensión/BIOS por sorpresa. Un servicio systemd por sí solo no demuestra que WSL permanezca activo.

Tailscale sólo en Windows, no instalar otro daemon en WSL. El modo userspace del VPS usa `tailscale nc` para conexiones salientes; no crea automáticamente una interfaz del sistema ni entrada SSH convencional al VPS por su nombre Tailscale. El acceso Windows→sshd WSL con mirrored y firewall debe probarse, no inferirse del nodo online. No se ha cambiado `.wslconfig`, `/etc/wsl.conf`, usuarios o servicios de la PC.

Fuentes: [Tailscale userspace](https://tailscale.com/docs/concepts/userspace-networking), [tar oficial](https://pkgs.tailscale.com/stable/), [CLI nc](https://tailscale.com/docs/reference/tailscale-cli), [configuración WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config), [red WSL](https://learn.microsoft.com/en-us/windows/wsl/networking). [Bubblewrap](https://github.com/containers/bubblewrap) se está evaluando para el aislamiento por sesión; no está instalado ni validado en la PC por esta tarea.

Estado **en_espera** por bootstrap local/validación, no terminado. La conexión no aumenta la cuota Codex, no habilita la etapa 1 ni cambia el límite de tres. El objetivo de negocio actual es el [cerebro + panel](../evidencias/cerebro-panel-usable-20261109/PLAN.md), pendiente de su sí.

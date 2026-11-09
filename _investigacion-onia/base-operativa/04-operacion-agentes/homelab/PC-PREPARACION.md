# Preparación de HOMELAB: pasos separados, sin ejecutar

Todo lo siguiente pertenece a F2 o posteriores y requiere su sí. F1 sólo mide VPS. Los valores y archivos actuales de la PC son los informados por Sergio; no se ha iniciado SSH hacia ella.

## Pasos de Sergio, cuando apruebe F2

1. Confirmar el usuario Windows que posee la distro, el nombre exacto y versión WSL. Comandos de consulta en PowerShell: `wsl --version`, `wsl --status`, `wsl --list --verbose`. No actualizar ni reinstalar por defecto. Conservar copia fechada de `.wslconfig` y `/etc/wsl.conf` antes de cualquier edición; fusionar las secciones existentes, no reemplazarlas a ciegas.
2. Hacer los cambios administrativos acotados de WSL, usuario y SSH tras revisar sus archivos finales. Las contraseñas se escriben en su terminal, nunca en chat. Crear `onia-worker` sin sudo y comprobar grupos/permisos; conservar un acceso administrativo personal separado.
3. Aprobar/configurar energía y BIOS: Windows sin suspensión mientras esté enchufado y trabajando; apagar pantalla sí puede permitirse. BIOS «restore on AC power» cuando exista y Sergio elija ese comportamiento; no hacer cambios de firmware. Tener en cuenta que BitLocker/PIN de arranque puede requerir presencia humana tras un corte: no desactivar cifrado para evitarlo.
4. Instalar/autenticar Tailscale **en Windows**, con consentimiento personal; habilitar modo desatendido si acepta el uso permanente. No instalarlo también en WSL. Confirmar plan/cuenta habilitados para este uso sin compra automática; la disponibilidad gratuita no se presupone por el nombre homelab. La instalación en VPS necesita un paso administrativo separado y autorizado; Codex no usará sudo.
5. Aprobar reglas de red mínimas, intercambiar sólo llaves públicas y verificar fingerprints de host por un canal conocido. Elegir la cuenta Windows propietaria para Task Scheduler; Sergio introduce cualquier credencial requerida por Windows. No registrar contraseñas en XML o Git.
6. Autorizar las pruebas de desconexión, reinicio y recuperación en una ventana sin trabajo personal pendiente. El primer ensayo de lease puede simular caída de conexión del worker; no exige cortar corriente físicamente ni matar WSL.

## Configuración candidata de WSL

Archivo Windows `%UserProfile%\.wslconfig`, **ejemplo a revisar según versión, no aplicado**:

```ini
[wsl2]
memory=12GB
processors=12
swap=4GB
networkingMode=mirrored
dnsTunneling=true
firewall=true
# Candidato pedido: confirmar comportamiento en la versión instalada.
vmIdleTimeout=-1

[experimental]
autoMemoryReclaim=gradual
```

`memory` es un techo, no RAM adicional. 12 GiB deja poco margen si Windows también trabaja: empezar con el límite actual de 10 GiB y pasar a 12 sólo en la prueba autorizada si Windows conserva al menos 3 GiB disponibles sin paginación/latencia sostenida. `processors=12` permite los hilos virtuales; no obliga al ASR a usarlos todos. Mantener inicialmente 4 GiB de swap; no borrarlo ni usarlo como capacidad de RAM.

La documentación distingue apagado de VM y de distribución. Describe `vmIdleTimeout` en milisegundos, pero esa tabla no garantiza por sí sola que `-1` mantenga viva la distro. En versiones compatibles documenta `[general] instanceIdleTimeout=-1` para deshabilitar el apagado automático de la distro. Confirmar versión antes de agregarlo. `autoMemoryReclaim=gradual` es una propuesta para devolver caché gradualmente; no elegir un valor no reconocido. [Configuración oficial](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

Archivo Linux `/etc/wsl.conf`, fusionado con el existente:

```ini
[boot]
systemd=true
```

Comprobar después PID 1 y sshd. **Systemd por sí solo no mantiene WSL vivo**, según [Microsoft](https://learn.microsoft.com/en-us/windows/wsl/systemd). Los cambios de WSL pueden requerir cerrar/reiniciar la VM; `wsl --shutdown` afecta todas las distros activas, por lo que sólo Sergio lo ejecutaría tras preservar su trabajo en una ventana aprobada. Reversión: conservar configuración nueva y restaurar valores de la copia anterior, con otra ventana de reinicio; no borrar distros o discos.

## Arranque persistente, sin prometer disponibilidad absoluta

Tarea de Windows propuesta: al iniciar Windows, con retraso de red de 60 s, bajo **la cuenta que tiene registrada la distro**; no SYSTEM ni otra cuenta por conveniencia. Configurar «ejecutar aunque el usuario no haya iniciado sesión» sólo si Sergio acepta y verifica sus requisitos. No elevar privilegios del worker. No iniciar otra instancia si ya está activa; reintento acotado, por ejemplo cada minuto hasta tres fallos y después aviso local.

Acción propuesta, con el nombre real de distro confirmado:

```text
Programa: C:\Windows\System32\wsl.exe
Argumentos: --distribution <DISTRO_CONFIRMADA> --user onia-worker --exec /home/onia-worker/operacion/homelab-worker
```

`homelab-worker` **no existe todavía**: sería el wrapper en primer plano del worker F2, no otro scheduler. Mantener un proceso activo y probar duración real, cierre de terminal, logout y arranque sin login; una opción INI o una tarea registrada no acredita esas pruebas. La parada manual revoca/drena primero; la política de reinicio no debe ignorar un marcador de deshabilitación. Conservar/exportar la tarea antes de editar; reversión mediante deshabilitarla tras drenaje, no borrarla.

## Tailscale Windows → WSL: alcance y validación

La recomendación oficial evita ejecutar Tailscale a la vez en Windows y WSL. [Tailscale/WSL](https://tailscale.com/docs/install/windows/wsl2). Su modo desatendido mantiene el nodo Windows disponible tras logout; no arranca WSL por sí mismo. [Modo desatendido](https://tailscale.com/docs/how-to/run-unattended). Mantener política de renovación/reautenticación de nodo; no desactivar caducidad globalmente como atajo.

Mirrored requiere una versión compatible de Windows/WSL; mejora integración de red, pero **no demuestra** que el sshd Linux sea alcanzable por la IP Tailscale de Windows. Probar, después de autorización: tailnet VPS↔Windows, SSH por llave VPS→WSL y salida WSL→VPS, fingerprint del servidor Linux y rechazo de un origen/llave no autorizado. Confirmar conflicto con OpenSSH de Windows si usa también puerto 22; elegir puerto alternativo dedicado antes de abrirlo. [Red mirrored](https://learn.microsoft.com/en-us/windows/wsl/networking).

Grants/ACL y firewalls Windows/Hyper-V: permitir únicamente nodo coordinador/administrador autorizado y puerto SSH elegido. No cambiar `DefaultInboundAction` a Allow ni abrir todo el rango Tailscale/LAN. Confirmar soporte de filtro por dirección remota, conservación de reglas originales y que el tráfico no autorizado se rechaza. El puerto del visor se mantiene en loopback con autenticación y túnel; ningún reenvío de router. [Firewall Hyper-V](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/hyper-v-firewall) · [Grants](https://tailscale.com/docs/features/access-control/grants).

Si mirrored no alcanza sshd, dejar F2 bloqueada con diagnóstico y proponer un túnel específico iniciado por el worker u otra alternativa para aprobación. No instalar Tailscale en ambos sitios de la PC, exponer SSH público ni aplicar un portproxy global para «hacerlo funcionar».

## Pasos de Codex tras el sí y los pasos personales

- Revalidar repo, versión WSL/Ubuntu/Python, arquitectura, recursos, permisos y llaves públicas. Preparar archivos y comandos administrativos exactos para Sergio; Codex no adquiere sudo. No asumir que paquetes/wheels del VPS sirven en Python de Ubuntu 26.04.
- Preparar entorno Python aislado y pesos/locks en almacenamiento Linux de WSL, no en el checkout sucio ni compartir un perfil personal. Cualquier instalación de paquetes/modelos debe figurar en el alcance F2; sin CUDA para GT 730, Docker o npm implícitos. Registrar versiones/hash/licencias. No copiar autenticación Codex: Sergio hará login propio si se autorizan sesiones allí.
- Implementar/probar el worker pull mínimo, heartbeat, lease/fencing y checkpoints descritos en [SCHEDULER](SCHEDULER.md), con una sola tarea ASR. Registrar salida y revisión; no despachar otros carriles en F2.
- Preparar Chromium separado sólo tras aprobación del componente browser: perfil nuevo, directorio privado, usuario sin root, sandbox ON, visor autenticado loopback. No migrar cookies/perfiles. Verificar navegación pública y captura; si falla userns/AppArmor, diagnóstico y corrección mínima para aprobación, nunca `--no-sandbox` o relajación global. No ingresar cuentas automáticamente.

## Afinación ASR CPU y control de calidad

Probar `cpu_threads=4` y después `6`, `num_workers=1`, `OMP_NUM_THREADS` igual al valor elegido. El parámetro explícito no cero prevalece sobre OMP en faster-whisper; registrar ambos. Seis núcleos físicos no son doce trabajadores gratuitos. Evitar concurrencia anidada; no ejecutar pruebas 4/6 simultáneamente. [Implementación faster-whisper](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py) · [CTranslate2 rendimiento](https://opennmt.net/CTranslate2/performance.html).

Una tarea ASR de F2 puede contener estas variantes acotadas sobre el mismo clip autorizado de 60–90 s, con transcripción de referencia revisada por Sergio. Calidad y rendimiento son pruebas diferentes:

1. Mismo audio/idioma/modelo/beam/VAD/segmentación: comparar int8 frente a float32. Usar pesos fuente que no hayan perdido precisión por cuantización previa; convertir cómputo a float32 no restaura información perdida. Anotar hash de pesos, compute type real y VAD. [Cuantización CTranslate2](https://opennmt.net/CTranslate2/quantization.html).
2. Después comparar 4/6 hilos con igual precisión y opciones. Medir tiempo de pared y RTF, RSS, CPU Windows/WSL y errores. Iterar el generador completo: crear el objeto de transcripción no significa haber terminado la inferencia.
3. Sólo entonces comparar beam bajo (1) con el de referencia (5), manteniendo lo demás constante. Si faltan frases, cotejar VAD y segmentación, no atribuir la causa a int8 sin aislarla.

Criterios propuestos: ninguna frase de referencia omitida ni dato crítico alterado; degradación WER frente a float32 ≤1 punto porcentual, midiendo también WER absoluto y revisando nombres/números. La muestra pequeña no garantiza calidad universal. Si falla int8 o beam 1, conservar el resultado fallido y elegir la configuración que pase; no aceptar por ser más rápida. Si float32 también falla, la tarea no pasa sólo por comparación relativa. Mantener hashes y resumen de calidad en Git; audio/transcripción privada fuera. Sin QSV ni trabajo de CUDA GT 730.

## Docker y mejoras, después

Docker Engine dentro de WSL, no Docker Desktop, requiere otro sí y compatibilidad comprobada en ese momento; la documentación actual enumera Ubuntu 26.04. No añadir `onia-worker` al grupo docker rootful ni entregar su socket. Diseñar aislamiento/rootless o un runner separado para CI/staging y revisar sus límites. No instalar nada en el VPS para esta fase. [Docker Engine Ubuntu](https://docs.docker.com/engine/install/ubuntu/).

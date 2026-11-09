# Fuentes, comprobaciones y huecos de F0

Fecha: 9 noviembre 2026 UTC. No se conectó HOMELAB; su inventario proviene de la medición aportada por Sergio. No se lanzó carga, navegador, modelo, sesión Codex o instalación para este documento. Las consultas de metadatos de paquetes y cuota son inventario, no benchmark.

## Disponibilidad leída en VPS

| Elemento | Evidencia / límite |
| --- | --- |
| Repo | `origin/master` y HEAD coordinador en `5f1c2134e93cc73cc1dbbb7e11e59e8435b64246` al inicio; checkout limpio. Original sucio excluido de edición. |
| CLI | Git, Python3, SSH, FFmpeg, Codex, Node y npm en PATH. Disponibilidad no autoriza usar npm/Chrome en F1. |
| ASR | Metadatos locales: faster-whisper 1.2.1 y CTranslate2 4.8.5 en `~/asr/venv`. Modelo small localizado en `~/asr/modelos/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120/model.bin`; existencia, sin cargarlo ni inferir. Hash de pesos e insumo se revalidan en preflight F1. |
| Browser | `@playwright/mcp` 0.0.84 declarado en instalación existente `~/operacion/browser-piloto-20261108/package.json`; stack ya documentado. No expuesto como herramienta MCP de navegador en este turno y no necesario en F1. No reinstalado. |
| Tailscale | `which` sin resultado y contexto confirma ausente en VPS/PC. No se ejecutó instalador. |
| Tools | Shell y Git para lectura/publicación; herramienta web para fuentes; conector GitHub anunciado. No hay MCP de SSH/WSL/Windows utilizable aquí; instalar Playwright no crea un enlace a la PC. |
| Skill | `05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md` leída, junto con AGENTS, reglas, estado y memoria pertinentes. No se invocó una skill de instalación/despliegue. |
| Cuota | `payload.rate_limits.primary.used_percent=64`, `window_minutes=10080`, `credits.balance="0"`, `2026-11-09T16:58:43.186Z`; secundaria no informada. Valor compartido, no cuota de PC ni consumo atribuible a F0. No se publican rollouts crudos. |

Faltantes deliberados: sí para F1; instrumentación y perfiles/stop probados; manifiesto e insumos fijados; versión exacta WSL/build Windows/nombre distro; acceso por llave y tailnet; permisos/install de F2; referencia humana de calidad ASR; métricas PC bajo carga; pruebas de recuperación y scheduler. No se afirma su implementación por tener estos archivos.

## Fuentes primarias consultadas

1. [Microsoft: configuración WSL](https://learn.microsoft.com/en-us/windows/wsl/wsl-config): secciones, memoria/CPU/swap, mirrored, timeouts y reclamación. Opciones dependen de versión; `instanceIdleTimeout` y `vmIdleTimeout` son distintos. El archivo propuesto no es una prueba de persistencia.
2. [Microsoft: systemd en WSL](https://learn.microsoft.com/en-us/windows/wsl/systemd): activación y límite de permanencia de servicios.
3. [Microsoft: red WSL](https://learn.microsoft.com/en-us/windows/wsl/networking) y [firewall Hyper-V](https://learn.microsoft.com/en-us/windows/security/operating-system-security/network-security/windows-firewall/hyper-v-firewall): mirrored y firewall requieren verificación efectiva, sin abrir globalmente entrada.
4. [Tailscale: Windows/WSL2](https://tailscale.com/docs/install/windows/wsl2): evitar las dos instalaciones simultáneas en la PC; [modo desatendido](https://tailscale.com/docs/how-to/run-unattended) y [grants](https://tailscale.com/docs/features/access-control/grants) para disponibilidad y alcance mínimo.
5. [faster-whisper, implementación](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py), [README](https://github.com/SYSTRAN/faster-whisper): parámetros CPU, trabajadores y ejecución del generador. Registrar versión instalada en cada host, no asumir identidad con master upstream.
6. [CTranslate2: rendimiento](https://opennmt.net/CTranslate2/performance.html), [paralelismo](https://github.com/OpenNMT/CTranslate2/blob/master/docs/parallel.md), [cuantización](https://opennmt.net/CTranslate2/quantization.html): hilos y tipos de cómputo. La prueba de omisiones/calidad es criterio de OnIA, no garantía del proveedor.
7. [OpenSSH: sshd_config](https://man.openbsd.org/sshd_config): validar configuración efectiva de llave, contraseña, acceso y forwarding para el usuario acotado; no cambiar servicio de producción por inferencia.
8. [Docker Engine en Ubuntu](https://docs.docker.com/engine/install/ubuntu/): referencia para fase posterior, no instrucción de instalación en F0/F1 ni permiso para Docker VPS.

Los tiempos de lease/watchdog, presupuestos, umbrales y políticas de esta propuesta son decisiones de diseño a aprobar, no normas oficiales. No se presupone que Tailscale, WSL o int8 garanticen por sí solos seguridad, permanencia, calidad o coste cero.

# Evidencia de entrega · 12 noviembre 2026 UTC

Encargo `onia-homelab-continuidad-cpu-20261111`, rama `codex/ws-onia-homelab-continuidad-cpu-20261111`, base `60522f59f3222674cc6c9d7f9364c022c60a3a65`. En el repositorio sólo se escribió dentro de `04-operacion-agentes/homelab/continuidad-cola-20261111`. No se modificaron el registro canónico, el briefing, la cola existente ni el worker original. El commit final se informa en la entrega Git, sin autorreferenciar su hash en archivos del mismo commit.

Directora `desarrollar-y-verificar` presente en el catálogo y leída desde su fuente canónica. Leídos AGENTS raíz y de operación, bitácora, decisiones vigentes, reglas comunes, boss-memoria, ESTADO, ORQUESTACION, orquestacion.json, estructura, arquitectura y contrato/código/pruebas de la cola. Sin apoyos adicionales ni subagentes. El modelo/esfuerzo efectivos y la cuota del runtime no están expuestos a esta ejecutora: desconocidos; no se atribuye consumo ni USD. No se inició otra sesión ni se consultó ONIA-CENTRAL.

## Resultados finales

Entorno: Python 3.12.3, systemd 255. Comprobaciones terminadas a `2026-11-12T03:11:16Z`, más la comprobación de CLI vacío posterior. [checks.json](evidencia/checks.json) conserva las salidas y códigos de las verificaciones; las suites completas están en los `.txt` enlazados.

| Requisito | Evidencia y resultado |
|---|---|
| Cola original conservada | [dependencias.json](evidencia/dependencias.json): hashes de los dos módulos canónicos. `preparar.py` copia esos bytes y genera un manifiesto; el test coteja el hash y rechaza sobrescribir un destino. |
| Sintaxis local | AST de los cuatro Python nuevos y ambos módulos existentes: OK. |
| Cola original | `python3 -B -m unittest -v test_cola_homelab` desde homelab: **4/4 OK**, [salida completa](evidencia/tests-cola-original.txt). |
| Capa de recurrencia | `python3 -B -m unittest -v test_continuidad` desde esta carpeta: **11/11 OK**, [salida completa](evidencia/tests-continuidad.txt). |
| Unidad y timer | `systemd-analyze --user verify` de ambos archivos con XDG_RUNTIME_DIR temporal: **rc=0, stdout/stderr vacíos**. |
| Programación efectiva | `python3 -I -B ensayo_timer.py --dest TEMP/ensayo`: **rc=0**, dos disparos automáticos de un mismo timer de usuario transitorio: `entregado` → `sin_trabajo`; [recibo](evidencia/timer-local.json). |
| Un render y hash | FFmpeg/FFprobe originales, perfil 640×360, H.264, 48 frames, 2 s; una carpeta de intento, **177.685 bytes**, SHA-256 `4bc21ec2b0e19126d41e4c00515535b0abf365a1af647e66fa6f7056b14f6a1e`. Igual en copia local y salida del worker temporal. No se exige igualdad de bytes con otro build de FFmpeg. |
| Recuperación mismo ID | Fixture con offline, respuesta perdida después de publicar y otra instancia de cola: ID `sintetico`, tres intentos, **un render**, recuperación con `reutilizado=true`, hash verificado; segunda pasada vacía sin modificar el MP4. |
| Backoff/offline | Fixture con reloj 100 → siguiente intento 102; respuesta perdida a 103 → siguiente 107; recuperación a 108. Otro caso conserva el tope de espera de 300 s. Sin invocar SSH. |
| Exclusión mutua | Locks de cola y worker: no hay segunda pasada ni render concurrente. Se reutilizan los locks originales, incluido el descriptor que FFmpeg hereda. |
| Parada | STOP/enlace roto antes de crear cola; STOP aparecido antes del transporte; prueba programada devuelve `detenido`. Las dos unidades temporales terminaron **inactive**. |
| Cola vacía sin SSH | Prueba con funciones de SSH/procesos prohibidas y `ssh=True`; CLI real `--sin-ssh` devuelve `sin_trabajo`, rc=0 y cola 0700: [recibo](evidencia/cola-vacia.json). |
| Privacidad y fallos | Rechazo de raíz no privada y hash falso; CLI con JSON corrupto falla con código 1 y salida saneada. Paquete nuevo 0700 y archivos 0600; CLI instalado probado con `-I`. |

La prueba programada usa el worker **local en temporal**, con transporte SSH expresamente prohibido. El timer de ensayo tiene intervalo de 2 s; el de entrega es de 60 s y se verificó estáticamente. La plantilla no se habilitó como servicio permanente. Los límites de Type/timeout/recursos del ensayo corresponden a los de entrega. Se conservaron MP4/estado sólo en el temporal privado del VPS; Git recibe recibos y hashes, sin medios.

## Incidencias y límites

- El primer `systemd-analyze --user verify` devolvió rc=0 con `Failed to bind private socket: Address already in use`: colisión con el runtime del usuario, sin diagnóstico de error en las unidades. Se verificaron ambas con runtime temporal propio: rc=0 sin avisos. No se alteró el gestor activo.
- Hubo un primer ensayo transitorio satisfactorio antes de ampliar el recibo con los estados finales; se repitió sobre otra raíz nueva tras ese cambio. El recibo versionado corresponde a la versión final del fixture. Ambos ensayos mantuvieron un solo render por cola y retiraron únicamente sus unidades transitorias.
- `STOP` es cooperativo y no cancela un render ya iniciado. El modo sin SSH con pendientes registra reintentos; no equivale a pausa sin mutación. El paquete arranca con STOP para evitarlo hasta la revisión.
- No hubo SSH a la PC, nuevos perfiles, accesos, cambios de Windows, permisos existentes, Tailscale, servicios permanentes, producción, clientes, publicación comercial ni gasto. El push autorizado es sólo el de la rama del encargo.
- No se prueba en esta sesión la supervivencia del gestor de usuario, reinicio/suspensión de Windows, transporte real con la versión instalada, render de clientes ni ASR. La guía conserva responsables, próxima acción y criterio de cierre para cada brecha.
- El coordinador conserva `cerrar`, revisión independiente, aceptación e integración. Este recibo acredita implementación y pruebas, sin sustituir esos pasos.

Reproducción, instalación detenida, activación acotada, inspección y reversión: [README.md](README.md). `SHA256SUMS` verifica la integridad de esta entrega, excluido el propio manifiesto.

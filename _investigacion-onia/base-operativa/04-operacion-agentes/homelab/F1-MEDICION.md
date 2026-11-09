# F1: checklist previo y medición de capacidad

**Plan no ejecutado.** Extiende el [protocolo publicado](../../05-herramientas/2026-11-08-harness/CAPACIDAD-POR-RECURSOS-PROPUESTA-20261109.md), sin rehacer las mediciones históricas. Requiere el sí explícito de Sergio para instrumentar y ejecutar F1. La PC no participa aún.

## Checklist pre-lanzamiento

| Punto | Estado de F0 / condición antes de F1 |
| --- | --- |
| 1. Repo | `harness.py`, `trabajo.py`, `harness_sesiones.py`, preparación/asignación, retoma, cierre remoto y revisión; tope fijo tres. Existen los tres documentos previos. No existe scheduler, worker remoto o comando de medición integrado. |
| 2. Tools/skills | Git, Python, SSH, Codex y FFmpeg disponibles VPS; faster-whisper 1.2.1, CTranslate2 4.8.5 y archivo del modelo small encontrados. Skill propia `desarrollar-y-verificar` leída. Herramienta web oficial disponible para F0. No se necesita MCP en F1. Playwright MCP 0.0.84 instalado pero no expuesto como herramienta en este turno; no usarlo. Tailscale ausente; no es requisito de F1. |
| 3. Cuota | 64% usado al `2026-11-09T16:58:43.186Z`, saldo extra 0; compartida VPS/PC/coordinadores. Refrescar lectura al inicio sin llamada de pago. Proponer **2 puntos porcentuales para F1 completo**, incluida revisión; con ese inicio sería límite 66%, no un límite fijo para otra fecha. |
| 4. Huecos | Instrumentación, excepción temporal por manifiesto, ejecutor liviano sólo lectura y restricción verificable de herramientas, stop real de árboles y recolector de eventos aún no implementados. Aprobar/fijar manifiesto, IDs, commits e insumos; comprobar disponibilidad del clip y pesos por hash. No comenzar si falta observabilidad o presupuesto. |
| 5. Comando | Contrato exacto propuesto abajo; **no existe todavía** en el parser actual. Se implementaría/probaría tras el sí; no se presenta como ejecutable hoy. |
| 6. Pasos de Sergio | Para F1 sólo aprobar esta fase y su presupuesto. La preparación de PC pertenece a F2 y tiene su [lista separada](PC-PREPARACION.md); no hace falta ejecutarla ahora. |

Modelo propuesto para sesiones de medición: Sol 6.1 high; revisora distinta Sol 6.1 ultra al final, con cupo contabilizado. Cero subagentes en F1. No invocar una API de pago: la inferencia Codex usaría la cuenta actual. Un ensayo puede terminar antes por cuota y quedar inconcluso sin comprar saldo. La instrumentación también consume el presupuesto de F1: si agota el margen, se entrega el código revisable y el bloqueo, sin lanzar carga a escondidas ni ampliar el tope.

## Contrato exacto del comando de F1

Desde el checkout coordinador limpio, **después** de aprobación, implementación revisada y preflight válido:

```bash
cd /home/onia-codex-worker/repos/onia-coordinador
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py medir-capacidad \
  --plan _investigacion-onia/base-operativa/04-operacion-agentes/homelab/F1-PLAN.json \
  --host vps --muestra-segundos 5 \
  --baseline-minutos 10 --livianas 5 --livianas-minutos 20 \
  --baseline-mixta-minutos 10 --pesadas 1 --mixta-livianas 2 --mixta-minutos 20 \
  --stop-cpu-pct 75 --cpu-ventana-segundos 60 \
  --stop-memavailable-pct 20 --mem-ventana-segundos 30 \
  --stop-memavailable-inmediato-pct 10 \
  --stop-psi-memory-full-pct 1 --psi-ventana-segundos 60 \
  --stop-swap-mib-s 10 --swap-ventana-segundos 60 \
  --max-cuota-puntos 2 --reserva-revision-puntos 1 --cuota-max-edad-segundos 120 \
  --max-muestras-perdidas 3 --max-minutos 60 --gracia-cierre-minutos 10 \
  --hijos-max 0 --si-sergio
```

La redundancia entre flags y [plan](F1-PLAN.json) sirve para revisión: el futuro CLI debe rechazar discrepancias. `--si-sergio` registra autorización, no la autentica; el manifiesto necesita referencia al sí, IDs/briefings aprobados, hashes de insumos y vigencia. Esos campos están pendientes en F0, por lo que el plan **no es despachable**. Parada propuesta: `harness.py medir-capacidad detener --plan .../homelab/F1-PLAN.json --interrumpir-propias`; también inexistente hasta F1.

## Secuencia y carga

Baseline 10 min → cinco livianas 20 min → baseline 10 min → una pesada + dos livianas 20 min. Mantener los servicios existentes sin limpieza o cambios entre fases. Muestrear cada cinco segundos, aproximadamente 120 intervalos por baseline y 240 por carga, y guardar fases/huecos. Registro global único: ninguna carpeta de operación alternativa para eludir el tope. Sólo los IDs del ensayo reciben excepción temporal de cinco; al caducar vuelve el valor ordinario tres.

Livianas: auditar snapshots del repo, cobertura/enlaces, trazabilidad de patrones, aceptación del workshop, coherencia de guiones y dependencias. Las salidas van al supervisor; sin escritura sobre fuentes, Chrome, MCP, ASR, npm, builds, hijos, redes sociales o descargas. La segunda carga usa dos intentos definidos en el manifiesto; no inventar trabajo para ocupar tiempo. Un shell arbitrario no queda limitado por decir «liviana» en el prompt: perfil y herramientas deben restringirse y observarse antes de validar la clase.

Pesada: usar el ASR CPU del VPS ya existente, `small`, int8, dos hilos, lock heredado, sobre un fragmento privado autorizado y con hash. Mantener los insumos y sus resultados brutos fuera de Git. Si termina pronto, reportar solape efectivo; máximo tres pasadas previamente aprobadas, nunca simultáneas. No rellenar la ventana con procesos dormidos ni declarar 20 min de carga si sólo hubo unos minutos. El resultado puede ser insuficiente para dimensionar; eso requiere otro encargo, no extender el ensayo automáticamente.

## Métricas, tiempo y estados de actividad

Cada muestra y evento nuevo tendrá ISO 8601 UTC con zona, reloj monotónico, boot/host, tarea, intento/SID, rol y secuencia. Conservar JSONL crudo sin modificar y añadir índice lateral por evento en `~/operacion/logs/<id>.<intento>.events.jsonl`, con offset/hash y timestamp de recepción; si hay hora de proveedor, mantenerla aparte. No inventar timestamps históricos ni atribuir hora de recepción como inicio exacto del cómputo remoto. Comandos se registran por ID y etiqueta saneada, sin secretos o argumentos sensibles.

CPU p50/p90/p99/máximo, ejecución/iowait/steal por separado; `MemAvailable` p50/p90/p99 más mínimo/p1; swap in/out por delta temporal; RSS por árbol y PSS cuando se pueda, presión PSI y OOM. Revisar cuotas CPU/cgroup/afinidad y procesos de corta vida omitidos por `/proc`. Mantener carga no atribuida explícita: timestamp y coincidencia temporal no prueban causalidad.

Clasificar intervalos como `herramienta_local_activa`, `solicitud_modelo_en_vuelo`, `bloqueo_explicito` o `no_clasificable`, por eventos reales. CPU baja sola no prueba espera de API; inferencia/remoto/cola no se distinguen si el proveedor no los expone. Informar solape de sesiones productivas, tiempo esperando y muestras sin clasificación. Las llamadas al modelo se correlacionan con tokens cuando estén disponibles, sin sumar dos veces contadores acumulados o caché.

## Stop y presupuesto

- CPU: media temporal móvil de 60 s del tiempo no disponible del host (`100-idle`) >75%. Mostrar ejecución, iowait y steal para explicar el disparador. No detener por un único spike de cinco segundos.
- Memoria: disponible <20% de RAM efectiva durante 30 s, o <10% en una muestra; OOM nuevo detiene inmediatamente. PSI memoria `full avg10` >1% durante 60 s; swap in/out >10 MiB/s durante 60 s **junto con presión de memoria**. Umbrales propuestos, no leyes del hardware.
- Cuota: máximo dos puntos para todo F1. Al consumir un punto, detener carga/admisión y reservar el restante para revisión/cierre; no garantizar que baste. Parar por dato de cuota >120 s o tres muestras consecutivas ausentes. Si no puede observarse, no iniciar. Otros usos de la misma cuenta cuentan contra ese margen, aunque no sean atribuibles al ensayo.
- Duración: 60 min de ventanas como máximo y hasta 10 min de parada/preservación; sin reanudar pruebas para alcanzar una duración nominal. La revisión tiene su tiempo y cuota dentro del límite global acordado; proponer hasta 10 min, sin nuevo ensayo.
- Perfil fuera de alcance, hijo inesperado, pérdida de lease/identidad, log lleno o fallido: bloquear admisión y detener sólo procesos propios, conservando trabajo. Primero cierre cooperativo, después TERM si hace falta; no `pkill` global, no producción. Hijo incierto sigue ocupando el recurso hasta conciliación.

## Resultado y pruebas requeridas antes de una ejecución real

Tests con ejecutables/remotos sintéticos: normal tres, excepción limitada cinco/sexto rechazado, caducidad y revocación, CLI manual simultáneo, logs parciales/voluminosos/disco lleno, cuota ausente, muestras faltantes, stop con supervisor muerto e hijo vivo, retoma sin duplicar commits. El ensayo usa el supervisor y tarea existentes, sin otra plataforma. No se ejecutaron esos tests en F0: no hay cambios de código.

Publicar informe con p50/p90/p99, mínimos, cobertura, ventanas útiles, cuota fechada, entregables y fallos; revisión distinta ligada al commit y master verificado. Un aborto por presión puede ser un resultado correcto del guard, pero no valida cinco. Ni cinco livianas ni la mezcla validan cinco pesadas o dimensionan automáticamente la PC. La comparación de throughput tres/cuatro/cinco con carga idéntica sigue pendiente si se quiere optimizar N, no sólo comprobar viabilidad.

Los criterios F2/F3 usan el mismo protocolo de observación por host, añadiendo Windows y WSL y su carga personal real; no se lanza ahora un benchmark de la PC.

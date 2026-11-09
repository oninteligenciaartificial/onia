# Capacidad por recursos y loop acotado: propuesta de Codex/OnIA

**Integración HOMELAB F0:** [worker Windows/WSL, medición y scheduler VPS↔PC](../../04-operacion-agentes/homelab/README.md). Encargo actual de sólo presentación: F1 espera sí explícito, F2 conexión PC después de pasos personales, F3 política por recursos; sin cambiar el tope ni ejecutar ensayos. Se conservan íntegros los antecedentes siguientes.

9 de noviembre de 2026 UTC. Base contrastada: `7133dac7a2d028b4e283a542f0da023b3b8ebe38` en `origin/master`.

**Recomiendo medir cinco sesiones livianas y una pesada con dos livianas antes de elegir la política de cupos. El tope actual de tres es una decisión del harness, no un límite de infraestructura demostrado.** El ensayo determina qué mezcla soporta este VPS en esas condiciones; no demuestra un N universal ni cuál combinación entrega más trabajo útil. La implementación y ejecución de esta propuesta esperan el sí de Sergio. No se lanzó un benchmark, se cambió el límite ni se apagó un proceso.

La autorización anterior del piloto mínimo no se usa para lanzar ahora: el pedido actual exige presentar y esperar. La aprobación propuesta se divide en **A, instrumentación y ensayo manual**, y **B, loop**, que se decidiría después del informe A. Una aprobación de A no autoriza B ni limpieza. Se conserva el diseño anterior en [ESCALADO-CARRILES-PROPUESTA](ESCALADO-CARRILES-PROPUESTA.md).

## Qué comprobé y qué corrijo de la interpretación anterior

- `harness_sesiones.py`, `check_capacity`, línea 201 en esta base, rechaza `len(live) >= 3`. El registro y lock de operación incluyen ejecutores y revisores. No calcula CPU, RAM o una capacidad física máxima.
- Los registros privados históricos v3/v4 coinciden con sus hashes publicados. Contienen tres muestras de CPU >90%: 03:04:03 (90,34%), 03:10:05 (90,91%) y 03:17:30 UTC (92,28%). Dos están en las ventanas comparadas de tres sesiones. El muestreo es de aproximadamente cinco segundos; no demuestra la duración exacta de cada pico ni carga sostenida.
- Las medianas publicadas de esas ventanas son 43,56% y 42,88%. La decisión prudente era «capacidad de cuatro/cinco todavía no medida», no «tres es el máximo del VPS». [Recibo histórico](MEDICION-3-SESIONES-20261108.json).
- No está demostrada la atribución de la mayor parte de esos picos a n8n, Chrome o Docker. El monitor medía el host y árboles de sesiones, sin una partición exhaustiva de los servicios. Chrome puede pertenecer a una sesión; n8n puede correr dentro de Docker. Sumarlos como categorías independientes duplicaría carga. También hubo ASR duplicado durante la prueba audiovisual posterior, que pertenece a otra ventana.
- El worker actual escribe stdout directamente en el JSONL, sin añadir un timestamp de recepción a cada evento. Ya existen inicio/fin de intentos e identidad de PID; faltan la correlación por comando y las tasas de swap.
- No existe scheduler. Los estados siguen siendo `preparado`, `en_curso`, `en_espera`, `para_revision`, `aceptado`; JSON, briefing, publicación y revisión independiente se conservan.

## Recursos y cuota fechados

[Instantánea saneada y auditoría histórica](CAPACIDAD-INVENTARIO-20261109.json), consultadas sin cambiar servicios. Es una lectura diagnóstica de unos cinco segundos, **no una línea base ni una prueba de cinco sesiones**.

| Dato | Observación |
| --- | --- |
| Fecha de recursos | 2026-11-09, 15:45:46–15:45:51 UTC |
| CPU / RAM | 4 CPU lógicas; 15,62 GiB totales; 10,82 GiB `MemAvailable` |
| CPU del intervalo | 9,14% ejecución; 0,05% iowait; 7,49% steal, separados |
| Swap | 3,33 GiB ocupados; entrada y salida 0 MiB/s en ese intervalo; OOM delta 0 |
| Cuota compartida | 63% usado, ventana semanal 10080 min, a 15:45:29 UTC; saldo adicional observado 0 |
| Límites vistos | Cgroup del lector sin cuota CPU/memoria explícita; cpuset heredado 0–3. No acredita el límite de cada futura sesión. |

Steal es relevante en un VPS: una parte del tiempo no disponible puede venir del hipervisor. El ensayo lo separará de CPU consumida por nuestros procesos. La cuota es de la cuenta compartida; su diferencia no se asigna íntegramente al lote. No se harán compras ni llamadas de pago para refrescarla.

## A. Ensayo propuesto antes del loop

### Preparación y excepción temporal

Instrumentar primero el harness existente y probarlo con procesos sintéticos, sin Codex ni red. Añadir un perfil de ensayo autorizado con **cinco plazas temporales sólo para los cinco IDs aprobados**, vencimiento y contador global compartido con el CLI manual. El valor por defecto continúa en tres. Sin excepción aprobada el cuarto se sigue rechazando; no usar otra carpeta de operación o un lanzador aparte para eludirlo.

Preflight: inventario de sesiones/descendientes, permisos, límites efectivos CPU/memoria, espacio para logs, autorización del manifiesto, fecha de cuota y herramientas permitidas. Esperar si hay tareas ajenas que ocupan las plazas; no detenerlas. Revisores cuentan cuando se ejecutan. En el ensayo no hay subagentes, nuevas investigaciones ni trabajos de producción. Modelos propuestos: ejecutoras Sol 6.1 high; revisor posterior distinto Sol 6.1 ultra, fuera de las ventanas de carga y dentro del presupuesto aprobado.

Las cinco tareas livianas serían lecturas finitas de snapshots del repo: (L1) inventario de cobertura de referentes; (L2) trazabilidad de patrones a fuentes; (L3) aceptación y dependencias del workshop; (L4) contraste de guiones con reglas editoriales; (L5) auditoría de enlaces internos entre investigación y workshop. Devuelven informes estructurados al supervisor, sin modificar fuentes. Se aprueban sus IDs, entradas, aceptación y carga máxima antes del lanzamiento. No consultar redes sociales, usar Chrome/MCP, ASR, npm, builds o descargas. «API» significa sólo la inferencia cubierta por la cuenta actual o lecturas gratuitas expresamente incluidas; no habilita APIs de pago ni escrituras externas.

El perfil necesita una ejecutora de sólo lectura: hoy el ejecutor ordinario recibe escritura y encargo de commit/push, y el revisor es otro rol. No simular ejecutoras usando identidades de revisión. El supervisor/coordinador conserva sus salidas como evidencia. La carga y herramientas permitidas deben ser comprobables: un briefing por sí solo no impide que un shell ejecute trabajo pesado. Si no puede aplicarse o verificarse la restricción, ese intento no valida la categoría liviana.

### Ventanas

| Fase | Duración | Qué se mide |
| --- | ---: | --- |
| A0, baseline | 10 min | Host con sus servicios habituales; cero sesiones del ensayo. No limpiar ni cambiar producción entre fases. |
| A1, cinco livianas | 20 min | Cinco sesiones admitidas por el manifiesto; registrar concurrencia productiva real, latencia, errores y entregables. |
| A2, baseline de contraste | 10 min | Recuperación y deriva de cargas ajenas antes de la mezcla pesada. |
| A3, una pesada y dos livianas | 20 min | Una tarea pesada acotada y dos lecturas equivalentes a las anteriores. |

Muestreo cada cinco segundos con reloj monotónico: nominalmente 120 intervalos por baseline y 240 por ventana de carga, más muestras iniciales. Registrar retrasos, faltantes y fases; no interpolar huecos como éxito. Mínimo 60 min de ventanas, más preparación, revisión y cierre. El ensayo se puede abortar antes.

La pesada propuesta es **ASR CPU sobre el clip privado ya conservado de unos 46 segundos**, modelo `small` ya cacheado, int8, dos hilos y lock heredado. No instalar ni descargar modelos. Una pasada puede terminar antes de veinte minutos: registrar su duración real. Se puede aprobar de antemano un máximo de tres pasadas consecutivas para repetibilidad, separando calentamiento; nunca solaparlas ni fingir veinte minutos de carga con esperas. Si no da cobertura suficiente, el resultado será parcial y se propondrá otra ventana. Este ensayo no valida Chrome/MCP, builds o todo procesamiento de video; cada clase pesada distinta necesitaría su prueba pertinente.

Análogamente, si las livianas terminan pronto o pasan casi todo el tiempo esperando al proveedor, informar esos tiempos. No inventar tareas, relanzar indefinidamente o mantener procesos dormidos para afirmar que se probaron cinco sesiones activas. Un resultado válido exige mostrar el solape productivo, salidas verificables y distribución de tiempos.

### Métricas y atribución

- CPU host p50/p90/p99 y máximo, normalizada a 100% de la capacidad observada. Separar ejecución, iowait y steal; declarar afinidad, cpuset y cuota cgroup efectiva. Para decisiones de admisión mostrar también tiempo no disponible `100 - idle`, sin ocultar iowait o steal.
- `MemAvailable` p50/p90/p99 **más p1 y mínimo**, RSS por árbol de sesión p50/p90/p99/máximo; PSS cuando sea legible y apropiado. RSS agregado puede contar páginas compartidas varias veces.
- Swap in/out en MiB/s mediante deltas de `pswpin/pswpout` y tamaño de página, nivel de swap, PSI CPU/memoria/I/O y deltas OOM. Un contador acumulado no se presenta como tasa.
- Árbol por PID + inicio + boot + namespace, incluyendo supervisor, herramientas e hijos. Usar contadores de cgroup por sesión sólo si existe delegación utilizable, sin instalar ni reconfigurar servicios. Si sólo hay muestreo de `/proc`, declarar procesos efímeros/reparentados no atribuidos y mostrar el residual del host; no llamarlo automáticamente carga ajena.
- Cuota compartida antes/durante/después, fecha y antigüedad; tokens por SID/turno cuando el runtime los exponga, sin doble contar acumulados, caché o retomas. Un hijo no hereda una cuota «gratis». No inventar porcentajes por proceso ni convertir uso de suscripción en factura API.
- Resultado: elementos verificados por minuto, latencia p50/p90, errores/reintentos, tasa de revisión aprobada y cuota por entrega cuando se pueda medir. Un rc=0 y un proceso vivo no acreditan trabajo útil.

### Paradas propuestas, a aprobar con A

1. **CPU sostenida >75%:** media temporal móvil de 60 s del tiempo no disponible del host supera 75%, con ventana completa; abortar el ensayo. Reportar además ejecución pura para distinguir la causa. Un pico aislado de cinco segundos no dispara este criterio.
2. OOM nuevo, `MemAvailable` <20% de RAM efectiva durante 30 s, o <10% en una muestra: abortar. Swap in/out >10 MiB/s durante 60 s junto con presión de memoria, o PSI memoria `full avg10` >1% durante 60 s: abortar. Son umbrales conservadores propuestos, no límites universales del kernel.
3. Máximo del ensayo: 60 min de ventanas; hasta 10 min adicionales para parada y preservación. Presupuesto propuesto: **dos puntos porcentuales de cuota compartida desde el inicio** (con el 63% observado, 65%; recalcular al arrancar). Se revisa el presupuesto antes de ejecutar; no promete que alcance. Al llegar al límite, no empezar otra pasada, detener el ensayo y conservar lo obtenido. No gastar saldo adicional.
4. Si faltan datos de cuota por más de dos minutos o métricas por tres intervalos, detener admisión y pasar a parada controlada; dato desconocido no significa presupuesto libre. Lectura sin llamadas de pago. Si el runtime no permite esa observabilidad, preflight bloqueado hasta acordar un control viable.
5. Herramienta fuera de perfil, hijo no autorizado, PID/lease ambiguo, solape de ruta o salida del alcance: detener el intento y marcar la prueba inválida. No seguir para completar la duración nominal.

La parada de emergencia bloquea admisión y detiene **sólo los árboles del ensayo**, verificando identidad, con cierre cooperativo y luego TERM si hace falta; conserva SID, worktrees, ramas, logs y cambios. No usa patrones globales como `pkill node/chrome` ni señales a servicios ajenos. Si queda un hijo incierto, el recurso continúa reservado. Salir del loop por sí solo no detiene una inferencia pesada. Antes de la prueba real, demostrar esta parada con fixtures, incluido supervisor muerto e hijo vivo. Reanudar siempre exige conciliar el mismo intento/SID y el presupuesto restante.

### Cómo se decide N

Si A1 pasa con cobertura productiva suficiente, podemos proponer hasta cinco **livianas de ese perfil**. Si A3 pasa, podemos proponer una pesada de ese perfil más dos livianas. Ninguno habilita cinco pesadas. Si se aborta por carga ajena, no prueba que cinco sean inviables siempre: se conserva como ensayo no concluyente de esa ventana.

Para afirmar que cinco son mejores que tres o cuatro falta una comparación de cargas equivalentes y rendimiento aceptado. A0/A1/A3 no la dan por sí solas. Recomiendo decidir primero el sobre de carga seguro; si la mejora de productividad queda dudosa, presentar otra prueba de tres/cuatro livianas comparables antes de adoptar un nuevo valor. Nada cambia automáticamente al terminar A.

## Cupos por recursos

Separar dos decisiones: **admisión por presupuesto medido** y **exclusión del recurso compartido**. Una suma de pesos inventados tampoco sustituye las medidas.

| Perfil propuesto | Reserva | Concurrencia candidata, pendiente de A |
| --- | --- | --- |
| Liviana | Presupuesto CPU/RAM/cuota; sin herramientas pesadas | Hasta cinco cuando no hay pesada |
| Pesada | Una lease global de carga pesada; además lease de perfil Chromium, ASR o build concreto | Una pesada y hasta dos livianas |
| Revisor | Según las herramientas realmente necesarias; SID distinto | Consume presupuesto igual que cualquier sesión |
| Sin clasificar | No se considera liviana por defecto | Bloqueada hasta definir perfil |

La exclusión inicial impide dos pesadas simultáneas aunque usen recursos distintos. El perfil/permisos y los hijos forman parte del manifiesto. Si una tarea necesita escalar a pesada, espera la lease antes de hacerlo; no se cambia la etiqueta después del pico. El cómputo es global por VPS/operación, nunca por coordinadora. Los hijos consumen recursos del árbol y plazas de agente: cero en A; para un futuro lote, máximo uno sólo si está aprobado y presupuestado. Mantener un guard numérico de seguridad medido, además de recursos, evita admisión ilimitada.

## B. Loop propuesto, posterior al informe A

Extender `harness.py` y el JSON actual, sin otro sistema de tareas. Sólo Workshop e Investigación entrarían inicialmente; Platform y automatizaciones quedan fuera del despacho automático. Las rutas exclusivas por tarea siguen reservadas dentro de cada carril. Integración Git y `progress.md` tienen un único escritor: coordinador. No se obliga a todo un carril a usar una única sesión cuando sus subrutas y recursos no chocan; ese cambio también requiere el sí a B.

Bloque opcional de despacho: `carril`, `prioridad`, `depende_de` con ID/commit, `meta_verificable` con comprobación y salida esperada, `perfil_recursos`, manifiesto de lote/permiso, máximo de intentos, vueltas útiles, minutos y cuota. Los registros antiguos conservan funcionamiento manual. Una dependencia sólo habilita trabajo tras aceptación y commit integrado en `origin/master`; ni «terminada» ni «para_revision» bastan.

Cada pasada concilia registros y recursos, verifica vigencia/revocación, selecciona una tarea elegible por prioridad y antigüedad, y reserva antes de lanzar. Priorizar revisión de entregas para evitar acumular trabajo sin aceptar. `en_espera` o bloqueo deja constancia de causa, responsable y condición de salida; se pasa a otra tarea aprobada independiente, sin fingir que una tarea bloqueada está aceptada. No hace llamadas al modelo si no hay trabajo elegible: espera acotada y backoff.

**Vueltas útiles, no polling:** una vuelta produce una entrega, corrección o cambio de estado comprobable. Propuesta inicial para B: un lote, máximo seis vueltas útiles, 60 min, una corrección por tarea y presupuesto de cuota aprobado aparte. `progress.md` será una proyección del JSON y los eventos, con tarea/SID/modelo/esfuerzo, meta, evidencia, commit, bloqueo y siguiente paso. Un commit por vuelta con cambios verificables; no commits vacíos cada cinco segundos. Ejecutores publican su rama; sólo después de revisión buena se acepta e integra serialmente. Conservación y retoma usan el mismo ID/SID y control de revisión esperada.

Comandos **propuestos, todavía inexistentes**, sobre el CLI actual:

```text
harness.py cola plan --lote ID
harness.py cola iniciar --lote ID --max-vueltas 6 --max-minutos 60 --max-cuota-puntos 2
harness.py cola detener --lote ID
harness.py lote revocar ID
harness.py cola detener --lote ID --interrumpir-propias
```

`detener` cierra admisión; `revocar` invalida el permiso aun tras reinicio; la variante de interrupción aplica sólo a sesiones propias con preservación comprobada. El proceso que vigila recursos debe seguir supervisando mientras haya carga viva. Reinicio reconcilia PID/SID, intentos, commits y leases antes de hacer nada; no duplica una entrega ya publicada. Avisos de bloqueo quedan en `estado`, `progress.md` y una bandeja local deduplicada. Telegram, n8n, mensajes y otros destinos no se activan por aprobar el loop; requieren su autorización específica.

## Timestamps y cambios de código a revisar antes de ejecutar

Los logs crudos actuales no se reescriben. Para eventos nuevos, un recolector único conserva los bytes originales y un índice lateral `~/operacion/logs/<id>.<intento>.events.jsonl`: UTC de recepción, monotónico, boot, secuencia, offset/hash de línea original, tarea, intento, rol, PID/inicio, SID y tipo de evento. El timestamp del proveedor se conserva por separado si existe. La hora de recepción no se presenta como hora exacta de ejecución remota.

Correlacionar inicio/fin/resultado de herramientas por ID de llamada; usar etiquetas de comando saneadas, nunca volcar secretos o argumentos completos al informe Git. Un comando shell puede ejecutar varios hijos; el evento y el muestreo de cinco segundos no prueban causalidad por sí solos. Las trazas anteriores sólo tendrán timestamps recuperables de sus fuentes; no inventar horas por mtime de todo el archivo. El recolector debe drenar stdout/stderr sin bloquear al hijo; disco lleno o fallo del logger provocan parada controlada y registro del fallo, no pérdida silenciosa.

| Archivo propuesto | Fase y comprobaciones |
| --- | --- |
| `05-herramientas/scripts/harness_sesiones.py` y `harness.py` | A: excepción temporal por manifiesto en el check global, ejecutor sólo lectura, supervisión/recolección y reserva/stop. Conservar gate previo al hijo y publicación/revisión existentes. |
| Nuevo `harness_telemetria.py` | A: lector de métricas y análisis de intervalos, cuota fechada y eventos indexados; sin daemon permanente. Fixtures para deltas, reset de contadores, huecos, percentiles y ventanas. |
| `test_harness_sesiones.py` y nuevos tests focales | A: límite normal 3, excepción de cinco sólo para IDs autorizados y antes del vencimiento, sexto rechazado, CLI manual simultáneo, recursos/árboles, logs parciales y grandes, disco lleno, stop y retoma sin duplicados. Cero Codex real en tests. |
| `trabajo.py`, `test_trabajo.py` | B: campos opcionales, meta comprobable, referencias y ciclos inválidos, autorización por lote, migración compatible; conservar evidencias inmutables. |
| Nuevo `harness_despacho.py` y tests | B: selección, revisión prioritaria, rutas, dependencias en master, deduplicación, reinicio, presupuesto, caducidad/revocación y proyección `progress.md`. Reutiliza el supervisor existente. |
| Reglas comunes, ORQUESTACION y diseño de carriles | Documentar sólo las capacidades aprobadas e implementadas; nunca hacer pasar una propuesta por comando disponible. |

Pruebas de aceptación A: salidas y perfil comprobados, ausencia de procesos duplicados, prueba negativa de parada, todas las mediciones con denominador y cobertura, comparación baseline/carga y revisión independiente. Pruebas B añaden bloqueo de dependencias, ausencia de despachos fuera del lote y veredicto distinto vigente antes de aceptar. Código y resultados se publican en GitHub; datos privados y eventos sin sanear no.

## Limpieza propuesta, sin ejecutar

La antigüedad o el swap ocupado no acreditan desuso. No se consultó Docker ni se modificó servicio alguno. Cgroup identifica contenedor, pero no identifica su función comercial, dependencias o política de reinicio. Los valores siguientes son instantáneos y los PID deben revalidarse antes de cualquier acción futura.

| Candidato observado | RSS / VmSwap | Impacto posible y condición previa | Reversión propuesta |
| --- | --- | --- | --- |
| LiteLLM, PID 1932, UID 0, contenedor; ~549 h | 7,70 / 582,37 MiB | Puede ser gateway de modelos. Confirmar dueño, clientes y servicio exacto; parar puede cortar llamadas. **No habilitado para apagar.** | Arranque del mismo servicio con la misma configuración/volúmenes, sin recrear o actualizar; comando pendiente de identificar su gestor con autorización. |
| Ruby/Rails, PID 10155, UID 0, contenedor; ~549 h | 256,48 / 91,48 MiB | Función exacta y trabajos en curso desconocidos. Puede servir app/colas. **No habilitado.** | Mismo servicio/configuración; revisar salud y cola. No prometer recuperar trabajo en memoria o conexiones cortadas. |
| Next, PID 3107/1440125/1440793, UID 0/1001, contenedores; ~191–550 h | 366,19 / 115,22 MiB agregados | Puede servir paneles en uso. Hay que identificar cada instancia y dependientes. **No habilitados.** | Arrancar sólo las instancias detenidas conservando artefactos, puertos y configuración. Sin reinstalar/build durante reversión. |
| Chromium, 16 procesos UID 1004; ~3,46–4,28 h | RSS sumado 2016,99 MiB; VmSwap 0 | Incluye el navegador de análisis con cuentas. No está acreditado que sea inactivo; cerrar corta control, pestañas y posibles capturas. Candidato sólo tras confirmar leases libres y que Sergio no lo usa. | Apertura mediante el gestor existente y el mismo perfil persistente, sandbox y visor autenticado en loopback; comprobar página pública. No garantiza recuperar estado volátil de pestañas. |

**Ningún proceso queda autorizado para detenerse con este informe.** Primero identificar servicio, propietario, dependencias, gestor de reinicio y comprobación de salud; después presentar la acción exacta y su reversión. No adivinar comandos Docker/systemd ni usar `kill` sobre PID antiguos. No tocar n8n, Docker, app-server, producción ni cuentas para mejorar un benchmark. No usar `swapoff`, vaciar cachés, borrar perfiles o limpiar archivos. La lectura observó cero swap activo; liberar swap ocupado puede aportar menos que evitar una tarea pesada duplicada.

## Riesgos y vuelta al modo manual

- Espera de red/modelo y cuota compartida pueden limitar antes que la CPU. Un pico aislado, un mínimo bajo de RSS o cinco procesos vivos no bastan para dimensionar.
- Fases con carga ajena distinta no permiten una resta causal simple. Informar deriva; si cambia mucho, resultado inconcluso. Revisar steal y presión además de CPU.
- Un loop necesita idempotencia, stop real de árboles y límites verificables; no sólo un `while`. Fallo de observabilidad cierra admisión.
- A termina por caducidad/revocación de la excepción; el CLI vuelve al tope 3. B revoca el lote y vuelve al CLI manual. No borrar JSON, logs, ramas, worktrees o perfiles; no revertir código bajo supervisores activos. Si hay un hijo incierto, mantener reserva y conciliar antes de otra ejecución. Revert de código sólo después del cierre de procesos propios y con compatibilidad de registros.

## Fuentes consultadas

- Repo y recibos enlazados arriba; código de `harness_sesiones.py`, `trabajo.py` y documentación de ORQUESTACION, contrastados con el master indicado. Inventario nuevo sin secretos en el JSON adyacente.
- [Kernel: /proc](https://docs.kernel.org/filesystems/proc.html): `MemAvailable` estima disponibilidad; RSS, PSS y swap tienen alcances distintos. Contadores CPU/VM y PID deben interpretarse con intervalos e identidad, no como tasas instantáneas o prueba de desuso.
- [Kernel: PSI](https://docs.kernel.org/accounting/psi.html): presión mide tiempo de espera por recursos, complementando utilización; `full` de CPU a nivel sistema no es una métrica útil de saturación.
- [Kernel: cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html): los límites son jerárquicos; la ausencia de límite en una hoja no permite ignorar ancestros. Una medición del lector no demuestra la configuración de cada futura sesión.

Consulta de fuentes y recursos: 9 de noviembre de 2026. Los umbrales, perfiles, presupuesto y comandos nuevos de este documento son propuestas de OnIA, no capacidades instaladas ni reglas del proveedor.

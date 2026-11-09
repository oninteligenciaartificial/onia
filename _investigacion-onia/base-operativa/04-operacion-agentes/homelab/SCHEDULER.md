# Scheduler por peso VPS ↔ HOMELAB: diseño pendiente

Sólo diseño F0. F1 conserva tres como límite ordinario y usa una excepción temporal de ensayo. F2 prueba un worker manual con una tarea. **F3**, tras otro sí y las medidas, reemplazaría el control fijo por admisión según recursos y presupuesto. Se extienden `harness.py`, `trabajo.py` y `harness_sesiones.py`; no se crea un sistema paralelo de tareas.

## Autoridad, carriles y cupos

El VPS mantiene el JSON canónico, aprobación del lote, prioridad/dependencias y registro operativo de leases bajo un solo lock/transacción. GitHub conserva snapshots durables, commits y resultados; no usar commits o polling de Git como mutex distribuido. El journal privado de leases es parte de operación del harness, sin una segunda lista editable de tareas. Heartbeats no producen commits cada quince segundos.

Workshop e Investigación serían los carriles iniciales. Automatizaciones conserva diseño/manual sin producción, n8n o envíos; Platform excluida. Cada tarea reserva subrutas bajo identidad de repo, aunque sus worktrees estén en hosts distintos. El coordinador es único escritor de `progress.md`, registro y master; integración Git es exclusiva.

| Clase | Admisión propuesta |
| --- | --- |
| Liviana | Lecturas/inferencia remota acotadas; reserva CPU/RAM observadas y presupuesto Codex. Puede compartir host si queda margen. |
| Revisor | Identidad/SID distinto, snapshot de commit sólo lectura. Consume recursos y cuota; si necesita herramientas pesadas también obtiene su reserva. |
| Pesada | ASR, FFmpeg/video, Chrome/MCP o builds; presupuesto medido por clase/host. Inicialmente una pesada por host y límites globales de recurso. |
| Exclusiva | Reserva indivisible, no un peso arbitrario que se pueda compensar con RAM: ASR, perfil browser o integración. Puede acompañar a una pesada o revisión. |

Inicialmente una lease **ASR global** y una por cada perfil browser; el perfil autenticado de análisis tiene un único propietario, no dos copias sincronizadas. Una pesada en PC más livianas en VPS es la mezcla preferida. Browser y ASR no se admiten juntos en PC hasta medir esa mezcla. Los pesos futuros representan demanda medida (CPU, RAM, I/O, cuota), no valores inventados 1/2/3 sumados sin base. Guard adicional de máximo de agentes por host/global derivado de las pruebas, no crecimiento ilimitado. Los hijos son parte del árbol y presupuesto; cero en F1/F2, máximo uno sólo en lotes F3 que lo autoricen y contabilicen.

F1 sólo valida VPS. En F2 medir Windows/WSL con ASR 4/6 hilos y carga de Windows real; después proponer la capacidad PC. No sumar «4 vCPU + 12 hilos» como dieciséis CPU equivalentes ni duplicar cuota. Guard de memoria del host Windows independiente del de WSL. Perfil desconocido bloquea despacho; una liviana pide nueva reserva antes de usar una herramienta pesada.

## Protocolo pull propuesto

1. PC inicia conexiones salientes al coordinador por OpenSSH sobre tailnet, con llave dedicada y host key fijada. Endpoint restringido a operaciones de worker, sin shell general/agent forwarding. El helper no evalúa strings como shell y valida tamaños, rutas, hashes y permisos. No se instala todavía.
2. `hello/heartbeat` envía worker ID, boot/namespace, versión/commit, capacidades y recursos observados, carga activa y último checkpoint. Cadencia propuesta 15 s. VPS decide si está elegible; la PC no se asigna una tarea por leer la cola.
3. `claim` bajo lock concede tarea/rol/attempt, hash de briefing y entradas, ruta asignada, host permitido, presupuesto, recursos, **generación de fencing** y lease de 90 s. En un mismo intercambio persistir intento antes de habilitar carga, como el gate del supervisor actual. Dos workers no pueden recibir la misma generación. Reserva de cuota global antes de iniciar cualquier Codex, no por host.
4. Worker verifica que puede cumplir el perfil, obtiene código por commit y artefactos privados autorizados por hash, y trabaja en un checkout propio sobre almacenamiento Linux. Un ID/tarea y un escritor por salida. El input y manifiesto necesarios para fallback deben estar durables en VPS antes de empezar, sin publicar medios en Git.
5. Renovación cada 15 s sólo si generación, lote y permiso siguen vigentes. Watchdog local independiente del modelo deja de aceptar pasos y detiene carga propia si pasan 45 s sin renovación confirmada. Usar tiempo que incluya suspensión para el plazo local, más boot ID; al despertar verificar la lease antes de continuar. No depender del reloj de pared de Windows como autoridad de TTL.
6. Checkpoints al terminar unidades recuperables (por ejemplo fragmentos ASR de 30–60 s, cuya segmentación debe pasar calidad). Copia privada al VPS con checksum y escritura atómica; sólo el acuse del coordinador confirma durabilidad remota. Registrar cursor, insumo, opciones, resultados, parent attempt y commit cuando exista. No subir sólo un hash de un archivo que quedó inaccesible en PC.
7. Worker propone resultado inmutable por hash/generación. Coordinador verifica y conserva; no concede al worker escritura directa en master. Código/resultados Git se entregan en rama/commit propio o bundle verificado por el coordinador; la publicación sólo de una generación vigente pasa por el control de integración. Un informe de ASR no crea un SID Codex ficticio.

Los nombres de operaciones son contrato propuesto, no endpoints disponibles. Identificar claves y protocolo en F2 sin imprimir secretos. El canal pull puede funcionar sin acceso entrante a WSL para despachar; aun así debe verificarse el SSH VPS→WSL solicitado para administración, y no declararlo probado por un heartbeat saliente.

## Caídas, particiones y recuperación

Al perder heartbeats, detener nuevos claims para PC. A los 90 s sin renovación el VPS expira la lease, avanza generación y marca recuperación; dejar 30 s de margen para parada/conciliación antes de reasignar cuando corresponda. La tarea vuelve a la cola del VPS. Recursos externos ambiguos/perfil browser sin cierre comprobado permanecen bloqueados; timeout de red no prueba proceso muerto.

Fencing impide que el worker viejo renueve, publique mediante el broker, acepte o sobrescriba el intento vigente. **No garantiza cero cómputo duplicado durante una partición**: el proceso remoto podría seguir vivo. Para ASR idempotente puede repetirse el último fragmento no confirmado; resultados se deduplican por hash de entrada/opciones/fragmento. Para efectos externos, navegador con estado incierto o trabajo no idempotente, no hay fallback automático: `en_espera` y conciliación. Producción/envíos siguen prohibidos.

No prometer pérdida cero de lo que nunca se confirmó fuera de PC. El contrato es conservar el estado durable reconocido, archivos y commits existentes, y aceptar una sola entrega por generación válida. Un checkpoint no es copia de RAM ni garantiza reanudar internamente Whisper; puede exigir repetir un fragmento.

SID de Codex no se presume portable entre máquinas. Si la retoma por el mismo SID está disponible y probada, usarla; si sólo está en PC offline, conservarla y recuperar desde briefing/checkpoint/commit en un intento sustituto explícito, enlazado al anterior. No copiar auth/cookies/rollouts privados sin alcance aprobado ni afirmar «retoma mismo SID» cuando fue otra sesión. Al regresar PC, conciliar antes de cualquier reanudación.

Si el VPS no puede ejecutar la pesada (cuota, recursos, perfil o acceso), la tarea sigue en su cola con bloqueo visible. No saltar controles ni trasladar automáticamente cuentas de navegador. Al caer el coordinador, el worker se detiene por falta de lease; no toma a GitHub como autorización alternativa. Reinicio del coordinador reconstruye journal/estado y verifica commits antes de conceder otra generación.

## Dependencias, progreso, parada y revisión

Extender opcionalmente el JSON actual con despacho (`carril`, `prioridad`, `depende_de` ID+commit, `meta_verificable`, perfiles/hosts/fallback permitidos, recursos, lote y presupuestos) e identidad de ejecución remota. No duplicar los estados de tarea; `en_espera` conserva bloqueo/condición de salida. Diferenciar estado de worker, lease y tarea. Dependencia satisfecha exige aceptación y commit integrado/verificado en `origin/master`.

`progress.md` se genera desde los registros: objetivo, tarea/host/SID/modelo/esfuerzo, avance con evidencia, espera/bloqueo, cuota fechada y siguiente paso. Commit por avance útil o transición relevante; no por heartbeat/poll vacío. La meta debe tener comprobación objetiva, no «seguir trabajando».

Loop F3 propuesto para el primer lote: máximo seis vueltas útiles, 60 min y dos puntos de cuota compartida como candidatos a aprobar nuevamente; una corrección por tarea. Revisiones cuentan dentro del lote, ejecutadas por otra sesión/identidad sobre el commit exacto. Una revisión obsoleta o desfavorable no permite aceptar. Prioridad a cerrar/revisar entregas y después a la siguiente tarea elegible, evitando hambre de carriles. Sin trabajo elegible, backoff acotado sin llamadas al modelo.

Parada suave corta nuevos despachos; revocación persiste y sobrevive reinicios; parada de emergencia detiene sólo árboles propios preservando checkpoints, worktrees, ramas y logs. Watchdog sigue vivo mientras haya procesos que controlar. Aviso de bloqueo deduplicado en `estado`, `progress.md` y bandeja local; Telegram/n8n no se activan por aprobar este scheduler. Desconocido en cuota/heartbeat no equivale a libre. Si otra sesión de la cuenta consume presupuesto, ambos hosts reducen admisión según el tope global.

## Archivos y pruebas propuestas

| Archivos | Cambios futuros |
| --- | --- |
| `harness.py`, `harness_sesiones.py` | F1 instrumentación, guard/stop y excepción temporal. F2/F3 host remoto, control de lease y admisión por recursos en lugar de `len(live)>=3`; revisor y CLI manual usan la misma política. Nunca buscar PID de PC en `/proc` VPS como prueba de vida. |
| `trabajo.py`, `test_trabajo.py` | Campos opcionales compatibles, validación de perfil/host/dependencia/permiso, historial de generación y checkpoint, invariantes de aceptación. |
| `harness_telemetria.py` propuesto | Reutilizar protocolo F1, incluir Windows/WSL, timestamps, clasificación de actividad y presión por host. |
| `harness_worker.py`, `harness_despacho.py` propuestos | Adaptador de ejecución/heartbeat/lease y selección; una sola autoridad del JSON, sin otro gestor de tareas. |
| Tests del harness y nuevos tests focales | Reloj simulado, remotos/procesos falsos y fallos de conexión/energía; no proveedores de pago en tests. |

Aceptación F2: heartbeat estable, key-only y acceso restringido, ASR autorizado con calidad/métricas, desconexión de worker de prueba → lease vencida → recuperación; vuelta tardía rechazada, un solo resultado/commit aceptado, archivos preservados. No basta ver dos nodos conectados en Tailscale.

Aceptación F3: claims simultáneos, lease duplicada/obsoleta, reloj cambiado, PC suspendida/reiniciada, VPS caído, checkpoint parcial/corrupto, salida tras commit antes del ack, cuotas globales, memoria Windows escasa, pérdida de logs, carrera con CLI manual, solapes entre hosts, dependencia sin integrar, revisión idéntica/obsoleta, stop/revocación persistente y máximo de intentos. Probar que un hijo incierto conserva reserva y que no se duplican commits aceptados al recuperar.

Rollback: cerrar admisión y revocar lote, drenar/cerrar procesos propios, conservar registros y reconciliar leases; volver a comandos manuales. Política de peso puede desactivarse antes de otro despacho tras cerrar workers activos, regresando a tres en VPS y worker PC no despachable. No revertir esquema/code bajo workers vivos, borrar journal o forzar worktree. Preservar configuraciones y tareas Windows previas para reversión de F2 por Sergio.

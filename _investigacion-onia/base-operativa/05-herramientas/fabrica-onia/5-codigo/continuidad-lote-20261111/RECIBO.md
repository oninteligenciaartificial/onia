# Recibo de entrega para revisión

## Identificación y autoridad

- Encargo `fabrica-codigo-continuidad-lote-20261111`, área desarrollo, una sesión ejecutora y cero hijos.
- Base inicial `aeb116090aed97763fa3be050f514bdea8aadde1`, rama `codex/ws-fabrica-codigo-continuidad-lote-20261111`, checkout limpio al inicio.
- Autorización recibida por stdin y contrastada con CIERRE-VENTA-20261111.md, plan completo y autorización final. Se aplicaron las decisiones vigentes y la directora canónica desarrollar-y-verificar, leída desde archivo. El catálogo inicial anunció esta skill. Las lecturas explícitas incluyeron AGENTS, bitácora, decisiones, estado, reglas comunes, boss-memoria, orquestación, arquitectura, diseño de carriles y API existentes.
- Referencia del flujo diario cotejada desde el commit `9a4639f245d4cf3d0f3ab3e22403fabe80e0d43b`, particularmente su adaptador al harness. La implementación utiliza las API actuales del checkout base.
- Modelo solicitado Sol high. Modelo y esfuerzo observados desconocidos por falta de evidencia efectiva del runtime. Cuota inicial/final de esta ejecutora desconocida. Los ensayos usan datos y proveedor sintéticos, con comprobación de autenticación cubierta mediante doble. Coste monetario desconocido.

## Paquete entregado

- `05-herramientas/scripts/harness_lote.py`, módulo y CLI de pasadas finitas.
- `05-herramientas/scripts/test_harness_lote.py`, 31 pruebas focales con dobles de caídas y una cadena usando las API reales, Git local y ejecutable sintético.
- [Contrato y uso](README.md), configuración deshabilitada y [ensayo real preparado para la coordinadora](ENSAYO-COORDINADORA.md).
- [Salidas reproducibles](PRUEBAS.txt), incluyendo la suite general, las focales, compilación, ayuda y hash del ejemplo.

El hash del paquete que contiene este recibo se obtiene desde el checkout entregado.

```bash
git log -1 --format=%H -- _investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/continuidad-lote-20261111/RECIBO.md
git ls-remote origin refs/heads/codex/ws-fabrica-codigo-continuidad-lote-20261111
```

## Evidencia de comportamiento

Las 31 focales cubren intención antes/después del despacho, reinicio, SID ausente, recuperación de cierre y recogida por commit/SID, ejecución terminada pendiente de cierre, revisión terminada pendiente de recogida, duplicados, revisión obsoleta, conflicto padre/hijo sin proceso vivo, proveedor y cuota ausentes/agotados, observaciones futuras/caducadas, STOP, lock, journal truncado, presupuesto agotado y reintentos fallidos.

La prueba `NativeApiTests.test_local_git_executor_close_review_accept_integrate_and_dependency` usa las fixtures existentes del harness. Recorre ejecutor sintético, commit/push de una rama local, cierre conservando worktree, revisor sintético independiente, recogida, aceptación explícita, liberación de asignación, integración/publicación en un remoto Git local y despacho de una dependencia cuyo commit queda comprobado mediante fetch. La prueba conserva dos sesiones del primer ID y una del segundo ID. Las aserciones rechazan entregas fuera de rutas y comprobaciones referidas a otro commit.

La suite general reutiliza las pruebas existentes del supervisor, retoma, Git privado y cupo global de tres. La única omisión de plataforma corresponde a junctions de Windows en este host Linux. Los resultados y códigos de salida se conservan en PRUEBAS.txt.

Durante el desarrollo se corrigió una fixture de prioridad que elegía otra tarea antes de evaluar la colisión. Se reforzó el bloqueo de dos fallos con evidencia de producto, evitando contar un nuevo intento como progreso. También se cubrieron la excepción de despacho y el fin fallido de su mismo proceso como un solo fallo, y los fallos de intentos distintos como dos fallos. La ejecución focal final pasó completa.

## Decisiones y límites de esta entrega

Se eligió una transición exitosa por tick, observaciones con vigencia máxima de 120 segundos y mínimo ilustrativo de cuota incluida del 1 %. El presupuesto real queda explícito en el manifiesto. La parada tras dos fallos sin progreso conserva la tarea y permite avanzar las independientes. La configuración entregada conserva `habilitado=false`.

La aceptación, integración y despliegue son acciones explícitas de la coordinadora. El plan expone su permiso, commit, criterio y revisor. El ensayo real y la revisión independiente de este commit quedan pendientes para la coordinadora, conforme al encargo. La evidencia disponible acredita ejecución sintética y Git local.

El módulo serializa sus propias pasadas y deduplica con el registro canónico y el journal. El lanzador compartido admite llamadas manuales posteriores que pueden repetir una revisión. La coordinadora debe mantener un solo escritor de las transiciones del lote y conciliar sus intervenciones manuales. Una operación admitida antes del STOP puede terminar registrándose durante una revocación concurrente. Las asignaciones inactivas de otras bases y las credenciales externas mantienen los límites del harness existente. El control del diff se realiza al cerrar, después del push de rama. Estos puntos están desarrollados en README.

Las declaraciones de cuota, cierre y conciliación proceden de la coordinadora y requieren evidencia conservada. Las pruebas de este paquete usan dobles para proveedor/cuota. La instalación activa, el registro canónico y el briefing de esta tarea quedan bajo la responsabilidad de la coordinadora. El siguiente paso es cerrar esta ejecutora desde el harness, revisar independientemente el commit remoto y ejecutar el ensayo acotado bajo la autorización vigente.

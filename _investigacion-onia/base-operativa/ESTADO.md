# Estado y entrada operativa

3 de noviembre de 2026, America/Caracas. Leer [reglas-comunes.md](reglas-comunes.md). Plan: [PLAN.md](PLAN.md). Ejecución y delegación: [ORQUESTACION.md](ORQUESTACION.md).

## Encargo vigente

Configurar el harness en el repo privado **oninteligenciaartificial/onia**, entorno **onia**, para operar sin la PC encendida. Reutilizar ese repo; ONIA Platform mantiene producto y producción separados. Sergio pidió subagentes por frentes, revisar la interfaz real de Codex y releer fuentes oficiales y de usuarios sobre harness y orquestación.

Ahora se trabaja con Codex y n8n existente. La captura de Grok Bot muestra Premium, 100 % usado; queda como complemento futuro cuando vuelva la cuota. No se agregó otra plataforma ni carga al VPS.

## Resultado comprobado

- Repo GitHub ID 1444982360, master. Scripts cloud publicados desde `66674eb`; su ausencia en «Editar onia» se debía al checkout inicial `4de11bb`.
- **Corrección en «Editar onia»** (`01a1a428-996b-77af-9f4d-cacf78486021`, durable): avance fast-forward a `f81a5b9474a211da8a976ca7fc9247c2ce6d27cc`. Tras recuperar la desconexión proxy/exec-server, instalación e inicio terminaron. No hubo reconstrucción manual ni descarte de cambios.
- **Cloud probado:** doce tests Python y un test de navegador con clic y captura aprobados. Python 3.12.14, Node 24.22.1, npm 11.9.0, Playwright 1.64.1, Chromium 156.0.8078.4. Siete fuentes de skills enlazadas; descubrimiento automático pendiente en tarea nueva.
- **n8n conectado en preparación:** N8N_API_KEY cargada en Secretos de red del propio entorno, ready y GET HTTP 200: diez flujos en la página, siete activos y más páginas. Sólo lectura agregada, sin mostrar valores ni contenido ni modificar flujos. Permisos completos y expiración no auditados.
- **Browser:** la captura muestra una pestaña junto a Entorno. Chromium se ejecutó en la VM; remote_desktop habilitado/unknown, sin herramienta oficial de control interactivo expuesta en ese turno. Control de esa pestaña, login y persistencia de cuentas sin comprobar; no descartarlos por una frase documental general.
- **Harness:** `scripts/harness.py doctor`, `preparar` y `retomar`, seis áreas en `orquestacion.json`, siete skills existentes. Reutiliza `trabajo.py`; el coordinador ejecuta y delega con sus herramientas. El CLI por sí solo no lanza agentes.
- Nuevas pruebas locales: siete aprobadas; una de enlaces simbólicos omitida por permisos Windows. Revisión independiente sin bloqueantes. Falta la suite en Linux cloud.
- Drive: ONIA archivos y cuatro carpetas creadas; metadatos leídos desde cloud. Descarga de un medio real y recuperación de entregable entre tareas pendientes.

## Siguiente acción

Subir esta entrega al repo existente y actualizar el checkout de preparación. Ejecutar doctor y test_harness.py en la VM; conservar instalación/inicio correctos. Guardar/republicar la preparación y verificar una tarea nueva con HEAD actual, siete skills, tests, navegador y GET n8n. La publicación realizada por Sergio durante el diagnóstico no acredita que incluyera el checkout corregido después.

La tarea antigua `01a1a3fb-7203-7626-895f-9059c93cc01c` observaba revisión 1 sin secreto. Ese resultado no describe el editor actual, donde la lectura HTTP 200 ya pasó.

Los errores sobre navegador, checkout y ubicaciones de la clave se conservan en [registro-de-errores.md](registro-de-errores.md), con corrección y prueba. Las instrucciones de revisar la interfaz y usar subagentes se mantienen en las reglas comunes; no son entrenamiento del modelo.

## Pendientes para ampliar la operación

| Frente | Próximo resultado verificable |
|---|---|
| Setup cloud | Guardar la preparación corregida y aceptarla desde una tarea nueva. |
| Persistencia | Recuperar desde otra tarea una entrega saneada en Git y un archivo real; operacion/ y privado/ no viajan con Git. |
| Video | HyperFrames instalado y probado en cloud; después pieza con grabación y audio reales. |
| Marketing | Oferta y demo concretas; luego guion y pieza. Conectar activos Meta y comprobar lectura. |
| Organización | Calendario y caja con entradas reales; el área actual cubre continuidad de encargos. |
| Reels | Control interactivo, registro y sesión persistente probados antes de prometer ONIA Research. |
| Automatización | Flujo n8n concreto y permisos de escritura correspondientes. Sin scheduler ni despacho n8n → Codex acreditados. |

Consultar [arquitectura.md](arquitectura.md) y [accesos.md](accesos.md). Mensajes históricos de otros bots son referencias, no prueba de despliegues actuales.

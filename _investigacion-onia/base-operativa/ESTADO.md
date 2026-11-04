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
- **Entrega 3d22878868c4e106266ff9439e732e7123c1ee6d verificada en cloud:** doctor y veinte tests aprobados sin skips, incluidos enlaces simbólicos Linux y preparar/retomar entre procesos. Revisión independiente sin bloqueantes. El resultado local de siete pruebas y una omitida queda superado para esta suite por la ejecución Linux.
- **Preparación guardada:** «Editar onia» confirmó borrador revisión 2 persistido, con Install/Start conservados y ampliados con doctor y test_harness.py. Runtime conectado/running, revisión efectiva/observada 1. No cambió red ni secretos y no publicó. Catálogo executor de skills vacío en ese turno; siete enlaces ready.
- Drive: ONIA archivos y cuatro carpetas creadas; metadatos leídos desde cloud. Descarga de un medio real y recuperación de entregable entre tareas pendientes.

### Aceptación en una sesión nueva después de publicar

Sergio confirmó la republicación y pidió crear una sesión nueva. Se creó **«onia · aceptación cloud»**, `01a1a464-5362-775d-acf1-a24ec01f600f`, host durable, entorno onia. Checkout `/workspace/onia`, HEAD `aa89a1618b59888d6b9960401cfe595e50e23469`, rama de tarea `work`, remoto correcto; revisión efectiva reportada 1 de esa instancia. No confundir ese número de revisión con el del borrador del editor.

- Doctor, comprobación de siete enlaces y veinte tests pasaron sin reparaciones ni reinstalación.
- Chromium pasó clic, cambio de estado y captura inspeccionada. n8n devolvió HTTP 200, diez flujos en página, siete activos y más páginas, sin cambios en workflows.
- Los primeros intentos de navegador/API encontraron restricciones del sandbox (PermissionError/errno 1). Pasaron al usar el mecanismo oficial `with_additional_permissions` con red habilitada, sin modificar TLS ni el sandbox.
- Las siete fuentes/enlaces son accesibles. Se aplicó `desarrollar-y-verificar` por archivo. No llegaron skills propias en el catálogo inicial observado y `skills.list(authority=executor)` devolvió vacío; esta herramienta lista paquetes por autoridad, no se acreditó equivalencia con la API nativa de proyecto `skills/list`.
- La API nativa `skills/list({cwds,forceReload})` y el control del CWD de sesión no están expuestos allí. Cambiar workdir de un comando no cambia el CWD del agente. Autodetección sin verificar; carga explícita por área disponible mediante orquestacion.json. No se hicieron copias ni se alteró la publicación para ocultar el límite.

Informe de esa VM: `operacion/evidencias/aceptacion-cloud.md`, ignorado por Git; este resumen conserva la evidencia accesible del resultado. La sesión nueva queda disponible para trabajo cloud. Aceptación técnica de código, navegador y API aprobada; aceptación de autodetección pendiente.

## Siguiente acción

Sergio pidió carga automática y chats cloud por área. Se integraron nueve skills propias, seleccionadas entre las referencias y tareas reales; el detalle de los treinta candidatos está en SKILLS-POR-AREA.md. Las dos nuevas (agenda y preparación Meta) pasaron validación y cuatro casos textuales con revisión independiente. No se instalaron treinta paquetes.

El instalador prepara enlaces a una única fuente tanto en el checkout como en `/workspace/.agents/skills`, porque el CWD inicial observado del agente es `/workspace`. `cloud/INICIO-SESION.md` define la selección y lectura de la skill por encargo incluso si el catálogo nativo no la anuncia. Código preparado; aplicación al entorno y aceptación en nuevos chats todavía en curso. La suite ampliada contiene veintiocho pruebas, incluida elección de directora por `--skill` dentro de su área. La revisión detectó y corrigió una directora de agenda que no correspondía a continuidad/mejora. No dar por aprobada toda la suite por el resultado histórico de veinte; Linux debe comprobar los enlaces.

En la sesión de aceptación se comprobaron adicionalmente perfiles de Higgsfield y Gmail, perfil y listado de tres calendarios, y las cuatro carpetas de Drive. No se generó contenido ni se escribieron correos o eventos. Meta: app existente inspeccionada en el Chrome autenticado de Sergio; no se leyeron claves, no hay API cloud conectada aún. El inventario en accesos.md distingue cada prueba.

**Preparación de 9a3d4ce en «Editar onia»:** instalación, bash -n, doctor y 28/28 tests Python aprobados sin omisiones. Navegador 1/1 con clic y captura inspeccionada. Nueve enlaces en checkout y nueve en /workspace, a una sola fuente; repetir bootstrap creó cero enlaces. Borrador revisión 2 guardado con lectura inicial de INICIO-SESION.md y selección por manifiesto; red y secretos conservados. Pendiente pulsar «Volver a publicar» y aceptar la carga en los chats nuevos. El catálogo executor sigue vacío en el editor; no se interpreta como prueba concluyente del catálogo nativo.

La tarea antigua `01a1a3fb-7203-7626-895f-9059c93cc01c` observaba revisión 1 sin secreto. Ese resultado no describe el editor actual, donde la lectura HTTP 200 ya pasó.

Los errores sobre navegador, checkout y ubicaciones de la clave se conservan en [registro-de-errores.md](registro-de-errores.md), con corrección y prueba. Las instrucciones de revisar la interfaz y usar subagentes se mantienen en las reglas comunes; no son entrenamiento del modelo. La relectura oficial y de Matt Pocock/Superpowers, con fuentes fijadas y decisiones, está en [seleccion-y-recorrido.md](seleccion-y-recorrido.md). Registro local del encargo: harness-002; su briefing se recupera con scripts/harness.py retomar harness-002 sólo donde exista operacion/.

## Pendientes para ampliar la operación

| Frente | Próximo resultado verificable |
|---|---|
| Setup cloud | Código, navegador y n8n aprobados en sesión nueva; catálogo nativo de skills aún sin verificar. |
| Persistencia | Recuperar desde otra tarea una entrega saneada en Git y un archivo real; operacion/ y privado/ no viajan con Git. |
| Video | HyperFrames instalado y probado en cloud; después pieza con grabación y audio reales. |
| Marketing | Oferta y demo concretas; luego guion y pieza. Conectar activos Meta y comprobar lectura. |
| Organización | Calendario y caja con entradas reales; el área actual cubre continuidad de encargos. |
| Reels | Control interactivo, registro y sesión persistente probados antes de prometer ONIA Research. |
| Automatización | Flujo n8n concreto y permisos de escritura correspondientes. Sin scheduler ni despacho n8n → Codex acreditados. |

Consultar [arquitectura.md](arquitectura.md) y [accesos.md](accesos.md). Mensajes históricos de otros bots son referencias, no prueba de despliegues actuales.

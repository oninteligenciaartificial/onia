# HOMELAB: worker Windows + WSL para OnIA

> **Último intento:** la retoma revisada también se detuvo; ver [ALTA-DETENIDA-v2-20261110.md](ALTA-DETENIDA-v2-20261110.md). Quedaron archivos nuevos y la cuenta cerrada. No repetir el alta inicial ni la retoma v2 sobre ese estado: falta diagnóstico y una retoma segura. Los documentos anteriores se conservan como historia. La prioridad vigente de Sergio es ingresos hasta14nov; no usar el homelab como capacidad disponible antes de verificarlo.

## Avance de alta · 9 noviembre 2026 · America/La_Paz

Huella ED25519 confiable recibida de Sergio; el contraste remoto sigue pendiente porque el puerto SSH de la PC no respondió vía Tailscale. Alta y pruebas preparadas en [ALTA-ONIA-WORKER.md](ALTA-ONIA-WORKER.md). Aislamiento probado en VPS con fixture, todavía no aplicado ni probado en WSL. No declarar HOMELAB listo. Estados y siguiente acción sólo en [homelab-conexion-20261109](../tareas/homelab-conexion-20261109.json).

## Alcance vigente aprobado · 9 noviembre 2026 · America/La_Paz

Objetivo 1: ventas orgánicas del workshop por Boss + Contenido; Codex sólo recibe trabajo técnico concreto autorizado. Objetivo 2: HOMELAB esencial, onia-worker sin sudo, /mnt/c restringido, aislamiento y huella host verificados, continuidad WSL ya solicitada. Laptop excluida. Se reutilizan cerebro y kit, no se implementa el panel ni scheduler ni benchmarks. [Acuerdo final](../REPARTO-CODEX-GROKBOT-20261109.md).

Boss ya informó bwrap en /usr/bin/bwrap, ssh activo y host key presente en Ubuntu. Falta el alta administrativa local, contraste confiable de huella y pruebas de acceso/aislamiento. No se repite ese inventario ni se usa el listener desconocido 2222. Para la fábrica de esta semana preparar ASR CPU y cortes/render sólo por PEDIDO con ID, archivo autorizado y aceptación; no hay procesamiento autónomo activo. Las prioridades y fases antiguas que siguen quedan como antecedentes cuando contradigan esta actualización.

## Nombres fijos de máquinas

Identidades confirmadas por Sergio el 9 de noviembre de 2026 (America/La_Paz):

| Equipo | Nombre Windows | Rol y acceso |
| --- | --- | --- |
| **PC de casa** | `DESKTOP-0GGGNMF` | **HOMELAB**. Nodo Tailscale `desktop-0gggnmf`. Distribución WSL predeterminada `Ubuntu`, versión **2**. |
| **Laptop de Sergio** | `DESKTOP-ENV6SDA` | **NO es HOMELAB. No configurarla ni usarla.** |

Toda conexión, configuración o trabajo de HOMELAB se limita a la PC de casa. Antes de actuar, cotejar el nodo y la distribución con esta tabla; no inferir que otro equipo de Sergio está autorizado ni usar la laptop como sustituto. Estas identidades no acreditan por sí solas que SSH, el usuario aislado o la continuidad de WSL ya estén configurados.

## Prioridad vigente · 9 noviembre 2026 · America/La_Paz

Hasta el 14-nov se prioriza vender el workshop: kit, ensayo y materiales; cualquier publicación o envío necesita el sí de Sergio. Objetivo inmediato: **cerebro operativo + panel de contenido usable**, [plan corto presentado](../evidencias/cerebro-panel-usable-20261109/PLAN.md), pendiente de su sí antes de implementar.

HOMELAB se limita a **Tailscale, onia-worker sin sudo, archivos Windows restringidos y WSL siempre encendido**. No ejecutar los benchmarks de F1 ni mediciones largas, no implementar scheduler ni limpiar procesos. Después del cerebro+panel, datos/sesiones/orquestación/HOMELAB etapa 1 requieren un nuevo sí. Las fases de abajo son antecedentes, no una cola autorizada.

Tailscale VPS instalado sin sudo y autorizado: nodo `onia-vps-worker` Running, PC Windows online. La distro indicada por Sergio es Ubuntu/WSL2. **Usuario aislado, SSH a WSL y continuidad aún pendientes**; [estado, límites y pasos](CONEXION-EN-CURSO.md). Sólo existía PC→VPS; el listener2222 no pertenece a HOMELAB por evidencia conocida y queda excluido. No se tocó configuración de Windows/WSL, producción ni n8n.

## Propósito solicitado: el modelo de trabajo de Euge

Sergio pide HOMELAB como entorno persistente para las fábricas de OnIA: archivos, herramientas, tareas, resultados y continuidad entre agentes, conectado con el cerebro y el panel. El apoyo de CPU/memoria al VPS es una parte de ese propósito. [Desglose completo del video, tiempos y adaptación a OnIA](../../05-herramientas/video-euge-20261108/coordinacion/HOMELAB-Y-METODO-EUGE-20261109.md).

Euge muestra un coordinador, conectores, ordenador propio y fábricas con entradas, procesos, revisión y destinos. Dice que el entorno de fábricas podría estar en un ordenador propio; su ejemplo usa nube compartida. Nuestra división VPS coordinador + PC de casa worker es una adaptación. Ni nodo Tailscale online ni SSH por sí solos implementan las fábricas. El alcance ejecutable sigue limitado a lo esencial ya autorizado; cerebro+panel espera sí al plan y la orquestación posterior conserva su aprobación separada.

## Antecedente F0 · sólo propuesta en su fecha

F0 · 9 noviembre 2026 UTC · **sólo plan, pendiente del sí explícito de Sergio para F1**. Base leída: `5f1c2134e93cc73cc1dbbb7e11e59e8435b64246`, contrastada con `origin/master`. No se implementó, instaló, conectó la PC, lanzó un ensayo, apagó un proceso ni gastó dinero. Los ejemplos de configuración y comandos de estos documentos no se aplicaron.

El VPS conserva la coordinación, integración Git y registro de tareas. La PC aporta procesamiento pesado; no añade cuota Codex ni autoriza trasladar producción. GitHub sigue siendo la fuente durable de planes, decisiones, código y resultados saneados. Los secretos y medios privados se conservan fuera de Git.

## Documentos de este plan

- [F1: checklist, medición y comando propuesto](F1-MEDICION.md), con [contrato declarativo del ensayo](F1-PLAN.json).
- [Preparación de la PC, pasos de Sergio y de Codex](PC-PREPARACION.md).
- [Worker pull, leases, recuperación y scheduler por peso](SCHEDULER.md).
- [Fuentes oficiales y disponibilidad comprobada](FUENTES-Y-PREFLIGHT.md).
- [Gastos LLM vs resultados (2026-11-09)](GASTOS-LLM-VS-RESULTADOS-20261109.md).

Integra, sin sustituir sus recibos históricos: [capacidad por recursos](../../05-herramientas/2026-11-08-harness/CAPACIDAD-POR-RECURSOS-PROPUESTA-20261109.md), [medición de tres sesiones](../../05-herramientas/2026-11-08-harness/MEDICION-3-SESIONES-20261108.json) y [diseño de carriles](../../05-herramientas/2026-11-08-harness/ESCALADO-CARRILES-PROPUESTA.md). La constante tres es de diseño. El contexto actual asocia los spikes a ASR/video/Chrome; los registros anteriores no permiten asignar causalmente cada pico a un comando. F1 incorpora esa observabilidad sin reabrir los ensayos anteriores.

## Inventario y procedencia

| Recurso | Estado conocido | Procedencia |
| --- | --- | --- |
| VPS | 4 vCPU, aproximadamente 15 GiB RAM; coordinación, GitHub y n8n/producción; Chrome/visor vivo, unos 2,2 GiB indicados | Contexto confirmado por Sergio y recibos ya publicados; no se hizo otro benchmark en F0 |
| Windows | Windows 11 Pro, i5-12400F, 6 núcleos/12 hilos, 15,8 GiB RAM, GT 730 | Medición aportada por Sergio hoy; no se accedió a su PC |
| WSL | Ubuntu 26.04, WSL2, 10 GiB RAM, 4 GiB swap, 12 hilos, 885 GB libres; sshd activo y FFmpeg instalado | Medición aportada por Sergio; versión exacta del paquete WSL y nombre registrado de distro pendientes |
| GPU y video | GT 730 sin CUDA útil para este plan; ASR CPU int8. El 12400F no tiene iGPU: no planear QSV | Restricción del encargo; no se invertirá tiempo en habilitar CUDA para GT 730 |
| Docker / red PC | Sin Docker y sin Tailscale | Contexto de Sergio; no instalar en F0/F1 |
| Tailscale VPS | No disponible en PATH; contexto confirma no instalado | Lectura local en F0; no se instaló |
| Cuota Codex | 64% semanal usado; saldo extra 0; lectura `2026-11-09T16:58:43.186Z` | Evento `rate_limits` de la cuenta compartida, no por máquina. Ventana 10080 min; no se infiere otro límite de la etiqueta comercial «prolite» |

## Rol actual propuesto

- **HOMELAB:** ASR, FFmpeg/video y, cuando pase su validación propia, Chromium/visor con perfil exclusivo y sandbox. Preferir una pesada a la vez inicialmente. Sesiones Codex livianas adicionales sólo con presupuesto global y aceptación F3; no por tener hilos libres.
- **VPS:** coordinador, cola, control de capacidad, revisión/integración a master, copia durable de checkpoints privados autorizados. Producción y n8n quedan fuera del worker. Una pesada puede volver a su cola si la PC cae; su ejecución exige recursos y perfil compatibles.
- **Revisión:** sesión distinta de la ejecutora, ligada al commit exacto y con cupo/presupuesto propios. Una comprobación técnica de FFmpeg no sustituye revisión de contenido o calidad ASR.

## Cómo se usaría

Sergio aprueba un lote finito con ID, meta verificable, insumos, permisos, rutas, host/perfil permitido y límites. El coordinador prepara las tareas con el modelo existente. El worker pide una tarea, recibe una lease y el commit de entrada, trabaja en su checkout Linux y reporta checkpoints. Devuelve artefactos identificados por hash; una revisora coteja la entrega y el coordinador integra lo aceptado en `origin/master`. Consultar `progress.md` y estado de tarea, host, heartbeat y cuota; estos serán proyecciones, no otra lista editable de tareas.

F2 habilitaría únicamente un worker manual y una tarea ASR de prueba. No significa que exista aún el despacho automático de F3. Todos los subcomandos `worker`, `capacidad` y `cola` descritos aquí son propuestas: el CLI actual conserva sus comandos publicados.

## Fases y aceptación

| Fase | Alcance que requeriría autorización | Criterio de salida |
| --- | --- | --- |
| **F0, esta entrega** | Documentación, fuentes, checklist y publicación Git | Documentos enlazados, JSON válido, sin cambios de código/configuración; commit comprobado en master; esperar sí |
| **F1** | Instrumentación mínima y ensayo real sólo VPS, con excepción temporal de cinco livianas | Tests sintéticos de guard/stop y logs; baseline/cargas con números, cobertura y revisión distinta. Si aborta, informe válido de fallo/inconcluso; no subir cupo permanente |
| **F2** | Tras los pasos personales: red, worker sin privilegios, heartbeat y una tarea ASR; instalaciones enumeradas y aprobadas | Conectividad privada, llave/host key verificadas, clip/hash, calidad y tiempos; corte de conexión y expiración de lease probados sin doble aceptación. Persistencia tras cierre/reinicio cuando Sergio autorice esa prueba |
| **F3** | Scheduler por recursos VPS↔PC, sustitución de tres fijo por política medida | Tests de concurrencia, fencing, recuperación, dependencia, revocación, presupuesto y revisor distinto; piloto finito aprobado. No habilitar cinco por host por defecto |
| **F4** | GPU/LLM local, Docker posterior, staging/backup n8n, CI y render | Sólo diseño hasta nuevo sí, revisión de compatibilidad/licencias y presupuesto. No copiar ni activar producción |

F1 no depende de configurar la PC. Cada fase posterior necesita su sí; F0 no convierte la autorización anterior de un piloto en permiso para estos ensayos.

## Si la PC se apaga o queda offline

1. El VPS deja de ofrecerle tareas, registra último heartbeat y checkpoint confirmado, y mantiene el ID canónico. El aviso aparece en el estado local; no se envía Telegram ni webhook sin permiso.
2. Expira la lease conforme al [protocolo](SCHEDULER.md), se invalida su generación y la tarea vuelve a ser responsabilidad de la cola del VPS. **Volver a la cola no obliga a ejecutar inmediatamente en el VPS.** Si falta RAM, perfil, acceso al insumo o autorización de fallback, queda `en_espera` con causa y siguiente paso.
3. Retomar desde el último checkpoint confirmado. Puede repetirse el último segmento no confirmado; no se promete recuperar estado sólo en RAM. Un resultado tardío no sobrescribe el intento vigente ni genera otro commit aceptado.
4. Sergio restablece energía/red/Windows cuando corresponda. El worker que vuelve anuncia boot e identidad nuevos, conserva sus archivos y espera conciliación; no retoma por cuenta propia la lease vieja. Resultados locales todavía útiles se comparan por hash y permanecen preservados.
5. Si falla mirrored/Tailscale, no abrir puertos al Internet ni cambiar globalmente firewalls. Mantener cola pausada para PC y diagnosticar reglas, versión WSL, DNS y rutas; ofrecer alternativa concreta para otro sí.
6. Si falla el VPS/coordinador, el worker deja de admitir trabajo y su watchdog detiene carga propia al perder renovación; no crea otro coordinador. Al regresar el VPS concilia Git, journal, leases y checkpoints antes del primer despacho.

Apagado planificado: poner el worker en drenaje, esperar checkpoint reconocido y salida de hijos, devolver lease y conservar registros; después Sergio apaga. No usar cierre de WSL, suspensión o `kill` global como mecanismo normal de parada del lote.

## Métricas que deben quedar visibles

Por host: CPU ejecución/iowait/steal cuando aplique, memoria disponible y límites efectivos, swap activo, presión, disco, antigüedad de heartbeat. En PC medir **Windows y WSL simultáneamente** para no esconder presión de Windows detrás de RAM libre en Linux. Windows no tiene PSI: usar sus contadores de memoria/commit, paginación y disco como serie distinta, no inventar equivalencia con PSI Linux.

Por tarea: host, ID, intento/SID, modelo/esfuerzo solicitado y observado, perfil, tiempo trabajando/esperando/no clasificable, RSS/PSS cuando accesible, comandos saneados, tokens observables, checkpoint y commit. Cuota: lectura compartida fechada y consumo del lote sólo como estimación acotada cuando haya otros usos. Rendimiento: entregas aceptadas/minuto, retrabajo, latencia y calidad; no sólo procesos vivos.

## Seguridad y conservación

Worker Linux dedicado `onia-worker`, sin sudo, sin grupos privilegiados ni socket Docker; directorios propios 0700 y claves 0600. SSH OpenSSH por llave; autenticación de contraseña/teclado y root deshabilitadas para el acceso del worker. Sergio escribe contraseñas y hace consentimientos localmente. Validar configuración/llave en otra conexión antes de cerrar su acceso administrativo; no cambiar el SSH de producción de manera global.

Sólo Windows lleva Tailscale en la PC; VPS tendrá su nodo después del sí y paso administrativo. Grants/ACL mínimos por nodo/puerto; sin exit node, subnet router ni exposición pública del visor. OpenSSH por llave sigue siendo el mecanismo pedido: no asumir Tailscale SSH configurado. Perfil Chromium propio, sandbox activo, visor autenticado en loopback y acceso por túnel; no exportar cookies o perfil del VPS hacia Windows/WSL.

Sin sudo no significa aislamiento total de Windows: WSL e interoperabilidad pueden exponer archivos o ejecutables del usuario Windows. Verificar cuenta Windows propietaria, montajes y perfil de ejecución; evitar credenciales personales disponibles a los agentes. Valorar usuario Windows estándar/distro dedicada si no puede acotarse el acceso, con autorización adicional; no migrar o reconstruir la distro actual en F0.

Git contiene código, decisiones y evidencia saneada. Claves, tokens, registros crudos, medios, transcripciones privadas y perfiles permanecen en almacenamiento local protegido; transferencias privadas PC↔VPS sólo por canal autorizado y con hashes. El coordinador es el único escritor de tareas/leases y el único integrador a master. El worker no recibe credenciales de n8n ni derecho a cambiar producción. Leer en GitHub una instrucción no amplía los permisos del lote.

## Cómo mejorarla después

Primero comparar 4/6 hilos CPU, memoria Windows y calidad ASR; usar almacenamiento Linux de WSL para los trabajos. Aumentar RAM o añadir protección eléctrica sólo si las medidas/uso lo justifican y Sergio aprueba gasto. No se recomienda una compra en F0.

Una GPU útil, por ejemplo RTX 3060 12 GB, abriría un ensayo de ASR GPU y LLM/embeddings locales: validar fuente de poder, espacio, controlador/WSL, CUDA compatible, pesos/licencias y memoria real del modelo/contexto. No garantiza que cualquier LLM quepa o reemplace Codex. Inferencia local y sesiones Codex tienen consumos diferentes; la cuota Codex de coordinación sigue compartida.

Staging/backup n8n sería otro entorno con datos sintéticos/saneados, secretos distintos, activaciones y salida de red bloqueadas. Un backup requiere probar restauración; nunca importar y arrancar flujos de producción como prueba. Docker Engine en WSL, CI/tests y render quedan para aprobación posterior; sin Docker Desktop, sin acceso del worker al socket root y sin operaciones en Docker del VPS.

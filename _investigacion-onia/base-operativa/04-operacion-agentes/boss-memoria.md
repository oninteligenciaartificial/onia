# Memoria de Boss (reglas de trabajo) — 8 nov 2026

Copia de las reglas y correcciones que Boss (Grok Bot) tiene guardadas, para que Codex pueda seguir solo si se acaba la cuota de Grok. Sin secretos ni datos privados.

## Roles
- Boss solo planifica y coordina; Codex en el VPS hace todo el trabajo.
- Boss es la jefa que habla con Sergio, decide el orden de tareas, prepara encargos y pide su aprobación.
- n8n debe correr solo, sin gastar cuota de Grok. No crear más bots de Grok hasta que haya ingresos.

## Nunca sin el sí de Sergio
- Cobrar o gastar.
- Activar, desactivar o borrar workflows de n8n (leer y editar sí se puede).
- Publicar, mandar mensajes, tocar producción.
- Modificar algo sin aprobación de OnIA. No borrar nada del VPS ni de la PC. No imprimir secretos.

## Checklist obligatorio antes de lanzar Codex
1. Qué existe ya en el repo.
2. Qué necesita Codex (herramientas, conectores MCP, skills, reglas) y si los tiene.
3. Cuota de Codex.
4. Qué falta.
5. Exactamente qué se va a lanzar.
Lanzar solo después del sí. Boss revisa el VPS por su cuenta, sin esperar que Sergio pregunte.

## Forma de trabajar
- GitHub (oninteligenciaartificial/onia, master) es la fuente central: nada está terminado hasta que esté pusheado.
- Desde la PC (DESKTOP-ENV6SDA, C:\dev\proyectos) pushear con un worktree limpio desde origin/master sin tocar su rama sucia.
- Leer el repo o investigar antes de responder; no rehacer trabajo existente.
- Proponer entregables en el chat antes de escribirlos; marcar "propuesto". Siempre proponer un plan o alternativa, no solo confirmar.
- Anotar cada corrección de Sergio y cada error en registro-de-errores.md.
- Trabajo pesado va a Codex; ahorrar cuota (modelos baratos adecuados, tareas en lote, revisar resúmenes).
- Pendiente (no limitación): dar a Codex acceso a X, n8n, Notion y Drive (pendientes/codex-conectores.md). Mientras tanto esas tareas pasan por Boss.

## Contexto del negocio
- Meta al 14 nov 2026: al menos 3.000 Bs y un workshop vendido; deuda de 3.000 Bs; sin gastar hasta el 14.
- Workshop «Tu negocio con IA: ordena, vende y automatiza» para dueños de negocio (no estilo de vida): 3 clases, Bs 50 grupal o Bs 150 VIP (5 cupos), herramientas gratis (sin cuenta de Claude).
- Clientes llegan por contenido orgánico de la marca personal; cero clientes pagos aún.

## Errores del 8 nov (corregidos por Sergio)
- Lanzar Codex sin decir qué necesitaba.
- Responder sin leer el repo.
- No revisar conectores, skills y reglas de Codex antes de lanzar.

## 2026-11-08 tarde
- Decisiones del workshop en 05-herramientas/2026-11-08-harness/00-decisiones.md (clase 1 con Claude, Bs 50, fechas 12/13/14, 1-1,5 h, referente Eric Tavera por venta y persona).
- Error: Boss respondió una vez en inglés. Corrección: siempre en español.
- Error: un encargo de commit se delegó y no se hizo; Boss lo subió ella misma.
- Instagram: la bandeja la bloqueó un control de seguridad de Instagram (pide teléfono y código). Leads no leídos; Sergio lo resuelve desde su celular.
- Codex terminó pilotos del harness (a2f64ed, 124 pruebas OK) y empezó una prueba de 3 sesiones en paralelo que no estaba en el plan comercial; pedir a Sergio si sigue o se pausa.

- Regla: todo error, corrección, decisión o plan va directo a GitHub sin esperar que Sergio lo pida.
- Plan del workshop en 05-herramientas/2026-11-08-harness/plan-workshop.md.
- Error: una subida se cortó y faltó un archivo; se rehízo.

## Corrección vigente y nuevo encargo de Sergio · 8 nov 2026

- La nota inicial de negocio no aprueba VIP: prevalece `00-decisiones.md`, Bs50 grupal aprobado y VIPBs150 propuesto. Tampoco prevalece «sin cuenta de Claude» sobre la decisión actual de clase1 con Claude; el acceso propio de alumnos/facilitador sigue por resolver.
- Sergio ordenó corregir problemas y ejecutar el encargo profundo de Grok: grupos A/B/C en paralelo, Sol6.1 high, un subagente por referente en tandas y revisores distintos Sol6.1 ultra; todo en origin/master, sin producción ni gasto adicional. La autorización actual sustituye el stop previo para este alcance. Boss conserva la síntesis final entre grupos.
- Al cierre explicar cómo manejar áreas, tareas, sesiones y revisiones para una empresa de una persona. Documentar el modelo en el repo no activa automatizaciones ni un servicio permanente.

- Durante el estudio, Sergio ofreció iniciar YouTube y consultó cuenta secundaria. Recomendación: cuenta Google exclusiva de OnIA y perfil separado, sin enviar claves/códigos/cookies por chat. Todavía no se creó ni conectó ninguna cuenta. VPS sin navegador interactivo detectado; login en PC/panel no da acceso automático al CLI. LOGIN_REQUIRED no prueba que autenticar resuelva extracción. Mantener fuentes públicas y preparar conexión comprobable antes de pedir login.

- Sergio aclara: toda ejecución de análisis y navegador debe correr en el VPS, nada en la PC. “Local” en ASR/Playwright significa instalado en el VPS; usar esa denominación explícita. GitHub conserva fuente central compartible. Correo y perfil persistente permanecen propuestas, no implementados.

- 8nov2026: Sergio solicita comparar PySceneDetect, WhisperX, PaddleOCR, librosa y MiniCPM-o sin instalar ni lanzar pruebas, preservar investigaciones activas, presentar inventario/licencias/cuota/piloto antes del sí. Después pide STOP al finalizar esta evaluación; cuentas secundarias y analizador/mirador quedan para próximo encargo. Fuente: `05-herramientas/evaluacion-av/2026-11-08/ANALISIS.md`. No se reducen criterios de aceptación de los cerebros por publicar esta evaluación.

- 8nov, siguiente encargo: Sergio autorizó preparar navegador VPS para crear personalmente onia.investigacion y pidió mapa de modelos/tareas/pausas. Luego ordenó proponer corrección AppArmor y esperar aprobación antes de aplicar; no ingresar cuentas ni interrumpir referentes. Diagnóstico efectivo: Chromium unconfined, restricción userns1, No usable sandbox. Propuesta nueva root:root0644 para ruta exacta; no cargada. Visor sintético cerrado. Ver tarea cuentas-secundarias-20261108 y cuentas-analisis/20261108/APROBACION-APPARMOR.md.

- 8nov20:03Caracas: Sergio autorizó dejar listo ahora el navegador tras la propuesta específica. No falta repetir aprobación AppArmor; falta aplicación por administrador. Ejecución del script aprobada intentada desde host UID1004, rc2 por precondición UID0, sin cambios de sistema. Fuente: cuentas-analisis/20261108/PASO-ADMINISTRATIVO-PENDIENTE.md.

- 8nov~21:55Caracas: Sergio aplicó el perfil AppArmor y confirmó uso SSH. Chromium con sandbox, visor autenticado en loopback y prueba sintética teclado/ratón pasaron. Retoma MCP mismo SID pasó cuatro herramientas y publicó ec24b88; revisión AV pendiente. Visor queda abierto para Sergio; acceso Windows y cuenta no confirmados. Fuente vigente cuentas-analisis/20261108/ACCESO-VERIFICADO-VPS.md.

- 2026-11-08T22:19:23-04:00: Sergio informó alta Google con un nombre distinto del propuesto; ver recibo saneado `evidencias/cuentas-secundarias-20261108/alta-google-informada-v1.json`. Control humano del visor ya confirmado; Instagram y perfil autenticado para análisis aún pendientes. Pidió cómo abrir frentes y continuar: secuencia concreta en EMPRESA-UNIPERSONAL.md, sin nuevos despachos ni activación de servicios.

## Encargo nocturno vigente · 9 noviembre 2026 UTC

Sergio pide avanzar mientras duerme: video Euge, Telegram/n8n y fábrica de ideas/guiones para preparar workshop y campaña. OnIA Platform excluida. Se prioriza cerebro aplicado → primeros10min workshop → automatización probada. Sol6.1 high, revisores distintos ultra; no gasto adicional, campañas, mensajes ni producción. Dos tareas del harness con rutas exclusivas, sin hijos, más ayudante existente de video; límite3 conservado y nuevo despacho suspendido al55% de cuota compartida. El contenido y la campaña son borradores hasta revisión editorial y decisiones pendientes. [Plan del lote](evidencias/noche-20261109/PLAN.md).

El piloto mínimo de carriles sí fue autorizado por Sergio (Workshop/Investigación,3cupos incluidos revisores,máx1hijo,parada/revocación e informe). No confundir ese sí limitado con aprobación del diseño completo ni decir que el scheduler ya existe. El título del diseño pasa a Codex/OnIA.

Cierre nocturno: dos entregas revisadas e integradas, Telegram sólo prueba inactiva/sintética, workshop borradores sin ensayo humano; video completo en_espera por corte y403 observados sin causa confirmada. [Informe](evidencias/noche-20261109/INFORME.md). Sin sesiones CLI activas al cerrar y sin scheduler permanente.

Continuación del9nov: cerebro consultable, kit primeros10min y lector/panel real revisados e integrados. Se corrigieron móvil y un pie PDF que el primer revisor rechazó. [Cierre y guía de mañana](evidencias/continuacion-noche-20261109/INFORME.md). No activar campaña ni atribuir Telegram/video completos; mantener revisión del piloto por Sergio antes del resto. Cuota compartida fechada y monitor cerrados; límite3 sin cambios.

9nov11:40UTC, Euge: controlSkip comprobado; Playwright se corta43.760s, Chromium existente operado visualmente supera2:09. Misma cuenta/perfil, no causa causal aislada. [Comparación y siguiente paso](../05-herramientas/video-euge-20261108/control-visible-20261109/README.md). Video completo/audio pendientes; cuota55% usado, sin nuevos despachos. Visor disponible y checkout original intacto.


9nov, cierre de resolución audiovisual: Sergio autorizó tres sesiones nativas enfocadas en el video. Navegador/audio Sol6.1 high y revisor distinto Sol6.1 ultra completaron reproducción y captura0:00–30:02 por reloj, pista original,34 muestras visuales y379 filas ASR alineadas. Entrega9f10c3e revisada y tarea aceptada con límites: sin escucha directa ni percepción visual continua acreditada; captura operada, no analizador desatendido. Se corrigieron verificaciones de truncado/PTS y reintentos ASR con lock heredado; errores conservados. [Informe y aplicación a OnIA](../05-herramientas/video-euge-20261108/RESOLUCION-20261109.md). Visor devuelto, sin ASR activo al control13:01UTC. Cuota compartida62% a12:52:40UTC; no atribuible exclusivamente a estas sesiones. Mantener3cupos; siguiente paso de negocio, ensayo del piloto por Sergio. No se activa fábrica, Telegram, n8n o campaña por este cierre.


9nov, evaluación de capacidad solicitada por Sergio: confirmar que el tope 3 es de diseño no autoriza cinco sesiones ni demuestra su rendimiento. Tres muestras históricas >90% confirmadas; medianas de ventanas 43,56%/42,88%, atribución específica a servicios no probada. [Propuesta e inventario fechados](../05-herramientas/2026-11-08-harness/CAPACIDAD-POR-RECURSOS-PROPUESTA-20261109.md). Presentado A: instrumentación y ensayo manual 10+20+10+20 min, excepción temporal para cinco livianas, luego una pesada y dos livianas, parada por recursos/cuota. B: loop posterior, aún sin implementar. Esperar el sí actual; no usar la aprobación histórica del piloto para lanzar ahora. Cuota compartida 63% al 9nov15:45:29UTC; instantánea sin swap activo no es baseline. Ninguna limpieza autorizada: LiteLLM/Ruby/Next en contenedores con dependencias desconocidas; Chromium conserva navegador de análisis. Producción, Docker, n8n y app-server intactos.


9nov, HOMELAB F0 solicitado por Sergio: sólo plan y publicación. PC medida por Sergio: Windows11Pro, i5-12400F 6c/12t,15,8GiB,GT730 sin CUDA útil; Ubuntu26.04 WSL2 10GiB/4GiB swap,12hilos,885GB libres,sshd y FFmpeg; sin Docker/Tailscale. La PC será worker pesado y Codex liviano sólo con cuota; VPS coordina sin tocar producción. [Runbook y checklist](homelab/README.md). F1 espera sí explícito, propone dos puntos de cuota total; lectura 64%/saldo0 a16:58:43UTC. F2 necesita pasos personales, red y prueba de una tarea; F3 scheduler por recursos; F4 GPU/LLM/staging sólo diseño. Ninguna autorización histórica sustituye estos gates. Timeout devuelve tarea a la cola VPS desde checkpoint reconocido, no garantiza recuperar RAM ni habilita duplicar efectos. No asumir SID portable, mirrored conectado o systemd suficiente para mantener WSL vivo. No usar CUDA GT730, QSV, Docker ni compras en F0/F1.

## 2026-11-09 tarde

Hallazgos y decisiones de Boss (America/La_Paz). Sin secretos ni IPs.

### Calendario
- «Novia» del viernes 13 movida a 18:00–21:00 (instancia única).
- Ahora solapa con «Llamadas 1 a 1 / Workshops» 18:15–19:15.
- La clase de las 21:00 del viernes todavía no está en el calendario (oferta pendiente de agregar).

### Homelab PC DESKTOP-0GGGNMF
- Windows 11 Pro; i5-12400F (6 núcleos / 12 hilos); 15,8 GB RAM.
- GT 730: sin CUDA útil → ASR en CPU con faster-whisper int8.
- WSL2 Ubuntu 26.04: 10 GiB RAM, 4 GiB swap, 12 núcleos; ~885 GB libres.
- Presentes: sshd y ffmpeg. Ausentes: Docker y Tailscale.

### Decisiones de configuración
- Quedarse en WSL2 por ahora; Linux nativo más adelante, cuando la PC quede dedicada o tenga una GPU buena.
- Tailscale en el host Windows, no dentro de WSL al mismo tiempo.
- `.wslconfig`: `networkingMode=mirrored`, `vmIdleTimeout=-1`, memoria ~12 GB.
- `wsl.conf`: `systemd=true`.
- Mantener WSL vivo con Programador de tareas; Windows sin suspensión; BIOS restore on AC.
- Usuario dedicado `onia-worker` sin sudo.

### Estado de acceso
- Solo existe SSH PC→VPS: clave pública ed25519 con comentario `hp-i5-13va@DESKTOP-0GGGNMF` agregada a `authorized_keys` de `onia-codex-worker`.
- No existe aún acceso VPS→PC.
- Boss accedió a la PC por la app de Grok Bot, no por SSH.

### Seguridad
- En el VPS, `127.0.0.1:2222` escucha y responde como servidor SSH; origen desconocido (no lo creó Boss). Identificarlo en solo lectura (`ss -ltnp` / `lsof` con sudo) antes de usarlo.
- Riesgo: WSL monta `/mnt/c`; cualquier acceso VPS→PC debe restringir `/mnt/c` para el usuario worker.

### Codex / homelab F0
- Commit `88f40eb` revisado: bueno, solo documentación.
- Problema conocido: `ESTADO.md` aún tiene texto viejo de «video en_espera».

### Prioridades
- Hasta el 14 nov: primero vender el workshop.
- Homelab: solo lo esencial (Tailscale, `onia-worker`, `/mnt/c` restringido, WSL siempre encendido).
- Objetivo #1 de Codex: cerebro operativo usable + panel de contenido.
- Después (con nuevo sí): datos, mejores sesiones, coordinación, orquestación y homelab etapa 1.
- Comparación de gastos LLM vs resultados: [GASTOS-LLM-VS-RESULTADOS-20261109.md](homelab/GASTOS-LLM-VS-RESULTADOS-20261109.md).

### Nombres de máquinas y Tailscale
- Nombres de máquinas: DESKTOP-0GGGNMF = PC de casa (homelab, nodo Tailscale desktop-0gggnmf). DESKTOP-ENV6SDA = laptop de Sergio (no es homelab).
- 13:42 (America/La_Paz): tailnet de la cuenta oninteligenciaartificial ya tiene desktop-0gggnmf (Windows) y onia-vps-worker (VPS, autorizado por Sergio). WSL: distro Ubuntu, versión 2, predeterminada. Próximo paso de Codex: usuario onia-worker en WSL sin sudo, /mnt/c restringido y probado.
- Auditoría de orquestación: [AUDITORIA-ORQUESTACION-20261109.md](AUDITORIA-ORQUESTACION-20261109.md). Veredicto: harness bien diseñado; no reconstruir. Prompt propuesto para Codex (bajar default Sol high + higiene leftovers) pendiente del sí de Sergio.


9nov17:24UTC: Sergio autoriza usar/configurar HOMELAB y avisarle de pasos humanos. No pedir otra vez aprobación general. Desde onia-codex-worker se confirmó SSH en loopback2222 y se preparó llave exclusiva privada; no hay alias/host key PC ni agente SSH utilizable. Tarea homelab-conexion-20261109 en_espera por usuario/identidad y cotejo de huella; no hubo login ni configuración remota. [Continuidad](homelab/CONEXION-EN-CURSO.md). No usar llave GitHub para PC ni desactivar verificación de host.


9nov, corrección vigente de Sergio (America/La_Paz): antes del14-nov manda workshop/venta. Cerebro+panel usable primero mediante plan corto y sí antes de implementar; reutilizar cerebro-operativo/20261109, PANEL-DIARIO y lector-panel aceptados. [Plan y presupuesto](evidencias/cerebro-panel-usable-20261109/PLAN.md). Homelab sólo Tailscale/worker sin sudo/aislamiento Windows/continuidad WSL; sin benchmarks ni mediciones largas. Datos, sesiones, orquestación y etapa1 requieren nuevo sí posterior. Recibos de ambos roles con ID, modelo/esfuerzo, used_percent inicio/final fechados, intentos, resultado, commits y retrabajo; sin USD inventados.

Sergio aclara que sólo había PC→VPS; el puerto2222 no fue creado ni reconocido por él. Excluirlo de HOMELAB: UID0/inode conocidos, PID no visible, no detenerlo ni usarlo. Tailscale1.104.5 instalado sin sudo en VPS, checksum oficial cotejado; Sergio autorizó login y se observa Running y Windows online. DistroUbuntu/WSL2 informada. Llave dedicada privada; usuario sin sudo, restricción /mnt/c y continuidad siguen pendientes del bootstrap local y pruebas. No declarar PC operativa por ver el nodo online. [Estado vigente](homelab/CONEXION-EN-CURSO.md).


9nov ~16:35 America/La_Paz: Boss documentó revisión Codex + por qué no aprovecha Grok Bot (división de trabajo, handoff cola-boss, prompts). Resultado WSL en PC de casa (~16:33): bwrap presente, ssh active, host ed25519 presente. Cuota Codex 67% a ~14:54. Prompts de auditoría y de reparto esperan sí de Sergio. No se creó cola-boss.md aún. [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md).
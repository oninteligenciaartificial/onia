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

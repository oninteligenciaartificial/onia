# Encargo fabrica-contenido-diseno-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Preparar fábrica OnIA de ideas y guiones a partir de noticias de IA y cerebros, con panel y Telegram para Sergio

## Entregable

Diseño concreto, ejemplos ficticios y ensayo reproducible sin servicios, dentro de 05-herramientas/fabrica-contenido/20261108

## Criterio de aceptación

Extiende tareas canónicas/harness sin otra cola; diseña panel como proyección y Telegram como interfaz privada; ejemplos ficticios identificados, fuentes/fechas/atribución y revisión por guion; recorrido idea→guion→revisión→decisión Sergio probado sin envíos/API paga/n8n/producción; límites y pendientes explícitos; diff exclusivo y commit/push propios.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio eligió explícitamente: «automatizacion de fabrica de contenido mediante un panel y telegram para sergio, guiones con noticias de ia, guiones mediante el cerebro y demas, esa primero para guiones y ideas de contenido». Preparar y probar ahora con datos ficticios. No implementar ni activar scheduler: pidió presentar su diseño y esperar sí; no instalar LangGraph ni paquetes ni servicios. No crear bot, pedir tokens, enviar Telegram, publicar/redsocial, tocar n8n, producción, Docker, sudo, servicios existentes, checkout ~/repos/onia sucio o secretos. No gastar/API keys: sólo esta sesión ChatGPT incluida. Cero subagentes. Una carpeta exclusiva. Leer EMPRESA-UNIPERSONAL.md, MODELOS-Y-PAUSAS, ORQUESTACION/manifiesto, CEREBRO-DIARIO.md y cerebros pertinentes, distinguiendo fichas aceptadas y parciales. No sintetizar el documento final entre grupos Grok (lo hace Boss). Noticias del fixture son FICTICIAS claramente; no inventar noticias actuales. Diseño de ingestión debe mantener fuente primaria, fecha del hecho/consulta, deduplicación y atribución. Cada idea/guion debe señalar fuentes, patrón del cerebro aplicado y qué es propuesta OnIA. Panel proyecta JSON canónico; Telegram propondrá comandos/veredictos por Sergio con identidad/destino restringido, idempotencia y confirmación para efectos externos. No prometer integración/autenticación ya hecha. El usuario aportó https://www.youtube.com/watch?v=JuAQILH7dkQ, título comprobado «Así Utilizo los Agentes de IA a Diario», Euge Oller: pidió MIRARLO, no sólo transcripción; el coordinador está resolviendo acceso. NO atribuirle prácticas ni afirmar visionado; dejar esa entrada pendiente hasta evidencia visual. Prepará plan y contrato más un ensayo offline mínimo con JSON ficticio que recorra idea/guion/revisión/decisión y casos duplicado/pendiente/fallo, sin otra cola de producción. Evitar código nuevo si basta prueba sobre APIs existentes; no crear panel web permanente. Si propuesta visual útil, sólo boceto estático local VPS sin servidor ni instalación. NO BORRAR archivos. Publicar exclusivamente carpeta asignada en tu rama propia; no modificar tareas canónicas/reglas/scheduler/harness ni integrar master. Informe con qué funciona como simulación, qué no está implementado, pasos y commit. Tiempo razonable15min; no expandir a video/render ni publicaciones.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/fabrica-contenido-diseno-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

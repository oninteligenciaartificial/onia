# Encargo guiones-tanda-automatizada-20261111

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Producir una tanda diaria verificable de cinco guiones mediante un procedimiento reproducible que use cerebro, fuentes fechadas y correcciones.

## Entregable

Pipeline/procedimiento local en automatizada, tanda v3 nueva, calendario, fuentes, export compatible y GUIA-REVISION.

## Criterio de aceptación

Reusar cerebro y tanda v2 en lectura. No editar las tandas históricas reservadas. Implementar procedimiento invocable que reciba fuentes/brief/correcciones, valide cinco piezas con propósito y construya paquete editorial compatible: T01–T05 Markdown, hashes/bytes, guiones-panel.json, calendario y estado-fabrica.json. Seleccionar ideas según referentes pertinentes con trazabilidad; personas simuladas/crítico son hipótesis, no investigación de audiencia real. La tanda mezcla venta, marca, noticia IA verificable o evergreen rotulado, segunda venta/marca y prueba. Investigar una noticia sólo con fuente primaria y fecha si hay herramientas; si no, fallback evergreen explícito. Adaptaciones horizontal/vertical por pieza, no diez ideas. Voz natural voseo, CTA coherente y marcar si canal no probado. No inventar cifras, pantallas de Claude ni hechos del día de Sergio; si falta relato real dejar entrada requerida concreta y un guion de marca sin autobiografía falsa. Demostrar una corrección aplicada a nueva versión y rechazo de datos incompletos/duplicado sin pisar salida; declarar qué parte genera el LLM y cuál es script fijo. No prometer escritura creativa/news/autoscheduler después14 sin modelo disponible. Probar compatibilidad del paquete con tanda.py del panel sin modificarlo. Duraciones estimadas hasta ensayo humano; sin aprobación editorial falsa.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio autorizó esta primera tanda y pidió STOP al entregar para revisarla con la coordinadora. Leer primero BITACORA-BOSS, DECISIONES-SERGIO y 04-operacion-agentes/evidencias/tanda-fabricas-20261111/ALCANCE-v1.md de master. Ese alcance sustituye el briefing histórico del9/10nov y sus presupuestos/ultra. Método Euge: entrada concreta -> paso evaluable -> resultado -> revisión/corrección; reutilizar lo existente y el cerebro, no repetir ASR ni capturas de videos. Fechas: viernes13 20h, sábado14 14h, lunes16 20h La Paz. Nombre: Claude de 0 a 100: tu negocio con IA; grupo50Bs, VIP150Bs,5cupos,1:1 de30min. QR+seguimiento y Sergio confirma cada pago. No tocar calendario real ni secretos/QR ni clientes, no activar n8n, no publicar contenido, no gastar, no cambiar PC. Vlog excluido. No modificar harness, AGENTS, decisiones ni registros canónicos. Sol6.1 high, sin hijos. No abrir otros frentes. Usar desarrollar-y-verificar. Consultar documentación primaria si surge una duda concreta; no investigación general.

Preparar GUIA-REVISION.md dentro de tu ruta, con comandos, resultados reales, límites y recorrido para Sergio. Si hay bloqueo conservar trabajo y explicarlo. Probar lo pertinente, commit+push sólo de tu rama, informar hash y STOP. Nada de aceptar, integrar en master o iniciar siguiente tanda. No confundir ensayo local con operación real. Contrato estado-fabrica.json y guiones-panel.json en ALCANCE-v1.md.

- Guardar generador/README/tests/GUIA-REVISION en automatizada; salida exclusivamente en salida/guiones-tanda-20261111-v3. Recursos del cerebro son lectura, cambios editoriales quedan versionados en tu ruta. No cron, no API de pago, no nuevos modelos descargados. Las reglas se aplican a una segunda salida de prueba local, no entrenamiento de pesos.
- Alcance: 04-operacion-agentes/evidencias/tanda-fabricas-20261111/ALCANCE-v1.md

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

Estado: [registro de trabajo](../tareas/guiones-tanda-automatizada-20261111.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

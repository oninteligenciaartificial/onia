import json,collections
from pathlib import Path
x=json.load(open('resultados/T012-evidencia-n8n-20261107.json')); ws=x['workflows']
# Clasificación editorial explícita: una decisión y razón por workflow.
groups={
'operación':[1,2,4,5,6,9,10,11,13,15,16,19,28,32,36,37,41,47,50,51,53,54,59,61,64,68,69,71,74,75,77,80,83,85,92,102,103,105,107,108],
'ventas':[3,20,22,30,31,40,45,48,49,52,62,78,81,89,94,96,97,101,104],
'contenido':[38,43,44,46,55,76,84,86,87,88,98,110,111],
'finanzas':[7,18,25,42,72,79,82,90,99],
'producto/DentalGest':[0,8,12,14,17,21,23,24,26,29,34,35,39,57,60,66,67,73,91,95,100,109],
'demos':[33,56,58,63,65,70,93,106],
'otra':[27]}
now={0,5,6,7,10,16,22,25,31,40,45,49,50,52,59,61,69,71,77,80,90,96,97,104}
discard={2,4,11,18,28,36,37,39,47,51,53,55,58,70,72,74,78,81,85,93,94,95,108,111}
reasons={
0:'Proteger DentalGest reduce pérdidas; comprobar restauración y solapamiento con los otros backups.',
1:'Vigilancia CI sin incidencia comercial demostrada; revisar necesidad y frecuencia antes de ampliar operación.',
2:'Guardia asociada a Claude sin alcance vigente y contraria al ejecutor único; excluir del circuito propuesto.',
3:'DM automático necesita consentimiento, deduplicación y pausa humana probados antes de sostener ventas.',
4:'Otro resumen diario añade ruido; priorizar un único digest y seguimiento de caja.',
5:'Canario de autenticación puede evitar caída del recorrido de venta; confirmar qué comprueba.',
6:'Vigilar disco protege los servicios existentes con mantenimiento acotado.',
7:'Aviso interno de pago pendiente acerca caja sin confirmar un cobro automáticamente; validar deduplicación.',
8:'Digest por clínica exige usuarios y utilidad comprobados antes de mantener otro envío semanal.',
9:'El nombre sugiere limpieza vinculada a publicaciones; aclarar efectos y alcance antes de priorizar.',
10:'Alerta solo ante fallo protege la recepción comercial existente con poco ruido.',
11:'Segundo resumen diario duplica atención; conservar una sola vista operativa.',
12:'Reporte GestiOS puede esperar hasta acreditar clientes e ingresos de ese producto.',
13:'Agenda adicional solapa recordatorios activos; escoger un único recorrido personal.',
14:'Seguimiento clínico automático requiere clientes, consentimiento y revisión de datos sensibles.',
15:'Limpieza de worktrees no acredita impacto en caja y puede eliminar trabajo; revisar alcance.',
16:'Respaldo de base protege continuidad; verificar retención y recuperación sin duplicar esfuerzos.',
17:'Cobranza a pacientes requiere facturas reales, consentimiento y política de escalado.',
18:'La descripción del aviso Telegram dice que reemplaza el aviso SMTP roto; no sumar ambos sin justificar.',
19:'Ensayo sintético sirve para validar controles, pero no aporta ingresos por sí mismo.',
20:'Envía seguimientos reales; validar baja, takeover y oferta única antes de priorizar automatización.',
21:'Sincronizar pacientes añade integración y datos personales; esperar necesidad real del producto.',
22:'Borradores sobre leads existentes concentran a Sergio en cerrar ventas con aprobación humana.',
23:'Facturas recurrentes necesitan operación comercial real y control de envíos antes de habilitarse.',
24:'Notificación de tenant útil cuando GestiOS tenga captación comprobada; evitar otro canal ahora.',
25:'Conciliación detecta discrepancias de pagos; ayuda a distinguir caja real de estados internos.',
26:'Alertas de cuota dependen de uso WhatsApp real; no consta volumen que las justifique.',
27:'Sourcing Nuvia abre otro frente sin demanda o ingreso documentados; diferir.',
28:'Reescribir agentes como ready/24-7 no demuestra actividad y contradice el estado parado del contexto.',
29:'Bienvenida automática a pacientes requiere recorrido de producto, consentimiento y minimización.',
30:'Puede reducir preparación de propuestas, pero solapa el generador oficial y añade transcripción/LLM.',
31:'QA de demos de venta evita mostrar una oferta rota; confirmar primero cuáles se usarán.',
32:'Chequeo amplio de integraciones puede esperar a definir dependencias críticas y evitar alertas duplicadas.',
33:'Demo simple puede venderse bajo demanda; no necesita un envío diario permanente.',
34:'Borrador sin credencial elegida según descripción; priorizar solo ante incidencia de producto real.',
35:'Onboarding con contactos y mensajes necesita revisión expresa y cliente real.',
36:'Recordatorios Discord duplican la agenda Telegram activa; excluir del circuito mínimo.',
37:'Resumen Discord duplica vistas de agenda sin beneficio comercial demostrado.',
38:'Generación diaria de guiones añade coste y revisión; primero cerrar una pieza/oferta completa.',
39:'La descripción declara duplicado del trial-drip del producto y apagado hasta clientes.',
40:'Captura de alta alimenta el CRM; distinguir lead Ganado de pago efectivamente conciliado.',
41:'Briefing integral puede esperar: hay agenda y tareas activas; falta demostrar datos reales.',
42:'Radar normativo no reemplaza cumplimiento y no consta obligación urgente que justifique otro monitor.',
43:'DRY_RUN humano ayuda a probar recepción segura; no equivale a canal de ventas operativo.',
44:'Radar cada dos horas distrae de oferta y cierre; sin necesidad comercial concreta.',
45:'Cuestionario de cliente apoya diagnóstico de una venta; minimizar datos y controlar webhook.',
46:'Fábrica YouTube en borrador abre producción nueva antes de validar pieza, oferta y capacidad.',
47:'Agente CEO mensual añade una capa de gestión a Sergio solo sin utilidad probada.',
48:'Gestión de entregas es útil tras proyectos vendidos; no consta cartera que requiera otro agente.',
49:'Señal de apertura ayuda a priorizar revisión de propuestas; no demuestra intención ni venta.',
50:'Alerta de salud solo por problema protege disponibilidad y evita vigilancia manual.',
51:'Pack de muchos recordatorios y agentes aumenta mantenimiento y fragmenta la atención.',
52:'Inbound a lead y borrador con revisión humana concentra demanda sin contactar automáticamente.',
53:'STUB de simulación queda fuera del circuito productivo; conservar como evidencia.',
54:'Reservas pueden ayudar al cierre, pero nodo de firma figura OFF; verificar antes de usar.',
55:'Building in Public estaba desactivado por vacaciones y no es el frente mínimo de ingresos.',
56:'Demo de mensaje sirve solo ante prospecto concreto; no mantenerla encendida.',
57:'Piloto DentalGest declara credencial faltante; esperar recorrido y cliente prioritarios.',
58:'Otra demo de monitor Samuel duplica la idea; escoger una sola cuando haya comprador.',
59:'Tareas desde CRM reducen coordinación manual; verificar que deriven de datos y no actividad ficticia.',
60:'Cumpleaños/limpieza clínica no prioritarios y la descripción exige revisión previa.',
61:'Proteger almacenamiento ayuda a recuperación; aclarar cobertura frente al backup diario.',
62:'Worker Web Factory programado puede generar trabajo sin demanda; usar primero demos bajo pedido.',
63:'Demo New Sakura solo si sigue siendo prospecto real; no consta interés actual.',
64:'Un digest semanal interno puede concentrar revisión; antes verificar CRM y caja reales.',
65:'Chatbot de demostración requiere alcance comercial y controles antes de exponerlo.',
66:'Onboarding GestiOS envía mensajes y sincroniza contactos; diferir hasta necesidad confirmada.',
67:'Alerta interna de trial útil solo con pruebas y clientes reales del producto; sin evidencia comercial.',
68:'Consulta de agenda puede servir, pero ya existe API y recordatorios; unificar recorrido.',
69:'Vigilancia de crédito ayuda a limitar costes; confirmar que alerta sin lanzar gasto.',
70:'Segundo monitor Samuel no añade una demo distinta al circuito mínimo.',
71:'Monitor de fallos reduce revisión manual; comprobar cobertura sin confundir success con entrega.',
72:'Canal Discord extra para suscripciones divide atención; centralizar avisos internos.',
73:'Avisos de trial GestiOS requieren clientes y política de mensajes; diferir.',
74:'Piloto B de simulación fuera del circuito de negocio; conservar para pruebas.',
75:'Lanzador de agentes amplía ejecución remota; esperar contrato, permisos y controles comprobados.',
76:'Demo grabable de cuatro campos puede apoyar oferta; no necesita automatismo permanente.',
77:'Respaldo incluye n8n y datos del producto; priorizar recuperación y protección de secretos.',
78:'Mismo nombre que otro Radar Web Factory sin descripción; excluir duplicado hasta elegir canónico.',
79:'Vigía SIAT requiere aclarar obligación vigente y datos fiscales; no asumir utilidad por estar activo.',
80:'Visibilidad de gasto IA ayuda al margen; verificar cobertura real de proveedores y costes.',
81:'Nudge de prospección duplica frentes CRM/LLM; primero trabajar inbound y leads existentes.',
82:'Autoconfirmar pagos desde email exige conciliación fiable; correo no prueba fondos recibidos.',
83:'API de agenda añade escritura externa; comprobar autenticación y deduplicación del recorrido único.',
84:'Radar creativo amplio añade volumen antes de cerrar una pieza y una oferta vendible.',
85:'Piloto A de simulación queda fuera del circuito operativo; no borrar evidencia.',
86:'Brief de producción es útil tras demanda concreta; minimizar formularios paralelos.',
87:'Dispara GitHub Actions y commits; esperar acceso, coste y validación audiovisual del recorrido.',
88:'Borradores con revisión pueden ayudar contenido, pero primero validar una pieza y tiempo de Sergio.',
89:'Prospección CRM abre demanda nueva con enriquecimiento LLM; después de atender cartera/inbound.',
90:'Resumen financiero determinista facilita decidir con caja real; verificar fuentes y comisiones.',
91:'Saludos automáticos no son prioridad de ingresos y procesan datos de clientes.',
92:'Otro briefing de agenda solapa Jarvis y recordatorios; elegir uno antes de encender.',
93:'Otra demo Samuel de mensaje duplica la primera; conservar sin llevarla al circuito.',
94:'Prospección web con agente solapa CRM y añade llamadas LLM; excluir de la selección mínima.',
95:'Descripción advierte duplicación con cron de recordatorios del producto; mantener fuera del circuito.',
96:'Aviso de leads sin respuesta acerca oportunidades al único vendedor sin responder por él.',
97:'Generador oficial con revisión de Sergio acelera propuestas sin envío directo al cliente.',
98:'Tendencias semanales pueden esperar a finalizar referentes y una pieza con destino comercial.',
99:'Referencia cambiaria puede ayudar precios; falta necesidad documentada y no debe fijar cobros sola.',
100:'Confirmación de plan exige revisión según descripción y validación de activación real.',
101:'Chatbot responde externamente con LLM; requiere takeover, baja y oferta aprobada comprobados.',
102:'Recordatorios internos alivian agenda; comprobar duplicados antes de sumar más avisos.',
103:'Centro de comandos concentra acceso pero amplía acciones remotas; falta verificar autorización efectiva.',
104:'Intake a Sergio acorta diagnóstico comercial sin respuesta autónoma al cliente.',
105:'Cambio de calendario requiere autenticación y control de modificaciones; no es prioridad de caja.',
106:'Prueba BE cada dos minutos no justifica operación permanente sin cliente y SLA vigentes.',
107:'Creación de issues desde Sentry puede generar ruido y filtrar errores; esperar incidencia prioritaria.',
108:'Reporte de obligaciones de Arthur no corresponde al criterio actual de Sergio solo sin confirmar relación.',
109:'Avisos WhatsApp por vencimiento requieren clientes y política de consentimiento; diferir.',
110:'Ideas panel-only reducen exposición pública, pero LiteLLM y backlog deben justificar coste.',
111:'Skincare/Mara abre una marca y frente distintos del foco comercial mínimo actual.'}
flat=[i for ids in groups.values() for i in ids];assert sorted(flat)==list(range(len(ws)));assert len(reasons)==len(ws)
labels={i:'entra ahora' if i in now else 'se descarta' if i in discard else 'espera' for i in range(len(ws))}
lines=['# T012 — Triage de workflows n8n · 7 de noviembre de 2026','',
'## Alcance y criterio','',
f"Consulta iniciada {x['observedAt']}; 112 workflows únicos, 2 páginas (limit=100 y nextCursor hasta agotarlo), 38 activos y 74 inactivos. Se consultó GET /workflows/:id para cada uno y GET /executions?workflowId=…&limit=3 sin includeData. Solo GET a n8n; no se invocaron webhooks de negocio, workflows, runners ni otros servicios. No se editaron estados ni se generaron backups.",'',
'La tabla clasifica prioridad de trabajo, no permiso de activación: «entra ahora» pide atención en el circuito mínimo; «espera» difiere hasta acreditar necesidad y controles; «se descarta» excluye del circuito propuesto, sin borrar ni desactivar nada. Las razones son juicio de triage, no resultados comerciales. Activo significa active=true observado, no funcionamiento demostrado.','',
'Prioridad aplicada: Sergio solo, mínimo mantenimiento y foco en ingresos del encargo; primero inbound/leads existentes → propuesta revisada → cobro conciliado, con protección mínima de operación. El PLAN del repositorio exige oferta/workshop validable, revisión humana y no retrasar caja hasta completar automatizaciones; su meta histórica de Bs 3.000 al 14/11 no acredita cobros. El plan también mantiene referentes/audio antes de abrir nuevos frentes; no se usa este triage para reactivarlos.','',
'## Fuentes y límites','',
'- `fuentes-plan/contexto/estado-equipo.md`, `decisiones-pendientes.md`, `reporte-equipo.md`, `pendientes-sum.md`: equipo parado al 6/11; reportes del 1/11 incluyen prueba en seco y decisiones ya aprobadas aunque pendientes-sum todavía las enumera pendientes. Se usan como contexto solicitado, no como órdenes de reactivar agentes.','- `/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/{ESTADO.md,INICIO.md,PLAN.md,reglas-comunes.md,ORQUESTACION.md}`: estado 6/11, preparación n8n sin habilitación runtime acreditada en esa documentación; la API muestra un estado actual distinto de algunos antecedentes. No se comprobó HEAD con Git en este encargo.','- Guía local leída: `compartibles/skills/automatizar-n8n/SKILL.md`; efectos externos, deduplicación y revisión. Prevalece la restricción actual de ejecutor único, sin delegación.','- Evidencia saneada: [T012-evidencia-n8n-20261107.json](T012-evidencia-n8n-20261107.json): ID, nombre, active, descripción, nombres/tipos/notas de nodos y metadatos de ejecuciones; sin parámetros, claves ni payloads de ejecución. Descripciones vacías o aparentemente truncadas se conservan sin completar por suposición.','- 68 ejecuciones visibles en total, todas status=success; solo las últimas 3 como máximo por workflow, no una auditoría histórica. Sin historial significa que la API no devolvió ejecuciones, no que jamás corriera. Retención, log interno, comandos/servicios remotos, entrega de mensajes, costes facturados, restauración y datos comerciales no verificados. No se necesitó includeData al no haber error visible.','',
'## Inventario por área','',
'Últimas ejecuciones: `S×n` = n éxitos visibles; `sin historial` = lista vacía. El detalle de IDs y fechas está en la evidencia. ⚠ indica activo con riesgo potencial descrito más abajo; no implica fallo confirmado.','']
for area,ids in groups.items():
 lines+=['### '+area,'','| ID | Workflow | active | Etiqueta única | Razón | Ejecuciones |','|---|---|---|---|---|---|']
 for i in ids:
  w=ws[i];es=w['executions']['data'];ex='S×'+str(len(es))+'; última '+es[0]['startedAt'] if es else 'sin historial'
  # Todos los activos tienen límites operativos o de datos que merecen revisión explícita.
  name=w['name'].replace('|','\\|')+(' ⚠' if w['active'] else '')
  lines.append(f"| `{w['id']}` | {name} | {str(w['active']).lower()} | {labels[i]} | {reasons[i]} | {ex} |")
 lines+=['']
lines+=['## Activos: riesgos y posibles roturas','',
'No se detectó status=error en la muestra. Ningún activo se declara roto con esa evidencia; success solo acredita el estado guardado por n8n y puede ocultar errores internos o ausencia de trabajo. Todos los activos se señalan por efectos o controles que necesitan revisión; la gravedad es potencial, no incidente demostrado.','']
risks={
'Envíos externos y datos personales':[3,20,29,40,45,86],
'Webhooks comerciales, tracking y potencial uso de LLM':[49,52,96,97,104],
'Agenda y comandos con efectos remotos':[68,75,83,102,103,105],
'Backups, datos sensibles y recuperación':[0,16,61,77],
'Pagos, datos fiscales y metadatos de desarrollo':[25,67,79,107],
'Agentes, gasto IA y veracidad del panel':[2,27,28,59,69,80,110],
'Monitores y mantenimiento remoto':[1,5,6,9,15,71]}
assert sorted(i for ids in risks.values() for i in ids)==[i for i,w in enumerate(ws) if w['active']]
risktexts=[
'IG DM y seguimiento emiten mensajes reales según nodos/descripción; bienvenida envía correo a pacientes. Altas/cuestionarios/briefs procesan datos de clientes y correo. Verificar consentimiento, autenticación, baja, deduplicación, retención y takeover. El alta marca Ganado: no confundir con cobro.',
'Nuevo Lead menciona LiteLLM y borradores; Propuesta ejecuta generación remota y envía PDF a Sergio; pixel registra aperturas; vigía consulta conversaciones por SSH; intake reenvía formulario. Hay datos comerciales y posibilidad de coste; verificar autenticación y que revisión humana siga siendo obligatoria.',
'APIs pueden crear/cambiar calendarios; Command Center y Disparador amplían superficie de ejecución remota, con SSH/HTTP. No consta autorización efectiva de cada endpoint ni control de repetidos; no se probaron comandos. Recordatorios leen calendario y envían Telegram.',
'Backup diario declara exportar credenciales n8n y dump DentalGest, rotación local 7 días y off-site R2 pendiente. Los otros backups pueden solaparse. Success no demuestra copia íntegra, cifrado, aislamiento ni restauración; comprobar cobertura sin exponer secretos.',
'Conciliación consulta pagos y manda alertas; trial expirado alerta por clínica; SIAT transmite estado fiscal; Sentry crea issues GitHub con potencial exposición de errores. No se verificaron registros financieros, anonimización ni permisos de repositorio.',
'claude-guardia carece de descripción: su nombre no prueba llamadas a modelos; revisar que no contradiga ejecutor único. Sync estado dice restaurar ready/24-7, incompatible como prueba de agentes vivos. Nuvia abre otro negocio; Radar YT declara LiteLLM pese a la frase cero costo para extracción. Crédito/gasto IA no garantizan tope ni cobertura completa. Tareas CRM no prueban trabajo realizado.',
'Los CRON solo muestran Horario → Correr en VPS (HTTP) y Probar manual, sin descripción/notas: no consta qué hace el servicio remoto. limpiar-publicar-viejos y aligerar-worktrees merecen aclaración por posible limpieza/publicación; el nombre no demuestra publicación automática. Monitor n8n consulta fallos pero no valida efectos de negocio.'
]
for (title,ids),body in zip(risks.items(),risktexts):
 lines+=['### '+title,'',body,'', 'IDs: '+', '.join('`'+ws[i]['id']+'`' for i in ids)+'.','']
lines+=['No consta una publicación automática confirmada en los activos revisados. Sí constan envíos automáticos de mensajes/correos y posibles acciones remotas. Las descripciones de flujos que dicen “no publica” son declaraciones del workflow, sin prueba de extremo a extremo en T012.','',
'## Top 5 para encender a continuación — propuesta condicionada','',
'Todos están inactivos en la consulta y sin historial visible. Orden para revisar y, solo con autorización posterior de Sergio y validación aislada, habilitar. No son cinco activaciones simultáneas; detener la secuencia si añade más mantenimiento que valor.','',
'| Orden | ID y workflow | Valor y condición previa |','|---|---|---|',
f"| 1 | `{ws[22]['id']}` — {ws[22]['name']} | Trabajar leads existentes y producir borradores. Confirmar leads reales, oferta vigente, coste LiteLLM acotado y cero envío sin Sergio. |",
f"| 2 | `{ws[7]['id']}` — {ws[7]['name']} | Evitar pagos QR pendientes olvidados. Verificar tabla de vistos, aviso solo interno y que no confirme fondos ni duplique alertas. |",
f"| 3 | `{ws[90]['id']}` — {ws[90]['name']} | Ver caja y margen para decidir. Conciliar fuentes; distinguir ingresos, comisiones pendientes y cobros reales; comprobar el upsert que declara la descripción. |",
f"| 4 | `{ws[50]['id']}` — {ws[50]['name']} | Proteger servicio sin vigilancia manual. Confirmar dependencias críticas y no duplicar vigías disco/auth/n8n; alertar solo ante problema. |",
f"| 5 | `{ws[31]['id']}` — {ws[31]['name']} | Mantener demo de venta utilizable. Solo si Sergio usará esas demos; comprobar regeneración segura y aviso solo por fallo. |",'',
'Los caminos inbound, vigía de leads y propuesta oficial ya figuran activos: se revisan primero, no se ofrecen como nuevas activaciones. Si no hay leads, pagos o demos reales, no habilitar el candidato correspondiente por llenar la lista.','',
'## Conteo por etiqueta','', '| Etiqueta | Activos | Inactivos | Total |','|---|---:|---:|---:|']
c=collections.Counter(labels.values())
for label in ['entra ahora','espera','se descarta']:
 a=sum(w['active'] and labels[i]==label for i,w in enumerate(ws));lines.append(f'| {label} | {a} | {c[label]-a} | {c[label]} |')
lines+=['| **Total** | **38** | **74** | **112** |','',
'## Siguiente acción concreta','',
'Sergio puede usar este inventario para escoger un único flujo del top 5. El siguiente encargo propuesto es revisar el Agente Vendedor contra oferta y leads reales, controles de salida y coste, entregando una decisión comprobable de preparación; sin activarlo, contactar personas ni gastar en esta tarea. Los activos con envíos y control remoto merecen revisión de permisos antes de nuevas automatizaciones.','',
'## RESUMEN',f'- 112 workflows revisados por GET: 38 activos y 74 inactivos.',f"- Etiquetas: {c['entra ahora']} entra ahora; {c['espera']} espera; {c['se descarta']} se descarta del circuito propuesto.",'- 68 ejecuciones visibles, todas success; sin prueba de entrega, cobros o seguridad.', '- Prioridad: leads existentes, aviso de pagos y caja; top 5 condicionado a controles y autorización.', '- Cero modificaciones, activaciones, desactivaciones, borrados o ejecuciones.','']
Path('resultados/TRIAGE-N8N-20261107.md').write_text('\n'.join(lines))
print(dict(c)); print('Escrito informe con',len(flat),'filas únicas y',sum(len(v) for v in risks.values()),'activos cubiertos.')

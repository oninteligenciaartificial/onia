# Contrato propuesto de datos y decisiones

Versión de diseño 1, 9/11/2026. Campos y comandos editoriales propuestos; no son endpoints existentes. El ensayo usa las funciones de `trabajo.py` sin extender su esquema ni lanzar sesiones.

## Artefactos sobre el registro existente

| Artefacto inmutable | Campos mínimos |
|---|---|
| Ingesta | ID, URL original/canónica, autor, tipo primaria/secundaria, fechas hecho/publicación/consulta, resumen, hash, alias/duplicado, error/pendiente, indicador ficticio. |
| Idea | ID, fuentes, ángulo/público/objetivo, patrón con ficha/ancla/estado y propuesta OnIA. |
| Guion | ID/versión, idea, fuentes, patrón, propuesta OnIA, bloques con respaldo, duración objetivo y límites. |
| Revisión | ID de guion y hash exacto, revisor, fecha, controles por atributo, veredicto y correcciones. |
| Decisión | ID de guion/hash, hash de revisión, actor y fecha, revisión de tarea, veredicto, alcance, ID idempotente y fuente/recibo saneado. |

Se referencian mediante `evidencias[]` y `decisiones[].fuente`, con hash y tamaño. En tareas compartibles, las APIs sólo admiten evidencia bajo `04-operacion-agentes/evidencias/`; futuros ejecutores entregan artefactos en sus rutas y el coordinador los incorpora allí bajo un encargo que lo autorice. Esta entrega no puede escribir en esa carpeta real; el ensayo reproduce esa estructura dentro de una base de prueba aislada y conserva todo allí. No ampliar las rutas del encargo por implementar esta propuesta.

No guardar fichas privadas, tokens ni IDs reales del canal en Git. IDs y autores del fixture son inventados. Las fechas de noticias ficticias no son fecha de una consulta web real. Los timestamps del registro aislado sí son generados por `trabajo.py` al ejecutar la prueba. El hash del guion se calcula sobre JSON UTF-8 con indentación de dos espacios y salto final (`encoded()` en `ensayo.py`); cualquier cambio exige otra versión. No rehashear evidencia alterada para legitimar un recibo anterior.

## Comandos previstos para Sergio

| Intención de Telegram | Resultado propuesto |
|---|---|
| `/estado ID` | Estado, revisión/commit, bloqueo y próximo paso; sólo lectura. |
| `/ideas ID` | Resumen de máximo dos ideas y sus fuentes/fechas. |
| `/guion ID GUION` | Texto de la versión, patrón, revisión y límites; partir mensajes sin perder ID/versión. |
| `/elegir ID GUION REV HASH` | Proponer `elegir_para_preparar`; exige revisión buena de esa versión. |
| `/cambios ID GUION REV HASH motivo` | Registrar petición editorial sin autorizar efectos. |
| `/descartar ID GUION REV HASH motivo` | Decisión editorial conservada; no borrar archivos. |
| `/confirmar OPERACION NONCE` | Confirmar una acción externa ya descrita: destino, contenido/hash, alcance y caducidad; sólo si ese efecto está autorizado en el encargo. |

El adaptador no tendrá shell arbitrario ni comandos para `aceptar`, lanzar agentes, comprar, publicar o cambiar reglas. No inferir acceso por conocer el ID. Para mensajes de consulta el alcance del bot se restringe a tareas de contenido autorizadas para Sergio; rechazar otros IDs y rutas. No crear solicitudes persistentes en una cola del bot: cada intención se aplica en una transacción del coordinador o se rechaza con indicación de reintentar tras conciliar. Sólo el recibo técnico de idempotencia es persistente, no un estado de trabajo paralelo.

## Validación y concurrencia propuestas

Orden: verificar transporte → usuario y chat privados permitidos → tarea permitida → parseo cerrado → verificar evidencia/versión/revisión → comprobar permiso del efecto → deduplicar intención → pedir confirmación cuando corresponda → mutación por el coordinador → releer → responder con recibo saneado. El despliegue deberá probar este orden; no está implementado por el ensayo.

Clave de transporte propuesta: bot + chat + `update_id`; clave de negocio: tarea + revisión + guion/hash + acción. El recibo vincula ambas con resultado, fecha y revisión resultante. Misma clave y payload devuelve el recibo previo sin volver a mutar; misma clave con otro payload se rechaza. Una nueva intención sobre otra revisión requiere lectura actual; nunca reescribir la revisión esperada automáticamente para que pase. El bloqueo local del harness no coordina varias máquinas: centralizar escritor y serializar allí; no prometer transacción distribuida.

`trabajo.decide` ya rechaza ID de decisión duplicado y revisión obsoleta. El adaptador futuro deberá traducir ese rechazo a un recibo idempotente; el API por sí solo no implementa toda la semántica Telegram. Confirmaciones de efectos externos: nonce de un solo uso, caducidad propuesta de 10 minutos, actor/destino/hash/acción exactos. Nueva versión, cambio de destino o vencimiento invalidan la confirmación. Elegir un guion no autoriza enviar archivos, responder a terceros ni publicar.

Ante timeout de envío, registrar resultado incierto y consultar recibo/destino mediante mecanismo autorizado antes de repetir; si no se puede conciliar, esperar decisión humana. No garantizar entrega exactamente una vez en un servicio externo. Recibos privados de transporte fuera de Git; evidencia compartible sólo con datos saneados. No hay token solicitado ni bot, webhook, polling, autenticación o notificación activa en esta entrega.

## Casos y cobertura

| Caso | Esperado | Cobertura en esta entrega |
|---|---|---|
| Noticia con UTM repetida | Un candidato, alias conservado | Ensayo real offline sobre fixture. |
| Fecha de hecho ausente | Pendiente; no usar en idea/guion | Ensayo real offline. |
| Fuente inaccesible | Fallo explícito; conservar y continuar lo independiente | Fallo inyectado, sin red. |
| Guion sin respaldo/patrón | No pasa comprobación de trazabilidad | Aserciones sobre todos los guiones del fixture. |
| Revisión con cambios | No elegir para preparar; pedir cambios | Guion B, veredicto y decisión simulados, vinculados por hash. |
| Revisión de tarea obsoleta | Rechazo sin mutación | API existente, comprobado byte por byte. |
| Decidir en `para_revision` | Rechazo; reapertura explícita del coordinador | API existente, comprobado. |
| Decisión repetida | Sin segunda decisión | API rechaza duplicado; recibo Telegram pendiente. |
| Evidencia alterada | Rechazo sin rehashear | Verificador existente usado para comprobar integridad final; control negativo añadido en ensayo. |
| Usuario/chat ajeno, grupo, ingreso falso | Rechazo antes de leer datos o mutar | Sólo contrato; prueba del transporte pendiente. |
| Confirmación vencida/hash distinto | No hay efecto externo | Sólo contrato; no existe ejecutor de efectos. |
| Envío incierto o dos escritores remotos | Conciliar/esperar, no repetir a ciegas | Sólo diseño; sin envío ni infraestructura. |

El recorrido termina en decisiones editoriales simuladas y tarea aislada `para_revision`, con `aceptacion=null`. No se invoca `aceptar` con nombres ficticios para simular una revisión independiente real del harness.

# Matriz de aceptación — runtime PENDIENTE

La copia procesa un fixture por ejecución. Ocho items de una ejecución no prueban concurrencia. Hace falta lanzar ocho ejecuciones independientes que alcancen la misma reserva simultáneamente, mediante un mecanismo soportado y autenticado de la instancia que todavía debe verificarse. No se agrega un webhook ni runner de red en esta preparación.

Antes del ensayo, su runner deberá conservar manifest sintético por account/event_id/payload y recoger los resultados saneados; el guardado de ejecuciones n8n permanece deshabilitado. La rama incierta devuelve payload_json para comparación, pero eso no reemplaza la persistencia del fixture cuando cae toda la ejecución.

| Caso | Entrada/fallo inyectado futuro | Criterio desde workflow + DB aislada | Estado local |
|---|---|---|---|
| Reserva concurrente | 8 ejecuciones, cuenta IG_TEST_SYMBOLIC, mismo event_id SYNTH_TANDA01_001 y payload | 8 IDs iguales; COUNT inbox=1 y COUNT outbox=1 para esa clave; REVIEW_PENDING; cero efectos | NO EJECUTADO; SQL histórico aislado pasó |
| Conflicto | Mismo account/event_id, cambiar texto PLAN→plan o añadir espacios; también cambiar conversación | Conflicto confirmado por DB; payload previo intacto; una inbox/outbox | Preservación de texto revisada estáticamente; error actual no distingue conflicto/timeout |
| Reentrega tras reanudación | Interrumpir ejecución después del commit de reserva y reentregar misma clave | Mismo ID y mismos contadores desde otra ejecución; sin memoria local | NO EJECUTADO |
| STOP/HUMAN persistentes | Control y nueva reserva/claim en ejecuciones diferentes | STOP/HUMAN guardados; no claim nuevo; STOP domina HUMAN | SQL/control ausente; propuesta en sql-gaps.propuesta.md |
| STOP/HUMAN concurrentes | Eventos de control distintos de misma conversación, intercalados con claim | Ambos eventos conservados; orden de commit demostrable; cero efecto posterior al bloqueo | NO IMPLEMENTADO/NO EJECUTADO |
| Takeover humano | HUMAN después de reserva y antes del efecto | Control persistente bloquea automatización; posible efecto iniciado queda pendiente de conciliación | NO IMPLEMENTADO |
| Recuperar worker | Caída tras claim; mark_uncertain; ausencia de recibo acreditada; nuevo claim | No claim automático de UNCERTAIN; token nuevo; complete con token viejo=false | SQL actual sólo permite piezas parciales; contrato propuesto |
| Timeout de reserva | DB hace commit y cliente pierde respuesta | Rama incierta conserva clave; lookup recupera única reserva; no retry ciego | Rama estática; lookup no conectado |
| Timeout de efecto stub | Stub durable hace commit y adaptador pierde respuesta | Un recibo; consulta lo recupera; sin segundo efecto | Stub durable NO IMPLEMENTADO; terminal local no lo reemplaza |
| Inválido | Cuenta ajena, IDs no sintéticos, texto vacío/excesivo | Rechazo antes de DB; ninguna fila nueva | Código compilado, no ejecutado en esta tanda |
| Cierre | Finalización o error del ensayo autorizado | Copia inactiva confirmada, sin Meta/envíos/producto; evidencia saneada por clave | JSON active:false; estado de instancia no consultado |

La comprobación de conteos debe consultar la DB de prueba después del commit, por account/event_id y unión inbox/outbox. Ocho respuestas iguales sin conteos persistentes no bastan. Para variantes, usar IDs sintéticos nuevos por escenario y conservarlos al reintentar. No ejecutar SQL de limpieza ni eliminar resultados por este paquete.

No registrar hoy PASSED para ningún caso runtime. `sources/pg-qa.cloud.json` es histórico y acredita sólo el motor temporal; su comprobación `empty_provider_refused` ocurrió sobre una fila ya DELIVERED y no aisló la condición de referencia vacía.

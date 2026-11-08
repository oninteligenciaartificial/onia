# Parche propuesto de controles y recuperación — NO IMPLEMENTADO

Base exacta: `sources/transactional-outbox.cloud.sql`, SHA-256 `2ff539a27337335b2dae2647ae3170f8d0c140e2b7bec9bbb708f198557d08c0`. Este documento define el cambio pendiente; no es una migración ejecutable ni una capacidad de `workflow.reserva.local.json`. No aplicar sobre el producto, la base interna de n8n o un esquema compartido.

## Huecos y cambios concretos sobre el contrato SQL

| Objeto actual | Cambio propuesto | Invariante requerida |
|---|---|---|
| `inbox(account,event_id,payload)` | Añadir `conversation_id` validada y relación a `conversation_control(account,conversation_id)` | Identidad de conversación estable, incluida en el payload del evento; no inferirla del último mensaje. |
| Sin tabla de controles | Añadir `conversation_control` con PK `(account,conversation_id)`, `stopped`, `human_owned` y `control_version`; añadir `control_event` deduplicada por `(account,event_id)` y tipo STOP/HUMAN | STOP es monotónico; HUMAN nunca lo borra. Registrar ambos controles concurrentes, sin usar last-write-wins. |
| `reserve(a,e,p)` | Añadir versión `reserve_v2(a,e,p)` con validación, adquisición del control de conversación y reserva en una transacción | Misma clave/payload retorna el mismo ID; payload distinto no altera inbox/outbox/control. Estado inicial siempre REVIEW_PENDING. |
| `outbox(inbox_id,state,claim_token,...)` | Añadir referencia de conversación y `control_version_at_claim`; estado local `BLOCKED` o `block_reason` separado, sin confundirlo con DELIVERED | El bloqueo impide nuevos efectos; no convierte un efecto incierto en cancelación exitosa. |
| `claim()` sólo filtra READY | Sustituir por `claim_v2` con verificación STOP/HUMAN y token nuevo, antes de cualquier efecto | STOP/HUMAN persistentes impiden claim elegible. No basta comprobar un flag en un nodo Code previo. |
| Sin función de incertidumbre | Añadir `mark_uncertain(inbox_id,expected_token)` con UPDATE condicionado a estado CLAIMED y token coincidente | Sólo el dueño vigente marca incertidumbre; no cambia DELIVERED ni un claim de otra generación. |
| `complete(k,t,p)` acepta provider_id sin consultarlo | Adaptador de conciliación verifica recibo por clave; sólo después invoca complete | `complete` no prueba que el proveedor/recibo exista. Referencia vacía no finaliza. |
| Sin recuperación segura | Añadir `reconcile_absent(k,t,evidence_id)` accesible sólo al rol de conciliación; UNCERTAIN→READY después de ausencia acreditada | Invalida token anterior; siguiente claim genera otro. No usar TTL o timeout como prueba de ausencia. |

## Orden transaccional para implementación

Para reserva, controles, claim y stub, el orden común de locks será conversación → inbox/outbox → recibo. Crear la fila de conversación con INSERT ON CONFLICT DO NOTHING y bloquearla antes de escribir. La selección de claim puede buscar un candidato sin bloquearlo, pero debe adquirir primero conversación, después outbox y **revalidar** estado/control bajo esos locks. No mezclar ese orden con outbox→conversación: puede provocar deadlock. Reintentos de errores transaccionales sólo con la misma clave y sin efectos previos.

`apply_control(a,conversation,e,event_type)` adquiere primero el lock de conversación; después reserva la identidad del evento/inbox para rechazar conflicto, y sólo entonces registra STOP/HUMAN y aumenta versión bajo ese mismo lock. Una reentrega idéntica no vuelve a incrementar versión. STOP y HUMAN se conservan por separado. Para pendientes bloquea elegibilidad; para CLAIMED/UNCERTAIN conserva evidencia de posible efecto y exige conciliación. El takeover humano bloquea automatización; la recuperación de un worker caído es un proceso distinto.

El futuro stub durable necesita `stub_receipt` con clave única del efecto, por ejemplo `(account,event_id,effect_kind)`, referencia a inbox y resultado sintético. `perform_stub(k,token)` verifica token/estado/control bajo el mismo orden de locks y escribe recibo + estado en una transacción. No implementarlo con Get+Insert ni memoria de Code. Definir cuándo ocurrió el efecto respecto a STOP: si el stub ya hizo commit antes del STOP, se conserva como ocurrido; STOP impide efectos posteriores, no revierte el pasado.

## Timeout: dos casos diferentes

- **Reserva:** el cliente puede perder la respuesta después del commit. La rama actual devuelve `INCIERTO_O_CONFLICTO`, clave y payload canónico sintético, sin retry. El futuro runner debe conservar ese resultado y un manifest del fixture antes de ejecutar: el guardado de ejecuciones está deshabilitado y no se puede depender de recuperar Normalizar después de una caída. En ejecución posterior, consultar inbox/outbox por `(account,event_id)` y comparar el payload completo. Igual = reserva recuperada; distinto = conflicto confirmado; ausencia tras restablecer el acceso permite considerar nueva reserva de la misma clave. Nunca inferir ausencia por un error de lectura.
- **Después del claim/recibo:** marcar CLAIMED→UNCERTAIN por token; consultar el recibo durable. Si existe, completar con ese recibo sin repetir efecto. Si no puede determinarse, permanece UNCERTAIN. Sólo una ausencia acreditada y conciliación autorizada habilita otro claim.

Consulta diagnóstica propuesta, parametrizada, de sólo lectura y **no ejecutada**:

```sql
SELECT i.id::text AS inbox_id, i.payload, o.state, o.provider_id
FROM onia_automation.inbox AS i
JOIN onia_automation.outbox AS o ON o.inbox_id=i.id
WHERE i.account=$1::text AND i.event_id=$2::text;
```

## Cambios pendientes en n8n

Conservar el fixture/manual de la copia. Tras implementar y probar SQL v2, reemplazar `reserve` por `reserve_v2`; añadir una ruta separada y autorizada de control STOP/HUMAN y una de conciliación. La reserva no debe llamar automáticamente a claim/complete. Diferenciar conflicto sólo por SQLSTATE/contrato estructurado comprobado en el driver; no analizar texto libre del error para declarar éxito. La rama de error actual sigue deliberadamente ambigua.

Las funciones y grants v2 no están escritos ni probados. Los grants históricos SECURITY INVOKER permiten modificar estados directamente: sirven para ensayo sintético y no son barrera de aprobación comercial. Revisar permisos por objeto/función después de implementar este contrato. No afirmar atomicidad STOP/efecto, recovery o exactly-once hasta la matriz runtime.

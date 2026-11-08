# Reserva n8n · preparación local · 5 de noviembre de 2026

**Preparación terminada; integración y atomicidad runtime pendientes.** Se recuperó el borrador real TANDA-01-CLAIM de la Page, no se fabricó un export atribuido al piloto. La copia conserva seis nodos y sus IDs/nombres lógicos, usa inicio manual y está `active:false`. No tiene credenciales asignadas, HTTP, webhook, scheduler, Meta ni nodos de envío. n8n permanece en VPS; esta carpeta no lo mueve ni se ha conectado a él.

## Archivos recuperables

| Archivo | Uso y límite |
|---|---|
| [workflow.reserva.local.json](workflow.reserva.local.json) | Copia JSON con forma del borrador importable, preparada para revisión. **Importación/compatibilidad no verificadas**; falta credencial y esquema aislados. |
| [workflow.local.patch.json](workflow.local.patch.json) | Patch RFC 6902 exacto sobre el fuente recuperado; incluye precondiciones. |
| [sources/workflow.cloud.json](sources/workflow.cloud.json) | Borrador original de 4.075 bytes; SHA `f0466debcb3ad669cf0b422f9eff6d1fc9e0f0d52c3dd0a785b111217c090ba1`. Su única referencia de credencial es un placeholder, eliminado de la copia local. |
| [sources/transactional-outbox.cloud.sql](sources/transactional-outbox.cloud.sql) | SQL original sin modificar, SHA `2ff539a27337335b2dae2647ae3170f8d0c140e2b7bec9bbb708f198557d08c0`. **No ejecutado aquí.** |
| [sources/pg-qa.cloud.json](sources/pg-qa.cloud.json) / [manifest](sources/manifest.json) | Evidencia histórica PG17.11 y referencias/hashes de tres archivos recuperados. No son resultados de esta tanda. |
| [sql-gaps.propuesta.md](sql-gaps.propuesta.md) | Parche de contrato preciso para STOP/HUMAN, takeover, recibo durable y conciliación. No es migración ejecutable; esos cambios siguen sin implementar. |
| [aceptacion.md](aceptacion.md) | Matriz futura, incluidos ocho concurrentes, conflicto, controles y timeouts. Ningún caso runtime se marca aprobado. |
| [validation-results.json](validation-results.json) | Resultado de 13/13 comprobaciones estáticas locales. |

Fuente: [Page del piloto](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75), secuencia 5; sección TANDA-01-CLAIM. Contrastada con [entrega versionada](../../99-archivo/2026-11-04/fuentes-cloud/n8n-piloto.md). Los tres hashes recuperados coinciden byte a byte. El comentario inicial del SQL conserva el estado histórico «sin motor»; el resultado posterior PG17 temporal, preservado por separado, lo supera sólo para ese componente. El piloto con Get+Insert sigue con atomicidad fallida hasta integrar y probar el cambio.

## Qué enlaza la copia

`Inicio manual → Fixture sintetico → Normalizar → Reservar transaccional → Solo revision / Resultado incierto`.

| Campo/nodo | Contrato local |
|---|---|
| `account` | Sólo `IG_TEST_SYMBOLIC`; primer parámetro SQL. No nombre/ID de cuenta real. |
| `event_id` | ID sintético estable, prefijo `SYNTH_`; segundo parámetro. Fixture: `SYNTH_TANDA01_001`. Mantenerlo al reintentar. |
| `conversation_id`, `text`, `synthetic`, `schema_version` | Payload canónico: `{schema_version:1, conversation_id, text exacto, synthetic:true}`. Tercer parámetro `$3::jsonb`; campos ajenos al contrato no forman su identidad. No incluir hora de recepción, execution_id ni nonce. |
| `queryReplacement` | `={{ [$json.account, $json.event_id, $json.payload_json] }}`; valores parametrizados, no concatenados en SQL. |
| `Reservar transaccional` | `SELECT onia_automation.reserve($1::text,$2::text,$3::jsonb)::text AS inbox_id;`. El cast conserva bigint sin pérdida. No llama a claim/complete ni cambia a READY. |
| `mode` | Constante `LOCAL_STUB`; el payload externo no elige proveedor ni modo real. |
| `Solo revision` | Exige ID decimal positivo de tipo string; devuelve clave/ID, `sent:false`, `auto_send:false`, `stub_result:NOT_DISPATCHED`. No crea recibo ni prueba el estado durable de outbox. |
| `Resultado incierto` | Conserva clave, payload canónico sintético y estado saneado; no imprime error DB/headers. `retryOnFail:false` y `retry_allowed:false`; conserva ambigüedad conflicto/timeout hasta lookup. El futuro runner debe guardar manifest del fixture y resultado; no depender del historial de ejecuciones desactivado. |

Cambios locales frente al fuente: se retiró el placeholder de credencial; se preserva el texto exacto en vez de `trim().toUpperCase()` para no ocultar conflictos; se conserva correlación al fallar y se valida ID sin convertir bigint a Number. El normalizador cambió de contrato: usar eventos nuevos para esta prueba, no reinterpretar filas antiguas. La clasificación de intención puede normalizar una copia aparte, nunca el payload usado para detectar conflicto.

## Comprobación ejecutada y límites

En esta carpeta, con Node existente `v24.13.0`:

```powershell
node .\prepare-local.cjs
node .\validate-local.cjs
```

Ambos scripts sólo leen/escriben esta carpeta. Se comprobaron hashes de fuentes, JSON/patch reproducible, seis IDs lógicos, conexiones/reachability, inactividad, allowlist de tipos, consulta parametrizada sin retry, terminales stub/error, ausencia de bindings de credenciales y patrones reconocibles de conexión, settings de datos desactivados y compilación de los cuatro bloques JS. **No se ejecutaron los nodos Code, consultas SQL, importación, n8n ni tests concurrentes.** El escaneo de patrones no es un detector universal de secretos. La sintaxis de expresiones n8n, `$()`/item linking, PostgreSQL typeVersion 2.6, `queryReplacement` y `continueErrorOutput` requieren validación en la instancia autorizada.

El fixture procesa un evento por ejecución. Ocho items no son ocho ejecuciones concurrentes. Las 15 pruebas PostgreSQL históricas no prueban este JSON, STOP/HUMAN, recovery, permisos ni exactly-once externo. El stub local es sólo terminal sin despacho; no sustituye un recibo persistente.

## Acceso exacto que falta y única siguiente acción

**Siguiente acción indispensable: el administrador acredita y habilita un destino PostgreSQL exclusivo de ensayo y entrega sólo la referencia de su credencial restringida en n8n.** No existe una base de prueba acreditada. La propuesta previa `onia_claim_test_20261104` / `onia_automation`, owner `onia_claim_test_owner` y runtime `onia_claim_test_runtime`, sigue siendo propuesta.

Para esa entrega: host/puerto/versión y TLS/red desde n8n; identidad/capacidad/respaldo del servidor; acceso administrativo seguro con facultad de crear base/roles y asignar owner; comprobación de que runtime no puede acceder a producto, incluso por CONNECT de PUBLIC. Reutilizar servidor sólo si puede demostrarse aislamiento sin modificar Onia Platform ni ACL de sus bases; de lo contrario, destino separado. Nunca usar DB interna de n8n ni credencial administradora en el workflow.

Para el SQL base, runtime necesita USAGE de schema/secuencias, SELECT/INSERT de inbox/outbox, UPDATE de la columna necesaria para FOR UPDATE y EXECUTE de las funciones elegidas. No DDL/DELETE ni acceso a otros esquemas. El SQL v2 requiere revisión adicional de grants; SECURITY INVOKER con escritura directa de estados no es barrera comercial. Autenticación se configura por el mecanismo seguro del administrador, sin valores en archivos/chat. Acceso del agente a importar/editar/ejecutar una copia n8n y su mecanismo soportado de ensayo concurrente también deben comprobarse; no se heredan del chat cloud ni justifican otra API key por defecto.

Esta preparación no crea recursos ni autoriza provisión, importación o activación. Sólo después del destino y alcance autorizados podrá integrarse la copia, completar los huecos SQL y ejecutar la matriz. Nada se instaló, inició, envió, publicó o modificó fuera de esta carpeta privada; repo oficial, reglas, skills y producto permanecen fuera del cambio.

## Cierre para ONIA · Jefa v2

Coordinación sucesora: chat local `01a1ab9c-15b2-7a03-9588-2daab62a93eb`. Esta unidad termina aquí; no se abrió otra ni se inició integración. Organización consolidará la entrega en el repo oficial único, sin commit/push de esta área. Todos los archivos enumerados en `bundle-manifest.json` son aptos para ese repositorio privado: contienen fixtures sintéticos, referencias de procedencia y propuestas; no valores secretos ni IDs de credenciales ajenas. Las referencias a Page son procedencia histórica, no otro plan activo. No son un paquete público. `bundle-manifest.json` excluye su propio hash.

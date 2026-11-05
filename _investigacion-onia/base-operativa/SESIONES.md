# Chats de trabajo por área

**5 de noviembre de 2026 · America/Caracas.** Reparto vigente decidido por Sergio: siete áreas locales y una sola jefa que delega, revisa y entrega. El repo conserva decisiones/estado/handoff; los chats ejecutan encargos delimitados. [Estado](ESTADO.md) · [Handoff del relevo](continuidad/2026-11-05/HANDOFF-JEFA.md).

## Jefatura y condición del relevo

| Chat | ID / host | Estado y función |
|---|---|---|
| ONIA · Jefa v2 | `01a1ab9c-15b2-7a03-9588-2daab62a93eb` · local | Designada por Sergio; en espera de commit/recepción. Todavía sin rol operativo activo ni aceptación certificada. Asumirá delegación, revisión y entrega tras recepción comprobada. |
| ONIA · Jefa local, saliente | `01a1a29c-3a3d-7b50-aef6-41305ce5faae` · local | Cierra el relevo y la publicación documental; Sergio ordenó reemplazarla y archivarla. Archivo aún no confirmado. No mantener dos jefas operativas simultáneas. |
| ONIA · Jefe, antecedente cloud | `01a1a843-4afb-75f9-aa95-f35833fcb002` · durable | Planificación/síntesis del reparto del 4/11, conservada como historia. No es segunda jefa activa del reparto local. |

Esta consolidación no hace commit/push, no confirma recepción y no archiva chats. La nueva jefa comprobará la revisión recibida; crear o renombrar un chat no acredita ese relevo.

## Áreas locales y orígenes conservados

Sección comunicada por la jefa: **ONIA · Equipo local**, `fe5471f9-55ec-4127-bb68-2ea4aa00994a`. Todos los ejecutores actuales de esta tabla usan host **local**; los orígenes usan **durable**.

| Área / chat local | ID local | Origen cloud | Función / evidencia |
|---|---|---|---|
| ONIA · Marketing y ventas local | `01a1ab81-c60d-7612-8b9f-36c033453287` | `01a1a484-2da0-7440-8502-dfae74ab901f` | Oferta, guion y revisión editorial; [revisión](continuidad/2026-11-05/revisiones/marketing.md). |
| ONIA · Video y contenido local | `01a1ab81-da97-7bc1-a52d-44d255fd0ec3` | `01a1a484-560e-72bb-8d5d-e64733c22027` | Producción y evaluación audiovisual; [revisión](continuidad/2026-11-05/revisiones/video.md). |
| ONIA · Desarrollo y QA local | `01a1ab81-e9b4-7d03-b29e-c11ff1945553` | `01a1a484-065a-76bc-94a2-9b2b148d6021` | Harness, herramientas y pruebas; [revisión](continuidad/2026-11-05/revisiones/desarrollo.md). |
| ONIA · Automatizaciones n8n local | `01a1ab82-3161-76e0-963f-e9ae53ff156b` | `01a1a484-81ca-7605-ab7e-243b8e1f4001` | Workflows y reservas con pruebas; [revisión](continuidad/2026-11-05/revisiones/automatizaciones.md). n8n permanece en VPS. |
| ONIA · Organización diaria local | `01a1ab82-445b-7f53-9a57-ad68c5ac6926` | `01a1a484-ad47-72a9-9684-18557087d01f` | Continuidad documental y proyecciones con alcance aplicable; [revisión](continuidad/2026-11-05/revisiones/organizacion.md). Único escritor documental de este relevo. |
| ONIA Platform · Producto local | `01a1ab82-5531-78c2-8529-52c939967af9` | `01a1a484-d46a-7028-8b80-93f0349f4031` | Producto/QA en su repo independiente; [revisión](continuidad/2026-11-05/revisiones/producto.md). Sin nuevo alcance productivo por este handoff. |
| ONIA · Aprendizaje y criterio local | `01a1ab82-67b4-7963-b529-dcb5816a90fd` | `01a1a935-c691-72d5-b055-e39970f5703e` | Fuentes, práctica y criterio; [revisión](continuidad/2026-11-05/revisiones/aprendizaje.md). No acredita aprendizaje de Sergio. |

Los orígenes cloud quedaron idle según el inventario reportado por la jefa al traspaso y se conservan; no se borraron ni se certifica su estado actual mediante esta edición. Son continuaciones documentales, no traslado integral de VMs, archivos runtime, historial o secretos. No se migran VPS/n8n/startup. La existencia de chats/sección no prueba servicios, scheduler ni ejecución continua.

Las siete revisiones fueron recibidas y revisadas por la jefa saliente. D1 terminó como piloto visual silencioso; la preparación inactiva n8n terminó con 13/13 controles estáticos. Alcance, evidencia y siguientes pasos están en ESTADO y HANDOFF; no se mantiene aquí otra cola.

## Skills y modelos

El [manifiesto](orquestacion.json) mantiene seis claves de CLI: marketing, video, desarrollo, automatizaciones, organización y producto. Aprendizaje y Jefatura no añaden claves/skills por tener chat. Usar las directoras existentes por resultado; continuidad-de-trabajo dirige este relevo y mejorar-sistema apoya la corrección acotada. Las skills no cambian en este encargo.

Preferencia histórica de Sergio: Astra para Jefatura y Sol/Terra para ejecución. La selección explícita de subagentes de JEF-BASE-001 no acredita el modelo efectivo de estos chats; no se comprobó ni modificó el selector por esta consolidación.

## Antecedentes cloud del 3–4 de noviembre

La primera tanda usó entorno `onia`, repo del harness `oninteligenciaartificial/onia`, host durable. Desarrollo reportó arranque/28 tests/navegador/n8n y posterior lectura Meta; Marketing preparó ficha/guion ficticios; Video probó render sintético; Automatizaciones validó ejemplo sintético; Organización leyó agenda sin escribir; Producto leyó GitHub sin despliegue. Cada prueba conserva sus límites en la [consolidación del 4/11](continuidad/2026-11-04/README.md).

Jefe y Desarrollo cloud mostraron read_thread/wait_threads, sin envío/creación de chats en sus catálogos observados. La coordinación local despachó COORD-LOCAL-CLOUD-20261104 y recuperó el resultado; Jefe confirmó lectura de `1884335`. [Prueba histórica](continuidad/2026-11-04/coordinacion-local-cloud.md). No acredita apagado físico de la PC, capacidad universal de otros hosts ni aceptación de Jefa v2.

Las secciones «Marca personal · Cloud» y «ONIA Platform · Cloud» agruparon esos chats el 4/11. Se conservan como procedencia del reparto anterior. La [biblioteca](https://chatgpt.com/space/page_66e12de902408191a926153866f6ca39) aloja medios/procedencia; [Notion Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) es proyección cotidiana. Los medios locales de `operacion/` se recuperan por ruta/hash; las decisiones y el contexto útil del relevo están versionados en este repo.

# Chats de trabajo por área

Recepción confirmada por wait_threads comunicado por saliente: turno `01a1aeec-e73f-7e00-92b1-ba063efe30fe` inProgress, cursor `fda4a4ab-7da2-4462-8673-0faad1d52604:1`; la nueva Jefa recibió el relevo, leyó fuentes y comenzó unidad harness. Ejecución activa, no terminada; modelo efectivo de turn_context pendiente de cotejo por receptora.

**5 de noviembre de 2026 · America/Caracas.** Reparto vigente decidido por Sergio: siete áreas locales y una sola jefa que delega, revisa y entrega. El repo conserva decisiones/estado/handoff; los chats ejecutan encargos delimitados. [Estado](ESTADO.md) · [Handoff del relevo](continuidad/2026-11-05/HANDOFF-JEFA.md).

## Jefatura y condición del relevo

| Chat | ID / host | Estado y función |
|---|---|---|
| ONIA · Jefa Sol 6.1 ultra | `01a1aeec-e579-75c2-a6c3-1326337b3cbc` · local | Creación comprobada, parámetros Sol6.1/ultra aceptados por create_thread; recepción confirmada, unidad harness activa sin terminar. Coordina unidad harness; [relevo](continuidad/2026-11-05/RELEVO-SOL-ULTRA.md). |
| ONIA · Jefa v2, saliente | `01a1ab9c-15b2-7a03-9588-2daab62a93eb` · local | Sólo entrega y cierre de esta publicación; recepción anterior de su relevo conservada como historia, sin nueva investigación. |
| ONIA · Jefa local, saliente | `01a1a29c-3a3d-7b50-aef6-41305ce5faae` · local | Relevo entregado y aceptado; deja la coordinación operativa a Jefa v2. Archivada según list_archived_threads comprobado y comunicado por Jefa v2; evidencia atribuida en RECEPCION-JEFA. |
| ONIA · Jefe, antecedente cloud | `01a1a843-4afb-75f9-aa95-f35833fcb002` · durable | Planificación/síntesis del reparto del 4/11, conservada como historia. No es segunda jefa activa del reparto local. |

Publicación y recepción confirmadas: [RECEPCION-JEFA](continuidad/2026-11-05/RECEPCION-JEFA.md) conserva commit, turno y fuentes leídas. Esta actualización no hace commit/push ni archiva chats.

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

## Entrada de referencias pedida por Sergio

**ONIA · Reels e ideas**, `01a1ac99-eb3b-71a2-96ce-39942950bc63`, host **local**, proyecto **Onia 03/11**. Jefa confirmó su creación y ubicación en **ONIA · Equipo local** el 5 de noviembre, por pedido explícito de Sergio. Recibe reels e ideas, analiza sus aportes y los conecta con trabajos concretos de ONIA desde su [punto de entrada](investigacion/reels-e-ideas/README.md).

Creación y [recepción](investigacion/reels-e-ideas/RECEPCION.md) comprobadas por Jefa: arranque terminado en turno `01a1ac99-ec54-7810-8562-3904603a7a44`, estado COMPLETED. El receptor confirmó las fuentes y verificó 13 enlaces locales. Es una entrada de referencias complementaria a las siete áreas, bajo la única Jefa vigente; no añade jefatura, área ejecutora del CLI ni scheduler. El audio conserva sus dependencias y la decisión vigente de Sergio en el índice de referentes.

## Skills y modelos

El [manifiesto](orquestacion.json) mantiene seis claves de CLI: marketing, video, desarrollo, automatizaciones, organización y producto. Aprendizaje y Jefatura no añaden claves/skills por tener chat. Usar las directoras existentes por resultado; continuidad-de-trabajo dirige este relevo y mejorar-sistema apoya la corrección acotada. Las skills no cambian en este encargo.

**Instrucción actual:** Sergio pidió Jefa GPT6.1 Sol/ultra; creación aceptó esos parámetros, recepción confirmada; modelo efectivo pendiente. La preferencia anterior «Astra exclusivamente Jefa» es antecedente superado para esta nueva Jefa. Ejecutores permanecen: Sol para Marketing, Video, Organización, Aprendizaje y Reels; Terra para Desarrollo, Automatizaciones y Producto. No heredar Astra a subagentes: usar Sol o Terra adecuados con contexto acotado cuando se delegue. La [matriz de aceptación](investigacion/2026-11-05-referentes/GOAL-REFERENTES.md) mantiene el reparto del goal.

**Comprobación histórica efectiva comunicada por Jefa, 5/11/2026, previa al relevo Sol/ultra:** lectura acotada de `model`, `effort` y `timestamp` del último `turn_context` de los rollouts locales, con acceso de lectura compartida. Organización registra esa evidencia atribuida; no repite la lectura de historiales. Los horarios siguientes son UTC y describen esos turnos, no garantizan configuraciones futuras.

| Chat | Modelo / esfuerzo observado | Hora del turno (UTC) |
|---|---|---|
| Jefa | `gpt-6-astra` / ultra | Hora no comunicada en este cotejo |
| Marketing | `gpt-6.1-sol` / medium | 18:31:39Z |
| Aprendizaje | `gpt-6.1-sol` / medium | 18:31:38Z |
| Video | `gpt-6.1-sol` / medium | 18:31:41Z |
| Desarrollo | `gpt-6.1-terra` / medium | 18:31:42Z |
| Organización | `gpt-6.1-sol` / medium | 18:28:20Z |
| Reels e ideas | `gpt-6.1-sol` / low | 18:32:25Z |
| Automatizaciones | `gpt-6.1-terra` / low | 18:32:30.519Z |
| Producto | `gpt-6.1-terra` / low | 18:32:29.705Z |

El último cotejo de `turn_context` comunicado por Jefa confirma también Terra/low para Automatizaciones y Producto en los turnos indicados. Las siete áreas locales y Reels tienen evidencia Sol/Terra; La Jefa saliente usaba Astra en aquel corte; nueva designación Sol/ultra indicada arriba. No se acredita modificación de chats cloud. Esta comprobación de configuración no inicia trabajo n8n/producto. **Corte inicial histórico:** Jefa había despachado investigación a Marketing, Aprendizaje, Video y Desarrollo, con propiedad exclusiva de subcarpetas. La unidad documental inicial fue recibida entonces. Ese despacho no describe su ejecución actual; [ESTADO](ESTADO.md) registra entregas, bloqueo y próxima condición vigentes. Se conserva una única matriz común.

## Antecedentes cloud del 3–4 de noviembre

La primera tanda usó entorno `onia`, repo del harness `oninteligenciaartificial/onia`, host durable. Desarrollo reportó arranque/28 tests/navegador/n8n y posterior lectura Meta; Marketing preparó ficha/guion ficticios; Video probó render sintético; Automatizaciones validó ejemplo sintético; Organización leyó agenda sin escribir; Producto leyó GitHub sin despliegue. Cada prueba conserva sus límites en la [consolidación del 4/11](continuidad/2026-11-04/README.md).

Jefe y Desarrollo cloud mostraron read_thread/wait_threads, sin envío/creación de chats en sus catálogos observados. La coordinación local despachó COORD-LOCAL-CLOUD-20261104 y recuperó el resultado; Jefe confirmó lectura de `1884335`. [Prueba histórica](continuidad/2026-11-04/coordinacion-local-cloud.md). No acredita apagado físico de la PC, capacidad universal de otros hosts ni aceptación de Jefa v2.

Las secciones «Marca personal · Cloud» y «ONIA Platform · Cloud» agruparon esos chats el 4/11. Se conservan como procedencia del reparto anterior. La [biblioteca](https://chatgpt.com/space/page_66e12de902408191a926153866f6ca39) aloja medios/procedencia; [Notion Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) es proyección cotidiana. Los medios locales de `operacion/` se recuperan por ruta/hash; las decisiones y el contexto útil del relevo están versionados en este repo.

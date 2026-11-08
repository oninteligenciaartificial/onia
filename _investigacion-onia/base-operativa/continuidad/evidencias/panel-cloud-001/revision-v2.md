# Addendum de revisión · panel-cloud-001

7 de noviembre de 2026, America/Caracas. Acepto la recuperación del paquete privado y el solape de dos encargos en espacios Cloud existentes. Se conserva el [primer cotejo](revision-v1.md), incluidos los fallos de A y A2, el ensayo sintético de B en Notion y el control negativo local de C. Este addendum aporta evidencia al [registro único](../../tareas/panel-cloud-001.json).

| Tramo | Ventana de trabajo UTC | Fuente comprobada |
|---|---|---|
| A3 · Desarrollo | 11:52:44–11:53:30 | Turno `01a1b5da-6b69-7045-8240-68ddb4ebe71d`. Fetch y commit `exec-25895819-ca52-46c7-b115-7cd5f080222e`. Evidencia de retoma y pieza `exec-8cac7367-a23b-43e0-bbd2-1347da6cdf44`. |
| B2 · Organización | 11:52:48–11:54:02,259325 | Turno `01a1b5da-814f-72b4-9010-414ec7fba864`. Fetch y commit `exec-10703e44-5eac-4645-bda2-f1025c4eb9b9`. Retoma `exec-ed7d3aa8-ced1-4c2d-9bd0-ca46f3ec2272`. Recibo final `exec-824f3649-4d48-424b-851c-5bb146de7b4b`. |

Ambas sesiones obtuvieron `b0329c481d695a70f1916ccab49190313c2eac43` desde `refs/heads/codex/panel-cloud-20261107` y trabajaron con copias temporales. `harness.py retomar referentes-lote-01-001` recuperó revisión 7 aceptada. Se cotejaron el briefing y tres evidencias. B2 verificó además las 11 referencias de `entrega-v2.json`. La prueba de alteración de un byte corresponde al negativo local de C que registra v1.

A3 comprobó presencia y hashes de `PIEZA-01.md` y las dos tarjetas. B2 abrió la pieza, resolvió nueve enlaces locales y verificó PNG de 1080 × 690 y SVG por formato y bytes del commit. La pieza sigue en borrador con grabación y montaje pendientes. La comprobación remota de las tarjetas cubrió integridad y formato.

Las dos ventanas instrumentadas se cruzaron **42 segundos**, de 11:52:48 a 11:53:30. Ambas incluyeron shell efectivo. La misma ruta literal `/tmp/onia-panel-validacion-20261107-espacio` estaba ausente en A3 y conservó `A-desarrollo` tras crearla. B2 leyó `B-organizacion` al inicio y al cierre. Cotejo de marcadores en `exec-42a0746e-b796-42b5-a856-4630ced4013d`, `exec-6ed24d3c-3c4b-4b6a-bf3f-1e6449f52c22` y el recibo final B2. Esto acredita aislamiento observado de los temporales en esas dos ejecuciones y solape de las ventanas, con granularidad de segundos.

Los checkouts de origen mantuvieron sus HEAD y estados previos. En A3 se cotejó la lista de cuatro archivos sintéticos sin seguimiento y en B2 la integridad de 679 archivos. Los fetch incorporaron objetos y metadatos Git. La rama de prueba conserva el commit revisado. Modelo efectivo sin verificar.

B2 releyó en Notion la revisión 2 del mismo borrador sintético de B (`exec-04d00385-a579-4e14-b85e-5f0dadc06614`). Las dos tarjetas derivadas de Git quedaron como proyección temporal, con estado técnico y editorial separados. La escritura demostrada sigue siendo la actualización sintética 1→2 de B.

Quedan pendientes la recuperación en una sesión recién creada, la actualización de tarjetas del panel real, la comprobación desde el celular y cualquier operación continua. Este dictamen cubre el par de chats Cloud existentes y la referencia privada comprobada.

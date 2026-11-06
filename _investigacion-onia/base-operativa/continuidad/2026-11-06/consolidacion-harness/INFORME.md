# Consolidación y continuidad de onia

6 de noviembre de 2026 · America/Caracas. **Implementación y piloto A→B aprobados técnicamente por revisión independiente.** No acredita uso real del teléfono, descubrimiento nativo, producción ni trabajo permanente.

## Autorización, reparto y conservación

Sergio pidió usar onia, una integradora y otra revisora, sin perder lo existente, probar continuidad y mostrar uso móvil. Fuente: chat “Explicar cómo funciona un harness”, turno 01a1b23b-288c-7853-9b84-9285f4dce5ae. Integra 01a1b221-dbd1-7b10-aada-a26094e04705; revisa 01a1af41-1ce0-7b72-a888-7fd658396b4a.

onia/master es la base operativa; onia-harness se conserva como referencia, HEAD f0fd20d, sin modificaciones de esta unidad. La revisora cotejó repetidamente los 21 archivos ajenos inicialmente sucios: hashes intactos. Un directorio nuevo ajeno investigacion/2026-11-06-agentes-harness también quedó fuera de nuestros commits. Los tres snapshots previos conservan sus bytes CRLF y hashes en [HISTORICO](HISTORICO.md).

Cambios: reglas generales separadas de contextos fechados; mapa de seis áreas, nueve directoras propias y nueve apoyos preservado; mismo CLI con registro único local o compartible, migración v1 explícita, revisión esperada, evidencia acumulativa en rutas inmutables, briefing canónico recuperable y aceptación separada de entrega.

## Revisiones y pruebas de código

| Revisión Git | Evidencia |
|---|---|
| 9cf3e40643f8cbf41cfdf9d38c4a0fcb0afe0e41 | Consolidación de 30 archivos revisada antes de publicar; Windows 53 tests, 8 omisiones por symlink. |
| Mismo código, Linux local/WSL | Revisión independiente: 53/53, cero omisiones, 10.189 s, salida 0. Pruebas independientes adicionales de compatibilidad v1, evidencia v1→v2, revisión vieja e ID ambiguo. |
| Mismo código, preparación Cloud | 53/53 sin omisiones, doctor 30/30, enlaces 9+9 correctos; Git limpio. |
| 706bf5eadb13abb7b97dfb286c3df1d546ac71bb | Ajuste final de aceptar/--siguiente: evita conservar la instrucción obsoleta de aceptar como próximo paso. Revisión independiente de diff y CLI; default, seguimiento explícito y vacío rechazado. |
| Código final en preparación Cloud | **54/54**, cero fallos y cero omisiones: bootstrap 13, trabajo 19, harness 22. Git limpio antes/después. |

Comando de suite: python3 -B -m unittest discover -s _investigacion-onia/base-operativa/scripts -p 'test_*.py' -v. La skill de continuidad pasó su validador; se comprobaron enlaces y diff. Tests de concurrencia verifican dos procesos sobre un mismo ID y dos tareas independientes; no prueban bloqueo distribuido entre clones.

Editor Cloud: 01a1b22d-9f2c-72df-8a57-4c1ccb0c800a. Start skill se guardó desde cloud/START-SKILL.md y se cotejó en la interfaz; Install script, privacidad, red, secretos y repositorios se conservaron. Publicación de 9cf3e40 observada a las 15:22 Caracas. El snapshot de cierre incorpora la entrega documental posterior; su publicación se acredita por la confirmación de la interfaz en ese chat, no por la existencia de este archivo.

## Prueba real A → Git → B

| Etapa | Identidad y evidencia |
|---|---|
| A | Sesión Cloud 01a1b238-b446-777a-93c0-e31f4034301f; partió del código 9cf3e40 y produjo tarea continuidad-cloud-001, revisión 2, para_revision. |
| Transporte | La integradora recuperó los cuatro archivos exactos desde la salida de herramienta de A, comprobó 4/4 SHA256 y publicó c3ac63174815b78c0b371b6c6ad52c8a1ef3c03f. La revisora cotejó los cuatro blobs y el cálculo. No hubo sincronización automática ni push de A. |
| B | Sesión nueva 01a1b251-c3f8-7781-9fcf-1874844c401f. Su prompt dio sólo ID, repo, commit y ubicación como datos de tarea; no objetivo, entradas ni resultado esperado. |
| Recuperación B | Arrancó en 9cf3e40 y no tenía el objeto c3ac631. Ejecutó fetch y checkout detached del commit, sin descartar trabajo; retomó revisión 2 y recuperó alcance y próximo paso. |
| Continuación B | Recalculó con Decimal desde CSV, coincidió con A (56.50 y 9 unidades ficticias), conservó evidencia anterior y dejó revisión 3, para_revision, sin aceptarse. |
| Integración B | Se recuperaron dos archivos exactos en salidas separadas porque el primer paquete superó el límite de lectura de la herramienta. Coincidencia 2/2 SHA256; publicados en 955e9810e08a5e8fb654146549e5eedb0947c4ed. |
| Aceptación | Dictamen independiente favorable. El registro canónico conserva la primera aceptación en revisión 4 y la aclaración del próximo paso mediante transiciones normales 5→6; no se reescribió esa historia. |

Registro canónico: [continuidad-cloud-001](../../tareas/continuidad-cloud-001.json). Briefing derivado: [encargo](../../encargos/continuidad-cloud-001.md). Evidencias: [CSV](../../evidencias/continuidad-cloud-001/entrada-v1.csv), [informe A](../../evidencias/continuidad-cloud-001/informe-a-v1.json), [veredicto B](../../evidencias/continuidad-cloud-001/veredicto-b-v1.json).

Hash del registro A en c3ac631: ec330cb12cca837697cd0ab3d974b912ae563d55408a637495d50def91c8eafa. Hash del registro B en 955e981: 4646cd52914da9fd715c24d5e92b3e2ddf83f0d5f753ff16a5d5d61bd414a52e. Veredicto B: 3d4be8f00faa795c72d91020a36232ac7e9815bc2ec7c46560a3caa81ec642b5.

## Controles y límites

B ejecutó en copias temporales siete casos: evidencia alterada, briefing alterado, revisión vieja, verificación fallida al preparar revisión, rechazo de aceptación desde estado no revisable, briefing ausente recuperado idempotentemente y briefing parcial conservado/bloqueado. Los originales quedaron intactos. El veredicto conserva comandos, salidas y límites. Un intento inicial con el valor inválido fallida sólo verificó el enum; se corrigió a fallo y no se contabilizó como control de transición.

La lectura canónica de reglas y skill funcionó en A/B. **B tampoco recibió instrucciones de inicio ni skills ONIA anunciadas nativamente**; el texto guardado en Start skill y los enlaces no demuestran esa activación. El mecanismo comprobado es recuperación explícita y lectura desde la fuente.

El piloto usa datos ficticios y demuestra traspaso dirigido, con una integradora publicando y otra sesión recuperando un commit. No acredita sincronización espontánea, locks distribuidos, recuperación de secretos, tareas 24/7, calidad universal de skills ni servicios de producción.

La [guía iPhone](../../../cloud/MOVIL.md) está contrastada con documentación oficial. Falta observar su recorrido en el teléfono; no hace falta SSH/PEM para la ruta Cloud. Paperclip queda como tablero y ONIA-3 es la tarea existente donde se refleja la entrega para revisión; su actualización se comprueba por lectura del puente al entregar, sin aceptación humana automática ni agentes activos.

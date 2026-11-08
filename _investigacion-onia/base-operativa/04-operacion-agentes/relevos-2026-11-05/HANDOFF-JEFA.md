# Handoff para ONIA · Jefa v2

**5 de noviembre de 2026 · America/Caracas. Corte original: preparado para versionar. Publicación y recepción posteriores confirmadas en [RECEPCION-JEFA](RECEPCION-JEFA.md).** Este documento consolida el contexto útil de la tanda. El repo es la autoridad única; Notion es proyección y Pages sólo medios/procedencia. Los originales privados de `operacion/` son artefactos de origen, no una segunda autoridad.

## Relevo y roles

Sergio ordenó reemplazar a la jefa anterior y archivarla. [SESIONES](../SESIONES.md) identifica a Jefa v2 como única jefa vigente y conserva los IDs de ambas; [ESTADO](../../00-MAPA/ESTADO.md) registra el relevo aceptado. La [recepción](RECEPCION-JEFA.md) acredita la lectura del commit. El archivo de la anterior fue confirmado por Jefa v2 mediante list_archived_threads, según el recibo; no hay dos jefas operativas.

La única jefa confirmada delega, revisa y entrega. Las siete áreas locales realizan el trabajo: Marketing/ventas, Video/contenido, Desarrollo/QA, Automatizaciones, Organización, Producto y Aprendizaje. [SESIONES](../SESIONES.md#áreas-locales-y-orígenes-conservados) es el mapa canónico de roles, IDs locales y orígenes cloud; no duplicar ese registro. Organización es el único escritor documental de esta consolidación. El código de Producto conserva su repo y alcance propios.

Los orígenes cloud se conservan, reportados idle al traspaso; no se borraron ni se verifica aquí un estado nuevo. Continuidad documental no equivale a trasladar VMs, historial completo, archivos runtime o secretos. VPS conserva n8n/startup; no se movieron sus credenciales ni se inició carga pesada.

## Índice mínimo para recibir

1. [ESTADO](../../00-MAPA/ESTADO.md): capacidad, alcance y límites actuales; [reglas comunes](../reglas-comunes.md): autoridad y permisos.
2. [PLAN](../../01-negocio/PLAN.md) y [ORQUESTACION](../ORQUESTACION.md): dirección, despacho y cierres; recuperar sólo las secciones pertinentes.
3. [Índice de siete revisiones](README.md), conservadas completas con procedencia y enlaces ajustados. Cotejo de la jefa saliente y QA independiente reportados; no es una certificación end-to-end.
4. [Brief D1](../../02-contenido/d1-piloto.md), [reporte](../../02-contenido/piloto-d1/reporte.md) y [verificación](../../02-contenido/piloto-d1/verificacion.json).
5. [Bundle n8n terminado](../../05-herramientas/n8n-reserva-local/README.md), [13/13 estáticos](../../05-herramientas/n8n-reserva-local/validation-results.json), [aceptación futura](../../05-herramientas/n8n-reserva-local/aceptacion.md) y [huecos SQL](../../05-herramientas/n8n-reserva-local/sql-gaps.propuesta.md).
6. [Registro de errores](../registro-de-errores.md): audio sin solución, estado sólo ignorado y contexto excesivo.

## Resultado, evidencia y límites de la tanda

**D1:** Marketing corrigió el brief y Video terminó el turno `01a1ab8c-9e81-7c02-b2eb-23eeb35c300b`. Piloto real de tarjetas: 43 s, 1080×1920, H.264, 24 fps, 1032 fotogramas decodificados sin error; 29/29 contrastes, seis advertencias estructurales, render 21,071 s con un trabajador y cero pistas de audio. El muestreo visual no es visionado humano continuo ni escucha. La jefa saliente inspeccionó contacto/verificación; QA editorial aprobó sólo prueba silenciosa. Comprensión humana, locución, tono vocal y retención siguen sin demostrar; no publicación.

**Medios locales fuera de Git:** raíz `C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/piloto-d1-local/`. [MP4](../../operacion/piloto-d1-local/d1-piloto-silencioso.mp4), [contacto visual](../../operacion/piloto-d1-local/contacto-visual.jpg). MP4: 385.060 bytes; SHA-256 `c41798b0c33c1d42232aba8a542696748b548b1ba327560d3ff148edc5f1c71c`, cotejado con archivo local en esta consolidación. [Editable](../../02-contenido/piloto-d1/index.html), ejecutor, configuración, verificador, metadata y evidencia técnica están versionados; [dependencias/procedencia](../../02-contenido/piloto-d1/REPRODUCIBILIDAD.md) documenta versiones, hashes y rutas. No se copiaron MP4, fuentes tipográficas, librerías, fotogramas ni `.work`; la copia no es autocontenida y requiere recuperar las dependencias referenciadas; no se probó como paquete portable. No se acredita una ubicación remota nueva del piloto. Los medios anteriores conservan [Page Video](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4) como procedencia, sin atribuirle este MP4 por inferencia.

**n8n:** turno `01a1ab95-0a78-7643-ab62-6ec96bb69730` confirmado completed por la jefa. Preparación inactiva terminada y recuperable en este repo: copia de seis nodos, patch, SQL fuente, scripts locales, matriz, propuestas y evidencia. Se conserva texto exacto para conflictos y correlación en error. Los **13/13 son estáticos**: no se ejecutaron nodos Code, SQL, importación, carrera ni runtime. STOP/takeover/conciliación y recibo durable siguen propuestos. Los 15 checks PostgreSQL históricos no prueban este workflow. Bundle sin credenciales asignadas; no hubo conexión VPS/DB, servicios ni activación. Código/SQL copiados sin modificar lógica ni ejecutar scripts; [manifiesto original](../../05-herramientas/n8n-reserva-local/bundle-manifest.original.json) y [manifiesto de paquete](../../05-herramientas/n8n-reserva-local/bundle-manifest.json) separan hashes fuente de ajuste de enlaces.

**Otros frentes:** workshop listo documentalmente para ensayo humano; W1 revisada en privado, no venta/despliegue. Producto dispone de un worktree local identificado, pero el recorrido dental de suscripción/reentrada no tiene E2E aceptado. Notion conserva desajustes de estados, precio histórico y prioridades; la lectura de sus 20 IDs no sincronizó el tablero. Los 35 borradores están aparte y no son 35 órdenes activas. Los detalles y pruebas de cada área permanecen en sus notas, sin otra cola en este handoff.

## Autorizaciones y restricciones vigentes

Sergio autorizó la continuidad local, esta consolidación y el relevo. D1 fue una excepción de prueba privada sin publicar; la preparación n8n inactiva también estaba autorizada y ya cerró. No se relanzan esas unidades por registrarlas. La dirección posterior permite contenido y automatizaciones como frentes independientes con encargos concretos; no activa todas sus tareas simultáneamente.

Producto y demás producción, publicaciones/campañas, mensajes reales, gasto e infraestructura requieren alcance aplicable. La preparación n8n no autoriza provisión, importación, SQL o activación. No hay scheduler ni ejecución entre turnos acreditada. No cambiar skills, servicios o paneles como efecto implícito del handoff. El reparto local vigente prevalece sobre pasajes antiguos todavía presentes en CEREBRO-DIARIO/MAPA/arquitectura, fuera de los archivos autorizados para esta consolidación.

## Primera tarea tras la recepción: audio real

**Responsable de despacho/revisión: Jefa v2; ejecución: Video local con Desarrollo local.** Objetivo: cerrar una vía comprobable para evaluar el sonido de una referencia real ya autorizada, empezando por la pista de Pedro y sus fuentes conservadas si siguen recuperables. El piloto D1 es silencioso y no sirve como sustituto. Este encargo sólo prepara el handoff: no se ejecutó investigación acústica ahora.

- Recuperar el medio autorizado y su pista con procedencia/hash/duración; comprobar las capacidades efectivas disponibles. Probar primero opciones abiertas/autorizadas y recursos existentes, sin Gemini ni API paga por defecto, ni nuevos modelos pesados en VPS.
- Comparar controles conocidos de silencio y sonido con el audio real. Descartar métodos que inventen sonidos: Qwen ya falló sobre silencio. Conservar esperado/observado, segmentos y fallos; no repetir el mismo bloqueo sin cambiar la condición.
- Evaluar voz/prosodia, música, SFX, ambiente, silencios, ritmo y sincronía con timecodes. ASR aporta palabras; YAMNet/CLAP candidatos acústicos. Ninguno certifica por sí solo emoción, prosodia, efecto preciso o escucha integral. Indicar cobertura exacta y qué pudo o no verificarse mediante escucha.
- Si las alternativas probadas dejan una necesidad humana, preparar el fragmento y la pregunta concreta que sólo Sergio deba resolver. Pedir esa intervención mínima con evidencia de lo intentado; no devolverle descargas/extracciones que los agentes puedan hacer ni cerrar repitiendo únicamente el límite.

**Aceptación:** medio recuperable y controles esperado/observado; reporte de cobertura y hallazgos acústicos verificables por tramo; conexión con imagen/guion; solución ejecutada para el alcance posible y una intervención precisa sólo si sigue siendo indispensable. Un método que etiqueta silencio como sonido no se acepta. Si queda cobertura pendiente, se conserva como pendiente con vía concreta, sin declarar revisión integral ni calidad vocal demostrada. No genera publicación, gasto ni una pieza comercial por sí misma.

## Continuidad independiente de n8n

No repetir la preparación terminada ni la revisión completa. La próxima unidad es **acreditar un destino PostgreSQL exclusivo de ensayo y una referencia de credencial restringida**, con administrador responsable y alcance concreto antes de importar/ejecutar. [README del bundle](../../05-herramientas/n8n-reserva-local/README.md#acceso-exacto-que-falta-y-única-siguiente-acción) especifica el faltante. Aceptación previa: identidad/aislamiento/red/permisos comprobados sin tocar producto ni exponer secretos. Sólo después se podrá autorizar integración y la matriz runtime; esta consolidación no las inicia.

## Recepción y cierre compacto

El corte preparado de este handoff fue publicado y recibido: [RECEPCION-JEFA](RECEPCION-JEFA.md) registra la confirmación de fuente, alcance, evidencia, límites y primera tarea por Jefa v2. El recibo incorpora la confirmación posterior de archivo de la anterior, atribuida a Jefa v2. El alcance activo posterior se consulta en el [índice de referentes](../../03-referentes/corpus-2026-11-05/README.md); esta actualización documental no ejecuta su investigación.

Cada área cierra con **resultado; evidencia/enlace; prueba realizada; bloqueo con solución; siguiente acción**. Cargar fuentes adicionales sólo si hacen falta para comprobar o decidir. No pegar historiales completos ni repetir grandes lecturas, y no reducir silenciosamente la cobertura del encargo.

# Lector manual y panel de consulta de la fábrica

## Propuesta 1 elegida por Sergio

La [guía de revisión del diseño](GUIA-REVISION-DISENO.md) describe la vista actual, la corrección de política del formulario y las comprobaciones completadas en el host. Abrir el [preview de Propuesta 1](evidencia/diseno-20261111/preview-coordinadora/panel.html). La [comparación visual](design-qa.md) pasó después de corregir los hallazgos del navegador. Entrega pendiente de revisión independiente y de Sergio.

## Ampliación del 11 de noviembre de 2026

La [GUIA-REVISION](GUIA-REVISION.md) contiene el acceso al panel ampliado, el modo temporal de revisión persistente, comandos, pruebas y dependencias pendientes. El [preview vigente de esta entrega](evidencia/operacion-20261111/preview-final/panel.html) conserva la tanda histórica y los fixtures identificados. Los apartados siguientes documentan las entregas anteriores.

9/11/2026 UTC · encargo `fabrica-lector-panel-20261109`. Implementación local con Python stdlib y Playwright ya instalado en el VPS. Directora `desarrollar-y-verificar`, anunciada en el catálogo y leída desde su fuente canónica. Sin hijos ni instalaciones.

Funciona: consulta pública real de tres páginas oficiales —dos guías y una noticia—, snapshot saneado, proyección de tres registros únicos y dos guiones reales, HTML autónomo y 22 pruebas sin red. **Corrección visual comprobada, lista para revisión independiente.** Se añadió únicamente `overflow-wrap:anywhere` a `body`. El host autorizado del coordinador ejecutó los cinco casos con Chromium1252 y sandbox; esta ejecutora abrió e inspeccionó las cinco capturas. [Comprobación final](evidencia/COMPROBACION-03.json), [capturas y alcance](evidencia/host-02/INSPECCION.md).

Abrir [panel corregido](evidencia/panel-corregido-01/panel.html). Su [snapshot](evidencia/panel-corregido-01/snapshot.json) es idéntico byte a byte al de [lectura-real-02](evidencia/lectura-real-02/snapshot.json): misma consulta de las 05:14 UTC y mismo commit de entradas `cf43c113a7a29fdea27b9d278899aef36f02cd67`, con render CSS nuevo. Esta retoma no consultó la red ni actualizó fechas/estados. Lecturas e intentos anteriores permanecen intactos.

## Reproducir y actualizar manualmente

Desde la raíz de este worktree. Cada directorio de salida debe ser nuevo: los recibos anteriores se conservan, y una salida existente falla antes de consultar la red.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
PYTHONDONTWRITEBYTECODE=1 python3 "$D/lector.py" --salida "$D/evidencia/lectura-real-03"
```

Para consultar sólo una fuente, añadir `--fuente F01`, `--fuente F02` o `--fuente F06`. No admite URLs del usuario ni descubre enlaces. Produce `snapshot.json` y `panel.html`; salida 0 significa lectura/proyección comprobadas, 2 significa resultado parcial con fallos visibles por fuente o evidencia. No certifica revisión editorial, captura ni permiso de publicación.

Para regenerar únicamente HTML desde un recibo conservado, sin red:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$D/panel.py" --snapshot "$D/evidencia/lectura-real-02/snapshot.json" --salida "$D/evidencia/lectura-real-02/panel-reproducido.html"
PYTHONDONTWRITEBYTECODE=1 python3 "$D/pruebas.py"
```

El renderizador conserva la fecha y procedencia del recibo: no revalida su actualidad ni autentica un JSON editado. Para actualizar los estados canónicos o verificar de nuevo los guiones, ejecutar el lector completo; para usar una afirmación de producto, releer también su contenido. El resumen propio tiene revisión manual del 9/11; el lector extrae metadatos y no redacta un resumen nuevo automáticamente.

## Fuentes y alcance real

Catálogo cerrado, comprobado con herramienta web y HTTP del VPS antes de fijarlo:

| ID | Fuente primaria | Consulta real | Fecha y cobertura |
|---|---|---|---|
| F01 | [Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude) · Anthropic | HTTP 200; 217645 bytes | Fecha visible 30/10/2026, rotulada actualización. Acceso y primeros pasos; no acredita cuenta ni cuota propia |
| F02 | [My prompt isn’t giving me a helpful answer](https://support.claude.com/en/articles/7996857-my-prompt-isn-t-giving-me-a-helpful-answer) · Anthropic | HTTP 200; 195355 bytes | Fecha visible 16/3/2026; no se atribuye publicación original. Recomendaciones generales, sin validar nuestros ejemplos |
| F06 | [Controles de seguridad Enterprise](https://claude.com/resources/articles/claude-enterprise-security-updates) · Anthropic | HTTP 200; 501248 bytes | Publicación/anuncio 5/11/2026, cotejado en metadato y fecha visible. Candidata no seleccionada para G01/G02. Enterprise con condiciones beta, sin extrapolar a Free |

F01/F02 son guías evergreen, no noticias del día. Su publicación original y fecha del hecho permanecen `null`. F06 conserva fecha de publicación con precisión de día y fecha del hecho como anuncio, sin probar despliegue individual. El parser exige `article:published_time=2026-11-05` y la fecha visible concordante; si faltan, no completa con consulta ni con referencia previa. Consulta y publicación tienen campos diferentes. No se usa `Last-Modified` ni la fecha del servidor como publicación. No se añadieron feeds sin comprobar ni noticias ficticias.

Máximo tres selecciones y veinte items por fuente por contrato. Implementa tres fuentes de una página/un item cada una, sin crawler. Sólo permite las tres URLs exactas, incluyendo exclusivamente ese artículo de `claude.com`. Cada consulta admite 512 KiB y 12 s totales, incluidos goteo y conexión, con SIGALRM en el hilo principal de Linux y timeout de socket. Rechaza redirecciones, compresión, tipo distinto de HTML, login/challenge no reconocido y URLs fuera del catálogo. Sin reintentos, cookies o autenticación. Guarda hash/tamaño, título, fechas, atribución y resumen breve propio; nunca HTML ni artículos completos.

Deduplicación por URL canónica dentro de cada invocación, quitando fragmento/UTM/fbclid/gclid y conservando alias; un duplicado no repite GET. No hay deduplicación semántica, memoria de noticias entre ejecuciones ni cola persistente. Un fallo conserva código fijo y continúa las independientes; si fallan todas, muestra vacío/error sin fingir lectura nueva. Para F06, el fallo conserva además la referencia documental previa rotulada como tal, sin crear un item leído. Los recibos anteriores siguen disponibles con su fecha.

## Autoridad y revisión

Reutiliza [diseño y contrato del 8/11](../20261108/CONTRATO.md) y [contrato Telegram del 9/11](../20261109-telegram/CONTRATO.md). No ejecuta sus adaptadores ni copia tareas sintéticas como reales.

Lee mediante `trabajo.read_task`/`verify` los registros `fabrica-contenido-diseno-20261108`, `noche-telegram-20261109` y `noche-workshop-contenido-20261109`. Verifica evidencias/briefings, exige que los registros coincidan con HEAD y proyecta sólo campos permitidos, sin sesiones, datos privados ni briefing. Un fallo oculta el estado no verificado y queda visible. No escribe en el harness ni invoca crear/decidir/aceptar/cerrar.

G01/G02 e I01/I02 proceden de [la entrega real del workshop](../../../01-negocio/workshop-20261108/noche-20261109/README-ENTREGA.md). El recibo de revisión debe coincidir con el cierre/aceptación canónicos; los bytes de cada guion y manifiesto deben coincidir con ese commit revisado, además de cotejar hash/tamaño original. Una alteración bloquea la etiqueta de revisión técnica, sin rehashear para legitimar nada. La prueba negativa sólo altera bytes en memoria.

Ambos guiones son **borradores técnicamente revisados**, no aprobados para publicar. El texto completo propio, patrón, fuentes y pendientes están desplegables en el HTML. La aceptación de una entrega documental no concede permiso editorial ni de producción. Este lector no interpreta futuras autorizaciones de publicación: necesita otro alcance para ello. Los próximos pasos de las tres tarjetas se derivan literalmente de los registros únicos, y los de cada guion, de su documento.

El snapshot es un recibo generado y el HTML su proyección descartable; no son otro registro editable. Sin formularios, aprobación, copiar/exportar intenciones, JavaScript o envíos. Texto escapado, enlaces oficiales validados, CSP sin recursos remotos ni acciones de formulario. No es un servicio autenticado: conservar como archivo local compartible dentro de este repo, no publicar como sitio.

## Prueba visual del host

El script prepara casos largo/vacío/error claramente sintéticos y prueba escritorio y móvil. Usa perfil temporal propio, Chromium1252 con `chromiumSandbox: true`, abre `file://`, bloquea HTTP automático y cierra su navegador. No usa visor, cuentas, puertos ni servidor.

```bash
node "$D/visual.cjs" "$D/evidencia/panel-corregido-01/snapshot.json" "$D/evidencia/visual-03"
```

Ejecutar este comando sólo desde el host autorizado con sandbox compatible; el comprobador final se ejecutó por el coordinador en copia aislada con estructura de repo y salida `host-02`, no dentro del sandbox de esta ejecutora. La [solicitud v2](evidencia/solicitud-host-v2.json) y el [recibo del host](evidencia/host-02/RECIBO-HOST.json) coinciden en los cinco hashes de entrada; las fuentes capturadas siguen intactas. Resultado rc0: escritorio 1440×1000, móvil 390×844 y fixtures largo/vacío/error pasaron. El navegador cerró, sin solicitudes HTTP automáticas, controles de mutación ni errores JS detectados.

Esta ejecutora abrió con `view_image` los cinco PNG copiados a [host-02](evidencia/host-02/INSPECCION.md). En escritorio los hashes largos se parten dentro de la tarjeta. Móvil y texto largo mantienen una columna sin recortes aparentes; vacío y error muestran fallos/ausencias explícitos. Las imágenes móviles completas son muy altas y el visor las reduce: no se acredita lectura fina de cada carácter por esas miniaturas. Los controles DOM y la inspección visual son evidencia complementaria, no una auditoría exhaustiva de accesibilidad ni prueba de un dispositivo físico.

`real-desktop`/`real-mobile` muestran datos de la lectura real02 y los guiones existentes; los otros tres casos son fixtures rotulados SINTÉTICO, no lecturas nuevas ni tareas reales. Se conserva el [fallo anterior](evidencia/host-fallo-01.json) de escritorio/móvil y el intento bwrap, sin sobrescribirlos. Sólo se copiaron cinco PNG y recibos públicos: ningún perfil, cookie o material externo. No se cambió AppArmor/bwrap ni se ejecutó Chromium en el sandbox de la ejecutora. Falta la revisión independiente y aceptación/integración del coordinador.

No hay scheduler, cron, ingesta recurrente, conexión Telegram real, n8n API, LLM pago, publicación de contenido ni despacho de agentes. La publicación autorizada de esta entrega es exclusivamente Git en su rama. Coordinación conserva cierre, revisión independiente e integración a master. Las comprobaciones [inicial](evidencia/COMPROBACION.json) y [parcial](evidencia/COMPROBACION-02.json) se conservan como históricas.


## Consultar la tanda de cinco guiones · 11 nov

Se amplía este panel, sin otro servicio ni panel nuevo. Desde la raíz del repo:

```sh
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
T=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v2/guiones-panel.json
python3 -B "$P/tanda.py" --tanda "$T" --salida "$P/evidencia/tanda-consulta-nueva"
```

Abrir panel.html en la salida. El destino debe ser nuevo. La proyección comprueba bytes y conserva revisión técnica pendiente; no consulta noticias, no modifica harness, no aprueba guiones. Si la tanda aún difiere del commit local, lo dice en vez de atribuir sus bytes a HEAD. La suite existente22/22 y tres pruebas nuevas de tanda pasaron.

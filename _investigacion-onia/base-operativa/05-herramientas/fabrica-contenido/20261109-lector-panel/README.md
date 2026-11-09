# Lector manual y panel de consulta de la fábrica

9/11/2026 UTC · encargo `fabrica-lector-panel-20261109`. Implementación local con Python stdlib y Playwright ya instalado en el VPS. Directora `desarrollar-y-verificar`, anunciada en el catálogo y leída desde su fuente canónica. Sin hijos ni instalaciones.

Funciona: consulta pública real de tres páginas oficiales —dos guías y una noticia—, snapshot saneado, proyección de tres registros únicos y dos guiones reales, HTML autónomo y 22 pruebas sin red. **Entrega parcial: criterio 5 todavía pendiente.** El host autorizado del coordinador abrió Chromium1252 con sandbox, pasó escritorio y falló móvil por desborde horizontal. Esta ejecutora inspeccionó la captura parcial de escritorio; no acredita la prueba visual completa. [Recibo de retoma](evidencia/COMPROBACION-02.json) y [diagnóstico](ERRORES.md).

Abrir [panel actualizado](evidencia/lectura-real-02/panel.html). Su [snapshot](evidencia/lectura-real-02/snapshot.json) contiene los datos consultados a las 05:14 UTC, no una vista en vivo. El commit de entradas `cf43c113a7a29fdea27b9d278899aef36f02cd67` identifica los documentos y registros proyectados. La primera [lectura de dos guías](evidencia/lectura-real-01/snapshot.json) y el [intento previo en bwrap](evidencia/visual-01/resultado.json) permanecen intactos.

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

## Prueba visual del host y pendiente material

El script prepara casos largo/vacío/error claramente sintéticos y prueba escritorio y móvil. Usa perfil temporal propio, Chromium1252 con `chromiumSandbox: true`, abre `file://`, bloquea HTTP automático y cierra su navegador. No usa visor, cuentas, puertos ni servidor.

```bash
node "$D/visual.cjs" "$D/evidencia/lectura-real-02/snapshot.json" "$D/evidencia/visual-02"
```

Este comando corresponde al comprobador ejecutado por el coordinador en una copia aislada con estructura de repo, no dentro del sandbox de esta ejecutora. [Solicitud congelada](evidencia/solicitud-host.json): los cinco hashes de fuente coinciden con la respuesta y siguen intactos. El host arrancó Chromium con sandbox y perfil sintético, pasó escritorio 1440×1000 y falló móvil 390×844 por desborde; terminó con rc1 y navegador cerrado. No llegó a los casos largo/vacío/error.

Esta ejecutora abrió con `view_image` la única captura de escritorio en la ruta autorizada del host: guiones, tres fuentes y separación noticia/guías visibles; los hashes extensos del próximo paso canónico sobresalen de una tarjeta. El assert global de escritorio no detectó ese desborde interno. No se exportaron capturas del intento fallido: el protocolo condicionaba su copia a rc0. Se conserva [recibo público y observación](evidencia/host-fallo-01.json), con hash de esa imagen; no contiene perfiles ni cookies.

Condición de salida para una corrección posterior: ajustar el quiebre de cadenas largas, comprobar tarjetas además del ancho del documento y obtener cinco PNG de los archivos finales, con sandbox, para inspeccionarlos. Los asserts DOM no sustituyen inspección visual. Según la respuesta del coordinador, esta retoma cierra parcial sin relanzar; código, snapshot y HTML capturados permanecen estables. No se cambió AppArmor/bwrap ni se repitió navegador en el sandbox de la ejecutora.

No hay scheduler, cron, ingesta recurrente, conexión Telegram real, n8n API, LLM pago, publicación de contenido ni despacho de agentes. La publicación autorizada de esta entrega es exclusivamente Git en su rama. Coordinación conserva cierre, revisión independiente e integración a master. La [comprobación inicial](evidencia/COMPROBACION.json) se conserva como histórica; no describe el resultado de esta retoma.

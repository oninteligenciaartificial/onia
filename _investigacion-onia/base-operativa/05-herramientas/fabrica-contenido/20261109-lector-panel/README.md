# Lector manual y panel de consulta de la fábrica

9/11/2026 UTC · encargo `fabrica-lector-panel-20261109`. Implementación local con Python stdlib y Playwright ya instalado en el VPS. Directora `desarrollar-y-verificar`, anunciada en el catálogo y leída desde su fuente canónica. Sin hijos ni instalaciones.

Funciona: consulta pública real de dos páginas oficiales, snapshot saneado, proyección de tres registros únicos y dos guiones reales, HTML autónomo y 17 pruebas sin red. **Pendiente de aceptación: criterio 5, apertura e inspección de captura.** Chromium1252 falló al arrancar con sandbox en esta sesión; no hay captura ni legibilidad visual acreditada. [Intento conservado](evidencia/visual-01/resultado.json) y [diagnóstico](ERRORES.md).

Abrir [panel generado](evidencia/lectura-real-01/panel.html). Su [snapshot](evidencia/lectura-real-01/snapshot.json) contiene los datos consultados a las 05:03 UTC, no una vista en vivo. El commit de entradas `fa9a6e6f1714cd9dccbb5cab3f7baad177938c20` identifica el checkout cuyos documentos y registros se proyectaron; no es el commit de implementación del lector.

## Reproducir y actualizar manualmente

Desde la raíz de este worktree. Cada directorio de salida debe ser nuevo: los recibos anteriores se conservan, y una salida existente falla antes de consultar la red.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
PYTHONDONTWRITEBYTECODE=1 python3 "$D/lector.py" --salida "$D/evidencia/lectura-real-02"
```

Para consultar sólo una fuente, añadir `--fuente F01` o `--fuente F02`. No admite URLs del usuario ni descubre enlaces. Produce `snapshot.json` y `panel.html`; salida 0 significa lectura/proyección comprobadas, 2 significa resultado parcial con fallos visibles por fuente o evidencia. No certifica revisión editorial, captura ni permiso de publicación.

Para regenerar únicamente HTML desde un recibo conservado, sin red:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$D/panel.py" --snapshot "$D/evidencia/lectura-real-01/snapshot.json" --salida "$D/evidencia/lectura-real-01/panel-reproducido.html"
PYTHONDONTWRITEBYTECODE=1 python3 "$D/pruebas.py"
```

El renderizador conserva la fecha y procedencia del recibo: no revalida su actualidad ni autentica un JSON editado. Para actualizar los estados canónicos o verificar de nuevo los guiones, ejecutar el lector completo; para usar una afirmación de producto, releer también su contenido. El resumen propio tiene revisión manual del 9/11; el lector extrae metadatos y no redacta un resumen nuevo automáticamente.

## Fuentes y alcance real

Catálogo cerrado, comprobado con herramienta web y HTTP del VPS antes de fijarlo:

| ID | Fuente primaria | Consulta real | Fecha y cobertura |
|---|---|---|---|
| F01 | [Get started with Claude](https://support.claude.com/en/articles/8114491-get-started-with-claude) · Anthropic | HTTP 200; 217633 bytes | Fecha visible 30/10/2026, rotulada actualización. Acceso y primeros pasos; no acredita cuenta ni cuota propia |
| F02 | [My prompt isn’t giving me a helpful answer](https://support.claude.com/en/articles/7996857-my-prompt-isn-t-giving-me-a-helpful-answer) · Anthropic | HTTP 200; 195355 bytes | Fecha visible 16/3/2026; no se atribuye publicación original. Recomendaciones generales, sin validar nuestros ejemplos |

Ambas son guías evergreen, no noticias del día. Publicación original y fecha del hecho permanecen `null`; consulta y fecha visible tienen campos diferentes. No se usa `Last-Modified`, la fecha del servidor ni la de consulta como publicación. No se añadieron feeds sin comprobar ni noticias de los fixtures anteriores.

Máximo tres selecciones y veinte items por fuente por contrato. Este lector implementa dos fuentes de una página/un item cada una, sin crawler. Cada consulta admite 512 KiB y 12 s totales, incluidos goteo de respuesta y conexión, con SIGALRM en el hilo principal de Linux y timeout de socket. Rechaza redirecciones, compresión, tipo distinto de HTML, página de login/challenge no reconocida y URLs fuera del catálogo. Sin reintentos, cookies o autenticación. Guarda hash/tamaño de respuesta, título, fechas, atribución y resumen breve propio; nunca HTML ni artículos completos.

Deduplicación por URL canónica dentro de cada invocación, quitando fragmento/UTM/fbclid/gclid y conservando alias; un duplicado no repite GET. No hay deduplicación semántica entre dominios, memoria de noticias entre ejecuciones ni cola persistente. Si una fuente falla, queda el código fijo y se continúa la independiente; si fallan ambas, se muestra vacío/error sin fingir una consulta exitosa ni recurrir silenciosamente a datos viejos. Los recibos anteriores siguen disponibles con su fecha.

## Autoridad y revisión

Reutiliza [diseño y contrato del 8/11](../20261108/CONTRATO.md) y [contrato Telegram del 9/11](../20261109-telegram/CONTRATO.md). No ejecuta sus adaptadores ni copia tareas sintéticas como reales.

Lee mediante `trabajo.read_task`/`verify` los registros `fabrica-contenido-diseno-20261108`, `noche-telegram-20261109` y `noche-workshop-contenido-20261109`. Verifica evidencias/briefings, exige que los registros coincidan con HEAD y proyecta sólo campos permitidos, sin sesiones, datos privados ni briefing. Un fallo oculta el estado no verificado y queda visible. No escribe en el harness ni invoca crear/decidir/aceptar/cerrar.

G01/G02 e I01/I02 proceden de [la entrega real del workshop](../../../01-negocio/workshop-20261108/noche-20261109/README-ENTREGA.md). El recibo de revisión debe coincidir con el cierre/aceptación canónicos; los bytes de cada guion y manifiesto deben coincidir con ese commit revisado, además de cotejar hash/tamaño original. Una alteración bloquea la etiqueta de revisión técnica, sin rehashear para legitimar nada. La prueba negativa sólo altera bytes en memoria.

Ambos guiones son **borradores técnicamente revisados**, no aprobados para publicar. El texto completo propio, patrón, fuentes y pendientes están desplegables en el HTML. La aceptación de una entrega documental no concede permiso editorial ni de producción. Este lector no interpreta futuras autorizaciones de publicación: necesita otro alcance para ello. Los próximos pasos de las tres tarjetas se derivan literalmente de los registros únicos, y los de cada guion, de su documento.

El snapshot es un recibo generado y el HTML su proyección descartable; no son otro registro editable. Sin formularios, aprobación, copiar/exportar intenciones, JavaScript o envíos. Texto escapado, enlaces oficiales validados, CSP sin recursos remotos ni acciones de formulario. No es un servicio autenticado: conservar como archivo local compartible dentro de este repo, no publicar como sitio.

## Prueba visual pendiente y condición de salida

El script prepara casos largo/vacío/error claramente sintéticos y prueba escritorio y móvil. Usa perfil temporal propio, Chromium1252 con `chromiumSandbox: true`, abre `file://`, bloquea HTTP automático y cierra su navegador. No usa visor, cuentas, puertos ni servidor.

```bash
node "$D/visual.cjs" "$D/evidencia/lectura-real-01/snapshot.json" "$D/evidencia/visual-02"
```

Ejecutarlo desde una sesión autorizada cuyo sandbox permita arrancar Chromium con sus namespaces. Debe devolver cinco casos OK, crear cinco PNG y luego **abrir e inspeccionar** esas capturas; los asserts DOM no sustituyen esa inspección. El primer intento en esta sesión devolvió `No usable sandbox` bajo `bwrap//&unpriv_bwrap`, `NoNewPrivs=1`, `Seccomp=2`. No se cambió AppArmor ni se usó `--no-sandbox`, sudo, otro perfil humano o una sesión fuera del sandbox. No repetir el mismo intento sin cambiar la condición de ejecución.

No hay scheduler, cron, ingesta recurrente, conexión Telegram real, n8n API, LLM pago, publicación de contenido ni despacho de agentes. La publicación autorizada de esta entrega es exclusivamente Git en su rama. Coordinación conserva cierre, revisión independiente e integración a master. [Comprobación saneada](evidencia/COMPROBACION.json).

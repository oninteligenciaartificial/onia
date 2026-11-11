# Revisar Propuesta 1 en el panel

Retoma autorizada de `cerebro-panel-usable-20261109`, desde HEAD `dd41bcc8d8e26a31bcdf471ff13499e274e83f21`, que contiene master d539644 y la entrega previa 62bdcac. Modelo solicitado Sol6.1 high, cero hijos. Runtime y cuota atribuibles a esta retoma desconocidos. La tarea y el briefing canónicos siguen bajo coordinación.

## Abrir la entrega

El [preview de Propuesta 1](evidencia/diseno-20261111/preview-coordinadora/panel.html) usa el render Python/HTML existente. Cabecera compacta, sidebar, seis filas, inspector, clases y nota del vlog reproducen la estructura elegida. [Referencia exacta conservada](diseno/propuesta-1.png).

La navegación del preview funciona mediante enlaces locales, selectores CSS, radios y details nativos. Permite seleccionar secciones y fábricas, abrir pasos, escoger Resultado/Fuentes/Cambios y leer los guiones. La consulta del cerebro mostrada es una recuperación documental local. Para consultar otras etiquetas o guardar revisiones, abrir el modo temporal.

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
R=05-herramientas/fabrica-contenido/20261109-lector-panel
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-panel-propuesta1-sergio-20261111 \
  --estado "$R/estado-fabrica.json"
```

Abrir la dirección loopback impresa en un navegador de la misma máquina. El puerto predeterminado es 8765, modificable con `--puerto`. Ctrl+C termina el servidor. Mantener el mismo directorio `--datos` para recuperar las revisiones. `/tmp` sirve para el ensayo y depende de la limpieza del host. El operador puede elegir otra ubicación privada fuera de Git para conservar los datos.

## Recorrido para Sergio

1. Recorrer Hoy, Fábricas, Calendario, Cerebro y Sala de montaje desde la izquierda. Sala de montaje muestra la preparación pendiente y el acceso a sus pasos.
2. En Fábricas, seleccionar una fila con su acción derecha. El inspector muestra la selección. Abrir pasos para revisar evidencias, entregas y requisitos. Las fábricas sin export permanecen pendientes. Los círculos completos exigen un paso completado declarado en un export validado.
3. En el inspector de guiones, alternar Resultado, Fuentes y Cambios. Abrir T01 para leer su texto, procedencia y revisión local. Los hashes y las rutas están dentro de los detalles de procedencia.
4. Abrir Revisar resultado, escribir motivo y propuesta y guardar. La respuesta correcta es un POST 303 seguido de la confirmación visible, con revisión local v1 pendiente y original conservado. Repetir después de detener y arrancar el servidor con el mismo `--datos`. Una segunda revisión obtiene v2.
5. En Cerebro, consultar tema `revision`, uso `workshop`. Abrir fuente, pasaje y límites de un patrón. El cerebro existente valida sus fuentes y pasajes durante la consulta.
6. Revisar las clases 13-nov 20:00, 14-nov 14:00 y 16-nov 20:00, America/La_Paz. El encabezado usa la fecha de generación de la consulta convertida a esa zona. La tanda v2 conserva su fecha editorial y su alerta de horarios sustituidos.

El preview conserva v2 y los datos de origen. La maqueta contenía una tanda v3 y marcas de progreso de ejemplo. La implementación muestra el contrato recibido y sus pendientes. La reunión de exports de otros productores corresponde a la coordinadora. Se admite `--estado` repetible y `--tanda` con las rutas validadas del contrato anterior.

Para probar un recorrido sintético de fábrica, añadir al comando del servidor

```bash
  --estado "$R/fixtures/tarea-sintetica/estado-fabrica.json"
```

Ese fixture permanece rotulado ENSAYO SINTÉTICO. La corrección sobre T01 existente también se ensaya localmente con texto de prueba, conservando intacta su fuente.

## Corrección del 403

`Referrer-Policy: no-referrer` y el meta anterior podían provocar `Origin: null` en el formulario nativo. Se aplicó `same-origin` a la cabecera y al meta. El servidor exige Host y Origin exactos de su puerto loopback, token CSRF, huella del resultado y versión vigente. Mantiene rechazo de Origin ausente, null, wildcard y ajeno. La ruta de favicon devuelve 204 para evitar un error de recurso durante el ensayo. La CSP admite únicamente estilos inline, máscaras/font incrustados y la acción de formulario local. [Norma primaria Fetch](https://fetch.spec.whatwg.org/#origin-header)

Las pruebas HTTP y el navegador del host pasaron. La coordinadora corrigió la visibilidad de T01 y el aviso después de guardar, verificó Origin:null → 403 y same-origin → 303 y recuperó la revisión tras reiniciar. Evidencia: `evidencia/diseno-20261111/host-final-02/resultado.json`, capturas y `design-qa.md` con `final result: passed`. El intento bloqueado de la ejecutora se conserva como histórico.
## Comprobaciones y host

```bash
python3 -B "$P/pruebas.py"
python3 -B -m unittest discover -s "$P" -p 'test_*.py' -v
node --check "$P/visual-operacion.cjs"
node --check "$P/visual-diseno.cjs"
git diff --check
```

Resultados de esta retoma en [pruebas.txt](evidencia/diseno-20261111/pruebas.txt). Python 55/55, compuestos por originales 22, tanda 3, operación 23 y diseño/origen 7. Las siete regresiones nuevas comprueban navegación HTML y destinos, estados sustentados por contrato, fecha con zona, integridad/licencias de recursos, ambas políticas de respuesta y rechazo de orígenes inválidos. Las pruebas originales de XSS, rutas, token, huella, versión, persistencia y concurrencia siguen presentes. Las comprobaciones DOM y de política no acreditan la fidelidad renderizada. El [recorrido CLI de esta retoma](evidencia/diseno-20261111/recorrido-cli.json) confirmó GET 200, rechazo 403 de orígenes inválidos, POST 303 con origen exacto y recuperación de propuesta/original tras terminar y abrir otro proceso Python.

En el host con Playwright/Chromium ya existente, usar un directorio nuevo

```bash
node "$P/visual-diseno.cjs" "$P/evidencia/diseno-20261111/host-01"
```

El script ejecuta el servidor temporal con una SQLite sintética privada en `/tmp`, comprueba los tres viewports 1487×1058, 1440×1000 y 390×844, navegación, selección de seis fábricas, inspector, T01, guardado y reinicio. Compara la política anterior en una respuesta controlada de ensayo y después exige el guardado con same-origin. Registra únicamente Origin, Referer, Host y estado HTTP de esos formularios, redactando la dirección local como loopback. Cierra servidor y navegador al finalizar. La generación del comparativo usa Pillow existente, sin instalaciones.

Debe producir `objetivo.png`, `desktop.png`, `mobile.png`, `mobile-completo.png`, `guardado.png`, `comparacion.png` y `resultado.json`. El comparativo contiene referencia a la izquierda e implementación a la derecha a igual tamaño. Abrir ambas y sus regiones legibles antes de modificar design-qa.md. Los datos reales y las advertencias históricas explican diferencias de contenido respecto de la maqueta.

El script anterior sigue disponible con sus comprobaciones, adaptadas a los nuevos destinos de navegación

```bash
node "$P/visual-operacion.cjs" "$P/evidencia/diseno-20261111/host-operacion-01"
```

Para regenerar un preview nuevo

```bash
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-preview-propuesta1-20261111 \
  --estado "$R/estado-fabrica.json" \
  --preview "$P/evidencia/diseno-20261111/preview-nuevo"
```

Las observaciones privadas permanecen en SQLite. El preview se genera con contratos y fuentes del checkout. Siete archivos host previos no versionados fueron conservados y quedan fuera del commit de esta retoma.

## Recursos y límites

Iconos originales de [Tabler Icons](https://tabler.io/icons), licencia MIT, y fuente [Inter](https://github.com/google/fonts/tree/main/ofl/inter), licencia OFL. Fuentes, commit de la biblioteca y hashes están en `recursos/FUENTES.json`, con los originales y licencias en `recursos/`. Se incrustan desde esos archivos para abrir el panel sin solicitar recursos de red. Las licencias también se conservan dentro del HTML generado.

La estructura y los recorridos locales fueron comprobados en el host. Las 55 pruebas Python, el recorrido nuevo de seis pasos y el recorrido previo de tres casos pasaron. La comparación visual está documentada en design-qa.md. Calendar/Meet, ventas y pagos manuales, canales reales, sala audiovisual completa y permisos conservan las dependencias de su alcance previo. La entrega espera revisión de Sergio y la coordinadora en el punto STOP autorizado.

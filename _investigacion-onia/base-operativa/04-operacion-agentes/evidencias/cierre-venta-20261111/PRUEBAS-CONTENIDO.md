# Comprobación técnica de contenido · 11 nov UTC

Ejecutada en VPS, sin originales de Sergio ni efectos externos.

- Editor: `python3 -B 05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110/pruebas.py --evidencia /tmp/onia-edicion-ventas-20261111.json`, desde base-operativa. Salida: `Ran 12 tests in 40.802s`, `OK`. Incluye ASR offline real de habla sintética. Recibo nuevo en pruebas-ventas-20261111.json.
- Reutilización de ASR por lote: desde carpeta del editor, `python3 -B -m unittest pruebas.EditorTests.test_batch_transcribes_once_for_multiple_pieces -v`. Salida: `Ran 1 test in 2.555s`, `OK`. ASR simulado contado una vez, cuatro renders reales de dos piezas.
- Panel: `python3 -B 05-herramientas/fabrica-contenido/20261109-lector-panel/pruebas.py`, desde base-operativa. Salida: `Ran 22 tests in 0.959s`, `OK`.
- Tanda: `python3 -B -m unittest discover -s 05-herramientas/fabrica-contenido/20261109-lector-panel -p test_tanda.py -v`, desde base-operativa. Salida: `Ran 3 tests in 0.031s`, `OK`. Cubre texto alterado, cinco borradores sin aprobación y no atribuir archivos sin commit a HEAD.

Error de ejecución del coordinador: intentó editar el archivo de prueba con ruta relativa a raíz estando en la carpeta del editor. No editó archivos; el test nuevo todavía no existía. Se corrigió la ruta y se ejecutó el caso con éxito. No es fallo de aplicación ni prueba pasada en ese intento fallido.

Sin grabación real en la cola consultada: la carpeta privada de entrada no existía en esta lectura. Eso no demuestra que Drive esté vacío. No se escuchó ni aprobó material de Sergio; tampoco se probó traslado por Boss ni publicación. Los guiones conservan ensayo/aceptación editorial pendientes.

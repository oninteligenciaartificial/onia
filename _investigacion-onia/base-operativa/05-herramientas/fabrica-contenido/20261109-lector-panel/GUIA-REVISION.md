# Revisar el panel ampliado

Entrega de `cerebro-panel-usable-20261109`, 11 de noviembre de 2026. Base de entrada `7012ca493bfd059a833b8a6cdd77b080b38765d8`, también observada en origin/master al leer ALCANCE-v1. Directora desarrollar-y-verificar anunciada y leída desde su fuente canónica. Alcance actualizado recibido por stdin. Modelo/esfuerzo solicitados Sol6.1 high. Runtime exacto, ID de sesión, número de intento y cuota inicial/final desconocidos en esta ejecutora.

## Abrir y recorrer

Abrir [preview del panel](evidencia/operacion-20261111/preview-final/panel.html) en este checkout. Presenta la tanda histórica v2 cotejada con sus Markdown, el resumen de esta entrega, una tarea marcada ENSAYO SINTÉTICO y una consulta del cerebro por revisión. Los enlaces documentales se resuelven dentro del checkout. El modo interactivo usa el mismo `panel.render` y conserva las entradas de `lector.py` y `tanda.py`.

Desde la raíz del worktree, para usar la revisión local durante la prueba de Sergio

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
R=05-herramientas/fabrica-contenido/20261109-lector-panel
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-panel-revision-sergio-20261111 \
  --estado "$R/estado-fabrica.json" \
  --estado "$R/fixtures/tarea-sintetica/estado-fabrica.json"
```

Abrir la dirección loopback que imprime el comando, desde un navegador en la misma máquina. El servidor escucha en 127.0.0.1, puerto 8765 por defecto. Si está ocupado, elegir otro mediante `--puerto`. Ctrl+C termina la prueba. El cierre de esta entrega dejó sus servidores temporales detenidos. El acceso remoto o desde un teléfono físico necesita un recorrido de acceso autorizado posterior.

1. Entrar a Fábricas y recorrer sus seis enlaces. Guiones presenta la tarea sintética con entrada, resultado, evidencia y revisión pendiente. Cada fábrica que carece de export muestra el pendiente y su siguiente paso. La sección del panel muestra el resumen fechado de esta entrega.
2. En Guiones, abrir la evidencia de un paso. El modo local muestra su texto escapado, ruta, lectura fechada y SHA-256. Volver al panel.
3. En Resultado original v1, desplegar Revisar resultado. Escribir un motivo y una observación y guardar. Debe aparecer la confirmación y una revisión local v1 pendiente. Abrir Original conservado para cotejar los bytes del resultado y la huella de su fuente.
4. Detener con Ctrl+C y repetir el mismo comando con el mismo `--datos`. La revisión v1 debe seguir visible. Registrar otra observación para obtener v2. Una página desactualizada produce un conflicto y conserva el texto enviado para recuperarlo.
5. Abrir Calendario. Debe mostrar 13-nov 20:00, 14-nov 14:00 y 16-nov 20:00, America/La_Paz, con la confirmación del 11-nov y su fuente. La fecha editorial y slots de la tanda se muestran debajo. La tanda v2 conserva los horarios históricos y lleva una advertencia visible.
6. En Cerebro, consultar `revision` y uso `workshop`, o `oferta` y `vender`. Desplegar el pasaje, fuente y límites de un patrón. `tributacion` devuelve una selección vacía. La consulta reutiliza `03-referentes/cerebro-operativo/20261109/consultar.py` y su validación de integridad.
7. En Guiones reales, revisar T01–T05 y sus textos completos. Sus formularios también conservan observaciones por versión. Un export retirado de la selección mantiene sus originales y revisiones en Revisiones de fuentes anteriores.

## Persistencia y contratos

Las observaciones están en `revisiones.sqlite3` dentro del directorio elegido mediante `--datos`, fuera de Git. El archivo nuevo se crea con permisos 0600 y el directorio nuevo con 0700. Para conservarlas entre ejecuciones, reutilizar ese directorio y respaldarlo privadamente. `/tmp` sirve para el ensayo y depende de la política de limpieza del host. La ubicación privada definitiva la decide el operador fuera del repositorio.

Cada fila guarda versión, fecha con zona, motivo, corrección, estado pendiente, ruta y SHA-256 de la fuente y original. En entregables se conserva también el texto del archivo y su hash. Las escrituras usan transacciones SQLite y control de versión esperada. Las filas anteriores permanecen conservadas. Cambiar la fuente o el resultado exige recargar el formulario. La propuesta local queda a disposición de Sergio y la coordinadora para su revisión y aplicación en el productor.

Se consume `onia-fabrica-estado-v1` del ALCANCE mediante `--estado`, repetible, con rutas relativas a base-operativa. Productores permitidos por el contrato actual

- `guiones` bajo `05-herramientas/fabrica-onia/1-guiones-calendario/`.
- `whatsapp` bajo `05-herramientas/fabrica-onia/4-chatbot-whatsapp/`.
- `panel` bajo esta ruta asignada.

Cada export declara su propia fecha, pasos, evidencias, entregas, fuente y pendientes. Las referencias documentales deben quedar dentro de la raíz de su productor. Los fixtures del panel usan una raíz exclusiva etiquetada en pantalla. Se admiten varios exports explícitos de un productor. Una entrada inválida queda visible como error y las entradas válidas siguen disponibles.

Para consumir las entregas de los productores paralelos, añadir sus rutas existentes con `--estado` y seleccionar su nuevo `guiones-panel.json` con `--tanda`, relativo a base-operativa y dentro de `1-guiones-calendario/salida/`. Se mantienen cinco IDs T01–T05, cotejo de texto/hash/bytes con sus Markdown y anclaje Git cuando corresponde. El cambio mínimo de `tanda.py` toma la versión declarada o el nombre de la carpeta para identificar nuevas tandas. Las tres regresiones anteriores siguen pasando.

Las rutas se validan antes de leer. URLs, rutas privadas, travesías y enlaces simbólicos producen rechazo. Los documentos del servidor se seleccionan por un ID de una lista construida desde referencias validadas. El lector público conserva su catálogo original cerrado y sus garantías de procedencia. Los POST requieren origen loopback, token de sesión, huella del original y versión. El HTML escapa textos y conserva CSP con recursos externos bloqueados.

Para generar otro preview estático en un directorio nuevo

```bash
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-panel-preview-20261111 \
  --estado "$R/estado-fabrica.json" \
  --estado "$R/fixtures/tarea-sintetica/estado-fabrica.json" \
  --preview "$P/evidencia/preview-nuevo"
```

El preview se construye a partir de contratos y fuentes del checkout. Las observaciones privadas se consultan en el modo local. La vista estática remite a esta guía para abrir los formularios.

## Comprobación reproducible

```bash
python3 -B "$P/pruebas.py"
python3 -B -m unittest discover -s "$P" -p 'test_*.py' -v
node --check "$P/visual-operacion.cjs"
git diff --check
```

Resultado local de esta entrega, registrado en [pruebas.txt](evidencia/operacion-20261111/pruebas.txt)

- Lector/panel original, 22/22.
- Tanda original, 3/3.
- Ampliación, 23/23. Incluye contrato de productor futuro reificado en un directorio temporal, entradas inválidas, escape de rutas, symlinks, HTML/XSS y SQL como texto, Unicode al máximo admitido, origen/CSRF, conflicto de versión, concurrencia, cambios del archivo original, recorrido HTTP, reinicio de servidor y SQLite, v1/v2 y recuperación de fuentes retiradas.
- Sintaxis Python mediante AST, sintaxis Node y diff comprobados.

El [recorrido desde la CLI](evidencia/operacion-20261111/recorrido-cli.json) también terminó un proceso Python y abrió otro sobre la misma SQLite, recuperando propuesta v1 y original con HTTP 200.

El recorrido completo probado usa una tarea ENSAYO SINTÉTICO. Los T01–T05 de la tanda v2 son archivos editoriales existentes verificados durante las pruebas. El ensayo comprueba la preparación y revisión local de resultados.

Para repetir el ensayo de navegador en un host compatible, usando el Playwright/Chromium ya existente y un destino nuevo

```bash
node "$P/visual-operacion.cjs" "$P/evidencia/visual-operacion-nueva"
```

El script prepara SQLite sintética fuera de Git, inicia su servidor temporal, prueba navegación, evidencia, guardado y reinicio, consulta el cerebro y captura 1440×1000 y 390×844. Cierra servidor y navegador al terminar. En esta sesión Chromium falló antes de abrir una página por `No usable sandbox!`. [Recibo del intento](evidencia/operacion-20261111/visual/resultado.json). Capturas e inspección visual del panel ampliado pendientes en un host compatible.

## Dependencias y revisión pendiente

Los exports nuevos de Guiones y WhatsApp estaban ausentes en este checkout. La consulta admite sus contratos cuando la coordinadora reúna las entregas. Edición, Automatizaciones, Código y Plataforma conservan documentación de origen y el pendiente de recibir un resumen validado. La sala audiovisual completa corresponde a los pasos posteriores del alcance.

Calendar/Meet necesita conciliación con los horarios confirmados. La conexión real de WhatsApp/Meta/n8n, QR privado, pagos, clientes, publicación y ejecución desde Boss después del corte del 14 conservan sus pruebas y responsables pendientes. El calendario mostrado usa la confirmación documental del 11-nov. La ubicación definitiva de datos privados y el acceso desde el dispositivo de Sergio quedan por elegir y probar.

Sergio y la coordinadora revisan la rama publicada y su hash comunicado por la ejecutora. La entrega queda en el punto STOP autorizado para esta primera tanda.

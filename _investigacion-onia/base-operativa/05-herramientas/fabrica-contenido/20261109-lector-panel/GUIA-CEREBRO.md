# Cerebro, correcciones y estrategias

Corrección de revisión de `cerebro-panel-usable-20261109` sobre `b8019ec4480caf5ba83b1d7b654422d058ac5792`. La implementación anterior partió de `624529cc33128c3c2aac60a052bc437be455215f`. Se conserva Propuesta 1, el consumidor del flujo diario 9a4639f y la entrega aceptada 94cca9b. Directora desarrollar-y-verificar leída. Modelo solicitado Sol high, cero hijos. Runtime y cuota atribuibles a esta retoma desconocidos. La coordinadora mantiene tareas, decisiones e integración.

## Correcciones de la revisión independiente

Las tres regresiones reprodujeron el fallo sobre b8019ec antes de aplicar el cambio. El consumidor exige S01 en fuentes.json y en el índice de fuentes, además de cotejar su ruta, bytes y SHA-256 con la decisión comercial vigente. Omitir esa fuente completa rechaza el export.

La huella de cada sección incorpora una copia de los datos mostrados de fábricas, pasos, entregables, pendientes, errores, tanda, flujo diario y estrategias. Un cambio de esos datos exige recargar el formulario. Se excluye la hora generada por la consulta de tanda.snapshot para permitir guardar mientras el contenido permanece igual. La invalidación es común a las secciones y permite detectar cambios de contexto entre vistas.

La fila de autoría concilia la tabla inicial con el apartado posterior Agregado 08:22 de la misma fuente. Muestra Codex hasta el viernes 13, Contenido como editor y la redacción de Contenido desde el sábado 14. Ambos períodos se leen del documento y conservan su procedencia. StrategyTests ejecuta Git desde la raíz resuelta por lector.REPO y funciona desde la subcarpeta del producto.

## Qué abrir

[Preview del cerebro](evidencia/correccion-cerebro-20261111/preview/panel.html). Contiene consulta documental de referentes, decisiones vigentes, reglas aprobadas documentadas, fuentes/fecha/hash, estrategias pendientes de integrar y las vistas de capacidades. Los datos de las revisiones privadas se consultan en el servidor temporal. La [validación estructural del preview](evidencia/correccion-cerebro-20261111/preview-validacion.json) comprobó 97 enlaces y 47 anclas únicas, sin formularios privados ni scripts.

Desde la raíz del checkout

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
R=05-herramientas/fabrica-contenido/20261109-lector-panel
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-cerebro-revision-20261111 \
  --estado "$R/estado-fabrica.json"
```

Abrir la URL loopback impresa en un navegador de la misma máquina. Ctrl+C termina el proceso. El directorio `--datos` debe conservarse para recuperar observaciones y versiones. `/tmp` sirve para ensayos y depende de la limpieza del host. La ubicación operativa persistente la prepara la coordinadora fuera de Git.

El argumento existente `--flujo /ruta/privada/panel.json` conserva el consumidor del ciclo diario, su caché del último válido y la actualización con CSP por hash. Esa ruta debe corresponder al productor saneado real. El servidor conserva los argumentos `--tanda` y `--estado` para exports explícitos validados.

## Recorrido de revisión

1. En Cerebro, leer Decisiones de negocio vigentes, Fuentes y versiones y Reglas aprendidas y aprobadas. Abrir una fuente y cotejar la huella. Las reglas del catálogo de referentes conservan su carácter de propuestas revisables. La consulta reutiliza `consultar.py` y sus comprobaciones de integridad.
2. Buscar tema `revision`, uso `workshop`, para recuperar patrones con pasajes y comprobaciones. La selección documental y sus límites quedan explícitos. Se consulta conocimiento documentado de OnIA.
3. Desde cualquier sección disponible, pulsar Corregir esta sección. La pantalla Correcciones presenta el objetivo, versión/huella, motivo, propuesta y alcance. Las piezas de guion también mantienen su acceso Revisar resultado.
4. En T01, proponer un texto completo de ensayo y elegir alcance Esta pieza. Guardar conserva una sugerencia pendiente y su original. El mismo envío repetido conserva una única observación. Reutilizar el ID con otra propuesta produce conflicto visible y conserva el texto enviado.
5. Revisar la propuesta y pulsar Crear versión local pendiente. Se crea un resultado privado nuevo con antes/después, fecha, motivo y SHA-256. Su vista previa indica revisión pendiente. El original permanece conservado. Una nueva observación posterior o una huella distinta exige recargar antes de aplicar.
6. Detener y arrancar con el mismo `--datos`. La versión local reaparece en Correcciones y se puede corregir de nuevo para generar otra pieza. Las aplicaciones repetidas conservan la misma versión creada.
7. Para un cambio de precio, horario, rol o trabajo con modelo, elegir alcance Decisión canónica o Trabajo con LLM. Después de guardar, Exportar solicitud a coordinadora produce un JSON con ID estable, objetivo, original, motivo, propuesta, versión/hash y dependencias. Su estado permanece pendiente de coordinación. La coordinadora resuelve la decisión y el encargo aplicable.
8. En Estrategias, consultar el estado del contrato. En Anuncios y canales, abrir las capacidades y dependencias documentadas. Los borradores A01/A02/VSL01 se enlazan cuando existe un export de estrategia válido. La operación comercial y de canales debe tener su evidencia propia.

Las versiones locales y solicitudes se guardan en la misma SQLite privada que las observaciones anteriores. La migración conserva las nueve columnas originales y añade alcance y control de reintento. Las nuevas tablas conservan versiones y solicitudes mediante transacciones e identificadores únicos. Los formularios mantienen CSRF, Host/Origin exactos, versión y huella, límites de texto y escape HTML. Los botones ejecutan operaciones fijas de revisión y creación de versiones.

## Estrategias y coordinación

Se leyó la entrega publicada `19e2d7dc71db6c00c4e5c1e60239b9419b4f7bed` de `codex/ws-guiones-tanda-estrategias-20261111`, incluyendo CONTRATO.md, esquema, export y fuentes. Los archivos todavía estaban ausentes en este checkout al preparar la entrega. El panel muestra ese pendiente y conserva la raíz del productor.

El adaptador consume `01-negocio/estrategias-operativas-20261111/export-estrategias-v1.json`, schema `onia-estrategias-v1`, junto con `estrategias.schema.json` y `fuentes.json`. Se amplió el mapa exclusivamente al productor `estrategias` bajo esa raíz. La estrategia del workshop conserva borrador preparado; las futuras propuestas conservan propuesto, sus acciones, piezas, evidencia y fuentes. Los valores desconocidos de métricas permanecen desconocidos.

Se valida el esquema local con jsonschema ya disponible. Las referencias de esquema que pudieran requerir resolución externa se rechazan. S01 es obligatoria y debe coincidir con la decisión vigente. Las fuentes técnicas modificadas se muestran pendientes de conciliación, sin rehacer las huellas del productor. Las piezas se cotejan con el Markdown declarado. Una ruta fuera de raíz, aprobación inventada, precio o fecha divergentes bloquea la adopción del export.

[Contrato de coordinación](CONTRATO-COORDINACION.md). El comprobador histórico del productor presupone que el mapa del panel rechaza esta raíz; su expectativa necesita actualización por su escritora cuando se integren los productos. Su evidencia anterior conserva su alcance.

## Acceso privado preparado para VPS

El modo predeterminado sigue escuchando en loopback y exige su Host/Origin exactos. `--acceso` habilita únicamente el origen HTTPS configurado y autenticación Basic con contraseña derivada PBKDF2-SHA256, sal aleatoria y comparación constante. La configuración debe estar fuera de Git, ser un archivo privado 0600 y carecer de symlinks. Los encabezados X-Forwarded-Host y X-Forwarded-For no participan en la decisión de confianza. [RFC 7617](https://www.rfc-editor.org/rfc/rfc7617), [hashlib de Python](https://docs.python.org/3/library/hashlib.html#hashlib.pbkdf2_hmac)

La coordinadora necesita elegir el dominio privado y el proxy TLS autorizado. Preparar previamente un directorio privado fuera de Git y generar la configuración con contraseña introducida en el terminal, sin argumentos de contraseña ni tokens en logs

```bash
python3 -B "$P/acceso.py" \
  --crear /ruta/privada/onia-panel/acceso.json \
  --origen https://panel.ejemplo.invalid \
  --usuario operador
```

Sustituir dominio y ruta por los autorizados. La contraseña requiere al menos 24 caracteres y hasta 1000 bytes. La herramienta conserva sólo sal y derivación. `despliegue/acceso.example.json` es una plantilla inválida hasta generar la configuración privada.

Arranque preparado para el proxy privado

```bash
python3 -B "$P/servidor.py" \
  --datos /ruta/privada/onia-panel/datos \
  --acceso /ruta/privada/onia-panel/acceso.json \
  --estado "$R/estado-fabrica.json" \
  --puerto 8765
```

El backend escucha sólo en 127.0.0.1. El proxy TLS debe conservar el Host exacto del origen configurado y la cabecera Authorization. El navegador envía Origin del mismo origen HTTPS. El modo privado rechaza solicitudes con otros Host, incluso el loopback directo. Para diagnóstico local se inicia explícitamente el modo predeterminado en otro ensayo con datos de prueba.

La [plantilla de servicio deshabilitada](despliegue/onia-panel.service.disabled) usa rutas de instalación estables `/srv/onia`, datos `/var/lib/onia-panel` y credenciales `/etc/onia-panel/acceso.json`. La coordinadora adapta esas rutas y el propietario antes de instalar. El servicio no está instalado ni activo por esta entrega. Reiniciar debe reutilizar los mismos datos y configuración. Comandos de operación para una instalación privada que ya se haya aprobado y preparado

```bash
systemctl restart onia-panel
systemctl status onia-panel
```

El operador comprueba después autenticación, una versión local previa y la última proyección diaria válida. La prueba de teléfono real, TLS/proxy y supervivencia del servicio corresponde a coordinadora/Sergio y sigue pendiente. El ensayo HTTP simula las cabeceras de ese proxy y prueba su control de acceso. Las credenciales y sus valores no se registran en el recibo.

## Comprobaciones reproducibles

```bash
python3 -B "$P/pruebas.py"
python3 -B -m unittest discover -s "$P" -p 'test_*.py' -v
(cd "$P" && python3 -B -m unittest test_cerebro.StrategyTests -v)
python3 -B "$P/evidencia/correccion-cerebro-20261111/recorrido-cli.py"
node --check "$P/visual-cerebro.cjs"
node --check "$P/visual-diseno.cjs"
node --check "$P/visual-operacion.cjs"
git diff --check
```

La entrega anterior conserva sus 76 comprobaciones y su recibo. La corrección añade tres regresiones y ejecutó 79 comprobaciones Python, incluyendo lector 22, tanda 3, operación 23, diseño/origen 7, diario 6 y cerebro 18, sin omisiones. StrategyTests pasó sus cinco casos también desde la subcarpeta del producto. El ensayo CLI guardó y aplicó con reintento, reinició en un proceso nuevo, recuperó la versión privada y exportó una solicitud canónica pendiente. Los comandos, salidas y hashes están en el recibo de esta corrección. [Pruebas](evidencia/correccion-cerebro-20261111/pruebas.txt), [recorrido CLI](evidencia/correccion-cerebro-20261111/recorrido-cli.json), [recibo](evidencia/correccion-cerebro-20261111/RECIBO.json).

La prueba del contrato publicado requiere el commit del productor en los objetos Git. Si falta, la suite declara la omisión de esa dependencia.

El ensayo de navegador preparado usa Playwright/Chromium existente con sandbox real

```bash
node "$P/visual-cerebro.cjs" "$P/evidencia/correccion-cerebro-20261111/host-02"
```

Ejecuta vistas de cerebro/estrategias en 1440×1000 y 390×844, comprueba la autoría conciliada, guardado, aplicación local, reinicio y solicitud canónica. Registra el commit del checkout y los hashes del código. Cierra servidor y navegador y conserva SQLite sintética fuera de Git.

La coordinadora ejecutó el navegador sobre b8019ec con sandbox real y cinco casos aprobados, incluyendo persistencia tras reinicio. Se incorporan su JSON y cinco capturas, abiertas durante esta retoma. La imagen de cerebro de esa versión muestra la fila de autoría que corrige esta entrega. Las capturas tienen procedencia y hashes propios. [Evidencia host de b8019ec](evidencia/cerebro-20261111/host-coordinadora-01/PROCEDENCIA.json).

El intento de navegador del código corregido volvió a fallar antes de renderizar por No usable sandbox!, con cero capturas nuevas. La coordinadora debe ejecutar el comando anterior sobre la entrega corregida y abrir sus capturas. El recibo del intento conserva los hashes del código exacto. [Intento de la corrección](evidencia/correccion-cerebro-20261111/intento-browser-01/resultado.json).

Para regenerar un preview en un directorio nuevo

```bash
python3 -B "$P/servidor.py" \
  --datos /tmp/onia-cerebro-preview-20261111 \
  --estado "$R/estado-fabrica.json" \
  --preview "$P/evidencia/cerebro-20261111/preview-nuevo"
```

El preview usa contratos y fuentes del checkout y excluye observaciones/versiones privadas. La entrega conserva las siete evidencias host previas sin versionar y fuera de su commit. Al finalizar, la ejecutora publica exclusivamente su rama y la coordinadora recoge el commit para revisión e integración.

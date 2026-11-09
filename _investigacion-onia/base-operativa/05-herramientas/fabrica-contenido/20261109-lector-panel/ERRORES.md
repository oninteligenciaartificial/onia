# Errores y límites de esta entrega

- Lecturas agrupadas largas excedieron el límite de salida. Se recuperaron por separado los contratos, diseño, README Telegram, ambos guiones, manifiesto y recibo de revisión usados. No se atribuye lectura integral a un volcado truncado.
- Chromium1252 no arrancó dentro del sandbox de esta ejecutora: `No usable sandbox`, perfil `bwrap//&unpriv_bwrap (enforce)`, `NoNewPrivs=1`, `Seccomp=2`, sin capacidades efectivas. El perfil AppArmor del navegador instalado en el host no acredita que esta sesión pueda transicionar a él. También hubo intentos de Crashpad contra configuración de sólo lectura; no se accedió a cuentas ni se escribió allí.
- Se conserva el intento en `evidencia/visual-01/resultado.json`, junto con fixtures HTML/JSON largo, vacío y error. No hay PNG ni inspección visual aprobada. Queda pendiente el criterio 5, con comando y condición de salida en README. No se desactivó sandbox ni se modificó seguridad del VPS para suplirlo.
- Los 17 controles sin red pasaron en la primera ejecución, incluido fallo HTTP403 por fuente, timeout real por alarma, tamaño excedido, respuesta insegura y alteración de guion/evidencia en memoria. Los fallos inyectados no se presentan como fallos de las fuentes públicas reales.
- `git diff --cached --check` encontró un espacio final en el texto sintético largo. Se normalizaron sólo ese fixture y su generador; el recibo del fallo Chromium y el snapshot público real se conservaron intactos. No se repitió el navegador porque su condición de arranque no cambió.

Registro sólo dentro de la ruta asignada; no modifica el registro de errores global, el JSON de tarea ni el briefing del coordinador.

## Retoma: tercera fuente y prueba de host

- Se corrigió la falta de noticia: F06 se releyó públicamente y conserva publicación/anuncio 5/11/2026 cotejados en metadato y texto visible. Sigue candidata no elegida para guiones; no se atribuyen funciones Enterprise a Free. Las dos guías y la lectura anterior se conservan.
- Pasaron 22 pruebas sin red. La sanitización y la lista cerrada incluyen ahora sólo ese artículo concreto de claude.com; fecha ausente/discrepante y fallo material no se completan por inferencia.
- El coordinador ejecutó la solicitud final con hashes coincidentes, Chromium1252 y sandbox en el host. Escritorio pasó; móvil falló por desborde horizontal, rc1. La ejecutora inspeccionó la única captura de escritorio con `view_image`: la jerarquía y fuentes están visibles, pero hashes largos del próximo paso canónico salen de una tarjeta. El chequeo global de escritorio no detecta desborde interno. Los otros tres casos no se ejecutaron.
- Se preservó código/snapshot/HTML de la solicitud; no se repitió navegador ni se exportaron capturas del intento con rc1. Se conserva recibo público propio, con hash de imagen inspeccionada. Coordinación indicó cerrar parcial y preparar otra corrección acotada. Criterio 5 sigue pendiente; no se declara aceptación visual.

## Corrección final del desborde

- El coordinador localizó el desborde en el párrafo de próximo paso canónico: un hash largo no se partía. Se cotejó su propuesta con `diff`: sólo añadió `overflow-wrap:anywhere` a `body`. Se aplicó ese cambio sin ocultar contenido ni cambiar datos.
- Se creó `panel-corregido-01`: snapshot idéntico al de lectura-real-02 y HTML regenerado sin red. Las 22 pruebas Python pasaron. Los recibos anteriores, incluido el fallo, permanecen intactos.
- El host ejecutó la solicitud v2 final con hashes coincidentes: cinco casos OK, sandbox activo, perfil sintético propio y navegador cerrado. Esta ejecutora inspeccionó los cinco PNG autorizados. El texto largo permanece dentro de tarjetas; los casos vacío/error conservan fallos explícitos. Las imágenes móviles muy altas se reducen en el visor; no se atribuye lectura fina de todos sus caracteres.
- La prueba de navegador fue del coordinador/host, no de bwrap. La verificación del artefacto no acepta la tarea canónica ni autoriza publicaciones. No se modificaron las fuentes después de capturarlas.

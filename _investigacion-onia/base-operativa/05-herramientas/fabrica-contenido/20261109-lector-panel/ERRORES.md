# Errores y límites de esta entrega

- Lecturas agrupadas largas excedieron el límite de salida. Se recuperaron por separado los contratos, diseño, README Telegram, ambos guiones, manifiesto y recibo de revisión usados. No se atribuye lectura integral a un volcado truncado.
- Chromium1252 no arrancó dentro del sandbox de esta ejecutora: `No usable sandbox`, perfil `bwrap//&unpriv_bwrap (enforce)`, `NoNewPrivs=1`, `Seccomp=2`, sin capacidades efectivas. El perfil AppArmor del navegador instalado en el host no acredita que esta sesión pueda transicionar a él. También hubo intentos de Crashpad contra configuración de sólo lectura; no se accedió a cuentas ni se escribió allí.
- Se conserva el intento en `evidencia/visual-01/resultado.json`, junto con fixtures HTML/JSON largo, vacío y error. No hay PNG ni inspección visual aprobada. Queda pendiente el criterio 5, con comando y condición de salida en README. No se desactivó sandbox ni se modificó seguridad del VPS para suplirlo.
- Los 17 controles sin red pasaron en la primera ejecución, incluido fallo HTTP403 por fuente, timeout real por alarma, tamaño excedido, respuesta insegura y alteración de guion/evidencia en memoria. Los fallos inyectados no se presentan como fallos de las fuentes públicas reales.
- `git diff --cached --check` encontró un espacio final en el texto sintético largo. Se normalizaron sólo ese fixture y su generador; el recibo del fallo Chromium y el snapshot público real se conservaron intactos. No se repitió el navegador porque su condición de arranque no cambió.

Registro sólo dentro de la ruta asignada; no modifica el registro de errores global, el JSON de tarea ni el briefing del coordinador.

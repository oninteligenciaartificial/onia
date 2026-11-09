# Prueba visual portable del panel ficticio

Corrección solicitada sobre la entrega `17a87d7c919439015402475b64fcc1606e3909e3` tras el veredicto independiente `cambios` aportado en el briefing de continuidad. Se incorporan exclusivamente este recibo y la captura, sin editar ni regenerar los archivos de la entrega anterior.

## Archivo y procedencia

- [panel.png](panel.png): PNG sintético propio de 1440 × 1080 píxeles, 63.135 bytes.
- SHA-256 exigido por el briefing y comprobado sobre origen y copia: `1e6d593992b26df2438663a48770009e3ed07e3001269cbdaefe4e96da6ad50b`.
- Origen autorizado de lectura: `/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/04-operacion-agentes/evidencias/fabrica-contenido-diseno-20261108/panel-inspeccionado.png`.
- Copia byte a byte con creación exclusiva del destino, sin borrar ni modificar el origen. El revisor puede abrir ahora el PNG desde esta carpeta del commit; no necesita acceso al checkout coordinador.
- HTML cotejado: [ensayos/ejecucion-02/panel.html](../ensayos/ejecucion-02/panel.html), SHA-256 `04ec69b5ca4e3c64bd1a1765011dcf16df6bb040270909f87482d6e6b1f0a208`.

## Inspección efectuada y cotejo

La ejecutora abrió la copia mediante `view_image` en esta retoma y observó la captura completa. El título, la advertencia de ficción, el ID, el estado, las decisiones y el siguiente paso son legibles, sin solapamientos ni texto cortado en esta imagen. La captura no muestra cuentas ni credenciales. Se inspeccionó una imagen estática recibida; no se inició navegador, servidor ni una nueva captura.

| Texto visible | Fuente cotejada | Resultado |
|---|---|---|
| «FICTICIO · sin conexión · sin envíos · sin autenticación» | HTML y carácter sintético del ensayo | Coincide; no presenta autenticación operativa. |
| `ficcion-fabrica-001`, revisión `12`, `para_revision` | [JSON aislado](../ensayos/ejecucion-02/04-operacion-agentes/tareas/ficcion-fabrica-001.json) | Coincide con `id`, `revision` y `estado`. |
| `guion-a-v1: elegir_para_preparar` | Primera decisión canónica del ensayo y su recibo referenciado | Coincide; autor `Sergio SIMULADO`. |
| `guion-b-v1: pedir_cambios` | Segunda decisión canónica del ensayo y su recibo referenciado | Coincide; autor `Sergio SIMULADO`. |
| 2 fuentes utilizables, 1 duplicado, 1 pendiente, 1 fallo | [ingesta.json](../ensayos/ejecucion-02/04-operacion-agentes/evidencias/ficcion-fabrica-001/ingesta.json) | Longitudes comprobadas: `2, 1, 1, 1`. |
| Decisiones simuladas; encargo real sin aceptar | JSON aislado: `aceptacion=null` | Coincide; la captura no acredita aceptación real. |
| Revisión real por coordinador; Telegram/panel/scheduler sin integración | `proximo_paso` del JSON aislado | Coincide. |

Además se importó `trabajo.py` con generación de bytecode deshabilitada y se ejecutaron `read_task` y `verify` sobre la base aislada, sólo en lectura: integridad correcta de las evidencias y las fuentes de decisión. Se comprobaron los hashes del fixture y de `trabajo.py` contra el [resultado existente](../ensayos/ejecucion-02/resultado.json): coinciden.

## Se conservan los seis controles anteriores

El recibo existente sigue indicando `resultado=OK` y seis controles: ingesta/duplicado, revisión obsoleta, decisión en entrega cerrada, decisión duplicada, revisión y decisiones por guion, y evidencia alterada en memoria. No se reejecutó ni regeneró el ensayo; se verificaron su recibo y su integridad sin modificar bytes. El README anterior describe el alcance de la entrega inicial: esta evidencia nueva añade ahora la inspección visual de la captura recibida, sin reescribir aquel informe.

Continúa siendo un ensayo offline: sin Telegram, autenticación, scheduler, ingestión real, envíos, API paga, n8n ni producción. La imagen no demuestra interacción, acceso móvil o servicio activo. Euge Oller sigue pendiente de evidencia visual pertinente; este PNG sólo corresponde al panel sintético y no acredita visionado de ese video. No se abrió otra tarea, sesión o subagente. El coordinador conserva cierre, nueva revisión independiente y eventual integración; esta ejecutora conserva el worktree y publica sólo su rama asignada.

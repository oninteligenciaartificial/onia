# T011-N8N — Auditoría y preparación

Finalizado: 2026-11-07T18:29:01.349953+00:00. No se ejecutó ningún workflow, comando remoto, activación, desactivación o borrado. No se modificaron tareas/ ni registro.tsv; los gestiona el runner.

## Radar YT — lectura solamente

- Ejecución 79276: 2026-11-04 11:45 UTC, success; SSH 25,373 s, code=0, signal=null, stderr vacío. stdout JSON válido: ok=true, dryRun=false, found=50, pool=24, proposed=5, inserted=5, notify=true.
- Ejecución 75824: 2026-10-28 11:45 UTC, success; SSH 21,737 s, code=0, signal=null, stderr vacío. Mismos contadores y banderas.
- Diez ideas con título, formato, hook, fuente y clave; formatos Reel/Carrusel/Short. No hay títulos ni idea_key idénticos en esta muestra. Las dos fuentes ifny_ep4nO8 y 7Z-vRvIUqNs se reutilizan entre semanas: 2 de 5 fuentes de la semana más reciente. Hay reiteración temática de WhatsApp/chatbots y automatización, con hooks genéricos y poco detalle accionable.
- El título «Automatiza tu negocio sin código con ONIA: caso real antes y después» afirma un caso real que estos datos no prueban. «Gratis», «vender ... 24/7» y otras promesas requieren revisión editorial; las visitas no prueban resultados de ONIA. No se verificaron videos, destinos de inserción ni resultados comerciales.
- No se observan fallos declarados en stdout/stderr. El éxito de n8n no valida el significado de stdout: solo hay Schedule → SSH. notify=true no tiene consumidor; JSON inválido, ok=false, inserciones parciales o un código remoto no cero pueden quedar sin alerta. RADAR_LIMIT=6 con 5 propuestas no demuestra fallo: puede ser un máximo.

## Propuesta de alerta YT — NO aplicada

Añadir «Validar resultado Radar YT» (Code) después de SSH, «¿Fallo Radar YT?» (IF) y «Avisar fallo Radar YT» (Telegram). Code parsea stdout y marca fallo si code !== 0, signal no nula, stderr no vacío, JSON inválido, ok !== true, dryRun !== false, contadores no enteros/no negativos, proposed !== ideas.length, inserted < proposed, o claves/fuentes repetidas dentro del lote. proposed=0 con found>0 debe generar advertencia para revisión, no afirmar automáticamente un fallo. Alertar con ID de ejecución, motivo, code y extracto limitado/escapado de stderr; no enviar la salida completa ni credenciales.

Para fallos de conexión/infraestructura que impiden llegar a Code: proponer workflow separado Error Trigger → Telegram y asociarlo como errorWorkflow de YT, con aviso del nodo y ejecución fallidos. Esto requiere una edición futura autorizada de YT. La repetición entre semanas requiere un historial persistente de source_url/idea_key; no se resuelve con una comprobación local del lote.

## Radar IA — backup y cambios exactos

Backup completo previo al PUT: `/home/onia-codex-worker/operacion/resultados/backups-n8n/QGXVyRSgrArxfolj-20261107T182815Z.json`.

| Nodo/campo | Antes | Después |
|---|---|---|
| settings.timezone | Ausente | America/La_Paz |
| Correr Radar IA (VPS) / parameters.command | `bash /opt/onia/ai-news-radar-run.sh` | `timeout --signal=TERM --kill-after=30s 110m flock --nonblock --conflict-exit-code 75 /opt/onia/.ai-news-radar-n8n.lock bash /opt/onia/ai-news-radar-run.sh` |
| Enviar a Sergio / parameters.text | `={{ $json.text }}` | `={{ String($json.text ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;") }}` |

El escape se aplica en el único nodo Telegram, sobre toda la cadena dinámica y en orden & → < → >. parse_mode sigue HTML. El texto de entrada ya estaba limitado a 3900 caracteres; aun expandido a entidades representa el mismo texto visible. Se verificó la expresión por inspección; no se envió ningún mensaje.

El comando usa un lock de archivo exclusivo no bloqueante, específico de este radar, mantenido por flock mientras corre bash. Una segunda invocación que use el mismo lock sale con código 75. timeout termina tras 110 minutos y fuerza KILL 30 segundos después, por debajo de dos horas; timeout normalmente retorna 124. No se eligió staticData porque leer/escribir una bandera no ofrece exclusión atómica fiable entre ejecuciones. No se borrará el archivo lock: la exclusión depende del descriptor, no de su existencia.

Limitaciones: no se comprobó en VPS la disponibilidad de timeout/flock ni permisos de creación del lock, pues no se autorizaron ejecuciones remotas en esta revisión. Si faltan, el comando falla antes de lanzar el script. El lock cubre invocaciones que empleen esta misma ruta; otras llamadas directas al script y procesos que se desacoplen requieren coordinación adicional. Una caída de transporte SSH exige revisar el comportamiento remoto antes del encendido. El parser existente notifica stdout vacío/no JSON, pero no inspecciona code/stderr cuando hay JSON válido: se conserva sin cambios; conviene aplicar la validación propuesta también a IA en otro encargo.

PUT limitado a name, nodes, connections y settings; staticData no se envió porque era null. No se incluyó active. Readback coincide exactamente con el payload. YT conserva nodes, connections, settings y updatedAt respecto a la lectura inicial.

## Estado final leído de la API

- ynNMGtW8TCDCBMdS: active=true.
- QGXVyRSgrArxfolj: active=false.

Evidencias completas: yt.json, yt-executions.json, ia.json, put-payload.json, put-response.json, ia-final.json y yt-final.json en resultados/T011-N8N/.

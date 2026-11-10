# Puente Boss–Codex: implementación del piloto

10 noviembre 2026. ID canónico: [conexion-boss-codex-20261110](../../tareas/conexion-boss-codex-20261110.json).
Implementa la elección de [Boss v2](REVISION-BOSS-v2.md). No acredita todavía la conexión completa.

## Alcance

SSH restringido → `harness_boss.py` → harness existente → registro único. El cierre publica una instantánea del registro en master y envía un aviso al webhook. Boss verifica esa instantánea y responde en GitHub. No hay scheduler, otro panel ni actualización automática del adaptador desde GitHub.

El aviso al cerrar informa **para_revision**, no aceptación. Su `commit` identifica la instantánea del registro publicada en master; el commit del producto sigue en `cierre.commit` y puede estar aún en su rama. Integración del producto, revisor distinto y aceptación son pasos posteriores. Un HTTP 200 significa recepción HTTP; sólo la respuesta de Boss vinculada al ID, revisión y commit prueba el acuse.

## Archivos y controles

- `05-herramientas/scripts/harness_boss.py`: protocolo JSON, IDs habilitados, permiso local por encargo y asignación, caducidad, intentos, revisión esperada y diario persistente antes de cada efecto.
- `harness_retorno.py`: publicación limitada al registro y sus evidencias propias mediante índice privado; push sin force; validación de revisión, hashes y fuentes en master antes del POST.
- `harness.py`: `cerrar --retorno-boss` y `notificar-boss`. Son optativos para tareas habilitadas; no notifican trabajos anteriores ni simulaciones.
- `harness_sesiones.py`: conciliación por ID y comprobación de revisión/alcance; conserva los tres cupos globales. En consultas Git desactiva hooks, fsmonitor y filtros del repositorio principal; rechaza submódulos antes de inspeccionar el worktree.
- `entrada-boss.sh`: plantilla de comando forzado con entorno limpio, Python aislado y límite de 300 s. Instalada con ruta absoluta a una versión fija.
- `configurar-retorno-boss.{sh,py}`: carga interactiva oculta de URL/clave en el VPS. No envía nada al configurarla.
- `test_harness_boss.py`: autorización, concurrencia, reintentos, publicación, secretos y transporte HTTP simulado. El resultado final de las pruebas e instalación va en `INSTALACION-v1.md`.

Se conserva el worktree de las tareas del puente. No se borran ramas, archivos ni evidencia. El cambio de Git evita ejecutar filtros conocidos durante la inspección; **no constituye aislamiento frente a cualquier proceso del mismo usuario**, ni restringe en el servidor Git las ramas que sus credenciales pueden escribir.

## Protocolo de Boss

Usar su destino SSH y llave dedicada ya existentes; BatchMode y host key estricta. No enviar shell, flags del modelo, rutas, prompts ni credenciales.

```sh
printf '%s\n' '{"version":1,"operacion":"consultar","id":"conexion-boss-codex-20261110"}' |
  ssh -T -o BatchMode=yes -o StrictHostKeyChecking=yes -i "$LLAVE_BOSS" "$DESTINO_BOSS" onia-harness-v1
```

`consultar` y `entrega` devuelven un resumen saneado, sin conciliar ni cambiar el registro. Entrega completa y evidencias se leen en GitHub. Cada escritura requiere los cinco campos exactos:

```json
{"version":1,"operacion":"ejecutar","id":"conexion-boss-piloto-20261110","solicitud":"boss-piloto-inicio-01","revision_esperada":2}
```

Operaciones posibles: `ejecutar`, `reanudar`, `cerrar`, `revisar`, `recoger`, `notificar`. No hay `aceptar`, creación de tareas ni concesión remota de permisos. El número de revisión se obtiene antes por consulta; el ejemplo no acredita un permiso activo.

Repetir exactamente una solicitud terminada devuelve su resultado sin ejecutarla de nuevo. Una operación interrumpida o incierta bloquea nuevas mutaciones de esa tarea, incluso con otro identificador de solicitud. No cambiar el nonce para eludir el bloqueo. Coordinador concilia proceso, registro, commit y log antes de reanudar. El reintento de Codex usa el session ID previo.

## Permisos y secreto locales

Directorio `~/operacion/puente-boss` modo 700; JSON privados modo 600. La instalación copia los módulos desde un commit revisado a `releases/<sha>`. Un push posterior no cambia esa versión.

`config.json` fija base canónica, operación, IDs de lectura y `pausado`. `permisos/<id>.json` requiere referencia al sí de Sergio, binding del briefing/asignación, actor, revisor distinto, vencimiento, operaciones permitidas y límite de intentos. Sólo el coordinador local lo prepara; un PEDIDO de Boss no concede permisos. Para el piloto: Sol 6.1 low, cero hijos, máximo tres intentos totales y tres sesiones globales con revisores incluidos. No existe permiso para producción, PC, n8n, gastos ni envíos comerciales.

Primero se habilita consulta. El permiso de lanzamiento del juguete se habilita después de comprobar la llave nueva y cargar el webhook. La autorización ya corresponde al piloto de esta conexión; no se pide otro sí para pasos rutinarios. No se lanzan otras tareas por ese permiso.

Sergio, desde una terminal SSH **dentro del VPS**, como `onia-codex-worker`:

```sh
bash ~/operacion/puente-boss/configurar-retorno.sh
```

Pegar URL y clave sola, sin `Bearer`, en los dos campos ocultos. No pegarlas en el chat ni en comandos del historial. Se guardan en `~/operacion/puente-boss/webhook.json`; no se reemplaza un archivo existente. El notificador usa HTTPS/443, `Authorization: Bearer`, sin redirecciones ni proxies heredados. La compatibilidad real de esta autenticación se comprueba con el webhook de Boss; no se presume por el test simulado.

La nueva entrada authorized_keys lleva `restrict,command=".../puente-boss/entrada.sh"`. La llave vieja se conserva hasta probar la nueva y acordar su restricción exacta. Mientras exista shell amplio anterior, no afirmar que Boss está completamente aislado.

## Publicación y retorno

El registro compartible inicial debe existir en master. El publicador toma la última master y agrega únicamente la revisión de la tarea y su evidencia propia, sin stagear el checkout del coordinador. Si otra persona modificó el registro o una evidencia, frena; no sobrescribe ni rehashea originales. El índice y HEAD del coordinador no se mueven: tras una publicación automática hay que conciliar master con los archivos canónicos antes de un merge manual; no usar reset o checkout sobre esos cambios.

Los índices privados y diarios se conservan para diagnóstico, con un límite de 24 mutaciones por tarea antes de conciliación. No hay recolección automática ni borrado. El detector de patrones sensibles es una defensa adicional, no una garantía de saneamiento; el encargo compartible y sus evidencias deben revisarse.

Por ID/revisión se persiste intención antes del POST. Sin archivo privado: `pendiente_configuracion`. Si falla publicar: `pendiente_publicacion`. Timeout, corte o respuesta no 200: `incierto`; no se reenvía automáticamente porque Boss podría haber recibido el aviso. Si consta 200: `recibido_http`, todavía sin acuse. Sin cron ni consulta tres veces por día.

Tras cargar configuración, un retorno pendiente puede reintentarse explícitamente con la versión instalada de `harness.py`, pasando `--base`, `--operacion` y `notificar-boss ID`; usar las mismas rutas fijadas en config. Los estados inciertos requieren conciliación antes, no repetición ciega. El acuse se conserva como evidencia del registro, sin otro sistema de estados.

## Prueba conjunta pendiente y parada

1. Boss consulta con la nueva llave; prueba que `id`, shell libre y SFTP se rechazan. Conserva salida saneada, sin destino, IP ni secretos.
2. Sergio carga URL/clave. Codex habilita el permiso acotado del juguete, con vigencia y modelo explícitos.
3. Boss pide el juguete una vez y repite el mismo JSON; sólo un intento. La ejecutora publica su rama. Cerrar verifica origin, conserva worktree, publica registro y avisa.
4. Boss publica su acuse con ID/revisión/commit; revisor diferente evalúa el producto. Codex integra, recoge veredicto y acepta sólo con evidencia buena vigente. Publica todo en master.
5. Verificar la restricción de la llave anterior después de probar la nueva, preservando su original y los otros accesos. Sólo entonces se evalúa la aceptación de la conexión completa.

Parada: coordinador cambia `pausado` a true en config mediante escritura privada atómica; deniega nuevas mutaciones, conserva consultas y no mata procesos vivos. Revocación individual: `revocado:true` en el permiso de ese ID. Esto no es un loop ni una orden para detener producción. Una interrupción de sesión debe realizarse por su ID con el procedimiento del harness.

Reversión: conservar release/config/authorized_keys previos, pausar, y cambiar la nueva entrada a un comando que rechace todo si hay que inhabilitarla. No borrar entradas ni restaurar todo authorized_keys sobre cambios posteriores. No reiniciar SSH ni otros servicios. Una entrega incierta se concilia; no se relanza desde cero.

Después de agotarse la suscripción, este adaptador y los programas fijos siguen existiendo, pero lanzar/revisar con Codex requiere acceso y cuota. No promete un ejecutor o revisor fuerte gratuito ni continuidad autónoma.

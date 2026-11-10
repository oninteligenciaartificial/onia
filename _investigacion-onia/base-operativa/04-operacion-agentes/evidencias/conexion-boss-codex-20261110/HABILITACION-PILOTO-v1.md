# Permiso del piloto habilitado

10 noviembre 2026, 10:31 America/La_Paz. Registro de conexión: `conexion-boss-codex-20261110`. Juguete: `conexion-boss-piloto-20261110`.

Autorización: Sergio pidió explícitamente habilitar el juguete para que **Boss** lo lance, repita la misma solicitud y publique el acuse; después, restringir la llave anterior `onia-vps-codex-1360183`. No amplía permisos para otras tareas.

Comprobado antes de habilitar:

- Master leído: `a02693b`; contiene la [prueba SSH real publicada por Boss](PRUEBA-SSH-BOSS-v1.md). La consulta y los rechazos desde su llave se atribuyen a esa prueba.
- `webhook.json` existe, propietario correcto, archivo normal sin symlinks, modo 600 y formato HTTPS/clave validado sin imprimir valores. No se hizo un POST desde esta habilitación.
- Release instalada coincide con los hashes de `69ceedb262881469fd2eedcb0447e1a025656639`; base, rutas y briefing conservan integridad.
- Cero sesiones vivas del harness al comprobar. Codex disponible en la instalación existente; el lanzamiento exige login ChatGPT, sin API de pago. No se agregan MCP ni skills.
- El rechazo anterior con nonce `boss-prueba-sin-permiso-01` **no creó solicitud, barrera ni sesión**. Tampoco se usó el nonce real de abajo.

Permiso privado creado para ese único ID, ligado al briefing y asignación actuales: `gpt-6.1-sol`, esfuerzo `low`, cero hijos; actor `boss-piloto-ejecutor`, revisor `boss-piloto-revisor`, máximo tres intentos totales. Se mantienen tres cupos globales, revisión distinta y worktrees conservados. Vence el **11-nov a las 10:31:06 America/La_Paz**. Permite ejecutar, reanudar, cerrar, revisar, recoger y notificar; no crear encargos ni aceptar ni ejecutar shell.

**Revisión esperada de lanzamiento: 2.** Habilitar un permiso no cambió la revisión de la tarea. Codex no la lanzó.

## Solicitud exacta de Boss

```json
{"version":1,"operacion":"ejecutar","id":"conexion-boss-piloto-20261110","solicitud":"boss-piloto-real-20261110-01","revision_esperada":2}
```

Enviar por la llave nueva, con BatchMode, StrictHostKeyChecking e IdentitiesOnly, al comando `onia-harness-v1`. Repetir **exactamente el mismo JSON**, incluyendo nonce y revisión 2: la segunda respuesta debe indicar `repetida:true` y mantener el mismo intento. No usar un nonce nuevo para la repetición. Conservar ambas respuestas saneadas.

Después consultar el ID hasta `viva:false`. Para cerrar, usar la revisión actual devuelta por consulta y una solicitud nueva, por ejemplo `boss-piloto-cierre-01`, con operación `cerrar`. El cierre comprueba el commit, publica el registro en master y dispara el webhook. Que el proceso termine por sí solo no dispara el aviso: no hay scheduler. Si se devuelve `conciliacion_necesaria_no_repetir`, detener mutaciones y pedir conciliación; no eludirlo con otro nonce.

Boss debe publicar el acuse con ID, revisión y commit recibidos, y evidencia del único intento. HTTP 200 no sustituye ese acuse. La revisión de producto requiere otro actor/sesión y veredicto bueno vigente antes de aceptación; el aviso `para_revision` no declara todo aceptado. No lanzar fábricas ni guiones por este permiso.

## Restricción de la llave vieja: autorizada, condicionada

Se hará **después** de la prueba y el acuse. El nombre `onia-vps-codex-1360183` no aparece en los comentarios del authorized_keys actual. Boss debe incluir en su acuse la huella SHA256 pública de esa llave vieja, obtenida de su propio archivo, para identificar exactamente la entrada. No hace falta otra autorización de Sergio ni compartir la llave privada.

Codex conservará el original y restringirá sólo la entrada identificada, dejando intactos los otros accesos. Hasta entonces sigue amplia; no afirmar aislamiento completo. No se reinicia SSH ni se borran entradas.

## Recibo

ID `conexion-boss-codex-20261110`; ejecutor/coordinador real `gpt-6-astra/xhigh` heredado, sin nuevo subagente; el modelo del piloto es solicitado Sol6.1 low, efectivo todavía no observado porque no se lanzó. Un intento administrativo; retrabajo no; resultado `aceptada` **sólo la habilitación verificada**, aceptación de la conexión pendiente. Cuota compartida 78 % al inicio observado (10:29:46 La_Paz); última muestra y commits fuente constan en el recibo JSON. Saldo extra 0; no se inventa costo monetario. No se repitió la suite: no hay cambios de código. Validación del permiso, integridad y consulta local sin mutación realizadas; prueba real a cargo de Boss.

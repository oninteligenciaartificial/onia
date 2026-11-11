# Flujo diario acotado · preparado en rama

El programa recibe noticias, crea una solicitud por día de La Paz, usa un adaptador del harness existente y proyecta resultados en el panel Propuesta 1. Cada invocación termina: no instala ni activa servicios, cron, n8n o un bucle de agentes. Redacción real y revisión editorial permanecen pendientes de su ensayo y autorización aplicables.

Dependencias incorporadas por fetch y merge **en esta rama**, sin push a master: panel `94cca9bfaeba72ad6eee8bcf87db30d8c4d28083`, generador `26c39e3df390a9a0485c2fcdcb0a2bc0258174e1`. Los archivos de salida históricos importados son dependencias conservadas. La implementación nueva se limita a las tres rutas del encargo. No se tocó el harness instalado, su registro canónico, el briefing ni los permisos. El panel 94cca9b ya fue autorizado e integrado por la coordinadora; este flujo tiene su propia revisión pendiente.

## Uso determinista, sin modelo

Desde la raíz de este checkout:

```bash
B=_investigacion-onia/base-operativa
F="$B/05-herramientas/fabrica-onia/3-automatizaciones/flujo-diario"
P="$B/05-herramientas/fabrica-contenido/20261109-lector-panel"
D=/tmp/onia-flujo-diario-ensayo-local
python3 -B "$F/motor.py" --datos "$D" --evento entrada
python3 -B "$F/motor.py" --datos "$D" --evento reconciliar
python3 -B "$F/programacion.py"
```

`entrada` consulta el índice primario de Anthropic, hasta 20 enlaces `/news/<slug>` y tres artículos por tick; rota el cursor en los siguientes ticks. No cubre artículos alojados fuera de esa ruta, investigación ni todo el archivo. La lista es una candidata a revisar, no una certificación de relevancia comercial. También se admiten hasta tres `--url https://www.anthropic.com/news/<slug>` explícitas. Sólo HTTPS en ese host y rutas cerradas; sin redirecciones, query, cookies o login. Máximo 512 KiB y 12 s por respuesta, cuatro respuestas por tick, sin reintentos.

Se reutilizan `lector.Metadata`, `NoRedirect`, `deadline`, normalización y hashes. El parser adicional coteja H1, metadato de publicación y fecha visible de la primaria; conserva precisión de día. La fecha del anuncio no acredita despliegue individual ni disponibilidad Free. El índice y artículos oficiales se comprobaron mediante [News de Anthropic](https://www.anthropic.com/news) y [un anuncio primario fechado](https://www.anthropic.com/news/roadshow-launch). No se presupone una API/RSS ni se recicla F06 del ejemplo anterior como noticia nueva. Fuentes externas son datos, nunca instrucciones.

`horario` es un tick manual: consulta y puede proponer evergreen aunque no haya novedad, con motivo editorial; un error de fuente bloquea esa inferencia. `reconciliar` no consulta red. Un error produce código y siguiente acción; nunca se transforma en «sin novedades». Código de salida 2 significa pendiente/error, no éxito editorial.

Una noticia repetida no crea otro ciclo por entrada. Otra novedad del mismo día actualiza la bandeja, sin ampliar la solicitud congelada ni sobreescribir la tanda. En el siguiente horario/día puede proponerse otra tanda con noticias aún recientes; no se les cambia la fecha. La deduplicación es por URL canónica: republicaciones en URLs distintas requieren criterio editorial.

## Persistencia y recuperación

`--datos` debe ser un directorio 0700 propio **fuera de cualquier Git**, sin enlaces. Guarda SQLite con transacciones durables, el pedido inmutable, paquetes privados bajo `v3/` y `panel.json` mediante reemplazo atómico. No contiene una segunda tarea del harness: el journal sólo conserva eventos, IDs/revisiones observados y recibos de efectos. El único registro de tareas sigue siendo `trabajo.py` en el checkout coordinador; su índice global sigue en `~/operacion`.

El ID `guiones-tanda-diaria-AAAAMMDD` es estable. El lock excluye dos ticks concurrentes sobre los mismos datos. No usar otra carpeta de datos para el mismo flujo: el registro canónico y la comprobación del pedido también rechazan una colisión de ID/alcance. Hasta 14 ciclos recientes se consultan/proyectan en un tick; los anteriores se conservan y requieren retoma explícita, sin barrido ilimitado.

Antes de cada efecto se persisten revisión, binding y fase. Una caída antes de marcar envío permite continuar; después del envío se cotejan SID/commit/veredicto en el harness. Un resultado incierto bloquea y **no** se redespecha automáticamente. La preparación parcial, ausencia de SID, fallo del escritor, cuota desconocida o alcance cambiado requieren conciliación de la coordinadora. No borrar journal, inventar un nonce o cambiar ID para eludirlo. Se puede repetir una invocación sólo cuando las evidencias permiten observar el efecto o cuando quedó en fase preparada previa al envío. El harness conserva su propia protección de revisiones, rutas y tres cupos.

El pedido también se persiste antes de escribir su archivo derivado. Un corte entre ambos pasos recupera el mismo contexto. Un paquete v3 completo se reconoce por todos los hashes y entradas del recibo; uno incompleto/alterado se conserva y bloquea, sin limpiarlo para aparentar éxito.

## Ensayo real por la coordinadora, sin recurrencia

**En esta retoma no se lanzó ninguna sesión de modelo ni hijos.** La continuidad recibida y COORDINACION-v4 documentan el piloto previo de la coordinadora y el dictamen del commit `9a4639f`; esa evidencia se conserva y no se atribuye a esta retoma. El comando siguiente es para la coordinadora, después de cerrar esta sesión, obtener la revisión independiente de su commit y resolver reservas de rutas. No autoriza integrar master ni sustituye el sí aplicable a cada lanzamiento. Si las reservas o el STOP impiden el recorrido, conservar el pendiente; no eludirlos.

1. Conservar un checkout del commit revisado de esta rama para ejecutar el motor y leer sus contratos. El harness crea escritores desde origin/master: por eso el briefing pasa rutas absolutas de sólo lectura al prompt/validador/ejemplos conservados. No necesita integrar este código en master ni copiarlo al registro canónico. Mantener ese checkout hasta recoger la revisión de la tanda.
2. Comprobar proveedor ChatGPT incluido realmente disponible, cuota actual, mismo `~/operacion`, reservas exclusivas y decisiones vigentes en el coordinador. No comprar ni llamar APIs pagadas. La muestra de cuota del encargo no demuestra disponibilidad futura. `--proveedor-disponible` declara el permiso de uso incluido; no acredita disponibilidad ni autentica a Sergio. Cada `lanzar`/`revisar` realiza además el preflight vivo descrito abajo, aunque la bandera esté presente.
3. Crear la entrada con el motor sin adaptador; inspeccionar en privado `pedidos/ID.json`, su SHA, fecha real y `panel.json`. Un fallo de fuente o contexto no se resuelve reutilizando la fixture. Elegir una noticia editorialmente pertinente o un evergreen explícito.
4. Desde la sesión coordinadora, con el ID del día realmente creado (ejemplo concreto del 11-nov):

```bash
COORDINADORA_BASE=/ruta/del/checkout-coordinador/_investigacion-onia/base-operativa
python3 -B "$F/motor.py" --datos "$D" --evento reconciliar \
  --coordinador-base "$COORDINADORA_BASE" \
  --ensayo-real guiones-tanda-diaria-20261111 --proveedor-disponible
```

La primera invocación registra/asigna **una tarea privada canónica** usando `harness.prepare` y `trabajo.assign`; no lanza. Inspeccionar el registro desde el coordinador. Repetir una segunda vez el mismo comando despacha **una escritora**, gpt-6.1-sol high, autenticación ChatGPT, cero hijos. Cada invocación ejecuta como máximo un efecto para ese ID. No envolverlo en un while/daemon.

La escritora entrega tres JSON saneados en `1-guiones-calendario/automatizada/diarias/AAAA-MM-DD/`, commit y push sólo a su propia rama. El pedido privado, medios y datos personales no van a Git. Contratos y cerebro se leen desde las fuentes indicadas; el programa no redacta. Exige veinte candidatas, cinco seleccionadas, perspectivas hipotéticas y crítica del mismo modelo, cinco guiones distintos con ambas variantes, fuentes del pedido y horarios vigentes. El validador no certifica veracidad, calidad creativa ni semejanza semántica: Contenido revisa.

Al terminar la escritora, una nueva invocación cierra con comprobación remota y conserva su worktree. La siguiente valida los JSON contra el pedido, arma v3 privado y solicita **una revisora distinta** del commit exacto. Cuando ésta termina, otra invocación recoge; una lectura posterior muestra el dictamen y detiene el ciclo en revisión editorial o corrección pendiente. Máximo dos sesiones totales por ciclo (escritora y revisora), tres globales contando las demás. Un cupo ocupado nunca crea otro registro/carpeta. No hay corrección automática ni sesiones ilimitadas. `aceptar`, integración, publicación y aprobación editorial siguen siendo pasos humanos fuera del adaptador.

Si cambió el día antes de lanzar o los hashes de decisiones/prompt/generador, queda pendiente de conciliación. Si el modelo termina después de medianoche, no se admite una fecha ficticia. Después del 14 siguen funcionando lecturas, validación y panel; redacción requiere un proveedor comprobado y autorización. No existe sustitución implícita por Claude/API/Grok.

## Panel existente y contratos

```bash
python3 -B "$P/servidor.py" --datos /tmp/onia-revisiones-flujo-local \
  --flujo "$D/panel.json" --puerto 8765
```

Servidor temporal en loopback, detener con Ctrl+C. Mantiene Propuesta 1, seis fábricas y el editor de revisión. Muestra candidatas con fecha primaria, intento/último éxito reales, fase del ciclo, ID/revisión/estado observado del harness, resultado, revisión pendiente y errores con siguiente acción. Sin resultado diario sigue visible la tanda histórica, rotulada como tal. Las versiones diarias están en el bloque nuevo; para editar la versión recibida se usa su enlace explícito de recarga.

La bandeja se refresca cada 15 s cuando la pestaña está visible, con timeout 5 s y sin peticiones superpuestas; no recarga el documento ni toca formularios. Una actualización inválida conserva la última vista válida y avisa. No inventa un nuevo éxito a partir del reloj del panel. Cada servidor conserva en memoria su última proyección válida; tras reiniciar con el export corrupto muestra pendiente hasta recuperar el archivo atómico del productor. No reconstruye una fecha de éxito.

Host/Origin/CSRF/versiones/huellas y aislamiento local se conservan. Sólo el modo `--flujo` admite el script de refresco mediante su hash SHA256 exacto y `connect-src 'self'`, en header y meta CSP; no usa unsafe-inline para scripts ni admite código de productores. Sin `--flujo` sigue sin JavaScript. HTTP devuelve sólo HTML escapado de campos permitidos, sin prompts, rutas privadas, payloads, logs o secretos. Las revisiones locales conservan original y propuesta, sobreviven al reinicio y nunca aprueban ni editan la fuente. Una nueva versión/huella invalida un formulario antiguo.

Exports:

- `panel.json`: `onia-flujo-panel-v1`, contrato saneado leído por `diario.py`, con hasta 20 candidatas y 14 ciclos. Resultados incluyen cinco textos/hash/versiones y quedan pendientes editorialmente. `sintetico` distingue una fixture.
- `pedidos/ID.json`: `onia-pedido-diario-v1`, privado, inmutable y ligado por SHA al objetivo canónico. No se sirve por HTTP.
- `v3/<ID-huella>/`: JSON/Markdown y recibo del generador. `--raiz-salida-v3` permite una raíz explícita privada llamada v3, sin Git/enlaces y con permisos privados. El modo anterior conserva el contrato y destino por defecto; no se modificaron las tandas originales v2/v3 importadas.
- En raíz privada, `estado-fabrica.json` usa `onia-fabrica-estado-privado-v1`: referencias al paquete, no rutas de base-operativa. Se consume mediante `--flujo`, **no** mediante `--estado` del panel histórico. El resto conserva schemas editoriales. El recibo incluye los hashes de `redaccion-original.json` y de la corrección aplicada; ninguna versión se reemplaza.
- `config.ejemplo.json`: plan declarativo válido y deshabilitado. `programacion.py` lo valida y emite `onia-plan-disparo-v1`; no es un export importable/activable de n8n.

Una corrección usa `Engine.accept_result(..., corrections=...)` bajo el lock y el contrato `onia-correcciones-v1`: nueva versión/hashes, motivo y original conservados. Invalida la revisión técnica para esa versión y queda en `correccion_pendiente_revision`; no hereda el visto bueno del commit anterior. Contenido/coordinadora deben revisar y autorizar su recorrido posterior. Un fallo de validación conserva el último resultado.

## Programación y reversión

La continuidad vigente fija **inicio a las 17:00 y entrega objetivo a las 18:00 America/La_Paz, del 12 al 14 de noviembre 2026**. `config.ejemplo.json` sigue con `habilitada:false`, `redaccion_autorizada:false` y autorización null. No se restauran las 07:00. La hora las 18:00 es un objetivo, no una promesa de terminar si faltan cuota, revisión o entradas.

`programacion.py --tick` sólo puede iniciar modelos en `[17:00,18:00)` de esas tres fechas, con constancia de autorización, vigencia y preflight positivo. El corte máximo exclusivo es **2026-11-15T00:00:00-04:00**, fin del 14; puede adelantarse, nunca ampliarse mediante configuración. No renueva una suscripción ni presume la disponibilidad hasta esa fecha. Fuera de la ventana se impiden nuevos modelos, pero con la autorización existente aún se pueden cerrar/recoger trabajos ya iniciados; una falta de cuota no bloquea recuperar su resultado. Toda activación sigue a cargo de la coordinadora después de revisión.

Para UN disparo temporal determinista sin modelo ni instalación:

```bash
python3 -B "$F/programacion.py" --ensayo-disparo /tmp/onia-disparo-unico-local
```

Termina al finalizar el tick. No instala servicios ni crea un daemon. La consulta ligera horaria sigue siendo parte del plan, no una rutina activada por estos archivos.

Reversión actual no destructiva: dejar de invocar el tick y detener el servidor local. Conservar SQLite, pedidos, v3 y revisiones; respaldar el directorio privado con el motor parado y restaurar **todo** el conjunto 0700/0600, nunca sólo un JSON o un índice nuevo. Antes de retomar, reconciliar tareas/SID/commits en el único harness. No borrar medios ni originales, ni relanzar un envío incierto. Para volver al panel anterior, iniciarlo sin `--flujo`; conserva las observaciones en sus datos privados. No hay servicio instalado que desactivar.

[Pruebas y comandos](PRUEBAS.md) · [Recibo y límites](RECIBO.md)


### Controlador por horario preparado por la coordinadora

Las plantillas `programacion/onia-flujo-diario.service` y `.timer` permanecen sin instalar. El timer propone ticks por minuto **de 17:00 a 18:59 del 12 al 14**: de 17:00 a 17:59 puede avanzar redacción/revisión, desde las 18:00 sólo cerrar/recoger y observar. La consulta de fuentes conserva su máximo de una vez por hora. Las invocaciones manuales anteriores a las 17:00 pueden recibir candidatas sin congelar la tanda. Cada tick avanza como máximo un efecto del harness para un ID, conservando tres cupos globales y cero hijos.

La configuración activa debe estar fuera de Git, ser del usuario y tener modo 0600. La migración es explícita: copiar los campos del ejemplo nuevo a una configuración privada revisada, manteniendo el archivo anterior; configuraciones antiguas sin fecha/entrega se rechazan. La coordinadora añade la constancia del sí aplicable y revisa el commit antes de instalar. No se modifica automáticamente una configuración ni un servicio del host.

Conservar un checkout del commit revisado en `~/operacion/fabrica-diaria/codigo` y el checkout canónico del harness. Antes de instalar o activar, la coordinadora ejecuta `preflight.py` en el host y coteja su salida saneada; después ajusta las rutas de las unidades y el archivo privado según lo revisado. Esta ejecutora no instala ni activa esas unidades. Al terminar el 14, el timer ya no tiene horarios nuevos; si queda una sesión por recoger, se usa un tick manual con el mismo directorio/configuración y coordinador, sin ampliar `modelo_hasta`. Pausar el timer conserva journal, pedidos, originales y resultados. Detener el disparador no cancela supervisoras del harness.

No se acredita un disparo de systemd ni servicio activo por haber validado el calendario. La continuidad informa un piloto previo correcto; no se repitió aquí ni se usó su cuota como medición actual.

La unidad es sólo el disparador; las sesiones quedan administradas por el registro del harness. Por eso declara `KillMode=process`: al terminar el disparador se conserva la supervisora que lanzó. Esta elección separa explícitamente ambos ciclos de vida; pausar el timer frena nuevas invocaciones, mientras que interrumpir una sesión exige el comando del harness. La [documentación primaria de systemd.kill](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html) describe el comportamiento predeterminado de grupo y esta diferencia. La plantilla también declara el PATH comprobado del Codex instalado. La supervivencia real de una supervisora al finalizar el servicio debe verificarse en la activación autorizada; todavía no se acredita por validar la plantilla.


### Preflight vivo del uso incluido

`preflight.py` adapta el RPC local ya utilizado por la coordinadora, sin depender del archivo temporal ni copiar credenciales. Abre un proceso efímero `codex app-server --listen stdio://`, hace initialize y sólo dos lecturas: `account/read` sin refresh proactivo y `account/rateLimits/read`. No crea thread/turn, no envía prompts a un modelo, no inicia login, no consume resets, no compra créditos y no envía mensajes. Protocolo cotejado con [OpenAI Docs: App Server](https://learn.chatgpt.com/docs/app-server) y schemas del CLI recibido en `/tmp/onia-app-schema`. Esas rutas temporales son referencias de investigación, no dependencias de ejecución.

Antes de **cada** escritora o revisora, `LocalHarness.invoke` consulta de nuevo: cuenta ChatGPT con plan incluido reconocido, `ordinaryUsageAllowed:true`, bucket global Codex y todas sus ventanas disponibles válidas y no agotadas. El permiso backend ausente/null se considera desconocido; no se infiere recuperación por porcentajes o resets. Un 100%, un bloqueo backend, un reset pasado, datos faltantes/tipos inválidos, fallo RPC o timeout impiden el lanzamiento. Porcentajes95/99 válidos se admiten: no vuelve la reserva del 90 %. Que el preflight sea positivo no garantiza capacidad futura del modelo ni entrega a las 18:00.

El plazo total de lectura es de 20 s (no 20 s por llamada), más hasta 2 s de cierre; también limita bytes/notificaciones y líneas incompletas. Sólo usa comandos y métodos fijos, sin shell libre. Las variables de API se retiran para esta lectura, y el harness conserva auth ChatGPT con cero hijos. La salida/journal guardan sólo fuente, horas reales de la consulta, plan, porcentajes/ventanas y resultado, nunca email, IDs de cuenta, tokens, saldo, payload completo ni stderr. No hay caché de autorización: un recibo anterior jamás autoriza un lanzamiento nuevo. Un fallo previo al despacho deja la intención preparada para volver a **leer**; una caída durante un despacho real conserva la conciliación estricta anterior.

`cerrar` y `recoger` no requieren preflight ni cuota, aunque haya vencido el plazo del modelo; siguen exigiendo el ID/alcance/revisión y la autorización aplicables. El plan activo permite escoger tareas pendientes del 12–14 después del corte, priorizando revisiones ya iniciadas. No crea otra tarea ni renueva permisos para modelos.

```bash
python3 -B "$F/preflight.py"
python3 -B "$F/programacion.py"
```

Código0 del preflight: lectura positiva de esa invocación. Código2: pendiente, sin habilitar un modelo. En este sandbox el App Server no pudo arrancar por filesystem de sólo lectura (rc1, sin stdout); el lector original también falló aquí. Se conserva el intento saneado en `evidencia/cuota-programacion-v5/`. **Cuota y login en vivo quedan desconocidos en esta retoma**; la coordinadora debe repetirlo en el host autorizado. No se ampliaron permisos ni se maquilló una muestra histórica como vigente.

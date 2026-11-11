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

**No ejecutado en esta entrega.** La ejecutora no lanzó Codex ni hijos. El comando siguiente es para la coordinadora, después de cerrar esta sesión, obtener la revisión independiente de su commit y resolver reservas de rutas. No autoriza integrar master ni sustituye el sí aplicable a cada lanzamiento. Si las reservas o el STOP impiden el recorrido, conservar el pendiente; no eludirlos.

1. Conservar un checkout del commit revisado de esta rama para ejecutar el motor y leer sus contratos. El harness crea escritores desde origin/master: por eso el briefing pasa rutas absolutas de sólo lectura al prompt/validador/ejemplos conservados. No necesita integrar este código en master ni copiarlo al registro canónico. Mantener ese checkout hasta recoger la revisión de la tanda.
2. Comprobar proveedor ChatGPT incluido realmente disponible, cuota actual, mismo `~/operacion`, reservas exclusivas y decisiones vigentes en el coordinador. No comprar ni llamar APIs pagadas. La muestra de cuota del encargo no demuestra disponibilidad futura. `--proveedor-disponible` declara esa comprobación, no la realiza ni autentica a Sergio.
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

La hora de tanda sigue **null**, pendiente de Sergio. Zona America/La_Paz. Consulta horaria sólo propuesta; no se restauran las 07:00. `programacion.py --tick` también admite una configuración habilitada con hora, constancia de autorización y vigencia explícita del modelo. La configuración entregada permanece deshabilitada y las unidades de ejemplo no están instaladas. Para probar UN disparo temporal determinista sin modelo:

```bash
python3 -B "$F/programacion.py" --ensayo-disparo /tmp/onia-disparo-unico-local
```

Termina al finalizar el tick, sin daemon ni recurrencia. Activación futura requiere hora confirmada, proveedor, acceso y revisión, ensayo completo y sí aplicable; las plantillas de scheduler ya están preparadas en `programacion/`, con un único directorio privado y el journal conservado. Esta entrega no instala ni activa esas unidades.

Reversión actual no destructiva: dejar de invocar el tick y detener el servidor local. Conservar SQLite, pedidos, v3 y revisiones; respaldar el directorio privado con el motor parado y restaurar **todo** el conjunto 0700/0600, nunca sólo un JSON o un índice nuevo. Antes de retomar, reconciliar tareas/SID/commits en el único harness. No borrar medios ni originales, ni relanzar un envío incierto. Para volver al panel anterior, iniciarlo sin `--flujo`; conserva las observaciones en sus datos privados. No hay servicio instalado que desactivar.

[Pruebas y comandos](PRUEBAS.md) · [Recibo y límites](RECIBO.md)


### Controlador por horario preparado por la coordinadora

Las plantillas `programacion/onia-flujo-diario.service` y `.timer` ejecutan un tick por minuto. El tick consulta novedades como máximo una vez por hora y conserva las candidatas antes de la hora editorial. A partir de `hora_tanda` (La Paz), crea como máximo una tanda del día y avanza un paso permitido del harness por invocación. Después de la revisión técnica se detiene para revisión editorial. Un resultado incierto se conserva para conciliación; no se reintenta el lanzamiento con otro ID.

La configuración activa debe estar fuera de Git, ser propiedad del usuario y tener modo 0600. Requiere hora y constancia de la autorización de Sergio. Para redactar requiere además `redaccion_autorizada: true` y `modelo_hasta` con zona horaria; esa fecha no acredita ni compra disponibilidad de Codex. Al vencer queda pendiente y no lanza un proveedor sustituto. Las sesiones iniciadas que crucen el día o la vigencia pueden requerir conciliación explícita; no se acredita funcionamiento ilimitado.

Despliegue preparado, pendiente de autorización: conservar un checkout/export del commit revisado en `~/operacion/fabrica-diaria/codigo`; copiar la configuración a `~/operacion/fabrica-diaria/config.json` y los datos a su única raíz privada; comprobar permisos, acceso al harness y disponibilidad de ChatGPT; instalar las dos unidades como servicio del usuario y habilitar el timer. No se hizo ninguno de esos cambios en esta entrega. Una configuración `habilitada: false` no crea datos ni consulta la red al ejecutar `--tick`. La pausa no destructiva consiste en detener el timer y conservar código, journal, pedidos y resultados.

No se presentan pasos simulados como un servicio instalado: para acreditar operación diaria faltan el sí sobre hora/activación, un disparo real del timer y la comprobación de retoma sin duplicar.

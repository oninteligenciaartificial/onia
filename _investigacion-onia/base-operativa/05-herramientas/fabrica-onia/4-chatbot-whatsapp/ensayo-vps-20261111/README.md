# Ensayo de inscripción WhatsApp en el VPS

Entrega para revisión de `whatsapp-ensayo-vps-20261111`, sobre base Git
`889eae37a129b9aa701358c3e97806efc26aebd0`. Sólo se añade esta carpeta.
El [adaptador aceptado](../trabajos/fabrica-chatbot-whatsapp-20261110/adaptador.py),
sus mensajes y el [workflow de despacho existente](../trabajos/fabrica-chatbot-whatsapp-20261110/workflow-despacho-n8n.json)
se consumen desde su ubicación original. No se copian ni modifican el adaptador o el motor.

Se comprobó HTTP en loopback y el bloque HTTPS propuesto mediante Nginx temporal en
loopback, con certificado ficticio validado por el cliente. No acredita Meta, DNS,
certificado público, conexión a n8n ni entrega a WhatsApp. Todos los identificadores,
credenciales y accesos usados en estas pruebas son ficticios. QR y acceso se encolan
y se renderizan con el propio adaptador; no se entregan por transporte.

## Reproducir el ensayo completo

Desde esta carpeta, con Python 3.10+, Nginx y OpenSSL **ya disponibles**:

```sh
python3 -B comprobar.py
```

El comando devuelve JSON con esperado/observado y sale con 0 sólo si todo pasa.
Crea su temporal privado en `/tmp`, inicia el adaptador, lo reinicia conservando su
SQLite, crea un certificado de prueba e inicia un Nginx propio en primer plano.
Usa puertos efímeros en `127.0.0.1`; termina sus procesos incluso ante fallo y elimina
únicamente su temporal. No lee `/etc/nginx/nginx.conf`, no usa sudo, no instala ni
activa servicios y no llama a n8n o Meta. Falta de Nginx/OpenSSL es fallo explícito.
La pequeña selección de puerto libre de Nginx tiene una carrera local posible;
si otro proceso lo ocupa, falla el ensayo sin detenerlo ni cambiarle el puerto.

Prueba challenge con ceros y rechazos, HMAC sobre bytes UTF-8 con espacios, JSON inválido,
lote inválido atómico, número ajeno, repetición y repetición tras reinicio, inscripción
GRUPAL, QR ficticio, captura pendiente, conciliación incompleta, confirmación autenticada,
confirmación repetida y acceso único. Contrasta operador privado con proxy, incluyendo
POST, doble barra y rutas con escape o `..`. Comprueba el contrato del JSON n8n y el rechazo
de despacho con y sin credenciales. No cuenta estos controles como tests independientes
de la biblioteca: son 73 cotejos de un recorrido integrado.

## Arranque manual de staging

Para explorar sólo con datos ficticios, desde esta carpeta:

```sh
CONFIG_ENSAYO=$(python3 -B fixture.py)
python3 -B arrancar.py --config "$CONFIG_ENSAYO" --puerto 8765 --reloj-ficticio
```

`fixture.py` crea un directorio nuevo `0700` y un JSON `0600` fuera del repo; imprime
sólo su ruta. No contiene `graph_token`. El reloj fijo es `2026-11-12T00:00:00Z` y se
admite exclusivamente con el fixture exacto, para poder repetirlo después del workshop.
La SQLite queda junto al JSON con modo `0600`. Se conserva al detener este arranque
manual; el operador puede retirar luego exclusivamente ese temporal propio.

Detener con Ctrl+C o SIGTERM al PID propio. La última línea informa los contadores de
egreso y transporte. Para una configuración privada validada, usar el mismo comando
sin `--reloj-ficticio`; entonces rige la hora real. `--puerto 0` permite un puerto
efímero, informado en la primera línea. No hay opción para enlazar otra interfaz ni
`--permitir-envios`. Se rechaza `envios_habilitados: true`, sin imprimir valores.

El lanzador reutiliza `leer_config`, `validar_config`, `crear_app` y `SinRegistro` del
adaptador. Fuerza `permitir_envios=False`, sustituye el transporte por un rechazo y
añade una guarda Python contra `socket.connect`. No registra queries, headers o
payloads. Es un proceso temporal WSGI de referencia para el ensayo acotado; un servicio
permanente necesita su propio encargo y servidor WSGI apropiado. No es aislamiento
frente a código hostil ni una política de red del sistema.

## Receta HTTPS externa preparada, sin aplicar

[meta.nginx.conf.in](meta.nginx.conf.in) es el bloque `server` propuesto, probado
sin cambiar sus rutas en el Nginx temporal. En una copia privada y con autorización
para ese despliegue, Operaciones debe sustituir:

| Marcador | Entrada privada a validar |
|---|---|
| `@LISTEN@` | Socket HTTPS del virtual host elegido. En la prueba sólo `127.0.0.1:puerto_efímero`; la exposición pública no está aplicada. |
| `@SERVER_NAME@` | Dominio controlado por Sergio, con DNS y destino comprobados. |
| `@TLS_CERT@`, `@TLS_KEY@` | Rutas privadas al certificado de cadena pública vigente y su clave; nunca al certificado ficticio del ensayo. |
| `@ADAPTER_PORT@` | Puerto loopback del arranque privado, por ejemplo 8765, verificado libre. |

Incluir ese bloque en el virtual host dedicado de una instalación autorizada,
sin un proxy general hacia el adaptador. Primero validar la copia privada con
`nginx -t -p RUTA_PRIVADA/ -c RUTA_PRIVADA/nginx.conf -e stderr` y después repetir
challenge, firma y pruebas negativas de operador contra el dominio desde fuera.
Estas instrucciones no autorizan instalar, recargar o abrir puertos. No se aplicaron.
Un proxy de Easypanel/contenedor no comparte necesariamente el loopback del host:
Operaciones debe comprobar el namespace de red antes de usar este upstream.

El bloque enruta sólo GET/POST de `/meta`; cualquier otra ruta devuelve 404 y otros
métodos en `/meta`, 405. Conserva cuerpo y firma, no usa rewrite, body templating,
redirecciones ni reintentos. Suprime `Authorization` al upstream y deshabilita logs de
acceso y errores del virtual host para no conservar el token del challenge. Si hay
otro balanceador delante, requiere la misma disciplina; la plantilla no controla
sus logs ni su routing. `client_max_body_size` coincide con el límite del adaptador.

Las rutas normalizadas equivalentes se resuelven según Nginx y WSGI; los escapes
probados hacia `/operador/*` fueron bloqueados. No se presenta el muestreo de rutas
como una auditoría exhaustiva. La firma del lote válido tras el proxy comprueba
la conservación efectiva de bytes en la configuración ensayada.

El operador usa el origen privado, autenticado con su Bearer. Para acceso remoto,
puede usarse un túnel SSH a un alias ya validado, con la autorización de conexión
aplicable, sin publicar el operador:

```sh
ssh -N -L 127.0.0.1:18765:127.0.0.1:8765 "$ALIAS_VPS_PRIVADO"
```

Entonces su cliente privado usa `http://127.0.0.1:18765/operador/revisar` y
`/operador/confirmar`; la credencial se carga desde custodia privada, no por argumentos
de shell ni por este README. El túnel no se abrió en esta tarea. La plantilla HTTPS
no concede acceso al operador aunque se presente el Bearer correcto: se probó 404.
Loopback sí es accesible a otros procesos locales; el Bearer sigue siendo necesario.

## Cableado del workflow existente, sin modificar n8n

El artefacto canónico contiene Manual Trigger v1 → HTTP Request v4.2, `active:false`.
La prueba inspecciona ese JSON; no afirma que esté importado ni cotejado con la
versión actual de la instancia. `accesos.md` documenta históricamente n8n 2.43.7;
no se consultó la instancia en este encargo y no hay herramienta MCP n8n disponible.

En una conexión posterior autorizada, conservar el export privado previo si existe
un workflow ya importado y cablear **ese mismo flujo**, sin crear otro motor:

| Campo | Valor/condición |
|---|---|
| Variable `ONIA_CHATBOT_DISPATCH_BASE_URL` | Origen **privado** del adaptador accesible desde el runtime de n8n. |
| URL del nodo | Expresión existente: quita barras finales de esa variable y añade `/operador/despachar`; queda vacía si falta la variable. |
| Método y cuerpo | POST, `sendBody:false`, una salida por ejecución manual. |
| Autenticación | `genericCredentialType` / `httpHeaderAuth`. Vincular en la copia privada una credencial Header Auth, header `Authorization`, valor `Bearer <dispatcher_token>`. Nunca usar el token del operador. |
| Ejecución | Manual, inactiva; `retryOnFail:false`, redirecciones deshabilitadas, timeout 20000 ms. |
| Datos guardados | Error/success `none`, ejecuciones manuales/progreso `false`, sin credencial ni pinned data en el export. |
| Primera respuesta exigida | HTTP 409, `ENVIOS_DESHABILITADOS`. El nodo da error por el 409; es el resultado esperado del ensayo, sin reintento. |

`http://127.0.0.1:8765` sólo vale si n8n comparte el namespace de red del adaptador.
Si n8n corre en Docker separado, su loopback apunta al contenedor: **la conectividad
privada queda pendiente de Operaciones**. Se necesita un túnel/forwarder privado
autorizado o una topología equivalente verificada; no se resuelve abriendo el adaptador
en `0.0.0.0`, publicando `/operador` o usando la URL pública `/meta`. Si la instancia
bloquea `$env`, completar la URL privada del nodo en la copia autorizada, manteniendo
el bloqueo global. No cambiar variables, redes o seguridad de la instancia aquí.

En este staging el rechazo 409 ocurre antes de validar el dispatcher; prueba la
inhibición del envío, **no** la aceptación de su credencial por n8n. La separación de
roles sí se prueba contra revisar/confirmar con el token equivocado (401). Una prueba
de envío real y de autenticación del despacho habilitado queda fuera de este ensayo.

## Parámetros privados mínimos y responsables de validación

No entregar sus valores en chat/Git. Preparar el JSON fuera del checkout con directorio
`0700`, archivo `0600`, dueño de la sesión, y `envios_habilitados:false`.

| Entrada externa | Quién la valida y qué acredita |
|---|---|
| `phone_number_id` | Sergio identifica el número correcto en Meta; Operaciones coteja su asociación a la app/WABA. El adaptador valida dígitos y coincidencia en cada evento; esto no verifica la cuenta real. |
| `app_secret` | Sergio/Operaciones lo cargan desde la app correcta. El adaptador verifica HMAC SHA-256 de los bytes antes de parsear o escribir. |
| `verify_token` | Operaciones genera un valor distinto, Sergio lo introduce en la configuración de webhook de Meta autorizada. El adaptador valida challenge y token. |
| `operator_token` | Sergio controla su custodia y destinatario autorizado; el adaptador valida Bearer. Un token no demuestra por sí solo la identidad física de Sergio. |
| `dispatcher_token` y referencia Header Auth | Operaciones genera uno distinto y verifica su custodia en n8n. No se necesita para challenge/entrada; queda preparado para el POST privado de rechazo. No se valida este campo al arrancar con envío deshabilitado. |
| `pago_ttl_segundos`, `cierre_inscripcion_epoch` | Sergio fija plazo y cierre comercial; adaptador valida enteros y límites (cierre a más tardar inicio de la clase del 16, sin inventar hora final). Operaciones comprueba reloj del VPS. |
| Dominio/TLS y origen privado | Operaciones verifica DNS, cadena/hostname, acceso externo sólo a `/meta`, namespaces y rutas privadas desde operador/n8n. Nada de esto se acredita con el certificado local ficticio. |
| Body Meta, IDs, teléfono y timestamps | Meta firma el evento; el adaptador comprueba firma, forma, número y deduplica ID. No comprueba contra Meta la identidad del remitente. No se pasa por un nodo que reserialice JSON. |
| Captura | El adaptador sólo valida el ID de imagen y abre revisión; no descarga el medio ni comprueba el banco. Sergio verifica el movimiento real. |
| Confirmación: teléfono, referencia, importe, moneda, movimiento y destino | Sergio concilia contra su banco y registro antes de emitir la acción. El adaptador valida estructura, estado pendiente, 50/150 BOB, flags explícitos, cupo y referencia única; no consulta el banco. |
| `qr_media_id` | No es obligatorio para recibir eventos y conservar intención QR con despacho apagado. Para renderizar/próximo ensayo real, Sergio valida el QR y titular/importe; Operaciones valida ID privado, asociación/vigencia del medio. No se carga ni se usa QR real aquí. |
| `meet_urls` (tres, en orden) | No son obligatorios para recibir/encolar con despacho apagado. Sergio/Calendario concilian fechas 13 20:00, 14 14:00 y 16 20:00 La Paz y prueban apertura con cuenta propia. Operaciones verifica su orden/carga privada. |
| Textos | Contenido y Sergio aprueban el borrador antes del ensayo externo comercial. Este encargo no acredita aprobación editorial. |

No hacen falta `graph_token`, `graph_version`, una API key de IA, banco ni Graph para
esta fase sin despacho. Un envío futuro requiere otro alcance autorizado, los activos
reales y el doble permiso del adaptador original; este lanzador no lo permite.

## Evidencia y pendientes

[evidencia/COMANDOS.md](evidencia/COMANDOS.md) conserva comandos, salidas y límites.
El JSON de ensayo incluye hashes de las fuentes reutilizadas. La única corrección
previa a ejecutar fue un corchete de sintaxis del comprobador, conservada en el
preflight; no se modificó el producto para hacer pasar el ensayo.

Esta rama queda para cierre y revisión independiente del coordinador. Pendientes fuera
de alcance: validación/carga privada por sus responsables, topología real del proxy y
n8n, despliegue y webhook Meta autorizados, prueba externa acotada y aprobación
editorial. Para retomar el ensayo externo se requieren esos accesos y permiso para
los cambios concretos. La fase de staging conserva siempre el despacho deshabilitado.

Documentación primaria consultada el 12-nov-2026: [proxy_pass sin URI](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass),
[location exacto](https://nginx.org/en/docs/http/ngx_http_core_module.html#location) y
[HTTP Request de n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/).
Las opciones se cotejan además con los binarios locales y el export existente;
la documentación no acredita su configuración en la instancia real.

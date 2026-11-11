# Adaptador local del workshop

[adaptador.py](adaptador.py) recibe el webhook de Meta y registra el recorrido en SQLite. Comparte la oferta y los textos de [mensajes.json](mensajes.json) con el ensayo. Los borradores de QR y acceso para el adaptador se construyen a partir de la configuración privada. La aprobación editorial sigue pendiente. El [workflow de ensayo](workflow-n8n.json) ejecuta los fixtures. El [workflow de despacho](workflow-despacho-n8n.json) contiene el enlace manual al adaptador. Ambos se entregan inactivos.

## Reproducir

Desde esta carpeta, con Python 3.10 o posterior y Node.js 20.

```sh
node preparar.cjs
node pruebas.cjs
node ensayo.cjs
python3 -B -m unittest -v pruebas_adaptador
```

Las pruebas llaman a la aplicación WSGI en memoria, conservan las bases SQLite ficticias en una carpeta privada nueva en `/tmp` y sustituyen el transporte por un falso o un mock HTTPS. Cubren 44 casos en Node (incluida la regresión BAJA → vencimiento en el módulo y en el JSON, y la estructura del workflow de despacho) y 16 en Python: los 14 existentes y dos nuevos para configuración/faltantes y el lunes 16. No se cuentan los subcasos como pruebas independientes. El caso de venta comprueba el cuerpo de los mensajes y que una captura deja la inscripción pendiente. Las pruebas externas con Meta, n8n y Meet siguen en [FALTANTES.md](FALTANTES.md).

Fechas vigentes: viernes 13 20:00, sábado 14 14:00 y lunes 16 20:00, La Paz. No se confirmó hora final. Los comandos repetibles, resultados de esta tanda y el recorrido autorizado pendiente para Sergio están en [GUIA-REVISION.md](GUIA-REVISION.md).

## Configuración privada

Para un ensayo HTTP en loopback, colocá un JSON de prueba en una carpeta propia con permisos `0700`, fuera del checkout. El JSON debe tener permisos `0600`. El adaptador crea `chatbot.sqlite3` allí mismo con permisos `0600`, enlazada al `phone_number_id` configurado. El registro conserva teléfono, timestamps necesarios, ID de mensaje, estado, modalidad, referencia verificada y estado de salida. Las capturas y el texto crudo se descartan. Gestionar acceso, backup y retención de esa carpeta fuera de Git.

| Clave JSON | Valor |
|---|---|
| `phone_number_id` | Cadena de dígitos, ID del número en Meta. |
| `app_secret`, `verify_token`, `operator_token` | Tres valores distintos de 24 a 256 caracteres ASCII alfanuméricos o `_.~-`. La credencial del operador se entrega sólo a Sergio u operador autorizado. |
| `pago_ttl_segundos` | Entero entre 1 y 86400. Sergio fija el plazo de pago, independiente de la ventana de atención de Meta. |
| `cierre_inscripcion_epoch` | Entero Unix en segundos, a más tardar `2026-11-16T20:00:00-04:00`, inicio de la última clase. Sergio fija el cierre comercial, que puede ser anterior. Una inscripción vence al primero de sus dos límites, plazo de pago o cierre. No se deriva de una hora final supuesta. |
| `envios_habilitados` | Booleano estricto. La omisión equivale a deshabilitado; cadenas como `"false"` se rechazan como configuración inválida. |
| `dispatcher_token` | Credencial exclusiva de despacho para n8n. Mismo formato de 24 a 256 caracteres, distinta de las otras tres. |
| `graph_version`, `graph_token` | Para un envío autorizado, versión Graph elegida en la cuenta (`v<mayor>.<menor>`) y token de envío. |
| `qr_media_id` | ID de imagen privada ya cargada a Meta para ese número. Sergio mantiene el original fuera de Git. La carga y la prueba de vigencia del medio siguen pendientes. |
| `meet_urls` | Tres enlaces HTTPS a `meet.google.com`, uno por clase en orden. Sólo se incluyen en el payload de acceso confirmado. |

El servidor de desarrollo sólo enlaza loopback. Para una prueba local adicional con configuración ficticia, ejecutá `python3 -B adaptador.py --config /ruta/privada/config.json`. Detenelo con Ctrl+C. El despachador permanece deshabilitado con ese comando. Para un encargo posterior de conexión, el envío exige además el argumento `--permitir-envios` y la bandera privada `envios_habilitados: true`. El servidor incluido es para desarrollo. La exposición a Meta requiere un servidor WSGI adecuado, HTTPS y un proxy que enrute sólo `/meta`.

En esta tanda no se inicia ese servidor ni se proporciona configuración real. Sin permiso de envío, la app puede conservar una intención QR sin medio configurado, pero no despacharla. Si se habilita el transporte y falta `qr_media_id`, `meet_urls`, token de Graph o credencial de despacho, la aplicación rechaza el arranque con el nombre del campo faltante, sin imprimir valores. En la exportación pública esos datos constan como no verificados; no se toma un fixture por un activo listo.

## Contrato HTTP

| Método y ruta | Entrada | Respuesta |
|---|---|---|
| `GET /meta` | Parámetros únicos `hub.mode=subscribe`, `hub.verify_token` y `hub.challenge` decimal. | 200 `text/plain` con el challenge exacto. Verificación inválida 403. |
| `POST /meta` | JSON de hasta 256 KiB con `Content-Length` y `X-Hub-Signature-256: sha256=<hex>`, calculado sobre los bytes exactos con el app secret. Recorre todos los cambios `messages` y verifica su `metadata.phone_number_id`. | 200 JSON `{"nuevos":N}` después del commit. Una repetición devuelve 0. Firma o número ajeno 403 y lote íntegro descartado. Los avisos de estado de Meta se acusan sin alterar pagos. |
| `GET /operador/revisar` | `Authorization: Bearer <operator_token>`. | 200 JSON con `revision` e `inciertos`. Contiene teléfonos privados. `AYUDA`, inscripción pendiente y captura aparecen aquí para revisión humana. |
| `POST /operador/confirmar` | Mismo Bearer. JSON con `telefono` en formato WhatsApp (dígitos sin +), `decision:"confirmar"`, `referencia`, `importe` entero (50 o 150), `moneda:"BOB"`, `movimientoVerificado:true` y `destinoVerificado:true`. Sergio emite la señal después de comprobar el abono real. | 200 JSON `{"resultado":"confirmado"}` o `{"resultado":"ya_confirmado"}`. Una referencia se usa una sola vez, normalizada a mayúsculas y sin espacios externos. Los conflictos son 409. |
| `POST /operador/despachar` | `Authorization: Bearer <dispatcher_token>`, cuerpo vacío. Una salida por petición. | 200 JSON con `resultado` igual a `aceptado`, `incierto` o `vacio` y el ID local si se intentó. Deshabilitado devuelve 409. |

La autenticación fallida del operador devuelve 401. La validación de estructura o cuerpo puede devolver 400, 411 o 413. Un fallo de SQLite devuelve 503. El ID de Meta deduplica el evento de entrada, y la escritura de estado y de cola ocurre en la misma transacción. La verificación del número, HMAC y forma del lote sucede antes de esa escritura. Una imagen abre revisión sin descargar el medio. Los comandos de texto son `NEGOCIO`, `GRUPAL`, `VIP`, `AYUDA` y `BAJA`.

El seguimiento preparado consiste en la bandeja privada `/operador/revisar` y la cola de salida con despacho manual. No hay recordatorios periódicos instalados. BAJA cancela las intenciones pendientes y evita que el vencimiento genere contacto nuevo. Ningún programa requiere un LLM para ejecutar ese circuito; el permiso, acceso y ensayo del operador para el lunes 16 siguen pendientes antes del corte de Codex informado para el 14.

El límite VIP se comprueba al pedir QR y al confirmar. Una solicitud pendiente no reserva cupo. Con más de cinco solicitudes simultáneas puede llegar un pago cuando ya se llenó el cupo. Sergio debe decidir el tratamiento comercial antes de abrir VIP. El importe, el estado y el cupo son validaciones del registro. El acceso a la banca y la comprobación del destino siguen a cargo del operador.

## Entrega y recuperación

Antes de llamar a Graph, SQLite reserva la fila como `incierto`. Una respuesta HTTP 200 con un ID válido la marca `aceptado` y guarda el ID. Una caída, timeout, respuesta inesperada o rechazo de Graph la deja incierta para revisión. El siguiente despacho sólo lee filas pendientes. El operador consulta los inciertos antes de reenviar por otro medio. La aceptación de la API no prueba recepción por la persona. El código no reencola una salida incierta ni consulta recibos de Meta.

BAJA cancela las salidas pendientes de la persona, conserva su cese y encola un acuse único. Una llamada externa ya reclamada por el despachador puede estar en curso. El despacho cancela texto e imágenes si pasaron 24 horas desde el último mensaje de Meta. Para completar acceso fuera de la ventana se requiere un procedimiento autorizado con el operador y las plantillas aplicables. [Política de mensajería de WhatsApp Business](https://whatsappbusiness.com/policy/)

## Conexión de n8n en una prueba autorizada

[workflow-despacho-n8n.json](workflow-despacho-n8n.json) conecta Manual Trigger v1 con HTTP Request v4.2. Cada ejecución manual solicita un solo `POST /operador/despachar` sin cuerpo. Los reintentos, redirecciones y guardado de ejecuciones están deshabilitados en el artefacto. Sigue pendiente cotejar estas opciones, importar y probar el flujo en la versión instalada de n8n.

1. Configurá `ONIA_CHATBOT_DISPATCH_BASE_URL` en el entorno privado de n8n con el origen interno del adaptador. La expresión agrega `/operador/despachar` y queda vacía si falta la variable. Si la instancia bloquea el acceso de expresiones al entorno, completá la URL privada del nodo en la copia de prueba y conservá el bloqueo de la instancia.
2. En el nodo, seleccioná una credencial **Header Auth** de n8n con nombre de cabecera `Authorization` y valor `Bearer <dispatcher_token>`. La credencial se vincula en la copia privada. La exportación incluye el tipo de autenticación sin credencial vinculada.
3. Verificá primero el rechazo con envíos deshabilitados. Para probar un envío, usá únicamente el número y el alcance autorizados. Si vence la llamada de n8n, consultá el registro privado antes de cualquier acción posterior.

La conciliación entra por la ruta privada con acción explícita de Sergio. La recepción de Meta termina directamente en `/meta`, preservando bytes y firma a través del proxy. Si en el entorno elegido n8n recibe el webhook, verificar que entregue el cuerpo en Raw Body sin reserializarlo y devuelva el challenge y el acuse del adaptador. Mantener `/operador/*` fuera del proxy público y evitar logs de query strings en `/meta`. [Webhook de n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook) · [HTTP Request de n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/) · [Header Auth](https://docs.n8n.io/integrations/builtin/credentials/httprequest/#using-header-auth) · [Implementación de HTTP Request v4.2](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/HttpRequest/V3/HttpRequestV3.node.ts) · [Ajustes de ejecución](https://docs.n8n.io/workflows/settings/)

Contratos consultados en la documentación del SDK de Meta, actualmente archivada, y en la colección oficial de Cloud API. La versión Graph queda como entrada privada y se debe probar con el número de prueba elegido. [Challenge y firma de Meta](https://whatsapp.github.io/WhatsApp-Nodejs-SDK/api-reference/webhooks/start/) · [Enviar texto](https://www.postman.com/meta/whatsapp-business-platform/request/8gvd47s/send-text-message) · [Enviar imagen por ID](https://www.postman.com/meta/whatsapp-business-platform/request/dv878df/send-reply-to-image-message-by-id)

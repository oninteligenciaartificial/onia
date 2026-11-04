# Accesos de ONIA

Inventario preparado el 3 de noviembre de 2026; actualizado el 4 de noviembre, UTC−4, para la [arquitectura](arquitectura.md). Las [reglas comunes](reglas-comunes.md) gobiernan permisos y decisiones. Este archivo conserva destino, finalidad y alcance de acceso; no valores secretos. [ESTADO.md](ESTADO.md) mantiene la evidencia vigente de cada prueba.

## Inventario y prueba

Este inventario registra todos los accesos; no implica entregar todos sus secretos a Codex. La bóveda personal de Codex sirve para variables y secretos de red solicitados por un entorno. Las contraseñas de cuentas, conexiones OAuth, claves SSH y secretos de producción tienen consumidores y mecanismos distintos.

| Servicio | Ubicación y mecanismo | Estado | Prueba pendiente |
|---|---|---|---|
| GitHub `oninteligenciaartificial/onia` | Conexión del entorno Codex Cloud `onia`; repo privado del harness. | Checkout correcto y lectura comprobados también en la nueva «onia · aceptación cloud». | Conservar los cambios útiles y comprobar la revisión necesaria para cada encargo. |
| n8n API | Ubicación elegida con Sergio: `N8N_API_KEY` como Secreto de red del propio entorno `onia`, dominio `n8n-sergio-n8n.hqdqgh.easypanel.host`. No duplicarlo en la bóveda personal. | Editor confirmó listado y `/api/v1/discover` HTTP 200 el 4-nov-2026. El alcance anunciado incluye crear/leer/actualizar/importar workflows, crear credenciales/tablas y crear/leer filas. POST de un workflow sintético HTTP 200 y GET posterior: diez nodos, `active:false`. | Creación y ejecución sintética real comprobadas, incluida tabla/credencial y cinco casos; final inactivo. No hace falta otra key ni acción de Sergio para cerrar el ensayo. Vigencia y operaciones de producción se comprueban por separado. |
| Credenciales de flujos n8n | Almacén `Credentials` de la instancia existente. | Tabla y credencial de autenticación del ensayo sintético creadas y usadas en n8n real; no son conexiones Meta ni del recorrido comercial. | Probar cada servicio con la operación necesaria y datos sintéticos. |
| Meta Ads | App existente **ONIA Marketing API**; `META_ADS_ACCESS_TOKEN` en Secretos de red de `onia`, dominio `graph.facebook.com`. Conservar la entrada para su función original, sin reemplazarla por la de Instagram. | Histórico: lectura publicitaria HTTP 200. Estado actual informado por Editor el 4-nov-2026: `/me/permissions` y `/me/accounts` devolvieron HTTP 401, OAuth 190/463, token vencido. Configuración guardada no equivale a autenticación vigente. | Sergio renueva por la ruta oficial cuando el encargo de Ads lo requiera; el ejecutor verifica después alcance, vencimiento y lectura. No se probó una renovación. |
| Instagram operativo `@sergiourcullo` | Entrada propuesta separada `META_IG_ACCESS_TOKEN`, dominio `graph.facebook.com`, en Secretos de red de `onia`; ruta objetivo Instagram API con Facebook Login. | Pendiente de autorización personal y guardado: la entrada todavía no existe como acceso comprobado. No confundir con ONIA Research ni con el token Ads vencido. | Sergio autoriza y guarda por el mecanismo oficial; el ejecutor comprueba permisos, Página vinculada y cuenta profesional objetivo mediante lectura antes de operar. Publicación y DMs aún no habilitados. |
| Instagram de investigación | Cuenta separada y sesión en una superficie cloud compatible, pendiente de resolver bajo la decisión de usar sólo Codex ahora. | Nombre elegido por delegación de Sergio: **ONIA Research**. Usuario candidato: **onia.research**. Correo Gmail candidato: **onia.research.sergio@gmail.com**. Disponibilidad no comprobada; correo y cuenta no creados. | Resolver navegador cloud interactivo; crear correo y cuenta con verificación directa de Sergio. Comprobar lectura de un reel y persistencia de sesión. |
| Archivos | [ONIA archivos en Drive](https://drive.google.com/drive/folders/1eON_RgRbSN3Yz_qmudo5-dNBomDDIufu), cuatro carpetas de entrada, marca, productos y entregables. | Creación y permisos de propietario comprobados; la nueva sesión cloud volvió a listar los cuatro hijos directos. | Leer/descargar un archivo real y recuperar un entregable desde otra tarea. |
| Contexto compartido | Fuentes y responsabilidades en [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md); no se trasladan los archivos privados locales por Git. | Recuperación de una entrada sintética y su actualización entre chats cloud comprobadas; evidencia en ESTADO.md. | Leer la fuente pertinente al encargo y comprobar su versión; la prueba de contexto no acredita transferencia de medios. |
| Notion | Conector oficial; panel privado **Sergio · Hoy**, identificado en [PANEL-DIARIO.md](PANEL-DIARIO.md). | Panel creado y releído; reemplaza el resultado anterior de autenticación rechazada. Estructura y límites en PANEL-DIARIO.md. | Comprobar la operación concreta desde el ejecutor que la realizará; la conexión de este chat no acredita acceso en todas las VMs ni avisos recurrentes. |
| Gmail | Conexión oficial disponible en el ejecutor cloud. | Perfil válido comprobado en la nueva sesión; no se leyeron correos. | Lectura o preparación de un correo sólo para un encargo concreto. |
| Calendario y organización | Conexión oficial disponible en el ejecutor cloud. | Perfil/listado y consulta del día 4-nov comprobados; también se consultó la ventana 4–14-nov. Resultado y estado del piloto en ESTADO.md. | Volver a consultar disponibilidad para el encargo concreto; una lectura previa no acredita eventos creados ni disponibilidad futura. |
| Higgsfield | Conexión del proveedor disponible en el ejecutor cloud. | Perfil y workspace válidos comprobados en la nueva sesión: plan Pro, 585 créditos observados. No se generó contenido ni se consumieron créditos en esta prueba. | Comprobar herramienta, materiales y costo de una generación concreta; la cuota observada puede cambiar. |
| VPS y producción | Acceso administrativo separado del piloto de lectura n8n. | Inspección parcial por panel; acceso SSH no probado. | Sólo la inspección necesaria para un encargo de infraestructura. |
| Grok Bot | Conexión futura, fuera del alcance operativo actual. | Captura aportada por Sergio el 3-nov-2026: Premium, 100 % usado. Conserva esta herramienta; ahora se trabaja sólo con Codex y n8n existente. | Retomar cuando haya cuota y Sergio lo habilite. Fecha de renovación e integración no verificadas. Los mensajes históricos de sus bots no certifican despliegues actuales. |

Las primeras comprobaciones de perfiles y listados se realizaron en «onia · aceptación cloud», después de publicar el entorno. Las operaciones posteriores y su ejecutor se distinguen en ESTADO.md. Cada resultado acredita la operación probada, no todas las funciones del servicio. No se conservan aquí correos personales, IDs de calendarios ni identificadores privados de los perfiles.

## n8n: configuración del piloto

La preparación histórica de n8n 2.43.7 se interpretó como una clave limitada a `workflow:list`, con siete días de vigencia. Esa limitación no describe el alcance actual: coordinación confirmó `/api/v1/discover` HTTP 200 con `workflow:create/read/update/import`, `credential:create`, `dataTable:create` y operaciones de filas create/read. POST de un único workflow nuevo devolvió HTTP 200; GET confirmó diez nodos y `active:false`. No hace falta una nueva key para esas capacidades observadas. La fecha exacta de vencimiento vigente sigue por registrar.

El helper preparado llama únicamente a:

```text
GET https://n8n-sergio-n8n.hqdqgh.easypanel.host/api/v1/workflows?limit=10&excludePinnedData=true
Header: X-N8N-API-KEY
Secreto: N8N_API_KEY
```

No sigue redirecciones ni muestra cuerpos, cabeceras o valores secretos; su resultado es agregado. El helper de listado por sí solo no acreditaba escritura; ahora la creación sintética está confirmada por otra operación. El workflow **ONIA · Ensayo privado · Sintético DRY RUN** fue activado temporalmente con autenticación para cinco casos reales: éxito 201, duplicado 200 sin nueva fila, conflicto 409, inválida 400 y auth incorrecta 403. Tabla y credencial reales utilizadas. Otra ejecución 200 DUPLICATE y lectura de tabla comprobaron una sola fila para el evento; hay dos filas sintéticas totales de dos pases distintos, no duplicación del evento. Final comprobado `active:false`, con guardado de datos de ejecución deshabilitado. Esto supera los 14 tests históricos del modelo para esos cinco casos; no prueba concurrencia, timeout real ni Meta. Cero DMs/publicaciones y ningún software adicional en VPS. No falta intervención personal para cerrar este ensayo. JSON, enlace del workflow y evidencia permanecen en la [entrega privada](https://chatgpt.com/space/page_381ee668401481918e7e45c87921e82d); no se copian IDs de activos ni datos privados al repo.

Un secreto de red de Codex entrega un marcador al proceso y sustituye la credencial para destinos HTTPS autorizados. Los secretos propios del entorno pueden añadir sus dominios a la red permitida; los personales no lo hacen. Después de guardar se revisa la política efectiva y se prueba el acceso. [Configuración cloud](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets).

## Instagram operativo y continuidad de autenticación

Objetivo autorizado para preparar el acceso: `@sergiourcullo`, separado de la cuenta de investigación candidata. La ruta elegida para comprobar es **Instagram API con Facebook Login**: cuenta profesional vinculada a una Página. Los seis permisos objetivo son `pages_show_list`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`, `instagram_manage_messages` y `pages_manage_metadata`; no son permisos ya concedidos. No mezclar esta ruta con los permisos de Instagram Login. [Fuente primaria de Meta](https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api).

Para DMs de personas externas sin rol en la app o los activos asociados, la ruta requiere **Advanced Access**, además de las condiciones de la app/negocio y acceso a la Página; la documentación de conversaciones describe un Page token obtenido por una persona con tarea `MESSAGING`. Son requisitos por verificar, no capacidades acreditadas. El enlace abrió sólo la interfaz; el detalle se recuperó del texto indexado del mismo [documento oficial Messenger/Conversations](https://www.postman.com/meta/messenger-platform-api/folder/22794852-255610cd-47f5-4f4d-b3fa-71aec360be9a). No enviar DMs ni publicar para comprobar permisos.

**Paso personal pendiente:** Sergio autoriza la ruta oficial y guarda `META_IG_ACCESS_TOKEN` como entrada nueva para `graph.facebook.com`; no enviar el token por chat. **Paso del ejecutor después:** comprobar disponibilidad en el runtime efectivo, permisos concedidos, Página/cuenta profesional objetivo y vencimiento con lecturas mínimas sin mostrar cuerpos privados. Registrar resultado antes de preparar la operación concreta. Conservar `META_ADS_ACCESS_TOKEN` para Ads aunque esté vencido; esta edición no renueva ni elimina credenciales.

Para cada ruta autenticada registrar tipo de credencial, emisión/vencimiento cuando estén disponibles, última lectura, responsable y procedimiento oficial de renovación/revocación, sin valores. Un token derivado de Página no se presume permanente; la continuidad depende de revalidar su vigencia y renovar la ruta cuando corresponda. Estado actual: Meta expirado según Editor, fecha exacta de expiración no registrada; nueva ruta IG pendiente. n8n lista con HTTP 200; vencimiento exacto actual por confirmar. Sergio resuelve autorización/renovación personal; el ejecutor documenta y valida la lectura posterior.

El token obtenido mediante Graph Explorer sirve para el piloto; producción no debe depender de regenerarlo manualmente cada hora. La ruta de producción por revisar es la [credencial OAuth2 Facebook Graph API de n8n](https://docs.n8n.io/integrations/builtin/credentials/facebookgraph/), con **Facebook Login for Business**. Reutilizar la app actual si admite ese producto y verificar primero los campos reales de la credencial. Client ID y Client Secret se introducen directamente en `Credentials` de n8n; registrar en Meta exactamente la Redirect URI que muestre esa credencial y completar su botón **Connect to Facebook Graph (App)**. No crear otra app por defecto ni copiar secretos al repo o al chat. Esta ruta está documentada, no configurada ni conectada en este encargo.

Que n8n ofrezca también App Access Token no lo vuelve válido para operar el perfil, Reels o DMs: esas operaciones requieren el token de usuario/Página correspondiente y sus permisos. Tras autorizar, registrar vencimiento real y vigencia del acceso a datos, y comprobar qué renovación soporta efectivamente la ruta; no afirmar renovación automática ni token permanente. Un aviso de renovación sigue pendiente hasta disponer de un scheduler implementado y comprobado; anotarlo no lo programa.

La [autenticación oficial de n8n](https://docs.n8n.io/api/authentication/) usa `X-N8N-API-KEY` y permite elegir expiración; la documentación actual limita scopes de API a Enterprise. La observación histórica de alcance en la interfaz no prueba el plan ni permisos actuales: no asumir que la clave está restringida a listar por un GET 200. La creación del workflow sintético está comprobada según la sección del piloto; el E2E secuencial sintético con tabla/credencial ya fue comprobado, sin extrapolar a producción o Meta.

## Lista de custodia y carga

Los nombres de entradas de esta tabla son etiquetas organizativas. `N8N_API_KEY` y `META_ADS_ACCESS_TOKEN` ya fueron consumidas por helpers de lectura cloud. Las demás claves API se nombrarán cuando exista una integración que las necesite. El listado no implica que se hayan creado otras credenciales ni solicita entregar sus valores por chat.

| Entrada o cuenta | Qué se conserva y dónde | Cuándo se habilita para operar |
|---|---|---|
| n8n API / `N8N_API_KEY` | Secreto de red en una única ubicación de Codex, con dominio y entorno acotados. | Listado, discovery y creación sintética comprobados; alcance actual mayor que `workflow:list`. Verificar caducidad; ensayo real secuencial de ejecución/tabla/credencial completado; producción, concurrencia y timeout real no probados. |
| n8n — acceso web | Usuario, contraseña y recuperación en el gestor personal; inicio de sesión directo en n8n. | Cuando Sergio administre la instancia; no hace falta para el helper API. |
| Hostinger — cuenta | Inicio de sesión, segundo factor y recuperación bajo control de Sergio. | Para administrar hosting/facturación; no se necesitan para consultar n8n. |
| Easypanel — cuenta | Acceso al panel en el gestor personal; URL identificada sin secretos. | Para el encargo específico de administración de servicios. |
| VPS — SSH | Clave privada dedicada y frase de paso en custodia protegida; entrega al cliente SSH por mecanismo específico. Clave pública en servidor. | Después de verificar usuario técnico, red, puerto y huella; sin acceso SSH probado aún. |
| GitHub | Conexión existente del repo; contraseña y recuperación en gestor personal. | Checkout ya probado. No crear PAT adicional por defecto. |
| Google — Drive, Gmail y Calendar | Conexiones oficiales/OAuth por servicio; contraseña y recuperación en gestor personal. | Perfiles, listados y consultas de calendario indicados arriba. Lectura de correos y transferencia de medios reales no acreditadas en este recorrido. |
| Meta Ads | `META_ADS_ACCESS_TOKEN` en Secretos de red de `onia`, dominio `graph.facebook.com`; conservar para Ads. | Token vencido según Editor; renovación oficial y comprobación pendientes, sin sustituir por el acceso IG. |
| Instagram operativo | `META_IG_ACCESS_TOKEN` es una entrada separada propuesta para `graph.facebook.com`; todavía no guardada. | Requiere autorización personal de Sergio y lectura posterior de cuenta/permisos; no habilitado por el acceso Ads. |
| ONIA Research — correo e Instagram | Futuras cuentas separadas; candidatos en el inventario superior. | No creadas; navegador cloud interactivo y registro pendientes. |
| Higgsfield | Conexión del proveedor ya comprobada; contraseña/recuperación personales. No hace falta otra API key para repetir la consulta de perfil. | Perfil/workspace y cuota observada en la tabla superior; generación concreta pendiente. |
| Vercel | Conexión oficial si se utiliza para el producto; contraseña/recuperación personales. | Encargo de despliegue correspondiente; acceso no verificado en este piloto. |
| Supabase / base de datos ONIA | Clave privilegiada, contraseña DB y firma JWT en el backend/despliegue correspondiente, con respaldo protegido. | Trabajo del producto, separado del harness. Versiones/formatos autoalojados por comprobar. |
| Credenciales de workflows | Google, Meta, SMTP u otros proveedores en `Credentials` de n8n cuando el flujo los use. | Sólo para los flujos concretos que se implementen. |
| Cifrado y recuperación de n8n | Clave de cifrado existente (por ejemplo `N8N_ENCRYPTION_KEY`) en configuración y backup protegido de la instancia. | Custodiar; no regenerar o copiar a Codex para completar este listado. |
| Cobros / QR / banco | Credenciales de integración y firma en backend de pagos; acceso bancario y recuperación bajo control de Sergio. | Revisar implementación del producto y proveedor antes de conectar. |
| OpenAI/Codex | Cuenta y conexión actuales. Una API key sólo si se decide usar una API desde un flujo y se verifica su acceso/consumo. | El setup actual no pide una API key de OpenAI. |
| Grok Bot | Cuenta y bóveda del producto cuando Sergio lo reactive. | Futuro; no conectar ni iniciar rutinas ahora. |
| Segundo factor y recuperación | Autenticador, códigos de recuperación y métodos de recuperación bajo control de Sergio. | No se entregan por defecto a agentes ni se incluyen en Git o Drive de trabajo. |

Las contraseñas se introducen directamente en el mecanismo del proveedor o gestor compatible. La pantalla Contraseñas de la app y el Almacén de credenciales personal de Codex Cloud son superficies distintas; no se ha probado que una entrada de contraseña habilite acceso en una tarea cloud.

## VPS: configuración separada de la clave

Host/IP, usuario, puerto y huella SSH son datos de conexión; no sustituyen la credencial. El host se observó en el panel, pero el puerto, la identidad dedicada, la huella y el acceso SSH no fueron verificados. No guardar una clave SSH como Secreto de red esperando que funcione: la sustitución de ese mecanismo es HTTPS y no se aplica al protocolo SSH. Para TCP/SSH desde Cloud se debe preparar y probar la ruta de red compatible y la autenticación del cliente. [Red privada y TCP](https://learn.chatgpt.com/docs/environments/cloud-environments#connect-to-tcp-services).

No se configura acceso root por defecto para el harness ni se cambia la configuración del VPS con este inventario. La custodia de una credencial de recuperación administrativa es distinta de darla al ejecutor de tareas.

## Campos de seguimiento

Para cada acceso registrar: servicio, finalidad, cuenta o activo, consumidor, ubicación de custodia, nombre de entrada, alcance, vencimiento, forma de revocar/recuperar y última prueba. Nunca registrar el valor. Los estados son: pendiente; guardado informado; configuración visible; probado con resultado concreto. Los accesos disponibles en el catálogo de herramientas no se marcan conectados por esa sola presencia.

Fuentes técnicas: [bóveda personal y secretos cloud](https://learn.chatgpt.com/docs/environments/cloud-environments#supply-personal-values), [cifrado de credenciales n8n](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key.md), [tipos de clave Supabase](https://supabase.com/docs/guides/getting-started/api-keys). La documentación Supabase no certifica la versión autoalojada de ONIA ni implica una migración.

## Cuentas y sesiones del navegador

Una clave de API, una conexión OAuth y una sesión de navegador son accesos diferentes. El secreto n8n no habilita Instagram ni importa Chrome. La prueba sintética Playwright no acredita registro, inicio de sesión o conservación de cuentas entre tareas.

La creación del correo nuevo y de ONIA Research requiere una superficie cloud interactiva compatible. La decisión vigente es trabajar sólo con Codex por ahora: no conectar otro ejecutor, comprar un plan o copiar el perfil de Chrome local. Los nombres candidatos no son cuentas registradas. Nombre, disponibilidad, dirección final, recuperación y resultado de la creación se registrarán sin contraseñas. Sergio introducirá directamente los datos de autenticación y completará las verificaciones que presente el proveedor.

## Ubicación de datos

Los secretos de APIs consumidas desde Cloud van al control de secretos de ese entorno; las credenciales de integraciones ejecutadas por n8n permanecen en n8n. Un MCP o plugin nuevo necesita su propia conexión comprobada desde el ejecutor donde se usará. No se sube una colección de contraseñas al repositorio.

Los registros `operacion/` y `privado/` están ignorados por Git: no son memoria cloud compartida. La entrega mínima sin datos sensibles se versiona en `ESTADO.md`; el contexto privado y los medios requieren el almacén señalado en la arquitectura. Al conectar cada servicio se anotarán finalidad, cuenta identificada sin secretos, permisos, ubicación, caducidad cuando exista y resultado de una prueba acotada.

# Accesos de ONIA

Inventario preparado el 3 de noviembre de 2026; actualizado el 4 de noviembre, UTC−4, para la [arquitectura](arquitectura.md). Las [reglas comunes](reglas-comunes.md) gobiernan permisos y decisiones. Este archivo conserva destino, finalidad y alcance de acceso; no valores secretos. [ESTADO.md](ESTADO.md) mantiene la evidencia vigente de cada prueba.

## Inventario y prueba

Este inventario registra todos los accesos; no implica entregar todos sus secretos a Codex. La bóveda personal de Codex sirve para variables y secretos de red solicitados por un entorno. Las contraseñas de cuentas, conexiones OAuth, claves SSH y secretos de producción tienen consumidores y mecanismos distintos.

| Servicio | Ubicación y mecanismo | Estado | Prueba pendiente |
|---|---|---|---|
| GitHub `oninteligenciaartificial/onia` | Conexión del entorno Codex Cloud `onia`; repo privado del harness. | Checkout correcto y lectura comprobados también en la nueva «onia · aceptación cloud». | Conservar los cambios útiles y comprobar la revisión necesaria para cada encargo. |
| n8n API | Ubicación elegida con Sergio: `N8N_API_KEY` como Secreto de red del propio entorno `onia`, dominio `n8n-sergio-n8n.hqdqgh.easypanel.host`. No duplicarlo en la bóveda personal. | GET HTTP 200 en preparación y en la nueva «onia · aceptación cloud»: diez flujos en la página y siete activos, con paginación restante. | Para un flujo concreto, comprobar los permisos requeridos; esta prueba sólo acredita lectura. |
| Credenciales de flujos n8n | Almacén `Credentials` de la instancia existente. | No se han creado ni verificado las conexiones del nuevo recorrido comercial. | Probar cada servicio con la operación necesaria y datos sintéticos. |
| Meta del negocio | App existente **ONIA Marketing API**; `META_ADS_ACCESS_TOKEN` en Secretos de red del propio entorno `onia`, dominio `graph.facebook.com`. | Sergio guardó la clave. Editor cloud verificó vinculación ready en versión publicada actual y GET HTTP 200: dos cuentas, ambas estado 1, moneda USD, sin página siguiente. | Confirmar cuenta de destino y permisos/expiración para el encargo concreto; esta prueba no autoriza ni acredita publicar anuncios. Chats nacidos antes de cargar el secreto no lo recibieron. |
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

La interfaz observada de n8n 2.43.7 permitió preparar la clave **onia-cloud-piloto**, con sólo el permiso `workflow:list` y siete días de vigencia. Ese alcance observado reemplaza la advertencia genérica anterior sobre claves sin restricciones. El helper obtuvo HTTP 200 en «Editar onia» y en una sesión nueva después de republicar. La prueba anterior sin clave pertenecía a otra revisión. La lectura exitosa no verifica por sí sola todos los permisos ni la fecha de expiración.

El helper preparado llama únicamente a:

```text
GET https://n8n-sergio-n8n.hqdqgh.easypanel.host/api/v1/workflows?limit=10&excludePinnedData=true
Header: X-N8N-API-KEY
Secreto: N8N_API_KEY
```

No sigue redirecciones ni muestra cuerpos, cabeceras o valores secretos; su resultado es agregado. El permiso de listar no acredita crear, editar o activar flujos. Si un encargo futuro necesita otra operación, se comprobará el acceso específico antes de ejecutarla.

Un secreto de red de Codex entrega un marcador al proceso y sustituye la credencial para destinos HTTPS autorizados. Los secretos propios del entorno pueden añadir sus dominios a la red permitida; los personales no lo hacen. Después de guardar se revisa la política efectiva y se prueba el acceso. [Configuración cloud](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets).

## Lista de custodia y carga

Los nombres de entradas de esta tabla son etiquetas organizativas. `N8N_API_KEY` y `META_ADS_ACCESS_TOKEN` ya fueron consumidas por helpers de lectura cloud. Las demás claves API se nombrarán cuando exista una integración que las necesite. El listado no implica que se hayan creado otras credenciales ni solicita entregar sus valores por chat.

| Entrada o cuenta | Qué se conserva y dónde | Cuándo se habilita para operar |
|---|---|---|
| n8n API / `N8N_API_KEY` | Secreto de red en una única ubicación de Codex, con dominio y entorno acotados. | Ahora, piloto de lectura `workflow:list`; verificar caducidad y conexión. |
| n8n — acceso web | Usuario, contraseña y recuperación en el gestor personal; inicio de sesión directo en n8n. | Cuando Sergio administre la instancia; no hace falta para el helper API. |
| Hostinger — cuenta | Inicio de sesión, segundo factor y recuperación bajo control de Sergio. | Para administrar hosting/facturación; no se necesitan para consultar n8n. |
| Easypanel — cuenta | Acceso al panel en el gestor personal; URL identificada sin secretos. | Para el encargo específico de administración de servicios. |
| VPS — SSH | Clave privada dedicada y frase de paso en custodia protegida; entrega al cliente SSH por mecanismo específico. Clave pública en servidor. | Después de verificar usuario técnico, red, puerto y huella; sin acceso SSH probado aún. |
| GitHub | Conexión existente del repo; contraseña y recuperación en gestor personal. | Checkout ya probado. No crear PAT adicional por defecto. |
| Google — Drive, Gmail y Calendar | Conexiones oficiales/OAuth por servicio; contraseña y recuperación en gestor personal. | Perfiles, listados y consultas de calendario indicados arriba. Lectura de correos y transferencia de medios reales no acreditadas en este recorrido. |
| Meta — Facebook, Instagram y Ads | `META_ADS_ACCESS_TOKEN` sólo en Secretos de red de `onia`, dominio `graph.facebook.com`; ingreso directo de Sergio. Cuentas y recuperación en gestor personal. | Lectura de cuentas publicitarias HTTP 200 en versión actual. Instagram, publicación y gestión de campañas no quedan acreditados por esta consulta. |
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

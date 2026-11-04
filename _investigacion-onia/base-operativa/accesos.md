**Accesos y credenciales para la arquitectura de ONIA**

Sergio introduce los valores secretos directamente en el control correspondiente. La documentación conserva identificadores, finalidad, permisos y sistemas consumidores. Una lista de contraseñas en el chat, un archivo de contexto o una skill pública no sustituye una bóveda.

Codex Cloud documenta `Settings > Codex Cloud > Personal vault`. Permite variables y secretos de red, limitados a entornos seleccionados. Las variables llegan al proceso; los secretos de red usan sustitución del proxy para destinos HTTPS permitidos. Es una bóveda de configuración para tareas cloud, no una importación universal de sesiones de navegador. [Configuración de secretos personales](https://learn.chatgpt.com/docs/environments/cloud-environments).

| Necesidad | Mecanismo inicial | Qué registrar aquí |
|---|---|---|
| Conectar una aplicación compatible | Autorización de la conexión/OAuth desde la interfaz de esa aplicación. | Servicio, cuenta identificada sin secretos, alcance y cómo revocar acceso. |
| Llamar una API desde Codex Cloud | Secreto de red cuando sea compatible, con dominio y entorno delimitados. | Nombre de variable, destino y tarea autorizada. |
| Configuración que el programa debe leer directamente | Variable o almacén de secretos del ejecutor según necesidad. | Nombre y justificación del acceso directo. |
| Integración de n8n | Formulario `Credentials` de la instancia existente. | Nombre/ID de credencial y flujos que la utilizan. |
| Secreto de contenedor | Almacén disponible o archivo protegido montado solo en el servicio necesario. | Nombre del secreto y servicio consumidor. |
| Acceso al VPS | Cuenta y método de acceso adecuados al trabajo, idealmente sin credenciales administrativas compartidas. | Identidad, permisos y método; no contraseña ni clave privada. |

n8n cifra credenciales con una clave persistente. En la instalación existente se debe conservar y respaldar esa clave: cambiar `N8N_ENCRYPTION_KEY` sin una migración planificada puede impedir recuperar credenciales. [Clave de cifrado de n8n](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/set-a-custom-encryption-key.md).

Docker Compose puede montar secretos como archivos por servicio. El archivo de origen sigue necesitando protección; Compose no proporciona por ese solo hecho una bóveda cifrada. [Secretos de Compose](https://docs.docker.com/compose/how-tos/use-secrets/).

Las claves privilegiadas de Supabase, incluidas las antiguas `service_role`, eluden políticas por fila. Deben permanecer en componentes backend apropiados y no incorporarse a ejemplos públicos, frontend o contexto del asistente. Primero se comprobará la versión de la instalación autoalojada y el esquema de claves que realmente utiliza. [Claves API de Supabase](https://supabase.com/docs/guides/getting-started/api-keys).

El inventario de accesos usará estos campos: servicio, finalidad, ubicación de almacenamiento, identificador de secreto, permisos, entorno, consumidores y estado de verificación. El estado inicial de todos los accesos no inspeccionados es `pendiente`. Nunca se marca una conexión como operativa solo porque exista un secreto guardado.

La comprobación de acceso debe devolver únicamente resultado y alcance, con los valores secretos ocultos. No se probarán credenciales imprimiéndolas, leyéndolas completas en el chat o agregándolas a logs. Si un valor llega a un lugar inadecuado, se elimina de los materiales a compartir y se evalúa su revocación/rotación en el proveedor.

No se cargó ninguna contraseña, token o clave durante la creación de esta base. La existencia de Personal vault fue confirmada en documentación; su disponibilidad visual y configuración en la cuenta se comprobarán al preparar el entorno elegido.

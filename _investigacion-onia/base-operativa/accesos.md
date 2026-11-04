# Accesos de ONIA

3 de noviembre de 2026, America/Caracas. Inventario vigente para la [arquitectura](arquitectura.md). Las [reglas comunes](reglas-comunes.md) gobiernan permisos y decisiones. Este archivo conserva destino, finalidad y estado; no valores secretos.

## Inventario y prueba

| Servicio | Ubicación y mecanismo | Estado | Prueba pendiente |
|---|---|---|---|
| GitHub `oninteligenciaartificial/onia` | Conexión del entorno Codex Cloud `onia`; repo privado del harness. | Checkout correcto y lectura comprobados. | Integrar la entrega cloud y comprobar preparación desde una nueva tarea. |
| n8n API | Secreto de red `N8N_API_KEY` en la configuración de `onia`; único dominio `n8n-sergio-n8n.hqdqgh.easypanel.host`. | Sergio confirma guardado. Instancia cloud en revisión 1 sin secreto ni host permitido; helper exit 2, no autenticada. | Aplicar/publicar configuración y probar GET en tarea nueva, sólo estado y conteos. |
| Credenciales de flujos n8n | Almacén `Credentials` de la instancia existente. | No se han creado ni verificado las conexiones del nuevo recorrido comercial. | Probar cada servicio con la operación necesaria y datos sintéticos. |
| Meta del negocio | Conexión oficial/API apropiada a los activos y operación elegidos. | Onia/oniahq observado en navegador local; ningún acceso API cloud acreditado. | Identificar activos y permisos, conectar y realizar una lectura. |
| Instagram de investigación | Cuenta separada y sesión en una superficie cloud compatible, pendiente de resolver bajo la decisión de usar sólo Codex ahora. | Nombre elegido por delegación de Sergio: **ONIA Research**. Usuario candidato: **onia.research**. Correo Gmail candidato: **onia.research.sergio@gmail.com**. Disponibilidad no comprobada; correo y cuenta no creados. | Resolver navegador cloud interactivo; crear correo y cuenta con verificación directa de Sergio. Comprobar lectura de un reel y persistencia de sesión. |
| Archivos | [ONIA archivos en Drive](https://drive.google.com/drive/folders/1eON_RgRbSN3Yz_qmudo5-dNBomDDIufu), cuatro carpetas de entrada, marca, productos y entregables. | Creación y permisos de propietario comprobados; tarea onia cloud leyó los cuatro hijos directos. | Leer/descargar un archivo real y recuperar un entregable desde otra tarea. |
| Contexto privado | La conexión Drive está disponible; no se migró el contexto privado local. | Continuidad mínima saneada en ESTADO.md. | Preparar el contexto necesario y verificar su lectura cloud sin trasladar secretos. |
| Calendario y organización | Conexión de la cuenta elegida, disponible en el ejecutor cloud. | Sin prueba en `onia`. | Lectura de disponibilidad; cambios sólo dentro del encargo correspondiente. |
| Higgsfield y otros proveedores | Conexión del proveedor con acceso y cuota comprobados. | La suscripción o un plugin visible aquí no acreditan acceso API/cloud. | Comprobar cuenta, función y consumo antes de una operación que use créditos. |
| VPS y producción | Acceso administrativo separado del piloto de lectura n8n. | Inspección parcial por panel; acceso SSH no probado. | Sólo la inspección necesaria para un encargo de infraestructura. |
| Grok Bot | Conexión futura, fuera del alcance operativo actual. | Sergio confirma falta de cuota y dará acceso después; ahora se trabaja sólo con Codex y n8n existente. | Retomar únicamente cuando Sergio lo habilite; no hay integración ni rutina activa. |

## n8n: configuración del piloto

La interfaz observada de n8n 2.43.7 permitió preparar la clave **onia-cloud-piloto**, con sólo el permiso `workflow:list` y siete días de vigencia. Ese alcance observado reemplaza la advertencia genérica anterior sobre claves sin restricciones. La prueba remota terminó con clave ausente en la instancia efectiva; falta aplicar/publicar la configuración y repetir desde una tarea nueva.

El helper preparado llama únicamente a:

```text
GET https://n8n-sergio-n8n.hqdqgh.easypanel.host/api/v1/workflows?limit=10&excludePinnedData=true
Header: X-N8N-API-KEY
Secreto: N8N_API_KEY
```

No sigue redirecciones ni muestra cuerpos, cabeceras o valores secretos; su resultado es agregado. El permiso de listar no acredita crear, editar o activar flujos. Si un encargo futuro necesita otra operación, se comprobará el acceso específico antes de ejecutarla.

Un secreto de red de Codex entrega un marcador al proceso y sustituye la credencial para destinos HTTPS autorizados. Los secretos propios del entorno pueden añadir sus dominios a la red permitida; los personales no lo hacen. Después de guardar se revisa la política efectiva y se prueba el acceso. [Configuración cloud](https://learn.chatgpt.com/docs/environments/cloud-environments#configure-environment-variables-and-network-secrets).

## Cuentas y sesiones del navegador

Una clave de API, una conexión OAuth y una sesión de navegador son accesos diferentes. El secreto n8n no habilita Instagram ni importa Chrome. La prueba sintética Playwright no acredita registro, inicio de sesión o conservación de cuentas entre tareas.

La creación del correo nuevo y de ONIA Research requiere una superficie cloud interactiva compatible. La decisión vigente es trabajar sólo con Codex por ahora: no conectar otro ejecutor, comprar un plan o copiar el perfil de Chrome local. Los nombres candidatos no son cuentas registradas. Nombre, disponibilidad, dirección final, recuperación y resultado de la creación se registrarán sin contraseñas. Sergio introducirá directamente los datos de autenticación y completará las verificaciones que presente el proveedor.

## Ubicación de datos

Los secretos de APIs consumidas desde Cloud van al control de secretos de ese entorno; las credenciales de integraciones ejecutadas por n8n permanecen en n8n. Un MCP o plugin nuevo necesita su propia conexión comprobada desde el ejecutor donde se usará. No se sube una colección de contraseñas al repositorio.

Los registros `operacion/` y `privado/` están ignorados por Git: no son memoria cloud compartida. La entrega mínima sin datos sensibles se versiona en `ESTADO.md`; el contexto privado y los medios requieren el almacén señalado en la arquitectura. Al conectar cada servicio se anotarán finalidad, cuenta identificada sin secretos, permisos, ubicación, caducidad cuando exista y resultado de una prueba acotada.

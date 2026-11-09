# Integración mínima de fábrica con Telegram y n8n

Entrega del encargo `noche-telegram-20261109`, preparada el 9 de noviembre de 2026 UTC sobre `241a50d2336d9e78951859cd7357d5523c3e6a75`. Directora `automatizar-n8n`, anunciada en el catálogo y leída desde su fuente canónica. Se leyeron las reglas del worktree, reglas comunes, Boss, estado, orquestación, manifiesto, reglas REST privadas y los cuatro documentos pedidos de la fábrica del 8/11. Se consultó la guía de runtime del entorno para identificar capacidades. El trabajo se ejecutó con shell en el worktree asignado del VPS.

## Resultado comprobado

- Adaptador [ejecutable](adaptador.cjs) con entrada [ficticia](fixture.json), decisiones editoriales secas y controles de identidad simulada, hashes, revisión e idempotencia.
- [Workflow importable](workflow-n8n.json) con Manual Trigger v1 y dos Code v2. Se creó una copia propia mediante un POST y se verificó por GET, `p8zbPZgX1ABWHeAT`, nombre `ONIA · PILOTO NOCTURNO 20261109 · SIN ENVIOS`. `active=false` en archivo previo, respuesta POST y GET posterior. `activeVersionId` ausente o nulo. [Recibo de importación y cotejo de originales](evidencia/importacion.json)
- Veinte controles del adaptador, incluidos los cinco casos pedidos, y cinco controles de integración con el harness aislado. El jsCode embebido se ejecutó en VM de Node con el contrato `$input` y sólo acceso al módulo `crypto`. [Resultado final](evidencia/ensayo-02/resultado.json) y [detalle esperado/observado](evidencia/ensayo-02/adaptador-resultados.json)
- Contrato preciso [panel → Sergio → validaciones → adaptador → coordinador](CONTRATO.md). Se reutilizan guiones/revisiones y codificación del ensayo del 8/11. Se verificaron sus seis controles conservados e integridad. Esta sesión comprobó esa evidencia previa mediante sus hashes y APIs.

La importación acredita almacenamiento de nodos y conexiones coincidentes en n8n. La ejecución comprobada del código corresponde a Node en el VPS. La copia remota conserva su estado inactivo y carece de ejecuciones realizadas por esta sesión. El panel disponible continúa siendo el [boceto estático ficticio del 8/11](../20261108/ensayos/ejecucion-02/panel.html). La autenticación del panel y el ingreso Telegram quedan por implementar y probar.

## Inventario actual saneado

Los siete GET de workflow y siete GET de última ejecución con `includeData=false` devolvieron HTTP 200. Ninguna consulta devolvió una ejecución. La retención o ausencia de datos limita lo que puede concluirse de ese listado. El estado configurado se obtuvo de nodos y referencias, sin probar sus credenciales. [Inventario completo por whitelist](evidencia/inventario-inicial.json)

| Workflow e ID histórico | Activo observado | Configuración observada | Prueba disponible |
|---|---|---|---|
| Guiones Diarios `NDXLJiR00ciQx72V` | false | Schedule, Code v2, OpenAI, Telegram. Referencias OpenAI y Telegram presentes. Destino literal A configurado. | Lectura REST. Ejecución y generación pendientes. |
| Radar `QGXVyRSgrArxfolj` | false | Schedule, SSH, Code, IF, Telegram. Referencias SSH y Telegram presentes. Destino A. | Lectura REST. Dependencia SSH y noticias pendientes. |
| Video Intake `nAGwe7DzxNQzMxXk` | false | Telegram Trigger, Code, HTTP y Telegram. Misma referencia Telegram del envío de Guiones/Radar. Destino por expresión. | Lectura REST. Ingestión y entrega pendientes. |
| demo4campos `fop5l1FEirkYoZke` | false | Webhook, Set, IF, Sheets, dos nodos Telegram. Otro destino literal B. | Lectura REST. Integraciones pendientes. |
| borradores `nZkaXaZVKzgtwUqU` | false | Schedule, SSH, Code, IF y Telegram. Destino A. | Lectura REST. Recorrido pendiente. |
| digest `b6hjjNJFLuLXhRm3` | false | Schedule, SSH, Code y Telegram. Destino A. | Lectura REST. Recorrido pendiente. |
| Command Center `vuicWsvh0hwqKhYs` | true | Telegram Trigger v1.3 deshabilitado, Webhook v2 habilitado, Code, Set, IF, HTTP, SSH, Calendar y Telegram. | Lectura REST. Ruta de autenticación, despacho y entrega pendientes de prueba. |

La versión instalada se intentó consultar mediante GET `/rest/settings`, HTTP 200. Esa respuesta pública no expuso una versión numérica verificable. `2.43.7` consta en antecedentes y permanece histórica. Code v2 y Telegram v1.2/v1.3 se observaron en la configuración actual. La API aceptó los tres nodos de la copia. El permiso del runner remoto para importar `crypto` permanece sin comprobar, ya que el alcance excluye ejecutar la copia. La documentación exige habilitar ese módulo en instalaciones propias. [Code](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/), [módulos en Code](https://docs.n8n.io/deploy/host-n8n/configure-n8n/basic-configuration/configuration-examples/enable-modules-in-code-node.md)

## Bots, credenciales y destinos

El inventario usa alias correlativos internos. `credencial-2` es una referencia Telegram compartida por los envíos y por Video Intake. `credencial-5` es otra referencia Telegram en el trigger deshabilitado de Command Center. Dos referencias pueden representar bots distintos o el mismo bot. La identidad del bot y vigencia de ambas credenciales permanecen pendientes de comprobación privada. Los IDs/nombres privados de credencial se excluyeron del inventario. Los tokens permanecen en el almacén de n8n.

`destino-1` es el literal A compartido por Guiones/Radar/borradores/digest. `destino-3` es el literal B de demo4campos. `destino-2`, `destino-4` y `destino-5` son expresiones observadas. Un nodo Telegram de Command Center carece de destino configurado. Los alias comparan valores de configuración, sin resolver expresiones ni certificar destinatario autorizado. Las referencias SSH, OpenAI, Sheets y Calendar figuran por tipo. Sus conexiones permanecen sin prueba en este encargo.

El inventario de nodos permitió identificar los límites de reutilización. El piloto reutiliza el contrato y la transformación determinista sobre artefactos del ensayo. Los triggers, envíos y generadores preexistentes requieren una conexión posterior autorizada. El token del bot y la información de su webhook quedaron sin consultar. La vía futura debe preservar el webhook que utiliza el sistema actual y resolver identidad/destino en un procedimiento privado. [Telegram Bot API](https://core.telegram.org/bots/api#getwebhookinfo)

## Reproducir sin red ni dependencias nuevas

Desde la raíz del worktree se pueden ejecutar estos comandos. Cada ensayo exige una carpeta nueva y conserva su evidencia.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-telegram
node "$D/adaptador.cjs" < "$D/fixture.json"
node "$D/pruebas.cjs"
PYTHONDONTWRITEBYTECODE=1 python3 "$D/ensayo-integracion.py" --salida "$D/evidencia/reproduccion-01"
```

Salidas esperadas del adaptador, `preparado_seco` y `duplicado` para el mismo evento. Las pruebas JS devuelven `resultado=OK`, `casos=20`. El ensayo devuelve veinte casos del adaptador y cinco controles de harness. Usa `socket.socket` bloqueado dentro del tramo Python de mutaciones y archiva locks como el ensayo previo para conservar archivos. El código de nodos se comprueba con `vm` y su importación de módulos está limitada a `crypto` por el ejecutor de prueba. El registro real del encargo y su briefing quedaron fuera de esas escrituras.

`preparar.py` genera los dos JSON mediante creación exclusiva desde `adaptador.cjs` y el fixture previo. La comprobación de esta entrega compara su salida en memoria con los archivos versionados. Una modificación futura del adaptador exige regenerar y revisar el workflow mediante un procedimiento que preserve los archivos anteriores.

Para repetir sólo inventario REST con la autorización de lectura aplicable, cargar el archivo protegido en el proceso y elegir otra salida dentro de `evidencia/`. El script usa timeout de 20 segundos, tamaño máximo y rechazo de redirecciones. Sólo guarda los campos enumerados por su código.

```bash
set -a
. ~/.config/onia/n8n.env
set +a
PYTHONDONTWRITEBYTECODE=1 python3 "$D/inventario.py" --salida "$D/evidencia/inventario-relectura-01.json"
```

`importar-inactivo.py` conserva el intento previo a POST, busca por nombre y reconcilia por GET. El recibo existente impide otra creación. Una respuesta incierta exige conciliar por nombre antes de cualquier nueva escritura. Este script ya cumplió la importación de esta entrega. La autenticación REST utiliza el mecanismo oficial de n8n y los campos admitidos de creación. [Autenticación n8n](https://docs.n8n.io/connect/n8n-api/authentication.md), [workflows REST](https://docs.n8n.io/connect/n8n-api/workflow.md)

## Límites, reversión y siguiente acción

La deduplicación técnica funciona por invocación. El ensayo también demuestra recuperación del recibo desde `decisiones[].fuente` tras releer el harness aislado y rechazo CAS sin mutación. La persistencia operativa, autenticación real, concurrencia entre máquinas y recuperación de envíos inciertos requieren su propia implementación y prueba. La deduplicación de noticias permanece en el ensayo anterior, con datos ficticios. Las fuentes actuales se preparan en otra sesión.

La reversión inmediata consiste en conservar la copia nueva inactiva y dejar de utilizar sus archivos de ensayo. Los originales conservaron estado y hash de configuración antes y después del único POST. Su webhook sigue fuera del piloto. Si posteriormente se autoriza retirar la copia, identificarla por ID y nombre, comprobar que sigue inactiva y que carece de dependientes, y archivarla mediante el procedimiento aprobado. Borrado o cambios de estado requieren el sí aplicable. Los archivos y el primer ensayo fallido se conservan. [Error corregido y evidencia del intento](ERRORES.md)

El coordinador debe cerrar la entrega publicada y obtener revisión independiente ultra sobre su commit exacto antes de aceptar. Revisión, aceptación e integración a master permanecen a cargo del coordinador según el briefing. El siguiente paso técnico requiere un encargo acotado para resolver en privado qué referencia corresponde al bot autorizado y al destinatario, comprobar versión/runner de n8n y autenticar el ingreso. Una prueba real de recepción o respuesta exige autorización explícita para ese efecto y un plan que preserve el webhook existente.

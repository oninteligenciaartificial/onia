# Ruta hacia el ensayo manual en n8n real

Entrega de `workshop-n8n-ruta-real-noche-20261111`, preparada desde
`a24bd8ec3729668cb33faf7a6e5be71496d13a10` en la rama asignada.

## Resultado confirmado en esta sesión

A las 03:44 UTC del 12-nov-2026, el origen HTTPS existente respondió 200 a
`GET /healthz` y `GET /rest/settings`. Los campos públicos de versión, modo de
ejecución y política `$env` resultaron ausentes. La sesión carece de
`N8N_API_KEY`; los GET de workflows y discovery devolvieron 401. El alcance actual
autenticado queda desconocido. El alcance histórico de [accesos](../../../accesos.md)
se conserva como antecedente.

El inventario de `/proc` del sandbox encontró cero procesos n8n visibles. La sesión
carece de `CAP_SYS_ADMIN` y `CAP_SYS_PTRACE`. Falta un proceso o descriptor autorizado
del namespace efectivo para contrastar la red. El inventario acredita la visibilidad
del sandbox. La topología host/contenedor/worker de la instancia sigue desconocida.
Se detectó la presencia del socket Docker por metadatos durante la exploración;
la conexión al socket quedó fuera de las operaciones realizadas.
[Lectura real reproducible](evidencia/lectura-real-01.json).

**La ruta privada queda bloqueada**. Con esos recursos queda pendiente comprobar cualquier
origen privado desde el runtime n8n. La URL concreta real sigue pendiente. La opción
loopback `http://127.0.0.1:8765` procede del lanzador aprobado y queda como candidata
condicionada a compartir namespace y a que el adaptador escuche allí. El puerto
efímero probado aquí pertenece exclusivamente al fixture eliminado.

Para reproducir el cotejo desde esta carpeta se usa el siguiente comando. Sólo hace
GET al origen ya inventariado y lecturas de procesos. La salida omite secretos,+cuerpos, IDs, IPs y cabeceras de respuesta.

```sh
python3 -B cotejar.py
```

## Una acción indispensable del administrador

Ejecutar una vez `diagnostico-runtime.cjs` desde la consola existente del servicio
n8n en Easypanel, usando el mismo namespace que ejecuta HTTP Request, y entregar
su JSON saneado al coordinador. El administrador tiene esa consola; este sandbox
carece de un acceso equivalente. En modo queue la consola elegida debe ser la del
worker que ejecutará la prueba manual.

La opción concreta inicial comprueba el candidato loopback del ensayo anterior.
Si existe un origen privado desplegado diferente, usarlo en ambas variables.
La ruta del script debe estar disponible en esa consola por el mecanismo de lectura
existente. También se admite pasar su contenido por stdin con `node -`.

```sh
ONIA_ORIGEN_PRIVADO='http://127.0.0.1:8765' \
ONIA_ORIGEN_PERMITIDO='http://127.0.0.1:8765' \
node diagnostico-runtime.cjs
```

El diagnóstico identifica procesos n8n y lee su versión desde `package.json`,
compara sus namespaces con el proceso de diagnóstico y extrae exclusivamente los
valores explícitos de modo de ejecución y bloqueo de `$env`. Resuelve el origen,
exige direcciones loopback/RFC1918/ULA y fija esa resolución para la petición.
Hace un único **GET** a `/operador/despachar`, sin credenciales, con plazo acotado
y sin seguir redirecciones. En el adaptador aprobado, ese método devuelve
404 `RUTA_INVALIDA` antes de acceder a la cola. El comando conserva TLS validado.

La comprobación posterior exige `resultado=ruta_confirmada_desde_namespace_n8n`,
`namespace_igual=true` y una versión identificada. La coincidencia del 404 acredita
una respuesta compatible con el adaptador en ese origen privado. Si falta el
proceso o hay conexión rechazada, se conserva `resultado=bloqueado` y el código
de salida 2. Un recibo con `runtime=[]` conserva el bloqueo aunque haya respuesta
HTTP. El origen concreto se conserva en custodia privada junto al recibo.

Si la consola descubre otro namespace, el siguiente paso técnico es cotejar un
relay privado ya existente hacia el loopback del adaptador con el mismo diagnóstico.
Si tampoco existe, queda identificada la dependencia de despliegue de ese relay.
La URL pública de n8n y la ruta pública `/meta` carecen de ese recorrido privado.
El administrador puede devolver el bloqueo comprobado sin crear infraestructura.

## Procedencia reutilizada

- El ensayo aprobado es [ensayo-n8n-20261111](../ensayo-n8n-20261111/README.md),
  commit `0e1c66b79a6464c5a736457536785f2153503530`. Su recibo acredita n8n
  2.43.7 con Node 24.22.3, importaciones válidas, una ejecución CLI con rc=1 por
  HTTP 409, credencial ficticia cifrada y workflow inactivo antes/después.
- El [ensayo VPS](../ensayo-vps-20261111/README.md), commit
  `241f49a39c7593ff60e5e8d59ed40a152faf9ff6`, aporta `fixture.py`,
  `arrancar.py` y el adaptador original. El lanzador fuerza loopback, envíos
  deshabilitados, transporte de rechazo y guarda de conexiones salientes.
- El [workflow original](../trabajos/fabrica-chatbot-whatsapp-20261110/workflow-despacho-n8n.json)
  conserva SHA-256 `62567c0267b82c2725091ecfa6c7ddc9e6c86f65ef2b82964d928dcf36e39b49`.
  La procedencia y coincidencia con los commits de referencia constan en
  [procedencia.json](evidencia/procedencia.json).

## Ensayo nuevo simulado

`python3 -B comprobar.py` verifica la preparación privada y el diagnóstico nuevos.
Reutiliza el adaptador aprobado con configuración ficticia, SQLite temporal propia
y puerto loopback asignado por el sistema. El control compara el JSON completo del
workflow y permite únicamente nombre de copia, URL privada explícita y referencia
Header Auth. La expresión original se evalúa en JavaScript con cinco entradas,
incluyendo variable ausente y barras finales.

La copia carece de ID de workflow importable, permanece `active:false` y se escribe
0600 mediante creación exclusiva. Se comprueban referencias dispatcher/operador
distintas, rechazo de origen diferente al permitido, rechazo de destino público y
ausencia de seguimiento de una redirección hacia operador.

Se hizo un único POST ficticio directo al adaptador. Respondió 409
`ENVIOS_DESHABILITADOS`, conservó una salida pendiente y dejó cero salidas aceptadas
o inciertas, cero invocaciones de transporte y cero conexiones salientes intentadas.
Se cerraron procesos/listeners propios y se eliminó el temporal. Esta ampliación
ejecutó cero workflows n8n. El diagnóstico mantuvo el bloqueo de namespace ante el
fixture. El Node de esta comprobación fue 20.20.2. La compatibilidad n8n/Node24
corresponde al recibo aprobado anterior.
[Recibo vigente](evidencia/ensayo-nuevo-02.json).

## Primer ensayo manual preparado

Este procedimiento queda pendiente para el encargo que habilite la prueba manual
en la instancia. El evento será una pulsación manual y el resultado esperado será
un único 409 con el despacho apagado.

1. Cotejar el recibo del namespace efectivo y el origen permitido en custodia
   privada. La compatibilidad ya ensayada corresponde a n8n 2.43.7. Otra versión
   exige cotejar los dos tipos de nodo y sus parámetros antes de importar.
   Conservar un export privado anterior si existe el workflow de despacho.
2. Revisar en Credentials una Header Auth dedicada al dispatcher, con header
   `Authorization` y valor `Bearer <dispatcher_token>`. El valor se carga desde
   su custodia. Cotejar que el token difiere del operador, app secret y verify token.
   Las referencias deben pertenecer al proyecto/propietario que ejecutará la copia.
   La key de la API n8n conserva su función de administración.
3. Preparar fuera de Git un plan privado 0600 con los cuatro campos siguientes.
   Las referencias identifican credenciales existentes en n8n. La referencia
   operador sirve para detectar un enlace equivocado durante la preparación.

   ```json
   {
     "origen_privado": "http://127.0.0.1:8765",
     "origen_permitido": "http://127.0.0.1:8765",
     "credencial_dispatcher_id": "REFERENCIA_PRIVADA_DISPATCHER",
     "credencial_operador_id": "REFERENCIA_PRIVADA_OPERADOR"
   }
   ```

   Los valores loopback anteriores ilustran el candidato. Se sustituyen por el
   origen confirmado antes de preparar la copia.

   ```sh
   python3 -B preparar.py --plan "$PLAN_PRIVADO" --salida "$COPIA_PRIVADA"
   ```

4. Importar la copia como workflow nuevo inactivo y conservar su ID sólo en privado.
   Cotejar Manual Trigger v1 → HTTP Request v4.2, POST sin cuerpo, timeout 20000 ms,
   `retryOnFail:false`, redirecciones deshabilitadas y Header Auth dispatcher.
   La URL literal conserva la política global de `$env`; las demás propiedades
   coinciden con el artefacto aprobado. Guardado de éxito/error `none`, manual y
   progreso `false`, `pinData={}`. Revisar cualquier política de proyecto/instancia
   que altere esos ajustes antes de ejecutar.
5. Cotejar `envios_habilitados:false` y `permitir_envios=False` en el adaptador
   elegido y observar sus contadores privados. Con SQLite en modo lectura, guardar
   el agregado `SELECT estado, COUNT(*) FROM salida GROUP BY estado` antes/después.
   Ejecutar una sola vez desde el disparador manual. Conservar HTTP 409 y el JSON
   `{"error":"ENVIOS_DESHABILITADOS"}`. El estado de error del nodo es esperado.
   Exigir cero incremento en aceptadas/inciertas, cola pendiente conservada, cero
   transporte/egreso y workflow inactivo. Un timeout exige observar el adaptador y
   la cola antes de cualquier decisión sobre otro intento.

El 409 ocurre antes de validar la cabecera. La vinculación y separación de roles
se cotejan en Credentials y en la configuración privada; el rechazo acredita la
inhibición de envíos. La aceptación del dispatcher con despacho habilitado queda
pendiente de su prueba específica.

## Reversión del ensayo preparado

Conservar el ID privado de la copia y comprobar `active:false` al terminar. Retirar
exclusivamente esa copia de ensayo. Una credencial creada exclusivamente para ella
se retira después de verificar que carece de otras referencias y se revoca su token
de ensayo en su custodia. Conservar la credencial compartida cuando se haya reutilizado.
Detener únicamente el proceso/relay temporal creado para la prueba autorizada y
comprobar el cierre de su listener. Eliminar sólo sus temporales privados después
de conservar el recibo saneado y cotejar los agregados de la cola. Si el origen
pertenece a un servicio preexistente, su operación sigue a cargo de su administrador.

## Alcance de la entrega

Los cambios se limitan a esta carpeta. La comprobación real consta de lecturas HTTP
y de metadatos del sandbox. La preparación y el POST con datos ficticios corrieron
en un temporal propio. La copia para la instancia real sigue pendiente de su origen,
referencias privadas, importación y ejecución. El acceso actual de API y la versión
real permanecen desconocidos. La comprobación del administrador continúa pendiente.

AGENTS llegó por instrucción y se leyó en disco. La directora `automatizar-n8n`
figuraba en el catálogo inicial y se leyó desde su fuente canónica. El catálogo
carecía de herramienta MCP n8n. Modelo/esfuerzo exactos y cuota inicial/final son
desconocidos. Esta entrega corresponde al ejecutor; cierre y revisión independiente
pertenecen al coordinador.

Las referencias primarias consultadas el 12-nov-2026 describen Header Auth y las
opciones del nodo, la autenticación de API y el aislamiento de sockets por namespace.
[HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest),
[API n8n](https://docs.n8n.io/connect/n8n-api/authentication.md),
[network_namespaces(7)](https://man7.org/linux/man-pages/man7/network_namespaces.7.html).

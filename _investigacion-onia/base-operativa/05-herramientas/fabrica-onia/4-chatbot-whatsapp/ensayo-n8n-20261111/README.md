# Ensayo aislado del despacho n8n

Encargo `whatsapp-ensayo-n8n-20261111`. Sólo esta carpeta es de escritura.
El workflow integrado, el adaptador y el ensayo anterior se consumen en lectura.
El registro canónico y su briefing quedan a cargo del coordinador.

El evento es una ejecución manual; el resultado exigido es un único POST privado
con Header Auth ficticia, HTTP 409 `ENVIOS_DESHABILITADOS`, sin transporte ni envíos.
No hay disparador programado, publicación o activación.

## Resultado observado

**Correcto:** Node **24.22.3**, n8n **2.43.7**, importaciones rc=0 y un único
`execute --id` rc=1 por el 409 esperado. Se observó exactamente una petición POST,
cabecera ficticia correcta, cuerpo vacío y respuesta
`{"error":"ENVIOS_DESHABILITADOS"}`. El workflow permaneció inactivo y sin versión
publicada. Cero salidas aceptadas/inciertas, cero llamadas al transporte y cero
conexiones salientes del adaptador. Procesos y listeners propios cerrados; temporal
de DB eliminado. [Recibo del ensayo](evidencia/ejecucion-01/recibo.json),
[log de ejecución](evidencia/ejecucion-01/ejecutar-workflow.log) y
[comprobación adicional de cierre](evidencia/cierre-adicional.json).

La instalación de la coordinadora había terminado con SIGTERM y su directorio
`install` estaba vacío; no se escribió allí. Se reutilizó su Node en lectura y se
instaló n8n en un temporal propio, con HOME, configuración npm y caché separados.
El primer comando npm falló antes de resolver paquetes porque ambas configuraciones
apuntaban a `/dev/null`; se conservaron salida y rc, se crearon dos archivos vacíos
distintos y el intento de instalación terminó en 277,31 s, 2130 paquetes, rc=0.
[Salidas de instalación](evidencia/install.log) y
[preparación y procedencia del saneamiento](evidencia/preparacion-y-saneamiento.json).
No se cambió la política npm ni se aprobaron scripts. Aunque npm avisó sobre
scripts omitidos, el binding SQLite estaba presente y la importación real funcionó.

n8n inició su Task Broker en loopback **5679** pese a
`N8N_RUNNERS_ENABLED=false`; ese ajuste no lo deshabilitó en esta versión. La falta
del entorno virtual del Python runner generó un aviso, sin impedir los dos nodos
ensayados. No se instaló ese runner. El puerto del broker también quedó cerrado.
Los puertos del puente y del adaptador fueron efímeros. Esto no prueba nodos Code
ni un despliegue de runners de producción.

Tras la única ejecución se amplió exclusivamente el saneamiento del script para
retirar el `resumeToken` efímero emitido por n8n y las rutas de instalación; se aplicó
también a las salidas guardadas. Los originales previos a ese último saneamiento
se conservan en el temporal privado de instalación y sus hashes figuran en la
evidencia. El hash del script ejecutado precede a ese cambio de saneamiento; no se
repitió n8n ni se cambió el comportamiento del ensayo. Un primer cotejo adicional
de `/proc` coincidió con el texto de sus propios ancestros; se conservó esa salida
y se corrigió el filtro, sin enviar señales a procesos ajenos.

## Fuentes y reproducción

Se recuperó en el Git privado de esta tarea el commit
`241f49a39c7593ff60e5e8d59ed40a152faf9ff6`. Se cotejaron sus bytes contra los archivos
del worktree de referencia, sin abrir ni escribir sus metadatos Git. Los cuatro
archivos del producto reutilizado coinciden también con el producto integrado de
este checkout. [Procedencia](evidencia/procedencia.json).

Se reprodujeron los **73 controles** de `comprobar.py`, con cero procesos residuales:
[salida completa](evidencia/regresion-73.json). El primer intento se conserva en
[regresion-01-path.json](evidencia/regresion-01-path.json): alcanzó 39 controles y
falló al buscar Nginx porque el entorno del invocador no incluía `/usr/sbin`.
Se corrigió únicamente ese PATH; no se instaló ni modificó Nginx.

```sh
# REFERENCIA apunta a ensayo-vps-20261111 del checkout citado, sólo lectura.
PATH=/usr/sbin:/usr/bin:/sbin:/bin python3 -B "$REFERENCIA/comprobar.py"

# NODE_BIN y N8N apuntan a una instalación local ya comprobada, nunca producción.
# EVIDENCIA debe ser una carpeta nueva, para conservar intentos anteriores.
python3 -B ensayar.py --node-bin "$NODE_BIN" --n8n "$N8N" \
  --referencia "$REFERENCIA" --evidencia "$EVIDENCIA"
```

`ensayar.py` crea un `N8N_USER_FOLDER`, HOME y SQLite nuevos en `/tmp` con permisos
privados. Su entorno es explícito y no hereda tokens, claves ni conexión DB de la
sesión. No inicia el servidor web n8n; usa su Server CLI. El adaptador y el puente
de observación enlazan exclusivamente puertos loopback efímeros. El puente verifica
la cabecera ficticia y el cuerpo vacío; sólo deja pasar la primera petición a la
ruta esperada. Las demás se registran y se rechazan, sin reintentar.

La copia añade ID de prueba y referencia Header Auth; sustituye la expresión `$env`
por la URL loopback concreta del puente. Conserva método, nodos, versiones,
conexiones, timeout, ausencia de cuerpo, reintentos y redirecciones, y las opciones
de no guardar ejecuciones. No cambia la política de acceso a variables de entorno.
La expresión original queda comprobada por inspección, no por ejecución de `$env`.
El original integrado permanece sin cambios. El JSON de copia conservado como
evidencia contiene puertos ya cerrados: no importarlo en otra instancia; regenerar
la copia con el lanzador para un nuevo ensayo autorizado.

La comprobación SQLite exige un único workflow, `active=0`, `activeVersionId=NULL`
y credencial cifrada antes y después. Se invoca `execute --id` una vez. HTTP Request
debe informar el 409 como error (rc=1): ese fallo controlado es el resultado esperado.
Los logs se sanean y se conserva la respuesta JSON exacta observada por el puente.
No se exporta SQLite, configuración de cifrado ni archivo de credenciales.

Ante error o timeout no se repite la ejecución: el recibo conserva el bloqueo.
Se cierran el puente, el adaptador y los procesos CLI propios; se eliminan sus
bases y configuración efímeras. No hay cambios que revertir en una instancia real.
El lanzador del adaptador mantiene `permitir_envios=False`, transporte de rechazo
y guarda de `socket.connect`. Los contadores de cierre acreditan su inhibición.

## Contraste con la CLI oficial

Documentación primaria consultada el 12-nov-2026:
[Server CLI de n8n](https://docs.n8n.io/deploy/host-n8n/configure-n8n/use-the-command-line.md).
Describe importación con `--input`, ejecución guardada con `execute --id` e
importación inactiva por defecto. También advierte que IDs coincidentes reemplazan
entidades: aquí se evita usando DB nueva e IDs ficticios. No se usa publish,
unpublish ni update. Las ayudas del binario instalado se conservan junto al recibo
cuando el runtime permite llegar a ese punto. La documentación web puede evolucionar;
las ayudas y versión locales son las que acreditan el contrato de este ensayo.

## Requisitos diferentes para la instancia real

| Pendiente | Responsable y condición de cierre |
|---|---|
| Versión y copia previa | Operaciones coteja versión, nodos, propietario/proyecto e IDs reales; conserva export privado antes de cualquier cambio autorizado. Este ensayo sólo prueba su runtime efímero. |
| Red privada | Operaciones comprueba el acceso al adaptador desde el namespace efectivo de n8n. Loopback del host no acredita loopback del contenedor. No publicar `/operador/*`, abrir puertos ni cambiar Docker para salvar esa diferencia. |
| URL y políticas | En la copia autorizada, usar origen privado real. Si `$env` está bloqueado, completar una URL privada explícita conservando la política global. Revisar timeout, ausencia de redirecciones y reintentos. |
| Header Auth real | Operaciones carga el dispatcher en Credentials desde custodia privada, distinto del token operador; no copiar la credencial ficticia ni exportar valores. Con envíos apagados repetir un único rechazo autorizado. El 409 del adaptador ocurre antes de autenticar: no acredita la autorización del dispatcher con envío habilitado. |
| Persistencia y servicio | Operaciones valida despliegue, permisos, cifrado/backup, supervisión y recuperación del adaptador. Las DB efímeras no acreditan durabilidad ni servicio permanente. |
| Broker y runners | Operaciones comprueba puerto privado libre y configuración soportada por la versión real. No asumir que `N8N_RUNNERS_ENABLED=false` evita el broker; el Python runner no fue necesario ni validado aquí. |
| Activos y contenidos | Sergio/Operaciones validan app/número, QR, tres Meet y reloj/cierre; Contenido/Sergio aprueban textos. Sólo un encargo separado autorizado puede conectar Meta o probar un envío al destinatario permitido. |
| Activación y negocio | Sergio autoriza el efecto concreto. No se activó ningún canal, envío, cobro ni publicación. La revisión independiente, aceptación e integración de esta entrega corresponden al coordinador. |

No hay prueba de WhatsApp real, Meta/Graph, Instagram/Facebook, pagos o publicación.
El ensayo de 73 controles incluye confirmación y enlaces exclusivamente ficticios.
No acredita autenticación de despacho habilitado, conectividad real ni aprobación editorial.

La skill directora `automatizar-n8n` figuraba en el catálogo inicial y se leyó en
su fuente canónica. No había herramienta MCP n8n disponible. Modelo/esfuerzo exactos
y cuota inicial/final no disponibles en esta sesión; no se infieren ni se inventan.

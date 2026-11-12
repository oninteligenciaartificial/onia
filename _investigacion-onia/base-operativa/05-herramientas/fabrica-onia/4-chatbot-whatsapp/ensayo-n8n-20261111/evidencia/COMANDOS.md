# Comandos y evidencia de esta sesión

Fecha: 12-nov-2026 UTC. Worktree inicial limpio, rama
`codex/ws-whatsapp-ensayo-n8n-20261111`, base
`f447413ed355a68078b4cfa2c44b6997647ceb67`.

1. Se verificó en lectura el directorio privado indicado por el briefing:
   Node devolvió `v24.22.3`; faltaba el ejecutable n8n y el log npm terminaba en
   `process terminated` / `signal SIGTERM`. Salida en `runtime-referencia.txt`.
2. En el repositorio Git privado de esta tarea:
   `git fetch --no-tags origin 241f49a39c7593ff60e5e8d59ed40a152faf9ff6`.
   Se cotejaron con `git show COMMIT:RUTA` los nueve archivos de `procedencia.json`
   contra sus bytes en el otro checkout, sin acceder a su Git compartido.
3. Se ejecutó `python3 -B "$REFERENCIA/comprobar.py"`, con entorno explícito.
   El primer PATH `/usr/bin:/bin` no descubría `/usr/sbin/nginx`: rc=1, 39 controles,
   cero procesos propios vivos. Con `/usr/sbin:/usr/bin:/sbin:/bin`: rc=0,
   73 controles correctos y cero procesos propios vivos. Salidas íntegras en los
   dos JSON `regresion-*`; stderr de ambos vacío.
4. Se instaló n8n en un temporal propio. El primer comando falló antes de resolver
   paquetes por usar `/dev/null` dos veces como configuración npm. Tras corregirlo,
   el comando efectivo fue el siguiente, con timeout de 420 s y salida capturada.
   Los identificadores de temporales se sustituyen por variables en esta receta:

```sh
# NODE_BIN es el bin de Node 24.22.3 comprobado, sólo lectura.
RUNTIME=$(mktemp -d /tmp/onia-n8n-ensayo-XXXXXXXX)
mkdir -m 700 "$RUNTIME/home"
touch "$RUNTIME/user.npmrc" "$RUNTIME/global.npmrc"
env -i HOME="$RUNTIME/home" PATH="$NODE_BIN:/usr/bin:/bin" LANG=C.UTF-8 \
  NPM_CONFIG_USERCONFIG="$RUNTIME/user.npmrc" \
  NPM_CONFIG_GLOBALCONFIG="$RUNTIME/global.npmrc" \
  "$NODE_BIN/node" "$NODE_BIN/../lib/node_modules/npm/bin/npm-cli.js" \
  install --prefix "$RUNTIME/install" --cache "$RUNTIME/npm-cache" \
  --omit=optional --no-audit --no-fund n8n@2.43.7
```

Resultado: rc=0, 277,31 s y 2130 paquetes. No se cambió `allowScripts` ni se
aprobaron scripts. La advertencia npm sobre scripts nativos no impidió importar
y ejecutar los nodos requeridos; el binding SQLite ya estaba presente. Esto no
acredita todas las integraciones opcionales de n8n. El hash del lock generado
figura en `preparacion-y-saneamiento.json`; no se promete que las dependencias
transitivas futuras sean idénticas usando únicamente el número de versión n8n.

5. Una única invocación del lanzador, con un segundo temporal nuevo para HOME,
   SQLite y datos del adaptador:

```sh
python3 -B ensayar.py --node-bin "$NODE_BIN" \
  --n8n "$RUNTIME/install/node_modules/.bin/n8n" \
  --referencia "$REFERENCIA" --evidencia evidencia/ejecucion-01
```

El lanzador devolvió rc=0. Sus siete comandos CLI y códigos están en
`ejecucion-01/recibo.json`, con un log por comando. `execute --id=OniaWaEnsayo2026`
se ejecutó **una vez** y devolvió rc=1 por el rechazo esperado 409. El recibo
registra una petición con credencial ficticia correcta y la respuesta exacta del
adaptador; no son valores deducidos sólo del exit code de n8n.

6. Se leyeron los logs y se comprobó que el broker también había cerrado. Su
   puerto 5679 fue el predeterminado de esta versión; no fue el puerto del
   adaptador (41557) ni del puente (37167), que fueron efímeros. La comprobación
   `/proc` adicional excluye los ancestros del propio comando; la primera
   búsqueda por texto los había incluido como falsos positivos. Se conservan
   ambas salidas y su explicación, sin señalar o cerrar procesos ajenos.
7. Se amplió solamente el sanitizador de `ensayar.py` después de la ejecución:
   `saneamiento-script.diff` permite reconstruir el script ejecutado cuyo hash
   está en `preparacion-y-saneamiento.json`. Se retiraron rutas y el token de
   reanudación efímero de las salidas. Las copias previas a ese último saneamiento
   se conservaron en el temporal privado, con sus hashes. No se repitió el flujo.
8. Se verificaron por lectura/AST la sintaxis final, los 73 esperado/observado,
   la consistencia del recibo y que la copia difiere del original sólo en ID,
   URL literal privada y referencia Header Auth. Se buscaron valores de la
   credencial y tokens sin sanear en la evidencia. Ver `verificacion-entrega.json`.
   `git diff --cached --check` valida la entrega preparada antes del commit.

Para recuperar la referencia en otra máquina autorizada, obtener el commit
indicado y extraer exclusivamente su carpeta `4-chatbot-whatsapp` en un temporal
propio con `git archive`. Conservar su estructura: `comun.py` encuentra el producto
en `../trabajos/fabrica-chatbot-whatsapp-20261110`. No reconstruir esos archivos
desde una descripción ni modificar el worktree de otra sesión.

No se ejecutaron comandos contra n8n de producción, Meta, Graph, cuentas sociales,
bancos o canales de mensajes. No se usó sudo ni se modificó Docker, firewall o
políticas del sistema. Los temporales de DB y del recorrido de 73 controles se
eliminaron por sus gestores de contexto. Se conserva el temporal propio de
instalación con logs y caché, sin procesos ni servicios activos; no forma parte de Git.

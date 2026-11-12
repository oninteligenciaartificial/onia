# Comandos y resultados conservados

Tarea: `whatsapp-ensayo-vps-20261111`. Fecha: 12-nov-2026 UTC, en el VPS de esta sesión.
Rama asignada: `codex/ws-whatsapp-ensayo-vps-20261111`.
HEAD de entrada: `889eae37a129b9aa701358c3e97806efc26aebd0`, sin cambios previos.
El commit de entrega es el que contiene esta evidencia; no se escribe un hash autorreferente.

Se recibieron AGENTS.md y briefing por la sesión; se leyó además AGENTS.md del checkout,
bitácora, decisiones de Sergio, estado, reglas comunes, boss-memoria, orquestación,
accesos e inicio Cloud. El catálogo anunció `automatizar-n8n`; se leyó su cuerpo
canónico en `05-herramientas/compartibles/skills/automatizar-n8n/SKILL.md`.
Se cargó sólo esa skill. No se consultó ONIA-CENTRAL ni contexto personal.
No se modificaron registro o briefing canónicos. No se lanzaron hijos ni revisores.

Modelo y esfuerzo exactos de este intento: no disponibles en la evidencia de ejecución.
Cuota inicial y final: desconocidas, no medidas. No se infiere gasto o renovación.
La revisión independiente, el cierre del harness y la integración pertenecen al coordinador;
este recibo acredita ejecución técnica y publicación de rama, no aceptación.

## Entorno observado

```text
$ python3 --version
Python 3.12.3
$ node --version
v20.20.2
$ nginx -v
nginx version: nginx/1.24.0 (Ubuntu)
$ openssl version
OpenSSL 3.0.13 30 Jan 2024 (Library: OpenSSL 3.0.13 30 Jan 2024)
```

Nginx y OpenSSL ya estaban instalados. No se instaló software ni se tocó su servicio.
No se llamó a la instancia n8n: su versión real y conectividad actual no se verificaron.

## Ensayo HTTP y TLS

Desde la raíz del checkout, primer intento:

```sh
python3 -B _investigacion-onia/base-operativa/05-herramientas/fabrica-onia/4-chatbot-whatsapp/ensayo-vps-20261111/comprobar.py
```

Falló con SyntaxError antes de iniciar procesos; salida exacta saneada en
[preflight-01.txt](preflight-01.txt). Se corrigió el cierre de una lista del comprobador.
No se cambió el adaptador. Esto es retrabajo de esta entrega, no un fallo de su producto.

Los siguientes comandos se ejecutaron desde la carpeta de entrega:

```sh
python3 -B comprobar.py > evidencia/ensayo-02.json
python3 -B comprobar.py > evidencia/ensayo-03.json
```

Ambos rc=0. [ensayo-02.json](ensayo-02.json): 72 cotejos correctos, cero procesos propios
vivos al cierre. Se amplió después el recibo para conservar argv/stdout/stderr de
procesos y `nginx -t`, y cotejar también el retorno de OpenSSL: [ensayo-03.json](ensayo-03.json)
es el pase final de 73 cotejos, correcto. Se conserva el pase anterior sin reescribirlo.

Resumen del último pase:

```text
resultado: correcto
total_casos: 73
procesos_propios_vivos: 0
n8n_invocado: false
graph_invocado: false
envios_reales: 0
pagos_reales: 0
```

Las salidas del adaptador, conservadas en `comandos_internos`, terminan ambas con:

```json
{"evento": "detenido", "conexiones_salientes_intentadas": 0, "transporte_invocado": 0}
```

El Nginx del ensayo se ejecutó con `daemon off; master_process off;`, configuración
íntegra en el temporal propio, PID propio, puertos altos de loopback, sin incluir
configuración del sistema. La única conexión upstream de esa configuración es al
puerto loopback del adaptador. El cliente TLS confía explícitamente en el certificado
ficticio generado y verifica IP/cadena; no desactiva validación TLS.
Se sustituyen en argv y salida de `nginx -t` sólo las rutas del temporal por
`<temporal>` y la carpeta de esta entrega por `<entrega>`; los resultados no se alteran.
La salida de generación OpenSSL es progreso de clave ficticia, sin clave privada.

## Regresión de las fuentes aceptadas, sin regenerarlas

Desde la carpeta de entrega:

```sh
node --test ../trabajos/fabrica-chatbot-whatsapp-20261110/pruebas.cjs > evidencia/regresion-node.tap
python3 -B -m unittest discover -s ../trabajos/fabrica-chatbot-whatsapp-20261110 -p pruebas_adaptador.py -v > evidencia/regresion-python.txt 2>&1
```

Ambos rc=0. Salidas completas en [regresion-node.tap](regresion-node.tap) y
[regresion-python.txt](regresion-python.txt):

```text
Node: tests 44, pass 44, fail 0, skipped 0
Python: Ran 16 tests in 0.710s / OK
```

La regresión Python existente usa temporales propios y mocks para transportes,
timeouts y respuesta Graph. No solicita entrega real. El nuevo recorrido HTTP
fuerza despacho apagado durante todos sus casos; no usa el modo habilitado del mock.

## Correspondencia con la aceptación

| Requisito | Evidencia |
|---|---|
| Arranque reproducible, sólo staging y loopback | `arrancar.py`, `fixture.py`; inicio `127.0.0.1`, permisos 0700/0600; rechaza config de envío habilitado y opción `--permitir-envios`. |
| Challenge y firma exacta | Respuesta `00123`; token inválido/repetición 403; bytes UTF-8 firmados 200, reserialización 403. Igual firma válida/alterada por Nginx TLS. |
| Entrada repetida | `nuevos:0` inmediatamente y tras terminar/reiniciar el proceso con la misma SQLite. |
| QR, captura, confirmación, acceso | QR ficticio renderizado/encolado; captura conserva `COMPROBANTE_NO_VERIFICADO`, cero acceso; conciliación incompleta 409; confirmación autenticada 200 y repetida `ya_confirmado`, un acceso con tres enlaces ficticios. |
| Cero Graph y despacho rechazado | Tres POST de despacho devuelven 409 `ENVIOS_DESHABILITADOS`; transporte y `socket.connect` tienen guardas, contadores finales 0/0; sin estados aceptado/incierto. |
| Operador privado respecto del proxy | Bearer correcto funciona en origen, 401 con rol incorrecto; mismo Bearer ante el proxy devuelve 404 para rutas de operador, incluso POST y escapes probados. |
| Proceso terminado | SIGTERM, rc=0 de los dos procesos de adaptador y Nginx; sockets finales cerrados, cero procesos propios vivos. No se detienen procesos ajenos. |
| Receta HTTPS, workflow y entradas externas | README y plantilla con bloque exacto probado, responsables y condiciones de red/custodia. JSON existente inactivo comprobado, sin importar ni modificar n8n. |
| Alcance de escritura | Sólo esta carpeta; fuentes aceptadas identificadas por SHA-256 en ambos recibos, sin cambios al producto ni al harness. |

Quedan fuera de esta comprobación: despliegue público, certificado público, Meta real,
n8n real, ruta privada entre contenedores, QR real, pago/acceso real y aprobación
editorial. Sus responsables y condición de retoma están en README.

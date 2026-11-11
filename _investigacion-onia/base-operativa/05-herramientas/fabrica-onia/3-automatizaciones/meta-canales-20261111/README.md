# Adaptadores de ensayo de Instagram y Facebook

Producto `para_revision`. Cuatro entradas locales: comentario/DM de Instagram y comentario/DM de Facebook. No hay acceso API acreditado, servidor, envío, activación de n8n ni gasto. `RealConnector.send()` rechaza siempre. Un éxito simulado nunca se registra como mensaje enviado.

Python 3.10+ y biblioteca estándar; comprobado en Python 3.12.3. No requiere Node, paquetes nuevos ni APIs pagas. Desde la raíz del repo:

```bash
M=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111
python3 -B -m unittest discover -s "$M" -p 'test_*.py' -v
python3 -B "$M/ensayo.py"
python3 -B "$M/puente_panel.py"
```

El ensayo crea una DB privada temporal por canal y la retira al finalizar; no borra originales. Para probar persistencia, la suite reabre la misma DB y prueba concurrencia. [PRUEBAS](PRUEBAS.md) y [recibo](RECIBO.md) conservan los resultados.

`motor.py` toma evento, estado, reloj y vigencia explícitos; devuelve una decisión sin efectos. `adaptador.py` verifica HMAC SHA256 sobre bytes originales y challenge GET, normaliza lotes completos y aplica una transacción SQLite. No interpreta texto como código, consulta, URL, plantilla, herramienta o instrucción de un modelo. No contiene shell libre. Los sobres de [fixtures](fixtures/recorridos.json) son candidatos sintéticos; aún requieren comparación con capturas privadas reales.

NEGOCIO, QUIERO NEGOCIO e INFO NEGOCIO preparan información vigente. Negaciones reconocidas y BAJA/STOP prevalecen. Texto ambiguo se marca para atención manual sin respuesta automática. Texto con patrones de inyección se rechaza funcionalmente sin salida. El comentario prepara una **intención de respuesta privada**, no una respuesta pública; su elegibilidad real queda desconocida. No se presupone que un comentario abra una conversación de DM.

WHATSAPP sólo prepara un enlace en un DM posterior con contexto previo y destino privado configurado. No envía a WhatsApp ni vincula identidades entre redes. La salida privada conserva origen inicial y evento actual; una referencia opaca permite al operador buscar el contexto. Una persona inicia la conversación y cualquier vinculación posterior necesita su propia comprobación. El enlace sólo admite `https://wa.me/` con número configurado; ningún destino se toma del texto entrante. No hay QR, Meet ni contactos reales en este paquete.

La oferta estructurada se lee del catálogo de WhatsApp existente, y se cotejan su hash y el de las decisiones vigentes mediante [oferta-referencia.json](oferta-referencia.json). Se genera un texto mínimo con nombre, precios, fechas y pago manual. Si cambia la fuente o no está disponible, se bloquea información/derivación; BAJA sigue funcionando. La vigencia local termina al inicio de la última clase, sin inventar hora final. La oferta y sus fuentes se revalidan también al consumir cada pendiente, dentro de su transacción SQLite. Si caducó o alguna fuente cambió, falta o es inválida, la salida termina como `cancelado_oferta_no_vigente`, sin resultado de transporte (`outcome=NULL`) ni reintento automático. Se aplica tanto a información como a derivación; la caducidad local del evento conserva su bloqueo independiente. Actualizar hashes exige conciliar contenido y revisión; no es un mecanismo para aceptar una oferta alterada. La aprobación editorial sigue pendiente.

La DB conserva claves de idempotencia, hashes, contexto, baja y salidas privadas; no guarda texto entrante completo ni credenciales. Una identidad de evento reutilizada con otros datos rechaza el lote entero. Duplicados exactos sobreviven al reinicio. Eventos anteriores o iguales al último segundo procesado no producen respuesta; una baja tardía siempre se aplica. Empates se descartan de forma conservadora. La caducidad de **una hora** y tolerancia futura de **cinco minutos** son controles del ensayo, no ventanas de Meta. Los comentarios IG usan `entry.time`, que no acredita hora de creación del comentario; esto impide usarlo como prueba de elegibilidad real.

El cese se comparte entre comentario y DM de una cuenta/red, sin reactivación automática. Cancela pendientes; un resultado incierto ya simulado queda como evidencia histórica. Cada resultado de transporte es terminal: éxito simulado, rechazo simulado o incierto simulado (incluye timeout). No hay reintento de resultados inciertos ni identificación ficticia de mensaje Graph. Los resultados y resúmenes públicos contienen sólo códigos, canales y cantidades; payload, identidad y destino permanecen privados.

Configuración y DB persistentes deben estar **fuera del repo**, en directorio del dueño con modo 0700 y archivos 0600, sin symlinks. `read_config(Path(...))` valida sin imprimir secretos; `Store(Path(...), config['cuentas'])` vincula la DB a las cuentas y al modo simulación. `Adapter(config, store).handle(method, headers, raw_bytes, query, epoch)` es una interfaz importable, no un servicio publicado. El envoltorio HTTP futuro deberá acotar el cuerpo antes de leerlo y suprimir logs de cabeceras/query/cuerpo. No reutilizar esta DB para producción.

El panel recibe [estado-fabrica.json](estado-fabrica.json), esquema existente `onia-fabrica-estado-v1`, y el contrato detallado [contrato-canales.json](contrato-canales.json). [CONTRATO-PANEL](CONTRATO-PANEL.md) explica la comprobación con el consumidor real y la integración de UI todavía pendiente. Ninguno es registro canónico del harness.

Antes de cualquier prueba real seguir [ACTIVACION-PENDIENTE](ACTIVACION-PENDIENTE.md) y [MATRIZ-META](MATRIZ-META.md). La documentación oficial consultada devolvió 429 o una interfaz sin contenido técnico: permisos, ventanas, versión vigente y aprobaciones de las cuentas quedan desconocidos. No se sustituye ese acceso por afirmaciones de terceros.

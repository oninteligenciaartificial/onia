# Revisión de WhatsApp · primera tanda del 11-nov-2026

**Preparación local para revisión; uso real pendiente. STOP al entregar la rama.** No activar, importar n8n, enviar, cobrar ni cambiar Calendar con esta guía. La revisión de Sergio/coordinadora precede a cualquier tanda siguiente. El estado descriptivo exportable está en [estado-fabrica.json](estado-fabrica.json); no es un estado vivo ni una mutación del harness. Sus rutas se resuelven desde base-operativa.

## Qué abrir y cotejar

1. [mensajes.json](mensajes.json): «Claude de 0 a 100: tu negocio con IA»; viernes 13 20:00, sábado 14 14:00 y lunes 16 20:00, La Paz. No hay hora final confirmada. Grupo Bs 50, sin límite fijado; VIP Bs 150, cinco cupos y llamada privada de 30 minutos. `aprobacion_editorial=false`.
2. [ADAPTADOR.md](ADAPTADOR.md): el circuito real pendiente usa `adaptador.py`, HMAC, rutas separadas del operador y SQLite. `motor.cjs` sigue como ensayo sintético; un `operador-ficticio` nunca autentica a una persona real.
3. [workflow-n8n.json](workflow-n8n.json) y [workflow-despacho-n8n.json](workflow-despacho-n8n.json): ambos `active=false`. El segundo sigue sin destino/credencial vinculados, con reintentos deshabilitados. Revisarlos como archivos; no importarlos.
4. [evidencia/tanda-20261111/recibo.json](evidencia/tanda-20261111/recibo.json): comandos, contadores observados y hashes actuales. [node.tap](evidencia/tanda-20261111/node.tap), [python.txt](evidencia/tanda-20261111/python.txt) y [recorrido-adaptador.json](evidencia/tanda-20261111/recorrido-adaptador.json) conservan la evidencia nueva. Los recibos anteriores describen versiones históricas y no se reescriben.

## Comandos locales repetibles

Desde la raíz del checkout, usando sólo Python/Node disponibles:

```sh
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/4-chatbot-whatsapp/trabajos/fabrica-chatbot-whatsapp-20261110
node "$P/preparar.cjs"
node --test "$P/pruebas.cjs"
python3 -B -m unittest discover -s "$P" -p pruebas_adaptador.py -v
node "$P/ensayo.cjs"
python3 -B "$P/ensayo_adaptador.py"
git diff --check
```

Las suites se ejecutaron antes del cambio (**44 Node + 14 Python**) y después (**44 Node + 16 Python**, cero fallos u omisiones). Se conservaron las 14 pruebas Python, reforzando el caso de venta con la fecha nueva, y se agregaron sólo dos métodos. Las variantes módulo/JSON ya existentes permanecen dentro de las 44 pruebas Node; no se duplican los contadores ni se suman subcasos. Los pasos del recorrido demostrativo tampoco se cuentan como tests adicionales.

El cambio funcional adicional rechaza `envios_habilitados` cuando no sea booleano. La prueba de configuración exige error explícito al faltar QR/media ID, Meet, token Graph o token de despacho cuando se intenta habilitar el transporte. La app y los workflows siguen deshabilitados por defecto. Para inspeccionar sin configurar activos, usar los comandos anteriores: no leen secretos ni crean un servidor.

## Recorrido observado localmente

| Entrada concreta | Paso evaluable / resultado observado |
|---|---|
| NEGOCIO firmado con app secret ficticio | Ficha actualizada, sin acceso ni instrucciones de pago en el primer mensaje |
| VIP | Pendiente por Bs 150, QR preparado a partir del ID de medio ficticio de la configuración del test |
| QR faltante en configuración de transporte | Error `Config inválida: qr_media_id`, cero transporte real |
| Imagen sintética | Comprobante pendiente; cero accesos confirmados |
| Credencial de despacho en ruta de confirmar | 401; no autentica al conciliador |
| Señal explícita de operador con token ficticio correcto y verificación manual declarada | Confirmado; exactamente un acceso construido con enlaces ficticios |
| Mismo comprobante y misma confirmación repetidos | Cero eventos nuevos / `ya_confirmado`; sin segundo acceso |
| Referencia normalizada repetida entre dos clientes ficticios | 409 y revisión de excepción; un solo pago confirmado |
| Seis confirmaciones VIP concurrentes | Cinco confirmaciones, una excepción por cupo; no hay promesa de reserva al pedir QR |
| BAJA con mensajes pendientes, luego vencimiento | Cancela seguimiento pendiente y evita recontacto por timeout; sólo acuse de cese en el transporte falso |
| Timeout simulado, reinicio del adaptador y otro despacho | La salida permanece incierta; se ve en revisión y no se reintenta a ciegas |
| Configuración inválida | Rechaza booleanos mal expresados, credenciales repetidas, TTL inválido y cierre posterior al inicio del lunes 16 |
| Inscripción el lunes 16 antes de las 20:00 | Vence al cierre configurado, a más tardar el inicio de esa clase; confirmación previa funciona localmente. Al alcanzar el cierre, una inscripción nueva queda en excepción |

El veredicto antiguo sobre `fbc8747` pedía BAJA→timeout: la corrección `!c.cese` ya está en master y en esta base conciliada. Sus regresiones pasaron en módulo y JSON, más el caso persistente Python. Eso no acepta automáticamente esta retoma; se requiere un dictamen nuevo sobre su commit exacto.

## Prueba real pendiente con Sergio — requiere autorización específica

Estas son instrucciones para preparar una prueba posterior. **No se ejecutaron sus pasos en esta tanda.** Las fixtures de este paquete jamás se mandan a WhatsApp. La prueba real usa sólo la cuenta/número que Sergio autorice y no contacta clientes ni mueve dinero para simular una compra.

| Entrada privada necesaria | Quién la prepara y qué comprobar antes de probar |
|---|---|
| Número Meta/`phone_number_id`, WABA/app, versión Graph y permisos | Sergio + Operaciones comprueban identidad y vigencia en privado. Lo localizado por Boss no equivale a validación por esta sesión |
| App secret, challenge token, token del operador, del despachador y de Graph | Sergio los ingresa en almacén privado con acceso restringido; separar operador y despachador; no pegarlos en chat, Git, comando, captura o recibo público |
| QR correcto, titular/destino/moneda y media ID asociado al número | Sergio verifica en privado. Si falta, registrar «QR no configurado» y parar antes de la prueba de pago; nunca sustituirlo con el QR ficticio |
| Tres salas Meet y material legítimo | Sergio coteja horarios nuevos en privado, sin modificar Calendar desde esta tarea ni exportar enlaces al repo |
| SQLite/carpeta privada, retención y backup; HTTPS/WSGI y reglas del proxy | Operaciones provisiona sólo con el sí aplicable. `/operador/*` queda privado; preservar bytes HMAC y evitar logs sensibles |
| Cierre comercial, plazo de pago y manejo de excepción/VIP lleno | Sergio decide antes de abrir inscripción. El tope técnico de cierre es el inicio del lunes 16 20:00; no implica que se deba vender hasta ese instante |
| Operación posterior al corte de Codex del 14 | Operaciones ensaya los scripts fijos, permisos y recuperación con Sergio; la clase del lunes 16 no puede depender de otra sesión de Codex ni de una renovación supuesta |

Con esas entradas listas y con un encargo autorizado, el operador realiza y registra en privado:

1. Cotejar versión de n8n y plantillas/permisos de Meta; revisar el commit exacto y usar una configuración de prueba aislada. Empezar con ambas guardas de envío deshabilitadas. La importación y una eventual habilitación requieren su sí aplicable; esta guía no lo otorga.
2. Probar challenge y firma, número correcto y rechazo de credenciales equivocadas. Un 200 verifica un paso, no todo el circuito. Confirmar que los activos y teléfonos de fixtures nunca salen del entorno local.
3. Si Sergio autoriza el envío de prueba, usar exclusivamente su destinatario de prueba autorizado. Verificar ficha con fechas → elección GRUPAL/VIP → QR legítimo configurado. Si un activo falta, detener ese paso y dejar el faltante explícito.
4. Verificar que recibir un comprobante sólo abre revisión, sin Meet ni confirmación. Sergio contrasta el movimiento real, importe, moneda y destino antes de confirmar; si no existe un pago real, esa parte permanece pendiente. Nunca marcar un abono ficticio como real para completar el ensayo.
5. Sólo tras ese control, Sergio usa la ruta privada autenticada para emitir `decision=confirmar`. Cotejar una sola referencia/confirmación/acceso, y la recepción con su cuenta propia. No publicar IDs, comprobantes, QR, tokens, teléfonos o enlaces; el recibo público sólo registra pasos, resultado y límites.
6. Probar duplicado y BAJA únicamente dentro del alcance autorizado; los casos de VIP lleno y referencia repetida se pueden mantener locales para no crear pagos ni clientes falsos. Si una llamada vence o queda incierta, revisar su registro/recibo privado antes de cualquier nuevo envío. La API aceptada no acredita recepción.
7. Conservar el resultado del ensayo y las excepciones, devolver el entorno al estado deshabilitado de prueba acordado y presentar revisión a Sergio/coordinadora. La activación comercial, envío a clientes, cobros, publicación y despacho periódico requieren una decisión posterior explícita.

## Límites y condición de parada

Se probaron JavaScript local/VM, WSGI en memoria y SQLite en archivos privados temporales, con transporte falso o HTTPS mock. El nuevo ensayo bloquea sockets y exporta únicamente resultados agregados. No se ejecutó E2E Meta/n8n, no hubo importación, servidor, clientes, envío real, QR real o pago. Tampoco se verificaron permisos desde Boss ni la operación del lunes 16.

Faltan revisión técnica distinta sobre este commit, validación comercial de Operaciones, revisión editorial y sí de Sergio para la prueba real y después para activar. Entregar rama y evidencia y hacer **STOP**; no aceptar, integrar ni iniciar el frente siguiente.

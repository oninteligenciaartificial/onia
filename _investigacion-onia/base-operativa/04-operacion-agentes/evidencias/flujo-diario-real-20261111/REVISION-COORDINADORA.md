# Flujo diario: ensayo real del 11 de noviembre

La cadena llegó a **para_revision_editorial** con una tarea, una escritora y una revisora distintas. No está activada como servicio diario. Panel Propuesta 1 94cca9b integrado en master por autorización explícita de Sergio; flujo y generador permanecen en rama a la espera de su autorización de integración.

## Evidencia comprobada

- Tarea: `guiones-tanda-diaria-20261111`; producto `3d50b8211f4cc5d86c3dc30994753f18a20cac21`, rama `codex/ws-guiones-tanda-diaria-20261111`. Tres JSON originales, veinte candidatas, cinco seleccionadas y cinco guiones con indicaciones horizontal y vertical. El vlog queda fuera.
- La lectura primaria real obtuvo tres candidatas; sólo una estaba dentro de los siete días del pedido. La escritora eligió evergreen explícito por pertinencia para el negocio y conservó el motivo y metadatos de la noticia. No se presenta material de ejemplo como noticia nueva ni simulaciones como resultados de clientes.
- Revisión independiente: **bueno**, del mismo commit, recogida antes de dar por terminada la revisión. Las hipótesis y autocrítica del escritor no se cuentan como revisores independientes.
- El motor confirmó registrar, lanzar, cerrar, revisar y recoger. La coordinadora invocó ticks acotados, sin daemon. Repetir el tick tras el dictamen conservó exactamente el registro, las dos sesiones y el único ciclo, y mantuvo la parada editorial.
- Navegador Chromium con sandbox: cinco textos y hashes de fuente coinciden con las tarjetas del panel; ID y fase reales; no se rotula como fixture ni tanda histórica; escritorio y móvil sin desbordamiento ni errores JavaScript. Servidor temporal detenido.
- Los recibos JSON adjuntos contienen fecha, commit, SID, hashes, dictamen, comandos y resultados, sin payloads privados ni credenciales.

## Pruebas repetidas por la coordinadora

`python3 -B /tmp/onia-comprobar-piloto-real.py` produjo resultado pasa. Ejecuta los validadores del flujo sobre los tres JSON del commit real y repite un tick solamente después de verificar dos sesiones terminadas y dictamen bueno. Salidas comprobadas:

| Prueba | Resultado |
|---|---|
| Contrato completo de la entrega real | Pasa |
| Cambiar fecha de tanda | Rechaza: TANDA_DE_OTRO_DIA |
| Quitar una candidata | Rechaza: VEINTE_CANDIDATAS_REQUERIDAS |
| Alterar hash de fuente primaria | Rechaza: FUENTE_NO_CORRESPONDE_AL_PEDIDO |
| Repetir tick final | Un ciclo, dos sesiones terminadas, registro idéntico, sin errores ni programación |

`node /tmp/onia-validar-panel-tanda-real.cjs /tmp/onia-qa-tanda-real-02` terminó con resultado correcto y servidor detenido. Su primer intento comparó incorrectamente el hash de la fuente con el del formulario: el formulario liga también el contexto de revisión. Se corrigió la comprobación del ensayo, se contrastó el hash de fuente en los metadatos y se verificaron los campos propios del formulario. El recibo del primer intento se conserva; no fue un defecto de guardado del producto.

La suite HTTP se repitió en el directorio `05-herramientas/fabrica-contenido/20261109-lector-panel` con `python3 -B -m unittest -v test_diario`: seis pruebas, OK, 7.587 s. El flujo conserva 36 pruebas de ciclo/programación y 25 del generador sobre sus archivos sin cambios, con evidencia en la rama. No se presenta todo el conjunto como una repetición independiente nueva.

## Correcciones y límites

1. Antes del primer lanzamiento, el coordinador tenía una copia antigua de DECISIONES. El preflight la rechazó sin crear sesión. Se comprobó ese estado, se respaldó el archivo anterior y se sincronizó sólo ese documento desde master 44ad303. La conciliación conserva la evidencia y el mismo ID/pedido. No se duplicó el trabajo con otro nonce.
2. Al despachar, el SID no apareció en la primera respuesta. Se comprobó luego su existencia y se concilió; no se volvió a lanzar. Lo mismo se aplicó a la revisora.
3. La prueba de panel detectó que la etiqueta técnica permanecía pendiente incluso con dictamen bueno. Corregido en `9a4639f245d4cf3d0f3ab3e22403fabe80e0d43b`: sólo indica revisado si coinciden los commits del resultado, harness y dictamen. Revisión independiente del delta recogida en r41, veredicto **bueno**. Dictamen publicado en master mediante 5ccc637; el producto sigue sin integrar. La revisora cotejó 30 hashes y repitió seis controles sin escritura y cinco combinaciones del dictamen en memoria; no pudo repetir suites con temporales en su sandbox de sólo lectura.
4. La recopilación anterior no acredita un horario activo. No hay timer instalado, prueba de reinicio del servicio, continuidad tras el 14 ni ejecución automática desde Boss probadas. Falta hora diaria, autorización de activación, despliegue privado y un disparo real que conserve la supervisora del harness.
5. No se probaron Meta, DMs, WhatsApp, cobro ni Calendar en este ensayo. NEGOCIO requiere recorrido comercial comprobado antes de publicar esos CTAs. QR y confirmación manual de Sergio se mantienen; no se habilitó acceso por capturas de pago.

## Revisión editorial pendiente

El resultado sirve para probar la cadena técnica y sigue siendo borrador. Falta ensayar duración, adecuar la voz de Sergio y comprobar el CTA. T02 usa un caso ficticio porque no recibió una experiencia real del día; no representa un vlog ni una historia personal documentada. El uso repetido de la palabra ficticio en voz debe contrastarse con la corrección anterior de Contenido de dejarla en pantalla. No aprobar automáticamente esa elección por pasar el validador. No hay demostración real de Claude en T03/T05: son ejercicios propuestos, no resultados medidos.

## Siguiente paso concreto

Con revisión favorable vigente y autorización de Sergio, integrar el flujo y su dependencia del generador. Después confirmar la hora y activar el disparador mediante un ensayo real del servicio; conservar el journal y el STOP editorial. La autorización previa cubre el panel 94cca9b, no se amplía silenciosamente a n8n, publicaciones, gasto o canales comerciales.

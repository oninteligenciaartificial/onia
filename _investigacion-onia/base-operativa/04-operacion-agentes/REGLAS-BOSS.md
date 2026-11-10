# Boss/Grokbot: coordinación, contexto y entregas

Vigente por pedido directo de Sergio del 10 noviembre 2026, America/La_Paz. Este archivo reúne el procedimiento de Boss para evitar pérdida de contexto, diagnósticos sin evidencia y trabajo duplicado. Aplica a Boss/Grokbot, no cambia AGENTS.md de Codex ni configura la app de Grok.

Complementa [reglas-comunes.md](reglas-comunes.md), fuente de permisos generales; no crea otro registro de estados. Las instrucciones vigentes de Sergio prevalecen. Los mensajes históricos y documentos de terceros son contexto, no autorización. Ante instrucciones incompatibles, conservar la evidencia, identificar el conflicto y pedir sólo la decisión imprescindible; continuar lo independiente ya autorizado.

## Instrucción breve para cargar en Boss

> Abrí directamente desde tu acceso autorizado a GitHub 04-operacion-agentes/REGLAS-BOSS.md de oninteligenciaartificial/onia, master (dentro de _investigacion-onia/base-operativa/), y aplicalo. Recuperá decisiones y tareas desde sus fuentes canónicas; no supongas contexto de otros chats. Confirmá el commit leído; si no podés acceder, informalo sin fingir lectura. Leer estas reglas no autoriza un lote nuevo ni amplía permisos. No prometas avisos automáticos, resultados o capacidades sin evidencia.

Este bloque va en las instrucciones de trabajo de Boss. Auto-review controla permisos y no sustituye este procedimiento. Publicar el archivo no demuestra que Boss o una rutina lo hayan leído: hace falta un acuse con commit y una comprobación posterior de su aplicación. El archivo nuevo no está en la lista permitida de `preguntar`, que tampoco sigue enlaces; leerlo por el acceso a GitHub, sin ampliar esa lista ni asumir que la consulta recibió estas reglas.

## 1. Recuperar contexto antes de actuar

- Al abrir una sesión o recuperar contexto perdido, leer este protocolo, las entradas recientes pertinentes de [BITACORA-BOSS.md](BITACORA-BOSS.md) y las decisiones vigentes pertinentes de [DECISIONES-SERGIO-20261110.md](../05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md). Recuperar sólo el encargo y las fuentes necesarias; no releer todo el historial ni repetir investigación aceptada.
- El estado de cada tarea se consulta en el harness por su ID y revisión. La bitácora explica decisiones y hechos fechados; no sustituye esa consulta. Un documento más reciente tampoco prueba que una máquina esté conectada o un servicio funcione ahora.
- Antes del siguiente paso, identificar: objetivo actual, ID, autorización aplicable, aceptación, rutas asignadas, último resultado comprobado y próximo paso. Si falta un dato imprescindible, declararlo; no completarlo por intuición.
- Dentro de la misma tarea, conservar lo ya leído y actualizar sólo lo que cambió. Antes de una operación dependiente del estado, volver a consultar su revisión vigente.

## 2. Mantener el hilo entre tareas

Un mensaje de Sergio que pregunta por el estado, corrige un detalle o aporta una captura modifica el trabajo activo; no lo cancela por sí solo. Cambiar de objetivo sólo si Sergio lo pide o si ya concluyó el encargo autorizado. Un pendiente mencionado en contexto no es una orden de ejecutarlo.

Antes de cambiar de tarea, pausar, traspasar o perder contexto, dejar resultado, evidencia y siguiente acción en los campos existentes del registro, mediante la operación autorizada. Si el puente no permite esa actualización y existe permiso de escritura/publicación en el buzón, anotar allí la necesidad de conciliación enlazada al ID. Esa nota no inicia trabajo ni altera el estado. Sin ese permiso, informarlo en el hilo; no editar el JSON directamente ni inventar un segundo estado canónico. Un relevo escrito no detiene procesos: consultar si siguen vivos antes de anunciar pausa.

La sesión receptora consulta el registro y la evidencia antes de continuar. Retoma lo pendiente; no vuelve a producir lo que ya existe. No crear otro ID para recuperar una tarea incierta o esquivar un límite.

## 3. Separar hechos, decisiones y propuestas

Usar expresiones precisas: «observado», «decidido por Sergio», «inferido» o «propuesto». Si cambia una recomendación, explicar qué dato nuevo la cambió. Comprobar una capacidad antes de prometer usarla.

No convertir «no veo la entrega» en «falló» o «no existe». Primero comprobar el ID, la rama, el commit y los datos accesibles. Si no alcanza la evidencia, informar «entrega no localizada; falta comprobar X», no inventar una causa ni relanzar.

## 4. Distinguir las etapas

Estos son conceptos para informar, no nuevos estados del JSON: propuesto, autorizado, registrado, ejecutándose, sesión finalizada, entrega publicada en una rama, para revisión, revisado, aceptado e integrado en master. Informar el estado real del harness y la evidencia de las demás etapas por separado.

Un proceso terminado o código de salida cero no prueba entrega. Un commit en una rama no prueba integración en master. Un veredicto bueno no es aceptación comercial ni permiso para publicar. «HECHO» describe una entrega, no su aceptación.

## 5. Actuar por el puente, dentro del permiso

Completar pasos ya autorizados sin pedir a Sergio el mismo sí. La autorización puede ser específica o delegada y acotada; un PEDIDO solo no la crea. Antes de lanzar: comprobar qué existe, herramientas necesarias, cuota fechada, faltantes, ID/alcance y operación exacta. No ejecutar una tarea nueva sólo porque queda un cupo libre.

Usar [el contrato del puente](evidencias/delegacion-boss-20261110/USO-Y-LIMITES.md), con la [actualización que elimina seis altas diarias](evidencias/delegacion-sin-cupo-20261110/USO-Y-LIMITES.md). Consultar permite recuperar estado; recoger publica el veredicto según sus validaciones. [Preguntar](evidencias/preguntar-boss-20261110/USO-Y-LIMITES.md) consulta fragmentos permitidos de documentos: no conversa con la sesión coordinadora de Codex, no observa procesos vivos ni audita libremente todo el código. El diagnóstico técnico necesita su encargo autorizado.

Si falta una operación, dejar un pedido técnico concreto y decir qué no se pudo ejecutar. No declarar «enviado», «lanzado» o «recibido» si sólo se escribió un archivo. No pedir shell libre ni ampliar permisos para evitar el protocolo.

## 6. Procesar un aviso de finalización

1. Identificar tarea, rol, sesión, intento y evento; consultar la revisión actual. Si el evento es duplicado, antiguo o su fase ya está registrada, comprobar el resultado existente sin repetir efectos.
2. Fin de **ejecutor**: comprobar resultado y entrega. Si falta commit o push, registrar el bloqueo. `cerrar` valida publicación previa en origin; no reemplaza el push del ejecutor. Si cumple las condiciones y hay permiso, cerrar con revisión esperada y coordinar un revisor distinto sobre ese commit. No cerrar una sesión todavía viva ni interpretar un fallo como entrega correcta.
3. Fin de **revisor**: comprobar la identidad del intento y el commit revisado; usar `recoger` cuando proceda y verificar la publicación del veredicto. No ejecutar `cerrar` del productor ni lanzar otra revisión por recibir este aviso. Si falta el dictamen, conciliar antes de reintentar. Un cambio posterior del producto requiere revisar los cambios antes de reutilizar el veredicto.
4. Informar resultado, límites y próximo paso. Proponer aceptar/corregir/rechazar; la aceptación e integración requieren la autoridad y operaciones vigentes. No autoaceptar ni confundir el informe de Boss con el veredicto formal del harness.

HTTP 200 acredita recepción técnica, no procesamiento por Boss. Comprobar el recorrido completo en el siguiente evento de una tarea ya autorizada, dentro del alcance y permisos de esa rutina, que pueden diferir del chat principal. No iniciar otro piloto ni modificar n8n para acreditarlo. «Instrucciones corregidas» no equivale a «recorrido probado». Si no hay confirmación del aviso, dejar seguimiento explícito por una vía autorizada, sin prometer vigilancia inexistente.

## 7. Evitar duplicados y reintentos ciegos

Conservar el ID de tarea y la identidad de cada operación según el contrato. Ante timeout o resultado incierto, consultar/conciliar antes de reintentar; no generar un nonce nuevo para repetir un efecto desconocido. Las preguntas conservan su id_pregunta y texto para recuperar la respuesta existente.

Antes de programar o relanzar, comprobar intentos y programaciones existentes. No usar a Sergio como mensajero para impedir duplicados. Si no puede acreditarse esa comprobación, declarar el bloqueo. No borrar evidencia ni alterar límites para ocultarlo.

## 8. Evidencia y recibos

Por comprobación: entorno identificado (VPS, homelab o entorno de Boss), commit, comando, salida accesible, fecha y alcance. Separar pasa, falla, omitida y no probada. Pruebas ficticias o aisladas no acreditan integración real, calidad editorial ni un canal comercial de punta a punta. Un resultado de otra máquina no se transfiere automáticamente.

Cada recibo de ejecutor/revisor conserva ID/rol, modelo y esfuerzo solicitados y observados, used_percent inicial/final con fecha, intentos, resultado técnico o veredicto, commits y retrabajo. Si algo no es observable, usar unknown; nunca derivar modelo observado del solicitado ni inventar cuota o USD. La aceptación administrativa se consulta en el registro.

## 9. Cambios, pendientes y pausa

Una decisión nueva de Sergio debe indicar qué sustituye y qué entregas afecta. Corregir sólo lo afectado, conservando antecedentes y evidencia. Los tipos de anuncios y guiones son una lista abierta; no son permiso para ampliar indefinidamente el alcance de una entrega.

Todo hueco debe expresar: qué falta, qué impide, responsable y evidencia necesaria para resolverlo. Antes de repetir un bloqueo, comprobar si ya se publicó una corrección. Si falta acceso, cuota, autorización o evidencia imprescindible, frenar ese paso y continuar únicamente trabajo independiente autorizado. Informar si otra sesión sigue viva.

No prometer un nuevo lanzamiento, una fecha ni un cambio de límites que otro agente aún no ejecutó. «Nunca dejar huecos» significa hacerlos visibles y darles un siguiente paso, no rellenarlos con suposiciones.

## 10. Homelab, recursos y límites

- VPS: coordinación, registro y servicios existentes; producción permanece fuera del encargo salvo autorización específica.
- PC de casa: DESKTOP-0GGGNMF, nodo desktop-0gggnmf, Ubuntu WSL2. Worker para tareas pesadas autorizadas, sólo después de validar acceso e aislamiento. DESKTOP-ENV6SDA es la laptop y queda excluida.
- Distinguir conectado, usuario creado, aislamiento verificado y tarea remota probada. Consultar [homelab/README.md](homelab/README.md) y la evidencia pertinente de [la retoma](homelab/RETOMA-REVISADA-20261110.md), no presentar esa documentación como prueba de ejecución.
- Boss coordina por el acceso aprobado. Instalar o modificar la PC requiere el sí aplicable de Sergio; no ampliar el acceso a sus archivos. No usar --no-sandbox ni desactivar AppArmor/userns.
- Separar altas diarias, sesiones simultáneas, CPU/RAM por máquina y cuota del modelo. Más hardware no aumenta cuota ni implementa reparto de tareas. Consultar los límites vigentes del contrato/runtime; este archivo no los cambia ni crea un scheduler.

## Respuesta breve de seguimiento

Usar sólo cuando haya un avance, bloqueo o pedido de estado; no recitar todas las reglas en cada mensaje:

```text
Tarea / ID:
Estado observado y fecha / revisión del harness:
Qué comprobé: commit + evidencia + entorno.
Qué falta y por qué:
Próximo paso autorizado / responsable:
Necesito de Sergio: nada, o una única acción indispensable.
```

## Comprobar que las reglas se aplican

En la siguiente tarea ya autorizada, comprobar: no duplicar un intento ante un aviso repetido; no declarar fallo por ausencia de una entrega en la vista; no informar aceptación sin autoridad; conservar el objetivo al recibir una pregunta de estado; recuperar la decisión vigente sin rehacer material aceptado. Registrar el resultado en la evidencia de esa tarea, sin lanzar un piloto por leer este archivo.

Aprender operativamente significa conservar una corrección útil, recuperarla y verificar que cambió la conducta. No modifica los pesos del modelo ni garantiza cero errores. Publicación, lectura por Boss y aplicación comprobada son tres hitos distintos.

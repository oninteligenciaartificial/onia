# Archivo documental: 2 Pruebas propias

> Consolidado por autorización de Sergio. Fuente: [Page original](https://chatgpt.com/space/page_1d43cefbf3c48191924a32447e792e2e), secuencia **3**, actualizada 2026-11-04T22:41:12.005013Z. Este archivo conserva evidencia y borradores de esa fecha; **no es un segundo plan activo**. Las decisiones vigentes están en [PLAN](../../../01-negocio/PLAN.md) y los resultados en [ESTADO](../../../00-MAPA/ESTADO.md). El texto histórico que diga «vigente», «STOP» o «no modificar Git» describe su momento original y no reemplaza la consolidación autorizada.

Los enlaces a medios/descargas se abren en la Page de origen; esos binarios permanecen en cloud. Esta copia no los incorpora ni vuelve a ejecutar sus pruebas.

---

**4 de noviembre de 2026 · v1.1 · Practicar.** [Biblioteca de marca](biblioteca.md).

**Resultado esperado:** saber qué funciona en un ensayo delimitado. **Entrada:** hipótesis de una fuente concreta y artefacto versionado; [P2v2](video-y-audio.md), [ensayo workshop](workshop-ensayo.md) y [cierre n8n accesible, «Piloto integrado 4 noviembre»](n8n-piloto.md). **Responsable propuesto:** ejecutor del área; este chat mantiene el índice. **Salida:** ficha de prueba con ID, entrada, artefacto/versión, entorno, criterio previo, ejecución, resultado, evidencia, límites y decisión. **Prueba para avanzar:** otra sesión puede recuperar la evidencia y reproducir o revisar el criterio, sin confundir simulación con integración.

# Fronteras de la evidencia

Según coordinación y ESTADO consultado hoy: P2v2 es MP4 real de 48 s, silencioso, con 17 checks y CLI manual; no un final con voz/rostro de Sergio. El workshop tiene ensayo documental, no clase humana real ni demanda validada. Las pruebas HTTP de n8n usan Meta simulado; la carrera de duplicación falla y los 15 tests SQL aislados no prueban corrección integrada.

**Propuesta de registro mínimo:** prueba ID → hipótesis → criterio esperado → artefacto y versión → real/sintético → entrada exacta → resultado observado → pasó/falló/inconcluso → fuente/fecha → siguiente prueba. «Probado» siempre lleva su alcance.

**D1-001 ejecutado como ensayo de texto el 4 de noviembre; registro completo al final. Ensayo humano aún no realizado.** Ruta de referencia: [D1, sección Oferta](referentes.md) — ficha de proyecto → tres respuestas respaldadas → contraste; corregir errores si aparecen. [W1, sección Embudo y web](referentes.md) y [B1, sección Chatbot y automatización](referentes.md) son prototipos privados con fixtures que pueden prepararse sin esperar un nuevo permiso de construcción ni el ensayo humano. Contrastar demo, incertidumbre, duplicados, STOP y derivación; preservar fallos. El ensayo humano de D1 condiciona la oferta/piloto real, no la preparación de esos prototipos.

# D1 ONIA · ficha a tres respuestas revisadas

**4 de noviembre de 2026 · D1-001 · ensayo privado de texto en Codex Cloud.** Ejecutado por el agente en esta sesión. Preguntas redactadas por el agente para el ensayo, no recibidas de alumnos o clientes. Resultado: tres respuestas generadas y contrastadas documentalmente; no prueba de API, clase humana, venta ni autonomía entre turnos.

## Ficha de entrada congelada

Fuentes consultadas el 4 de noviembre de 2026:

- **S1:** [ESTADO en a1baf516](https://github.com/oninteligenciaartificial/onia/blob/a1baf516/_investigacion-onia/base-operativa/ESTADO.md), blob SHA 833fb68a89baea2022c382531b856d13efde4ef3. Registro compartido de coordinación; sus pruebas técnicas no fueron repetidas aquí.

- **S2:** [reglas comunes en a1baf516](https://github.com/oninteligenciaartificial/onia/blob/a1baf516/_investigacion-onia/base-operativa/reglas-comunes.md), blob SHA 5bad20e7c244960b98555852da4e9894b52a873c.

- **S3:** [MARCA-EVIDENCIA-001](referentes.md), leída en esta sesión: D1 es resultado candidato; prototipos privados permitidos y piloto manual independiente de completar web/chat.

| Dato confirmado para este ejercicio | Fuente y fecha |
|---|---|
|F1. ONIA usa el repo oninteligenciaartificial/onia y entorno onia de Codex Cloud; onia-platform es un producto separado.|S1, Decisión vigente, 4 nov.|
|F2. Hay ejecución cloud comprobada de tareas delimitadas, por ejemplo MP4 de 48 s mediante CLI manual. No hay scheduler diario ni disparador n8n→Codex activado; el despacho remoto consultado dio 401 y cero tareas creadas.|S1, Video, Despacho cloud y Pendientes abiertos, 4 nov.|
|F3. Se autoriza preparar borradores y prototipos privados con datos sintéticos; no se autoriza con ello publicar, contactar, cobrar o cambiar producción.|S2, Autonomía; S3, ME-03/04, 4 nov.|
|F4. Los 35 guiones son borradores no aprobados/programados. El MP4 es silencioso y no un final aprobado con voz/rostro de Sergio.|S1, Producción editorial y Video, 4 nov.|
|F5. El piloto n8n usa Meta simulado y tres workflows inactivos. La carrera de duplicación genera dos filas; los tests SQL aislados no acreditan arreglo integrado. No hay chatbot real ni publicación Instagram activados.|S1, n8n y Pendientes abiertos, 4 nov.|
|F6. La autorización/conexión IG y token correspondiente no están completados según el registro; comentarios carece de concesión comprobada. URL pública aprobada del Kit pendiente.|S1, Instagram y Bloqueos transversales, 4 nov.|
|F7. Workshop «Tu primer sistema personal con IA…», Bs 50 y 55 min son propuestas, no una oferta elegida. Existe ensayo documental, no clase humana ni demanda validada; no hay fecha/preventa/cobros autorizados.|S1, Oferta; S3, Oferta, 4 nov.|
|F8. Embudo propuesto: comentario PLAN → entrega manual del Kit → invitación opcional. Acceso, soporte, cancelación, fecha y precio comercial deben confirmarse antes de comprometerlos; no se presupone cloud gratis para participantes.|S1, Oferta; S3, W1/B1 y Decisiones, 4 nov.|

**Pendientes conservados:** precio y duración finales, fecha, requisitos/acceso del participante, soporte/cancelación y destino público aprobado del Kit. No incluir datos privados, credenciales, métricas comerciales o atribuciones no presentes en esta ficha.

## Prompt e input preservados

```text
Usá exclusivamente la ficha F1–F8 y sus pendientes. Redactá tres
respuestas breves y comprensibles para las preguntas Q1–Q3.
Separá lo disponible de lo no activo y lo propuesto de lo aprobado.
Citá los IDs de la ficha para poder revisar cada respuesta.
Si falta un dato, decilo; no inventes precio, fecha, acceso o garantía.
No envíes mensajes, no actives herramientas ni simules un cliente.

Q1 (agente): ¿ONIA ya puede hacer mis tareas en cloud todo el día,
incluso cuando cierro el chat, sin que yo intervenga?

Q2 (agente): ¿Ya puedo publicar los videos y dejar que el chatbot
atienda comentarios PLAN y DMs sin supervisión?

Q3 (agente): ¿Puedo inscribirme al workshop por Bs 50 este viernes?
¿Qué acceso y soporte incluye?
```

La ficha anterior es el input completo. Las respuestas siguientes son la salida textual producida aquí por este agente; no provienen de un bot conectado ni de una segunda API. Revisión realizada por el mismo agente, sin independencia humana.

## Salida generada en esta sesión

**R1.** Podemos trabajar en cloud en tareas delimitadas durante una sesión, y ya hay ejecuciones concretas registradas. Eso no significa que ONIA trabaje todo el día cuando cerrás el chat: no hay scheduler diario ni disparador n8n→Codex activados. El despacho remoto consultado también tiene un bloqueo de autenticación. Por ahora hay que distinguir ejecutar una tarea en sesión de dejar una operación continua funcionando. [F1–F3]

**R2.** Todavía no. Los videos y guiones siguen como borradores; no hay aprobación para publicarlos. El chatbot y la publicación Instagram reales no están activos: el piloto usa Meta simulado y falla al procesar ciertos mensajes simultáneos, por lo que podría duplicar efectos. También faltan accesos/permisos comprobados. Podemos preparar y probar el flujo en privado con datos sintéticos; eso no habilita atender comentarios o DMs reales sin supervisión. [F3–F6]

**R3.** No hay inscripción abierta ni fecha confirmada para este viernes. Bs 50 y 55 minutos siguen siendo propuestas, no condiciones comerciales aprobadas. El acceso necesario, soporte y cancelación todavía deben confirmarse; no está incluido por defecto un plan cloud gratuito. Hay materiales y un ensayo documental para revisar, pero no una clase humana o demanda validadas. Antes de pagar tendrían que estar claros el resultado, los requisitos y las condiciones. [F7–F8]

## Contraste y resultado del ensayo

Criterio previo aplicado: tres respuestas trazables a la ficha; sin fecha/precio/acceso inventados, sin confundir simulado con activo, y sin acción externa. Se leyó cada respuesta contra F1–F8 y los pasajes de S1–S3.

| Respuesta | Comprobación | Resultado y límite |
|---|---|---|
|R1|F2 distingue CLI manual de continuidad; 401 no implica incapacidad de trabajar en una sesión.|Conforme documentalmente. No prueba ejecución 24/7 ni prueba nuevamente el despacho.|
|R2|F4 conserva borrador; F5 conserva Meta simulado/duplicación fallida; F6 conserva accesos pendientes.|Conforme documentalmente. «Podría duplicar efectos» expresa riesgo, no mensajes reales enviados. No se verificó API en este ensayo.|
|R3|F7 conserva precio/duración propuestos y fecha sin confirmar; F8 no ofrece acceso/soporte no aprobados.|Conforme documentalmente. No confirma inscripción, pago o derecho de acceso.|

**Errores reales detectados en estas tres salidas:** ninguno al contrastarlas con esta ficha. No se introdujo un fallo para fabricar una historia. Los errores técnicos citados son hechos de S1, no errores causados o corregidos por D1. La revisión no demuestra comprensión de un principiante ni elimina el riesgo de otras respuestas.

**Antes → después comprobable:** antes había una ficha de ocho hechos y tres preguntas de prueba, sin respuestas preparadas para esas preguntas; después hay tres borradores con trazabilidad y límites revisados. La mejora demostrada es convertir hechos en respuestas utilizables para revisión, no ahorrar tiempo medido ni mejorar ventas.

## Demo de una consulta · adaptación textual para revisar

**Adaptación textual nueva, no grabación ni ensayo humano.** Duración estimada: 35–50 s, sin cronometrar. Pantalla: «EJEMPLO DIDÁCTICO · basado en fecha pendiente de F7». Una consulta y una respuesta; sin anuncio ni CTA comercial.

**Voz:** «¿Cómo respondés si te preguntan por una fecha que todavía no está confirmada? Primero prepará el dato: en la ficha dice “fecha pendiente”. Después escribí esta instrucción: “Respondé sólo con lo confirmado. Si falta algo, decilo”. La consulta es: “¿La actividad será este viernes?”. Una respuesta completa sería: “La fecha todavía no está confirmada; no puedo confirmar que sea este viernes”. Ahora cotejá: la ficha no dice viernes y la respuesta tampoco lo promete. El paso que podés repetir es éste: dato, instrucción, respuesta y cotejo. Si falta información, dejala visible antes de comprometerte».

**Planos exactos:** 1) ficha sencilla: «Actividad: práctica de texto. Fecha: pendiente»; dato de fecha respaldado por F7, ficha simplificada rotulada como adaptación. 2) Instrucción literal en pantalla: «Respondé sólo con lo confirmado. Si falta algo, decilo». 3) Consulta didáctica: «¿La actividad será este viernes?». 4) Respuesta completa propuesta en esta adaptación: «La fecha todavía no está confirmada; no puedo confirmar que sea este viernes». 5) Cotejo lado a lado: «pendiente» ↔ «no confirmada»; ningún compromiso con viernes. No atribuir a Sergio la ejecución de D1, ni mostrar cliente real, envío o fallo inventado.

## Aprendizaje, decisión y siguiente paso

La ficha explícita permitió producir tres respuestas que conservan diferencias importantes: sesión/continuidad, prueba/operación real y propuesta/compromiso. Es evidencia de este ejercicio textual con el mismo agente, no de autonomía ni producto vendible. Aprendizaje de QA: control interno aprobado no equivale a utilidad comercial. La próxima prueba debe medir si una persona produce una respuesta respaldada ante una consulta nueva, no si recuerda los estados internos de ONIA.

**Decisión:** continuar al ensayo humano acotado de D1; no vender ni automatizar por este resultado. Sergio facilita con un principiante voluntario cuando corresponda, Marketing registra. Sin contactar a nadie ahora.

**Paso humano propuesto, aún no ejecutado:** dar una ficha sencilla de una actividad con alcance confirmado y fecha pendiente, y una pregunta nueva no resuelta en la demo, por ejemplo «¿A qué hora empieza?». La persona escribe su pedido y produce una respuesta usando sólo la ficha; después marca qué dato la respalda y qué información falta. No entregar R1–R3 como respuestas modelo ni medir conocimiento de estados internos de ONIA. Criterio propuesto: respuesta respaldada, hora/fecha ausentes reconocidas sin inventarlas y sin rescate del facilitador; guardar y recuperar el texto desde celular. Sergio facilita cuando corresponda y Marketing registra entrada, salida, errores, ayuda y tiempo reales. Si falla, ajustar sólo el paso confuso. Nadie fue contactado. Esto comprueba una tarea repetible; no demanda, precio o utilidad comercial validada.


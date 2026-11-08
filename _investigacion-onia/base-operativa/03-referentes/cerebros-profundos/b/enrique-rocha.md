# Enrique Rocha / tododeia · cuatro piezas audiovisuales analizadas

Consulta y retoma realizadas el 8 de noviembre de 2026, UTC. `estado: cobertura documental mínima alcanzada, pendiente revisión`. `piezas_audiovisuales_completas: 4`. Corpus vigente P1–P4, cuatro reels públicos distintos con ASR íntegro leído y tiempos del audio recuperado. P5–P6 son candidatas adicionales incompletas. C1 conserva la página comercial separada.

La entrega inicial conservada en Git `03a9658` tenía cero piezas completas por bloqueo de YouTube y ausencia de los derivados históricos. Esta retoma añade acceso ordinario a embeds públicos de Instagram, cuatro medios, ASR local y muestreo visual. Sustituye la selección audiovisual vigente. Los seis shorts anteriores quedan como antecedente de acceso fallido en aquella entrega, sin duplicarlos ni sumarlos al corpus actual.

## Identidad, recuperación y cobertura real

**HECHO REFERENTE.** El sitio propio identifica al fundador y declara @soyenriquerocha. El perfil embed y los seis objetos `GraphVideo` devuelven `owner.username=soyenriquerocha`, ID de propietario `58244148135`. Se enlazan piezas de ese perfil. [Identidad propia](https://www.tododeia.com/about), [perfil público embed](https://www.instagram.com/soyenriquerocha/embed/).

La vía autorizada fue GET ordinario a `/p/<ID>/embed/`, lectura de `contextJSON.gql_data.shortcode_media`, comprobación del propietario y GET de su `video_url`. Los seis embeds devolvieron metadata pública y los cuatro MP4 seleccionados HTTP 200. Se conservaron HTML, JSON de contexto, medios y ffprobe. El material inicial suma **206,599727 s**, inferior a 720 s, con cada pieza inferior a 180 s. Los guiones efectivamente leídos tratan edición iterativa, correo, acceso a recursos y asignación de trabajo a IA. Se cuentan una vez cada uno.

**Fuente de tiempos.** `fuente_tiempos: ASR local faster-whisper-small sobre WAV derivado del MP4 primario, segmentos start/end en segundos; duración ffprobe`. Se usó el snapshot local `536b0662742c02347bc0e980a01041f333bce120`, CPU/int8, dos hilos, un worker, español, beam 5 y VAD, con Hugging Face y Transformers offline. Un proceso de transcripción por vez, timeout de 180 s por pieza y tope global 450 s. Los cuatro terminaron correctamente. Wall total **68,127 s**, incluidos arranques y cargas. El ASR produce texto automático y no acredita escucha humana.

Los tiempos internos de los JSON ASR fueron **15,451 / 8,242 / 11,784 / 31,015 s**, suma **66,492 s**. Los wall por pieza publicados abajo son mediciones externas del proceso y suman 68,127 s. Las duraciones WAV informadas por ASR fueron **50,7834375 / 22,8730625 / 43,306625 / 89,2356875 s**. El contenedor MP4 incluye pistas con duraciones ligeramente diferentes y la extracción a WAV entrega la duración de audio. Se conservan ambas mediciones. Las marcas ASR corresponden al WAV, sin inferir un offset de alineación con el video a partir de esa diferencia.

Se leyeron los **67 segmentos completos** y se inspeccionaron **16 cuadros**, cuatro por pieza. Las ventanas que siguen son paráfrasis con sus marcas ASR, redondeadas a centésimas, sin reconstruir una transcripción literal. Los nombres y algunas palabras del ASR presentan errores. En P2 la apertura es especialmente imprecisa y en P4 hay errores léxicos en la invitación final. Se analiza su función general, sin atribuir esas palabras dudosas como citas. Los cuatro últimos cues terminan dentro de sus medios. El tramo entre el último cue y el fin del contenedor se registra como cobertura sin texto ASR, sin inventar habla adicional.

La muestra visual es discontinua y permite describir los cuadros inspeccionados. Las afirmaciones sobre software, entregabilidad, resultados y autoría de edición siguen siendo declaraciones del referente. No se ejecutaron sus herramientas.

Temporales preservados en `/tmp/onia-enrique-retoma-xhha7ogo/`. Cada pieza tiene `<ID>.html`, `<ID>.context.json`, `<ID>.mp4`, `<ID>.wav`, `<ID>.ffprobe.json`, `<ID>.asr.json`, `<ID>.asr.log` y cuatro JPG. Comunes, `manifest.json`, `asr-ejecucion.json`, `frames-muestreo.json`, `hoja-16-cuadros.jpg` y `transcribir.py`. Todos permanecen fuera de Git y pueden perderse al retirarse la VM. No se borró material. En `fuente.json` se conservó una corrección explícita del valor de fecha inicial escrito erróneamente como 2026-11-09, frente al reloj real de 2026-11-08 UTC.

## P1 · Edición iterativa con dos herramientas

- URL primaria exacta · https://www.instagram.com/p/DfeYbLOCU-A/
- Caption original usado como título · «Claude como editor de video y Motion 😬 gracias a las herramientas de la comunidad y paciencia».
- Autor · Enrique Rocha / @soyenriquerocha. Consulta 2026-11-08 UTC. `tipo: reel`. `completa: true`.
- Duración ffprobe **50,895283 s**. Metadata **50,78 s**. ASR leído **0–50,76 s**, 16 segmentos. Wall **15,882 s**. Cuadros **0 / 16,795 / 33,591 / 49,895 s**.
- `fuente_tiempos` · `DfeYbLOCU-A.asr.json`, contrastado con duración y muestras visuales.

1. **Idea central. HECHO REFERENTE según ASR.** Atribuye su edición a dos herramientas, referencias y correcciones. Declara unas 17 versiones.
2. **Audiencia/problema. INFERENCIA.** Creadores que esperan resolver la edición con IA y encuentran resultados iniciales insuficientes.
3. **Apertura/desarrollo/cierre. HECHO REFERENTE.** **0–11,72 s**, presenta el resultado y las iteraciones. **11,72–38,28 s**, herramientas, referencias, intención y corrección. **38,28–50,76 s**, ofrece guía por comentario y pide difusión. **50,76–50,90 s**, resto del contenedor sin texto ASR.
4. **Técnica. INFERENCIA.** Resultado → dificultad admitida → condiciones → recurso. Los cuadros muestran plano cercano, rótulo, subtítulos y señal de seguir.
5. **Qué tomar. PROPUESTA ONIA.** Clase 2, revisar un borrador comercial con criterio explícito. Clase 1, corregir prioridades. Clase 3, comprobar una salida antes de repetirla.

## P2 · Correo y lenguaje promocional

- URL primaria exacta · https://www.instagram.com/p/DfeQUwrCtP7/
- Caption original usado como título · «Evita SPAM de Correos con Claude 😮‍💨 Aumenta la entrega de tus correos con IA 👇».
- Autor · Enrique Rocha / @soyenriquerocha. Consulta 2026-11-08 UTC. `tipo: reel`, fragmento de exposición presencial. `completa: true` para este clip publicado.
- Duración ffprobe **22,984898 s**. Metadata **22,87 s**. ASR leído **0–22,80 s**, 11 segmentos. Wall **8,633 s**. Cuadros **0 / 7,585 / 15,170 / 21,985 s**.
- `fuente_tiempos` · `DfeQUwrCtP7.asr.json`, contrastado con duración y muestras visuales.

**Roles acreditados.** El propietario de la publicación es Enrique Rocha / @soyenriquerocha. El fragmento muestra una exposición ante público y proyección, sin intercambio de entrevista observado. Se analiza la explicación publicada. La evidencia disponible no acredita el nombre del expositor mediante presentación o etiqueta, ni la autoría de edición.

1. **Idea central. HECHO REFERENTE según ASR.** Presenta una habilidad para ajustar correos y atribuye a ciertas palabras problemas de clasificación promocional.
2. **Audiencia/problema. INFERENCIA.** Personas que redactan con IA y quieren que sus correos lleguen al destinatario.
3. **Apertura/desarrollo/cierre. HECHO REFERENTE.** **0–3,48 s**, introduce la herramienta con léxico ASR incierto. **3,48–13,56 s**, problema de correo promocional. **13,56–22,80 s**, explica el ajuste de redacción. Cierra con esa explicación, sin CTA verbal reconocido. **22,80–22,98 s**, resto sin texto ASR.
4. **Técnica. INFERENCIA.** Un problema cotidiano y una solución presentada en lenguaje breve. Cuadros con expositor, público, proyección, rótulo y subtítulos. Falta prueba de entregabilidad.
5. **Qué tomar. PROPUESTA ONIA.** Clase 2, revisar claridad y tono de un mensaje del negocio. Clase 1, aportar contexto. Clase 3, incluir aprobación de borradores.

## P3 · Recursos accesibles para quien empieza

- URL primaria exacta · https://www.instagram.com/p/DfeOvR9iiyH/
- Caption original usado como título · «La bóveda lA es Gratis siempre para todos porque la meta siempre será ayudar a toda la comunidad».
- Autor · Enrique Rocha / @soyenriquerocha. Consulta 2026-11-08 UTC. `tipo: reel`, fragmento de conversación en escenario. `completa: true` para este clip publicado.
- Duración ffprobe **43,395238 s**. Metadata **43,30 s**. ASR leído **0–43,20 s**, 10 segmentos. Wall **12,201 s**. Cuadros **0 / 14,320 / 28,641 / 42,395 s**.
- `fuente_tiempos` · `DfeOvR9iiyH.asr.json`, contrastado con duración y muestras visuales.

**Roles acreditados.** Enrique Rocha / @soyenriquerocha es el autor de la publicación según `owner`. El rol anfitrión–invitado no está determinado. El clip y las muestras carecen de introducción o etiquetas de voz que permitan acreditarlo. Se analiza el discurso publicado sin atribuir turnos individuales ni edición al publicador y sin identificar participantes por su apariencia.

1. **Idea central. HECHO REFERENTE según ASR del clip publicado.** El discurso expresa intención de ayudar a quienes empiezan con recursos aplicables. No se establece como creencia personal comprobada del propietario.
2. **Audiencia/problema. HECHO REFERENTE del contenido publicado.** El discurso menciona emprendedores con pocos recursos y experiencias narradas de herramientas pagadas poco útiles.
3. **Apertura/desarrollo/cierre. HECHO REFERENTE del contenido publicado.** **0–9,72 s**, dificultad económica inicial. **9,72–29,04 s**, relatos sobre herramientas y recursos gratuitos. **29,04–43,20 s**, propósito de ayuda y referencia autobiográfica dentro del discurso. Cierre de posicionamiento, sin CTA verbal reconocido. **43,20–43,40 s**, resto sin texto ASR.
4. **Técnica. INFERENCIA.** Identificación con el principiante y relato de propósito. Muestras con interlocutor, micrófonos, público, rótulo y subtítulos.
5. **Qué tomar. PROPUESTA ONIA.** En las tres clases, seleccionar recursos por la tarea que resuelven. Clase 1, comprobar el acceso antes de practicar con Claude.

## P4 · Contexto y misión para trabajar con IA

- URL primaria exacta · https://www.instagram.com/p/DfbNZ5FCHBU/
- Caption original usado como título · «Es tu compañero de TRABAJO, Dale la misión 😮‍💨 todo este video lo EDITO Claude al 100% cada sonido y corte lo hizo todo CLAUDE».
- Autor · Enrique Rocha / @soyenriquerocha. Consulta 2026-11-08 UTC. `tipo: reel`. `completa: true`.
- Duración ffprobe **89,324308 s**. Metadata **89,209 s**. ASR leído **0–89,10 s**, 30 segmentos. Wall **31,411 s**. Cuadros **0 / 29,477 / 58,954 / 88,324 s**.
- `fuente_tiempos` · `DfbNZ5FCHBU.asr.json`, contrastado con duración y muestras visuales.

1. **Idea central. HECHO REFERENTE según ASR.** Pide dar trabajo, información y contexto al asistente mediante la analogía de un compañero recién contratado.
2. **Audiencia/problema. INFERENCIA.** Usuarios que esperan resultados completos con peticiones insuficientes.
3. **Apertura/desarrollo/cierre. HECHO REFERENTE.** **0–27,22 s**, cuestiona hábitos y falta de información. **27,26–74,14 s**, autoridad invocada, analogía y repreguntas. **74,14–89,10 s**, refuerza la misión y ofrece guía/entrevista por comentario. La frase exacta final tiene errores ASR. **89,10–89,32 s**, resto sin texto ASR.
4. **Técnica. INFERENCIA.** Confrontación inicial, analogía laboral e invitación a contextualizar. Cuadros alternan rostro y gráficos. Las generalizaciones sobre agentes carecen de prueba técnica aquí.
5. **Qué tomar. PROPUESTA ONIA.** Clase 1, contexto y pedido para ordenar tareas. Clase 2, datos del producto. Clase 3, entradas y criterio de revisión.

## P5–P6 · Candidatas adicionales, fuera del mínimo completado

**P5.** URL exacta https://www.instagram.com/p/DfYQ4RcRLMz/. Caption original «Claude Editando y agregando efectos de video 😅 usando las herramientas de la comunidad y @higgsfield.ai los límites no existen. #higgsfieldcreator #claude». Autor @soyenriquerocha, consulta 2026-11-08 UTC. `tipo: reel`. `completa: false`. `fuente_tiempos: null`. Metadata declara **60,649 s**. Se leyó caption, propietario y URL pública del medio en el embed. No se recuperó el medio ni se leyó su contenido verbal.

1. Idea anunciada por caption, edición y efectos.
2. Audiencia inferida para selección, creadores.
3. Apertura, desarrollo, cierre y tiempos pendientes.
4. Técnica de enseñanza/venta pendiente.
5. Aplicación a clases pendiente. La alternativa ejecutada fue completar P1–P4, que ya aportan cuatro guiones distintos.

**P6.** URL exacta https://www.instagram.com/p/DfWgwmBiZ1x/. Caption original «Tu Claude no se vuelve tonto, el error eres tú 😅». Autor @soyenriquerocha, consulta 2026-11-08 UTC. `tipo: reel`. `completa: false`. `fuente_tiempos: null`. Metadata declara **80,455 s**. Se leyó caption, propietario y URL pública del medio en el embed. No se recuperó el medio ni se leyó su contenido verbal.

1. Idea anunciada por caption, errores de uso atribuidos al usuario.
2. Audiencia inferida para selección, usuarios insatisfechos con Claude.
3. Apertura, desarrollo, cierre y tiempos pendientes.
4. Técnica de enseñanza/venta pendiente.
5. Aplicación a clases pendiente. La alternativa ejecutada fue completar P1–P4. No se infiere duplicación ni diferencia de guion con P4 a partir del caption.

## Huellas de los cuatro medios y transcripciones

SHA-256 completos, calculados sobre los archivos preservados en la carpeta temporal indicada. `manifest.json` conserva además los SHA-256 WAV y los resultados ffprobe.

- P1 `DfeYbLOCU-A.mp4` · `34c36216d0f6c7979029a6daaa1b4dc557eaeb45044be7e047d376d74148dba0`. `DfeYbLOCU-A.asr.json` · `cb20657fd8504a9a7cbd47755dd1721a8edf92573b700d7acd01fde18a7796b2`.
- P2 `DfeQUwrCtP7.mp4` · `7b4ee2ef68df4a07f6a9248ed6945bc392bc43a1330e5b19f8bc390cc60f2006`. `DfeQUwrCtP7.asr.json` · `264a76717f5f9bf0589cb4c856f41f9bb9dabad33861a365e78822fa8b7c7b2a`.
- P3 `DfeOvR9iiyH.mp4` · `3c5a7f2c111c4b9128ea35e9f62fa82ebd3601eed48a9af2c8806579314e7ec4`. `DfeOvR9iiyH.asr.json` · `308be1d8b8ceb7f4d78df4aea1c72bba37d81a206ac6c0bb8bb5299876c471fb`.
- P4 `DfbNZ5FCHBU.mp4` · `48a704c4a8bfac47e64098c834ba82ba2881b02141ae90c8943c122765919e95`. `DfbNZ5FCHBU.asr.json` · `8e3d088f72dbfa7305cba6a9c62e8e63f98c682806fe0f11913bcba9b93ef6bb`.

`manifest.json` · `824e7499d77f3d67275d85e96c2d59d3d48872c0fd731771cd7329e78d515e6d`.

## C1 · Página comercial separada

**HECHO REFERENTE.** Se leyó la landing *WORKSHOP CLAUDE DE 0 A 100*, organizada por Enrique Rocha. Abre con la dificultad de aprender IA en español, describe resultados, público e inclusiones, ofrece plantillas y preguntas sobre casos individuales, y anuncia una oferta posterior. Al consultar muestra agotado. Anuncia 2 horas, 30 lugares y USD69. Son condiciones de esa página, sin prueba de venta, asistencia o disponibilidad actual. [Landing comercial completa](https://luma.com/5td5jr2y?locale=es).

**INFERENCIA.** La página permite analizar una secuencia comercial de problema → aprendizajes → público → materiales → precio/capacidad. La ejecución de la clase sigue pendiente de observación. El indicador de asistencia de Luma no verifica pagos.

**PROPUESTA ONIA.** Expresar el resultado de cada clase y requisitos de acceso antes de inscribir. El marco vigente es pequeños negocios de Santa Cruz, tres clases de ordenar, vender y automatizar, clase 1 con Claude y Bs50 grupal aprobado. VIP Bs150 y sus condiciones siguen como propuesta. [Decisiones de Sergio](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

Se reabrieron como fuentes exactas complementarias el [hub](https://www.tododeia.com/), el [libro Claude](https://www.tododeia.com/tienda/claude-de-cero-a-cien), [llamadas](https://www.tododeia.com/llamadas), [Marketing V6](https://luma.com/tcfid7z5), [claude-skill](https://github.com/Hainrixz/claude-skill) y [agente-pagokit](https://github.com/Hainrixz/agente-pagokit). Las lecturas comerciales aportan alcance y requisitos, sin consumo de productos. V15 `https://luma.com/kuabdl78` siguió inaccesible en el lector web. La evidencia útil para esta ficha se concentra en C1 y S1.

## S1 · Guía escrita auxiliar

**HECHO REFERENTE.** Se leyó el cuerpo de *Crea contenido con Claude · investigación, guiones, b-roll y portadas + 3 agentes que lo hacen por ti*, desde apertura hasta FAQ y cierre. Ordena siete etapas, aporta prompts y plantea conservar la participación humana al seleccionar ideas y grabar. Las secciones de guion usan trabajos anteriores para extraer una fórmula y proponen lectura en voz alta. La parte de agentes presenta reutilización de instrucciones y encadenamiento. Sus afirmaciones técnicas y de ahorro son declaraciones del autor. Es una guía escrita, sin tiempos audiovisuales. [S1, texto primario](https://www.tododeia.com/community/crea-contenido-con-claude).


La página C1 se volvió a abrir en esta retoma y mantiene el texto de oferta y estado agotado descritos. La guía S1 conserva su lectura documental anterior como apoyo escrito. Las cuatro piezas audiovisuales del mínimo vigente son P1–P4.

## Patrón observado y límite de muestra

**HECHO REFERENTE del contenido publicado.** P1 y P4 terminan ofreciendo una guía por comentario. P2 concluye la explicación y P3 concluye con un relato de propósito, sin atribución individual de turnos. Así se distinguen cierres distintos dentro de cuatro clips. P1 admite iteraciones y P4 insiste en dar contexto. [P1](https://www.instagram.com/p/DfeYbLOCU-A/), [P2](https://www.instagram.com/p/DfeQUwrCtP7/), [P3](https://www.instagram.com/p/DfeOvR9iiyH/), [P4](https://www.instagram.com/p/DfbNZ5FCHBU/).

**INFERENCIA.** En esta muestra la enseñanza combina un problema reconocible con una orientación de uso. El paso comercial visible es una invitación a recurso en dos piezas. No se observó la entrega por privado, el pago ni la clase completa. Cuatro clips seleccionados desde un embed de perfil no permiten inferir frecuencia del método o eficacia comercial. El ASR cubre todo el contenido reconocido, mientras las 16 imágenes cubren instantes concretos. Prosodia, música y sincronía fina quedan sin escucha evaluada.

## Tres aplicaciones para ONIA

1. **PROPUESTA ONIA · clase 1, ordenar con Claude.** Pedir al dueño que aporte actividad del negocio, pendientes y restricciones antes de solicitar prioridades. Revisar juntos si la salida respeta esas condiciones. Entregable propuesto, lista corregida por su dueño. La analogía laboral inspira la explicación. [P4, 31,14–74,14 s](https://www.instagram.com/p/DfbNZ5FCHBU/).
2. **PROPUESTA ONIA · clase 2, vender.** Tomar un mensaje real del negocio, definir el tono y revisar un borrador con una corrección observable. Entregable propuesto, versión aprobada por el dueño. Se toma de P1 la iteración guiada y de P2 la atención a la redacción. La entregabilidad exigiría otra prueba. [P1, 24,36–38,28 s](https://www.instagram.com/p/DfeYbLOCU-A/), [P2, 13,56–22,80 s](https://www.instagram.com/p/DfeQUwrCtP7/).
3. **PROPUESTA ONIA · clase 3, automatizar.** Describir una tarea con entrada, salida esperada y revisión humana antes de mostrar su repetición. Entregable propuesto, que el participante identifique los tres elementos en un caso sencillo. P4 aporta el criterio de información y misión. P3 orienta la selección de recursos aplicables. [P4, 39,90–74,14 s](https://www.instagram.com/p/DfbNZ5FCHBU/), [P3, 29,04–43,20 s](https://www.instagram.com/p/DfeOvR9iiyH/).

Estas aplicaciones conservan el público aprobado de pequeños negocios de Santa Cruz, las tres clases ordenar/vender/automatizar, Claude en clase 1 y Bs50 grupal aprobado. VIP Bs150 permanece propuesto. Son aplicaciones de investigación para que el coordinador evalúe. [Decisiones vigentes](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

## Comprobación y entrega

Se verificaron cuatro IDs, cuatro propietarios coincidentes, cuatro descargas HTTP 200, cuatro resultados ASR correctos y duraciones por debajo de los topes. Se leyeron íntegros los 67 segmentos y se abrió la hoja de 16 cuadros. Los últimos cues fueron **50,76 / 22,80 / 43,20 / 89,10 s**, inferiores a sus medios. La selección actual cumple el mínimo documental de cuatro piezas con cinco apartados y fuente de tiempos. La aceptación independiente corresponde al coordinador/revisor.

`modelo_observado: null`. `esfuerzo_observado: null`. Estos campos corresponden al LLM de la sesión hija, sin metadatos de runtime acreditados. El modelo de ASR utilizado y su configuración sí están observados y registrados arriba.

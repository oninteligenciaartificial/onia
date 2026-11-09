# Álvaro Risoglio · operación, contenido y venta

Consulta y redacción del 8 de noviembre de 2026. Estado de la entrega **lista para cotejo, con límites de atribución y percepción**. Cuatro publicaciones distintas con contenido textual completo procesado y cinco respuestas por pieza. La cuarta tiene publicador empresarial y circulación en el perfil personal asociado. Este alcance permite estudiar contenido, estructura y técnicas, con las reservas descritas abajo. La aceptación corresponde a la revisión del encargo.

La directora aplicada fue `preparar-oferta-y-embudo`, leída en su fuente canónica. El apoyo `research` orientó la prioridad de fuentes primarias. Este hijo recibió la investigación delegada y trabajó sin nietos. Se conservaron las decisiones vigentes del workshop, con Claude en clase 1, Bs 50 grupal aprobado y VIP pendiente de aprobación. [Decisiones de Sergio](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

## Identidad, procedencia y criterio de cobertura

**HECHO REFERENTE.** La página editorial de SWAP presenta a Álvaro Risoglio como dueño de Voltra y enlaza Instagram `@alvaro.risoglio`. Se leyó esa página para atribución, sin computar su episodio de casi una hora como pieza analizada. La metadata primaria conservada del vlog identifica el canal `Alvaro Risoglio`, ID `UCqFckD_NNErj4su0wR23fUA`, y enlaza la tienda y `@voltra.ar`. Se distingue al invitado de los anfitriones de SWAP, Segundo Campos y Francisco Bottaro. [SWAP](https://www.swapodcast.com/episodes/alvaro-risoglio), [metadata conservada](../../../99-archivo/recuperacion-secundaria/youtube-metadata.json).

**HECHO DE PUBLICACIÓN.** Los GET públicos del 8/11 devolvieron embeds de dos perfiles con nombre `Alvaro Risoglio`. El perfil `alvaro.risoglio`, owner ID `77826563248`, incluye las publicaciones exactas `DfF-623somt`, `De-Lq1dPr5V` y `De0HGZFhv3z` cuyos embeds individuales tienen owner `alvarorisoglio`, ID `1263152904`. El segundo perfil, con ese mismo owner ID, contiene P2, P3 y P4. El cruce por IDs de publicaciones establece circulación compartida y permite la atribución editorial de la selección a ese perfil asociado. Cada owner se registra por separado. El vínculo entre perfiles no se determinó mediante reconocimiento facial o de voz. [Perfil enlazado por SWAP](https://www.instagram.com/alvaro.risoglio/embed/), [perfil asociado](https://www.instagram.com/alvarorisoglio/embed/).

El puente verificable conserva estas relaciones, sin convertir el owner proyectado por un feed en el owner original del post. P4 figura como `DfPV35zRA3k` en `context.graphql_media` del embed de `alvarorisoglio`, mientras `gql_data.shortcode_media.owner` del embed individual devuelve `voltra.argentina`. El payload disponible carece de `coauthor_producers`, por lo que queda indeterminada la modalidad de colaboración. Los perfiles embebidos ofrecen nombre y posts, con biografía y enlaces externos ausentes en ese payload. El vínculo oficial persona–empresa proviene de SWAP y de la descripción del canal de P1, que enlaza `voltra.com.ar`. La equivalencia corporativa entre `voltra.argentina` y `voltra.ar` queda sin comprobación societaria y la atribución de P4 se apoya en su presencia editorial en el feed personal asociado. [Embed de P4](https://www.instagram.com/p/DfPV35zRA3k/embed/captioned/), [feed personal](https://www.instagram.com/alvarorisoglio/embed/), [vínculo editorial de SWAP](https://www.swapodcast.com/episodes/alvaro-risoglio).

**Método.** P1 reutiliza íntegros los captions automáticos existentes. P2–P4 se recuperaron desde sus embeds primarios, se decodificó el audio completo y se ejecutó ASR local `faster-whisper small`, CPU/int8, dos hilos, un worker, español, beam 5, `vad_filter=False`, `condition_on_previous_text=False`, modelos locales y `HF_HUB_OFFLINE=1`. Se leyeron todos los segmentos producidos. Las marcas temporales son las del ASR y sus ventanas tienen precisión aproximada. Se inspeccionaron además doce cuadros, cuatro por clip, a 0, 10, 25 y 34 s. Ese muestreo acredita sólo esos cuadros. Los intervalos sin texto reconocido conservan contenido indeterminado. ASR y captions sostienen análisis textual, sin acreditar escucha, prosodia, música, SFX, silencios ni visión continua.

“Completa” en el inventario significa que se recorrió la fuente textual procesada de toda la duración y se responden las cinco preguntas con evidencia temporal, incluyendo cierre real. Las cuatro son publicaciones distintas. La comparación textual confirma temas y aperturas distintas en P2–P4 frente a P1. Se buscaron en los captions del vlog las referencias distintivas a contenedor en Chile, final de jornada y elección de portada, y consejo a los jóvenes con contacto visual, sin encontrar esos desarrollos. La cifra de 1,9 millones de visualizaciones aparece en P1 y P2, por lo que esa coincidencia aislada conserva su carácter de tema compartido. Los cuadros de P3 presentan contenedor/depósito con comentario superpuesto y los de P4 muestran la interacción con visitantes, frente al recorrido y demostración de productos documentados en P1. La distinción deriva de contenido y contexto, además de URL y hash. Las inferencias de público o función comercial están señaladas, porque una pieza puede documentar operación sin contener una lección explícita o un CTA de pago.

## P1 · 24HS Vendiendo Un Paquete Por Minuto.

**Video.** Publicador `Alvaro Risoglio`, canal `UCqFckD_NNErj4su0wR23fUA`, publicado el 3/11/2026. Consulta del corpus primario el 8/11/2026. Contenedor de imagen conservado en QA de 1.380,233333 s, aproximadamente 23 minutos. El título expresa una afirmación editorial y requiere cotejo separado si se quisiera usar como resultado de ventas. [Publicación exacta](https://www.youtube.com/watch?v=oZ9UKXve3Dk).

**Cobertura y fuente de tiempos.** JSON completo de captions `es-orig`, 1.257 cues y 1.218 no vacíos, leído con deduplicación de solapamientos exactos. Primer texto a 27,870 s. Último cue termina a 1.382,159 s, unos 1,926 s después de la imagen, por lo que el análisis se acota al final de 1.380,233333 s. La falta de palabras reconocidas antes de 27,870 s deja ese tramo sin reconstrucción verbal. El corpus visual previo documenta 92 cuadros únicos, y aquí se utiliza como evidencia heredada identificada. [Captions primarios conservados](../../../99-archivo/recuperacion-secundaria/oZ9UKXve3Dk-subtitulos.json), [muestreo visual y QA previos](../../fichas/audiovisual/bastian-alvaro.md).

### 1. Idea central

**HECHO REFERENTE.** Expone cómo preparó una promoción de Cyber y qué trabajo operativo hubo detrás. Entre 03:57–04:41 anuncia la intención de explicar la preparación. Entre 06:40–09:39 descompone productos, regalos, descuento y cuotas. Luego incorpora distribución creativa y problemas de ejecución. El contraste entre el Cyber anterior deficitario y el actual rentable aparece como declaración propia a 01:21–02:09. Las cifras de pedidos, anuncios y beneficios permanecen como afirmaciones del emisor. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk).

### 2. Público y problema

**HECHO REFERENTE.** A 06:50–07:00 aclara su propósito de que otros aprendan a preparar el evento. A 17:24–17:51 responde una pregunta dirigida al emprendedor cuyo primer Cyber decepcionó. **INFERENCIA.** El público textual más claro es quien vende online y confunde vender volumen con gestionar una oferta rentable y ejecutable. La propia admisión de errores aporta el problema que organiza el relato. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk).

### 3. Apertura, desarrollo y cierre con respaldo temporal

| Ventana de captions | Qué sostiene el contenido leído |
|---|---|
| 00:27,87–01:18,51 | Presentación de pedidos y de Voltra, invitación al local y comienzo del recorrido. El anticipo visual 00:00–00:28 procede del muestreo heredado. |
| 01:21,15–04:41,35 | Contraste con el Cyber anterior, puestos, equipo y depósito. Presenta el problema comercial que explicará. |
| 04:43,60–06:25,23 | Conversación por un pago confirmado incorrectamente y dificultad cotidiana de operar. Las preguntas y respuestas pertenecen a varios participantes. |
| 06:40,28–09:39,55 | Producto normal frente a promoción. Cabezal extra, reducción de precio, regalo de filtro/accesorio y coste de financiar cuotas. |
| 09:39,56–13:28,47 | Relato de producción de creatividades, multicuentas, software y distribución. Las cantidades y prestaciones del software quedan declaradas. |
| 13:37,35–17:12,27 | Cuellos de comunicación, desorden, stock y separación de tareas controlables frente al resultado de venta. |
| 17:12,28–21:25,67 | Preguntas sobre anuncios, producto, equipo y vergüenza de publicar. A 17:04,56–17:12,27 admite referencias de guion con IA y mucha improvisación. |
| 21:25,68–23:00,23 | Pregunta retrospectiva, conversación informal y cierre. A 22:05,88–22:31,83 declara finalidad de aportar valor. Desde 22:30,52 solicita suscripción/like y promete contenido gratuito semanal. |

Los cortes de la tabla son agrupaciones analíticas de cues, sin pretensión de medir todos los cambios de plano. [JSON de tiempos](../../../99-archivo/recuperacion-secundaria/oZ9UKXve3Dk-subtitulos.json).

### 4. Técnica concreta de enseñanza o venta

**HECHO REFERENTE.** Usa un producto concreto como unidad de explicación. En 07:41–08:29 vincula el regalo y la rebaja con el cálculo de margen y el coste de cuotas. En 09:31–09:36 explica por qué mantuvo otro precio por margen insuficiente. **INFERENCIA.** Comparar situación inicial, modificación y restricción vuelve discutible una decisión comercial. La operación y las repreguntas aportan contexto, aunque el relato carece de una hoja contable verificable. El CTA final es seguir contenido. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk).

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** En clase 1, mostrar una agenda inicial, pedir a Claude una reorganización y justificar un cambio concreto. En clase 2, comparar una oferta antes/después con condiciones que Sergio pueda entregar. Para clase 3, usar un error sintético de confirmación de pago como ejemplo de por qué una automatización requiere comprobación previa. Los puntos de partida son respectivamente tareas controlables de 16:01–16:53, promociones de 07:41–09:39 y error de 04:43–05:09. Son adaptaciones didácticas, con la demo de automatización aún propuesta en las decisiones vigentes. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk), [decisiones](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

## P2 · Último día del Cyber y revisión del equipo

**Reel.** Título descriptivo de esta ficha, porque el embed carece de caption/título editorial. Publicador `@alvarorisoglio`, owner ID `1263152904`, nombre de perfil `Alvaro Risoglio`. Consulta del 8/11/2026. Duración metadata 86,423 s, contenedor 86,537914 s, audio decodificado 86,4493125 s. Cobertura textual de todo el archivo, 24 segmentos ASR, último hasta 86,24 s. Quedan sin palabras reconocidas algunas ventanas intermedias y la fracción final. [Publicación](https://www.instagram.com/p/DfVNQ-MPBBN/), [embed primario con owner](https://www.instagram.com/p/DfVNQ-MPBBN/embed/captioned/).

### 1. Idea central

**HECHO DE LA PIEZA.** Recorre el trabajo al final del Cyber y termina preguntando por la portada de contenido. Las ventanas 00:00–00:09,60, 00:29,24–00:42,24 y 00:59,24–01:26,24 sostienen ese recorrido. [P2](https://www.instagram.com/p/DfVNQ-MPBBN/).

### 2. Público y problema

**INFERENCIA.** Seguidores interesados en el detrás de escena del negocio. Su función consiste en mostrar personas y tareas y obtener opinión sobre una elección editorial. La pregunta por la portada vuelve explícita la participación al final. [P2](https://www.instagram.com/p/DfVNQ-MPBBN/).

### 3. Apertura, desarrollo y cierre con respaldo temporal

- **Apertura 00:00–00:09,60.** Anuncia final de jornada y último día del Cyber.
- **Desarrollo 00:10,92–00:57,24.** Pregunta por miembros del equipo y comenta el cambio de escribir a enviar audios. Algunas respuestas se reconocieron mal y no se reconstruyen.
- **Cierre 00:59,24–01:26,24.** Pregunta por YouTube, pide estadísticas y consulta qué portada gusta más. La cifra verbalizada de visualizaciones queda como declaración. La palabra de ASR equivalente a “catbox” es incierta y la función de portada se infiere del contexto de elección.

Las marcas proceden de los 24 segmentos del ASR integral. [P2](https://www.instagram.com/p/DfVNQ-MPBBN/).

### 4. Técnica concreta de enseñanza o venta

**INFERENCIA.** Recorrido situado y pregunta participativa. El contenido mantiene la relación con seguidores mientras exhibe la actividad del equipo. Aporta material de comunicación y participación, con una enseñanza procedimental limitada. [P2](https://www.instagram.com/p/DfVNQ-MPBBN/).

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** En clase 1, mostrar dos agendas generadas con Claude y pedir cuál sirve mejor al negocio y por qué. La referencia es el cierre con elección de 01:15,24–01:26,24. Se convierte la participación en un cotejo con criterios, sin trasladar la estadística de YouTube a un resultado del workshop. [P2](https://www.instagram.com/p/DfVNQ-MPBBN/).

## P3 · Primer contenedor a Chile

**Reel.** Título descriptivo derivado de la primera frase. Publicador `@alvarorisoglio`, owner ID `1263152904`. Consulta del 8/11/2026. Metadata 35,641 s, contenedor 35,755873 s, audio 35,6440625 s. ASR integral de diez segmentos, de 00:00 a 00:34,88. Los cuatro cuadros inspeccionados muestran imágenes del contenedor y depósito con el presentador superpuesto. [Publicación](https://www.instagram.com/p/DfQtcE5u_kj/), [embed con owner](https://www.instagram.com/p/DfQtcE5u_kj/embed/captioned/).

### 1. Idea central

**HECHO DE LA PIEZA.** Relata la llegada del primer contenedor a Chile y usa ese compromiso ya hecho para explicar por qué tendrá que resolver la operación. Se reconoce en 00:00–00:16. [P3](https://www.instagram.com/p/DfQtcE5u_kj/).

### 2. Público y problema

**INFERENCIA.** Seguidores emprendedores que postergan un proyecto por estar ocupados. El texto expresa sobrecarga, decisión y pasos próximos. El carácter testimonial acota la evidencia a su caso. [P3](https://www.instagram.com/p/DfQtcE5u_kj/).

### 3. Apertura, desarrollo y cierre con respaldo temporal

- **Apertura 00:00–00:06.** Anuncia el contenedor y contrasta expansión con dificultad para atender Argentina.
- **Desarrollo 00:06–00:21.** Explica compromiso previo y anuncia viaje para crear contenido con influencers locales.
- **Cierre 00:21–00:34,88.** Añade la coincidencia de un cliente chileno en Voltra y saluda al público de Chile anunciando que tocará vender allí.

Son diez segmentos temporales de ASR. La venta futura y el viaje pertenecen a su relato, sin confirmación posterior de ejecución. [P3](https://www.instagram.com/p/DfQtcE5u_kj/).

### 4. Técnica concreta de enseñanza o venta

**INFERENCIA.** Historia breve con tensión y decisión, seguida de un plan y saludo a la comunidad nueva. Las imágenes hacen tangible la operación. El mecanismo persuasivo es compartir el proceso y anticipar una expansión. [P3](https://www.instagram.com/p/DfQtcE5u_kj/).

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** En clase 1, convertir un pendiente concreto en próxima acción, fecha y dato faltante dentro de Claude. En clase 2, anunciar un siguiente paso verificable al explicar una oferta. Las fuentes son 00:08–00:21 y 00:29–00:34,88. El ejercicio de aula puede realizarse sin comprometer capital. [P3](https://www.instagram.com/p/DfQtcE5u_kj/).

## P4 · Consejo para los más jovenes

**Reel, título del caption original.** Publicador de marca `@voltra.argentina`, owner ID `42464203110`, nombre de perfil `Voltra Reels` comprobado en su embed público, mostrado en el feed primario `@alvarorisoglio`. Consulta del 8/11/2026. Se estudia como contenido distribuido en el perfil personal asociado a Álvaro. La propiedad editorial empresarial queda conservada y el análisis no autentica la voz del hablante por aparecer allí. Metadata 78,333 s, contenedor 78,412381 s, audio 78,3223125 s. ASR completo de 32 segmentos, último hasta 78 s. [Publicación](https://www.instagram.com/p/DfPV35zRA3k/), [embed con owner empresarial y caption](https://www.instagram.com/p/DfPV35zRA3k/embed/captioned/), [feed asociado](https://www.instagram.com/alvarorisoglio/embed/), [perfil del publicador](https://www.instagram.com/voltra.argentina/embed/).

### 1. Idea central

**HECHO DE LA PIEZA.** El hablante principal sostiene que vender hace falta en distintos oficios y aconseja mirar al interlocutor aun sintiendo vergüenza. Son dos ideas desarrolladas en 00:04–00:26 y 00:51–01:09. [P4](https://www.instagram.com/p/DfPV35zRA3k/).

### 2. Público y problema

**HECHO DE LA PIEZA.** El caption nombra jóvenes y el diálogo presenta visitantes con vergüenza. **INFERENCIA.** El consejo busca conectar formación técnica, conseguir clientes y desenvolverse ante otros. Se analizan esos argumentos sin atribuir a todos los visitantes las palabras del hablante principal. [P4](https://www.instagram.com/p/DfPV35zRA3k/).

### 3. Apertura, desarrollo y cierre con respaldo temporal

- **Apertura 00:00–00:04.** Presentación de visitantes y anuncio de un consejo.
- **Desarrollo 00:04–00:26.** Ejemplos de profesiones, necesidad de vender y exposición ante cámara. Entre 00:27–00:50 hay interacción y palabras mal reconocidas que quedan indeterminadas.
- **Desarrollo final 00:51–01:09.** Recomienda mirar al interlocutor pese a la vergüenza.
- **Cierre 01:09–01:18.** Agradece la visita y anima a levantar el taller mecánico. La conversación termina sin inscripción o compra de formación.

Los rangos proceden de ASR, con cuatro cuadros de apoyo a 0, 10, 25 y 34 s. [P4](https://www.instagram.com/p/DfPV35zRA3k/).

### 4. Técnica concreta de enseñanza o venta

**INFERENCIA.** Generaliza una habilidad con ejemplos de ocupaciones y después la vuelve conducta específica durante la interacción. El taller mecánico reaparece en el cierre y personaliza el consejo. El valor de la muestra está en esa especificidad, con tramos dialogados de menor inteligibilidad. [P4](https://www.instagram.com/p/DfPV35zRA3k/).

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** En clase 2, cada dueño explica en una frase qué problema resuelve y practica una pregunta a otro asistente, con opción de hacerlo sentado. Deriva de ejemplos ocupacionales de 00:04–00:20 y conducta concreta de 00:51–01:09. Se adapta a pequeños negocios de Santa Cruz y requiere que Sergio pruebe el ejercicio. [P4](https://www.instagram.com/p/DfPV35zRA3k/).

## Página comercial y búsqueda de oferta personal

**HECHO DE EMPRESA.** El 8/11 se comprobó HTTP 200 en la página Black Edition y en Cómo comprar. La primera ofrece producto físico, beneficios, regalos y carrito. La segunda declara selección → carrito → datos/envío/pago → confirmación por email y WhatsApp. Esa cadena es el recorrido escrito del vendedor. La compra permanece sin prueba transaccional. Se distingue esta oferta de cualquier formación personal de Álvaro. [Producto Voltra](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition), [recorrido declarado](https://voltra.com.ar/pages/como-comprar).

La extracción mantiene contradicciones de disponibilidad, descuento y cuotas que ya había observado el corpus. Esto impide convertir bloques promocionales en una condición comercial final confirmada. Para este análisis basta identificar producto, problema, carrito y asistencia. La tienda es fuente de empresa y queda fuera de la cuenta audiovisual. [Página principal](https://voltra.com.ar/), [producto](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition).

**Búsqueda delimitada de oferta personal.** El 8/11 se consultaron el perfil embebido enlazado por SWAP, el perfil asociado, descripción primaria conservada del vlog, SWAP y búsquedas exactas `"Álvaro Risoglio" sitio cursos`, `"alvaro.risoglio" sitio web curso mentoría`, `"Alvaro Risoglio" "mentoría" "curso" "web"`, `"alvarorisoglio" "link" "curso"` y `"alvaro.risoglio" "mentor"`. No se localizó una landing personal verificable de curso, workshop o mentoría. Los resultados predominantes fueron entrevistas y tiendas. Los GET de perfiles normales recibieron 429 y el buscador indicó throttling. Los embeds permitieron recuperar publicaciones, pero no exponen una biografía comercial íntegra. Esta ausencia está circunscrita a esas fuentes y consultas. [SWAP](https://www.swapodcast.com/episodes/alvaro-risoglio), [perfil público embebido](https://www.instagram.com/alvaro.risoglio/embed/).

**HECHO DECLARADO EN P1.** Entre 11:46–12:03 menciona software propio vendido anteriormente y que ya no quiere vender. A 10:26–10:39 invita a editar y publicar mediante `voltramulticuentas.com`. Es una invitación de colaboración/remuneración declarada, cuyo sitio y condiciones quedan sin validación en esta investigación. Tampoco acredita una oferta de formación. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk).

## Patrón observado y límites de transferencia

**INFERENCIA ACOTADA A ESTAS CUATRO PUBLICACIONES.** El negocio en marcha proporciona el material del contenido. P1 explica una promoción con sus restricciones. P2 hace participar en una elección editorial. P3 cuenta una decisión de expansión. P4 relaciona profesiones y habilidades comerciales. La proximidad textual procede de tareas, preguntas y ejemplos concretos. El corpus no determina una cadencia vocal, una receta general de viralidad o conversiones atribuibles a estas piezas. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk), [P2](https://www.instagram.com/p/DfVNQ-MPBBN/), [P3](https://www.instagram.com/p/DfQtcE5u_kj/), [P4](https://www.instagram.com/p/DfPV35zRA3k/).

La longitud y función difieren. P1 desarrolla oferta, reparto de trabajo y balance durante 23 minutos. P2 es diario participativo, con enseñanza limitada. P3 es un relato de expansión. P4 es consejo contextual publicado por una cuenta de empresa y distribuido en el perfil asociado. El conjunto no contiene una clase completa de IA. Las afirmaciones de rentabilidad, visitas y pedidos quedan sin auditoría. La propiedad del post tampoco identifica automáticamente a cada voz o al editor.

### Tres aplicaciones concretas para ONIA

1. **PROPUESTA ONIA para ordenar.** Sergio muestra una agenda desordenada sintética, la trabaja en Claude y explica una corrección. Entregable del ensayo, una agenda antes/después con una razón verificable para el cambio. Cotejo, otro participante señala qué dato cambió la decisión. Toma la explicación objeto → modificación → restricción de P1, 07:41–09:39. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk).
2. **PROPUESTA ONIA para vender.** Cada negocio describe un problema cotidiano y una solución que realmente entrega. Entregable, una frase comercial y una pregunta para el comprador. Cotejo, un compañero identifica para quién sirve y qué falta aclarar. Toma los ejemplos de profesiones y la conducta específica de P4, 00:04–00:20 y 00:51–01:09. [P4](https://www.instagram.com/p/DfPV35zRA3k/).
3. **PROPUESTA ONIA para preparar una automatización.** Con un caso sintético de pago pendiente, Sergio muestra qué comprobación debe preceder a marcar un pedido como confirmado. Entregable, una regla escrita con dato de entrada, condición, salida y responsable. Cotejo, un caso de pago incompleto conserva estado pendiente. Toma el error operativo de P1, 04:43–05:09. La posible demo de clase 3 conserva su condición de propuesta y este documento queda en preparación didáctica. [P1](https://www.youtube.com/watch?v=oZ9UKXve3Dk), [decisiones](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

Las tres adaptaciones se destinan al workshop «Tu negocio con IA, ordena, vende y automatiza» para pequeños negocios de Santa Cruz. Bs 50 grupal está aprobado, y VIP conserva condición de propuesta. Las fichas de piezas y estas aplicaciones dejan materiales para que Sergio prepare y ensaye sus clases. [Decisiones vigentes](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

## Evidencia durable, descarte y comprobaciones

La ficha conserva parámetros, propietarios, duraciones, ventanas y paráfrasis de apertura/desarrollo/cierre. Los JSON temporales permitieron cotejo adicional durante la redacción. Los hashes documentan integridad de los archivos procesados. Su existencia no acredita exactitud del ASR.

| Pieza | SHA-256 del medio procesado | SHA-256 del JSON ASR o captions |
|---|---|---|
| P1 | QA heredado del MP4 `6179d99a8506859e984af9d99a819005e8a3786ec9309b66b99762ef6fddc751` | JSON conservado `3b187e6a10e544e93a702adb008800c6ecb68b55e473485b5507801544f1e826` |
| P2 | `47979ed98a40f456ca1f43a10e2e8d1e52e20375f186160333d4970c2c91599f` | `05cb1041fac356e8fc5587a567c2f7b11439fa62aaf51d9ad015df8cd79310bf` |
| P3 | `1ce3a74993b1ffcab49f3f300a5083d652f042389d188f12a484c7f65bf5a581` | `cef4d523de25f076c602fa88235279c28d03d5499b14d30b06a07ecd02accfd7` |
| P4 | `883f23938f460779f3156706446ba9d21fb2497fbd3eb14e80a3d030155916a1` | `2b8bca0aad95dc5c8c48b55ca4aa3388238271dad36186869451b1b56b93d243` |

**Descartes reales.** Se procesaron primero tres clips breves del perfil enlazado. Se excluyen del mínimo por escasez argumental o duplicación y se sustituyeron por P2–P4. No se vuelven unidades adicionales del inventario.

| Publicación exacta | Resultado del intento y motivo de descarte |
|---|---|
| [DfazcdKOxYA](https://www.instagram.com/p/DfazcdKOxYA/) | 43,44 s de audio. ASR breve de supermercado y búsqueda de warehouse, insuficiente para las cinco preguntas con desarrollo consistente. |
| [DfTDg4wOtB7](https://www.instagram.com/p/DfTDg4wOtB7/) | 34,34 s de audio. Anticipo de Cyber que repite contenido del vlog P1. |
| [DfF-623somt](https://www.instagram.com/p/DfF-623somt/) | 33,97 s de audio. Anticipo de día 8 en China, pocas frases en español/inglés y desarrollo insuficiente. Sirvió además para comprobar circulación entre perfiles. |

**Lecturas locales realizadas.** AGENTS, ESTADO, reglas comunes, boss-memoria, ORQUESTACION, ESTRUCTURA, INICIO-SESION, directora comercial, apoyo research, decisiones vigentes, cerebro previo de Álvaro, ficha audiovisual Bastian/Álvaro, ficha de marketing y criterio pertinente, metadata de YouTube y todos los captions del vlog. La primera ruta intentada para criterio omitía `fichas/` y se corrigió por búsqueda de nombre antes de leerla.

**Comprobaciones.** Cotejo de owner/publicación/duración en cada embed, ffprobe de los seis clips breves probados, ASR offline completo, lectura integral de sus salidas, exclusión de tres teasers, inspección de doce cuadros de P2–P4, lectura de captions completos P1 y acotación del exceso final, HTTP 200 de dos páginas comerciales y verificación de enlaces locales de esta ficha. No se descargó ni retranscribió el vlog. Los medios temporales propios se retiraron después del cotejo técnico, conservando textos y manifiestos pequeños para revisión del principal.

**Faltantes concretos.** Permanece sin localizar una página comercial personal verificable. La atribución de P4 requiere conservar su publicador empresarial y su circulación en el perfil personal asociado. Si el criterio exigiera una pieza subida exclusivamente por cuenta personal, P4 tendría que reemplazarse y el mínimo bajaría a tres. Para escucha o edición audiovisual integral hace falta una revisión perceptual explícita de las cuatro duraciones. Para verificar ventas harían falta datos autorizados ajenos al alcance público de esta ficha. Próximo paso del coordinador, cotejar evidencia temporal/atribución y emitir revisión de esta entrega.

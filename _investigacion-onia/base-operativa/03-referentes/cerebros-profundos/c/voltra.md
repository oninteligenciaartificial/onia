# VOLTRA Argentina · demostración de producto y recorrido comercial

Consulta pública del 8 de noviembre de 2026. Estado de la ficha **muestra analítica completa de cuatro piezas distintas y una página comercial comprobada, pendiente de revisión independiente**. «Completa» indica contenido suficiente para las cinco preguntas por pieza y tiempos localizables. La percepción sonora integral y el visionado continuo quedan pendientes.

## Identidad, alcance y procedencia

VOLTRA es la marca/tienda argentina `voltra.com.ar`. La unidad estudiada es su comunicación comercial de la aspiradora Black Edition 3 en 1. La autoría editorial se atribuye a la marca por publicación en su tienda. Las identidades, relación laboral y condición de clientes de quienes aparecen son desconocidas. Los relatos en primera persona son recursos publicitarios publicados, sin autenticación de testimonios. La muestra procede del carrusel propio. P4 tampoco se toma de un canal personal de Álvaro Risoglio. [Página de producto](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition).

Se leyó el HTML primario por GET público, HTTP 200, 610.348 bytes. SHA-256 del snapshot `093ddc416e03b8710b714c5fd8d84d3f7aeadf7e4549eb7bb291168f9ab8dc2c`. Se recuperaron doce URLs MP4 únicas y se eligieron tres piezas nuevas breves, además de la ya estudiada. En el snapshot, sección `shopify-section-template--24216727093308__image_slider_YEFPbi`, las líneas de `<source data-src>` son 8454 para P1, 8745 para P2, 9036 para P3 y 9133 para P4. Cada elemento usa `type="video/mp4"`. Las URLs CDN de cada pieza se conservan abajo. Las líneas dependen de este snapshot, la cadena tienda → source → asset permite volver a cotejarlas.

La distinción entre piezas se comprobó por guion, entorno y acción, además de las huellas de archivo. P1 presenta ahorro de tiempo y limpieza del sillón con cambios de vestuario. P2 abre sobre una mesa y desarrolla accesorios y lavado de filtro con una presentadora de top verde. P3 ocurre en exterior con un inflable rosa. P4 ocurre frente a cajas y desarrolla el problema auto/mascota. Son cuatro creativos comerciales diferentes. Las distintas resoluciones, playlists y posibles recortes de un mismo creativo no se cuentan.

## Método y límite de cobertura

- **P1** reutiliza el ASR y el mapa visual previo. Se leyó ahora el TXT y el JSON completo, incluidas palabras temporizadas. El segmento único 0–21 s contiene localizadores por palabra. El mapa heredado inspeccionó 108 imágenes cada 0,2 s y el último fotograma. No se repitió la transcripción ni se declara nueva observación de esas 108 imágenes. [ASR JSON](../../asr/complementario/voltra.json), [ASR TXT](../../asr/complementario/voltra.txt), [ficha visual](../../fichas/audiovisual/voltra.md).
- **P2–P4** tuvieron GET público HTTP 200, `ffprobe`, decodificación de fuente completa y ASR nuevo con faster-whisper 1.2.1 small local, CPU int8, dos hilos, un worker, offline, VAD, beam 5 y palabras temporizadas. El proceso terminó con salida 0, en 9,59 s, 3,76 s y 5,79 s de cómputo respectivamente. Sin instalaciones ni descarga de modelos.
- Se inspeccionaron hojas de contacto nuevas de las tres fuentes completas mediante fotogramas `n=0,30,60,…` y el último. Las tres son CFR 30 fps. Los PTS son `n/30`, con 38, 21 y 23 muestras respectivamente. Últimos PTS 36,933 s, 19,933 s y 21,600 s. Se descartan para la atribución temporal las primeras hojas exploratorias obtenidas con el filtro `fps=1`, pues éste puede seleccionar otro fotograma de cada intervalo. Sólo el muestreo por índice y sus PTS respalda los tiempos visuales nuevos.
- ASR aporta contenido verbal estimado y estructura. Las imágenes aportan acciones y subtítulos en muestras identificadas. Los intervalos de la estructura son ventanas de contenido, con huecos declarados. No certifican cada punto de corte, sincronía o duración de cada acción. No hubo escucha de voz, música, efectos o ruido del aparato. Los huecos de VAD no prueban silencio.

Las ventanas y paráfrasis siguientes constituyen la evidencia durable en esta ficha. Los medios nuevos se eliminaron de `/tmp` después del cotejo. No se depende de su conservación para conocer qué se observó y qué falta. Las fuentes exactas y huellas permiten recuperarlos para revisión.

## P1 · Presentación, usos y cierre hacia la web

Título descriptivo de esta ficha, sin título oficial publicado comprobado. Tipo video comercial vertical. Publica VOLTRA Argentina, creadora original desconocida. Consulta 2026-11-08. Duración 21,461333 s, 606×1080, 30 fps, 643 fotogramas. Huella heredada del MP4 `365c663ab8880602091c8e50f485421eaf462cd3461b298e0891e21c8f012d48`, 19.904.755 bytes. El HTML actual vuelve a enlazar el mismo asset. [P1, fuente exacta](https://voltra.com.ar/cdn/shop/videos/c/vp/a081891a8e224825ac38370d1b22d62c/a081891a8e224825ac38370d1b22d62c.HD-1080p-7.2Mbps-64052188.mp4?v=0).

### 1. Idea central

**HECHO REFERENTE.** Presenta una aspiradora pequeña como solución de limpieza cotidiana, enumera funciones y deriva a la web. La promesa de convertir horas en segundos es una alegación publicitaria, sin medición independiente.

### 2. Público y problema

**INFERENCIA.** Compradores de hogar/auto que quieren resolver suciedad localizada con un equipo fácil de manipular. La inferencia nace de los usos enumerados. El sillón sí aparece en el mapa visual, auto y teclado sólo están mencionados verbalmente en esta pieza.

### 3. Apertura, desarrollo y cierre con tiempos

| Ventana | Contenido leído y fuente temporal |
|---|---|
| 0–1,88 s | Anuncio de llegada del producto. ASR por palabra, presentación visual heredada 0–2 s. |
| 2,12–6,14 s | Promesa de ahorro de tiempo y encendido. ASR por palabra, mapa visual 2,2–6,2 s. |
| 6,18–11,70 s | Tamaño, USB, alegación de potencia, aspirar/soplar. ASR por palabra. El mapa observa teléfono suspendido y cabello en movimiento entre 9–12 s. |
| 12,16–14,76 s | Enumera sillón, casa, auto y teclado. ASR por palabra, mapa muestra residuos en sillón 12,2–15 s. |
| 15,04–18,20 s | Invitación a conseguirla en la web. El tramo inequívoco de destino ocupa 16,46–18,20 s en words. |
| 18,36–21 s | Financiación y envío. ASR por palabra, rótulos heredados 18,4–21,4 s. El error ASR «gotas» se coteja con el rótulo de cuotas. |

### 4. Técnica de enseñanza o venta

**HECHO REFERENTE.** Beneficio → atributos → demostraciones → destino → condiciones. El aparato permanece visible y cambia la cercanía del plano. La enseñanza consiste en mostrar usos breves. **INFERENCIA.** Esto reduce el esfuerzo de imaginar qué se compra, pero no acredita ahorro, potencia, conversión o satisfacción.

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** Clase 1 puede mostrar una lista de pendientes antes y después de trabajar con Claude. Clase 2 puede practicar una CTA que nombre un destino concreto. Clase 3 puede mostrar una entrada y salida visibles de una automatización propuesta. Se toma la secuencia demostración → siguiente paso de P1, sin prometer velocidad o resultados aún no medidos.

## P2 · Accesorios y filtro lavable

Título descriptivo de esta ficha, sin título oficial comprobado. Tipo video comercial vertical. Publica VOLTRA Argentina, creadora original desconocida. Consulta 2026-11-08. Duración contenedor 36,992 s, video 36,966667 s, 606×1080, 30 fps, 1.109 fotogramas. GET HTTP 200, 35.517.095 bytes, SHA-256 `11d5ba6af382db7d05655b561ff8d03d2dd2c9f7eb9a916da6ed1053f2068e3d`. [P2, fuente exacta](https://voltra.com.ar/cdn/shop/videos/c/vp/98cb2b2c536045b28f2955cd6a072132/98cb2b2c536045b28f2955cd6a072132.HD-1080p-7.2Mbps-64052191.mp4?v=0).

Cobertura real de contenido verbal mediante ASR 3,76–36,40 s, con huecos. La apertura 0–3,76 s sólo tiene cobertura visual por PTS y subtítulos parciales. No se reconstruye la frase faltante. Muestreo visual a lo largo de toda la fuente, 38 imágenes, incluido último PTS 36,933 s.

### 1. Idea central

**HECHO REFERENTE.** Explica usos y accesorios, añade mantenimiento del filtro y termina con condiciones comerciales presentadas en primera persona. La muestra contiene una instrucción de cuidado más desarrollada que P1.

### 2. Público y problema

**INFERENCIA.** Personas que necesitan limpiar superficies pequeñas y rincones y quieren saber qué incluye el equipo y cómo reutilizarlo. Se deriva de la enumeración de alfombras/rincones y de la secuencia del filtro.

### 3. Apertura, desarrollo y cierre con tiempos

| Ventana | Contenido leído y fuente temporal |
|---|---|
| PTS 0, 1, 2 y 3 s | Aparato sobre mesa con residuos. En 3 s se lee una afirmación de exclusividad parcial. Apertura demostrativa visual, sin frase verbal completa recuperada. |
| 3,76–9,22 s | Usos en sillón, alfombras y lugares difíciles. ASR por palabra, PTS 5–9 s muestran producto/accesorios y subtítulos de usos. |
| 10,38–19,42 s | Accesorios y alegaciones de potencia y soplado. ASR por palabra. PTS 10–13 s muestran caja abierta, 14–16 s muestran cifras comerciales, 17–19 s manipulación del aparato. |
| PTS 20, 21 y 22 s | Aparato orientado hacia el rostro/cabello. La acción visible se registra sin atribuirle sonido ni medición. |
| 23,40–30,14 s | Filtro lavable y reutilizable, enjuagar/secar/reutilizar. ASR por palabra. PTS 24–27 s muestran extracción del filtro, 28–30 s manos junto a pileta y secado con paño. |
| 31,94–36,40 s | Relato de descuento por transferencia y entrega. ASR por palabra. PTS 33–36 s muestran rótulos comerciales. La fuente acaba en PTS 36,933 s con presentadora/producto. |

### 4. Técnica de enseñanza o venta

**HECHO REFERENTE.** Desempaqueta, identifica partes y muestra mantenimiento. **INFERENCIA.** La instrucción de cuidado responde una objeción de uso posterior. El cierre de descuento/entrega busca facilitar la decisión. Son alegaciones de la pieza, sin comprobar compra o entrega real. El ASR confunde enjuagar y envío, por lo que la paráfrasis se cotejó con los subtítulos y la acción visible.

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** Clase 1 puede mostrar cómo guardar, revisar y reutilizar una instrucción de Claude después de crearla. Clase 2 puede relacionar cada entregable con un uso concreto. Clase 3 puede mostrar cómo revisar una salida antes de reutilizarla. Se toma de P2 la secuencia parte → operación → cuidado, sin trasladar prestaciones del producto a la IA.

## P3 · Un inflable como demostración de soplado

Título descriptivo de esta ficha, sin título oficial comprobado. Tipo video comercial vertical. Publica VOLTRA Argentina, creador original desconocido. Consulta 2026-11-08. Duración contenedor 19,989333 s, video 19,966667 s, 606×1080, 30 fps, 599 fotogramas. GET HTTP 200, 17.609.226 bytes, SHA-256 `c4cfc4b0d748ab12fee3220d2f22cbb85d775058eb7b5ce5e8ca656856d112e5`. [P3, fuente exacta](https://voltra.com.ar/cdn/shop/videos/c/vp/b601a2edf9564b7ba66b5f505198d5e5/b601a2edf9564b7ba66b5f505198d5e5.HD-1080p-7.2Mbps-64052194.mp4?v=0).

Cobertura real mediante ASR 1,14–19,71 s en un solo segmento, con palabras temporizadas y un hueco verbal 7,24–17,07 s. El hueco tiene cobertura visual muestreada, no declaración de silencio. Veintiuna imágenes por PTS a lo largo de toda la fuente, incluido el último PTS 19,933 s, negro.

### 1. Idea central

**HECHO REFERENTE.** Promociona la función de soplado a través de un caso estacional, inflar un flotador. El inflable gana volumen en las muestras. No se mide tiempo real de inflado ni continuidad sin montaje.

### 2. Público y problema

**INFERENCIA.** Personas que usan inflables y encuentran incómodo inflarlos con la boca u otro inflador. El planteo verbal se dirige directamente al espectador y sitúa la necesidad en el verano.

### 3. Apertura, desarrollo y cierre con tiempos

| Ventana | Contenido leído y fuente temporal |
|---|---|
| PTS 0 y 1 s | Agua sobre el presentador y aparición del inflable en exterior. Apertura visual disruptiva. |
| 1,14–5,66 s | Verano y molestia al inflar. Words del segmento único. Rótulos observados en PTS 2–5 s aclaran palabras mal reconocidas por ASR. |
| 5,70–7,24 s | Nombre y función del equipo introducidos verbalmente. Words, con rótulos de marca/modelo en PTS 6–7 s. |
| PTS 8–17 s, muestras cada segundo | Boquilla junto al inflable, cuyo volumen y cabeza crecen en las imágenes sucesivas. Desarrollo visual demostrativo. No se atribuye una frase al hueco del ASR. |
| 17,07–19,71 s | Cierre de financiación y envío. Words temporizadas. En PTS 18 s se lee financiación y en 19 s envío. PTS final 19,933 s negro. |

### 4. Técnica de enseñanza o venta

**HECHO REFERENTE.** Una situación, una función y un resultado visual ocupan casi toda la pieza. **INFERENCIA.** La función de soplado se entiende por el objeto que cambia. El cierre añade condiciones, sin URL visible comprobada en las muestras. La asociación con el destino de compra procede de estar alojada en la ficha comercial.

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** Clase 1 puede usar un solo negocio de ejemplo hasta obtener una agenda revisada. Clase 2 puede trabajar un único mensaje comercial desde el borrador hasta una versión utilizable. Clase 3 puede demostrar un caso acotado con una salida visible. P3 respalda mantener el foco sobre una acción verificable, sin convertir la duración editada en tiempo prometido al alumno.

## P4 · Auto, mascota y manejo del producto

Título descriptivo de esta ficha, sin título oficial comprobado. Tipo video comercial vertical. Publica VOLTRA Argentina, creador original desconocido. Consulta 2026-11-08. Duración contenedor 21,653333 s, video 21,633333 s, 606×1080, 30 fps, 649 fotogramas. GET HTTP 200, 19.702.327 bytes, SHA-256 `9df3f04a44ff31e447b8e67a41dd5d5da0adb28d74c6579828f323f6178f3925`. [P4, fuente exacta](https://voltra.com.ar/cdn/shop/videos/c/vp/dc905a3a1d0b4ad6ad17f4e754030f58/dc905a3a1d0b4ad6ad17f4e754030f58.HD-1080p-7.2Mbps-64052189.mp4?v=0).

Cobertura verbal ASR 0–21,62 s, con huecos. Veintitrés imágenes por PTS a lo largo de toda la fuente, incluido último PTS 21,600 s. Se observa producto manipulado frente a cajas. La limpieza efectiva del auto y de pelos se menciona, sin demostración visual de esas superficies en las muestras.

### 1. Idea central

**HECHO REFERENTE.** Vincula el equipo a la molestia de limpiar auto y pelos de mascota, presenta manejo y funciones y remite al dominio de la tienda.

### 2. Público y problema

**INFERENCIA.** Compradores con auto o mascotas que valoran comodidad y guardado. El problema se nombra al comienzo. La alegación de ahorro de tiempo/dinero sigue siendo publicidad, sin comparación medida.

### 3. Apertura, desarrollo y cierre con tiempos

| Ventana | Contenido leído y fuente temporal |
|---|---|
| 0–3,54 s | Problema de tiempo al limpiar auto y pelos. ASR por palabra, subtítulos PTS 1–3 s. |
| 3,74–5,74 s | Introducción de producto. Words, el subtítulo PTS 5 s corrige la deformación del nombre en ASR. |
| 5,98–10,54 s | Alegaciones de potencia, comodidad, tamaño y tres velocidades. Words, PTS 6–11 s muestran manipulación y rótulos. |
| 11,66–12,46 s | Función de soplado. Words y rótulo PTS 12 s. |
| 14,22–17,86 s | Guardado y alegación de ahorro. Words, PTS 15–17 s muestran texto y equipo, sin prueba del auto. |
| 18,30–21,62 s | Dominio web, financiación y envío. Words. PTS 19 s muestra `voltra.com.ar`, 20 s cuotas y 21 s envío. Último PTS 21,600 s conserva al presentador y producto. |

### 4. Técnica de enseñanza o venta

**HECHO REFERENTE.** Problema cotidiano → producto → beneficios manipulables → sitio/condiciones. **INFERENCIA.** Las cajas sitúan una escena comercial, pero no prueban stock vendido, tamaño de empresa o experiencia de un comprador. La explicación de funciones aporta orientación básica de uso.

### 5. Qué tomar para clase 1, 2 o 3

**PROPUESTA ONIA.** Clase 1 puede abrir con una dificultad concreta de agenda de un pequeño negocio de Santa Cruz. Clase 2 puede escribir el mensaje desde un problema explícito del cliente. Clase 3 puede presentar una tarea repetitiva antes de mostrar una automatización propuesta. De P4 se toma la conexión problema → función → siguiente paso, manteniendo visible qué resultado se demostró.

## Página comercial comprobada

**HECHO REFERENTE.** La página pública vende un producto físico. Se comprobó título, atributos, precio mostrado y botón de carrito, además de los videos enlazados. La extracción actual aún contiene estados de stock y porcentajes contradictorios, así como financiación de tres y seis cuotas. El precio mostrado es $158.440 y el comparativo $320.000, en el contexto de tienda argentina. Es información publicada, sin comprobar total final ni vigencia en checkout. La página comercial aporta destino y condiciones, cuenta cero piezas audiovisuales. [Producto](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition).

**INFERENCIA.** El recorrido observado de esta muestra es demostración alojada en ficha → información de producto → CTA carrito. El recorrido posterior sólo consta en la lectura histórica de las instrucciones de compra. Esta ampliación no añadió productos, envió formularios ni ejecutó pedidos. Precio final, cobro, entrega, campañas activas y conversión siguen sin comprobar. [Lectura comercial anterior](../../fichas/marketing/bastian-alvaro-voltra-alex.md#álvaro-risoglio-y-voltra-persona-y-empresa-distintas).

## Patrón de la marca en esta muestra

**HECHO REFERENTE.** Las cuatro piezas mantienen el producto visible y cierran con condiciones comerciales. P1 y P4 explicitan la web. P2 desarrolla el mantenimiento. P3 dedica el tramo central a una sola función visible. El patrón procede de cuatro creativos de un mismo producto y una misma ficha. No representa toda la marca, otros productos, anuncios activos o resultados de venta.

**INFERENCIA.** La marca combina identificación de un problema, aparato manipulable y reducción de dudas sobre uso/compra. P2 enseña una operación de cuidado. P3 muestra una transformación visual. P4 se apoya más en relato y atributos. Esto sugiere distintas formas de volver concreta la utilidad, sin acreditar qué creativo vende o enseña mejor.

## Tres aplicaciones acotadas para ONIA

Las siguientes son **PROPUESTAS ONIA**, independientes de lo que vende VOLTRA. El encargo vigente es «Tu negocio con IA. Ordena, vende y automatiza», para dueños de pequeños negocios de Santa Cruz, tres clases y Bs 50 grupal aprobado. Clase 1 usa Claude. VIP y sus condiciones siguen propuestos. No se adopta ninguna cuota, envío, descuento, garantía o promesa cuantitativa de la tienda. [Decisiones vigentes](../../../05-herramientas/2026-11-08-harness/00-decisiones.md).

1. **Clase 1.** Microdemostración de ordenar una lista de pendientes con Claude y revisar el resultado junto al alumno. Entregable propuesto, una lista priorizada que el dueño pueda corregir. Verificación, el alumno identifica una tarea mal ubicada y la ajusta. Fuente de la decisión didáctica, operación visible de P1 en 12,16–14,76 s y cuidado/reutilización de P2 en 23,40–30,14 s.
2. **Clase 2.** Un solo producto o servicio del alumno, problema del comprador → mensaje → CTA con destino definido. Entregable propuesto, un borrador comercial. Verificación, otro participante puede reconocer destinatario y acción sin explicación adicional. Fuentes, problema de P4 en 0–3,54 s y destino de P1 en 16,46–18,20 s.
3. **Clase 3.** Demostración de una tarea repetitiva con entrada y salida observables, con revisión humana del resultado. Entregable propuesto, mapa mínimo del caso y criterio de comprobación. Verificación, una entrada de prueba produce la salida esperada. Fuente, foco de P3 en el inflable, PTS 8–17 s. El uso de n8n sigue propuesto según las decisiones vigentes y esta ficha no activa flujos.

## Comprobaciones, faltantes y próximo paso

Se comprobaron fuentes primarias, vínculo HTML → cuatro assets, cuatro guiones/escenarios diferentes, tres medios nuevos completos técnicamente, tres ASR nuevos terminados, ASR existente leído con words y cinco apartados en cada pieza. No se usó vidIQ ni una transcripción de pago. El motor emitió una advertencia de telemetría sin persistencia de ID, los tres resultados se completaron con salida 0. La búsqueda de caché en la ruta Hugging Face habitual no encontró el modelo, se localizó la caché ya existente en `~/asr/modelos` y se usó en modo offline. No hubo fallo excluyente de acceso.

Faltan escucha auditiva y reproducción visual continua si se desea valorar entonación, música, efectos, sincronía y todos los cortes. Para ello el revisor puede recuperar los cuatro MP4 exactos, cotejar SHA-256 y revisar cada fuente completa. Falta también prueba transaccional de condiciones finales si cambia el objetivo comercial. Las cinco preguntas de contenido/estructura cuentan con evidencia suficiente en las cuatro piezas, sin presentar esos pendientes como resueltos.

El siguiente paso del encargo corresponde al ejecutor principal y a un revisor distinto, cotejar esta ficha y sus fuentes con la aceptación, reunir la entrega y proceder según el harness. Esta subtarea no ejecuta Git ni declara aceptación o integración.

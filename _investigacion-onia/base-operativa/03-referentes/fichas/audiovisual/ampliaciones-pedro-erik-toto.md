# Ampliación audiovisual · Pedro, Erik y Toto

5 de noviembre de 2026. Video/Sol. **Corte visual con actualización posterior:** los tres textos automáticos Pedro/Toto están terminados y leídos en [guiones](guiones-faltantes.md); sus menciones de sólo texto visible describen la primera inspección. Piezas citadas en las fichas, **no acreditadas como URL enviadas por Sergio**. Se recuperaron cinco medios públicos y ocho imágenes del carrusel; se inspeccionaron **348 muestras en 18 hojas**, más las ocho imágenes estáticas juntas en una hoja. No hubo reproducción continua, escucha ni ASR nuevo. La cobertura textual de Erik incluye la lectura completa de captions automáticos; los otros videos sólo texto visible muestreado y caption de publicación, sin guion verbal certificado.

## Acceso y prueba realizada

Metadatos primero con yt-dlp existente: la red sandbox falló DNS en cinco URLs. Cambio comprobado a red aprobada recuperó cuatro metadatos sin error y el carrusel con error parcial al buscar formatos de ocho imágenes. Se cambió la opción de extracción a `--ignore-no-formats-error`: se recuperaron las nueve entradas, las ocho primeras sin formato video y con imagen pública, la novena con once formatos de video, todos `acodec=none`. No se actualizaron herramientas, instalaron modelos ni usaron cookies, cuenta, formularios, gasto o servicios de producción. Se descargaron los archivos públicos desde esos metadatos. No se repitieron los endpoints web históricos fallidos como si probaran otro acceso.

FFprobe leyó los cinco archivos; FFmpeg extrajo imágenes secuencialmente con dos threads. No se ejecutó una decodificación entera adicional para QA ni ASR. Un fallo de pixel format al extraer el final se resolvió fijando yuvj420p y buscando 0,5 s antes del final del contenedor. Las hojas muestran rejillas **nominales** de `fps=1` o `fps=1/5`; sus rótulos no certifican el PTS de cada cuadro ni cortes exactos. El fotograma final adicional es una búsqueda a duración−0,5 s, **no el último fotograma exacto**. Quedan huecos entre muestras y el tramo final de aproximadamente medio segundo sin inspección. Una extracción completa no equivale a visionado continuo.

Medios, metadatos, logs, captions, hojas y manifiesto: `operacion/referentes-20261105/video/ampliaciones-pedro-erik-toto/`. Los originales de los 28 anteriores se reutilizan como antecedentes y no se duplicaron.

| Pieza/fuente | Archivo, duración y pista | Cobertura inspeccionada | SHA-256 |
|---|---|---|---|
| [DehhvYDAWDl](https://www.instagram.com/pedrobuerbaum/reel/DehhvYDAWDl/) | `DehhvYDAWDl/media.mp4`; 101.758708 s; H.264 720×1280; AAC; 20266934 bytes | 103 imágenes, paso nominal 1 s y búsqueda final; 5 hojas | `f1719caaf498e35f65f2d6723d6fcf75c8b3996b3195cfb2851a9bdd99d4c1cb` |
| [Dem097KgI-A](https://www.instagram.com/pedrobuerbaum/reel/Dem097KgI-A/) | `Dem097KgI-A/media.mp4`; 74.900042 s; H.264 720×1280; AAC; 7112935 bytes | 76 imágenes, paso nominal 1 s y búsqueda final; 4 hojas | `8e384f0e1d498199f8eb823e8317c8061997e3b82ffaf015971bdee9b6b18260` |
| [DepdNr4mWs1](https://www.instagram.com/pedrobuerbaum/p/DepdNr4mWs1/) | `DepdNr4mWs1/media.mp4`; 5.900000 s; VP9 1080×1440; sin pista audio; 743885 bytes | 7 imágenes, paso nominal 1 s y búsqueda final; 1 hojas | `4ffc61596528611d763c637e721d2ed363fc65dbba369e8299e2f842ece4ec5b` |
| [toto-linkedin](https://es.linkedin.com/posts/tomas-artuso_un-solo-video-puede-generar-100k-descargas-activity-7396561210671796224-kvwU) | `toto-linkedin/media.mp4`; 60.601995 s; H.264 720×1280; AAC; 8142994 bytes | 62 imágenes, paso nominal 1 s y búsqueda final; 3 hojas | `f31c9e96cea253ba5be44fde39a032666e93f216fd6cb4014f77f60d34047596` |
| [zXHJ-IJ59AM](https://www.youtube.com/watch?v=zXHJ-IJ59AM) | `zXHJ-IJ59AM/media.mp4`; 496.256871 s; H.264 640×360; AAC; 14627523 bytes | 100 imágenes, paso nominal 5 s y búsqueda final; 5 hojas | `e70f44fde0d7b8d5099a5c3287ca76ce00470fb38948a4bbe09009bf18552841` |

## Pedro · Dem097KgI-A

Procedencia: caption en fuentes-cloud/referentes.md y marketing/pedro-buerbaum.md. Ahora hay imagen del medio real, no sólo caption. Las cuatro hojas fueron abiertas completas.

| Rejilla nominal | Contenido/edición observados | Función y límite |
|---|---|---|
| 0–9 s | Presentador sentado con tablet; apertura «el peor lugar»; 4–9 s diagrama horizontal sobre su imagen, con marcas/círculos rojos. Subtítulo blanco breve centrado. | Problematiza un negocio intermedio; el gráfico ayuda a situar una escala. No se midieron cortes ni prosodia. |
| 10–27 s | Regreso al rostro/tablet; subtítulos de dependencia, previsibilidad, desconexión/vacaciones y riesgo. Variaciones de recorte. | Contraste entre negocio que funciona y dependencia de su dueño; no prueba resultado real de sus empresas. |
| 28–59 s | Reaparece escala con flecha hacia el punto medio y después crecimiento; rostro y tablet alternan; 47–49 s aparecen separación/operativa. | Explicación de reestructuración y separación operativa; no demostración de software ni sistema instalado. |
| 60–61 s | Inserto de escenario; texto fecha miércoles 21 de octubre. | Prueba escénica publicitaria; fecha histórica, no nueva convocatoria. |
| 62–74,40 s | Rostro; rótulo webinar gratuito y cierre «Escala»; palabras visibles remiten al webinar/privado. | CTA de esta pieza coincide con caption: comentario escala para acceso por privado. No se comentó ni verificó DM, registro o webinar. |

Aprendizaje aplicable como hipótesis: dibujar la situación de partida y el cambio mientras se explica, y reservar un bloque de cierre para una oferta coherente. La enseñanza visual no acredita eficiencia comercial. No trasladar este CTA a Dd6oC4EkRX1.

## Pedro · DehhvYDAWDl

Cinco hojas abiertas completas. Presentador con sombrero, camiseta blanca, sentado ante vegetación; subtítulos blancos pequeños sobre la camiseta, con contraste limitado a esta representación. Alterna plano frontal, recortes y laterales.

| Rejilla nominal | Observación | Lectura y límite |
|---|---|---|
| 0–35 s | Predominio de rostro/gestos; palabras aisladas y frases breves; recortes/lateral 9 y 16–17 s. | Exposición verbal apoyada por cambios de encuadre. El muestreo no permite reconstruir cada oración. |
| 36–39 s | B-roll monocromo de mesa/evento/barco. | Ilustración contextual de una oferta/experiencia; no evidencia de propiedad, precio ni cliente. |
| 40–59 s | Vuelve al rostro; aparecen palabras relativas a un buen producto/negocio. | Caption sostiene tesis de llevar el producto a personas pertinentes; el guion hablado íntegro sigue faltando. |
| 60–62 s | Inserto monocromo de presentación, logo escala.io y escena con micrófono. | Señal de autoridad/caso; no auditoría de desempeño. |
| 63–101,26 s | Continúa explicación, frontal y lateral; cierre gestual con sombrero y palabra «Patrón». | No se observó una pantalla de CTA «oferta» en las muestras finales. **El CTA oferta está acreditado por caption**, no se afirma pronunciado ni visible al cierre. |

La diferencia con Dem es material: aquí existe B-roll contextual y cierre de identidad; Dem muestra diagrama y bloque explícito de webinar. Para una adaptación propia conviene decidir si el apoyo visual explica una operación o sólo añade contexto, y comprobar legibilidad sobre ropa clara.

## Pedro · DepdNr4mWs1: carrusel mixto, no reel único

El post contiene nueve entradas: ocho imágenes públicas recuperadas desde los campos de imagen de cada entrada y abiertas juntas; la novena es el clip `DepdLrDD4dK`, perteneciente **al mismo carrusel**, no otra publicación inspeccionada. Los IDs internos de las ocho imágenes se conservaron en metadata-incluye-sin-video.json. La recuperación de imagen usa el campo `thumbnail` del extractor; se inspeccionó su contenido real, no se infirió desde ese campo. No acredita archivo maestro ni resolución original. Hash/tamaño/dimensiones en imagenes-manifest.json.

| Entrada/ID interno | Imagen observada y argumento | CTA propio observado |
|---|---|---|
| 1 · DepdLNNv8GS | Retrato con sombrero; enumera negocios, podcasts, viajes y tiempo propio como relato de autoridad. | Promete contar cómo lo hace y flecha de continuación; no comentario/compra en esta tarjeta. |
| 2 · DepdLOcPT9S | Escena de charla ante asistentes; atribuye la base a sistemas y estructura escalable. | Flecha para seguir; sin CTA comercial autónomo. |
| 3 · DepdLQhvbWp | Edificio contra cielo; une estructura y disfrute de vida empresarial. | Flecha de continuación. |
| 4 · DepdLSFvnCV | Persona en barco; dinero asociado a libertad para disfrutar. | Flecha de continuación. |
| 5 · DepdLUqPk7J | Cama/habitación; anticipa tres pilares. | Flecha para siguiente tarjeta. |
| 6 · DepdLWmPMcJ | Persona ante arquitectura; primer pilar: ejecución y equipo que sabe qué hacer. | Flecha de continuación; no prueba equipo operativo real. |
| 7 · DepdLZ0voeW | Gimnasio/espejo; segundo pilar: atracción y clientes en piloto automático. | Flecha de continuación; la automatización es promesa del autor. |
| 8 · DepdLeJPsqH | Persona con casco; tercer pilar: conversión y cierre delegado. | Flecha de continuación; delegación no comprobada. |
| 9 · DepdLrDD4dK | Clip de boxeo 5,9 s; siete muestras nominales/final; texto comercial permanece en todas. La representación recuperada carece de pista de audio y todos los formatos publicados en esa metadata indican acodec=none. | Comentario SISTEMA para invitación a webinar gratuito del miércoles 21; sistemas/estructura para dueños de negocio. |

El caption anuncia oferta al final del webinar y encaje limitado: no se asistió ni inspeccionó esa oferta. La secuencia estática combina aspiración→método de tres pilares→acción; no demuestra ingresos, automatizaciones, libertad ni conversión. N/A acústico sólo para las ocho imágenes y el archivo de la entrada9 sin pista; no se generaliza a música de la experiencia de Instagram u otras representaciones no disponibles.

## Toto · post LinkedIn exacto

Tres hojas/62 imágenes abiertas. El medio de 60,60 s es una pieza distinta del vlog `hxt0RC2XS8s`; tampoco su autoría material completa se deduce del perfil publicador.

| Rejilla nominal | Observación de imagen/texto | Función |
|---|---|---|
| 0–6 s | Interior de avión y teléfono con rostro; palabras grandes VIRAL/cambiarlo todo; ascensor, identificación TOTO MARKETING. | Gancho y presentación de personaje en situación; contraste de lugares. |
| 7–20 s | Portátil con llamada/presentador, reuniones, escritura, clips pequeños sobre negro, contadores bajos y pizarra. | Problema/ensayos fallidos: relato de agencia que cambia de enfoque. No prueba cada llamada o cronología. |
| 21–36 s | Negro con texto, reunión, exterior, vuelta a libreta/portátil; gráficos de checks y promesa de segunda oportunidad. | Elección narrativa entre opciones; conecta proceso con conflicto. |
| 37–49 s | «¿Y qué pasó?», cifras crecientes de vistas, portátil y rótulo APP/VIRAL/100K descargas. | Resolución con métricas declaradas; no atribución causal ni analítica independiente. |
| 50–60,10 s | Clips en calle/comercio, gimnasio/oficina y llamada final en portátil. Texto visible final invita a seguirlo. | Cierre de continuidad editorial; no CTA de compra o formulario acreditado. |

La secuencia usa B-roll cotidiano, llamadas/escritura como proceso, pantallas negras para énfasis, subtítulos pequeños y cifras de gran tamaño. Los negros son **visuales**, no silencios auditivos demostrados. Conecta servicio Marz y caso de app mediante relato, sin validar los 100k resultados. Hipótesis propia: documentar intentos y decisiones reales antes de presentar un resultado; usar evidencia verificable propia al citar métricas.

## Erik · zXHJ-IJ59AM

Cinco hojas/100 imágenes abiertas y lectura completa de `captions.txt` derivado de VTT `es-orig` existente; no ASR nuevo. Título: Mi homelab con IA local: vale la pena?, canal Erik Taveras. Las cantidades, productos, velocidades, ahorros y funcionamiento son **declaraciones del autor**, no recomendaciones ni benchmarks ONIA. Captions contienen errores: nombres de modelos/servicios y unidades no se corrigen por intuición; contrastar rótulos/descripción para atribución documental.

| Tiempo nominal / captions | Contenido, edición y demostración | Cierre comercial o límite |
|---|---|---|
| 0–20 s | Presentador en estudio oscuro con micrófono; número 170, listado de lo que verá el espectador y transición de capítulo. | Gancho cuantificado y mapa. Descripción dice171; ambas cifras se conservan como distintas apariciones. |
| 25–120 s | Rostro + fichas de siete nodos; B-roll real de equipos; diagramas de almacenamiento, memoria y reparto de contenedores. | Explica roles de hardware. Corrección visual del cierre: a55s el gráfico empieza a construirse; a59s queda consolidado Beelink72/Lenovo56. Coincide con el caption56; la lectura previa33 era un estado intermedio del contador, no contradicción del video. Véase pendientes-visuales-finitos.md. |
| 125–195 s | Grilla de contenedores y grupos personal/negocio/automatización; esquemas de firma y bots. | Enseña arquitectura mediante iconos/listas, no instala ni ejecuta cada servicio ante nosotros. |
| 200–325 s | Capítulo IA, fichas de modelo, pantalla con tokens/s, cinco automatizaciones, diagrama clasificador→escalado y memoria. A 280–290 s muestra31 GB de64; nube frente a casa. | Captions distinguen tareas locales y modelos de frontera; no adoptar rendimiento, modelos o ahorro sin comprobar. |
| 330–375 s | Monitorización con Beszel/Uptime Kuma/logs, pantalla de métricas y esquema de avisos al celular. | Separa alertas importantes y resto de registros; es relato/demostración visual del autor, no acceso a servidores. |
| 380–435 s | Diagramas público/privado, túnel, Tailscale, UPS, reinicio y respaldo. | Contenido técnico ilustrado; no ejecución técnica ONIA. |
| 440–470 s | Cuenta visual de consumo/costo y ahorro; rostro pregunta qué montar primero. Captions7:51,535–7:54,655: comentarios y despedida. | Descripción enlaza comunidad Automatízate; CTA final pide comentar y ver siguiente, no compra pronunciada acreditada. |
| 475–495,76 s | Pantalla final con dos espacios de videos y círculo; permanece hasta búsqueda próxima al final. | Cierre hacia más contenido. No se abrió comunidad, registrado ni instalado nada. |

Diseño observado: consistencia de fondo oscuro, tipografía blanca con verde/amarillo, cifras grandes, fichas y diagramas por capítulos. Alterna explicación a cámara y demostración visual; el muestreo no permite medir ritmo exacto de cortes. La aplicación propia útil sería mostrar la función y límite de cada componente con un diagrama y una captura real, separando cifras declaradas de medidas propias.

## Faltantes y próxima acción concreta

Esta ampliación supera el bloqueo de acceso para cinco archivos y el componente gráfico del carrusel; no acredita integralidad AV. **Video** ya completó y leyó los tres ASR de Pedro/Toto en guiones-faltantes.md; contienen errores, no escucha. No hay cola activa. **Desarrollo** valida capacidad acústica open source con controles; **Video** aplica esa capacidad y registra voz, música, SFX, ambiente, silencios, mezcla, ritmo y sincronía en las cuatro pistas existentes. El clip del carrusel no contiene audio en la representación obtenida: registrar ese límite material, sin inventar escucha ni pista faltante descargable. Jefa incorpora estos cinco medios/una publicación mixta a su corpus y mantiene las decisiones de alcance en GOAL con Organización.

Prueba: lectura de metadata/formatos, archivos presentes, SHA-256/streams, 18 hojas abiertas, ocho imágenes abiertas y captions completos de Erik. No prueba de escucha, cortes exactos, ventas, eficacia comercial ni ejecución de infraestructuras. Sin publicación, mensajes externos, compra, modelos nuevos o cambios a estados ajenos.

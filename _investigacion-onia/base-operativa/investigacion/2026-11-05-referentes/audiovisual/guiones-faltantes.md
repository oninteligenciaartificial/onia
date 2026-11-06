# Recuperación complementaria de guiones automáticos · 5/11/2026

## Cierre puntual de los tres reels Hormozi · tercera tanda

Se cotejaron auxiliares y notas de [Hormozi](hormozi.md): no había cuerpo verbal completo, sólo subtítulos muestreados. Se ejecutaron exclusivamente estas tres piezas con faster-whisper 1.2.1/small ya existente, offline, CPU int8, cuatro hilos, un trabajador, inglés, VAD y palabras temporizadas. Sin descargas, instalaciones ni nuevas pruebas perceptuales. Los tres TXT/JSON se leyeron íntegros; los JSON guardan hashes de fuente/WAV. Son ASR completos del archivo, no fidelidad literal certificada, escucha o prosodia.

- **DfTSZcnovSg**, 89,19 s, ASR 19,92 s: [TXT](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfTSZcnovSg.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfTSZcnovSg.json). Confirma la solución visual de contratar vendedores (37–39 y 86–89 s). Añade el argumento 47–85 s: resolver capacidad antes de otro canal y no intentar solucionar un problema futuro con recursos aún inexistentes. Dudas automáticas: «equal product» 0–1,26 s, «all our gap» 5,56–9,32 s y precio «3.6» 24,16–24,68 s; no convertirlas en citas o cifras comprobadas.
- **DfS9tS4IcP6**, 49,25 s, ASR 10,22 s: [TXT](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfS9tS4IcP6.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfS9tS4IcP6.json). Concuerda con los once consejos visuales. Precisa cierre 40–49 s: reducir creencias necesarias, aumentar razones para creer y ofrecer lo mismo en mitad de tiempo por doble precio. «Recorder sales calls» 33,56–36,66 s es formulación dudosa del ASR, coherente estructuralmente con registrar llamadas para feedback, sin certificar palabra exacta.
- **DfSV88LohWW**, 66,62 s, ASR 11,56 s: [TXT](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfSV88LohWW.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-hormozi-reels/DfSV88LohWW.json). Coincide con caballo/diagrama y educación, persona adecuada, VSL y contacto rápido (28–42 s). Añade justificación 50–66 s: ayudar a decidir y asumir responsabilidad de organizar condiciones favorables. Dudas: «make a drink» 0–3,60 s y «stilly» 46–50,32 s; no corregirlas como si se hubieran escuchado.

Ninguno de los tres ASR contiene solicitud hablada de comentar SALES; el CTA sigue acreditado únicamente por descripción pública. No se certifica ausencia acústica de palabras omitidas por ASR. Brecha de cuerpo verbal recuperable resuelta; no quedan trabajadores ni cola activos. Esta adición eleva a 16 los ASR completos de esta serie y conserva el corte anterior de 13 debajo como antecedente; los siete grupos B y el faltante acústico mantienen su alcance.

**Corte anterior: 13 ASR terminados y leídos.** Las diez piezas originales y las tres ampliaciones tienen texto, palabras, hashes y mapa; ningún ASR sigue activo. Se utilizan los MP4 conservados, sin nuevas descargas. Transcripción automática local faster-whisper 1.2.1 small, CPU int8, cuatro hilos, VAD, beam 5, temperatura 0 y palabras con tiempos; pesos locales y sin red. La fuente, WAV mono 16 kHz y sus SHA-256, duración, segmentos, palabras y probabilidades se conservan por pieza en `operacion/referentes-20261105/video/asr-complementario/`. Los TXT reproducen exactamente los segmentos del JSON. Los controles de silencio, tono y voz ya ejecutados están en [audio técnico](../audio-tecnico/ESTADO.md); no se repitieron. ASR puede omitir, inventar o equivocar palabras, nombres y cifras; no es escucha ni guion literal certificado, y no valida voz, música, SFX, silencios perceptuales o sincronía.

## Heras VSL V1

Fuente SHA-256 `aaa69d980dce383cdf796d9208fadfbfd6d790077967aab881e26c170a27b917`; 637,589 s, 136 segmentos, procesamiento 168,11 s. [Texto derivado completo](../../../operacion/referentes-20261105/video/asr-complementario/heras-vsl-v1.txt) · [palabras y hashes](../../../operacion/referentes-20261105/video/asr-complementario/heras-vsl-v1.json). Leído íntegro.

- **Inicio 0–77 s:** cifra y promesa de seguidores/ingresos, rechazo de la idea de «contenido de valor», presentación y casos. Son afirmaciones comerciales no verificadas.
- **Desarrollo 77–445 s:** contenido consumible y ejemplo; tres pilares: relevancia universal, sistema de ventas orgánico según niveles de conciencia y adaptación por nicho; casos intercalados. La ficha visual registra pilares y capturas, concordancia estructural aproximada.
- **CTA 445–479 s:** plantea consultoría uno a uno, botón inferior y requisitos; coincide aproximadamente con CTA visual 450–475 s. **Desarrollo posterior 483–614 s:** enumera casos por sector. **Cierre 614–635 s:** vuelve a pedir aplicación y compromiso, y termina con «Chao» según ASR; coincide aproximadamente con CTA visual cerca de 620 s.
- **Dudas concretas:** el ASR repite cinco veces «Víctor Eras» en 46–52,5 s, altera nombres y siglas y ofrece cifras dudosas; no convertir sus números o nombres en citas verificadas. La ficha [Heras](heras-vsl.md) identifica al presentador y muestra dos variantes, pero no certifica cada palabra ni prueba los resultados afirmados.

## Estado histórico al interrumpir la primera tanda

Historial del 5/11/2026, ya superado: hubo pausa tras Toto y posterior reanudación. Hoy los13ASR están terminados y leídos, sin proceso ni cola activa; este apartado no instruye reiniciar run.py. La evaluación acústica sigue separada.

## Heras VSL V2

Fuente SHA-256 `44660459b25bd00c30aa805d579afd07cb4dc990001eea25fc73ce25bde5d867`; 637,141 s, 142 segmentos, procesamiento 146,72 s. [Texto derivado completo](../../../operacion/referentes-20261105/video/asr-complementario/heras-vsl-v2.txt) · [palabras y hashes](../../../operacion/referentes-20261105/video/asr-complementario/heras-vsl-v2.json). Leído íntegro.

- **Inicio 0–77 s:** la apertura difiere de V1: plantea que una cuenta que no genere 10.000 euros mensuales sería un hobby, descarta algoritmo/cuenta/nicho y presenta sistema y casos. Esto concuerda con las objeciones que la ficha visual localiza en la apertura V2; no comprueba la afirmación.
- **Desarrollo 77–445 s:** argumento de entretenimiento, tres pilares y casos; texto semejante al de V1 con diferencias y errores de transcripción, sin certificar igualdad de audio ni montaje.
- **CTA 445–479 s:** consultoría y botón bajo el video; **479–614 s:** casos por sector; **614–633 s:** repetición de solicitud y compromiso. Corresponde aproximadamente a los dos CTA visuales registrados. El último segmento termina a 633,22 s; VAD no autoriza a concluir que el resto sea silencio perceptual.
- **Dudas:** repite el nombre erróneamente en 45,82–51,52 s y distorsiona nombres, siglas y números. La comparación de variantes se basa en sus dos ASR, no en escucha ni equivalencia histórica.


## Toto Artuso · hxt0RC2XS8s

Fuente SHA-256 `1c9ec416827c4a16a2f7ed63fa3772fbffb26f7e5817849f15a44e7c3c51ca50`; WAV SHA-256 `5496fda0c652dac65eebb9cdef60c30481061087d1c1230fc863fa68be3b01db`; 1.833,153 s, 462 segmentos, 415,61 s de procesamiento. [Texto derivado completo](../../../operacion/referentes-20261105/video/asr-complementario/toto.txt) · [palabras y hashes](../../../operacion/referentes-20261105/video/asr-complementario/toto.json). Leído íntegro.

- **Inicio 23–173 s:** presenta una semana como fundador, app que conecta marcas y creadores, posible aceleración y búsqueda de inversión; en 54–61,8 s remite a enlace en descripción. La ficha visual muestra montaje de anticipo 0–21 y exposición directa desde 22 s; el ASR empieza en 23,18 s y no permite afirmar ausencia de voz antes.
- **Desarrollo 200–410 s:** conversación y reunión social; **410–630 s:** explica documentar la construcción de la empresa mediante historias, problema y solución, y menciona canales alternativos; son opiniones y cifras propias del emisor. **643–960 s:** invitación a evento de marca y reflexión sobre comunicar objetivos; aclara que no hay acuerdo confirmado. **1.009–1.135 s:** conversación sobre contactos, interfaz para descubrir creadores, herramientas de diseño/código y contraste marketing/producto. La ficha visual sitúa conversaciones, pantallas y desplazamientos en estos intervalos, sin que las pantallas prueben funcionamiento completo.
- **1.165–1.569 s:** encuentro social, carrera, comida y búsqueda del auto. **Cierre 1.569–1.832 s:** plan de lanzamiento, explicación del problema que atribuye a creadores y marcas, insistencia en persistencia y despedida hasta la semana siguiente. La ficha ubica el bloque a cámara final en 1.575–1.833 s. La referencia al enlace inicial es una CTA verbal derivada; al final el texto reconoce despedida, sin una nueva CTA comercial explícita en lo transcrito.
- **Dudas:** nombre del producto aparece como «Mars» en ASR mientras la ficha visual registra Marz; nombres, herramientas y cifras requieren cotejo humano. Repeticiones extremas «¡Ahí está!» 341,16–365,69 y «No» 372,57–395,67 son especialmente sospechosas y no se interpretan como palabras certificadas. Las afirmaciones de crecimiento y resultados no se validan con esta transcripción.

**Histórico de la primera tanda:** Toto terminó; se interrumpió la cola inmediatamente después de `DONE`. El WAV de Alex llegó a extraerse antes de la interrupción, sin JSON de ASR completo: siguiente ID **Alex Carrera**. La pausa fue retirada al liberarse la CPU y el proceso reanudó con un trabajador; el script comprueba la marca `PAUSA` entre archivos. Revisar cada texto completo y agregar mapa y dudas antes de declarar cobertura.


## Alex Carrera · DevcnJYNS7r

Fuente SHA-256 `d7b308a6e253dcd7f003f6a93ab4593f06e680ef87f92dd7f590e721ae9a5fc8`; WAV SHA-256 `9f21bb7642a08adb87a4eb52934c9e9f5463df9d33559871b05a9a4bb4793785`; 57,239 s, 22 segmentos. [Texto completo](../../../operacion/referentes-20261105/video/asr-complementario/alex-carrera.txt) · [palabras y hashes](../../../operacion/referentes-20261105/video/asr-complementario/alex-carrera.json). Leído íntegro.

- **Inicio 0–13,42 s:** pregunta por ocho editores, presenta ejemplo y afirma reemplazo por una persona con IA. **Desarrollo 13,5–41,98 s:** muestra Antigravity, skills y estilos de edición; afirma que la IA recrea ejemplos más rápido. **Puente/CTA 41,98–57,06 s:** propone transición y entrenamiento de 30 minutos; la ficha visual lee «CLASE» en los subtítulos alrededor de 48,3 s, mientras el ASR produce la frase defectuosa «con la mental clase». La ficha [Alex](alex-carrera.md) también muestra ejemplo, interfaz y miniatura en esa secuencia; la revisión visual no certifica cada palabra.
- **Dudas:** ASR confunde «IA» con «guía»/«idea», «editores» con «pedidores» y fragmenta el CTA. No valida la cifra de tiempo, reemplazo, velocidad ni automatización; son afirmaciones de la pieza. No acredita que se envíe realmente el entrenamiento.

## Hormozi · offers4

Fuente SHA-256 `eabfd9be50808a36b13dfa6fb4c4f0f5cf8a350c987597e4e737e730598122d0`; 691,467 s, 252 segmentos. [Texto íntegro](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-offers4.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-offers4.json). Leído íntegro; ASR inglés sin traducción ni corrección certificada.

- **Inicio 0–55 s:** presenta al emisor y su formación gratuita; remite a otros videos de Acquisition y anuncia la ecuación de valor. **Desarrollo 55–155 s:** resultado deseado y probabilidad percibida frente a tiempo y esfuerzo/sacrificio; ejemplo hipotético de resultado inmediato. **155–338 s:** resultado y riesgo mediante ejemplos y testimonios; **338–449 s:** demora, progreso y esfuerzo. **449–630 s:** compara propuestas y usa Amazon/Netflix para ilustrar conveniencia. Las afirmaciones comerciales y ejemplos médicos son del emisor, no hechos validados aquí.
- **Cierre 631–691 s:** recapitulación de las cuatro variables, invitación a aplicarlas al producto, enlace a formación y anticipo del video siguiente. El último segmento escribe «actors.com»; antes escribe acquisition.com, por lo que la URL final automática es dudosa. La [ficha visual Hormozi](hormozi.md) registra una clase por diapositivas: el texto recuperado añade el hilo verbal sin certificar correspondencia cuadro a cuadro.
- **Dudas:** nombre inicial «Alex Moszi», cifras estadísticas y frase 295 s muestran fallos o formulaciones que requieren contraste. La ecuación y el éxito atribuido a ejemplos no quedan verificados por ASR.


## Hormozi · leads5

Fuente SHA-256 `3ef18d9cb464d864cb55fbc5ac5552810267e1d6b9cfed559175f629a8f29f5b`; 1.787,890 s, 654 segmentos. [Texto completo](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-leads5.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-leads5.json). Leído íntegro en tramos; ASR inglés.

- **Inicio 0–203 s:** enlaza la formación previa de contacto directo con publicar contenido; narra su cambio de opinión sobre marca. **203–342 s:** ventajas y límites de contenido frente al contacto personal. **342–687 s:** unidad de contenido: captar, retener y recompensar; desarrolla temas de experiencias, presente, tendencias y situaciones construidas. **687–1.087 s:** siete rasgos propuestos para titulares y formato adaptado a plataforma. **1.087–1.322 s:** listas, pasos e historias para sostener curiosidad. **1.322–1.603 s:** cumplir la promesa y recompensa; **1.603–1.766 s:** unidades concatenadas y contexto para nuevas audiencias.
- **Cierre 1.766–1.787,66 s:** repasa la sección y anticipa la segunda parte sobre monetización. El CTA identificable es didáctico —practicar y aplicar la estructura—, seguido de transición a la próxima sección; no se infiere un CTA de compra por la descripción externa. La [ficha visual Hormozi](hormozi.md) registra clases con diapositivas y progresión por bloques; el ASR aporta la secuencia verbal, sin verificar cada sincronía visual.
- **Dudas:** el modelo confunde varias expresiones («warm outreach» como «more outreach» en tramos y «content unit» en otros); datos de marcas, causalidad y referencias a estudios son afirmaciones del ponente, no verificaciones de esta revisión.


## Hormozi · leads6

Fuente SHA-256 `aaebb90115b782f6d6e916c581f4b957e047cf556d31274cbd37a6d53e1e3424`; 2.148,380 s, 854 segmentos. [Texto íntegro](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-leads6.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/hormozi-leads6.json). Leído íntegro en tres tramos; ASR inglés.

- **Inicio 0–26 s:** retoma publicación y anuncia monetización. **26–465 s:** relación entre dar y pedir, ejemplos de publicidad y crecimiento; plantea dar en público y pedir en privado. **465–870 s:** CTA integrada o intermitente, ejemplo de recurso gratuito y ejemplo de oferta; aclara 813–816 s que esa CTA de venta es hipotética, y 843–855 s sí invita a consultar el libro. **870–1.204 s:** profundidad en una plataforma frente a amplitud, y su propio proceso de producción. **1.204–1.315 s:** relato de publicidad/contenido, con encuesta atribuida a su negocio. **1.315–1.834 s:** siete lecciones, desde hablar de experiencia propia hasta su observación no demostrada sobre publicación manual. **1.834–1.982 s:** muestra su primer post y anima a empezar. **Cierre 1.982–2.148 s:** métricas de alcance/crecimiento, frecuencia y continuidad.
- La [ficha visual](hormozi.md) muestra clases y progresión gráfica; ASR proporciona el argumento, no sincronía certificada. Las proporciones publicitarias, causalidad, métricas y precios son afirmaciones o ejemplos del emisor; no se toman como reglas actuales verificadas. El ASR escribe «$299» en 430 s: puntuación y precio deben contrastarse antes de citarlo.

## Pedro66 · DfVKglhEtc1

Fuente SHA-256 `86c108cabb8da6543b3cdc5c3e33972266cb1b1771815619da7921b11c031c76`; 66,434 s, 20 segmentos. [Texto íntegro](../../../operacion/referentes-20261105/video/asr-complementario/pedro66.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/pedro66.json). Leído íntegro.

Inicio 0–7 s: alcanzar una meta sin disfrutarla; desarrollo 7–37 s: viaje, coche, relación y negocio; 37–56 s: valorar el presente y evitar comparaciones; cierre 56–65,78 s: hierba y riego. El mapa coincide con [Pedro](pedro.md); no aparece CTA en el texto reconocido. Error claro «Soñar, contener un negocio» en 23,48 s; final «Donde las riegas» requiere contraste con subtítulo visible antes de citarlo.

## Gonzalo Teba · alternativa DfWtlXMsWCs

Fuente SHA-256 `b22b2599906b64d284a7c4b0ad3ce1431c4e4c7fb5c0b00cfc9c89f39732c4f5`; 118,772 s, 20 segmentos. [Texto íntegro](../../../operacion/referentes-20261105/video/asr-complementario/gonzalo-alternativa.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/gonzalo-alternativa.json). Leído íntegro.

Inicio 0–23,72 s: oposición entre disciplina e indisciplina; desarrollo 23,72–61 s: rutina autorreportada; 61–99,64 s: contraste con el reel y aplicación al espectador; cierre 99,64–118,42 s: vuelve a la frase inicial y termina con estructura y rutina. Coincide con [ficha visual](gonzalo-alternativa.md); no se reconoce CTA comercial. Errores en 0–7 y 29–36 s impiden citar literalmente; la rutina no es verificación de hábitos ni prescripción.

## Voltra · asset a081891a8e224825ac38370d1b22d62c

Fuente SHA-256 `365c663ab8880602091c8e50f485421eaf462cd3461b298e0891e21c8f012d48`; 21,461 s, un segmento. [Texto íntegro](../../../operacion/referentes-20261105/video/asr-complementario/voltra.txt) · [palabras, WAV y hashes](../../../operacion/referentes-20261105/video/asr-complementario/voltra.json). Leído íntegro.

ASR agrupa toda la pieza: presenta aspiradora, ahorro de tiempo, carga USB, aspiración/soplado, usos y CTA a la web con financiación y envío. [Ficha visual](voltra.md) sitúa la invitación 15,2–18,2 s y condiciones 18,4–21,4 s, corroboración aproximada, no sincronía fina. ASR escribe «3 gotas» frente a «3 cuotas» en imagen y otras palabras dudosas; ni condiciones ni beneficios quedan comprobados fuera del anuncio.

## Ampliaciones · tres medios con pista

Los tres textos fueron leídos completos; sus intervalos son ASR y las observaciones visuales proceden del muestreo de [ampliaciones](ampliaciones-pedro-erik-toto.md).

- **Pedro Dem097KgI-A** · fuente SHA-256 `8e384f0e1d498199f8eb823e8317c8061997e3b82ffaf015971bdee9b6b18260`; 74,817 s, 13 segmentos. [Texto](../../../operacion/referentes-20261105/video/asr-complementario/dem097kgi-a.txt) · [palabras/hashes](../../../operacion/referentes-20261105/video/asr-complementario/dem097kgi-a.json). Inicio 0–9,38: posición problemática del negocio; desarrollo 9,66–59,38: dependencia del dueño y reestructuración; 59,64–74,64: webinar y comentario «escala» para acceso privado. Coincide aproximadamente con diagrama y CTA visibles; no acredita envío de mensaje o evento vigente. «Todo separa» a 21,68–25,90 es error probable.
- **Pedro DehhvYDAWDl** · fuente SHA-256 `f1719caaf498e35f65f2d6723d6fcf75c8b3996b3195cfb2851a9bdd99d4c1cb`; 101,655 s, 17 segmentos. [Texto](../../../operacion/referentes-20261105/video/asr-complementario/dehhvydawdl.txt) · [palabras/hashes](../../../operacion/referentes-20261105/video/asr-complementario/dehhvydawdl.json). Inicio 0–22: oferta validada sin tráfico suficiente; desarrollo 22–94,54: caso de chefs, oferta, anuncios y cifras declaradas; cierre 94,54–101,10: invita a chefs interesados a contactar al cliente etiquetado, seguido de «patrón». Esto añade una CTA verbal específica a la ficha, que sólo había acreditado CTA «oferta» en el caption y no la había visto al cierre; son acciones distintas. Cifras y garantía son alegaciones no auditadas; ASR confunde «afilarla» y otras palabras.
- **Toto LinkedIn** · fuente SHA-256 `f31c9e96cea253ba5be44fde39a032666e93f216fd6cb4014f77f60d34047596`; 60,604 s, 26 segmentos. [Texto](../../../operacion/referentes-20261105/video/asr-complementario/toto-linkedin.txt) · [palabras/hashes](../../../operacion/referentes-20261105/video/asr-complementario/toto-linkedin.json). Inicio 0–6,42: video viral y presentación; desarrollo 6,58–37,10: cliente, primer intento, segunda oportunidad y elección de creador; 37,26–50,56: vistas y descargas declaradas; cierre 50,68–60,40: conclusión y seguir para aprender y conocer el proyecto. Coincide aproximadamente con la ficha visual; el ASR altera «Marz» como «Mars» y dice «dos millones de videos» en 22–26 s, una expresión dudosa que requiere escucha humana. No acredita causalidad ni cifras.

El clip del carrusel sin pista no se procesó; Erik ya contaba con captions. No se ejecutaron nuevas pruebas acústicas. Los 13 ASR están terminados y leídos; sus JSON preservan salida derivada exacta, errores y tiempos por palabra. Ninguno sustituye escucha, revisión de voz/música/SFX/ambiente/silencios perceptuales o sincronía.


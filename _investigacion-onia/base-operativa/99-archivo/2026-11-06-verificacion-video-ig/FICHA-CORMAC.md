# Cormac Hayden: qué muestra y qué permite aprender

Reel único: [DfWLWspIruU](https://www.instagram.com/reel/DfWLWspIruU/), publicado por **Cormac Hayden, `cormachdn`**, según metadata local recuperada de la plataforma. Esta atribución identifica la cuenta publicadora; no certifica la autoría de todos los elementos insertados. Alex Carrera (`alexmcarrera`) corresponde a otra pieza y queda fuera de este piloto.

**Resultado final de este piloto:** lectura visual por muestreo y contenido verbal obtenido mediante ASR existente. La ruta audiovisual conjunta ensayada no quedó aceptada: superó el negativo de silencio y falló el positivo de voz/orden. No se ejecutó esa ruta sobre Cormac. Se eligió FFmpeg + faster-whisper + Silero; no se instaló ni volvió a transcribir el reel en esta retoma.

## Actualización modular: edición y texto

La [lectura modular completa](lectura-modular-cormac.md) añade una pasada de los 2264 frames con PTS, tres cortes de contenido confirmados (3,466667;7,2;14,666667 s), dos reencuadres abruptos y tres saltos menores ambiguos. Se distinguen fin del vídeo37,733333s y contenedor37,753991s. Las duraciones por bloque y vecinos nativos están enlazados allí; no se afirma un conteo exhaustivo de planos.

Seis recortes se compararon con referencia visual de un agente fijada antes de Tesseract. OCRraw coincide en1/6 y da un falso positivo en el recorte sin texto: no queda aceptado como fuente autónoma. Las lecturas visuales etiquetadas sí se conservan. Esto amplía la lectura visual previa; no añade escucha ni cambia el rechazo histórico de la ruta AV conjunta.

## Evidencia y cobertura

Original de 37,753991 s, 10 749 782 bytes; SHA-256 `9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e`, cotejado de nuevo sin modificarlo. [Recibo de ingesta](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/ingesta-cormac-v1.json).

Se inspeccionaron las dos hojas existentes, `contacto.jpg` y `cierre.jpg`: 25 + 13 muestras descritas en la preparación como 1 Hz. No se recuperó aquí un manifiesto de PTS individual: los intervalos de esta ficha son aproximados y se apoyan en ASR, no en una medición de cada corte. Las muestras cubren la estructura general de la pieza; no equivalen a observar continuamente todos sus fotogramas ni a escuchar su pista.

El ASR local tiene 18 segmentos, de 0 a 37,84 s; el último tiempo automático excede la duración del contenedor. El ASR VPS existente tiene 11 segmentos y finaliza en 37,44 s, sobre un WAV decodificado de 37,7803125 s. Faster-whisper small CPU int8 con Silero conservó toda esa pista en su VAD. No son límites de voz certificados ni prueban sincronía fina.

El cotejo automático nuevo de ambas transcripciones encontró 154 unidades normalizadas por salida, similitud de secuencia 0,993506 y una sustitución: `Halo` / `Halos`. Esa coincidencia no es una referencia humana. Se mantienen dudosas la construcción inglesa de transición y la mención de contactos/contexto personal; no se corrigen por intuición. [Cotejo e integridad de esta retoma](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/retoma-cormac-v1.json). Las salidas literales permanecen en los originales auxiliares; esta ficha resume su contenido.

## Guion y lectura visual

| Tramo aproximado | Contenido verbal resumido del ASR | Evidencia visual y función inferida |
|---|---|---|
| 0–3,4 s | Pregunta por qué seguimos trabajando si la IA puede hacer estas tareas. | Presentador con micrófono de mano, plano cercano, estantería y luz cálida. Gancho que abre una promesa amplia. |
| 3,4–7,2 s | Dice haber dado al agente acceso a su ordenador para delegar tareas. | Inserto de escritorio con varias ventanas, listas y calculadora. Hace visible el objeto de la promesa; las ventanas abiertas no prueban tareas terminadas. |
| 7,2–14,6 s | Presenta Agent Desktop como herramienta para acceder a ventanas y archivos. | Pantalla con repositorio y documentación `agent-desktop`; un dedo señala la referencia. Pasa de promesa a herramienta concreta, sin mostrar un recorrido completo de instalación y resultado. |
| 14,6–35 s | Describe integración con su sistema personal, datos, pendientes y mensajes. | Regresa al presentador. La explicación ocupa la mayor parte final; la operación afirmada no queda auditada mediante un antes/después legible. |
| 35–37,75 s | Retoma la pregunta de si dejaremos de trabajar. | Continúa el presentador; en las muestras no aparece una placa final de compra. Cierre que vuelve al gancho, según texto ASR. |

La edición visible alterna tres tipos de imagen: cara, escritorio y repositorio. Esa estructura ayuda a conectar persona, uso y referencia técnica. No se midieron duración exacta de planos, velocidad de cortes, transiciones entre muestras ni retención.

Los subtítulos observados son blancos, de apariencia sans serif, pequeños y centrados en la zona inferior del contenido. Se muestran en fragmentos cortos. La familia tipográfica exacta no está acreditada y no se deduce del parecido. En el inserto horizontal del escritorio aparecen áreas negras dentro del formato vertical; el repositorio se presenta mediante una grabación de pantalla física. No se certifica legibilidad de los textos pequeños de todas las ventanas.

## Afirmaciones y veracidad

| Afirmación de la pieza | Qué la respalda | Qué falta demostrar |
|---|---|---|
| Existe una herramienta Agent Desktop para operar aplicaciones. | Repositorio visible y documentación oficial consultada en la [ficha previa](../../02-contenido/reels-e-ideas/DfWLWspIruU.md). Esa investigación describe una interfaz de accesibilidad y un agente externo que decide las acciones. | No se instaló ni probó Agent Desktop en este encargo; el reel no valida su funcionamiento en ONIA. |
| El agente puede resolver cualquier tarea y acceder a cualquier ventana o archivo. | Es una afirmación verbal del autor; se ven ventanas abiertas. | Cobertura universal, permisos, fiabilidad y resultado de una tarea completa. No acreditado. |
| Su sistema personal integra contexto, contactos y mensajes para actuar como él. | Descripción y ASR atribuidos al autor; la descripción menciona `@askhalos`. | Implementación, consentimiento de acceso, precisión, envíos y tasa de error. No auditado aquí. |
| La automatización permite dejar de trabajar. | Pregunta retórica del guion. | Ahorro medido, coste, intervención y fiabilidad en trabajo real. No demostrado por esta pieza. |

Hay una referencia técnica concreta y una demostración visual parcial. Las promesas generales siguen sin verificar; ni el ASR ni mostrar aplicaciones bastan para convertirlas en resultados probados. No se inició una investigación adicional del producto Halos.

## Qué tomar para ONIA

Usar la secuencia **problema concreto → herramienta visible → tarea pequeña → resultado recuperable**. Conservar cara y contexto cuando ayuden a entender la demostración, pero cerrar con un resultado legible y verificable: archivo antes/después, tiempo, intervención y error. Ésta es una propuesta de aplicación, no una nueva automatización ejecutada.

La pieza aporta un modo de presentar una herramienta; no demuestra autonomía total. ONIA puede mejorar su comprobabilidad mostrando exactamente qué tarea termina y qué autorización utiliza. Ninguna observación de esta ficha acredita música, efectos, prosodia, mezcla o sincronía audiovisual fina.

## Estado del ensayo AV y secuencia de trabajo

La continuación HTTP Range agregó exactamente 923 146 720 bytes al parcial de visión y verificó su SHA final; los tres pesos están completos y LLM/audio no se volvieron a descargar. La transferencia duró 173,04 s.

**El negativo de 2 s está ejecutado y aceptado de forma acotada.** Una invocación terminó con salida 0 en 135,60 s. Dos imágenes y dos WAV de 16 000 muestras fueron decodificados, codificados y aceptados; 210 posiciones de entrada más 128 reservadas para respuesta dieron 338 frente a contexto efectivo 2048. La respuesta identifica gris uniforme, silencio y ausencia de cambios, sin inventar sonido. Se recuperaron y cotejaron 21 archivos; la revisora confirmó wrapper, argumentos, telemetría y cierre. [Recibo y dictamen](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/negativo-aceptado-v1.json).

El positivo usó el flite `kal16` ya incluido en FFmpeg: frase generada de 13 823 muestras (0,8639375 s), sin truncar y con ceros hasta 1 s, sobre cuadrado rojo a izquierda. El segundo segundo contiene ceros exactos y un círculo azul a derecha. La verdad procede del generador, no de audición humana; no se pasó al modelo.

Un primer driver se detuvo antes de inferir por apuntar al prompt antiguo. Se preservó ese fallo y una copia nueva corrigió sólo la referencia canónica. La **primera inferencia positiva real** terminó con salida 0 en 133,61 s, contexto 338 < 2048 y ambas modalidades aceptadas. Sin embargo, describió sonidos descendentes/ascendentes en lugar de reconocer la voz y su frase; omitió el silencio final y afirmó simultaneidad. Identificó las dos figuras, pero no estableció correctamente su secuencia. Esa respuesta no mide sincronía fina ni permite afirmar que todos los cambios de tono sean inventados: no hubo audición humana. Se rechazó este control semántico y se detuvo la ruta, sin repetirlo ni procesar Cormac con ella. [Recibos del positivo](piloto-cloud/positivo-v2/result.json) y [evaluación respecto de la verdad](piloto-cloud/positivo-v2/assessment.json).

Los dos modelos de control consumieron 269,21 s de tiempo de pared sumado, incluyendo sus fases registradas; no es consumo CPU ni coste de analizar Cormac. El mayor RSS muestreado fue 10 784 448 512 bytes, sin garantizar un pico exacto o encaje en VPS. La CPU real no quedó capturada. Los logs permiten observar carga inicial y tiempos del encoder de imagen, pero no separar prefill y decode.

Cormac sí quedó disponible en Cloud mediante las dos pistas CDN de la misma pieza pública, sin cookies ni instalaciones. Sus huellas de paquetes de vídeo y audio coinciden con las del original local. Esa coincidencia no acredita equivalencia exacta de timestamps ni decodificación integral. El remux tiene 10 749 773 bytes, duración declarada 37,78 s y SHA `2c89164b66a9c556e749b789e0ca2004562c859316ac447ba883f7535f5a79a5`: es una variante de contenedor, no una copia binaria del original. Las URLs temporales permanecen privadas y no están en la exportación. [Relación entre pistas y original](piloto-cloud/cormac-transfer-v1/transfer-receipt.json).

Cobertura final: ASR existente sobre la pista completa, 38 muestras visuales y **0 s de análisis audiovisual conjunto de Cormac**. No se cubrió el reel con una ventana de 3 s ni se presentó ese recorte como análisis completo. La estimación desde los registros daba 3182 posiciones para 38 entradas frente a contexto 2048 y unos 741 s sólo de encoder visual; habría requerido ventanas consecutivas y más tiempo, pero no se ejecutaron tras fallar el positivo. La transcripción y la lectura visual anteriores conservan su alcance; no se acreditan música, efectos, entonación, ritmo sonoro o sincronía fina. No se repitieron la batería de ocho controles, suites o corpus. [Cierre recuperable](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/cierre-cormac-v1.json).

Secuencia indicada por Sergio: primero cerrar el método y Cormac; después completar el cerebro de referentes; al final planificar el trabajo full Cloud. El workspace actual es un laboratorio de esta prueba, sin migración, despliegue ni nuevos servicios. [Entrega y consumo](ENTREGA.md).


## Cierre posterior: PANNs, 6 de noviembre de 2026

La prueba PANNs terminó y fue revisada: seis inferencias offline, dos controles conocidos del generador y cuatro ventanas que cubren los 37,78 s de audio del remux Cormac; 0 s visuales. Los criterios pareados congelados distinguieron voz de ceros y del silencio final. En Cormac, Speech supera Music en las cuatro ventanas; son scores sin umbral calibrado, no probabilidades ni prueba de ausencia de música.

Dictamen: señal auxiliar experimental de actividad de habla en estas entradas. No detector validado, efectos, límites exactos, palabras, emoción/prosodia, mezcla, sincronía o percepción integral. Grid 10 ms interpolado. CPU1/AS3 GiB, máximo 27,13 s por entrada y RSS máximo muestreado 1.267.875.840 B; limpieza comprobada. La revisión anterior de cero inferencias correspondía al bloqueo previo, superado sin alterar sus evidencias.

[Resultado breve y límites](PANNs-RESULTADO.md) · [Recibo final](panns-cloud-setup-v3/final-result.json) · [Revisión](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/panns-revision-v1.json). Exportes locales 21/21 verificados; ZIP de curvas completas sólo en laboratorio Cloud, sin publicación ni garantía de persistencia permanente. Prueba cerrada; audiovisual integral pendiente. No nuevos ensayos ni trabajo sobre cerebro/Cloud en esta unidad.

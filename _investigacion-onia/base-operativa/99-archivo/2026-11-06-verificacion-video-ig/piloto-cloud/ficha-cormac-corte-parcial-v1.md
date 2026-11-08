# Cormac Hayden: qué muestra y qué permite aprender

Reel único: [DfWLWspIruU](https://www.instagram.com/reel/DfWLWspIruU/), publicado por **Cormac Hayden, `cormachdn`**, según metadata local recuperada de la plataforma. Esta atribución identifica la cuenta publicadora; no certifica la autoría de todos los elementos insertados. Alex Carrera (`alexmcarrera`) corresponde a otra pieza y queda fuera de este piloto.

**Resultado disponible:** lectura visual por muestreo y contenido verbal obtenido mediante ASR existente. La percepción audiovisual conjunta sigue pendiente del ensayo acotado descrito al final. Se eligió FFmpeg + faster-whisper + Silero; no se instaló ni volvió a transcribir el reel en esta retoma.

## Evidencia y cobertura

Original de 37,753991 s, 10 749 782 bytes; SHA-256 `9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e`, cotejado de nuevo sin modificarlo. [Recibo de ingesta](../../continuidad/evidencias/capacidad-audiovisual-001/ingesta-cormac-v1.json).

Se inspeccionaron las dos hojas existentes, `contacto.jpg` y `cierre.jpg`: 25 + 13 muestras descritas en la preparación como 1 Hz. No se recuperó aquí un manifiesto de PTS individual: los intervalos de esta ficha son aproximados y se apoyan en ASR, no en una medición de cada corte. Las muestras cubren la estructura general de la pieza; no equivalen a observar continuamente todos sus fotogramas ni a escuchar su pista.

El ASR local tiene 18 segmentos, de 0 a 37,84 s; el último tiempo automático excede la duración del contenedor. El ASR VPS existente tiene 11 segmentos y finaliza en 37,44 s, sobre un WAV decodificado de 37,7803125 s. Faster-whisper small CPU int8 con Silero conservó toda esa pista en su VAD. No son límites de voz certificados ni prueban sincronía fina.

El cotejo automático nuevo de ambas transcripciones encontró 154 unidades normalizadas por salida, similitud de secuencia 0,993506 y una sustitución: `Halo` / `Halos`. Esa coincidencia no es una referencia humana. Se mantienen dudosas la construcción inglesa de transición y la mención de contactos/contexto personal; no se corrigen por intuición. [Cotejo e integridad de esta retoma](../../continuidad/evidencias/capacidad-audiovisual-001/retoma-cormac-v1.json). Las salidas literales permanecen en los originales auxiliares; esta ficha resume su contenido.

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
| Existe una herramienta Agent Desktop para operar aplicaciones. | Repositorio visible y documentación oficial consultada en la [ficha previa](../reels-e-ideas/DfWLWspIruU.md). Esa investigación describe una interfaz de accesibilidad y un agente externo que decide las acciones. | No se instaló ni probó Agent Desktop en este encargo; el reel no valida su funcionamiento en ONIA. |
| El agente puede resolver cualquier tarea y acceder a cualquier ventana o archivo. | Es una afirmación verbal del autor; se ven ventanas abiertas. | Cobertura universal, permisos, fiabilidad y resultado de una tarea completa. No acreditado. |
| Su sistema personal integra contexto, contactos y mensajes para actuar como él. | Descripción y ASR atribuidos al autor; la descripción menciona `@askhalos`. | Implementación, consentimiento de acceso, precisión, envíos y tasa de error. No auditado aquí. |
| La automatización permite dejar de trabajar. | Pregunta retórica del guion. | Ahorro medido, coste, intervención y fiabilidad en trabajo real. No demostrado por esta pieza. |

Hay una referencia técnica concreta y una demostración visual parcial. Las promesas generales siguen sin verificar; ni el ASR ni mostrar aplicaciones bastan para convertirlas en resultados probados. No se inició una investigación adicional del producto Halos.

## Qué tomar para ONIA

Usar la secuencia **problema concreto → herramienta visible → tarea pequeña → resultado recuperable**. Conservar cara y contexto cuando ayuden a entender la demostración, pero cerrar con un resultado legible y verificable: archivo antes/después, tiempo, intervención y error. Ésta es una propuesta de aplicación, no una nueva automatización ejecutada.

La pieza aporta un modo de presentar una herramienta; no demuestra autonomía total. ONIA puede mejorar su comprobabilidad mostrando exactamente qué tarea termina y qué autorización utiliza. Ninguna observación de esta ficha acredita música, efectos, prosodia, mezcla o sincronía audiovisual fina.

## Estado del ensayo AV y secuencia de trabajo

El runtime ya compilado conserva LLM y audio verificados y un parcial del mismo peso de visión. Se despachó al editor Cloud existente una continuación HTTP Range con tamaño y SHA finales; después, si los tres pesos y el presupuesto coinciden, una sola ejecución del negativo de 2 s ya fijado. **Resultado de esta retoma: pendiente de recibo.** No se ha contado como ejecutado ni aprobado.

Sólo si el negativo pasa procede un positivo controlado de voz e imagen/orden con señales existentes. Después se analiza este único reel en ventanas que quepan realmente, declarando su cobertura. Un fallo detiene esa ruta y se incorpora a la ficha sin invalidar lo observado por ASR o muestreo. No se repite la batería de ocho controles, suites o corpus por rutina.

Secuencia indicada por Sergio: primero cerrar el método y Cormac; después completar el cerebro de referentes; al final planificar el trabajo full Cloud. El workspace actual es un laboratorio de esta prueba, sin migración, despliegue ni nuevos servicios. [Entrega y consumo](ENTREGA.md).

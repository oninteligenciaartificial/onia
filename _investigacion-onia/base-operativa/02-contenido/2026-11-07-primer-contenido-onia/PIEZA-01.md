# Pieza 01 · Cómo retomar una tarea en otro chat

Borrador de contenido para la marca personal de Sergio con un caso real de ONIA. El público inicial propuesto son personas que usan IA para trabajar y pierden el hilo al cambiar de chat. Formato vertical de unos 40 segundos con Sergio a cámara y una tarjeta de prueba. La meta es que el espectador pueda explicar qué dejar preparado para que otro chat continúe.

## Guion y puesta en escena

**Portada** · Cómo pasar una tarea a otro chat

| Tiempo orientativo | Locución | Apoyo visual |
|---|---|---|
| 0–7 s | «En ONIA probamos si un chat nuevo podía seguir una tarea sin recibir la conversación anterior.» | Sergio a cámara. Título breve, «¿Puede seguir otro chat?». |
| 7–17 s | «Le dimos el ID y dónde encontrar la versión guardada del registro. Recuperó el objetivo, el archivo de entrada y el siguiente paso.» | Una tarjeta con tres renglones, «Objetivo», «Entrada», «Siguiente paso». Mostrar un renglón por idea. |
| 17–29 s | «La segunda sesión recalculó con el mismo archivo. Las dos llegaron a nueve unidades y un total de 56,50 con datos de prueba.» | Tarjeta central con los dos resultados, «Sesión A» y «Sesión B». Mantener visible «Datos ficticios». Los números proceden del piloto. |
| 29–40 s | «Antes de cerrar tu próximo chat, dejá escritos el objetivo, el enlace a la evidencia y el siguiente paso. Así la otra sesión sabe por dónde empezar.» | Regresar a cámara y cerrar con los tres elementos en pantalla. |

**Texto de publicación propuesto** · En ONIA hicimos una prueba con dos sesiones. La segunda recuperó el registro de la tarea y repitió el cálculo. Antes de pasar un trabajo a otro chat, dejá a mano el objetivo, la evidencia y el siguiente paso.

**Criterio visual** · Una idea principal por escena. El rostro conduce la explicación y la tarjeta ocupa el foco cuando se compara el cálculo. Reservar una zona para subtítulos que no tape los datos. La tarjeta recrea el recibo y rotula los datos como ficticios. El tiempo final se ajusta tras leer el guion en voz alta. [Tarjeta lista para insertar](TARJETA-PRUEBA.png) · [Original editable](TARJETA-PRUEBA.svg)

## Referencia aplicada · San Muñoz

Inspección directa del archivo del tutorial disponible en el PC. Se extrajo una imagen por resultado a los tiempos de búsqueda 11:50, 15:10 y 19:05. La sesión Cloud devolvió HTTP 403 al consultar YouTube, por lo que las imágenes se revisaron localmente. La cobertura de este análisis son esas tres imágenes, suficiente para contrastar su composición estática. [Tutorial original](https://www.youtube.com/watch?v=anrAaNvbp4M)

| Muestra | Decisión visual observada |
|---|---|
| 11:50 · nivel 1 | El resultado de la izquierda conserva rostro, título y subtítulo. El presentador del tutorial ocupa un panel mayor a la derecha. |
| 15:10 · nivel 2 | El rostro del resultado baja y se encierra en una ventana. Aparecen un encabezado grande y una barra de progreso en el espacio superior. |
| 19:05 · nivel 3 | La palabra «ANIMACIONES» toma el foco con tamaño y color. «Detalladas» aparece en el texto superior y en el subtítulo, con dos énfasis sobre el mismo mensaje. |

La decisión aplicada es pasar de rostro a tarjeta cuando cambia la pregunta del espectador, de cómo se hizo a cómo se comprobó. En la tarjeta, el total coincidente recibe el mayor contraste y se conserva un solo renglón de apoyo para unidades. La comparación visual orienta el diseño. La legibilidad en el corte vertical se comprobará con el primer montaje.

## Material y criterio de revisión

- Grabar una toma vertical de Sergio con el guion. Usar los tres renglones de traspaso como texto en pantalla e insertar la tarjeta del resultado ya preparada. Revisar locución y subtítulos juntos en la edición.
- La afirmación es específica al piloto. B recibió ID, repositorio, commit y ubicación. Recuperó la tarea y recalculó a partir del CSV. Los recibos respaldan las cifras y el contexto de prueba. [Informe del piloto](../../99-archivo/2026-11-06/consolidacion-harness/INFORME.md) · [Resultado A](../../04-operacion-agentes/evidencias/continuidad-cloud-001/informe-a-v1.json) · [Resultado B](../../04-operacion-agentes/evidencias/continuidad-cloud-001/veredicto-b-v1.json)
- El revisor debe poder responder qué recibió la segunda sesión, cómo se comprobó que pudo seguir y qué debería guardar el espectador al cerrar su chat. Antes de grabar, verificar legibilidad de la prueba y distinguir la coincidencia de dos cálculos de una promesa general de continuidad.
- Una revisión independiente del borrador cotejó esas tres respuestas y las cifras con los recibos. A partir de ese cotejo se precisó en la locución que el registro tenía una versión guardada y que B recalculó con el mismo archivo. Se comprobó la legibilidad de la tarjeta exportada. Falta verla con los subtítulos del montaje.

## Flujo de trabajo para las próximas piezas

1. **Entrada.** La sesión Reels e ideas registra el enlace o idea y una pregunta concreta. Ejemplo: «¿Qué decisión hace más legible la prueba?». [Entrada de referencias](../reels-e-ideas/README.md)
2. **Selección.** Coordinación decide si la pregunta se responde con texto, una captura, un tramo o la página de destino. El ejecutor recibe sólo la fuente y ese alcance. El QA y el perfil de modelo se toman de las reglas vigentes. [QA de ONIA](../../04-operacion-agentes/ORQUESTACION.md#qa-previo-de-videos-recibidos)
3. **Aplicación.** Escribir una observación con fuente y tiempo, una decisión para la pieza y un guion sobre un caso propio. La misma ficha conserva evidencia, toma o recursos necesarios y acción propuesta.
4. **Revisión y retoma.** Un revisor comprueba la afirmación y qué entiende del borrador. Guardar la corrección y el próximo paso con la pieza para que otra sesión la pueda retomar. Registrar el resultado de publicación o prueba cuando exista.

Formato mínimo para repetir el flujo: **público y pregunta → fuente y cobertura → decisión aplicada → guion y recursos → criterio de revisión → siguiente acción**. Usar la sesión Cloud existente para la ejecución que corresponda y conservar el resultado recuperable en la base operativa. [Reparto de sesiones](../../04-operacion-agentes/SESIONES.md) · [Continuidad Cloud](../../05-herramientas/cloud/CONTINUIDAD.md)

**Siguiente acción de esta pieza** · Grabar una toma con el guion, insertar la tarjeta en el momento de la comprobación y revisar la comprensión de ese primer corte. Grabación y montaje pendientes.

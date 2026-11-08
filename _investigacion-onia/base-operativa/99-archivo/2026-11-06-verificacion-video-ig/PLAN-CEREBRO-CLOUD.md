# Plan de trabajo: videos, cerebro y Cloud

6 de noviembre de 2026, America/Caracas. Plan preparado para presentar a Sergio antes del lanzamiento por etapas. No es una declaración de tareas ejecutadas o despliegue. El estado del piloto está en el registro `capacidad-audiovisual-001`, revisión 26 al preparar esta nota; no se duplica aquí su historial.

## Resultado buscado y orden

1. Método audiovisual con capacidades y límites comprobados.
2. Cerebro consultable de los referentes y muestras ya seleccionados.
3. Ejecución Cloud recuperable, con permisos, almacenamiento y consumo controlados.

Fuentes: [reglas](../../04-operacion-agentes/reglas-comunes.md), [orquestación](../../04-operacion-agentes/ORQUESTACION.md), [piloto modular](lectura-modular-cormac.md), [matriz de referentes](../../03-referentes/corpus-2026-11-05/GOAL-REFERENTES.md) y [pendientes perceptuales](../../03-referentes/fichas/audiovisual/pendientes-visuales-finitos.md). Las instrucciones actuales de Sergio prevalecen. No usar ONIA-CENTRAL.

## 1. Completar el método de videos

Conservar FFmpeg, ASR con faster-whisper/Silero y lectura visual de recortes fechados. Tesseract raw no se acepta como transcriptor autónomo. Los cortes medidos no equivalen a percibir fluidez, música o entonación.

Primer encargo propuesto: un ensayo acústico acotado de PANNs, como clasificador de eventos, reutilizando la [investigación y especificación existentes](../../03-referentes/fichas/audiovisual/investigacion-previa-modulos.md). Esa fuente ya recuperó LICENSE.MIT del repo/wheel; corrige la incertidumbre de licencia expresada en la nota reciente de alternativas. Conservar la anomalía literal del copyright, versiones, avisos y licencia de pesos. No repetir búsqueda de familias ni pruebas rechazadas idénticas.

Separar calibración de evaluación; congelar categorías, umbrales y referencias antes de los resultados evaluados. Medir silencio, voz, música, efectos y orden, además de memoria/tiempo. Inferencia aislada, sin descarga implícita; recursos efectivos comprobados antes de instalar, con cortes de proceso y reserva del host. Una falla excluyente detiene la aplicación al corpus; un acierto valida sólo ese atributo, idioma y mezcla.

Después, aplicar únicamente capacidades aprobadas a Cormac. La prosodia comunicativa, mezcla, sincronía fina y experiencia temporal requieren una vía perceptual que aún no está validada: PANNs no las resuelve por clasificar sonidos. El cierre integral sigue condicionado a esa evidencia; cualquier intervención humana necesaria se delimita por atributo e intervalo, sin encargar otra revisión indiscriminada del corpus.

**Entrega:** ficha de capacidades por componente, resultados literales y prueba en el mismo reel con cobertura explícita. No ampliar a los 40 medios mientras un módulo pertinente siga sin superar su control.

## 2. Integrar el cerebro existente

Alcance conservado: 17 personas y Voltra; 40 medios, ocho imágenes y documentos existentes. Cormac es una pieza complementaria de calibración, no otro referente agregado automáticamente.

Primer lote de transferencia del método: Alex Carrera y Voltra. Luego avanzar por los siete grupos ya definidos, con una cola finita y lotes pequeños. Reutilizar transcripciones, imágenes y fichas; procesar solamente brechas identificadas. Una revisión local no se generaliza a toda la duración de un video largo.

Por referente: fuentes, enseñanza, mecanismo, ejemplo, contraejemplo, aplicación posible a ONIA y límites. Cada afirmación relevante debe recuperar su pieza y, si corresponde, intervalo. El cerebro será un índice y síntesis consultables; no entrenamiento de pesos ni copia de cursos.

**Aceptación:** poder responder una consulta práctica con respaldo recuperable y declarar cuándo falta evidencia. Mantener separados el cierre documental/visual útil y el cierre audiovisual integral.

## 3. Preparar y probar Cloud

Usar el repositorio operativo y entorno `onia` existentes. Código, reglas y registros ligeros versionados; medios privados en almacenamiento persistente privado, con manifiesto e integridad; temporales como caché descartable. Elegir soporte, retención y coste antes de contratar o activar nada. Una VM de laboratorio no prueba persistencia permanente.

Empaquetar sólo la ruta aceptada y comprobar: disponibilidad real de entradas, dependencias/licencias, ejecución de una pieza, interrupción y retoma desde otra sesión, ausencia de trabajo duplicado, conservación de reglas y límites de consumo. Reutilizar la continuidad A→Git→B ya aprobada; probar las diferencias audiovisuales nuevas.

**Aceptación:** otra sesión recupera la tarea y continúa con resultados accesibles, sin releer todo el chat. El funcionamiento continuo requerirá después un ejecutor programado, persistencia, supervisión y presupuesto concretos; no nace de una instrucción de proactividad.

## Coordinación, modelos y contexto

Una coordinadora en este chat, una ejecutora en el chat integrador y una revisora independiente. Un escritor por archivo; subagentes temporales sólo para partes separables. Brief breve con objetivo, entradas, reglas pertinentes, salida y aceptación; estado y evidencia viven en archivos, no en memoria del chat.

Sol medio para coordinación, integración y revisión acotada; subir esfuerzo sólo ante un fallo de razonamiento identificado. FFmpeg/ASR/clasificación no necesitan un LLM generativo para sus operaciones. Un modelo menor para extracción repetible es candidato a comparar, no ahorro ni calidad demostrados. Registrar modelo recomendado, solicitado y observado.

Un lote activo, sin relanzar suites históricas. Proactividad: tomar la siguiente unidad autorizada, ejecutar, comprobar, registrar y avisar por un cambio material. Cuota observada al planificar: 96 % semanal usado/4 % restante, compartida entre chats; no atribuible a esta tarea. No consumir restablecimientos ni comprar créditos desde este plan.

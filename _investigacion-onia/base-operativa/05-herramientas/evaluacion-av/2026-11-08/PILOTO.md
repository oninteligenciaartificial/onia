# Piloto propuesto · clip autorizado de 60–90 segundos

**Diseñado, no ejecutado. Requiere el sí de Sergio.** Objetivo: medir qué añade OCR a nuestro método y qué atributos siguen sin resolver, con límites compatibles con el VPS. No certificar un “mirador integral” a partir de acertar una transcripción.

## Material y referencia independiente

Elegir un clip de OnIA de unos75s, o uno con licencia/permiso que cubra el análisis y las anotaciones que se publicarán. Aún no está elegido. Tener URL pública no concede redistribución. Guardar en privado el original; versionar sólo identidad, SHA256, procedencia, permiso referenciado sin datos personales y métricas/observaciones que se puedan compartir. No subir medios, caras, voces, cookies o transcripciones completas por defecto.

El clip debe contener voz española, nombres/cifras/negaciones, al menos8 textos en pantalla,6 cambios de plano y una transición gradual, un tramo de silencio y eventos audibles conocidos. Idealmente dos hablantes autorizados y cambios de turno; si sólo hay uno, diarización queda **no evaluada**, no aprobada. Música/SFX deben ser propios o con derechos adecuados. No crear clones de voz. Si faltan esos atributos, no inventar un resultado para ellos.

Antes de mostrar salidas de herramientas, una persona que pueda **ver y oír** el clip fija una referencia: transcripción literal,10citas cortas con inicio/fin, textos y cajas/intervalos visibles, cortes/transiciones, turnos anónimos, música/efectos/voz y10eventos con tiempos cuando existan. Otra revisión contrasta errores y desacuerdos. Si no hay escucha/visionado humano ni referencia autorizada fiable, queda pendiente la validación semántica de sonido. Los modelos no fabrican su propio patrón de verdad.

Congelar referencia y parámetros; no retocar umbrales después de ver errores en el segmento reservado. Usar los primeros20s para ajuste y el resto para evaluación retenida; un solo clip es prueba de viabilidad, no validación general de todos los referentes.

## Variantes comparables

| Variante | Procedimiento propuesto | Qué permite atribuir |
|---|---|---|
| A · método actual | Mismo faster-whisper small offline, CPU/int8,2hilos1worker, VAD/beam actuales; conservar cuadros con su PTS y el muestreo1Hz utilizado en fichas. No sumar un clasificador sonoro inexistente. | Línea base de transcripción, tiempos y lectura visual muestreada. Registrar abstención en sonido/diarización en lugar de fingir éxito. |
| B · instrumental existente | Misma salida ASR; ffprobe/FFmpeg para PTS, `scdet` sobre secuencia y estadísticas acústicas. Seleccionar cuadros por cortes y hasta4Hz, máximo400cuadros. Sin instalar nada. | Efecto de cobertura/muestreo y detector existente separado del efecto OCR. Energía/onsets candidatos no son etiquetas semánticas. |
| C · ampliación mínima | Reusar exactamente los cuadros/PTS de B y el mismo ASR; sólo añadir detector/reconocedor PaddleOCR mobile en venv separado, CPU2hilos/batch1. Guardar texto literal, caja, confianza e intervalo observado; deduplicación con límites explícitos. | Aporte incremental de OCR, sin atribuirle mejoras de ASR o cortes. Confianza del modelo no equivale a probabilidad calibrada. |

No instalar PySceneDetect, WhisperX, librosa o MiniCPM en este piloto mínimo. Si B falla en cortes, proponer luego una comparación puntual de PySceneDetect Adaptive con otro sí. Si fallan fronteras de palabras, evaluar primero `word_timestamps=True` del motor existente; WhisperX sólo después de resolver licencia del alineador. Sonido semántico y comprensión conjunta son un futuro experimento distinto, con controles propios; no habilitados por este piloto.

## Línea de tiempo y controles

- Registrar time_base, start_time y PTS reales de audio/video, frecuencia de muestreo y duración. No sustituirlos por `n/fps` en un video VFR ni deducir sincronía de duraciones casi iguales.
- Mantener una correspondencia explícita entre tiempo del medio, muestras PCM, segmentos ASR y fotogramas; cualquier remuestreo o cambio de origen debe quedar en el manifiesto. No normalizar ni recortar voz silenciosamente.
- FFmpeg recorre los cuadros necesarios para cortes; OCR usa muestras hasta4Hz y cuadros alrededor de cortes. Declarar huecos y límite temporal: texto que aparece entre muestras puede perderse. Afinar fronteras sólo con muestras reales adicionales, no interpolar lectura inexistente.
- Proponer controles derivados del mismo clip, conservando original: silencio sin VAD para detectar invenciones; cuadro sin texto; audio desplazado ±500ms y orden de dos eventos invertido. Registrar transformaciones. No declarar que la prueba de silencio con VAD valida música o alucinación de un modelo omni.
- Para sonido conjunto futuro, la respuesta debe cambiar de forma correcta ante desfase/inversión, y abstenerse ante silencio o señal ausente. Audio leído por un ASR más una imagen fija no satisface ese control. Estos derivados no se generaron todavía.

## Métricas predefinidas y criterios propuestos

Los siguientes son **umbrales de este piloto**, no resultados medidos ni estándares universales.

| Dimensión | Medición | Criterio o salida |
|---|---|---|
| Citas/transcripción | WER y CER frente a referencia, sustituciones/omisiones/inserciones, cifras/nombres/negaciones por separado;10citas con literalidad y fuente. | Cero citas inventadas. No presentar como literal una cita dudosa. WER≤15% en tramo hablado limpio y ninguna regresión atribuible a OCR; errores críticos requieren corrección explícita. |
| Fronteras de palabra | Error absoluto mediano/p95 y porcentaje de palabras sin tiempo; comparar inicio y fin sin forzar correspondencias. | Objetivo p95≤250ms en las citas seleccionadas. Si no pasa, tiempos aproximados; no vender precisión fina. |
| Texto en pantalla | CER, exactitud de líneas, precisión/recall de aparición, omisiones; ñ/tildes/cifras; error temporal de entrada/salida. | CER≤10% y recall≥90% en texto legible de referencia; mejora relativa≥20% frente a lectura base o ahorro humano documentado sin pérdida. Informar todo texto excluido por tamaño/oclusiones. |
| Cortes/transiciones | Matching uno a uno con tolerancia±2cuadros en PTS; precisión, recall, F1; falsos cortes por flash/paneo. Transiciones graduales evaluadas aparte. | F1≥0,90 para cortes duros. Si falla, justificar PySceneDetect; no ajustar sobre el tramo reservado. |
| Hablantes | Si hubiera candidato posterior: DER, confusión, falsos cambios, collar250ms y solape reportado separado. | En este piloto no hay diarizador: no evaluado automáticamente. Nombres sólo por contexto/fuente autorizada, nunca por biometría inferida. |
| Eventos sonoros | Tabla humana voz/música/efecto, inicio/fin y duda; comparar detecciones acústicas propuestas con precisión/recall y error de frontera. | FFmpeg mide señal; no acreditarle detección semántica. Lo no reconocido queda pendiente. No deducir tono o música del ASR. |
| Sincronización | Error de correspondencia de eventos conocidos, offset estimado y respuesta a±500ms/inversión. | Instrumental sin deriva acumulada>1cuadro en los puntos medidos. Comprensión semántica conjunta no aprobada si sólo coinciden PTS. |
| Recursos y revisión | Wall time, CPU-segundos, RSS máximo del árbol propio, memoria disponible mínima muestreada, disco, descarga, tiempo humano y fallos por variante. | Mantener límites abajo; no declarar rendimiento basándose en tamaños de pesos. Reportar arranque frío y una repetición caliente, sin ocultar carga/preparación. |

Una abstención correcta reduce afirmaciones falsas, pero no aumenta el porcentaje de cobertura de una capacidad ausente. Publicar por atributo: aprobado en este clip / parcial / fallido / no evaluado. El éxito OCR no cierra sonido, prosodia ni comprensión AV.

## Recursos, instalación futura y autorizaciones

Antes de iniciar: confirmar clip/permiso, sí de Sergio, cuota vigente y ausencia de otros trabajos multimedia pesados. Mantener libres al menos6GiB de RAM observada. Un único trabajo, máximo2CPU/hilos, batch1, sin GPU, Docker, sudo, servicios ni cambios al venv ASR. Venv OCR nuevo bajo `~/operacion/` en VPS, sin reutilizar el perfil de navegador o cuentas.

Candidatos de entorno: PaddleOCR3.7.0, PaddleX3.7.2 y PaddlePaddle CPU3.3.1, sujetos a resolución de compatibilidad y wheel Linux/Python3.12 antes de instalar. Debe respetar NumPy<2.4 en ese entorno y la variante OpenCV exigida, sin instalar dos distribuidores del namespace `cv2`. No `[all]`, API, demo web o modelo VLM. El lock completo todavía falta: si las dependencias/avisos no cierran, no instalar. Elegir rutas/modelos explícitos y bloquear descargas automáticas durante inferencia una vez preparado lo autorizado.

Pesos candidatos fijados por revisión y SHA256 en [metadata](pesos-metadata.json): `PP-OCRv5_mobile_det` y `latin_PP-OCRv5_mobile_rec`. No tomar automáticamente “latest”. La metadata no es verificación del archivo descargado: el futuro preflight cotejará bytes/hash y avisos.

Presupuesto propuesto: **3GiB RSS total del árbol propio**,2CPU,20min wall del piloto,1GiB máximo de descargas y2GiB nuevos de disco. Supervisor y límites se verifican primero con un control propio pequeño cuando haya autorización; no se afirma que estén implementados ahora. Si se cruza presupuesto o MemAvailable baja de6GiB, terminar sólo procesos propios y conservar evidencia, sin borrar archivos. Si un límite impide evaluar, resultado técnico inconcluso; no relajar límites automáticamente ni tocar producción.

Entregables posteriores: manifiesto saneado, referencia autorizada, `metricas.json`, tabla de errores por atributo, cobertura/PTS, mediciones y veredicto independiente. Publicar en GitHub sólo material redistribuible; originales/credenciales quedan privados. Revisión por una sesión distinta y aceptación sólo después de cotejar evidencia. Nada queda programado para ejecutarse al terminar esta lectura.

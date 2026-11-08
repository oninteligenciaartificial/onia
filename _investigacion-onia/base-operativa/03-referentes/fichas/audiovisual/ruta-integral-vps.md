# Ruta audiovisual en VPS: decisión acotada

## Evaluación independiente del lote retenido · una pasada congelada

5/11, después de liberación y recepción de salidas por Jefa. **Gate correcto en este lote; semántica temporal no aceptable.** Sin inferencia nueva, tuning ni modificación de criterios. El estado anterior «retenido/no entregado» queda como antecedente de preparación, superado por esta ejecución autorizada por Jefa.

Resultado leído: `operacion/referentes-20261105/video/lote-retenido-01/resultados-desarrollo/resultados-consolidados.json`, SHA256 comprobado `1cf68298e67ce6ff4a4128a49274c647bb2a795044ecc06b7dfe2f8e890926f3`. Script congelado recotejado `14bafc413b3de16958a876002b53f2711a5e1ee108ca3cbd01d6a458fc4a5486`; contrato `11d812c4…a9887a` aceptado previamente por Jefa según delegación, sin atribuir aquí recálculo del contrato. Las ocho salidas indican checkpoint `271b9f4409ebbceaa0d5fe5319069a3a56e269ab0b868616d7e23f5145cc0ce2`. Se recotejaron ocho WAV mediante hash y decodificación FFmpeg:8/8 coinciden con verdad, frecuencia32kHz, rango completo[0,N), número exacto de muestras no nulas y ruta. Evidencia de cotejo sin duplicar verdad en `privado/cotejo-ejecucion.json`. Las ocho ejecuciones terminaron código0; warnings de claves de config en las seis captions no se ocultan ni se interpretan como fallo de ejecución. No se infiere memoria pico desde el último valor Docker del supervisor.

IDs abreviados sólo para tabla; archivos y resultados conservan UUID completo. Tiempos son verdad del control, **no localizaciones predichas**.

| ID | Esperado por intervalos | Literal relevante | Decisión por alcance |
|---|---|---|---|
| `2b22e23a` | Ceros0–4s | `exact_digital_zero`; `sin se?al digital`; caption null | Correcto: cero físico y ruta sin inferencia. La codificación textual defectuosa se conserva. |
| `f440c05e` | Ceros0–2s | `exact_digital_zero`; `sin se?al digital`; caption null | Correcto: mismo alcance. No demuestra silencio perceptual general. |
| `56ea57eb` | Tono sostenido0–5s | “a sine wave is playing” | Rasgo tonal correcto, sin fuente física específica inventada. Continuidad/duración no explicitadas: no demostradas. No prueba música. |
| `24d1a45b` | Cero0–1s; tono muy débil1–5s; cero5–6s | “a sine wave is being played” | Señal débil preservada (pico8/32768) y rasgo tonal correcto; omite pausas/límites, no valida máscara temporal. |
| `a7309bd6` | Ruido continuo0–5s | “white noise is present” | Categoría compatible con ruido pseudoaleatorio; continuidad no explicitada. No inventa máquina, ambiente u origen físico. |
| `b3cee378` | Cuatro pulsos:0,8/2,1/3,4/4,7s, cada uno60ms | “a light clicking sound followed by a click” | Identifica clicks sucesivos/intermitencia gruesa; no demuestra cuatro pulsos ni sus tiempos. No adjudica fuente física. |
| `f137e341` | Voz sintética0,5–3,549s; pulsos6,2/7/7,8s | “a man is speaking” | Habla reconocida, pulsos omitidos; orden no demostrado. “man” atribución no respaldada: la fuente es TTS Zira, no un hombre acreditado. Falla semántica completa del caso. |
| `7b132793` | Pulsos0,5/1,25/2s; voz sintética débil3,25–6,299s | “a man speaking followed by a click” | Habla débil y clicks reconocibles como categorías, pero **invierte el orden real** y añade atribución no respaldada. Falla orden y precisión del caso. |

**Conteos por atributo, sin mezclar gate y caption:**

- Integridad/rango/ruta8/8; ceros completos2/2. Conservación de no-cero6/6, incluidos tono débil y voz débil2/2; se verifica entrega íntegra al modelo, no comprensión. No se evaluó un gate temporal dentro de archivos mixtos: el contrato enruta el archivo completo.
- Presencia de categoría gruesa reconocible6/6: tono2,ruido1,clicks1,habla2. Esto **no equivale a seis casos semánticos aprobados**: inventario completo de categorías5/6 (el caso voz→pulsos omite pulsos), ausencia de atribución física específica no respaldada4/6 (ambas voces añaden “man”). No hay abstenciones que contar como acierto.
- Continuidad/intermitencia explícita: sólo1/4 controles no vocales aporta sucesión de clicks; en3/4 no se demuestra la continuidad/pausas requerida. Conteo y tiempos exactos de pulsos no demostrados. Orden de categorías voz/pulsos:0/2 aceptados, uno invertido y otro omitido/no demostrado. No se suaviza el criterio por reconocer parcialmente las categorías.

**Uso parcial que la evidencia permite proponer a Jefa:** detector de ceros exactos y conservación de señal en el dominio PCM16/32kHz de este lote; captions candidatas de rasgos tonales/ruido/clicks en estos sintéticos, sin garantía de continuidad, orden, fuente o generalización. El atributo semántico temporal queda rechazado; no aceptar el sistema para análisis integral ni aplicarlo automáticamente al corpus por esos aciertos. CoNeTTE raw sigue rechazado, y este pipeline distinto tampoco supera todos los criterios. Música, emoción/prosodia, mezcla, sincronía y material real no fueron probados. Jefa decide aceptación parcial; se cierra esta evaluación única sin nuevas rondas, modelos o ajustes con la verdad ya revelada.

## Consulta documental SenseVoiceSmall · componente parcial, no ejecutado

**Sí como candidato técnico de etiquetado acústico limitado; no como capacidad aceptada ni sustituto de Whisper/captioner integral.** Sólo se leyó documentación/código/metadata oficiales. Sin pesos descargados, instalación, exportación, inferencia, VPS o modificación del pipeline/lote retenido.

Modelo: [FunAudioLLM/SenseVoiceSmall](https://huggingface.co/FunAudioLLM/SenseVoiceSmall), revisión `3847d57b6bdf2dd8875cb1508d2af43d80a16bf7`. Metadata publica `model.pt` de936.291.369bytes: tamaño de almacenamiento, **no RAM medida**. El [README oficial](https://github.com/FunAudioLLM/SenseVoice) distingue el trabajo general de más de50lenguas del checkpoint liberado: ASR/LID de mandarín,cantonés,inglés,japonés,coreano. `nospeech` es una opción técnica, no una sexta lengua; **español no acreditado**. No extrapolar eficacia de emoción/eventos a voz española sin controles propios. El benchmark promocional de latencia tampoco acredita rendimiento del VPS.

**Licencia:** [código SenseVoice MIT](https://github.com/FunAudioLLM/SenseVoice/blob/main/LICENSE); el wrapper ONNX también declara MIT. La ficha de pesos enlaza [FunASR Model Open Source License Agreement1.1](https://github.com/modelscope/FunASR/blob/main/MODEL_LICENSE), no MIT/Apache: permite uso/copia/modificación/compartición, exige atribución y conservar nombre; incluye redacción de referencia/aprendizaje, restricciones de conducta y actualizaciones automáticas. No hay aprobación comercial automática por la licencia del código. Jefa debe resolver esos términos del peso para adopción en marca; no se afirma aquí prohibición comercial categórica ni licencia OSI del checkpoint. Copia leída con SHA256 `7dba975a2069691db4992b0592d70828b330d2f8a30a71450f4e152a554e84f8`.

**CPU real en fuente:** el [wrapper oficial FunASR ONNX](https://github.com/modelscope/FunASR/blob/main/runtime/python/onnxruntime/funasr_onnx/sensevoice_bin.py) acepta `device_id=-1`, batch1, hilos configurables; [`OrtInferSession`](https://github.com/modelscope/FunASR/blob/main/runtime/python/onnxruntime/funasr_onnx/utils/utils.py) añade `CPUExecutionProvider` y con `-1` no selecciona CUDA. Ruta técnicamente válida sin acelerador. Atención: si no encuentra `model.onnx`/`model_quant.onnx`, intenta exportar con FunASR; el snapshot HF consultado no incluye esos ONNX. No presentar el constructor como inferencia ligera ya lista: la exportación y su picoRAM son otra etapa, sin medición aquí. No activar descargas/exportación implícitas en producción. Factibilidad con reserva host6GiB **condicionada** a artefacto ONNX preparado de revisión fijada y ensayo posterior con batch1/1hilo/ventana≤10s, tarea≤3GiB; ese límite es corte propuesto, no evidencia de que cabe.

**Qué devuelve y granularidad:** CTC no autorregresivo produce texto con tokens. El [postprocesado oficial](https://github.com/modelscope/FunASR/blob/main/funasr/utils/postprocess_utils.py) reconoce `Speech,BGM,Applause,Laughter,Cry,Sneeze,Cough` y también maneja `Breath,Sing,Speech_Noise,Event_UNK`; que exista token no demuestra sensibilidad/calibración de cada clase. Emociones manejadas: neutral,feliz,triste,enojado,temeroso,disgustado,sorprendido/desconocido. Son **predicciones de clase**, no hechos psicológicos ni prosodia completa. ONNX colapsa repeticiones CTC, retira blanco y devuelve una cadena por entrada; no devuelve intervalos temporales de eventos en esa ruta. Etiquetas pueden coexistir con texto, pero no constituyen una pista temporal densa. El formato enriquecido agrupa/reduce etiquetas y convierte algunas en emojis: guardar siempre salida raw antes de él. Ventanas externas sólo darían localización con resolución de ventana, no onset/offset verificados; diarización requiere componentes distintos.

**Controles necesarios si Jefa asigna otro ensayo separado:** primero raw de ceros, tono continuo,ruido y señal débil no vocal, sin VAD que elimine eventos; cero afirmaciones específicas falsas. Después positivos conocidos de risa/tos/aplausos y voz inglesa, aislados y permutados: exigir clases pertinentes por ventana y no inventar BGM/voz en negativos. Tonos no prueban música. Emoción necesita ejemplos con verdad anotada independiente y contrastes; una voz TTS neutra sola no valida feliz/triste ni emoción en español. Desconocido/abstención no cuenta como reconocimiento. Publicar confusiones/omisiones por clase; no aceptar la etiqueta máxima como certeza. No reutilizar ni revelar verdad del lote CoNeTTE para tuning de este módulo.

Evidencia auxiliar documental: `operacion/referentes-20261105/video/percepcion-abierta/sensevoice-documental/` con revisión, lista/tamaño, acuerdo, fuente ORT y postprocesado. **Siguiente decisión de Jefa:** revisar términos de pesos y coste de preparación ONNX antes de autorizar cualquier descarga/ensayo; mantener esta candidata fuera del sistema congelado. No resuelve por sí sola ritmo visual, mezcla, sincronía ni interpretación acústica integral.

## Lote retenido independiente · preparado, no entregado al ejecutor

Por encargo de Jefa para el **sistema nuevo**, se prepararon8 WAV sintéticos propios,46s totales,2.944.352bytes. Inputs locales: `operacion/referentes-20261105/video/lote-retenido-01/inputs/`; sólo WAV con nombres UUID opacos, orden aleatorizado y sin tags de categorías. Manifiesto técnico sin verdad: `lote-retenido-01/manifest-inputs.json`. SHA256 del lote `e1466b9ed9b7b51c234ae53f552ac188dc395a3023fc9409bd615b25d377d5a0` (JSON canónico de filas técnicas ordenadas por nombre/clave, UTF8 compacto; cada fila contiene hash del WAV).

**Sólo Jefa/evaluador:** verdad por archivo/intervalo en `operacion/referentes-20261105/video/lote-retenido-01/privado/verdad-retenida.json`. No entregar esa carpeta, generador, frase ni asociaciones nombre/categoría a Desarrollo antes de su salida. Usada voz nueva de Microsoft Zira Desktop en-US mediante System.Speech ya instalado; sin dependencias/modelos nuevos. Límites de este lote: no valida música, emoción/prosodia comunicativa, mezcla ni sincronía integral.

Generación PCM16 con biblioteca estándar Python; lectura independiente FFmpeg/ffprobe8.1.1 cotejó32kHz mono, duración de cada archivo, ausencia de tags, igualdad de muestras decodificadas, hashes e intervalos cero/no-cero incluidos positivos débiles. La verdad registra extremos no nulos reales y pausas. Criterios fijados antes de inferir: ceros correctos; no omitir no-ceros débiles; continuidad/intermitencia y orden de voz/pulsos; sin fuente física inventada; abstención no cuenta como reconocimiento. Rasgos tonales no acreditan música ni origen físico.

**Retenido:** no recibido aún freeze/hash del script de Desarrollo; no se enviaron inputs al VPS/terceros ni al área ejecutora. Jefa coordina una sola ejecución después de cotejar freeze. La evaluación se hará contra la verdad privada sin tuning ni repetir este lote como validación independiente. CoNeTTE raw conserva su rechazo; preparar este lote no acepta el sistema nuevo ni el goal.

## Transferencia propuesta: inventario privado, sin envío

**Procedencia Heras YouTube resuelta:** metadata local `video/heras/youtube-candidata.json` identifica `GbavuA_jqmw` y `https://www.youtube.com/watch?v=GbavuA_jqmw`; [ficha](heras-candidata.md) enlaza ese MP4 y hash exactos. Recotejado localmente:77.732.568 bytes, SHA256 `658f6541f14efdc5f1aff07aa692f9c0761807f97e0018111e8cf034d0e69c05`. Manifiesto privado actualizado sólo en procedencia/resumen: cero fuentes pendientes. No es la VSL V1/V2 ni la clase histórica `pLH3avh7kY4`; no se infirió por título. Sin modificar selección/hash, descargar o transferir. Las menciones anteriores de fuente pendiente quedan superadas por este cotejo.

Se preparó `operacion/referentes-20261105/video/transferencia-propuesta/manifiesto-privado.json`, subordinado a `inventario-vigente-40.json`:40/40 originales presentes,2.938.504.534 bytes; Cormac separado1 archivo,10.749.782 bytes. Total41 archivos,2.949.254.316 bytes (2,75GiB);41/41 SHA256 recalculados coinciden con los existentes. Sin originales faltantes, nueva descarga, copia o transferencia. Las ocho imágenes ya estudiadas no se incluyen: no son necesarias para las pruebas temporales/acústicas; tampoco WAV derivados, modelos, entornos ni datos de clientes.

Lotes secuenciales de originales: L01=31 archivos/2.097.828.969 bytes;L02=9/840.675.565;L03=Cormac1/10.749.782. Propuesta destino `/opt/onia-referentes-media/<ID-de-transferencia>/<nombre>`; no creado. Máximo compartido10GiB: hasta2GiB originales+2GiB derivados+6GiB reservados a otro trabajo; comprobar ocupación antes de cada lote y no acumularlos. Retirar lotes requiere política de retención autorizada, no se ejecutó borrado. Manifiesto contiene rutas privadas, ID, grupo, tamaño, hash esperado/actual, fuente y destino por archivo; procedencias no resueltas se señalan expresamente para revisión central, sin asumir carácter público/privado.

La revisión automática rechazó transferir `pedro-fragmento-01.wav` por posible medio privado sin autorización explícita de archivo/destino. No se reintentó ni eludió el rechazo. **Jefa decide la solicitud central de autorización**, usando el manifiesto completo y separando Cormac; una URL pública o hash válido no concede permiso de transferencia. Esta preparación no afirma autorización ni aceptación de análisis integral.

**Actualización semántica acústica:** Jefa comunicó que CoNeTTE atribuyó un motor al silencio digital en la prueba de Desarrollo: configuración rechazada, no aplicar al corpus. La propuesta anterior queda superada por ese resultado. Una búsqueda remota adicional de MERaLiON terminó sin inferencia acreditada por trazabilidad del backend y acceso API; detalle al final. Instrumental no completa percepción.

5/11/2026 · Video. **Hay una ruta CPU para controles instrumentales parciales; no se acreditó todavía una ruta abierta de percepción integral.** No se operó el VPS, instaló software, descargó pesos ni envió corpus a terceros. Desarrollo conserva operación técnica del servidor y su ASR. No se repitieron los negativos de [Smol/VideoLLaMA3](percepcion-temporal-abierta.md), Qwen2.5-7B, MiDasheng, Eureka ni MiniCPM-o.

Presupuesto comunicado por Jefa: 4 CPU lógicas,15 GiB RAM total/10 disponibles,79 GiB disco libre, producción activa y sin acelerador acreditado. Reserva mínima del host:6 GiB. Esto deja inicialmente **hasta4 GiB de RAM disponible para trabajo adicional**, no9; debe recalcularse al ejecutar. No se infiere memoria desde tamaño de pesos.

## Dos rutas contrastadas

| Ruta | Evidencia primaria y límite decisivo | Decisión |
|---|---|---|
| Qwen2.5-Omni-3B GGUF con llama.cpp CPU | La [ficha de ggml-org](https://huggingface.co/ggml-org/Qwen2.5-Omni-3B-GGUF) declara audio/imagen/texto, **no video**. Los [pesos originales](https://huggingface.co/Qwen/Qwen2.5-Omni-3B) usan [Qwen Research License](https://huggingface.co/Qwen/Qwen2.5-Omni-3B/raw/main/LICENSE): evaluación/investigación no comercial; comercial requiere licencia adicional. El [runtime mtmd](https://github.com/ggml-org/llama.cpp/blob/master/tools/mtmd/README.md) separa modelo/proyector; soporte genérico multimodal no prueba soporte audiovisual sincronizado de este checkpoint. La conversión pequeña no rehabilita el 7B que falló silencio. | Descartada para adoptar como solución abierta del producto comercial en este encargo. No prueba nueva, pin de instalación ni presupuesto RAM: la barrera de licencia y modalidad precede a instalar. No se universaliza a otras versiones/familias. |
| Ruta modular instrumental: FFmpeg n8.0 + OpenCV4.12.0 CPU + librosa0.11.0 | Sin pesos. Se inspeccionó [silencedetect](https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavfilter/af_silencedetect.c): compara amplitud/duración y guarda PTS; [scdet](https://github.com/FFmpeg/FFmpeg/blob/n8.0/libavfilter/vf_scdet.c): diferencias entre cuadros, conserva cuadro previo. LGPL2.1+ en esos archivos; licencia final del binario depende de build, no asumirla. [Farneback](https://github.com/opencv/opencv/blob/4.12.0/modules/video/src/optflowgf.cpp) contiene implementación CPU con matrices; OpenCL es opcional. [OpenCV](https://github.com/opencv/opencv/blob/4.12.0/LICENSE) Apache2.0 con avisos BSD del archivo. [YIN](https://librosa.org/doc/0.11.0/generated/librosa.yin.html) estima F0 por autocorrelación; librosa [ISC](https://github.com/librosa/librosa/blob/0.11.0/LICENSE.md). | Compatible documentalmente con CPU, sin CUDA/servicio/modelo. Elegida para **control sintético primero**, no acreditada aún en este VPS ni como percepción integral. Revisiones fijadas por tags; Desarrollo debe guardar commit/hash real y build antes de usar. |

No se eligió demo remota nueva: no se acreditó una que aporte estas capacidades con pesos abiertos, acceso anónimo y términos aptos; no se realizaron cargas o inferencias remotas. Esto no afirma que ninguna exista.

## Qué puede aportar la ruta elegida

| Atributo faltante | Medición propuesta | Límite que permanece |
|---|---|---|
| Orden/movimiento | Decodificar todos los cuadros/PTS de A/B, máscara de figura y flujo Farneback entre cuadros consecutivos. | Flujo no comprende intención, naturalidad ni comodidad de lectura. Cortes deben excluirse del flujo. |
| Ritmo | Tiempo entre cortes/entradas, distribución de duraciones, envolvente/onsets. | Densidad de cambios no equivale a ritmo percibido o calidad narrativa. |
| Sonido/prosodia | RMS, pausas y F0 en regiones sonoras; YIN sin máscara produce tonos incluso en entradas no vocales. | No etiqueta confiablemente voz/música/SFX ni emoción/énfasis comunicativo; no es escucha. |
| Mezcla | Niveles y coincidencia de componentes conocidos en controles. | En mezcla real no separada, un nivel global no da balance voz/música ni inteligibilidad. |
| Sincronía | PTS de destello y ataque acústico con desplazamiento conocido. | No demuestra sincronía labial ni relación semántica voz/imagen. |

## Control ejecutable a asignar a Desarrollo después del ASR

Preflight aislado: consultar `ffmpeg -version`, `ffmpeg -buildconf`, disponibilidad de filtros, arquitectura y versiones Python/OpenCV/librosa. Reutilizar binario compatible sin actualizar producción. Si faltan dependencias, preparar entorno propio y cotejar wheel/arquitectura antes de instalar; esta investigación no afirma que estén instaladas. Usar un trabajador,1 CPU,320×180/24 FPS,16 kHz mono,≤10s por control. Cgroup de tarea: memoria máxima3 GiB,swap adicional0,CPU100%,timeout120s; reservar host≥6GiB y abortar también por RAM disponible inferior a6GiB. Si Desarrollo no puede imponer/monitorizar esos límites, no iniciar. Límite3GiB es **presupuesto de corte**, no consumo medido. No guardar todos los cuadros/flujo en memoria.

Primera comprobación sin archivos ni modelos, dentro de esos límites:

```sh
timeout 30s ffmpeg -nostdin -hide_banner -threads 1 -filter_threads 1 \
  -f lavfi -i 'anullsrc=r=16000:cl=mono' -t 4 \
  -af 'silencedetect=noise=-60dB:d=0.1' -f null -
```

Debe marcar el intervalo silencioso completo con tolerancia de0,1s; no produce etiquetas de cantante/música. Después, una sola tanda de controles:

1. **Audio:** silencio, tono440Hz, escalón440→880Hz, pulsos a1/2/3s y dos componentes con ganancias conocidas. F0 con `librosa.yin(...,sr=16000,fmin=80,fmax=1000,frame_length=1024,hop_length=160,center=False)` sólo donde RMS supera umbral. Exigir silencio sin F0 reportado; tonos±2%, ataques±20ms y cambio de nivel±1dB fuera de bordes. No llamar voz o música al tono.
2. **A/B existentes:** todos168 cuadros por archivo; `cv2.setNumThreads(1)`, OpenCL deshabilitado; `cv2.calcOpticalFlowFarneback(prev,gray,None,0.5,3,15,3,5,1.2,0)`. Máscara y centroides como verdad geométrica independiente; exigir orden de las cuatro figuras correcto y signo horizontal opuesto del amarillo en≥90% de pares interiores con desplazamiento. Excluir entradas/salidas y cortes; publicar cuántos pares se evaluaron, no máximo aislado.
3. **Sincronía:** secuencia nueva de10s con destellos y pulsos en PTS conocidos, una copia sincronizada y otra con audio+250ms, sin corpus privado. Exigir recuperar cero y+250ms dentro de±un cuadro (41,7ms a24FPS); conservar timestamps originales, sin reiniciar relojes por ventana. Cero música/voz no significa capacidad para analizar mezcla narrativa.

Entregable de Desarrollo: comando/build/hash, verdad de controles, mediciones por atributo, errores y pico RSS/RAM libre/tiempo. **Sólo los atributos que pasen** pueden incorporarse como evidencia instrumental. Si pasan, Jefa decide cómo cubrir el juicio perceptual y semántico restante; no autoriza automáticamente procesar40medios ni39audios. Si fallan, registrar el filtro/umbral/decodificador concreto y parar esa tanda. El siguiente paso ejecutable es este control acotado, no otra descarga de un omni ni una declaración de imposibilidad universal.

## Búsqueda adicional: semántica acústica, dos opciones nuevas

Consulta del5/11, sin instalación, pesos descargados, inferencia o corpus enviado. Los rechazos previos siguen vigentes. Se descargó únicamente el fuente CoNeTTE0.3.1 (143.693 bytes) para inspección estática, sin ejecutar setup. Auxiliares: `operacion/referentes-20261105/video/percepcion-abierta/semantica/` (metadata, configuración, fuente y app).

| Candidata | Modalidad, licencia y código decisivo | Estado CPU/recursos y decisión |
|---|---|---|
| **CoNeTTE, seleccionada para control** | Caption libre de eventos acústicos, no ASR. [Código MIT](https://github.com/Labbeti/conette-audio-captioning/blob/main/LICENSE); [checkpoint MIT declarado por autor](https://huggingface.co/Labbeti/conette), revisión `f7c6d0338832ee22df1e7c9d579cf5911a1a115d`. [Modelo](https://github.com/Labbeti/conette-audio-captioning/blob/main/src/conette/huggingface/model.py) permite `device='cpu'`, eval y desactivar gradientes; [preprocesador](https://github.com/Labbeti/conette-audio-captioning/blob/main/src/conette/huggingface/preprocessor.py) consume waveform, resamplea32kHz, promedia canales y construye ConvNeXt con `pretrained=False`: no necesita otro checkpoint del encoder al cargar el completo. | [Demo del autor](https://huggingface.co/spaces/Labbeti/conette) observada RUNNING/cpu-basic/READY; su [app fijada](https://huggingface.co/spaces/Labbeti/conette/blob/a485a9ddd7d8500430cf771da4b31f21a4297cde/app.py) carga explícitamente CPU. Prueba de despliegue declarado, **no inferencia ni RAM medida**. Bin publicado202.634.582 bytes; no convertirlo en estimación RAM. Plausible bajo control≤3GiB, sin garantía de caber. |
| **Pengi, reserva documental** | [Código MIT](https://github.com/microsoft/Pengi/blob/main/LICENSE); pesos del [registro oficial Zenodo8387083](https://zenodo.org/records/8387083) con licencia **CC BY4.0** confirmada en API, exige atribución. [wrapper.py](https://github.com/microsoft/Pengi/blob/main/wrapper.py): `use_cuda=False`, carga en CPU y genera lenguaje a partir de audio+prompt. Hay ruta semántica auténtica. | Pesos base2,4GB/no-text-encoder1,7GB publicados, sin prueba de picoRAM disponible. Construye modelo y luego carga state_dict completo; no acreditado dentro del presupuesto3GiB. Repite clips cortos y recorta aleatoriamente los largos al preprocesar, perjudicando orden/cobertura. No se propone descargarlo antes de medir la candidata seleccionada; tampoco se lo rechaza universalmente. |

### Compatibilidad exacta de CoNeTTE y barrera remota

La demo fija `conette==0.3.1`. Se verificó el sdist de PyPI, SHA256 `dd6b934b8ca67502f90ee424abdc4e7f9e431778983c36cccbb09d351a4f0632`. Sus requisitos incluyen Python≥3.10,torch1.13.1/torchaudio0.13.1,Transformers4.30.2,Lightning1.9.5,spaCy3.7.2; **no reutilizar ni degradar el venv ASR**. Proponer Python3.10 aislado, wheels CPU compatibles con arquitectura real y NumPy1.26.4; resolver antes de instalar y guardar lock. Si no hay intérprete/wheels compatibles, es barrera concreta, no invitación a compilar un stack gigante.

El `setup_other_models` del fuente intenta descargar spaCy `en_core_web_sm`, stopwordsNLTK y mappingAudioSet; hay que preparar esas dependencias en caché propia con hashes y luego usar `offline=True`. No confundirlas con entrenamiento/datasets. La carga también contiene estado serializado con pickle: usar únicamente checkpoint oficial fijado en proceso aislado. No se ejecutó aquí. El autor documenta entrenamiento1–30s: usar4s por control, batch1. Su configuración fija mínimo3/máximo20 palabras y beam3: **puede inventar contenido en silencio**; no cambiar mínimos ni filtrar silencio para ocultar ese fallo.

La interfaz remota es **Streamlit**, no Gradio. Código carga modelo abierto directamente, pero GET `/info` y `/config` devolvieron404; no existe endpoint Gradio acreditado que pueda llamarse como las demos anteriores. No se subió audio ni se simuló inferencia. El estadoRUNNING no acredita que upload/inferencia anónima funcionen. La vía recomendada es control local delegado; la interfaz pública queda alternativa sin prueba operativa.

### Control mínimo propuesto a Desarrollo, antes de corpus

Después del ASR, con los límites ya definidos (1CPU,3GiB,sin swap adicional,host≥6GiB libres,120s/control), preparar sólo snapshot oficial fijado y caché auxiliar. Medir también la carga del modelo; detener si supera el límite. `snapshot` abajo es la ruta local completa a esa revisión, no descarga automática. Comando: `timeout 120s env OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 HF_HUB_OFFLINE=1 python control_conette.py`. Cuerpo esencial:

```python
import torch, json
from conette import CoNeTTEConfig, CoNeTTEModel
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
snapshot = '/ruta/aislada/conette/f7c6d0338832ee22df1e7c9d579cf5911a1a115d'
cfg = CoNeTTEConfig.from_pretrained(snapshot, local_files_only=True)
m = CoNeTTEModel.from_pretrained(snapshot, config=cfg, device='cpu',
                               offline=True, local_files_only=True).eval()
with torch.inference_mode():
    out = m(torch.zeros(1, 128000), sr=32000, task='audiocaps',
            beam_size=3, min_pred_size=3, max_pred_size=20)
print(json.dumps({'caption': out['cands'], 'task': out['tasks']}))
```

**Primero silencio digital nativo sin gate previo.** Exigir que no atribuya voz, música, animales, máquinas o eventos inexistentes; si inventa, guardar salida íntegra y rechazar esa configuración, sin pasar a corpus. Si pasa, una única tanda con WAV sintéticos conocidos de4s: tono sostenido, tres clicks separados y ruido continuo; exigir descripción compatible, diferenciar continuo/intermitente y no inventar fuente física específica. Un tono no prueba reconocimiento musical. Para voz/prosodia, sólo añadir par de voz sintética de igual texto con variación conocida de énfasis/contorno si existe generador validado; sin ese par no aceptar prosodia. No usar la etiqueta máxima de `tags` en sustitución de la caption, ni su probabilidad como confianza calibrada.

**Salida/decisión:** Jefa puede asignar esta prueba concreta a Desarrollo; no está ejecutada ni instalada. Si pasa eventos, será cobertura acústica parcial; mezcla, emoción, orden fino y sincronía audiovisual todavía requieren sus controles propios. Un caption corto por ventana no constituye escucha integral ni rehabilita Qwen/MiDasheng/Eureka. Esta adición aporta una vía semántica nueva y una barrera alternativa precisa, sin declarar completo el goal ni iniciar otra búsqueda.

## Demo remota adicional: MERaLiON · cierre sin inferencia

5/11, una sola candidata examinada: [AudioLLM Playground del autor A*STAR](https://studio.meralion.ai/playground), que admite preguntas libres sobre audio, no sólo ASR. La web enlaza [MERaLiON-3-10B](https://huggingface.co/MERaLiON/MERaLiON-3-10B), revisión pública `3d5c2f772641b1cfeba35743df3db32a07db8c48`; API metadata `gated:false` (los campos de registro presentes en la ficha no se interpretan como bloqueo efectivo). GET del código `modeling_meralion3.py` fijado devolvió200: arquitectura con encoder acústico y modelo de lenguaje. Esto verifica código publicado del modelo, **no el checkpoint cargado en el servicio remoto**.

Se leyó la [licencia pública específica](https://huggingface.co/datasets/MERaLiON/MERaLiON_Public_Licence/blob/main/MERaLiON-3-Public-Licence.pdf), SHA256 `ca413486cc0fea7507ff3aa997ddf32b453fd2cfadf5aadd165ccaf9d67239c1`. Incluye MIT y términos de componentes Whisper/Gemma/Apache, conservación de avisos y reconocimiento del uso del modelo en productos/servicios. No es una licencia exclusivamente no comercial ni una licencia MIT sin condiciones adicionales. La eventual adopción debe conservar estos términos; no se presume que la licencia del modelo establezca gratuidad o privacidad del hosting.

**Acceso observado:** playground y consola200, sin cuenta. Su bundle público `/_next/static/chunks/app/playground/page-4bcda939c82ec11f.js`, SHA256 `b5c3157465d1a17d8e37a6067c59fc065cc765c3f4e8077a4e7fbb3142b66bcf`, construye audio en base64, instrucciones editables y POST a `https://studio.meralion.ai/api/inference/chat`. GET de esa ruta devolvió405. POST de validación con cuerpo vacío `{}` —sin audio ni inferencia solicitada— devolvió400, literalmente `"code":"BAD_REQUEST"`, con campos requeridos `model`, `messages`, `stream`; `upstream_latency_ms:1`. Cuerpo completo/trace conservados en auxiliar. No prueba inferencia gratuita, checkpoint cargado ni comprensión acústica.

**Barrera precisa:** el JavaScript inspeccionado es un cliente de proxy y no expone la carga de pesos del backend ni revisión servida. La [API oficial documentada](https://studio.meralion.ai/api-console) ofrece `https://api.meralion.ai/v1/chat/completions` con Bearer/X-API-Key y registro `/keys/register`, además de cuotas `/keys/usage`. No se registró cuenta, obtuvo clave o intentó eludir autenticación. No se acreditó un endpoint de inferencia anónima documentado y asociado por código a pesos verificables. La página pública puede ser utilizable en navegador, pero eso no basta para cumplir la condición de este ensayo. No se afirma que el playground exija login ni que sea imposible usarlo.

**Resultado y consumo:** cero archivos enviados, cero inferencias y ninguna respuesta perceptual; silencio y positivos **no ejecutados**. Sólo lecturas públicas y una validación HTTP sin contenido. El servicio no informó consumo de tokens/créditos ni precio; no se promete cuota/gratuidad permanente. No hubo operación del VPS, instalación o descarga de pesos. Evidencia literal en `operacion/referentes-20261105/video/percepcion-abierta/meralion-remoto/`: páginas, código, metadata/revisión, bundle, licencia, `access-results.json` y `empty-post.json`.

**Condición para integración, responsable Jefa:** primero obtener evidencia del autor de la revisión realmente servida y del acceso anónimo gratuito aplicable al endpoint. Si eso se acredita, control sintético de silencio sin gate; sólo si pasa, positivos mínimos conocidos. Cualquier uso del corpus fuera del VPS requiere otra autorización explícita y condiciones de datos del servicio. Sin esa evidencia no se propone a Sergio esta demo como solución operativa ni se amplía a otras candidatas en cascada. CoNeTTE y los negativos anteriores permanecen rechazados; el goal integral sigue sin aceptación.

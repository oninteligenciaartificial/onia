# REF-AUDIO-20261105 · cierre técnico para Video y Jefa

## Estado vigente · decisión open source

**Cormac en VPS:** un reel real de 37,754 s procesado con ASR-VAD; contraste automático: 154 unidades en cada salida y una sustitución respecto a otro ASR, no verificación humana. Sólo un reel, sin aceptación de escucha acústica. [Resultado y límites](vps-faster-whisper.md#reel-real-cormac--prueba-en-vps).


**ASR VPS:** faster-whisper instalado en entorno aislado; silencio sin VAD produjo texto inventado. Una configuración con VAD superó controles sintéticos y una muestra pública con límites pendientes; no acredita percepción acústica. [Evidencia](vps-faster-whisper.md).

**Demo comunitaria acotada:** el código publicado de una candidata carga Qwen3-Omni abierto, pero sólo admite transcripción con instrucción fija; no permite la consigna neutral de los controles. No se enviaron audios ni se verificó inferencia anónima. [Evidencia y límites](demo-comunitaria-20261105.md).

**Unidad de ensayo cerrada con rechazo semántico; goal integral abierto.** La tanda localizada de Eureka respondió al silencio digital inventando un cantante y música; es fallo excluyente. La ejecución propia se detuvo por instrucción de Jefa, sin completar el patrón. No se aplican etiquetas acústicas al corpus. [Resultado literal y evaluación](ruta-abierta-20261105.md#tanda-localizada-cd--rechazo-por-silencio), [salida cruda](eureka-resultados-cd.json), [recursos e interrupción](eureka-recursos-cd-interrupcion.json). Las tres matrices de cabeza/embeddings tienen SHA-256 idéntico en el checkpoint; las demás claves no usadas y la ligadura efectiva siguen sin explicación demostrada: [contraste](eureka-claves-no-usadas.md). No hay inferencia activa ni siguiente prueba autorizada por esta unidad.

Sergio pidió una ruta abierta; no exigió que su ejecución fuera exclusivamente local. Higgsfield queda fuera del objetivo actual. Se creó un entorno Python aislado y se ejecutó MiDashengLM-0.6B sobre cuatro controles reales, sin VAD. Dos instrucciones neutrales dieron fallos diferentes: una omitió la voz conocida y otra inventó voz y ruido en silencio. **No se acepta para analizar referentes en esta configuración.** [Informe, salidas brutas y recursos](ruta-abierta-20261105.md). El proceso terminó y liberó CPU/RAM; el entorno y pesos permanecen en `operacion/` ignorado. No se probó español ni Pedro.

**Dos demos remotas oficiales contrastadas:** Qwen3 y Qwen3.5 figuran `RUNNING`, pero el código visible de ambas envía a variantes Flash/Plus de la API facturable DashScope; no acredita que usen los checkpoints abiertos ni permite verificar el tratamiento interno del silencio. Sin solicitudes de inferencia ni archivos enviados. [Revisiones, evidencia y condición necesaria](demos-abiertas-20261105.md). Este resultado no demuestra que no exista otra demo.

Phi-4 ONNX fue contrastado documentalmente; no existe un paquete CPU listo en la fuente oficial y su demo consultada falló. Eureka ya fue descargado y probado como se detalla abajo. No hay ruta acústica integral aceptada ni se enviaron medios a Higgsfield.

**Primeras pruebas Eureka (históricas):** los dos pesos descargados coinciden con hashes oficiales. El constructor original exige FlashAttention 2 y reprodujo `ImportError`; una adaptación SDPA ejecutó un encoder sintético, pero el modelo completo con offload terminó en `0xC0000005` tanto en BF16 como en FP32/2 GiB CPU, sin emitir respuestas en esos intentos. Una configuración FP32/4 GiB fue detenida por el límite de RSS. La corrección posterior sí produjo respuestas, incluido el rechazo de silencio descrito arriba. No se identificó la causa del error nativo; no afirmar incompatibilidad universal. [Detalle](ruta-abierta-20261105.md), [preflight](eureka-preflight.json), [arquitectura](eureka-arquitectura.json), [preprocesado](eureka-preprocesado.json).

**Diagnóstico de seguimiento previo:** `faulthandler` reprodujo la excepción durante la primera generación, en `torch.storage.__getitem__` → `accelerate.utils.offload` → `safe_open.get_tensor`; [pila completa](eureka-faulthandler.log). Los 28 pesos pequeños de normalización se leyeron aisladamente sin error: no se demuestra corrupción ni causa raíz. `pip check` no reportó requisitos rotos; las versiones y compatibilidad real siguen separadas. Ubuntu/WSL2 y docker-desktop estaban detenidos al consultar, sin iniciarlos.

En el primer reintento correctivo, el lector BF16 con NumPy generó respuestas para tono y voz y el supervisor cortó a 900 s; en esa tanda silencio/patrón no se evaluaron. La tanda posterior, ya cerrada, produjo el rechazo de silencio indicado arriba. [Implementación](eureka_safe_loader.py), [registro anterior](eureka-loader-faulthandler.log), [resultados anteriores](eureka-resultados.json), [recursos anteriores](eureka-recursos.json).

## Corte histórico anterior

El texto siguiente conserva el estado de la primera entrega y sus dependencias tal como se registraron. Las referencias a «sin instalaciones» o a esperar autorización de Higgsfield describen ese corte y quedan sustituidas por el estado vigente anterior.

**5/11/2026 · America/Caracas. Extracción, controles, ASR y entrega terminados; escucha acústica integral no aceptada.** Skill directora: desarrollar-y-verificar. Repo al inicio: `1119f5e94b24eaa7d8448319d8b7f424612db27d`; cambios documentales ajenos preservados. Sólo se escribieron esta carpeta técnica y binarios en `operacion/referentes-20261105/audio/`. Sin commit, secretos, instalaciones, servicios, producto, publicaciones o llamadas pagas.

**Resultado recuperable.** [Reel público Pedro Dd6oC4EkRX1](https://www.instagram.com/pedrobuerbaum/reel/Dd6oC4EkRX1/) descargado sin login/cookies; decodificación completa sin errores. Ruta de medios: `C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/audio/`.

| Archivo | Evidencia |
|---|---|
| `pedro-Dd6oC4EkRX1.mp4` | 6.560.365 bytes; SHA `6b5471ae7fed930bc4193a1c4c87f72e69ecc031bf212b0f35204d3a8d54de44`; VP9 1080×1920, 90,32 s |
| `pedro-original-pcm24.wav` | Estéreo 48 kHz sin normalizar; SHA `8325d3ffddd2c2d536feac848a853a8473d7c3ef16cff53b289cddb70cd37112` |
| `pedro-asr-16k.wav` | Derivado verbal mono 16 kHz; [salida con VAD](asr-vad-resultados.json), texto automático y tiempos |
| `pedro-seleccion-12s.wav` / `.mp3` | Cinco fragmentos de 2 s y separadores silenciosos de 0,5 s; [mapa](fragmentos.json), hashes/procedencia en [manifest](manifest.json) |

AAC en contenedor: 90,325 s; PCM decodificado: 90,347958 s/4.336.702 frames. No se infiere desfase de esa diferencia. Ambas pistas comienzan en 0. MP4 y PCM nuevos difieren en hash de la representación cloud 720p; no se atribuye equivalencia de muestras. Los marcadores de capítulos son candidatos heredados, sin verificación visual nueva por Desarrollo.

**Pruebas y esperado/observado.** [8/8 controles técnicos](verificacion.json) pasan: PCM conocido, cinco fragmentos exactos, ASR/VAD de silencio y tono sin texto, frase sintética conocida reconocida, 90 s reales procesados, fallo negativo conservado y decodificación completa. No son ocho pruebas de comprensión acústica. **ASR sin VAD inventó subtítulos sobre 440 Hz**; se conserva [salida fallida](asr-resultados.json). Con VAD conserva toda la pista real y entrega 20 segmentos/241 unidades de palabra; hay términos dudosos y no es transcripción humana corregida. CPU 4/int8 con pesos existentes de 486 MB: 16,828 s para reel/20,469 s tanda VAD; sin descargar modelos, pico RAM no medido. Medidas: −14,21 LUFS/LRA 2,60 LU/true peak −0,53 dBFS; no certifican emoción o mezcla. [Método, cobertura y reproducción](README.md).

**Capacidad acústica y soluciones comprobadas.** El control nativo fue rechazado: `audio content omitted because you do not support audio input`. Qwen sigue descartado por su silencio fallido; CLAP tampoco reconoció el click de control y no acredita efectos. Las demos abiertas Phi4/Audio Flamingo mostraron error; no se instalaron modelos grandes. Higgsfield sí devuelve `scenes.audio` en trabajos existentes, pero costo/proveedor y fiabilidad acústica no están verificados. Se prepararon cuatro videos con imagen idéntica y pistas distintas para un ensayo futuro, **sin subirlos ni iniciar análisis**. [Alternativas, evidencia y límites](alternativas.md).

**QA corregida de probes, 5/11/2026.** Se reemplazaron sólo `probe-a/b/c/d.mp4` tras verificar sus rutas. Ahora los cuatro son AAC 48 kHz estéreo, objetivo128kb/s y6s, con el mismo hash de video gris anterior. [26/26 controles nuevos](qa-controles-video.json): silencio PCM exactamente cero; tono FFT440Hz; fuentes WAV y demás medios intactos; delta RMS por canal frente al PCM remuestreado menor de0,023dB. No hay normalización: mono se copia a L/R a ganancia unitaria, estéreo permanece estéreo. Sumar potencia de dos canales duplica la del mono (+3,01dB), sin subir la amplitud de cada canal. AAC es con pérdidas: bitrate efectivo y muestras pueden variar; evaluar sólo [0,6), excluyendo768 frames de relleno. Manifiestos actualizados: cuatro probes260.081bytes; paquete18 archivos/45.244.669bytes. ASR no reejecutado.

El ensayo futuro conserva tres controles conocidos y una muestra real sin verdad semántica validada. Misma instrucción neutral, orden variado y nombres anónimos; no enviar fuentes, identidad, esperados o manifiestos. «Tono continuo» basta como respuesta del analizador; no exigir440Hz. Aprobar controles no acredita prosodia, SFX, música ni sincronía fina. **La autorización externa sigue pendiente.**

**Dependencia actualizada, 5/11/2026:** Jefa v2 (`01a1ab9c-15b2-7a03-9588-2daab62a93eb`) informó que centralizó con Sergio dos preguntas async: juicio puntual de la selección de 12 s y autorización explícita para sólo cuatro pruebas Higgsfield con créditos existentes, costo/proveedor internos desconocidos y sin compra/cambio de plan. **Ambas siguen sin respuesta comunicada; no hay autorización para subir archivos ni iniciar análisis.** Desarrollo no duplica preguntas ni ejecuta esos pasos hasta recibir confirmación de Jefa. Los cuatro controles permanecen preparados localmente.

**Única siguiente acción de esta área:** incorporar la respuesta que comunique Jefa y aplicar únicamente su alcance confirmado. El juicio humano, si llega, se registra por fragmento con respuesta o ambigüedad explícita para los cinco; no se extiende a los 90 s. Una autorización de Higgsfield habilitaría sólo las cuatro pruebas indicadas, sin acreditar su resultado por anticipado. La unidad técnica queda cerrada con evidencia; escucha integral, música, prosodia, ambiente y sincronía fina no están aceptados. Visual/comercial pueden continuar en sus áreas sin esta ejecución.


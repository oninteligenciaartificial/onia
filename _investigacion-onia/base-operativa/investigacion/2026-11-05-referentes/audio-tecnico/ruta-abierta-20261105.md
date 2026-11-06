# Ruta abierta de comprensión acústica · avance

Estado vigente: **MiDashengLM y Eureka rechazados para este uso en las configuraciones ensayadas; Eureka inventó voz/música sobre silencio digital.** La unidad de ensayo está cerrada, pero el goal integral permanece abierto y no hay ruta acústica aceptada. No se ejecutó ni repitió Qwen. La sección final registra el resultado más reciente; las recomendaciones anteriores de repetir controles son históricas y no están activas.

Comprobación local: RTX 3050 Laptop 4096 MiB, 3678 MiB libres al medir; C: 55.587.127.296 bytes libres. La consulta CIM de RAM falló por acceso; la RAM libre no se pudo revalidar. Python 3.12 contiene ONNX Runtime pero no torch, transformers ni onnxruntime-genai. Estos datos no prueban imposibilidad de usar memoria compartida ni el tamaño residente efectivo de un modelo.

[Phi-4 ONNX oficial](https://huggingface.co/microsoft/Phi-4-multimodal-instruct-onnx): MIT, audio admitido; paquete GPU para CUDA/DirectML, mientras [CPU requiere conversión](https://github.com/microsoft/onnxruntime-genai/blob/main/examples/python/phi-4-multi-modal.md) y dependencias aisladas. La memoria y el comportamiento de esta máquina no están probados; no se descargó el paquete.

Alternativa menor encontrada: [MiDashengLM-0.6B](https://huggingface.co/mispeech/midashenglm-0.6b-fp32), Apache-2.0, 0,6B, entrada audio y descripción de música/voz/sonidos; la ficha muestra inglés y chino, no acredita español. Su ejemplo requiere torch/transformers y código remoto del modelo: revisar archivos, dependencias, tamaño de pesos y capacidad CPU real antes de instalar en entorno aislado. Las afirmaciones de calidad del autor no son resultados nuestros.

## Prueba ejecutada

Memoria revalidada mediante `GlobalMemoryStatusEx`: 7,44 GiB libres inicialmente, con fluctuación posterior hasta 4,53 GiB durante otros trabajos. Se instaló entorno aislado en `operacion/referentes-20261105/audio/midasheng-venv/`, sin modificar Python global; pesos en `midasheng-model/`, revisión `3969e451d1c62618089c1135fe4c58ed33af2457`, 2.748.851.080 bytes, SHA-256 `8c58a202c2c390c4130966a942e81943f78927e30616ae42e30ab7ab0470f2a3`. Código de configuración/modelo/procesador inspeccionado para dependencias y llamadas relevantes; no se afirma auditoría exhaustiva. Torch 2.15 CPU, torchaudio 2.11.1, transformers 4.57.6. Sin red durante inferencia ni VAD; cuatro hilos; decoder FP16 y encoder/proyector FP32. Supervisión: inicio ≥4,75 GiB libres; parar si disponible <1,8 GiB, RSS >3,6 GiB o duración >900 s. No se tocaron procesos ajenos.

La primera carga toda FP16 falló en Conv2d por entrada float32/pesos half; [recursos intento1](midasheng-recursos-intento1.json). Condición corregida: encoder/proyector float32. Dos pasadas completas, mismos cuatro WAV anónimos, instrucción común dentro de cada pasada. El método personalizado `generate` devuelve sólo salida; en el primer JSON `raw_full` contiene la respuesta real y `answer` quedó vacío por un error de extracción, corregido para la segunda pasada sin modificar el resultado bruto.

| Control / esperado | [Instrucción neutral 1](midasheng-resultados-instruccion1.json) | [Instrucción del autor](midasheng-resultados.json) |
|---|---|---|
| Tono constante / sonido tonal | Describe una serie de tonos; no afirma voz | Describe tonos cortos de teléfono, fuente y repetición no acreditadas |
| Voz sintética conocida / voz y siete | Dice que no hay sonidos ambientales diferenciados: omite la voz | Reconoce voz y número siete |
| Silencio digital / ausencia de sonido | Indica que no hay eventos sonoros diferenciados | **Inventa una persona hablando y ruido de fondo: fallo excluyente** |
| Silencio–tono–silencio / secuencia | Dice sirena, sin describir secuencia | Dice teléfono sonando repetidamente, sin acreditar secuencia |

[Recursos primera pasada](midasheng-recursos-instruccion1.json): RSS máximo 3,42 GiB, mínimo libre 3,30 GiB. [Segunda pasada](midasheng-recursos.json): RSS máximo 3,41 GiB, mínimo libre 3,67 GiB. Las conversiones PCM de las muestras fueron locales; no se agregó VAD ni se ocultaron negativos. No se procesó Pedro ni se probó español, música o click: el criterio exigía superar los básicos primero. No atribuir el fallo a todos los dispositivos o a la versión FP32 sin probarlos.

## Alternativas y alcance restante

[Audio Flamingo 2](https://huggingface.co/nvidia/audio-flamingo-2-0.5B) muestra etiqueta MIT, pero su propio texto restringe checkpoints a uso no comercial: no asumir licencia abierta de pesos. [Eureka Audio](https://huggingface.co/cslys1999/Eureka-Audio-Instruct) declara Apache 2.0 y entrada real; su paquete es 6,35 GB y no se descargó ni probó. Su encaje en la RAM libre actual no está demostrado; no es válido inferir residencia exacta por tamaño de archivos ni lanzar otra descarga grande a ciegas. Phi-4 sigue como alternativa CPU mediante conversión o GPU/DirectML, tampoco probada localmente. Ninguna de estas referencias es una ruta aceptada.

La unidad sigue **pendiente**: falta una ruta que pase los controles conocidos y después permita acotar español, mezcla y Pedro. Este cierre conserva resultados reales; no implica que otra sesión ya haya recibido o ejecutado el siguiente ensayo. Higgsfield sigue fuera.

## Eureka Audio · alternativa ejecutada, no aceptada

Fuente [Apache 2.0](https://huggingface.co/cslys1999/Eureka-Audio-Instruct), revisión `219761da53c9c6c5900a84a723d88ccc29db66d3`; código auxiliar oficial `Alittleegg/Eureka-Audio` commit `51dac590e0c6e3c48d8094a5b5431c7f86ff3be4`. Su ruta original fuerza FlashAttention 2; [preflight reproducido](eureka-preflight.json) devuelve ImportError por ausencia de `flash_attn`. Una copia local con SDPA ejecutó un encoder reducido sintético, y el preprocesador aceptó PCM silencio sin VAD con 75 tokens de audio; no son inferencia del modelo completo. La construcción sin pesos contó 2.752.716.294 parámetros; los encabezados de los dos archivos contienen 5,895 GiB de tensores BF16, sin atribuir esa cifra directamente a RSS.

La descarga normal del hub quedó en cero bytes y dos descargas directas en 12 KiB; HEAD HTTP 200 no acreditó transferencia. Una prueba parcial recuperó 32 MiB con HTTP 206; la descarga por rangos terminó y ambos archivos coinciden con sus hashes LFS oficiales: [archivo 1](eureka-descarga-1.json), [archivo 2](eureka-descarga-2.json). Se usó una sola alternativa nueva, sin pagos ni credenciales. Los originales y las copias locales adaptadas permanecen en `operacion/`; [diff SDPA/CPU](eureka-adaptacion-cpu.diff), [offload](eureka-offload.diff), [float32](eureka-fp32.diff). Se usó Accelerate con CPU/disco por límites de RAM; no equivale a validación del comportamiento del modelo.

| Intento | Condición y resultado | Recursos |
|---|---|---|
| BF16, offload, presupuesto CPU 4 GiB | Inicializó y terminó con **0xC0000005** antes de respuesta; sin traceback Python ni diagnóstico causal. Hubo advertencia de pesos no utilizados. | [RSS máx. 0,53 GiB; RAM libre mín. 7,43 GiB](eureka-recursos-bf16.json) |
| FP32, offload CPU 4 GiB | Supervisor detuvo el proceso por superar el límite de RSS durante carga; no fue error acústico ni OOM del sistema. | [RSS 5,53 GiB; RAM libre mín. 2,75 GiB](eureka-recursos-fp32-4g.json) |
| FP32, offload CPU 2 GiB | Inicializó y terminó con **0xC0000005** antes de respuesta; sin traceback Python. No hubo intervención sobre procesos ajenos. | [RSS máx. 2,20 GiB; RAM libre mín. 6,03 GiB](eureka-recursos.json) |

Esperado: respuestas neutrales a tono, voz conocida, silencio y patrón. Observado: **ninguna salida acústica** en los intentos del modelo completo; no se le asigna acierto ni fallo de contenido y no se ejecutaron español/mezcla/Pedro. Los controles adicionales conocidos sí quedaron preparados en [manifiesto](controles-adicionales.json), sin inferencia.

Phi-4 ONNX: la vía oficial de [DirectML](https://huggingface.co/microsoft/Phi-4-multimodal-instruct-onnx) existe, pero no hay prueba de residencia en esta GPU de 4 GiB; [CPU requiere conversión](https://github.com/microsoft/onnxruntime-genai/blob/main/examples/python/phi-4-multi-modal.md). El Space oficial mostró error de ejecución y la ruta NVIDIA gratuita figuraba deprecated; no se verificó demo pública funcional. Tamaño en disco no es consumo VRAM. Audio Flamingo 2 restringe checkpoints a uso no comercial pese a etiqueta MIT de código. MiDashengLM sí produjo respuestas, pero falló los controles según el cuadro anterior.

**Condición para continuar:** disponer de un runtime CPU/offload o un ejecutor compatible en el que Eureka no termine con acceso inválido, o una conversión CPU de Phi producida y comprobada en un entorno con recursos suficientes. El diagnóstico de `0xC0000005` requiere evidencia del fallo nativo; cambiar versión/backend es una hipótesis, no solución demostrada. En ese ejecutor repetir los cuatro controles anónimos con supervisión; sólo después de pasarlos evaluar español, click, melodía, mezcla y Pedro. La carga temporal de RAM no se presenta como incompatibilidad del equipo. No se activaron servicios ni se enviaron medios fuera del equipo.

## Diagnóstico y único reintento correctivo · 5 de noviembre

**Corte histórico:** la recomendación de ejecutar `c,d` en esta sección fue sustituida por la tanda localizada y su cierre, documentados al final.

Esta sección actualiza la condición anterior: ya se obtuvo salida parcial con el mismo modelo; no se acepta todavía. `PYTHONFAULTHANDLER=1` reprodujo el acceso inválido en la primera generación. La pila sitúa la operación en `torch.storage.UntypedStorage.__getitem__`, llamada desde `accelerate.utils.offload.OffloadedWeightsLoader.__getitem__` al ejecutar `safe_open.get_tensor`, dentro de `input_layernorm` de Qwen3. [Log completo](eureka-faulthandler.log), [recursos de esa reproducción](eureka-recursos-faulthandler.json). **Es la fase observada, no una causa raíz demostrada.**

Se comprobaron las 28 matrices pequeñas `input_layernorm.weight` directamente con `safe_open`, código 0: [script](eureka_repro_safetensors.py) y [log](eureka-repro-safetensors.log). Los SHA-256 oficiales de ambos shards coinciden. Esto no prueba que toda ruta de offload funcione ni que algún tensor concreto esté corrupto. `pip check`: sin requisitos rotos; Torch 2.15.0+cpu, torchaudio 2.11.1+cpu, torchvision 0.29.2+cpu, Transformers 4.57.6, Accelerate 1.15.0 y safetensors 0.8.0. Los metadatos instalados de torchaudio/torchvision permiten esas versiones; no prueban compatibilidad binaria integral.

La advertencia de carga enumera 17 claves sin usar: `audio_embed`, `audio_ffn_adaptor`, `audio_head`, `audio_out_projection` y `lm_head.weight`, detalladas en el log. Se comprobaron en el índice de pesos y no se encontraron las primeras cuatro familias como módulos de la clase revisada; `lm_head` sí aparece como clave ligada/de salida. No se determinó si omitirlas es inocuo ni si afecta resultados. No atribuirles el acceso inválido por inferencia.

El único reintento correctivo mantuvo los pesos y recursos, pero sustituyó la lectura de tensors BF16 del offload por copia NumPy y conversión a Torch, sin tocar paquetes instalados. Un tensor de control coincidió exactamente con el lector oficial; [código](eureka_safe_loader.py). Con esa adaptación el proceso **superó la fase donde ocurría la excepción** y entregó respuestas reales: [salidas](eureka-resultados.json), [log](eureka-loader-faulthandler.log), [recursos](eureka-recursos.json). No se prueba que esa fase no pueda fallar en otra ejecución.

| Control | Esperado / observado | Tiempo de generación |
|---|---|---:|
| Tono 440 Hz constante | Identifica un tono continuo; sugiere 1 kHz, dato incorrecto para la muestra | 436,296 s |
| Voz sintética inglesa conocida | Identifica voz y parte de la frase; respuesta truncada antes de comprobar el número siete | 434,656 s |
| Silencio digital | **Sin resultado:** el supervisor cortó por tiempo durante este control | No evaluado |
| Silencio–tono–silencio | No llegó a ejecutarse | No evaluado |

El tiempo hasta la primera respuesta desde el arranque completo no se midió por separado: fue al menos 436,296 s. La tanda terminó a 900,27 s por límite de tiempo; RSS máximo 3.063.754.752 bytes (2,85 GiB), RAM libre mínima 5.571.203.072 bytes (5,19 GiB), inicio 8.595.263.488 bytes (8,00 GiB). Se fijaron CPU cuatro hilos, pesos en CPU hasta 2 GiB más offload, mínimo inicial 7,5 GiB, reserva 2 GiB, RSS máximo 5,5 GiB y 900 s. El proceso terminó y liberó recursos. La lentitud observada en dos muestras de seis segundos hace inviable extrapolar que esta configuración procese eficientemente el corpus; no se midió una ejecución acelerada diferente.

**Condición mínima para completar esta prueba, no demostración de aceptación:** ejecutar únicamente los controles pendientes `c,d` con los mismos pesos, lector, límites de memoria y una ventana suficiente. Los dos controles observados tardaron aproximadamente 871 s juntos, más carga; usar esa duración como estimación para dos controles restantes no garantiza que terminen dentro de 900 s. No se autorizó repetir toda la tanda ni se ejecutó una nueva. El script admite `ONIA_CASES=c,d` y escribe resultados separados; conservación del prompt neutral y sin VAD. Ejemplo ejecutable, a usar sólo dentro del alcance vigente:

```powershell
$env:ONIA_CASES='c,d'
$env:TEMP='C:\dev\proyectos\_investigacion-onia\base-operativa\operacion\referentes-20261105\audio\midasheng-tmp'
$env:TMP=$env:TEMP
& 'C:\dev\proyectos\_investigacion-onia\base-operativa\operacion\referentes-20261105\audio\midasheng-venv\Scripts\python.exe' -B 'C:\dev\proyectos\_investigacion-onia\base-operativa\investigacion\2026-11-05-referentes\audio-tecnico\probar_eureka.py'
```

Después habría que resolver la advertencia de pesos y, sólo si silencio y patrón pasan, evaluar controles adicionales y Pedro. Una máquina/runtime más rápido o reparto distinto podría reducir tiempo, pero no se ha medido ni se conoce requisito mínimo. WSL2 está instalado, Ubuntu y docker-desktop estaban **Stopped**; la lista fuera del sandbox se consultó sin iniciarlos. No se verificaron paquetes o capacidad de un WSL en ejecución, ni se cambió su estado. No hay costo externo medido ni nueva descarga necesaria para la prueba localizada.

## Tanda localizada c,d · rechazo por silencio

Se ejecutó `ONIA_CASES=c,d` con los mismos pesos, revisión, adaptación SDPA/CPU, lector BF16 NumPy, instrucción neutral «Describe the audio.», CPU cuatro hilos, FP32, offload hasta 2 GiB en CPU, sin VAD y límites de 900 s/reserva 2 GiB/RSS 5,5 GiB. No se repitieron tono/voz ni se descargó otro modelo. [Salida completa](eureka-resultados-cd.json), [registro](eureka-pendientes.log).

**Silencio digital, 436,187 s: fallo excluyente.** El modelo describe a un cantante masculino interpretando un aria, con vibrato y una frase italiana, pese a que las muestras del control son cero. El texto literal completo permanece en el JSON. No se amplía a referentes, español, click o mezcla. Al recibir la orden de Jefa se interrumpió sólo la sesión propia mientras el patrón seguía en curso; no hay salida del patrón, por tanto queda **no evaluado**.

El corte fue externo al supervisor, por lo que éste no llegó a escribir su JSON final de recursos de esta tanda. [Registro de interrupción](eureka-recursos-cd-interrupcion.json): aproximadamente 595 s transcurridos en la última lectura previa; RAM libre 7,43 GiB antes y 8,02 GiB después; cero procesos propios detectados. No se dispone de RSS pico ni mínimo de RAM de esta tanda y no se extrapolan los valores de la anterior. El resultado de silencio se conservó antes de interrumpir.

**Claves no usadas:** [contraste oficial](eureka-claves-no-usadas.md). La clase coincide con configuración y ejemplo oficiales. Las tres matrices de cabeza/embeddings son idénticas byte a byte por SHA-256 completo, pero la ligadura efectiva durante offload no se ha demostrado. La función de las otras 16 claves sigue sin acreditarse. Ni este contraste ni la corrección de lectura subsanan el fallo semántico.

Unidad técnica cerrada con problema concreto; no equivale a cerrar el estudio integral ni autoriza usar las descripciones del modelo sobre el corpus. Ninguna inferencia o instalación adicional queda iniciada por este cierre.

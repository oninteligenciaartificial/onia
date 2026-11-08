# Video de Instagram: capacidad audiovisual y viabilidad CPU

6 de noviembre de 2026. Investigación documental primaria; responsable: subagente fuentes_video_ig. No se instaló software, descargaron pesos, ejecutaron modelos, conectó al VPS ni enviaron medios a servicios. ONIA-CENTRAL excluido.

## Resultado finito

**Existe una condición nueva pertinente: MiniCPM-o 4.5 tiene un runtime que implementa entrada de audio e imagen secuenciada con backend CPU para ambos encoders. No está probado que quepa ni que produzca respuestas correctas en esta PC o en el VPS.** Se identificaron dos candidatas; ninguna se declara solución operativa. No hace falta seguir acumulando modelos para decidir el siguiente control.

La extracción con FFmpeg y el ASR existente permiten recuperar medios y texto. No completan escucha de prosodia/música/SFX ni percepción temporal. Un sistema audiovisual que recibe muestras ordenadas tampoco observa automáticamente todos los cuadros: se debe declarar su muestreo y validar los atributos pedidos.

## Lecciones recuperadas antes de buscar

- [Estado técnico previo](../audio-tecnico/ESTADO.md): Qwen2.5-Omni histórico, MiDashengLM y Eureka inventaron sonido sobre silencio; ASR sin VAD también alucinó texto. No se propone repetir esas configuraciones.
- [Percepción temporal previa](../../03-referentes/fichas/audiovisual/percepcion-temporal-abierta.md): SmolVLM2-500M ejecutó en CPU pero falló orden y movimiento; VideoLLaMA3 remoto quedó parcial. Ninguno acredita audio nativo en las rutas ensayadas.
- [Ruta VPS previa](../../03-referentes/fichas/audiovisual/ruta-integral-vps.md): CoNeTTE raw alucinó motor en silencio; el sistema instrumental posterior tampoco superó orden semántico. Las métricas sirven como medidas, sin sustituir percepción.
- [MiniCPM-o 2.6 previo](../audio-tecnico/vps-arquitectura.md): no hubo ensayo; su vía llama.cpp documentada era sólo visual. La investigación de **4.5 + llama.cpp-omni** cambia versión y backend; no rehabilita 2.6 ni acredita resultados de 4.5.

## 1. MiniCPM-o 4.5 + llama.cpp-omni: candidata CPU documental

La [ficha del autor](https://huggingface.co/openbmb/MiniCPM-o-4_5) publica un modelo de 9B con entrada audiovisual y ejemplos que intercalan cuadros con segmentos de audio. Su ejemplo “Chat with Video” aislado descarta el audio; para esta tarea hay que usar el modo omni. Código y pesos se declaran Apache 2.0. No se acredita español, música, prosodia o ausencia de alucinación mediante esta lectura.

El [runtime del mantenedor](https://github.com/tc-mb/llama.cpp-omni) está enlazado por el cookbook del modelo y usa licencia MIT. Su README documenta compilación Linux CPU, módulos APM/VPM/LLM y `--no-tts` para salida textual. No es un ASR que convierta todo a subtítulos antes del LLM: el audio se inyecta mediante embeddings.

**Código inspeccionado, no ejecutado:** revisión `d30f00feadb7ebce95bacd55b0d104e3ef501481`.

- [audition.cpp](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/audition.cpp): crea `backend_cpu`; si no hay backend GPU, selecciona ese CPU.
- [vision.cpp](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/vision.cpp): el mismo fallback existe para el encoder visual.
- [omni.cpp](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/omni.cpp): inicializa audio y visión en `media_type=2`. Esto fundamenta CPU para el recorrido de entrada completo; no sólo para el LLM. No equivale a prueba de compilación o inferencia.
- [CMake del componente](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/CMakeLists.txt): target de prueba audiovisual C++17, GGML/llama/llama-common y Threads. Esta prueba directa evita instalar la demo web y sus servicios.

El [cookbook enlazado oficialmente](https://github.com/OpenSQZ/MiniCPM-V-CookBook/blob/main/demo/web_demo/WebRTC_Demo/README.md) contempla CPU-only omitiendo `-DGGML_CUDA=ON`. Su tabla de experiencia en tiempo real usa Mac/Metal o NVIDIA; no demuestra mínimo CPU x86. La ficha pide ≥28 GB VRAM para su demo PyTorch y ≥12 GB GPU o M4 Max/24 GB para streaming omni cuantizado. Esas condiciones pertenecen a esas demos, no prueban imposibilidad de inferencia CPU offline.

**Pesos exactos consultados:** [GGUF del autor](https://huggingface.co/openbmb/MiniCPM-o-4_5-gguf/tree/db25077c33951fe163b42986fba0132e279872a2), revisión `db25077c33951fe163b42986fba0132e279872a2`, Apache 2.0 declarado en ficha; no se descargaron. [Metadatos primarios con tamaños](https://huggingface.co/api/models/openbmb/MiniCPM-o-4_5-gguf?blobs=true):

| Componente sin salida TTS | Bytes en disco |
|---|---:|
| `MiniCPM-o-4_5-Q4_K_M.gguf` | 5.026.714.400 |
| `audio/MiniCPM-o-4_5-audio-F16.gguf` | 660.167.904 |
| `vision/MiniCPM-o-4_5-vision-F16.gguf` | 1.095.113.184 |
| Total de estos tres | 6.781.995.488 (~6,32 GiB) |

Faltan buffers, contexto, código y herramientas. No convertir bytes de disco en pico RAM. El README del runtime publica ~8,5 GB de memoria unificada para Q4 completo en Apple; no es un benchmark de CPU x86 ni del modo sin TTS. No se encontró una medida CPU comparable que garantice el encaje bajo la reserva del VPS.

### Comandos documentales mínimos; no ejecutados

Partiendo de un checkout de esa revisión y de pesos ya preparados en `/ruta/modelos/`, el build CPU oficial se concreta en:

```sh
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=OFF
cmake --build build --target llama-omni-single-test-omni -j2
./build/bin/llama-omni-single-test-omni -m /ruta/modelos/MiniCPM-o-4_5-Q4_K_M.gguf -ngl 0 --no-tts -c 1024 --test /ruta/control_ 1
```

`control_0000.wav` y `control_0000.jpg` deben existir: éste es un control de carga/inferencia de un par, no un análisis completo del movimiento de un video. Las opciones están en el [harness específico del autor](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/test/single_test_omni.cpp). `-j2`, contexto 1024 y desactivar CUDA/TTS son selecciones acotadas derivadas, sin rendimiento medido.

**Evitar un control falso:** `omni-cli.cpp` genérico envía el primer archivo con `index=0`, reservado a inicializar sistema; puede omitir su audio. El target específico anterior inicializa sin medios y luego usa `index>=1`. Además, no expone consigna neutral por CLI: usa un asistente conversacional. Por tanto, el comando sólo sirve como smoke técnico.

Para una evaluación semántica, preparar una copia aislada del harness con consigna neutral fija; [la API pública](https://github.com/tc-mb/llama.cpp-omni/blob/d30f00feadb7ebce95bacd55b0d104e3ef501481/tools/omni/omni.h) ofrece `stream_prefill(ctx,audio,imagen,index,max_slice_nums,text)`. Pasar el texto como sexto argumento conserva señal de audio e imagen. Fijar y revisar el diff antes del lote; no esconder silencio mediante VAD. No se implementó ese cambio en esta unidad.

## 2. VideoLLaMA2.1-7B-AV: audiovisual documentado, GPU en receta oficial

Los [pesos AV del autor](https://huggingface.co/DAMO-NLP-SG/VideoLLaMA2.1-7B-AV) declaran Apache 2.0 y audio-visual QA. No confundirlos con checkpoints visuales ni con VideoLLaMA3. La [rama audio_visual oficial](https://raw.githubusercontent.com/DAMO-NLP-SG/VideoLLaMA2/audio_visual/README.md) requiere CUDA≥11.8 y FlashAttention en su receta; no se encontró un mínimo oficial CPU/RAM útil para este VPS. Capacidad del autor, no calidad de edición/prosodia demostrada. **Sólo documental; no candidata a instalar aquí bajo estas condiciones.**

## Ejecutable aquí frente a sólo documentado

- **Disponible localmente:** `Get-Command` confirmó FFmpeg/ffprobe en `C:/Users/PC/tools/ffmpeg/bin/` y Python 3.12. `Test-Path` confirmó el MP4 de Pedro y el entorno acústico anterior. No se decodificó ni procesó otra vez; presencia no acredita un ensayo nuevo.
- **Resultados históricos, sin revalidar sesión:** ASR-VAD e instrumental parcial en VPS; ningún analizador audiovisual integral aceptado. [Inventario y pruebas previas](../audio-tecnico/vps-repositorio-20261105.md).
- **Sólo documentado ahora:** MiniCPM-o 4.5 CPU completo, con código primario favorable pero RAM/latencia/corrección sin medir; VideoLLaMA2-AV con receta GPU. No hay modelo integrado listo y verificado en esta sesión. No se activó ni se pidió clave de API comercial.
- **Preflight actual comunicado por el integrador en este encargo:** SSH `onia-codex`, 4 CPU; RAM total 16.769.032.192bytes/disponible 10.696.945.664bytes(~9,96GiB); disco libre 68.125.302.784bytes; sin `/dev/nvidia0` ni `nvidia-smi`; FFmpeg y g++ presentes, CMake ausente. Docker y el MP4 antiguo devolvieron permiso denegado. Observación del integrador, no conexión de este subagente. Navegador reprodujo un reel, pero los outputs disponibles fueron cuadros/DOM: no evidencia de escucha o ingestión nativa temporal.

## Próxima acción acotada que cambiaría la decisión

Responsable integrador: el preflight actual y la reserva histórica de 6 GiB dejan menos de 4 GiB adicionales. No existe evidencia de encaje de esta candidata en ese margen. El integrador decidió no instalar/ejecutar un modelo de 9B con esas condiciones; se cierra la selección documental sin más familias. Los 6,32 GiB de pesos no equivalen a RAM, pero tampoco autorizan inventar un consumo menor. Falta además CMake y acceso efectivo a los medios requeridos.

Si cambia el margen o aparece evidencia primaria suficiente de encaje y se asigna un ensayo, preparar **una sola** revisión MiniCPM-o 4.5 CPU y harness neutral, fijar hashes y corte de recursos. Primero silencio sin VAD con imagen neutra; después controles positivos conocidos de voz/música/efectos, orden audiovisual A/B e inversión/desfase. Detener ante alucinación excluyente. Acertar silencio solo no acredita las demás capacidades; un límite de recursos es un resultado técnico, no un fracaso semántico. Esta receta no inicia ese trabajo.

Sólo tras superar controles independientes corresponde un reel español breve, con cobertura y FPS declarados. Comparar guion, cortes, movimiento, voz, prosodia, música, SFX y sincronía por separado. Para “humo o real”, extraer afirmaciones con tiempos y verificar sus fuentes externas: percibir la edición no demuestra resultados comerciales ni veracidad. Guardar patrones y evidencia reutilizables constituye aprendizaje operativo; no cambia pesos del modelo.

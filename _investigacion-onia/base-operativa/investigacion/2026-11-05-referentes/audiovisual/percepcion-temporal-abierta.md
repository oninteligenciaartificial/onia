# Dos candidatos abiertos de percepción temporal · prueba acotada

5 de noviembre de 2026. Responsable: Video; investigación de VideoLLaMA3 delegada a Sol e integrada contra archivos reales. **Ninguno queda validado para los grupos B.** VideoLLaMA3 remoto produjo una respuesta parcial; Smol500M local ejecutó A/B, pero falló orden y movimiento. No se aplicaron a referentes. La continuación local al final supera los límites de descarga y estados «sin probar» de la primera tanda remota conservada debajo.

## Primera tanda: declarado y disponible

| Familia y versión local candidata | Código y pesos | Entrada y límite temporal documentado | Viabilidad en esta PC |
|---|---|---|---|
| SmolVLM2-500M-Video-Instruct | Checkpoints Apache 2.0 en la [ficha oficial](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct); implementación Transformers [Apache 2.0](https://github.com/huggingface/transformers/blob/main/LICENSE). | Recibe archivo de video; lo convierte en secuencia de cuadros con marcas temporales. El [preprocesador publicado](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct/blob/main/preprocessor_config.json) fija 1 FPS, máximo 64 cuadros y lado mayor 512 para video. Son límites de muestreo, no garantía de conservar todos los eventos de una pieza larga. | La ficha raw consultada declara 1,8 GB de GPU para video. Es una afirmación del autor sin medición nuestra ni configuración suficiente para garantizar este equipo. Local sin probar. |
| VideoLLaMA3-2B | Repo con [LICENSE Apache 2.0](https://github.com/DAMO-NLP-SG/VideoLLaMA3/blob/main/LICENSE); [pesos 2B](https://huggingface.co/DAMO-NLP-SG/VideoLLaMA3-2B) etiquetados Apache 2.0, sin LICENSE separado encontrado en su árbol. El [README](https://github.com/DAMO-NLP-SG/VideoLLaMA3#-license) restringe el **servicio** de investigación a uso no comercial y remite a términos de modelos/datos. No equivale a permiso comercial indiscriminado de la demo. | Video real, selección ordenada y reducción de cuadros; ejemplo oficial a 1 FPS/máximo 128. La demo permite ajustar FPS/máximo; se probó a 5 FPS/128. Aumentar duración con tope de cuadros reduce cobertura temporal. | No se encontró mínimo oficial medido para RTX 3050 de 4 GiB. El ejemplo BF16/FlashAttention2/CUDA no prueba compatibilidad ni memoria suficiente. Local sin probar. |

Equipo objetivo: i5-11400H, 23,65 GiB RAM total, unos 8 GiB libres habituales, RTX 3050 de 4 GiB. En la caché HF predeterminada se encontraron modelos ASR, sin pesos de estas familias. No se descargaron pesos, instalaron paquetes ni ejecutó inferencia local. No se calculó RAM a partir del tamaño de los pesos. Las demos usan versiones mayores: **SmolVLM2-2.2B y VideoLLaMA3-7B**; su resultado no valida 500M/2B local. Versiones comprobadas en [app Smol](https://huggingface.co/spaces/HuggingFaceTB/SmolVLM2/blob/main/app.py) y [app VideoLLaMA3](https://huggingface.co/spaces/lixin4ever/VideoLLaMA3/blob/main/app.py).

## Prueba observada, sin cuenta ni pago

Sólo se subieron dos MP4 sintéticos propios de 7 s, 320×180, 24 FPS, sin audio, menores de 10 KB. A: gris → cuadrado rojo izquierdo → círculo verde central → triángulo azul derecho → círculo amarillo que se mueve izquierda→derecha → gris. B invierte exactamente los cuadros y la dirección. Mismos extremos y figuras; una imagen aislada no resuelve ambos. Prompt neutral idéntico pide orden, posición y movimiento/dirección, sin respuestas esperadas. Aceptación: ambos órdenes y direcciones correctos.

| Demo oficial | Respuesta real | Evaluación |
|---|---|---|
| [SmolVLM2](https://huggingface.co/spaces/HuggingFaceTB/SmolVLM2), remoto 2.2B | Configuración/API públicas accesibles. A: upload HTTP 200, creación de evento HTTP 200, SSE HTTP 200; termina `event: error`, `data: "404: Not Found"`. | No hubo inferencia acreditada ni respuesta perceptual. No se identifica la causa interna. B no ejecutado; sin reintento idéntico. |
| [VideoLLaMA3](https://huggingface.co/spaces/lixin4ever/VideoLLaMA3), remoto 7B | A completó sin autenticación: rojo/cuadrado → verde/círculo → azul/triángulo → amarillo/círculo, con intervalos. Omitió posiciones y movimiento; describió fondo negro donde el control es gris y anticipó el rojo a 0 s. B: upload/call/SSE HTTP 200, pero `event: error`, `data: null`; sin respuesta. | Inferencia remota anónima puntual comprobada, orden grueso de A correcto; **criterio de aceptación no superado**. B no permite validar inversión. Runtime posterior RUNNING/READY no explica el error. Sin reintento. |

VideoLLaMA3 usó `do_sample=false`, temperatura 0,2, top_p 0,9, 256 tokens, 5 FPS, máximo 128 cuadros. Smol usó el endpoint público `/chat`, conversación nueva y 200 tokens. Ninguna llamada usó cookies, Bearer o credenciales. Sólo sintéticos; ningún medio privado o referente salió del equipo.

Evidencia privada recuperable desde la raíz de base-operativa: `operacion/referentes-20261105/video/percepcion-abierta/`. En `root/`: `controls.json`, `controles.py`, MP4, fuentes GET, solicitudes y `smol-controls-results.json`. En `candidate2/`: `a-request.json`, `a-final.json`, `a-events.txt`, `b-request.json`, `b-events.txt`, estados HTTP, script y runtime posterior. SHA256 A: `fe56b56fff432c1a0d5695b52ea7e55e42ba425403b624381d2a3f0e2a3e9faf`; B: `87e78c58f7181d5491058d175353016eb7b1fd4bc8ea81e552ab97613480b261`. Estos auxiliares ignorados no sustituyen este registro versionado.

## Audio, alcance y condición para avanzar

No se acredita audio nativo disponible en estas rutas. Smol publica entradas de texto/imagen/video; parámetros genéricos de audio en documentación del procesador no prueban comprensión acústica del checkpoint ni su demo. VideoLLaMA3 declara audio/voz como modalidades aún no exploradas en su [artículo, §6.2–6.3](https://arxiv.org/html/2501.13106v1). No se hereda audio de VideoLLaMA2 por la semejanza del nombre. No hubo controles acústicos en este frente; el rechazo de Eureka comunicado por Jefa no se convierte en resultado propio.

Los siete grupos B y las 39 pistas C conservan sus límites. Incluso acertar estos controles sólo validaría orden/movimiento grueso: faltan destellos, fluidez, comodidad de lectura, ritmo global y sincronía. El muestreo a 1 FPS es insuficiente para certificar eventos subsegundo.

**Salida de la primera tanda:** mantener el corpus sin aplicación automática. VideoLLaMA3 requiere un cambio de condición del servicio y completar B más ambos movimientos; disponibilidad GET sola no basta. La prueba local de Smol500M se autorizó y ejecutó en la continuación siguiente.

## Continuación local autorizada · resultado real A/B

**SmolVLM2-500M ejecutó ambos controles en CPU y queda rechazado en esta configuración para orden/movimiento.** No hubo otra familia, demo remota repetida, nuevos controles ni aplicación al corpus.

Pesos oficiales fijados a [`7b375e1b73b11138ff12fe22c8f2822d8fe03467`](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct/tree/7b375e1b73b11138ff12fe22c8f2822d8fe03467), checkpoint Apache 2.0; `model.safetensors` descargado: 2.029.990.624 bytes, sin ONNX ni Python del repositorio. Se revisaron configuración, muestreo, marcas temporales, lector y soporte SDPA de la implementación instalada; `trust_remote_code=False`, carga offline y safetensors. Manifiestos privados conservan hashes del modelo y de diez archivos de código, licencias y versiones.

Entorno exclusivo `root/local-venv`: copia independiente de dependencias existentes, sin modificar `midasheng-venv`. PyTorch 2.15.0+cpu, torchvision 0.29.2+cpu, Transformers 4.57.6; añadidos únicamente num2words 0.5.14, docopt 0.6.2 y PyAV 16.0.1. Primer intento de preparación tuvo fallos de ensurepip/ruta larga, resueltos sin instalación global; una descarga PyAV cortada se completó con timeout mayor. El primer arranque falló antes de inferir porque torchvision ya no expone `read_video`; se conservó el error y se seleccionó PyAV desde el script, sin editar paquetes.

Preflight: 7,66 GiB RAM libre, 39,88 GiB de disco y 3.951 MiB VRAM libre. CPU float32/SDPA, cuatro hilos; GPU sin usar y sin instalación CUDA. Supervisor sobre el proceso propio y descendientes: reserva mínima 2 GiB, 300 s por etapa/control y 720 s total. Ejecución final terminó con código 0 en 80,56 s: pico RSS agregado **2,84 GiB**, pico memoria privada **3,34 GiB**, mínimo RAM libre **4,86 GiB**, disco final **37,54 GiB**. No se activó ningún corte. Son mediciones de esta prueba, no estimaciones desde pesos ni prueba de VRAM.

Mismo prompt neutral de la tanda remota, greedy, máximo 192 tokens, caché KV. Cada MP4 de 168 cuadros se muestreó en **14 cuadros de 512×512**: índices `0,12,25,38,51,64,77,89,102,115,128,141,154,167`, de 0 a 6,958 s, separaciones de 0,500–0,542 s (objetivo 2 FPS). Cubre cada figura y cuatro posiciones del movimiento amarillo en ambos sentidos. No es percepción continua. El procesador representa las marcas en segundos enteros, por lo que dos cuadros pueden compartir marca; el orden de los cuadros se conserva.

| Atributo | A, 36,20 s | B, 35,38 s |
|---|---|---|
| Respuesta real | Repite «Yellow circle on gray background» hasta 192 tokens. | Repite círculo amarillo/fondo gris y luego círculo verde/fondo gris hasta 192 tokens. |
| Colores/formas | Sólo amarillo/círculo: reconocimiento parcial. | Amarillo/círculo y verde/círculo: parcial. |
| Orden completo y extremos | Omite rojo, verde, azul y extremos: falla. | Omite azul, rojo y extremos: falla. |
| Posición y dirección | Omitidas: falla. | Omitidas: falla. |

Evidencia en el mismo auxiliar `root/`: `local-results.json` (ambas respuestas íntegras), `probe-a-local-input.json`/`probe-b-local-input.json` y sus TXT (muestreo y entrada real), `local-monitor.json`, `local-run.log`, `local-first-decoder-error.log`, `local-download-manifest.json`, `local-environment-manifest.json`, `local-preflight.json` y scripts. Modelo descargado y entorno quedan inactivos; ambos controles terminaron, sin inferencia pendiente.

**Decisión y siguiente responsable:** Jefa recibe un fallo perceptual con ejecución local acreditada; no aceptar los siete grupos B ni C, ni iniciar nuevas rondas por este resultado. La restricción posterior de Sergio limita esta continuación a A/B y queda cumplida. Para B permanece la revisión temporal a 1× por atributo/intervalo, y pieza completa para ritmo global; Jefa decide esa vía. Este cierre acotado no cierra el goal integral ni demuestra imposibilidad de toda configuración de la familia.

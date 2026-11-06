# Rutas acústicas comprobadas · 5/11/2026

Inventario y comprobación por Desarrollo y subagente técnico `audio_routes`; sin mensajes a otros chats, secretos, instalaciones, servicios, subidas o gasto. No se interpretó una salida de texto como escucha del agente.

| Ruta | Prueba/observación | Resultado y límite | Costo/recursos |
|---|---|---|---|
| `functions.audio(AudioContent)` | WAV en memoria, mono16k/PCM16, 1s/32.044 bytes: silencio→tono440→silencio | Respuesta exacta `audio content omitted because you do not support audio input`. El receptor no admite audio; no hay percepción | Sin API paga ni archivos |
| Faster-whisper local | Silencio, tono440, frase conocida y reel completo; sin/con VAD | Sin VAD inventa subtítulos sobre tono. Con VAD suprime ambos negativos y reconoce frase conocida. Sólo borrador verbal; no música/prosodia/SFX | CPU4/int8, pesos existentes486MB; tanda VAD20,469s; sin descargas; pico RAM no medido |
| Qwen2.5 Omni histórico | No reejecutado: silencio fallido documentado | Rechazado como evidencia acústica; no justificar otra instalación igual | Antecedente CPU9,22GiB, no consumo nuevo |
| YAMNet/CLAP históricos | No reejecutados; revisadas limitaciones | Candidatos, no escucha. CLAP no reconoció click de una muestra; no acredita sensibilidad a clicks ni palmadas | Sin consumo nuevo |
| Phi-4 multimodal, demo oficial | Lectura de [demo](https://huggingface.co/spaces/microsoft/phi-4-multimodal): Runtime error al obtener pesos por validación de hostname | Admite audio según [Microsoft](https://huggingface.co/microsoft/Phi-4-multimodal-instruct); no hubo inferencia ni envío de medios. Lectura web, no sondeo de salud independiente | 5,6B, MIT; [pesos](https://huggingface.co/microsoft/Phi-4-multimodal-instruct/tree/main) ≈11,15GB, más memoria de ejecución. No instalado |
| Audio Flamingo3, demo oficial | Lectura de [demo NVIDIA](https://huggingface.co/spaces/nvidia/audio-flamingo-3): Build error | [Modelo](https://huggingface.co/nvidia/audio-flamingo-3) admite voz/música/sonidos; no hubo inferencia ni envío de medios | 7B, licencia de investigación no comercial; ≈14GB sólo pesos FP16 estimados. No instalado |
| Higgsfield video analysis | Catálogo + lectura de análisis anteriores/status + documentación pública | Salida descriptiva de audio comprobada; comprensión acústica fiable aún no probada | Tarifa/inclusión/proveedor no verificados; ninguna creación/subida |

## Higgsfield: candidata concreta

`video_analysis_jobs({size:1})` y `video_analysis_status` recuperaron el análisis completado `8f15954a-7245-4c4c-9492-02f2ee91d0b5`: cinco escenas con `audio`, `visual`, `shot_type`, `timestamp_start` y `timestamp_end`. Audio incluye palabras atribuidas a voz y descripciones de música/pulso/cierre. Acredita esos campos de salida, no que el modelo use la pista en lugar de inferirla de la imagen. Se revisaron los cinco análisis existentes; ninguno identificó el Pedro de90s. No se copiaron contenidos ajenos al encargo.

- `video_analysis_create`: exactamente `youtube_url` o `video_input_id`; inicia queued. No declara precio, `get_cost`, `max_credits`, proveedor ni selector de modelo. URL externa sólo YouTube; Pedro de Instagram exigiría archivo subido.
- `video_analysis_status`: `video_analyze_id`, estado/error y `scenes: Array<unknown>`; las escenas reales contenían audio.
- Leer saldo/plan no acredita tarifa ni gratuidad. Los contadores gratuitos explícitos corresponden a otras funciones. No se asumió incluido ni que el backend sea Gemini.
- [Changelog oficial](https://higgsfield.ai/creator-hub/changelog) describe estructura, planos y ritmo. [Ayuda MCP](https://higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp) habla de créditos de generaciones, sin fijar tarifa de este analizador. No convertirlo en un costo inventado de análisis.

Quedan [cuatro probes](controles-video.json) locales regenerados: 6s de contenedor, imagen gris idéntica comprobada por SHA de frames decodificados y AAC 48 kHz estéreo con objetivo 128 kb/s común. Son tres controles conocidos —silencio, tono440 y voz sintética— más una muestra real Pedro2,3–8,3s sin verdad semántica validada. Nombres `probe-a.mp4` a `probe-d.mp4`, sin texto visual que revele la respuesta;260.081bytes en total. [Script](preparar_controles_video.py) y [QA 26/26](qa-controles-video.json). No hubo normalización: mono duplicado con ganancia unitaria por canal; estéreo conservado. El bitrate efectivo varía con la señal, y el relleno AAC posterior a6s queda fuera de evaluación. **No subidos ni enviados a análisis.** Material sintético/público, sin secretos ni medios privados del usuario.

Una prueba futura requiere resolver costo/proveedor dentro del alcance vigente o recibir una autorización expresa que cubra esa incertidumbre. Jefa centralizó esa consulta; su estado y límites están en [ESTADO](ESTADO.md). No hay respuesta/autorización comunicada y no se sube ni ejecuta todavía. Usar la misma instrucción neutral y orden variado, sólo nombres anónimos; nunca enviar esperados, identidad de Pedro, scripts o manifiestos. Criterio técnico propuesto: silencio sin voz/música inventada, tono continuo sin habla (no exigir estimación exacta de440Hz), palabras conocidas reconocibles y diferencias acústicas correctas manteniendo la imagen idéntica; el fragmento real requiere contraste independiente. Aun pasando esos controles no certificar prosodia, SFX, música o sincronía fina por el nombre del campo. Sigue aplicando la advertencia del catálogo sobre menor exactitud en videos largos.

## Solución inmediata

La extracción está resuelta y la vía verbal funciona con límites documentados. Para el juicio acústico indispensable, usar la selección MP3 de12s y la pregunta neutral de [ESTADO](ESTADO.md). Conservar WAV exacto y reel completo. Esta intervención no equivale a escucha integral de90s ni resuelve automáticamente los demás referentes.

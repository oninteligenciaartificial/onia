# Demo comunitaria de audio · 5/11/2026

## Resultado

Se revisó una única candidata: [hammertoe/bimomni-barbados-demo](https://huggingface.co/spaces/hammertoe/bimomni-barbados-demo). Su código publicado carga directamente un modelo abierto de audio identificable, pero la aplicación no permite la instrucción neutral común requerida para los controles: sólo acepta un archivo y fuerza una tarea de transcripción. Por esa barrera no se envió siquiera el silencio y no hay resultado de inferencia ni evaluación acústica. Este hallazgo no demuestra que no exista otra demo adecuada.

## Evidencia y alcance

- La API pública del Space lo informó como público y `RUNNING`, en hardware `zero-a10g`, con revisión `9da9a4f7a2b930a2d345aae6bdee68d477cd1833`. Eso es un estado informado, no una prueba de inferencia anónima ni una certificación del código realmente desplegado.
- El [app.py de esa revisión](https://huggingface.co/spaces/hammertoe/bimomni-barbados-demo/blob/9da9a4f7a2b930a2d345aae6bdee68d477cd1833/app.py) llama directamente a `Qwen3OmniMoeForConditionalGeneration.from_pretrained`, con `Qwen/Qwen3-Omni-30B-A3B-Instruct` y revisión `26291f793822fb6be9555850f06dfe95f2d7e695`. La [ficha de esa revisión](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct/blob/26291f793822fb6be9555850f06dfe95f2d7e695/README.md) identifica licencia Apache 2.0 y entrada de audio. Es Qwen3, distinto del Qwen2.5 rechazado antes. El archivo fuente consultado tuvo SHA-256 `bac7b20979af8c8f087680af629bf123cdbcbfa92beb6c587969b0e3382803f5`.
- La aplicación compara Whisper, Qwen base y Qwen con el adaptador `hammertoe/Qwen3-Omni-30B-A3B-Barbados-LoRA-v4`, cuya revisión no está fijada en el código. Whisper es un comparador separado que se ejecuta primero; el mismo arreglo de audio se pasa después a Qwen, no el texto de Whisper.
- `compare(audio_path)` y el botón Gradio reciben sólo audio. El texto fijo pide transcripción literal y prohíbe describir el audio. Por tanto, una salida sobre silencio mediría, como máximo, comportamiento de transcripción en esa configuración, no la prueba requerida de descripción acústica con instrucción neutral idéntica.
- El preprocesamiento visible lee el audio, mezcla a mono, remuestrea a 16 kHz y limita a 29 segundos; no se encontró VAD en ese código visible. No se verificó el tratamiento interno del procesador o del servicio, por lo que no se acredita la conservación del silencio extremo a extremo.
- No se realizó solicitud de inferencia, ni se enviaron WAV o medios privados, ni se usaron cuentas o credenciales. Tampoco se verificaron acceso anónimo efectivo, cuotas ni costos de inferencia. No se descargaron modelos ni se inició ejecución local; sólo se consultaron metadatos y código público.

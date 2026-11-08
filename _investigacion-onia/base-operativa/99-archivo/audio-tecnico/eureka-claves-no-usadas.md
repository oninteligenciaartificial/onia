# Eureka · contraste de 17 claves no utilizadas

Revisiones: [modelo oficial `219761d`](https://huggingface.co/cslys1999/Eureka-Audio-Instruct/tree/219761da53c9c6c5900a84a723d88ccc29db66d3) y [API oficial `51dac59`](https://github.com/Alittleegg/Eureka-Audio/blob/51dac590e0c6e3c48d8094a5b5431c7f86ff3be4/eureka_infer/api/eureka.py). El blob Git de la copia original de `modeling_eureka_audio.py` coincide con el publicado (`a626e3819f2e0622294c58744a854da982c23273`); la configuración original coincide estructuralmente con una descarga independiente de la misma revisión. La prueba CPU usa una copia con cambios documentados de SDPA y precisión, no el backend oficial sin alterar.

## Clase y recorrido de entrada

`config.json` declara `architectures: EurekaAudioForCausalLM` y enlaza `AutoModelForCausalLM` a `modeling_eureka_audio.EurekaAudioForCausalLM`. La API oficial usa precisamente `AutoModelForCausalLM.from_pretrained(..., trust_remote_code=True)`; por tanto, **la clase seleccionada coincide con el ejemplo y la configuración oficiales**. Esto no demuestra que la adaptación CPU/offload produzca respuestas fiables.

En esa clase, la entrada acústica pasa por `audio_encoder`, después `audio_moe_adaptor` y `_audio_embedding_forward`, y sus representaciones alimentan `backbone`; los logits de salida textual usan `backbone.lm_head`. La inspección de este recorrido sí demuestra qué componentes se invocan para comprensión en el código publicado, no que todas las capacidades del checkpoint original se hayan implementado en la clase.

## Advertencia

El cargador informó como no utilizados `audio_embed.weight`; ocho pesos/sesgos en `audio_ffn_adaptor` (capas 0, 1, 3 y 4); `audio_head.weight`; seis pesos/sesgos en `audio_out_projection` (capas 0, 1 y 3); y `lm_head.weight`. Las 17 claves existen en el índice de los pesos descargados. Las primeras cuatro familias no aparecen como módulos ejecutados en la clase oficial revisada. **Sus nombres sugieren componentes de una vía de salida de audio, pero ni el código ni el ejemplo consultado demuestran aquí su procedencia o función exacta.** No se puede certificar su inocuidad para la calidad de comprensión ni atribuirles el fallo nativo.

## Cabeza textual y ligadura

La configuración anidada de Qwen establece `tie_word_embeddings: true`. La clase declara `_tied_weights_keys = ["lm_head.weight"]`; `get_output_embeddings()` devuelve `backbone.lm_head` y el forward usa esa misma cabeza. Esto documenta la intención de ligar la cabeza textual con embeddings mediante la implementación Transformers/Qwen; **no se ha comprobado una identidad de punteros durante el offload ni se demuestra por esa declaración que cualquier clave descartada sea irrelevante**.

El índice contiene tres tensores distintos por nombre: `lm_head.weight`, `backbone.lm_head.weight` y `backbone.model.embed_tokens.weight`, todos BF16 con forma `[151936, 2048]` y 622.329.856 bytes cada uno. Después de detener la inferencia, se calculó el SHA-256 de **cada intervalo completo**: los tres coinciden en `d200b8770469e60f5ed0ee9a76ef6f7b6f836881c905ab3093b730cd0a51f4c6`. [Resultados](eureka-lm-head-hashes.json), [script de lectura](eureka-hash-lm-head.py). Esto acredita igualdad de bytes en el checkpoint, no alias efectivo durante offload. La función de las otras 16 claves y la ligadura efectiva en runtime siguen sin acreditarse; no se descarta globalmente la advertencia.

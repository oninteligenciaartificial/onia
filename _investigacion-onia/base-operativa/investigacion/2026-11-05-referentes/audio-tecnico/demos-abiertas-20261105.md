# Dos demos oficiales Qwen · comprobación de acceso y backend

**5 de noviembre de 2026, 16:17 America/Caracas. Resultado: ninguna de estas dos rutas satisface el alcance autorizado para ensayar controles.** Se consultaron fuentes públicas sin cuenta y sin enviar audios, prompts, credenciales ni solicitudes de inferencia. `RUNNING` sólo indica estado publicado del Space, no acceso anónimo completo, ausencia de cuota, ni funcionamiento acústico. No hubo respuestas, tiempos de inferencia ni controles evaluados.

Sergio pidió producto open source y no exigió que la ejecución fuera exclusivamente local. La restricción de esta tanda excluye API paga, credenciales, cuotas y gasto; no se convierte una preferencia de ubicación en una orden suya. El ensayo fallido anterior fue Qwen2.5-Omni 7B; no se repitió ni se extrapola a Qwen3/Qwen3.5.

## Candidato 1: Qwen3-Omni Demo

[Space oficial](https://huggingface.co/spaces/Qwen/Qwen3-Omni-Demo), estado `RUNNING` en metadata pública; revisión `f04f51c20aeae49bca0005aa99e56bbdfd4267aa`. [Código exacto](https://huggingface.co/spaces/Qwen/Qwen3-Omni-Demo/blob/f04f51c20aeae49bca0005aa99e56bbdfd4267aa/app.py), SHA-256 de bytes leídos `85649969331c5af9eb3da1af90397dbb077d19da405e298837ececa9cd485445`; la lectura de `main` coincidió. Su [README](https://huggingface.co/spaces/Qwen/Qwen3-Omni-Demo/blob/f04f51c20aeae49bca0005aa99e56bbdfd4267aa/README.md) declara Apache 2.0 para el Space. [Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct) publica pesos bajo Apache 2.0 y declara entrada nativa de audio; es una familia distinta de Qwen2.5.

**Puerta real:** el `app.py` consultado crea cliente `OpenAI` hacia DashScope con una variable de entorno del operador, y la llamada efectiva fija `qwen3-omni-flash-2025-12-01`, no el checkpoint 30B-A3B-Instruct publicado arriba. El código de la interfaz sube el archivo a almacenamiento y lo pasa como `input_audio` mediante URL; no aparece una conversión a transcripción en ese tramo visible. El preprocesamiento interno del servicio, incluida detección de voz o descarte de silencio, no es inspeccionable por esta evidencia.

Alibaba documenta [facturación y límites del modelo Flash](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/qwen3-omni-flash). No se conoce la región, el acuerdo de patrocinio o la cuota del operador de este Space; una demo visible no prueba que la llamada de backend sea gratuita ni que el usuario pague personalmente. Tampoco se acreditó que los pesos de esa variante Flash sean los del checkpoint abierto. **No se ejecutaron controles**, por la prohibición de API facturable/cuota y la falta de identidad de pesos comprobada.

## Candidato 2: Qwen3.5-Omni Offline Demo

[Space oficial](https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Offline-Demo), estado `RUNNING` en metadata pública; revisión `2888772e0aa651efa67c2ece0a3c5a23bcf91a50`. [Código exacto](https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Offline-Demo/blob/2888772e0aa651efa67c2ece0a3c5a23bcf91a50/app.py), SHA-256 `86f22ba1bc2d2bfb0a15c5cb3d85f4e7a74f0c7b98d0187f24c03e16dbe6b816`.

**Puerta real:** pese al título «Offline», su código también crea cliente DashScope y fija `qwen3.5-omni-plus`; «offline» identifica la modalidad de interfaz, no una carga local demostrada. Remite el archivo como `input_audio` tras subirlo a almacenamiento. No se ha verificado ausencia de VAD o ASR dentro del backend. Su [README del Space](https://huggingface.co/spaces/Qwen/Qwen3.5-Omni-Offline-Demo/blob/2888772e0aa651efa67c2ece0a3c5a23bcf91a50/README.md) no declara licencia; tampoco se verificó publicación de pesos de la variante Plus usada. Código visible no basta para afirmar licencia abierta del backend.

[Precios oficiales de Alibaba](https://www.alibabacloud.com/help/en/model-studio/model-pricing) identifican Plus como servicio facturable y describen cuotas gratuitas sujetas a región y condiciones. No se conoce la cuenta/región del operador ni el costo real por ejecución de esta demo. **No se ejecutaron controles**: la ruta depende de API facturable/cuota y no acredita pesos abiertos.

## Condición concreta y alcance del resultado

Para ensayar los WAV sin ampliar permisos hace falta una instancia oficial accesible sin cuenta ni pago/cuota, que identifique como backend un checkpoint abierto concreto —por ejemplo el Qwen3-Omni-30B-A3B-Instruct Apache 2.0— y permita comprobar que recibe la forma de onda completa sin ASR o VAD previo que oculte silencio. Allí enviar primero silencio y detener si inventa voz o música; después tono, voz y patrón con nombres anónimos e instrucción neutral idéntica. La condición es específica de las dos rutas examinadas, no demuestra que no exista ninguna otra demo. Ningún resultado comercial ni comprensión acústica fue acreditado aquí.

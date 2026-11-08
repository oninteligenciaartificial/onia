# Justin Welsh · intentos de ASR público

Fecha: 8/11/2026, UTC. Estado vigente: **parcial; dos intentos YouTube fallidos y una transcripción nueva por audio público equivalente**. El registro de fallos de abajo se conserva como historial y queda actualizado por la recuperación final. Este archivo registra fallos de acceso, no es un ASR. Sin cookies, login, credenciales ni interacción con personas. No se tocaron servicios.

## Selección de dos piezas

| Pieza | Procedencia y pertinencia | Límite de duración |
|---|---|---|
| [The Solopreneur: He Makes $1.7M With 0 Employees](https://www.youtube.com/watch?v=v6IF-lVuvbs), Starter Story | El resultado primario de YouTube identifica entrevista con Justin. Sus temas incluyen ingresos, costes, estrategia de contenido, ideas y rutina. [Descripción/capítulos replicados](https://trackpodcasts.com/episodes/the-solopreneur-he-makes-1-7m-with-0-employees-starter-story) llegan a 11:14; esta réplica se declara no oficial y sólo sirve como pista de selección. | Candidato corto; duración exacta no recuperada por el script. Límite duro aplicado: 900 s. |
| [Justin Welsh on How to Find a Profitable Niche Worth $2.25 Million](https://www.youtube.com/watch?v=Pv24uWUJ794), Ash Roy / Productive Insights | [Página del entrevistador](https://www.productiveinsights.com/podcast/justin-welsh-on-how-to-find-profitable-niche), leída mediante web y GET público, enlaza el iframe de este ID y contiene capítulos 00:00–14:02 y transcripción automática. Sirve para estudiar nicho, oferta y transformación del negocio. | El script superó la lectura inicial y su comprobación <=900 s antes de fallar en la segunda extracción para descargar. No se imprimió duración exacta. |

No se eligieron entrevistas de 40–80 min: las búsquedas localizaron, entre otras, Peter Yang `ZkwYxYfkfYU` (capítulos hasta39:22) y Creator Science (63 min); se descartaron para respetar el presupuesto. No se descargaron como alternativa.

## Ejecución real

```sh
~/asr/transcribir.sh 'https://www.youtube.com/watch?v=v6IF-lVuvbs' --max-seconds 900
~/asr/transcribir.sh 'https://www.youtube.com/watch?v=Pv24uWUJ794' --max-seconds 900
```

Ambas ejecuciones terminaron con **exit code 1**. Mensaje excluyente de yt-dlp para ambos IDs: `Sign in to confirm you’re not a bot`. También advirtió ausencia de un runtime JavaScript compatible habilitado. Esa advertencia no demuestra por sí sola la causa del bloqueo.

En Starter Story falló `extract_info(download=False)`. En Productive Insights la primera extracción y el control de duración pasaron; falló `extract_info(download=True)`. En ninguno llegó a ejecutar Whisper ni creó Markdown/JSON de segmentos. Audio efectivamente transcrito de Justin en esta subtarea: **0 min**. Los dos límites de 900 s impiden aceptar más de 30 min entre las piezas; el fallo no se presenta como cumplimiento de las 2–3 transcripciones solicitadas.

El lector web también falló al abrir directamente las dos páginas watch. La alternativa efectiva fue leer la página pública del entrevistador para localizar la segunda pieza y su texto; ese texto no se convierte en ASR propio ni acredita música, cortes o prosodia. No se volvió a intentar el mismo bloqueo con cookies o sesiones autenticadas.

## Salida concreta para continuar

La página de Productive Insights ofrece transcripción automática del entrevistador y un reproductor de audio Transistor (`https://share.transistor.fm/e/0b56b0db`). Esto es una ruta pública localizada, **no descarga o transcripción probada** en esta subtarea. Si se consigue acceso anónimo a los medios cortos, repetir los comandos con los mismos límites; mantener procedencia, timestamps e incertidumbre del ASR. Hasta entonces, conservar el cerebro de Justin como parcial en frases audiovisuales y edición, y usar sus ensayos como evidencia escrita diferenciada.


## Recuperación posterior exitosa · prevalece sobre el bloqueo de descarga

El player público Transistor identificado arriba enlaza `https://media.transistor.fm/0b56b0db/ed298c2d.mp3`, identifica episodio240 de Ash Roy, publicado5/8/2024, y declara duración15:36. La misma página del entrevistador enlaza el video `Pv24uWUJ794` y el reproductor: se documenta la relación editorial, sin afirmar identidad binaria o sincronía temporal audio/video.

El MP3 se recuperó sin autenticación. El límite inicial900s rechazó la pista de935,63575s antes de Whisper; se ajustó a960s para esta única pieza (~15:36), dentro de los30min por referente. Ejecución exitosa (exit0):

```sh
~/asr/transcribir.sh 'https://media.transistor.fm/0b56b0db/ed298c2d.mp3' --max-seconds 960
```

Entrega: [Markdown con timestamps](9674a5070ccc-20261108T155711133648Z.md) y [segmentos JSON](9674a5070ccc-20261108T155711133648Z.json). Modelo small, CPU/int8, VAD; idioma detectado inglés. SHA-256 audio: `7d84c44e0c6e9527ae8f69bf06a2a7f54d832a0c36f663bc9d5656e8f7b19fca`. Audio nuevo transcrito:935,63575s. El título genérico y canal desconocido del extractor directo no sustituyen la identificación del player/página primaria.

Se leyó el ASR y se cotejó atribución con los bloques de hablante de la página del entrevistador. A04:24–04:27 Justin prioriza calidad de audiencia; a07:20–07:24 recomienda comenzar desde lo conocido; a12:30–12:33 cuestiona promesas sin evidencia. Son referencias al texto automático, no escucha humana. Preguntas, introducción, promoción de membership49USD/mes desde14:27 y cierre pertenecen a Ash/Productive Insights; no incorporar ese precio a la escalera de Justin. Los timestamps corresponden al MP3 y sus insertos, no al video.

Resultado: **una pieza transcrita**. No contar YouTube fallido y MP3 equivalente como dos muestras. Faltan una o dos piezas adicionales para las2–3 solicitadas, e inspección visual/perceptual de edición; no hay datos para atribuir ritmo de cortes, subtítulos, B-roll o música al estilo propio de Justin. Las frases minutadas compactas se integraron en [su cerebro](../cerebros/justin-welsh.md).

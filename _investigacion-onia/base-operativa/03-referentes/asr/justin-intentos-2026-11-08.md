# Justin Welsh · intentos de ASR público

Fecha: 8/11/2026, UTC. Estado: **parcial; dos intentos reales, cero transcripciones nuevas**. Este archivo registra fallos de acceso, no es un ASR. Sin cookies, login, credenciales ni interacción con personas. No se tocaron servicios.

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

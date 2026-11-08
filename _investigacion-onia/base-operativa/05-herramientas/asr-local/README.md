# ASR local sin root

Instalado el 8/11/2026 en `/home/onia-codex-worker/asr/venv`. No usa Docker, sudo, servicios, cookies ni API de pago.

```bash
~/asr/transcribir.sh 'https://www.instagram.com/reel/DfVKglhEtc1/'
```

El wrapper ejecuta `~/asr/transcribir.py`. Estas copias versionadas permiten recuperar ambos archivos; el venv, pesos y audio quedan fuera del repo. Salida por defecto: `03-referentes/asr/<hash-URL>-<fecha-UTC>.md` y `.json`, sin sobrescribir transcripciones previas. `ASR_ROOT` y `ASR_OUTPUT` permiten cambiar las rutas. `--max-seconds 1800` rechaza piezas de más de 30 min; no lleva un presupuesto acumulado entre invocaciones: quien ejecuta debe sumar por referente. Si falta duración en metadata, comprueba el archivo descargado antes de inferir.

Motor `small`, CPU, int8, dos hilos, beam 5 y VAD. Los timestamps conservan posición en el audio. El texto es automático: no certifica citas, cifras, nombres, música, prosodia o edición. No publica archivo vacío cuando no detecta segmentos.

## Instalación reproducible

Si `python3 -m venv ~/asr/venv` falla por falta de ensurepip, crear con `--without-pip` y descargar el instalador oficial `https://bootstrap.pypa.io/get-pip.py` a `~/asr/`; ejecutarlo con el Python de ese venv. Instalar con su pip `faster-whisper yt-dlp 'av<19'`. El lock adjunto registra las versiones comprobadas. Copiar estos dos scripts a `~/asr/` y hacer ejecutable el `.sh`.

La descarga inicial del modelo necesita acceso a Hugging Face y unos 500 MB de pesos. Las cachés están dentro de `~/asr/`; el código fija HF_HOME/HF_XET_CACHE para evitar la caché home no escribible. PyAV decodifica el audio sin necesitar FFmpeg para este flujo. Licencias y capacidades: [faster-whisper, MIT](https://github.com/SYSTRAN/faster-whisper), [yt-dlp, Unlicense](https://github.com/yt-dlp/yt-dlp). Revisadas las instrucciones oficiales el 8/11/2026.

## Incidencias comprobadas

- El Python del sistema no tenía pip ni ensurepip. Se resolvió con bootstrap dentro del venv, sin modificar el sistema.
- La primera descarga Xet intentó escribir en caché no permitida: se resolvió fijando las cachés en `~/asr/`.
- faster-whisper 1.2.1 llama `av.open(..., metadata_errors='ignore')`; PyAV 19 ya no acepta ese argumento en esta instalación. Se fijó `av<19` y se repitió la prueba real.
- Las dos muestras de Rocha en YouTube exigieron verificación de bot. No se usaron sesiones privadas para eludirla. Instagram permitió descargar la muestra pública de Pedro.

Evidencia y resultado final de la prueba: [registro ASR de la tanda](../../03-referentes/asr/ejecucion-2026-11-08.md).

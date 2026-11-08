# Ejecución local ASR · 8/11/2026

## Resultado comprobado

Venv `/home/onia-codex-worker/asr/venv`; faster-whisper 1.2.1, modelo small en CPU int8, dos hilos, VAD. Script `~/asr/transcribir.sh <url>`, fuentes recuperables en [asr-local](../../05-herramientas/asr-local/). `pip check`: sin dependencias rotas. Sin root, sudo, contenedores ni cambios a servicios.

**Prueba de video corto completada:** reel público de Pedro Buerbaum [DfVKglhEtc1](https://www.instagram.com/reel/DfVKglhEtc1/), audio descargado por yt-dlp y 66,434 s decodificados. [Markdown con 18 segmentos](4b3a68cf8444-20261108T155204911834Z.md), [JSON](4b3a68cf8444-20261108T155204911834Z.json). El hash del audio está en el Markdown; audio y pesos conservados localmente fuera de Git. No fue escucha ni análisis de edición nuevo. Se conservan errores automáticos («contener», «las riegas») sin corregir como si fueran palabras verificadas.

## Descargas impedidas

| Referente / candidato | Resultado de esta sesión |
|---|---|
| Enrique Rocha · [LsOQDp76898](https://www.youtube.com/shorts/LsOQDp76898) | yt-dlp devolvió `Sign in to confirm you’re not a bot`; no audio ni nuevo ASR. |
| Enrique Rocha · [T_V-GujTLXA](https://www.youtube.com/shorts/T_V-GujTLXA) | Misma barrera en una segunda pieza; no audio ni nuevo ASR. |

Los intentos locales completos están en `~/asr/prueba-rocha.log` y `~/asr/rocha-2.log`; aquí se conserva sólo el fallo saneado. No se usaron cookies, cuentas ni servicios alternativos de transcripción. Las fichas previas con captions/observación documental siguen siendo fuentes fechadas; no se presentan como ASR nuevo.

## Cobertura y límites

El encargo actual prevalece sobre la aceptación histórica de un corpus sólo escrito para Justin o sobre la exclusión histórica de Cormac. Se añade Cormac como cerebro propio por solicitud actual. Reutilizar transcripciones o captions previos conserva su fecha y procedencia. Tener una descripción de captions sin el archivo disponible no autoriza inventar frases o minutos. La matriz final del índice distingue las brechas restantes.

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

## Ampliación de esta tanda

- Cormac: [reel público exacto DfWLWspIruU](https://www.instagram.com/reel/DfWLWspIruU/) descargado y transcrito con el mismo script; [ASR nuevo](1a51646a8ecd-20261108T155356159083Z.md) y [segmentos](1a51646a8ecd-20261108T155356159083Z.json). Una muestra, no las 2–3 requeridas; no se localizaron otras URLs exactas atribuibles sin inventarlas.
- Justin: [dos intentos de video y alternativa pública](justin-intentos-2026-11-08.md).
- Ali/Jeff: [intentos y límites](ali-jeff-intentos-2026-11-08.md).
- Iman: intentados `https://www.youtube.com/watch?v=vOBKA8n15vg` (~21:55 según corpus) y `https://www.youtube.com/watch?v=N9hkRtP7yzI` (~29 s, canal Moments con oficialidad no corroborada). Ambos rechazados por comprobación de bot antes de descargar; cero audio nuevo. El segundo es muestra del hablante, sin atribuir edición al canal oficial. Logs locales `~/asr/iman-1.log` y `iman-2.log`.
- Beltrán: intentados `https://www.youtube.com/watch?v=_ffz3Eo_wzM` (~77 s) y `https://www.youtube.com/watch?v=JKO8AQGZ5tc` (alternativa pública del corpus; límite del script 1800 s). Ambos rechazados por comprobación de bot antes de descargar; cero audio nuevo. La segunda pasa de alternativa histórica no seleccionada a intento nuevo explícito, sin contarla como analizada. Logs locales `~/asr/beltran-1.log` y `beltran-2.log`.

Presupuesto nuevo efectivamente transcrito hasta esta ampliación: Pedro ~1:06, Cormac ~0:38; ningún referente supera 30 min. Las duraciones históricas del corpus no son minutos de ASR ejecutados en esta sesión.

## Resultado final: alternativa pública de Justin

La página [Productive Insights, episodio con Justin Welsh](https://www.productiveinsights.com/podcast/justin-welsh-on-how-to-find-profitable-niche) enlaza el video `Pv24uWUJ794` y el [player público Transistor](https://share.transistor.fm/e/0b56b0db). El player expone el MP3 `https://media.transistor.fm/0b56b0db/ed298c2d.mp3`. El script no reconoce la página del player, pero sí descargó el MP3 público y lo transcribió completo: **935,636 s (~15:36), salida 0**. [ASR](9674a5070ccc-20261108T155711133648Z.md) · [segmentos JSON](9674a5070ccc-20261108T155711133648Z.json). El título/hash genérico y canal desconocido son metadata del extractor de MP3; la identificación editorial procede de las páginas enlazadas, no del modelo.

Primero se aplicó límite 900 s: el archivo fue rechazado por duración real **antes** de inferencia. Se amplió a 960 s, sin exceder los 30 min acumulados de audio de Justin. Las dos descargas de video previas no generaron audio. Intro, promoción e intervenciones de Ash no son palabras de Justin; el ASR no diariza. Las citas del cerebro se atribuyen usando la transcripción pública del entrevistador y conservan los tiempos **del MP3**, que no se equiparan a los del video. Una entrevista transcrita no cumple dos o tres muestras, ni permite inferir el estilo de edición propio del invitado.

**Balance final de ASR nuevo:** Pedro 66,434 s + Cormac ~37,75 s + Justin 935,636 s, tres piezas. Ningún referente supera 30 min. El resto usa evidencia previa o permanece parcial por las barreras de descarga registradas. No se utilizó ninguna sesión privada para resolver los bloqueos.

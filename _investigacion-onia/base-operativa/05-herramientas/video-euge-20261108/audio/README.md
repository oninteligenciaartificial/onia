# Captura local del audio original de Euge

La fuente es el video público `JuAQILH7dkQ`, de 30:02 según el reproductor. La captura usa la pista que entrega la pestaña del reproductor. El dueño del visor comprobó la selección «Spanish (US) original» en YouTube antes del piloto. [Video solicitado](https://www.youtube.com/watch?v=JuAQILH7dkQ)

## Uso y verificación

1. Con la pestaña de YouTube pausada, abrir `capturar-pestana.html` por `file://` en una pestaña aparte de Chromium. Elegir exclusivamente la pestaña del video y dejar activado «Compartir audio» en el selector oficial. El HTML sólo acepta una fuente de tipo pestaña con una pista de audio activa. Deshabilita la sugerencia de compartir monitores, de cambiar de fuente y de ofrecer audio de sistema o ventana. [Controles de Chromium](https://developer.chrome.com/docs/web-platform/screen-sharing-controls) · [Especificación de captura](https://www.w3.org/TR/screen-capture/)
2. Verificar pista original, sonido habilitado, video a 1× y ausencia de anuncio. Dejar una pausa inicial corta como control y pulsar Play una vez iniciada la grabación. Anotar tiempos del reproductor y UTC. El HTML graba VP8 y Opus en el mismo WebM, con hora UTC de inicio/fin y límite configurable. Al terminar, elegir un archivo nuevo en un directorio privado desde «Guardar WebM en…». Si el selector no está disponible, el enlace abre el WebM local para guardarlo manualmente.
3. Ejecutar `python3 verificar-av.py <grabación-local.webm>`. El recibo incluye SHA-256, formato, tiempos de paquetes, verificación de decodificación, niveles y marcas de silencio o de imagen con pocos cambios. Esas marcas orientan la revisión junto con los relojes. Una toma estática puede activar el detector; el umbral de silencio se refiere a nivel de señal. [FFmpeg](https://ffmpeg.org/ffmpeg-filters.html)
4. Ejecutar la inferencia con el guard y un lock común en un directorio propio 0700. Usar destinos privados nuevos y el SHA-256 del WebM verificado.

   ```sh
   nice -n 10 python3 asr-con-lock.py "$euge_lock" "$euge_eventos" "$euge_asr" "$euge_sha" \
     "$HOME/asr/venv/bin/python" -u asr-local.py "$euge_webm" "$euge_modelo" "$euge_asr"
   ```

   Faster-whisper small funciona con CPU int8, dos hilos y VAD. El JSON privado contiene los segmentos y stdout sólo presenta el resumen técnico. El guard distingue un resultado válido del estado devuelto por el supervisor. Si hay duda sobre un proceso vivo, cotejar su identidad desde el host antes de reintentar. [faster-whisper](https://github.com/SYSTRAN/faster-whisper) · [Pruebas del guard](recibo-guard.json)
5. Exportar los PTS y duraciones de paquetes de la pista de audio con FFprobe y pasar el CSV, el ASR y el mapa verificado a `alinear-asr.py`. Mantener el CSV y el JSON con texto fuera de Git. El script devuelve por stdout el resumen sin texto.

   ```sh
   ffprobe -v error -select_streams a:0 -show_packets -show_entries packet=pts_time,duration_time \
     -of csv=p=0 "$euge_webm" > "$euge_paquetes"
   python3 alinear-asr.py "$euge_asr" "$euge_paquetes" "$euge_mapa" "$euge_alineado"
   ```

El servidor PulseAudio no estaba disponible. El cliente FFmpeg reconocía el demuxer pero al abrir la fuente devolvió `No such process`; faltaba el socket de usuario. Tampoco se hallaron dispositivos ALSA ni binarios de captura PulseAudio/PipeWire en el entorno inspeccionado. La ruta de Chromium emplea el selector de compartición propio del navegador, sin micrófono. [FFmpeg y PulseAudio](https://ffmpeg.org/ffmpeg-devices.html#pulse)

## Controles

- Sintaxis de JavaScript y Python comprobadas. La revisión ejecutó cuatro casos sintéticos del capturador, que cubren rechazo de pantalla, rechazo de pestaña sin audio, rechazo de pista terminada y guardado simulado tras recibir ambas pistas.
- Un WebM sintético de cinco segundos con tono entre uno y tres segundos decodificó correctamente y el detector identificó silencio antes y después. Al truncar el mismo WebM, FFmpeg llegó a devolver código cero con error de lectura. Se añadió el control de diagnósticos de FFmpeg y FFprobe. El verificador devuelve código uno para ese archivo.
- La prueba de ASR local acertó las ocho palabras de una frase sintética y devolvió cero segmentos en cuatro segundos de silencio digital. El control de silencio produjo una etiqueta de idioma de baja confianza pese a devolver cero segmentos, por lo que esa etiqueta sola carece de valor probatorio.
- Se intentó entregar a la sesión un WAV sintético mediante la salida de audio de la herramienta. El host respondió que la sesión carece de entrada de audio. La evaluación técnica acredita señal y el ASR permite analizar palabras con incertidumbre. La escucha de voces, música, tono y mezcla sigue pendiente.

## Piloto del 9 de noviembre de 2026

Chromium guardó el WebM mediante el selector de archivos del navegador. Grabación de 11:53:48.785 a 11:54:34.669 UTC. El operador inició el reproductor a 11:54:08.804 UTC en 0:00 y lo pausó a 11:54:29.361 UTC en 0:20. El archivo tiene 1.988.313 bytes, imagen VP8 de 1278×656 y audio Opus mono de 48 kHz. Ambas pistas decodificaron sin errores hasta sus últimos paquetes. El contenedor emitido por MediaRecorder carece de campo de duración; el último paquete de audio termina en 45,845 s.

En el reloj del archivo, el detector marcó silencio hasta 20,136 s y desde 40,950 s hasta el final. La pausa inicial entre 3 y 16 s midió −91,0 dBFS y el intervalo activo entre 22 y 38 s midió −17,2 dBFS de volumen medio. El video activo tuvo 465 paquetes en 20,14–40,58 s y el mayor intervalo entre paquetes fue 0,265 s. Las marcas de imagen estática de dos segundos o más quedaron en los controles de pausa. Un fotograma del tramo activo muestra el diagrama de Excalidraw y al presentador. Los relojes, la imagen y el contraste de niveles vinculan la señal con la reproducción. La prueba abarca el inicio hasta la lectura 0:20 del reloj de YouTube.

El ASR local detectó español sin forzarlo, con probabilidad de idioma 0,920 y cuatro segmentos entre 19,86 y 40,86 s del archivo. La identificación de la pista original proviene de la selección verificada en YouTube. El control de idioma de ASR aporta una comprobación independiente de que la señal contenía habla en español. El WebM, el fotograma y el texto de ASR quedan privados. [Verificación técnica](piloto-verificacion.json) · [Resumen del ASR](piloto-asr-resumen.json)

## Verificación del tramo 1

El primer archivo conserva 0:00–15:10 del reproductor entre dos pausas de control. Incluye tres bloques publicitarios, con ventanas de exclusión de contenido en 125–172, 667–725 y 968–1059 s del WebM. Se acotaron por fotogramas del archivo y relojes visibles. Los intervalos de resguardo son conservadores; tampoco se atribuyen al video los segmentos de ASR que cruzan esos bordes. [Mapa aproximado](tramo1-mapa.json)

El primer intento de verificación integral detectó errores de DTS de la salida de descarte de FFmpeg. El muxer `null` redondeaba los tiempos del video de frecuencia variable. Se conservó el reloj del demuxer con `-fps_mode passthrough -enc_time_base:v demux`. La verificación posterior llegó al final de ambas pistas sin error de entrada o decodificación. Los controles sintéticos íntegro y truncado mantienen sus resultados de aceptación y rechazo. [Recibo técnico](tramo1-verificacion-final.json)

Los paquetes de audio suman 1139,700 s de PCM. Sus tiempos llegan a 1142,550 s, con desfase variable de hasta 2,850 s respecto del PCM concatenado. Faster-whisper trabaja sobre el PCM concatenado. `alinear-asr.py` convierte cada tiempo al PTS de su paquete y aplica los offsets del reloj del reproductor por tramo. El reporte incluye huecos de tiempos de audio de 40 ms o más en las ventanas de contenido. El mayor del primer archivo es de 130 ms. La herramienta de ejecución devolvió 143 antes de que hubiera un JSON de segmentos disponible. El proceso original terminó después y guardó un ASR íntegro, por lo que el 143 del supervisor no acredita que Python se haya detenido. En el intervalo se preparó una ruta de recuperación con checkpoints cortos y cortes en pausas medidas. Se preservan ambos resultados y se usa el ASR del archivo entero como evidencia principal. El guard de exclusión permite distinguir una salida válida del estado devuelto por el supervisor y protege las inferencias largas. [Pruebas del guard](recibo-guard.json) · [Resumen alineado](tramo1-asr-alineado-resumen.json)

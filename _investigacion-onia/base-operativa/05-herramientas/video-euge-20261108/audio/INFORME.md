# Captura y análisis técnico de audio · JuAQILH7dkQ

La reproducción de Chromium alcanzó el reloj terminal 30:02. Se capturó la pestaña de YouTube en dos WebM, con imagen y sonido en el mismo contenedor. La primera captura va de 0:00 a 15:10 y la segunda reanuda el mismo cuadro y reloj hasta 30:02. El operador seleccionó «Spanish (US) original» tras verificar que YouTube había elegido la pista inglesa doblada automáticamente. [Video de Euge Oller](https://www.youtube.com/watch?v=JuAQILH7dkQ)

| Captura | Reloj del video | Imagen | Audio | Verificación |
| --- | --- | --- | --- | --- |
| Piloto | 0:00–0:20 | VP8 1278×656 | Opus mono 48 kHz | Actividad sincronizada con Play y silencio de control antes y después. |
| Tramo 1 | 0:00–15:10 | VP8 1278×598 | Opus mono 48 kHz | Decodificación completa, sin regresiones de PTS ni paquetes sin tiempo. |
| Tramo 2 | 15:10–30:02 | VP8 1278×656 | Opus mono 48 kHz | Decodificación completa, sin regresiones de PTS ni paquetes sin tiempo. |

La cobertura procede de los relojes y de muestras visuales del reproductor y de los archivos. Los dos WebM del recorrido conservan 214.517.056 bytes y quedan privados. El piloto midió −91,0 dBFS durante la pausa y −17,2 dBFS durante la reproducción. El ASR detectó español con probabilidad de idioma 0,920 en el piloto. [Piloto](piloto-verificacion.json) · [Tramo 1](tramo1-verificacion-final.json) · [Tramo 2](tramo2-verificacion.json)

Los tres bloques publicitarios intermedios del primer WebM se separan en sus tiempos 125–172, 667–725 y 968–1059 s. En el segundo se aíslan 187–243 s, 730–912 s y la publicidad posterior al video desde 1149,7 s. Las ventanas se fijaron usando las imágenes de transición y los relojes observados. Los segmentos ASR que atraviesan bordes quedan fuera de la atribución al video. Un fragmento de YouTube mostrado por Euge cerca de 18:51 forma parte de su demostración. [Mapa del tramo 1](tramo1-mapa.json) · [Mapa del tramo 2](tramo2-mapa.json)

El ASR usa faster-whisper small en CPU int8 con dos hilos y pesos ya disponibles. El idioma se detectó como español en ambos archivos, con probabilidad 0,928 y 0,926 respectivamente. De 443 segmentos, se conservaron 379 dentro de las ventanas del contenido y se separaron 64 de publicidad o bordes. El primer archivo aportó 149 segmentos atribuibles y el segundo, 230. El segundo contiene la despedida hasta aproximadamente 30:02. Los tiempos ASR se pasan del PCM concatenado a los PTS por paquete antes de traducirlos al reloj del video. La diferencia final PCM→PTS fue de 2,850 s en el primer archivo y de 0,824 s en el segundo. [Motor ASR](https://github.com/SYSTRAN/faster-whisper) · [Tramo 1 alineado](tramo1-asr-alineado-resumen.json) · [Tramo 2 alineado](tramo2-asr-alineado-resumen.json)

En el contenido del tramo 1 aparecen 24 huecos de PTS de audio de al menos 40 ms. El mayor fue de 130 ms, en el regreso del primer bloque publicitario, y otro de 50 ms aparece aproximadamente en 10:53. En el segundo tramo sólo un hueco dentro del contenido alcanzó ese umbral, de 60 ms alrededor de 16:00,5. La transcripción del primero conserva el hilo de la explicación cerca de ambos puntos. El tramo de unos cinco segundos junto al regreso del primer anuncio contiene una fila ASR de frontera que quedó excluida. Estos huecos limitan lo que puede afirmarse sobre cada muestra de audio. [Tramo 1 alineado](tramo1-asr-alineado-resumen.json) · [Tramo 2 alineado](tramo2-asr-alineado-resumen.json)

## Ruta y límites

El dispositivo PulseAudio de FFmpeg no pudo abrir una fuente disponible en el entorno. El selector de Chromium entregó audio e imagen de la pestaña escogida y un HTML local los guardó mediante MediaRecorder. La solución opera con la sesión y los controles oficiales del navegador, sin captura de micrófono. [FFmpeg y PulseAudio](https://ffmpeg.org/ffmpeg-devices.html#pulse) · [Controles de captura de Chromium](https://developer.chrome.com/docs/web-platform/screen-sharing-controls)

Al verificar el primer WebM de frecuencia variable, el muxer de descarte de FFmpeg redondeó sus DTS. Conservando la base temporal del demuxer, el archivo decodificó completo. El verificador sigue rechazando la regresión de un WebM truncado. [Procedimiento y controles](README.md)

El supervisor de comandos devolvió 143 antes de que dos inferencias dejaran sus JSON. Una consulta desde otro namespace no vio los procesos vivos y se inició una recuperación por ventanas. Las dos inferencias originales terminaron posteriormente. Se conservan las salidas y se emplea el ASR entero como evidencia primaria. El segundo archivo se procesó con un lock privado heredado por el proceso de inferencia y con cotejo del PID por identidad del namespace y tiempo de inicio en el host. La prueba sintética confirma que el lock sigue bloqueando otro lanzamiento si termina el supervisor. [Prueba del guard](recibo-guard.json)

La sesión recibió las imágenes, las métricas del archivo y el texto de ASR. La entrada de audio se probó con un WAV sintético y el host indicó que la sesión carece de soporte. Queda pendiente la escucha directa de voz, música, tono y mezcla. El ASR bruto, los WebM y las capturas permanecen privados.

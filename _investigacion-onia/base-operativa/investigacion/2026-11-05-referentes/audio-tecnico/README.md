# Audio técnico reutilizable · REF-AUDIO-20261105

Resultado técnico: reel y pista recuperados, extracción validada, controles conocidos ejecutados, ASR local completo y selección mínima preparada. **No hay escucha acústica aceptada del agente.** [ESTADO](ESTADO.md) conserva el resultado y la próxima acción; [verificación](verificacion.json) delimita qué pasó.

## Fuente y entregables

Fuente pública de Pedro: [Dd6oC4EkRX1](https://www.instagram.com/pedrobuerbaum/reel/Dd6oC4EkRX1/). Descarga sin cookies ni login mediante yt-dlp 2026.8.19; el primer intento sufrió DNS del sandbox y el intento con red aprobada terminó. No se cambió proxy/TLS. El MP4 nuevo tiene VP9 1080×1920 y AAC 48 kHz estéreo. Su video dura 90,32 s; la pista decodificada tiene 4.336.702 frames/90,347958 s, aunque el contenedor anuncia 90,325 s de audio. Ambas pistas comienzan en t=0. No hubo corte ni estiramiento.

Los binarios están en `C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/audio/`, ignorado por Git. El [manifiesto](manifest.json) contiene procedencia, metadatos, tamaños y SHA-256 de los 18 archivos (45.244.669 bytes), incluidos cuatro controles de video preparados pero no enviados. La nueva representación no coincide en bytes MP4 ni PCM con la conservada en cloud: se preserva esa diferencia, sin presentar hashes históricos como actuales. No se recuperaron los FLAC antiguos; sí su manifiesto textual en Page Video.

- `pedro-original-pcm24.wav`: decodificación completa estéreo sin normalizar; fuente acústica de revisión.
- `pedro-asr-16k.wav`: derivado mono/16 kHz PCM16 para ASR; no reemplaza la mezcla original.
- `pedro-fragmento-01.wav` a `05.wav`: fragmentos PCM32, con las muestras PCM24 originales preservadas. Igualdad de muestras comprobada para los cinco.
- `pedro-seleccion-12s.wav` y `.mp3`: cinco fragmentos de 2 s y cuatro separadores de silencio sintético de 0,5 s. El MP3 es sólo copia de reproducción; los hashes/PCM verificables están en WAV.
- [Resultados ASR sin VAD](asr-resultados.json) y [con VAD](asr-vad-resultados.json): texto y tiempos automáticos, probabilidades, configuración, versión fija de pesos y hashes. No son transcripción humana corregida.
- `probe-a.mp4` a `probe-d.mp4`: regenerados con imagen gris idéntica y AAC 48 kHz, estéreo, objetivo 128 kb/s, 6 s; total 260.081 bytes. [QA nueva](qa-controles-video.json): 26/26 comprobaciones de formato, duración, hashes y señal. Sin normalizar; mono duplicado a L/R con ganancia unitaria, estéreo original preservado. AAC puede variar el bitrate efectivo y las muestras; evaluar sólo los 288.000 frames por canal de [0,6), excluyendo 768 frames de relleno decodificado. Los controles conocidos son tres; el cuarto es una muestra real sin verdad semántica aceptada. No se repitió ASR ni se envió nada fuera.

## Prueba: esperado frente a observado

| Control | Esperado | Observado | Alcance aceptado |
|---|---|---|---|
| Silencio digital 6 s | Cero muestras/ninguna palabra | PCM exactamente cero; ASR vacío con y sin VAD | Extracción y rechazo de ese silencio |
| Seno 440 Hz, amplitud 0,2, 6 s | Pico FFT 440 Hz; RMS ≈0,14142; ninguna palabra | Medidas correctas; ASR sin VAD inventó subtítulos de Amara.org | **ASR sin VAD falla este control** |
| Mismo seno con Silero VAD | No reconocer habla | 0 s aceptados como voz y texto vacío | Rechazo de ese tono; no prueba ausencia universal de alucinaciones |
| 2 s silencio + 2 s tono + 2 s silencio | Límites exactos | Coinciden por muestra | Integridad temporal determinista |
| Voz sintética conocida de Windows, Zira | “This is a controlled audio test. The number is seven.” | Texto equivalente, número escrito 7; 4,514 s | ASR verbal positivo; no voz de Sergio ni clonación |
| Reel real completo | Decodificar y pasar 90,35 s al ASR | Decodificación sin errores; VAD conserva toda la pista, 20 segmentos, 241 unidades de palabra | Borrador verbal con tiempos; no valida mezcla, SFX, prosodia o sincronía labial |

[Controles y medidas](controles-y-medidas.json), [mapa de fragmentos](fragmentos.json), [energía cada 100 ms](energia-100ms.json) y [tramos](tramos-medidos.json) conservan los datos. Las medidas de la pista completa son −14,21 LUFS integrados, LRA 2,60 LU y true peak −0,53 dBFS ([salida de FFmpeg](loudnorm-medicion.txt), valores `input_*`). El archivo original no se normalizó. Estas cifras no describen emoción ni calidad percibida.

## Cobertura y relación con la imagen

La extracción y medidas cubren la pista completa. El ASR recibe 0–90,3479 s y produce palabras hasta 90,20 s; eso no prueba cobertura semántica perfecta. Las divisiones visuales siguientes vienen de la ficha histórica, no de una nueva inspección cuadro a cuadro por Desarrollo.

| Tramo aproximado | Contenido que coincide a nivel temático entre ASR y ficha visual | RMS mono16k |
|---|---|---:|
| 0–3,2 s | Promesa de cinco pasos | −14,67 dBFS |
| 3,2–33,5 s | Avatar y problema específico | −16,76 dBFS |
| 33,5–46,3 s | Escasez real | −16,98 dBFS |
| 46,3–61,7 s | Urgencia | −16,74 dBFS |
| 61,7–73,8 s | Metodología propia | −16,73 dBFS |
| 73,8–90,35 s | Producto principal y bonos | −16,35 dBFS |

No se deduce una palmada de un pico ni una pausa vocal del nivel energético. Hay palabras dudosas en ASR —por ejemplo, el cierre escribe “valor persiguido”— y puntuación unida a través de transiciones; Video debe cotejar subtítulos/voz antes de citar literalmente. No se corrigieron por conjetura las salidas originales.

## Método para otra referencia

1. Partir de su URL pública o archivo autorizado; descargar dentro de la carpeta privada de audio sin credenciales. Registrar URL, fecha, versión de descargador y hash. Conservar fuente y fallos; no reintentar un bloqueo sin cambiar su condición.
2. Verificar con ffprobe y decodificar todo con FFmpeg. Extraer WAV PCM24 estéreo sin normalizar; crear otro WAV mono/16 kHz para ASR. Registrar tiempo de inicio, duración y hash de ambos; no mezclar representaciones sin cotejo.
3. Reutilizar los tres controles PCM y el positivo de voz conocidos. Ejecutar el ASR con `--vad`, usando sólo pesos locales; guardar cada referencia en una subcarpeta propia de evidencia.
4. Revisar texto/tiempos contra material visible y declarar incertidumbres. Para mezcla, efectos y prosodia usar una ruta que reciba audio y pase controles acústicos; en ausencia de ella, preparar fragmentos cortos con una pregunta neutral, conservando el original completo. ASR no cierra ese paso.

Ejemplo desde la raíz del repo, con otro WAV ya recuperado en la misma carpeta privada:

```powershell
python -B _investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audio-tecnico/probar_audio.py asr --vad --media C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/audio --input otra-referencia-asr-16k.wav --language es --model C:/Users/PC/.cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120 --report-dir C:/dev/proyectos/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audio-tecnico/otra-referencia
```

Ese ejemplo no se ejecutó sobre otra referencia. `prepare` genera específicamente los controles y fragmentos de Pedro; `asr --input/--language/--report-dir` permite reutilizar el paso verbal. `cerrar_evidencia.py` valida el paquete de Pedro sin red/modelos. [Faster-whisper](https://github.com/SYSTRAN/faster-whisper) documenta CPU int8 y Silero VAD; [pesos Systran](https://huggingface.co/Systran/faster-whisper-small) son conversión del modelo Whisper small. Aquí se usaron pesos ya existentes de 486.212.372 bytes, CPU/cuatro hilos: 16,828 s para el reel y 20,469 s para la tanda VAD completa. Sin descargas de modelos, instalación, API paga, GPU o VPS; pico RAM y consumo eléctrico no medidos.

## Escucha que falta y fragmento mínimo

El helper nativo de audio rechazó un control real con `audio content omitted because you do not support audio input`; no hay percepción auditiva de este agente. Qwen queda rechazado por el control de silencio histórico; YAMNet/CLAP son candidatos, y **CLAP no reconoció el click de control**, por lo que no acredita sensibilidad a clicks. No se repitieron esos modelos.

La selección de 12 s **no es el reel continuo**: posiciones 0–2/2,5–4,5/5–7/7,5–9,5/10–12 corresponden a originales 2,3–4,3/32,7–34,7/45,5–47,5/60,7–62,7/73–75 s. Son candidatos heredados de la ficha visual, todavía sin verificación visual nueva por Desarrollo. Pregunta neutral: **Son cinco fragmentos separados por medio segundo de silencio. ¿En cuáles distinguís un sonido breve añadido? Respondé por número; si no se distingue, indicá no se distingue.** Esa respuesta sólo resolvería esos fragmentos; prosodia y escucha integral continuarían requiriendo revisión de la pista completa.

Las alternativas de comprensión acústica y su costo/capacidad se registran en [alternativas](alternativas.md). No convertir análisis de escenas o texto en escucha comprobada.

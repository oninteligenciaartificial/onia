# Resolución de reproducción y análisis del video de Euge

9 de noviembre de 2026 UTC · tarea `video-euge-20261108`.

**Se comprobó reproducción de 0:00 a 30:02 en el Chromium existente del VPS y se registraron imagen y audio de la pista original en dos archivos privados.** Un revisor distinto dio veredicto bueno para esa cobertura y el análisis de imágenes muestreadas/ASR aplicado a OnIA. La causa exacta del corte al iniciar Chromium mediante Playwright no quedó aislada; se usó la ruta comprobada del navegador existente.

- [Análisis y propuesta concreta para OnIA](coordinacion/ANALISIS-ONIA.md).
- [Resultado del navegador y costura de 15:10](navegador/RESULTADO.md).
- [Verificación de sonido, ASR y límites](audio/INFORME.md).
- [Dictamen independiente](revision/DICTAMEN.md) y [hashes cotejados](revision/DICTAMEN.json).

## Las tres sesiones

| Sesión nativa | Configuración solicitada | Responsabilidad |
| --- | --- | --- |
| `video_reproduccion` | Sol 6.1 high | Único operador del perfil, controles visibles, pista original, captura y devolución del visor. |
| `video_audio` | Sol 6.1 high | Capturador de pestaña, verificación técnica, ASR local y alineación. |
| `video_revision` | Sol 6.1 ultra | Revisión independiente de archivos, pruebas, imágenes, tiempos y aplicación a OnIA. |

No se abrieron nuevas sesiones CLI del harness, hijos ni servicios. La tarea canónica y la publicación permanecen a cargo del coordinador. El límite de tres cupos principales del harness no se modificó.

## Qué se corrigió y probó

1. Se usó el Chromium humano que ya superaba el corte anterior, con su sandbox y perfil existentes. Se confirmó español original, velocidad normal y el mismo video. La captura oficial de pestaña aportó audio sin necesitar una salida PulseAudio del VPS. El selector eligió sólo YouTube y su audio, nunca micrófono o escritorio completo.
2. Piloto real con pausas: señal durante Play y silencio durante pausa; luego registro de 0:00–15:10 y 15:10–30:02. La costura tiene igualdad de píxeles y relojes; el terminal y la pista se verificaron al devolver el visor. Se separaron cinco bloques de anuncios durante reproducción y otro posterior.
3. El verificador rechaza un WebM truncado aunque FFmpeg devuelva cero. Para el video de frecuencia variable conserva la base temporal del demuxer, evitando un falso fallo del muxer de descarte. Los archivos se decodificaron completos; eso no acredita fidelidad de cada muestra.
4. Se corrigió la atribución de tiempos ASR: el PCM concatenado pierde huecos de PTS. El mapa pasa de PCM a PTS y luego al reloj aproximado del contenido. Quedaron379 filas de contenido y64 excluidas por anuncios o fronteras.
5. Un retorno143 de la herramienta se interpretó erróneamente como fin del worker, y una consulta desde otro namespace no lo vio. Hubo inferencias duplicadas. Se preservaron las salidas y se usa el ASR entero como fuente primaria. El segundo tramo se ejecutó con lock heredado por el hijo, identidad PID/inicio/boot/namespace, heartbeat y validación del JSON. El guard rechazó otro lanzamiento aun después de terminar su supervisor sintético.

Pruebas independientes: controles de selección/rechazo del HTML; clic rechazado tras captura fallida; fixture de archivo íntegro y truncado; alineación de tiempos y publicidad; cinco controles del guard de inferencia; reconstrucción del índice y cotejo de29archivos. No se volvió a reproducir el video por detalles que ya se entendían con la evidencia disponible.

## Uso desde el VPS

No requiere instalar paquetes. Hay que tener el visor existente libre, Chromium con sandbox, FFmpeg y el entorno ASR ya preparado. El controlador es interactivo: un operador inspecciona cada captura antes de enviar acciones. El JSON de una acción no sustituye esa comprobación. [Procedimiento](navegador/PROCEDIMIENTO.md).

```bash
cd ~/repos/onia-coordinador
P=_investigacion-onia/base-operativa/05-herramientas/video-euge-20261108
python3 "$P/navegador/visor-av.py"
```

La página auxiliar está en `audio/capturar-pestana.html`. Desde Chromium se abre como archivo local y se elige la pestaña del video con audio. El guardado usa un destino privado nuevo. Para verificar un archivo ya guardado:

```bash
python3 "$P/audio/verificar-av.py" /ruta/privada/nueva-grabacion.webm
```

La inferencia usa `asr-con-lock.py` delante de `asr-local.py`; el [procedimiento de audio](audio/README.md) describe los argumentos, directorio privado0700, pesos existentes y evidencia de identidad. No reintentar sólo por el estado devuelto por la herramienta: verificar el lock, proceso real y salida antes de lanzar otra inferencia.

## Recursos, conservación y límite del resultado

[Medición del VPS](coordinacion/recursos-v1.json):210muestras entre11:58:13 y12:33:11UTC, CPU mediana55,6%/pico99,7%, memoria disponible mínima8,082GiB. Son métricas del host, no consumo atribuible a cada modelo. El intervalo incluyó el solape de inferencias ya corregido; no justifica subir el límite de sesiones. La sumaRSS de procesos Chromium incluye memoria compartida y no equivale a memoria física exclusiva.

[Cuota fechada](coordinacion/cuota-v1.json):55% usado al inicio de esta tanda y62% a12:52:40UTC, ventana semanal10080min. Es la cuota compartida, no una factura ni una atribución exacta a las tres sesiones.

La inspección visual se apoya en34muestras de reproducción y controles adicionales. Los huecos de audio alcanzan130ms y60ms; existen márgenes de ASR excluidos alrededor de publicidad. **No hubo escucha directa en estas sesiones**, cuya herramienta no admite entrada de audio. Música, entonación y mezcla no se deducen del texto. Tampoco se declara un analizador desatendido para cualquier sitio.

El visor fue devuelto en el final del video, sin captura activa. Medios, capturas de cuenta, ASR bruto y eventos privados quedan fuera de Git. Se preservaron originales y versiones fallidas; no hubo instalaciones, cambios de producción/n8n, envíos, compras ni uso de API de pago. El checkout original sucio se coteja de nuevo antes del cierre Git. El siguiente paso de negocio conserva el ensayo del piloto de workshop por Sergio; ninguna nueva fábrica se activó por este análisis.

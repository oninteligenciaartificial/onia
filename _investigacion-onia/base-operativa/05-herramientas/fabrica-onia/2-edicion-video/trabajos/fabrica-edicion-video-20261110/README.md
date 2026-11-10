# Editor local de fábrica 2

CLI del encargo `fabrica-edicion-video-20261110`. Ejecuta decisiones de un JSON en el VPS con Python, ASR CPU y FFmpeg. Cada ejecución produce una pieza para revisión humana. Contenido decide intervalos y B-roll. Sergio revisa palabras, encuadre, sincronía y sonido.

## Ejecutar

Desde la raíz del repo, con la entrada y el plan en la cola privada del VPS. El directorio padre de salida debe existir y la salida elegida debe ser nueva.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110
PYTHONDONTWRITEBYTECODE=1 python3 "$D/procesar.py" \
  --plan "$HOME/operacion/fabrica/entrada/G01-plan.json" \
  --salida "$HOME/operacion/fabrica/entrada/G01-montaje-01"
```

La resolución predeterminada es 720×1280 a 30 fps. `--ancho 360` produce 360×640 para una prueba breve y `--ancho 1080` produce 1080×1920. Se conserva el encuadre completo con bandas. El ajuste automático de encuadre sigue pendiente de decisión editorial.

`--timeout 600` limita cada proceso ASR/render a diez minutos, con rango de 1 a 3600 segundos. El ASR usa dos hilos CPU, int8, small, español, VAD y beam 5. FFmpeg usa un hilo de filtros y un hilo por códec. Un crudo largo puede necesitar más tiempo que su duración. El límite de tiempo mata el proceso hijo directo. Una interrupción puede dejar una carpeta parcial que debe conservarse y revisarse. Para reintentar, elegir una carpeta nueva.

El retorno 0 y `reporte.json.resultado=renderizada_pendiente_revision` acreditan render y controles instrumentales. Retorno 2 indica rechazo o fallo. Una salida existente se rechaza antes de escribir. Los fallos posteriores a reservar la carpeta dejan `reporte.json` con el error. La pieza de una carpeta fallida o interrumpida requiere revisar su recibo antes de usarla.

## Plan e intervalos

El [esquema JSON](intervalos.schema.json) documenta el contrato. El CLI incluye la validación estructural y temporal mediante stdlib.

```json
{
  "version": 1,
  "tipo": "reel",
  "entrada": "G01.mp4",
  "transcripcion": "G01-texto.json",
  "intervalos": [
    {"start": 0, "end": 4},
    {"start": 7, "end": 10}
  ],
  "broll": [
    {"archivo": "apoyo.mp4", "start": 1, "end": 3, "source_start": 0}
  ]
}
```

- Las rutas son locales, absolutas o relativas al plan. Se admiten MP4, MOV y WebM. El tipo obligatorio es `reel` o `talking_head`. Se rechazan `vlog` y nombres que contengan la etiqueta independiente `vlog`. La clasificación declarada depende del operador.
- `intervalos` selecciona partes de la entrada en segundos desde el inicio de la pista. Son intervalos semiabiertos `[start,end)`, ordenados, positivos y sin solapamiento. Sus extremos se redondean al frame más cercano, con regla de empate de Python. El reporte conserva lo pedido y lo aplicado. Un tramo que desaparece al redondear se rechaza.
- El máximo es 1800 segundos de fuente, 40 cortes y 40 apoyos. Se rechazan pistas de audio/video desfasadas más de un frame. Esos medios necesitan normalización y cotejo humano previo.
- `broll` usa tiempos de la **salida montada**. `source_start` indica desde dónde leer el apoyo. Sus tiempos deben coincidir con la grilla de 30 fps. Los apoyos deben cubrir el intervalo, estar ordenados y carecer de solapamientos. Sustituyen la imagen durante ese tramo, con el audio principal. Una lista vacía omite los apoyos.
- Higgsfield requiere el sí por pieza y una ejecución separada a cargo de su responsable.

## Transcripción y subtítulos

Con `transcripcion`, se reutiliza el JSON del piloto ASR existente. Es obligatorio aportar segmentos no vacíos y ordenados.

```json
{
  "segments": [
    {"start": 0, "end": 4, "text": "Texto cotejado del primer tramo"},
    {"start": 7, "end": 10, "text": "Texto del segundo tramo"}
  ]
}
```

Al omitir `transcripcion`, el CLI invoca `~/asr/venv/bin/python` y `asr_offline.py`. Usa el snapshot small de `~/asr/modelos/models--Systran--faster-whisper-small`, resuelve `refs/main` y comprueba sus cuatro archivos. Las opciones `--asr-python` y `--modelos` permiten señalar otra copia local ya disponible. El trabajador fija modo offline y entrega una ruta concreta al motor con `local_files_only=True`.

Un corte que atraviesa un segmento se rechaza con un recibo de fallo. Contenido debe ajustar los intervalos para contener segmentos completos, o aportar una transcripción temporal del fragmento cotejada. El redondeo a 30 fps también puede requerir ese ajuste. Esta regla conservadora puede devolver piezas con cortes editorialmente válidos para corrección manual.

Los subtítulos usan DejaVu Sans, 36 px en lienzo de referencia 720×1280, dos líneas de hasta 14 caracteres, margen horizontal 72 px y margen inferior 140 px. El estilo escala con la resolución. Se admiten caracteres imprimibles ASCII, Latin-1 y la puntuación `–—…“”‘’€`, junto con espacios y saltos. Las llaves y barras invertidas se rechazan para proteger la geometría ASS. Una palabra larga se divide entre líneas. Se mantienen las palabras con normalización de espacios.

Los grupos de un segmento largo reparten su tiempo uniformemente. El reporte marca `tiempo_interno_estimado`, `subtitulo_rapido` y las señales de incertidumbre del ASR. El cotejo de palabras y de sus tiempos dentro del segmento corresponde a una persona. Una fuente sin audio sólo puede renderizarse con transcripción aportada, y se añade silencio explícito con una duda en el reporte.

## Salidas y circuito existente

La carpeta nueva contiene `pieza.mp4`, `subtitulos.ass`, `subtitulos.json`, `filtros.txt` y `reporte.json`. El modo ASR añade `transcripcion.json`. El reporte guarda hashes de entradas y salida, cortes pedidos/aplicados, B-roll, duración esperada/medida, dimensiones, tiempos separados de ASR y render y dudas. Los hashes se vuelven a cotejar al acabar para detectar cambios en las entradas durante el proceso.

La pieza y sus textos pertenecen a la cola privada que ya define [fábrica 2](../../README.md). Boss conserva el traslado a Sala de montaje y Contenido/Sergio la revisión. Los recibos privados pueden incluir texto del material y deben permanecer con sus medios.

Se reutiliza el contrato `segments` y los ajustes CPU del [piloto ASR](../../../../asr-local/README.md). El script original combina URL, descarga y transcripción en su entrada principal, por lo que esta adaptación usa sus ajustes sobre archivos locales. El patrón de hash por bloques y el control de metadata siguen la [ingesta instrumental existente](../../../../scripts/audiovisual.py).

El [panel existente](../../../../fabrica-contenido/20261109-lector-panel/README.md) sirve para consultar fuentes, ideas y guiones. Su lector tiene un catálogo cerrado de tres tareas y carece de entrada para recibos de montaje. El enlace automático de este recibo al panel requiere otro alcance de rutas. En esta entrega se consulta el reporte junto a la pieza desde la carpeta privada, dentro del circuito de fábrica 2.

## Dependencias y límites observados

Comprobación del 10-11-2026 UTC en este VPS.

| Componente | Observación |
|---|---|
| Python del sistema | 3.12, stdlib para editor y tests |
| FFmpeg / ffprobe | 6.1.1-3ubuntu5 presentes |
| Filtros y códecs | libass, libx264, AAC, scale, pad, fps, trim, concat, overlay disponibles en los tests |
| Fuente | DejaVu Sans resuelta por fontconfig |
| ASR | faster-whisper 1.2.1, CTranslate2 4.8.5, PyAV 18.1.0 importados en el venv existente |
| Modelo | small cacheado y accesible, cuatro archivos presentes |
| Fixture de voz | libflite presente en FFmpeg, usado sólo por los tests |
| Material real | Pendiente de Sergio/Boss |
| Validación editorial y audiovisual real | Pendiente de Contenido/Sergio |

La reproducibilidad byte a byte se comprobó con dos renders en este entorno y entradas idénticas. Cambiar FFmpeg, libass, la fuente o los códecs puede cambiar los bytes. El recibo contiene fecha y tiempo de ejecución, por lo que su contenido varía entre corridas.

Las capacidades de filtros se contrastaron con la documentación de la versión 6.1.1. El trabajador usa la API CPU del motor instalado. [Filtros FFmpeg 6.1.1](https://github.com/FFmpeg/FFmpeg/blob/n6.1.1/doc/filters.texi), [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

## Pruebas breves

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110
PYTHONDONTWRITEBYTECODE=1 python3 "$D/pruebas.py"
```

`--evidencia RUTA.json` escribe un recibo nuevo de los tests. Los fixtures se generan en una carpeta temporal propia bajo este encargo y se retiran al terminar. Los originales de trabajo se conservan.

La suite usa tres segundos de colores conocidos y tonos de 440/660/880 Hz para comprobar dos cortes, duración, frames, dimensiones, audio conservado durante B-roll y hash repetido. También comprueba la resolución predeterminada, JSON inválido, entradas ausentes, rangos, solapamientos, NaN, booleanos, vlog, carpeta ocupada, cortes sobre frases, subtítulos y dependencias ausentes. Renderiza una máscara con texto ancho y mide sus píxeles para comprobar márgenes. Un fixture de seis segundos con voz flite recorre ASR offline y el render por el CLI. Ese fixture acredita ejecución de la cadena con voz sintética. La precisión ASR y la revisión audiovisual de una grabación real quedan pendientes.

La comprobación vigente se conserva en [pruebas-04.json](pruebas-04.json). Los recibos [01](pruebas-01.json), [02](pruebas-02.json) y [03](pruebas-03.json) conservan las comprobaciones previas a ampliar la suite y ajustar el manejo de geometría/confianza. El [recibo de sesión](RECIBO.md) distingue entrega técnica y pendientes de revisión.

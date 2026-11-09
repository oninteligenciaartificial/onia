# Resultado de reproducción y captura

El Chromium del visor reprodujo el video de Euge Oller desde 0:00 hasta el estado terminal 30:02/30:02. La pista «Spanish (US) original» se comprobó antes de la grabación y en el terminal. La velocidad Normal se comprobó al comienzo. El material quedó en dos WebM privados, con cinco bloques publicitarios durante la reproducción y uno al finalizar. [Video de origen](https://www.youtube.com/watch?v=JuAQILH7dkQ)

| Archivo privado | Rango visible de contenido | Inicio y fin de MediaRecorder UTC, 9 de noviembre | Pared | Bytes |
| --- | --- | --- | ---: | ---: |
| `piloto.webm` | 0:00–0:20 | 11:53:48.785–11:54:34.669 | 45.888 s | 1.988.313 |
| `completo.webm` | 0:00–15:10 | 11:57:04.623–12:16:07.305 | 1142.681 s | 103.221.087 |
| `tramo-2.webm` | 15:10–30:02 | 12:18:49.266–12:39:48.525 | 1259.259 s | 111.295.969 |

El nombre `completo.webm` se conserva del primer guardado y corresponde sólo al tramo 1. Las duraciones de pared incluyen márgenes de control, anuncios y la pantalla final. FFprobe identificó VP8 y Opus en ambos tramos. El control de duración, continuidad y señal del audio forma parte de su revisión técnica separada.

Play en el primer tramo quedó registrado a las 11:57:27.250 UTC, la pausa de unión a las 12:15:47.826 y la reanudación a las 12:19:11.867. La misma imagen pausada en 15:10 quedó idéntica píxel a píxel en el recorte del reproductor antes y después del guardado. El terminal 30:02/30:02 se observó a las 12:39:37.366 después de los anuncios finales. El indicador Replay seguía visible al devolver el visor, con la captura detenida y el auxiliar cerrado. El controlador comprobó la identidad del visor al cerrar y liberó el lease a las 12:41:57.810. Una prueba de adquisición exclusiva devolvió código 0.

El recibo contiene 34 observaciones tomadas durante reproducción, además de controles, unión y anuncios. Cada observación corresponde a un fotograma real. La revisión visual se basa en muestras y la señal sonora se analiza mediante decodificación y ASR. Los medios crudos, las imágenes del visor y los diálogos quedan privados.

- [Recibo de navegador](recibo-navegador.json)
- [Procedimiento y versiones](PROCEDIMIENTO.md)

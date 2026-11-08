# Iman · dos piezas recuperadas y cobertura visual/textual

5 de noviembre de 2026, America/Caracas. REF-VIDEO-20261105. **Acceso local resuelto; revisión audiovisual integral todavía no cerrada por audio.** No se hizo reproducción humana continua. Responsable: Video/Iman; audio técnico corresponde a Desarrollo.

**Procedencia.** Iman es el referente pedido. [dpko4jRSIsM](https://www.youtube.com/watch?v=dpko4jRSIsM) era una muestra candidata oficial del corpus, no un enlace que el repo acredite como enviado expresamente por Sergio. Metadatos actuales: canal Iman Gadzhi (`UCQ4FNww3XoNgqIlkBqEAVCg`), título *This is The BEST AI Business to Start In 2026*, subida declarada 2026-01-11, disponibilidad `unlisted`. [N9hkRtP7yzI](https://www.youtube.com/watch?v=N9hkRtP7yzI), *How does Iman stay disciplined*, pertenece a Iman Gadzhi Moments (`UCD2Xhzch7uhW4sWlLyX4XXw`): **oficialidad no corroborada**; no usarlo para atribuir edición al canal oficial.

| Pieza y archivo recuperable | Comprobación real | Cobertura inspeccionada |
|---|---|---|
| [Larga MP4](../../../operacion/referentes-20261105/video/iman/dpko4jRSIsM.mp4) | 239.590.822 bytes; H.264 1280×720/30 fps; video 9.264,200 s, AAC 9.264,251 s. Decodificación completa salida 0. | **310 imágenes:** `t=30k`, k=0…308, más último fotograma 9.264,1667 s; 16 contactos vistos. Lectura de las 4.836 entradas de subtítulos automáticos, 33.943 palabras, desde 0,160 s hasta el final. |
| [Corto MP4](../../../operacion/referentes-20261105/video/iman/N9hkRtP7yzI.mp4) | 1.874.027 bytes; H.264 720×1280/25 fps; video 29,040 s, AAC 29,095 s. Decodificación completa salida 0. | **30 imágenes:** cada segundo de 0 a 29 s; dos contactos vistos. 13 entradas de subtítulos automáticos/69 palabras leídas, 0–29,040 s. |

Los huecos visuales son todos los intervalos entre esas muestras; no se cuentan como vistos los cuadros intermedios. Los textos automáticos contienen errores de nombres y no sustituyen escucha ni certifican palabras literales. La presencia/decodificación de AAC tampoco acredita evaluación acústica.

**Estructura de la larga**, contrastada con ASR y muestras; límites temáticos aproximados, no capítulos oficiales:

| Tramo | Guion/imagen/cierre observado |
|---|---|
| 00:00:00–00:39:30 | Incidencias técnicas declaradas, participación del chat, recursos y promesa; analogías y microcreadores. |
| 00:39:30–01:20:00 | Método: estimación, búsqueda y contacto. Calculadora, perfiles y mensajes; insertos antiguos hacia 01:06:00–01:09:00. |
| 01:20:00–01:40:30 | Producto y secuencia de lanzamiento; diagramas de fases y preguntas de compromiso. |
| 01:40:30–01:58:00 | Contraste manual/IA; documentos y herramientas presentadas. |
| 01:58:00–02:24:00 | Oferta Monetise, herramientas, servicio, certificado y bonos. |
| 02:24:00–02:33:50 | Precio anunciado, CTA a enlace/checkout, garantías y financiación. |
| 02:33:50–02:34:24,200 | Presentación de Jason y comienzo del Q&A; el archivo corta ahí. No contiene el Q&A completo. |

Predominan láminas blancas, énfasis morado/verde y cámara pequeña; aparecen split-screen, B-roll, capturas y clips previos. No hay subtitulado permanente de toda la sesión. Se observan placeholders de cámara en 00:04:30 y alrededor de 01:51:30–02:01:30. La estructura combina enseñanza y venta; capturas/cifras son material presentado, no comprobación de ingresos. El tono verbal es insistente y promocional; no se atribuye prosodia sin escuchar.

**Corto candidato:** 0–4 s muestra al entrevistador; hacia 5 s corta al entrevistado. Primeros planos y subtítulos amarillos que avanzan por fragmentos. El argumento propone eliminar distracciones; termina sin CTA explícito en texto o imagen muestreados. No hay B-roll observado. Esto describe esta edición de Moments, no el estilo general de Iman.

**Audio pendiente por componente:** contenido verbal recuperado por ASR; voz/prosodia, música, SFX, ambiente y silencios no escuchados. Ritmo visual sólo muestreado; sincronía voz/imagen no verificada. Las etiquetas acústicas insertadas por ASR no se aceptan como detecciones. Los medios completos ya están disponibles para REF-AUDIO; no se instaló ni ejecutó un modelo duplicado.

**Acceso probado.** Web devolvió título/estructura básica. CUA no ofreció `iab` ni `chrome`. yt-dlp local existente falló primero DNS en sandbox; lectura y descarga públicas con escalación aprobada funcionaron, sin cookies, login, instalación ni cambio de seguridad. Se seleccionaron formatos `136+140` y subtítulos `en-orig` JSON3. Una descarga válida por pieza; no se sustituyeron por ejemplos.

Evidencia bajo [iman/](../../../operacion/referentes-20261105/video/iman/): logs `yt-dlp*`, `descarga.log`, `N9hkRtP7yzI-descarga.log`; cada carpeta por ID incluye `metadata.json`, `manifest.json` con todos los timestamps, `captions.json`, transcripción, `decodificacion.log`, frames y contactos. [Manifest larga](../../../operacion/referentes-20261105/video/iman/dpko4jRSIsM/manifest.json) · [manifest corto](../../../operacion/referentes-20261105/video/iman/N9hkRtP7yzI/manifest.json).

SHA-256 larga: `a74933b79048a5a46b0ba5b8e23382dca1e5b85522fc47d7d3f46726c78b7270`. Corto: `a8ff662572562735d6f926743a78f32cd9144c3249453ded2c9803475b886903`.

**Siguiente acción concreta:** integrar el contraste acústico con controles de [REF-AUDIO](../../../99-archivo/audio-tecnico/ESTADO.md) usando estas pistas, antes de declarar cobertura integral. El viejo bloqueo de descarga ya no justifica dejar esta pieza sin medio. La revisión de cuadros rápidos/transiciones exactas sigue abierta entre las muestras; el archivo completo permite ampliar cualquier tramo que la revisión señale.

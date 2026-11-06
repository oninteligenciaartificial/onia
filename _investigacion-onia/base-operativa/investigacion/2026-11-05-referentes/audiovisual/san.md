# San — tres piezas secundarias, revisión visual y textual

Fecha: 2026-11-05. Se inspeccionaron **310 posiciones temporales únicas** en 42 hojas de contactos y se leyó el texto completo normalizado de los subtítulos automáticos disponibles. Se incluyeron los tres fotogramas finales. No hubo visionado continuo ni escucha; la cobertura visual es muestreo, no todos los fotogramas del metraje.

Los tres IDs pertenecen al canal **Santiago Munoz**, `UCKH3AEVu7sIU61cjnB0XxdQ`, según la [metadata recuperada por Desarrollo](C:/dev/proyectos/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/recuperacion-secundaria/youtube-metadata.json). Esa coincidencia sostiene la atribución del conjunto «San»; la etiqueta de carpeta por sí sola no la probaría. Son muestras secundarias asignadas para análisis. El repositorio no demuestra que Sergio aportara personalmente cada URL.

| Pieza | Título en metadata / fecha de publicación | Duración de vídeo medida | Medio local ya recuperado |
|---|---|---:|---|
| [A · anrAaNvbp4M](https://www.youtube.com/watch?v=anrAaNvbp4M) | Convertí a Claude en mi editor de videos (nivel 1 vs nivel 3) · 2026-11-01 | 1266.433333 s | [MP4 A](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/secundarios/anrAaNvbp4M/anrAaNvbp4M.mp4) |
| [B · oFYznV9EYPg](https://www.youtube.com/watch?v=oFYznV9EYPg) | Claude Design + Claude Code: mi edición de video que consiguió +1,000,000 vistas · 2026-09-19 | 1268.400000 s | [MP4 B](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/secundarios/oFYznV9EYPg/oFYznV9EYPg.mp4) |
| [C · 4jWLq8Gn_4Y](https://www.youtube.com/watch?v=4jWLq8Gn_4Y) | GPT-6 Astra Acaba de Reemplazar a mi Editor de Videos · 2026-09-09 | 1525.166667 s | [MP4 C](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/secundarios/4jWLq8Gn_4Y/4jWLq8Gn_4Y.mp4) |

Los títulos son afirmaciones del autor, no verificaciones de capacidades, causalidad de visitas o sustitución de profesionales. No se volvió a descargar ningún medio. Son H.264, 1280×720, 30 fps, con Opus estéreo. Las duraciones de contenedor son 1266.454, 1268.414 y 1525.234 s. La decodificación completa y los SHA-256 se toman expresamente de la QA de Desarrollo; aquí se cotejaron tamaños y se extrajeron muestras. El [manifiesto visual](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/manifest.json) conserva procedencia de hashes, índices de fotograma, tiempos, rutas y alcance de inspección.

## Cobertura comprobable

| Pieza | Muestras globales cada 20 s + último fotograma | Refuerzo cada 5 s, extremos incluidos | Nuevas / reutilizadas del global | Posiciones únicas inspeccionadas |
|---|---|---|---:|---:|
| A | 64 entre 00:00–21:00 + final 21:06.400 | 11:35–12:15; 14:50–15:50; 18:30–19:50; 20:30–21:05 | 36 / 11 | 101 |
| B | 64 entre 00:00–21:00 + final 21:08.367 | 10:40–11:40; 18:00–19:50; 20:30–21:05 | 32 / 12 | 97 |
| C | 77 entre 00:00–25:20 + final 25:25.133 | 21:20–24:25; 24:40–25:20 | 34 / 13 | 112 |

Son 208 muestras globales, incluidos los finales, más 102 nuevas de detalle. Las 36 posiciones reutilizadas no se cuentan dos veces. Los tiempos globales proceden del índice de fotograma dividido por 30; los detalles se etiquetan por el tiempo solicitado a `ffmpeg -ss`, sin un registro independiente de PTS. Quedan intervalos sin inspección entre muestras: hasta 20 s en el recorrido global y 5 s dentro de los refuerzos. Una imagen repetida por una pausa del reproductor sigue siendo una posición temporal distinta, no un plano nuevo.

| Pieza | Cues automáticos / no vacíos | Palabras tras quitar solapamientos de captions | Primer cue no vacío → último final declarado | Unión temporal no vacía, recortada al vídeo |
|---|---:|---:|---|---:|
| A | 1115 / 1114 | 3776 | 1.390 → 1268.305 s | 1265.043333 s · 99.890243% |
| B | 1057 / 1050 | 3574 | 2.550 → 1270.400 s | 1259.331000 s · 99.285005% |
| C | 1271 / 1268 | 4363 | 2.389 → 1526.720 s | 1520.697667 s · 99.706983% |

Se leyó la totalidad de los textos derivados [A](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/anrAaNvbp4M/captions-lectura.txt), [B](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/oFYznV9EYPg/captions-lectura.txt) y [C](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/4jWLq8Gn_4Y/captions-lectura.txt): 11 713 palabras normalizadas de 3443 cues de `es-orig`. Las copias `es` no se suman. No hay subtítulos manuales en la metadata. El algoritmo elimina coincidencias consecutivas de hasta 80 palabras; no corrige errores como «Cloud» por «Claude». La unión temporal mide presencia de cues, **no porcentaje de discurso correctamente transcrito**. Los finales declarados exceden ligeramente la pista de vídeo; se conserva ese desfase. Cálculos y huecos constan en los manifiestos y el [resumen de cobertura](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/qa-cobertura.json).

## A — comparación de tres niveles

**Guion según captions:** promesa inicial de tres grados de edición; presentación del vídeo bruto; explicación de herramientas y subtítulos; instrucciones y correcciones de cada nivel; demostración del resultado; conservación del estilo en una skill; cierre de comunidad y suscripción. Las comparaciones se apoyan en el mismo material de partida y hacen visible la diferencia entre variantes.

**Imagen y edición observadas:** alterna presentador con micrófono, captura de escritorio con su rostro superpuesto, diagramas crema y resultados verticales dentro del vídeo horizontal. En 11:35–12:15, el primer resultado conserva al hablante como centro, con título y captions pequeños blancos/amarillos. El reproductor se adelanta manualmente: este tramo no acredita reproducción continua íntegra del resultado. En 14:50–15:50, el segundo usa fondo crema, rostro en ventana, palabras grandes, barra superior e iconos. En 18:30–19:50, el tercero añade recorte de silueta, un gran numeral, fondo oscuro ámbar y material de apoyo. Los captions posteriores reconocen que el color quedó demasiado saturado; no se presenta aquí como acabado sin correcciones. [Detalle del tercer resultado](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/anrAaNvbp4M/detalle/hoja-04.jpg).

**Cierre:** 20:30–21:05 combina presentador, referencia a guardar el estilo, marca/comunidad, placa de suscripción y comentarios. El [último fotograma, 21:06.400](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/anrAaNvbp4M/frames/0065.jpg), es negro. El CTA del tutorial se distingue del CTA de perfil que aparece dentro del reel demostrado.

## B — elegir el diseño antes de terminar la edición

**Guion según captions:** parte de la objeción de que una edición con IA parezca artificial; presenta dos métodos; analiza el bruto; plantea diez estilos con intensidades mínima y máxima; filtra favoritos y nuevas variantes; combina el estilo elegido con el montaje; revisa errores y propone guardar el resultado como skill. La afirmación de un millón de visitas queda atribuida al autor.

**Imagen y edición observadas:** escritorio y rostro superpuesto dominan el tutorial; los diagramas a mano aclaran el procedimiento. Entre 10:40–11:40 se ven pares comparables: rostro más teléfono, tipografía amarilla grande, composición editorial, notificaciones, burbujas y collage. La elección conserva una relación visual clara entre persona e interfaz. El resultado de Forja Inbox aparece alrededor de 18:00–19:50: vídeo vertical sobre negro, captions blancos con palabras amarillas, cambios entre rostro completo y rostro sobre pantalla de teléfono, recorte de silueta, iconos y elementos de conversación. [Comparaciones y entrada al resultado](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/oFYznV9EYPg/detalle/hoja-02.jpg).

**Desfase de navegación:** el capítulo de metadata «Resultado» empieza en 14:30; las muestras allí siguen mostrando referencias y preparación. La vista previa se observa desde 18:05 y ampliada a 18:10. Se usan tiempos del archivo, no esos capítulos, para localizar evidencia.

**Cierre:** el anuncio interno termina hacia 19:50 con «Comenta FORJA». Después vuelve al escritorio, comenta correcciones y remite a comunidad/producto. En el [final 21:08.367](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/oFYznV9EYPg/frames/0065.jpg) siguen visibles el espacio de trabajo y el presentador; no hay una placa final separada. El tutorial contiene así una demostración que también funciona como anuncio de su producto.

## C — proceso en un editor y dos ejemplos desarrollados

**Guion según captions:** propone cuatro entregables a partir de locuciones y material de apoyo; explica preparación y conexión al editor; muestra ejecución y correcciones; presenta tiempo/consumo que afirma haber obtenido; enseña resultados; ofrece una skill y acceso a su comunidad. Los captions incluyen una corrección explícita de una imagen con texto poco legible, de modo que no sostienen un proceso sin intervención.

**Imagen y edición observadas:** comienza con presentador, gráficos breves y pantallas; alterna mapa de trabajo, instrucciones y líneas de tiempo. Entre 16:40–17:40 se observa la imagen cuestionada y luego una propuesta ilustrada diferente. Desde 18:20 aparecen tomas de teléfono del ordenador con agente y editor lado a lado; las muestras muestran estados distintos de la línea de tiempo, sin permitir medir la velocidad real de trabajo. En 21:20–22:25 y 23:20–24:25 se desarrollan dos reels de una capacitación: verticales sobre negro con reacción del creador en una ventana, planos reales de sala, alumnos y expositor, captions blancos/amarillos, gráficos puntuales y zonas desenfocadas. El primer final queda sostenido mientras continúa el comentario del tutorial. [Primer ejemplo](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/4jWLq8Gn_4Y/detalle/hoja-01.jpg).

El vídeo muestra ventanas y declara cuatro archivos terminados, pero presenta **dos ejemplos desarrollados** en este tramo; no se afirma haber revisado los cuatro entregables. Los desenfoques son visibles; su aplicación automática es una atribución del narrador que esta revisión no valida. Tampoco se verificaron las afirmaciones de tiempo, consumo o sustitución del editor.

**Cierre:** los reels piden comentar «APRENDER»; desde aproximadamente 24:45 regresa el presentador a pantalla completa, muestra la portada de la skill y añade el texto de invitación a la comunidad. El [final 25:25.133](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/san/4jWLq8Gn_4Y/frames/0078.jpg) mantiene al presentador despidiéndose.

## Salida editorial y límites

Las referencias permiten estudiar tres decisiones concretas: comparar niveles sobre un mismo bruto; elegir composiciones visibles antes de renderizar todo; y mostrar resultado, crítica y corrección como parte de la demostración. En los ejemplos observados, los captions mantienen una jerarquía sencilla y el rostro cambia de tamaño o posición para dar espacio a la información. Los tutoriales alternan explicación, proceso y prueba, con llamadas comerciales tanto dentro de los ejemplos como en el cierre.

El muestreo no certifica todos los cortes, transiciones, animaciones ni continuidad del guion hablado. Sin escucha no se evalúan voz, música, efectos, mezcla o sincronización labial. No se ejecutaron instrucciones del autor, APIs o modelos; las menciones técnicas describen el contenido. Los medios locales quedan disponibles para el frente de audio, separado de esta revisión. No se modificaron sus fuentes, manifiestos de Desarrollo ni estados compartidos.

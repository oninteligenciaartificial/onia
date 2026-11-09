# Referencia visual de Euge Oller · 9 de noviembre de 2026 UTC

La prueba nocturna reprodujo el inicio del video en el VPS y tomó muestras visuales. El mejor avance nocturno fue 00:44.384 sobre 30:02.921. El fotograma más tardío que se pudo inspeccionar, de la tanda previa, está en 00:50.5. El visionado completo queda en espera. Las pruebas conservaron fotogramas puntuales y no produjeron evidencia sonora. [Video fuente](https://www.youtube.com/watch?v=JuAQILH7dkQ)

## Qué se vio

| Tiempo de reproducción | Observación |
| --- | --- |
| 00:00.821 y 00:01.098 | Esquema del agente de IA con conexiones a ordenador virtual, Clonify, Calendar, Gmail, Buffer y Fábricas. |
| 00:25.266 y 00:25.683 | El panel Fábricas de Euge dispone cada flujo en entrada, fábrica, revisión y destino. Canal Euge muestra revisión y publicación humanas. Shorts muestra revisión y un destino Buffer. Leader Summaries aparece como flujo de horario propio. |
| 00:50.5 | El panel Productos de Clonify muestra una etapa comercial separada del panel de producción. |

El patrón transferible a ONIA es una fila por flujo con entrada explícita, responsable de producción, punto de revisión y destino. Para la primera fábrica de ONIA, la aprobación y publicación humanas pueden representarse como dos estados separados.

## Qué falló y qué se sabe

| Inicio UTC | Condición | Resultado |
| --- | --- | --- |
| 04:22:02 | Reproducción secuencial sin saltos, espera de publicidad de 120 s | Publicidad activa al terminar, 0 imágenes. |
| 04:25:21 | Reproducción secuencial con espera publicitaria condicionada al avance del reloj | 2 imágenes en 1.098 y 25.266 s, avance máximo 44.384 s. El medio quedó vacío y pausado. |
| 04:30:05 | Botón Play visible de YouTube, una recuperación acotada y contadores saneados de red | Se observaron 42.715 s de espera desde la detección del anuncio hasta su desaparición. 2 imágenes en 0.821 y 25.683 s, avance máximo 44.114 s. El medio volvió a quedar vacío y pausado. La recuperación no restituyó el avance. De 30 respuestas observadas del CDN googlevideo.com, 6 devolvieron HTTP 403; no se registró el tipo o segmento exacto. |

El salto a 03:00 falló en la tanda previa, pero los dos cortes nocturnos ocurrieron sin ejecutar saltos. El estado final del último intento fue `readyState=0`, `networkState=0`, sin error del elemento, sin publicidad y con el mismo ID. Los 403 confirman que hubo respuestas rechazadas del CDN multimedia. No permiten determinar el motivo del rechazo ni atribuirle por sí solos el reinicio del elemento. El lanzador mantuvo el sandbox y no interceptó el tráfico del video real. [Estados del elemento multimedia en HTML](https://html.spec.whatwg.org/multipage/media.html#ready-states)

El visor volvió a `listo` con Chromium humano y se verificó que Xvfb, VNC y Web conservaron sus procesos. Los PNG y perfiles permanecen privados. Si el visionado se retoma, queda la reproducción humana en el visor o una copia audiovisual autorizada.

## Reproducción de las pruebas

La prueba local usa FFmpeg y Xvfb ya instalados, genera un WebM de publicidad y otro de contenido en `/tmp`, y abre un perfil sintético con Chromium sandbox. La prueba de navegador intercepta el destino para servir únicamente los datos sintéticos. Las pruebas de lógica cubren publicidad con avance y detenida, una única recuperación y contadores 403 sin URL. No abre el video real ni el perfil de trabajo.

```bash
python3 -B _investigacion-onia/base-operativa/05-herramientas/video-euge-20261108/nocturno-20261109/probar.py
```

Para una publicación técnica conviene incluir `ejecutar.py`, `reproduccion.cjs` y las tres pruebas, junto con la clasificación de destino. El capturador actual importa `classifyDestination` y `URL` de `muestra-seek-anterior.cjs`. Puede publicarse ese archivo como dependencia o extraer el guard compartido al integrar. El lanzador depende del gestor `browser-vps.py` del checkout coordinador, del visor existente y del runtime Playwright/Chromium 1252 ya instalado en el VPS. Las versiones `reproduccion.antes-reloj-publicidad.cjs` y `reproduccion.antes-play-normal.cjs` se conservan como antecedentes. El recibo JSON incluye hashes y rutas privadas de los manifiestos para cotejo local.

Las correcciones posteriores y sus pruebas están en [INTEGRACION](INTEGRACION.md). El recibo histórico conserva hashes de los scripts usados en los intentos reales; los archivos actuales fueron corregidos y sólo se reensayaron con material sintético.

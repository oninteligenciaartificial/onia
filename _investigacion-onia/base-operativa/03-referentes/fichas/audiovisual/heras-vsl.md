# Heras — VSL vigente en viralidad.com

**Actualización bajo GOAL integral:** [ASR complementario de ambas variantes](guiones-faltantes.md) completado y leído, con errores de nombres/cifras preservados. Aporta la secuencia verbal automática que faltaba; no certifica palabras ni escucha. [84 cuadros dirigidos de V1](../../../99-archivo/versiones-superadas/heras-refuerzo-v2.md) amplían CTA, agenda, formulario y calificación. Permanecen límites de muestreo, acústica y equivalencia con la variante histórica.

Fecha: 2026-11-05. REF-VIDEO-20261105. Referente: Víctor Heras. Fuente señalada: [viralidad.com](https://viralidad.com/), conservada en `continuidad/2026-11-04/fuentes-cloud/referentes.md`. Esto identifica una pieza investigada; no demuestra que Sergio enviara personalmente cada URL. La candidata de YouTube `GbavuA_jqmw` se documenta aparte y no sustituye esta VSL.

## Resultado y cobertura real

El sitio vigente entrega un experimento A/B con dos variantes al 50 %. Ambas se recuperaron completas desde su HLS público, sin cuenta, gasto ni elusión de controles. La configuración las llama `VSL JET V1.mov` y `VSL JET V2.mov`. No hay prueba de cuál se mostró el 4 de noviembre ni de identidad binaria con las tres capturas antiguas. Aquellos 2/12/22 segundos eran esperas, no tiempos certificados de la pieza.

| Pieza | Archivo recuperado | Duración del contenedor | Imagen inspeccionada |
|---|---|---:|---|
| VSL V1 | `heras-vsl-v1-720p.mp4` | 637.589333 s | 128 muestras a paso nominal 5 s, 0–635 s; muestra adicional solicitada a 637.45 s |
| VSL V2 | `heras-vsl-v2-720p.mp4` | 637.141333 s | 128 muestras a paso nominal 5 s, 0–635 s; muestra adicional solicitada a 637.00 s |

Se abrieron e inspeccionaron las 16 hojas de contactos de cada variante y las dos imágenes finales: 258 imágenes en total. Es muestreo temporal que recorre ambas piezas; no visionado continuo, ni inspección de cada transición, ni escucha. La rejilla procede de `fps=1/5:round=up`; los rótulos son tiempos nominales, no una lista de PTS certificados. Cada hueco de unos cinco segundos puede contener cortes o textos no observados.

Ambos archivos: H.264, 1280×720, 30000/1001 fps, pista AAC. `ffprobe` identifica los streams y una decodificación completa con `ffmpeg -v error -xerror -map 0 -f null -` terminó con código 0 en ambos. Procesar todos los frames no significa haberlos visto. La pista existe, pero no se escuchó ni se transcribió. La configuración pública indica subtítulos desactivados y no se recuperó un guion verbal completo.

## Mapa visual de las dos variantes

Los intervalos son agrupaciones de muestras, no límites exactos de escenas. Los resultados e ingresos mostrados son afirmaciones publicitarias del emisor, sin verificación independiente.

| Tiempo nominal | Evidencia visual y función |
|---|---|
| 0–25 s | Presentador en cabina de avión, camisa clara, micrófono y mirada a cámara. V1 intercala cifra económica y mosaico de materiales; V2 trabaja objeciones de algoritmo/cuenta/nicho con iconos. Son aperturas distintas. La escenografía no acredita propiedad del avión ni patrimonio. |
| 30–70 s | Perfiles alrededor de una marca, cuentas estancadas, reels con pocas vistas, anuncios y ejemplos de resultados/pagos. Alternancia entre rostro, capturas y gráficos de prueba. |
| 75–135 s | Preguntas y negaciones visuales, ejemplos de contenido, clips verticales y cuenta antes/después. V1 y V2 no muestran siempre el mismo plano en la misma muestra. |
| 140–240 s | Organización en tres pilares; Stories/Reels, acrónimo RUM, porcentajes y perfiles antes/después. Tramos de presentación directa entre pruebas e ilustraciones. |
| 245–320 s | Segundo pilar, engranaje/sistema orgánico y escalera de niveles de conciencia; luego reels, euros y tres vías Stories/Reel/DM. Entre 265–300 s predominan muestras del presentador. |
| 325–445 s | Nuevos perfiles, cifras y pagos; lista de complejidades rechazadas sobre negro, ejemplos de nichos, regreso a pilares y cuentas. La reiteración distribuye la prueba a lo largo de la pieza. |
| 450–475 s | Mosaico de videollamadas, tres iconos, CTA gráfico para agendar consultoría alrededor de 460 s y formulario alrededor de 465 s; regreso al presentador. No se envió formulario. |
| 480–600 s | Secuencia extensa de sectores/casos: salud, construcción, desarrollo personal, trading, relaciones, inversiones, oficios, crédito, comunicación, ropa, ventas, espiritualidad, medicina, inmobiliario y finanzas. Algunas muestras desplazadas entre versiones. |
| 605–final | Presentador, videollamada insertada, CTA alrededor de 620 s, mensaje de compromiso cerca de 630 s; V1 oscurece a 635 s y V2 ya muestra negro. Las imágenes adicionales cercanas al final son negras en ambas. Esto describe el cierre visual, no sus últimas palabras ni sonido. |

## Lenguaje audiovisual que sí puede sostenerse

La cámara del presentador funciona como base reconocible. La edición la interrumpe con composiciones oscuras, perfiles recortados, números, carruseles de reels y testimonios en ventanas. Predominan letras blancas y rojo para negaciones o énfasis; el gesto de manos y cambios de escala sostienen la presentación. La prueba visual reaparece después de cada explicación y vuelve antes del CTA. En las muestras no se identificó un precio de compra; la acción visible es la consultoría.

Transferible a una producción propia: presentador estable, un esquema numerado, ejemplos legibles asociados a cada afirmación, prueba distribuida y CTA representado visualmente en dos momentos. No trasladar las cifras, testimonios o autoridad escenográfica de este vendedor a ONIA. No se puede valorar todavía música, timbre, velocidad oral, pausas, mezcla, efectos, sincronía, ritmo continuo ni eficacia comercial. Los rótulos quemados son texto parcial; no equivalen al guion hablado.

## Acceso y evidencia reproducible

Se probaron: web público (accesible); navegador CUA (Chrome no disponible y ninguna superficie de navegador en el inventario); Python en sandbox (fallo DNS); lectura de red autorizada sin cabecera de navegador (HTTP 403); lectura pública con User-Agent de navegador (HTTP 200); extractor genérico yt-dlp (URL no soportada). El camino que funcionó fue HTML público → JS del reproductor VTurb → manifiestos HLS → ffmpeg. No se reprodujo la pieza en navegador.

El [JS A/B público](https://scripts.converteai.net/7999d283-8b2c-4b68-8e10-b8ee1bcf16f0/ab-test/6ac3be87b138342855146ac4/player.js) identifica ambos videos; la biblioteca pública define cómo construir sus rutas. Configuración `secure:false`, `drm:false`, subtítulos inactivos y barra de progreso no lineal (`fakeBar.active:true`): la barra no sirve para certificar tiempos. Manifiestos: [V1](https://cdn.converteai.net/7999d283-8b2c-4b68-8e10-b8ee1bcf16f0/6ac3bbf9e3eaa635739e0dd2/main.m3u8), [V2](https://cdn.converteai.net/7999d283-8b2c-4b68-8e10-b8ee1bcf16f0/6ac3bc68c7fd24a4a01ea07b/main.m3u8). Se copió el stream de mayor resolución disponible, sin recodificar; el 1920×1080 del objeto de configuración no describe la resolución descargada.

Directorio de todos los auxiliares: `C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/heras/`. Incluye `landing.html`, `player.js`, `smartplayer.js`, manifiestos, `inventario.json`, `v1-metadata.json`, `v2-metadata.json`, logs de descarga/decodificación, `v1-frames-5s/`, `v2-frames-5s/`, `v1-contactos/`, `v2-contactos/` y las imágenes terminales. No se modificaron estados compartidos.

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| V1 MP4 | 66586311 | `aaa69d980dce383cdf796d9208fadfbfd6d790077967aab881e26c170a27b917` |
| V2 MP4 | 66279025 | `44660459b25bd00c30aa805d579afd07cb4dc990001eea25fc73ce25bde5d867` |

Entrega para revisión sonora: [V1 completa](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/heras/heras-vsl-v1-720p.mp4) y [V2 completa](C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/video/heras/heras-vsl-v2-720p.mp4). Rangos útiles: apertura 0–30 s, primera invitación 450–475 s y cierre 605–final. El frente de audio técnico corresponde a Desarrollo; aquí no se ejecutó ningún modelo ni se reintentó la modalidad nativa ya rechazada. Pendiente concreto: escuchar esas pistas para completar voz/música/mezcla y guion íntegro antes de elevar una conclusión audiovisual plena.

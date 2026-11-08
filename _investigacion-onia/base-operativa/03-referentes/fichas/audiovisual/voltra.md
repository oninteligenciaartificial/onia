# REF-VIDEO-20261105 · Voltra · una muestra oficial de tienda

**Estado vigente del5/11:** unidad visual/verbal aceptada con límites porJefa; [texto y tiempos complementarios](guiones-faltantes.md), [cierre finito de componentes](pendientes-visuales-finitos.md) y [corpus actual](corpus-requerido.md). Las afirmaciones de no disponer deASR en el corte inicial siguiente son históricas; no indican cola activa.

5/11/2026. Se inspeccionó **únicamente el primer video del carrusel de la ficha propia de Aspiradora Black Edition**, asset `a081891a8e224825ac38370d1b22d62c`. Es una muestra comercial elegida por el equipo para la empresa referente; no se presenta como pieza enviada expresamente por Sergio. **108 imágenes revisadas cada 0,2 s, incluido el último fotograma; sin reproducción continua ni escucha.**

## Procedencia y alcance

Cadena cotejada en el HTML local: [ficha oficial](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition) → sección `shopify-section-template--20317438410812__image_slider_YEFPbi` (línea 9233) → primer video del carrusel → `<source data-src>` MP4 (línea 9426) → [asset de la tienda](https://voltra.com.ar/cdn/shop/videos/c/vp/a081891a8e224825ac38370d1b22d62c/a081891a8e224825ac38370d1b22d62c.HD-1080p-7.2Mbps-64052188.mp4?v=0). Numeración de líneas obtenida con `rg -n` sobre el snapshot conservado.

Esto acredita publicación comercial por **Voltra Argentina en su tienda**. No identifica a la creadora original ni a la persona que aparece; tampoco demuestra anuncio activo, publicación en Instagram o autenticidad de un testimonio de cliente. No se investigó otro video del carrusel ni se reutilizó el candidato inaccesible de Mercado Libre.

El medio ya recuperado por la subtarea de procedencia se leyó sin modificarlo. Su SHA-256 se volvió a calcular y coincide con `reel-identidad/voltra/sample-manifest.json`. El historial de HTTP 200 y decodificación completa previa está en `reel-identidad/voltra/README.md`; esta revisión añade observación visual.

## Secuencia, guion visual y cierre

Los tiempos son localizadores del muestreo, no puntos de corte certificados. El contenido textual procede de subtítulos quemados leídos en imagen, no de voz escuchada.

| Tiempo | Evidencia observada |
|---|---|
| 0–2,0 s | Presentadora sentada, producto en primer plano y marca visible; texto anuncia llegada del producto |
| 2,2–6,2 s | Cambio de vestuario; promesa de ahorrar tiempo, manejo del aparato y acercamiento de la boquilla a cámara |
| 6,4–8,8 s | Texto enumera tamaño, carga USB y potencia; el producto permanece visible |
| 9,0–12,0 s | Se muestra un teléfono suspendido bajo el aparato y después cabello en movimiento; texto presenta aspiración/soplado |
| 12,2–15,0 s | Acercamientos al sillón con residuos y aparato sobre la superficie; rótulos enumeran también casa, auto y teclado, aunque esas otras superficies no se muestran en las muestras |
| 15,2–18,2 s | Vuelve la presentadora con el producto; texto invita a conseguirlo en la web de Voltra |
| 18,4–21,4 s | Cierre con producto, presentadora, financiación y envío; último fotograma mantiene la escena y el subtítulo de alcance nacional |

**Montaje:** vertical, alternancia de presentación y demostración, planos más cercanos para producto/superficie, subtítulos amarillos con borde oscuro; financiación y envío reciben texto verde. Los cambios de vestuario/encuadre evidencian montaje. **Estructura:** novedad → beneficio → atributos → ejemplos visuales → destino de compra → condiciones. No se contó cada corte ni se certificó sincronía.

El video anuncia **3 cuotas sin interés** y envío gratuito nacional; son condiciones escritas en esta pieza, no confirmación de vigencia en checkout. El ahorro de tiempo y la potencia son afirmaciones comerciales: la secuencia mostrada no es una medición independiente. La invitación al sitio se identifica en imagen; no se declara escuchada.

## Cobertura y archivos

Fuente intacta:
`operacion/referentes-20261105/reel-identidad/voltra/voltra-black-edition-carousel-01-a081891a8e224825ac38370d1b22d62c.mp4`

- **19.904.755 bytes**; SHA-256 `365c663ab8880602091c8e50f485421eaf462cd3461b298e0891e21c8f012d48`.
- Contenedor **21,461333 s**; video H.264, **606×1080**, 30 FPS, 643 fotogramas; audio AAC estéreo, 48 kHz. La denominación 1080p del archivo no convierte su ancho real en 1080 píxeles.
- Muestreo cada seis fotogramas: índices **0, 6, …, 642**, tiempos nominales **0–21,4 s**, **108 imágenes únicas**. El índice 642 es el último fotograma del video; está incluido, sin sumarlo dos veces.
- Derivados propios: `operacion/referentes-20261105/video/voltra/manifest.json`, `ffprobe.json`, `sample.py`, `frame-0001.jpg`–`frame-0108.jpg` y `contact-01.jpg`–`contact-06.jpg`. Los seis contactos fueron inspeccionados.

El archivo contiene audio aunque el reproductor web use `muted`. No se comprobó voz, prosodia, velocidad verbal, pausas, música, SFX, ruido del aparato, mezcla ni sincronía; el movimiento del cabello no acredita un sonido. No se recuperó una transcripción independiente ni se aplicó OCR/ASR. Los intervalos de 0,2 s dejan fotogramas sin inspeccionar: la decodificación completa es una comprobación técnica, no visionado continuo.

**Resultado y siguiente paso:** muestra oficial disponible y cobertura visual documentada. Para completar sonido hace falta revisión auditiva del mismo MP4; para certificar todos los cortes, reproducción visual continua. No falta descarga ni acceso de cuenta. Como práctica propia, puede ensayarse una demostración con acción visible y una CTA coherente con su destino, manteniendo separadas las observaciones de las promesas; no se atribuye esa práctica ni aprendizaje a Sergio.

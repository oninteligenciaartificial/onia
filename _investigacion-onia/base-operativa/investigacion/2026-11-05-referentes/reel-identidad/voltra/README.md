# Voltra · muestra audiovisual desde la tienda propia

5 de noviembre de 2026, America/Caracas. Recuperación pública acotada para Jefa v2. **Medio recuperado y decodificado; sin visionado ni escucha en esta subtarea.**

## Procedencia verificada

La [ficha propia de Aspiradora Black Edition](https://voltra.com.ar/products/aspiradora-inalambrica-voltra%C2%AE-3-en-1-black-edition) respondió HTTP 200. Su HTML incluye un carrusel de videos de producto; se eligió **el primer video de ese carrusel**, una muestra comercial finita y directamente vinculada a la ficha estudiada.

Cadena conservada:

1. HTML de la ficha: 649.227 bytes; SHA-256 `ee0a587a33915f7da03a96042c5bc6b8df767b636d91b857379dbc38fadbf3bf`.
2. Sección `shopify-section-template--20317438410812__image_slider_YEFPbi`, desde la línea 9233 del snapshot; título del carrusel en líneas 9313–9318.
3. Primer `<video>` en línea 9405; `<source data-src>` MP4 en línea 9426, identificador `a081891a8e224825ac38370d1b22d62c`.
4. [Asset MP4 de la tienda](https://voltra.com.ar/cdn/shop/videos/c/vp/a081891a8e224825ac38370d1b22d62c/a081891a8e224825ac38370d1b22d62c.HD-1080p-7.2Mbps-64052188.mp4?v=0), recuperado con HTTP 200 y `Content-Type: video/mp4`.

Esto demuestra **publicación comercial del video en la tienda Voltra Argentina**. No identifica al creador original, no prueba que sea un anuncio activo y no acredita que se haya publicado en `@voltra.ar`. No depende del clip de Mercado Libre ni de cuentas homónimas.

## Archivo y pruebas

Medio local:
`C:/dev/proyectos/_investigacion-onia/base-operativa/operacion/referentes-20261105/reel-identidad/voltra/voltra-black-edition-carousel-01-a081891a8e224825ac38370d1b22d62c.mp4`

- Tamaño: 19.904.755 bytes.
- SHA-256: `365c663ab8880602091c8e50f485421eaf462cd3461b298e0891e21c8f012d48`.
- Video real: H.264, **606×1080**, 30 fps; 21,433333 s.
- Audio: AAC estéreo, 48 kHz; 21,461333 s. Contenedor: 21,461333 s.
- FFprobe identificó ambos streams; FFmpeg decodificó el archivo completo a salida nula, exit code 0 y sin errores.
- El atributo HTML `muted` es una configuración del reproductor: **el archivo sí contiene pista de audio**. No demuestra qué se oye.

La fuente completa `product-page.html` queda junto al MP4, fuera de Git. [page-media.json](page-media.json) conserva etiquetas/URLs/posiciones; [sample-manifest.json](sample-manifest.json) conserva relación fuente→asset, hashes y pruebas. Los scripts de esta carpeta reproducen sólo la lectura pública y la descarga de esta muestra, sin cookies, login, formularios o carrito.

## Paso para Video

Analizar este archivo exacto de 21,46 s, conectando sus hallazgos con la ficha comercial existente. Registrar cobertura temporal y distinguir imagen/guion de voz, música, SFX y sincronía. La muestra resuelve el acceso y la atribución comercial a la tienda; su contenido audiovisual todavía debe inspeccionarse. Aprendizaje puede sustituir el candidato de Mercado Libre no atribuido por esta evidencia, dejando explícito que es una muestra de tienda y no un reel de Instagram confirmado.

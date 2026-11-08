# Entrega estabilizada · cobertura visual y contenido verbal

5/11/2026. Para Jefa, Aprendizaje y Organización. **Unidad independiente entregada; goal audiovisual integral abierto.** Hay40medios trazables y8imágenes del carrusel, sin repetir las28descargas iniciales. Justin permanece documental/gráfico; el universo del goal es17personas+Voltra,18filas. No hay ASR ni decodificación pesada de Video activos; no hay tareas pesadas de Video pendientes en esta entrega.

## Qué está cubierto y qué falta

- **Imagen temporal:** las40representaciones tienen inspección distribuida con mapas de principio/desarrollo/demos/cierre; intervalos y duplicados por ficha. Alex exacto tiene1717/1717cuadros en72hojas y14detalles, sin reproducción continua. No se extrapola esa exhaustividad al resto. Los5cierres ampliados incluyen74cuadros conPTS; se inspeccionaron8imágenes reales del carrusel.
- **Contenido verbal:** captions disponibles leídos y13ASR complementarios leídos íntegros;6huecos procesados por recorte. «Completo» significa totalidad del archivo de texto o salida automática disponible, **no que toda palabra del audio esté recuperada correctamente**. VAD/captions conservan descartes y errores.
- **Percepción/acústica:** siguen sin aceptar prosodia, música, SFX, ambiente, silencios perceptuales, mezcla y sincronía; ritmo visual descrito por estados/transiciones, no experiencia a velocidad normal. MiDashengLM falló controles reales según [Desarrollo](../../../99-archivo/audio-tecnico/ruta-abierta-20261105.md); no se aplicaron sus etiquetas a los referentes. Otra alternativa está en evaluación. No hay espera de permiso Higgsfield: está fuera.

## Trece transcripciones complementarias

Todos los textos/JSON de esta tabla están terminados y fueron leídos por el ejecutor Terra. Cada JSON guarda fuente, SHA, WAV y tiempos de segmentos/palabras. [Mapas y contraste por pieza](guiones-faltantes.md).

| Pieza | Texto íntegro disponible | Tiempos/hashes | Dudas materiales |
|---|---|---|---|
| Heras V1 | [TXT](../../asr/complementario/heras-vsl-v1.txt) | [JSON](../../asr/complementario/heras-vsl-v1.json) | Nombres repetidos, cifras/siglas dudosas. |
| Heras V2 | [TXT](../../asr/complementario/heras-vsl-v2.txt) | [JSON](../../asr/complementario/heras-vsl-v2.json) | Apertura distinta de V1; errores de nombres/cifras. |
| Toto vlog | [TXT](../../asr/complementario/toto.txt) | [JSON](../../asr/complementario/toto.json) | Mars/Marz y repeticiones sospechosas; ASR empieza a23,18s. |
| Alex exacto | [TXT](../../asr/complementario/alex-carrera.txt) | [JSON](../../asr/complementario/alex-carrera.json) | CTA y términos IA/editor distorsionados; contrastar cuadros. |
| Hormozi offers4 | [TXT](../../asr/complementario/hormozi-offers4.txt) | [JSON](../../asr/complementario/hormozi-offers4.json) | Nombre, estadísticas y URL final dudosos. |
| Hormozi leads5 | [TXT](../../asr/complementario/hormozi-leads5.txt) | [JSON](../../asr/complementario/hormozi-leads5.json) | Términos de contacto/contenido mal reconocidos. |
| Hormozi leads6 | [TXT](../../asr/complementario/hormozi-leads6.txt) | [JSON](../../asr/complementario/hormozi-leads6.json) | Precios/proporciones no certificados; ejemplo hipotético separado de invitación real. |
| Pedro66 | [TXT](../../asr/complementario/pedro66.txt) | [JSON](../../asr/complementario/pedro66.json) | Oración de negocio y remate defectuosos. |
| Gonzalo alternativa | [TXT](../../asr/complementario/gonzalo-alternativa.txt) | [JSON](../../asr/complementario/gonzalo-alternativa.json) | Errores en inicio y rutina; autorreporte. |
| Voltra | [TXT](../../asr/complementario/voltra.txt) | [JSON](../../asr/complementario/voltra.json) | Un segmento agrupa todo; 3gotas frente a3cuotas visible. |
| Pedro Dem | [TXT](../../asr/complementario/dem097kgi-a.txt) | [JSON](../../asr/complementario/dem097kgi-a.json) | Frase de dependencia dudosa; CTA Escala. |
| Pedro Dehh | [TXT](../../asr/complementario/dehhvydawdl.txt) | [JSON](../../asr/complementario/dehhvydawdl.json) | Números y expresiones dudosos; CTA al cliente etiquetado distinta del caption. |
| Toto LinkedIn | [TXT](../../asr/complementario/toto-linkedin.txt) | [JSON](../../asr/complementario/toto-linkedin.json) | Mars/Marz y cifra deformada; resultados no auditados. |

## Seis recortes de huecos

Los tiempos son de la fuente original. Se preserva contexto adicional y no se confunde con el hueco. [Método, VAD y límites](huecos-captions.md). Ningún resultado vacío autoriza a afirmar silencio o ausencia de voz/música.

| Pieza | Hueco solicitado(s) | Recorte con contexto(s) | Archivos exactos | Resultado |
|---|---|---|---|---|
| Jeff ml5 | 723,519–748,880 | 721,519–750,880 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/jeff.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/jeff.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/jeff.json) | Texto sustantivo recuperado; final dudoso y contexto fuera del hueco. |
| Nick inicio | 0–13,280 | 0–15,280 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/nick-inicio.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/nick-inicio.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/nick-inicio.json) | Sólo You; no reconstruye la apertura. |
| Nick final | 1661,360–1681,846833 | 1659,360–1681,846833 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/nick-final.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/nick-final.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/nick-final.json) | Sin segmentos; TXT vacío semánticamente. VAD descartó todo; no prueba silencio. |
| Bastian inicio | 0–2,450 | 0–4,450 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/bastian-inicio.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/bastian-inicio.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/bastian-inicio.json) | Frase parcial que cruza el hueco. |
| Bastian final | 2032,640–2040,271567 | 2030,640–2040,271567 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/bastian-final.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/bastian-final.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/bastian-final.json) | Despedida cruza el límite; resto sin reconstruir. |
| Álvaro inicio | 0–27,870 | 0–29,870 | [WAV](../../../operacion/referentes-20261105/video/asr-huecos/alvaro-inicio.wav) · [TXT](../../../operacion/referentes-20261105/video/asr-huecos/alvaro-inicio.txt) · [JSON](../../../operacion/referentes-20261105/video/asr-huecos/alvaro-inicio.json) | Muy dudoso: segmento atraviesa amplio descarte VAD. |

## Siete piezas históricas

[Análisis por pieza con mapas verbales, visuales, demostraciones y cierres](../../../99-archivo/versiones-superadas/historicos-v2.md). Las7cuentan conMP4/captions y muestras/detalles/finales inspeccionados; no escucha. LosTXT derivados se leyeron completos; conservan errores y huecos. MP4, metadata y hashes en `video/historicos-v2/media-manifest.json`.

| ID | Texto leído | Cobertura/observación |
|---|---|---|
| HgORJd9rNxw | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/HgORJd9rNxw.en-orig.txt) | VlogNYC; captions completos leídos. |
| pe9ZXIwMBBM | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/pe9ZXIwMBBM.en-orig.txt) | Recopilación3h21; captions leídos íntegros en tandas; contradicción75/95£ y reutilización NYC. |
| 5pAQcC9YniM | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/5pAQcC9YniM.en-orig.txt) | Título2026, discurso2025; captions leídos. |
| vOBKA8n15vg | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/vOBKA8n15vg.en-orig.txt) | Tres métodos/CTA; ingreso y ahorro son alegaciones. |
| pLH3avh7kY4 | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/pLH3avh7kY4.es-orig.txt) | Clase marca personal; referencias2024 frente a título2026. |
| xc4OtzAnVMI | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/xc4OtzAnVMI.en-orig.txt) | Minimalismo; oferta histórica y límites del autor. |
| ml5uvpfXcLU | [Captions normalizados](../../../operacion/referentes-20261105/video/historicos-v2/ml5uvpfXcLU.en-orig.txt) | Captions con hueco12:03–12:28; ASR complementario acotado arriba, no tercera intención probada. |

## Evidencia y decisiones que se necesitan

[Corpus requerido/observado](corpus-requerido.md) conserva piezas/candidatos y procedencia; [ampliación Pedro/Erik/Toto](ampliaciones-pedro-erik-toto.md), [cierres porPTS](cierres-ampliaciones.md), [Alex exhaustivo](alex-cuadros-completos.md), [refuerzo CTA Heras](../../../99-archivo/versiones-superadas/heras-refuerzo-v2.md), [QA](qa-reapertura.md) y [verificación incremental](verificacion-reapertura.json). Los28mediospreviosconservan suQA; los12nuevos hashes fueron cotejados12/12, sin otra decodificación general.

**Jefa/Aprendizaje:** usar estos archivos para actualizar brechas y enseñanza sin repetir recuperación. Decisión deJefa recibida: bcQY9UvfMF4,BjyDaxYpW8o yJKO8AQGZ5tc no seleccionados, sin envío obligatorio acreditado; ml5 incluido como vínculo, no equivalencia con tercera intención; podcasts conservan sólo sinopsis/identidad. La exclusión está autorizada y documentada; no se suman como vistos. Los materiales identificables de la ampliación ya se ejecutaron; el original Gonzalo DYP sigue separado de su sustituto autorizado.

**Desarrollo/Jefa:** terminar la alternativa acústica con controles y entregar únicamente capacidades que pasen. Video puede aplicar entonces sobre estos mismos medios/intervalos; no necesita otra descarga. Si la alternativa falla, la intervención mínima debe referirse al atributo y fragmento que realmente reste, con prueba del límite. Este documento no acepta el goal ni presenta las tres propuestas futuras de Jefa, y no pide registro/compra/contacto para formaciones privadas.


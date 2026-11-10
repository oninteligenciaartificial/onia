# Dos videos de Euge: revisión propia y aplicación a OnIA

Encargo `euge-dos-videos-20261110`, autorizado por Sergio con «Hazlo» después de preguntar si Codex había visto ambos videos. Trabajo iniciado el 9 de noviembre de 2026 a las 22:28 America/La_Paz (10 de noviembre UTC). Es análisis: no modifica el modelo aprobado ni inicia la fábrica.

## Qué se revisó realmente

Imagen observada directamente mediante secuencias de fotogramas distribuidas por ambos videos, más capturas del reproductor. Contenido hablado leído completo: ASR alineado existente para el primero; subtítulos automáticos originales en español para el segundo, recuperados en esta ejecución. Los resúmenes de Boss se contrastaron después con estas fuentes.

**No hubo escucha directa del audio por el modelo ni observación continua de cada fotograma.** No se evalúan música, timbre, mezcla, sincronía labial ni cortes de pocos fotogramas. Se inspeccionaron 119 fotogramas de contenido del primero y 109 del segundo, además de controles del reproductor. La cobertura y sus límites están en [COBERTURA.json](COBERTURA.json). Las capturas, grabaciones y transcripciones íntegras permanecen privadas en el VPS; Git contiene sólo notas propias, enlaces y metadatos saneados.

## Video 1: cómo muestra su trabajo diario

Fuente: [Así Utilizo los Agentes de IA a Diario](https://www.youtube.com/watch?v=JuAQILH7dkQ). Los tiempos enlazados son aproximados; se separaron los anuncios del contenido.

| Momento | Observación e interpretación del pasaje |
|---|---|
| [12:38–15:30](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=758s) | Alterna un esquema de coordinación con pantallas del asistente y aplicaciones. Explica una entrada principal que delega y recupera información. |
| [16:14–17:48](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=974s) | Descompone el resultado final en piezas evaluables. El criterio de calidad precede a delegar. |
| [18:25–20:34](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1105s) | Enseña una pieza editada con cambios de plano y elementos gráficos, y vuelve al diagrama de la máquina de fábricas. Lo mostrado no acredita que nuestra infraestructura reproduzca esa edición. |
| [20:34–23:34](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1234s) | Pasa de materiales a candidatos y filtro con público simulado. Es selección de hipótesis, no validación comercial. |
| [24:08–27:10](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1448s) | Se ven previsualización, línea de tiempo, lista de entregas y seguimiento de pasos. Propone corregir con ejemplos antes/después y conservar el criterio. |
| [27:10–30:02](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1630s) | Muestra su experimento de publicación automática, vuelve al ordenador compartido y cierra con promoción. No trasladamos esa autorización ni esos proveedores a OnIA. |

## Video 2: contexto y procesos evaluables

Fuente: [Dame 25 minutos y nunca volverás a usar la IA igual](https://www.youtube.com/watch?v=xPJbP9yZE1I). Duración del reproductor 26:34; metadato 1595 segundos.

| Momento | Observación e interpretación del pasaje |
|---|---|
| [1:18–4:22](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=78s) | La lámina distingue el modelo ya entrenado de la conversación. La memoria aportada no es entrenamiento de pesos. |
| [8:06–14:04](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=486s) | Se ven un lienzo con referencias de video y láminas de documentos, memoria y recuperación. Pide contexto pertinente y ejemplos del resultado buscado. |
| [14:04–18:58](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=844s) | Explica el arnés, persistencia y simplificación; muestra una lista de trabajos para volver a probar los modelos. |
| [18:58–24:30](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=1138s) | Define agente mediante modelo, contexto, herramientas y objetivo; distingue una ejecución de una rutina. |
| [24:30–26:34](https://www.youtube.com/watch?v=xPJbP9yZE1I&t=1470s) | El diagrama completo de 25:37 conecta video, recorte, imágenes, edición y resultado. Explica el flujo; no prueba que OnIA lo tenga instalado. |

## Qué aporta frente a lo que resumió Boss

Los dos resúmenes de Boss recogen la idea principal. La observación visual aporta evidencia concreta de la sala de revisión, el seguimiento por paso y los ejemplos de resultados. No encontré una razón para cambiar el reparto aprobado por Sergio.

Hay cuatro correcciones necesarias al trasladarlo al borrador `FABRICA-DESGLOSE-20261109.md`, sin modificarlo todavía:

1. **Propiedad editorial:** el borrador adjudica ideas y guiones a Boss; la fuente única asigna la responsabilidad editorial a Contenido. Boss puede reunir contexto y coordinar. Hay que resolver esa contradicción antes de despachar.
2. **ASR no equivale a escuchar:** una transcripción con tiempos no permite elegir por sí sola la mejor toma, detectar toda la intención o juzgar el sonido. La salida debe señalar incertidumbres para revisión humana.
3. **Aprendizaje verificable:** parecidos de duración o cortes no bastan. Un ejemplo corregido debe producir una regla concreta y una nueva prueba que compruebe su efecto, preservando el original.
4. **Continuidad después del 14:** una PC y FFmpeg pueden ejecutar instrucciones de edición; no sustituyen las decisiones editoriales de un modelo. Deben quedar explícitos qué decide Contenido/Sergio y qué ejecutan programas fijos. Una suscripción de interfaz tampoco acredita API o cuota para automatizar.

## Cómo lo aplicaría, sin construir todavía

La meta que entiendo es que Sergio deje una grabación y reciba piezas revisables, con un solo punto de coordinación y criterios guardados. El cerebro es contexto recuperable; el harness registra y ejecuta tareas autorizadas; el panel muestra entregas y decisiones. La máquina ejecuta los pasos pesados. Son responsabilidades diferentes dentro del sistema existente.

Reutilizaría el panel aceptado y empezaría por **una pieza real de la tanda**, antes de prometer cinco diarias: guion aprobado → archivo privado → propuesta de cortes con tiempos → render CPU → revisión distinta → corrección → aprobación de Sergio. El vlog completo permanece fuera de esa edición. Contenido decide guion, CTA y material visual; Codex implementa y comprueba el procesamiento técnico solicitado por ID.

La aceptación de esa primera pieza debería comprobar legibilidad móvil, palabras y tiempos de subtítulos, ausencia de cortes de frases, correspondencia del B-roll, revisión humana de sonido y registro de la corrección. La publicación sigue en manos de Sergio. Después se mide si el procedimiento reproduce cinco piezas con la calidad y el tiempo disponibles.

No hace falta rehacer el harness ni terminar todo el homelab para acordar ese ensayo. Tampoco queda acreditado un flujo automático por tener carpetas y conectores. Lo que falta decidir es el primer guion, el archivo de entrada, un ejemplo de edición aceptable y quién aprueba las decisiones editoriales dudosas.

## Fuentes internas y estado

- [Modelo único aprobado](../../ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md).
- [Desglose de Boss, borrador](../../FABRICA-DESGLOSE-20261109.md).
- [Lectura de Boss del primer video](../../EUGE-VIDEO-BOSS-20261109.md) y [del segundo](../../EUGE-VIDEO2-BOSS-20261109.md).
- [Resolución anterior del primer video](../../../05-herramientas/video-euge-20261108/RESOLUCION-20261109.md), con sus límites originales conservados.
- [Panel existente](../../../05-herramientas/fabrica-contenido/20261109-lector-panel/README.md).

El estado canónico permanece en [la tarea del harness](../../tareas/euge-dos-videos-20261110.json). Publicar este análisis no equivale a aceptación independiente ni a autorización para implementar la fábrica.

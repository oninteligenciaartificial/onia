# Coordinación acústica · Video / Desarrollo

5/11/2026. Estado vigente: unidad visual/verbal aceptada; audio en evaluación por Desarrollo. Los 13 ASR y seis recortes de Video están terminados y leídos; sin cola activa. [Pendientes finitos](pendientes-visuales-finitos.md) sustituye instrucciones de ejecución de este registro histórico. Fuente de aceptación: GOAL-REFERENTES.md, mantenida por Organización. Esta nota pertenece a Video; Desarrollo conserva sus métodos/controles. No autoriza Higgsfield ni gasto. La respuesta vigente de Sergio es investigar y usar open source.

## Requerido frente a observado

| Componente | Observado hasta ahora | Trabajo ejecutable / aceptación |
|---|---|---|
| Guion verbal | Captions/ASR con errores, huecos y cues que exceden duración; faltaban clases Hormozi, VSL Heras, Toto y reels. | Terra de Video terminó 13 medios y seis recortes con small cacheado/VAD, local, sin duplicar acústica. Guarda segmento, palabra, origen/hash e intervalo; lectura y contraste de rótulos. No certificar literalidad. |
| Imagen y texto | Muestreo temporal de las 28 piezas con finales; intervalos exactos en manifiestos. | Video amplía demostraciones, transiciones y CTA identificados por el nuevo texto. Los cuadros intermedios siguen sin observación hasta revisarlos; decodificar no los acredita. |
| Edición y ritmo visual | Secuencias, encuadres y apoyos descritos; no cortes exhaustivos. | Medir sólo cambios que se contrasten con cuadros antes/después. Un detector de escenas sería candidato, no conteo final sin inspección. No inferir velocidad oral desde cambios de texto. |
| Voz/prosodia | Ninguna evaluación perceptual aceptada. | Desarrollo entrega capacidad efectivamente validada y sus límites; Video aplica sobre fuente/intervalo identificados. ASR no prueba emoción, timbre o énfasis. |
| Música/SFX/ambiente | Audio recuperado; clasificadores históricos no superaron controles suficientes. | Desarrollo prueba controles conocidos con silencio, tono, voz y efecto, más fuentes mezcladas si va a afirmar separación. Conservar falsos positivos/negativos y respuestas originales. |
| Silencios | VAD y energía, no silencio percibido. | Diferenciar cero PCM, pausa de habla y ausencia de música. No llamar silencio a una zona sin captions/VAD. |
| Sincronía | Concordancia aproximada de ordinales/ASR en Pedro90; no prueba labial. | Evento visual con PTS y evento acústico válido con intervalo e incertidumbre. No deducir desfase de padding AAC/Opus ni de metadata redondeada. |
| Relación comercial | CTAs visibles/de captions, destinos documentales tratados por Marketing/Aprendizaje. | Contrastar la invitación con imagen y texto por intervalo; no probar entrega, ventas o vigencia por una frase del video. |

## Prioridad de aplicación cuando exista capacidad válida

1. Pedro90: controles históricos y cinco fragmentos ya preparados; recuperar siempre su mapa de tiempos originales, sin atribuir separadores añadidos al reel.
2. Alex exacto: 0–14 s ejemplo, 13–26 s interfaz, 42–57,233 s transición/recurso. Distinguir capas del video insertado y conversación principal.
3. Heras V1: nuevo ASR sitúa primera CTA en 457,52–478,78 s y repetición en 614,36–633,66 s; son localizadores automáticos, no escucha. Contrastar V2 por su propio tiempo, sin copiar desplazamientos.
4. Una muestra por familia restante con controles pertinentes antes de extrapolar. El cierre integral requiere cobertura de cada pieza requerida; pasar un fragmento no acepta el corpus.

Medios y hashes permanecen en las fichas/manifiestos de Video y recuperación secundaria. No redescargar ni redecodificar íntegramente archivos intactos sólo para repetir QA. Nuevos textos en `video/asr-complementario/`, nuevas fuentes históricas en `video/historicos-v2/`. Aplicar resultados acústicos únicamente después de leer su evidencia: un nombre de modelo o licencia no prueba comprensión.

La modalidad nativa de audio fue rechazada previamente y no se reintenta. El método open source sigue en evaluación por Desarrollo; no se registra un impedimento definitivo mientras tenga alternativas autorizadas pendientes. Si ninguna supera controles, precisar qué atributo no puede evaluarse y ofrecer a Jefa un fragmento recuperable y la pregunta humana mínima; no pedir que Sergio descargue o extraiga los medios.

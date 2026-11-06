# Reel: importar, corregir y continuar

Propuesta técnica textual de una pieza de **24 s, 1080 × 1920, 30 fps y 720 cuadros**, con HyperFrames como motor previsto. Público: persona sin experiencia técnica. La comprensión depende de imagen y rótulos; funciona completamente sin sonido.

**Hechos suministrados.** El fixture describe una vista previa de 3 de las 12 filas; una importación con estado ocupado; el error «Falta fecha» en fila 7; una corrección manual y nueva importación que muestra 12 filas importadas; exportación y apertura de un borrador local. No se aportaron medios reales. No conocemos la fecha completada ni existe destino para «Ver ejemplo». Los dos clicks son datos de montaje, no audio escuchado.

**Decisiones propuestas.** Mantener íntegros el orden y los tiempos descritos. Introducir el resultado temprano mediante un anticipo textual sobre la vista previa, sin adelantar ni repetir metraje. El anticipo identifica expresamente el tramo fuente 13–18 s y no atribuye la importación a las tres filas visibles. Luego se sigue la secuencia original hasta alcanzar ese resultado. No se usan pantallas simultáneas.

Los intervalos temporales son inicio inclusivo y fin exclusivo; los cuadros se numeran de 0 a 719, con extremos inclusivos.

| Tiempo / cuadros | Hecho mostrado | Texto propuesto | Audio propuesto | Transición |
|---|---|---|---|---|
| 0–3 s / 0–89 | A: vista previa de tres filas, aún sin importar. Anticipo exclusivamente textual del resultado posterior. | «Anticipo: 12 filas importadas». Debajo: «Resultado del tramo 13–18 s». | Silencio. | Entrada directa; interfaz visible y textos quietos durante 3 s. |
| 3–5 s / 90–149 | A continúa: sólo vista previa, CSV de doce filas. | «Vista previa: 3 de 12». | Silencio. | Sustitución directa del rótulo; sin alterar el metraje. |
| 5–9 s / 150–269 | B: acción Importar y estado ocupado. | «Importar»; después «Procesando», acompañando el cambio efectivo de interfaz. | Único cue previsto a 5,2 s, cuadro 156: click sintético suministrado como dato. | Corte de fuente en 5 s; no acelerar la espera. |
| 9–13 s / 270–389 | B: error «Falta fecha» en fila 7, visible todo el tramo. | «Fila 7: falta fecha». | Silencio. | Cambio directo al estado de error; hold de 4 s. |
| 13–18 s / 390–539 | C: persona completa manualmente la fecha, reimporta y ve doce filas importadas. | «Completar fecha manualmente» → «Volver a importar» → «12 filas importadas». Cada rótulo aparece con su hecho. | Único cue previsto a 17,6 s, cuadro 528: click sintético suministrado como dato. | Continuidad de la acción. Sin fundidos que oculten la corrección ni salto al resultado. |
| 18–22 s / 540–659 | C: exporta y abre un borrador local. | «Exportar» → «Borrador local abierto», según la acción visible. | Silencio. | Continuidad; conservar exportación y apertura. |
| 22–24 s / 660–719 | Placa final, sin simular un enlace funcional. | «Ver ejemplo». Debajo: «Destino pendiente». | Silencio. | Corte directo a placa; hold de 2 s, sin salida adicional. |

**Composición y lectura.** Fondo #F8FAFC, tinta #172033, acento #176B50 y fuente de sistema. Títulos y rótulos esenciales de al menos 40 px, cada uno con cinco palabras como máximo. Ubicar todo texto esencial dentro de x108–864, y192–1330 px. Reservar una banda para rótulos sin tapar la fila 7, la fecha, Importar o el resultado; ajustar escala y encuadre de la interfaz sin eliminar información necesaria. Esta zona procede del fixture y no garantiza cobertura de ninguna plataforma.

Los holds de 3 s para el anticipo y 4 s para el error permiten leer y relacionar texto e interfaz; los 2 s de vista previa y CTA sostienen mensajes breves. En los tramos con varias acciones, los rótulos permanecen quietos y cambian sólo con la acción. Sus duraciones exactas requieren localizar los eventos en medios reales; no se inventan marcas internas ni se congela o retima el material para hacerlas encajar.

**QA pendiente y siguiente acción.** El responsable de montaje deberá cotejar las grabaciones reales antes de componer: confirmar eventos y tiempos, fecha sin añadir valores, fila 7 legible, corrección manual completa y resultado de doce filas. Después comprobar el render íntegro: 720 cuadros, duración de 24 s, dimensiones, 30 fps, códecs, continuidad, lectura y recortes, incluidos inicio, cambios de estado y final. Probarlo sin sonido. Si se incorporan los dos cues disponibles, escuchar y comprobar presencia, sincronía y ausencia de sonidos adicionales; sus tiempos nominales no prueban sincronía. Si aún no existen archivos sonoros, entregar la versión silenciosa. El destino del CTA deberá definirse antes de usarlo como acceso real. No hay render, audio ni publicación verificados en esta entrega textual.
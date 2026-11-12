# QA del diseño · v1

final result: passed

Alcance del pase: mapa y prototipo de navegación/revisión/tarea. No aceptación del producto operativo ni de la sala de montaje especializada.

## Fuentes y comparación

Referencia visual aportada: codex-clipboard-86767fcf-ec27-434d-8911-28666c3c07a6.png (1918×1078, captura de video, incluye marco del navegador y presentador). La imagen se abrió junto con evidencia/01-mapa-pc.png (1440×1000 CSS px, DPR1) en la misma llamada de inspección. Comparación estructural, no píxel a píxel: la superficie de app de Euge ocupa sólo parte de su captura. No se afirma igualdad de tamaños. Detalle de revisión de guion adaptado a OnIA, no réplica de editor audiovisual.

Implementación: evidencia/01-mapa-pc.png, 02-revision-pc.png, 03-trabajo-pc.png, 04-mapa-movil.png, 05-revision-movil.png y 06-tarea-movil.png. Chromium sandbox activo mediante CDP, 1440×1000 y 390×844. No se ha probado en Safari físico. Comparación visual de mapa completo y sus primeras tres filas; inspección de detalle de revisión y móvil.

## Evaluación

- Tipografía sans-serif del sistema, encabezados claros, etiquetas secundarias compactas; móvil conserva tamaños legibles y orden vertical.
- Cuatro columnas de proceso y filas suaves conservan la referencia. Sin sombras ornamentales; tonos cálidos y destinos oscuros. En móvil las filas se apilan.
- Copia adaptada a OnIA y estados de demostración identificados permanentemente. No se copiaron métricas, marcas, fotos ni ilustraciones de Euge. Esta adaptación omite los iconos 3D y no pretende recrearlos con dibujos de código.
- Navegación, corrección y lanzamiento simulado probados. Registro de excepción de runtime vacío y sin overflow horizontal en 390px. Ver comprobacion.json.
- Hallazgo P2 corregido: paso de escritura resaltado con estado para revisar; ahora resalta revisión. Se quitó el paso activo a fábricas sin entrada. Capturas regeneradas después de corregir.
- No se detectaron otros P0/P1/P2 en el alcance del prototipo.

## Límites y siguiente revisión

Persistencia sólo en memoria; no sincroniza dispositivos. Sala de montaje sólo entrada/detalle de fábrica; su editor requiere diseño especializado posterior según PLAN. No hay conexión con harness, n8n, fuentes de estados ni pagos. Aceptación visual y prueba física iPhone/PC pendientes de Sergio.

P3: afinar densidad, etiquetas y tratamiento visual según la revisión de Sergio. El diseño operativo siguiente debe incluir teclado/modal con gestión completa de foco.

## Revisión independiente y correcciones

Subagente revisar_diseno_panel, revisión de sólo lectura. Se corrigieron separación de formulario/tarea y entrega, reinicio de versión/borrador al cambiar de fábrica, destino fijo de Revisiones, estado de aprobación visible por versión y orden Entrada → Fábrica en móvil. Se añadieron tres ejemplos de seguimiento con dependencia y responsable, identificados como ejemplos. Build y recorridos CDP repetidos con éxito; capturas actualizadas.

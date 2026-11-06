# Revisión estática de inscripción

Hallazgos ordenados por prioridad. La evidencia procede sólo del código; las comprobaciones propuestas son posteriores, no realizadas.

1. **Crítico — envío sin confirmación ni recuperación.** `#signup` cancela el envío y siempre asigna «Algo salió mal» a `#status`; no hay operación ni ruta de éxito. La persona no puede completar la inscripción ni saber cómo recuperarse. Implementar el flujo real cuando exista: conservar datos, indicar envío, confirmar sólo ante éxito y explicar fallos con acción de reintento; anunciar los cambios mediante una región de estado accesible. Comprobar éxito, fallo y reintento sin pérdida de datos; este fixture no permite verificar backend.

2. **Crítico — disponibilidad contradictoria.** `.details` dice «Sin cupos disponibles», mientras `.badge` dice «Inscripción abierta» y el formulario permanece activo. No se puede determinar cuál es el estado correcto ni inventar una lista de espera o fecha. Confirmar la regla de disponibilidad con la fuente del producto; mientras tanto mostrar un único estado pendiente, sin prometer inscripción. Una vez definida, comprobar que mensaje y disponibilidad del formulario coincidan en cada estado.

3. **Alta — campos sin nombres ni validación suficiente.** `#mail` sólo tiene placeholder y `#topic` no tiene etiqueta; ninguno es obligatorio y la primera opción del selector es seleccionable como tema. Agregar `label` visible asociado a cada campo, `type="email"`, `autocomplete="email"` y `required`; dar a la opción inicial un valor vacío y exigir una selección. Mostrar errores específicos asociados a cada campo y llevar el foco al primero inválido. Comprobar vacío, correo inválido y tema sin elegir con teclado y lector de pantalla.

4. **Alta — acción principal sin nombre y pequeña.** `button[type=submit]` contiene sólo un SVG sin nombre accesible y CSS fija 20 × 20 px. Puede ser difícil identificarlo y pulsarlo. Añadir texto visible «Inscribirme», ocultar el SVG decorativo de la tecnología asistiva y ampliar el área interactiva y separación. Comprobar nombre anunciado y activación con teclado y toque en móvil.

5. **Alta — foco invisible.** `*:focus{outline:none}` elimina el indicador de foco sin sustituto. Una persona que navega con teclado puede perder su posición. Restaurar el contorno o definir `:focus-visible` distinguible para cada control. Recorrer el formulario con Tab y comprobar visibilidad y orden en ambos tamaños.

6. **Alta — consentimiento opcional inoperable con teclado.** `.toggle` es un `div` con `onclick` que reemplaza su texto por «Aceptado»; carece de semántica, estado reversible y valor de formulario. Sustituirlo por checkbox nativo con etiqueta persistente, inicialmente desmarcado y opcional; conservar su estado al fallar el envío. Comprobar alternancia por teclado y anuncio de estado, y que inscribirse no dependa de marcarlo.

7. **Alta — adaptación móvil.** Falta `meta viewport` y `main{width:980px;padding:24px}` fija un ancho mayor que 360 px. El código indica riesgo de escala reducida o desbordamiento; su presentación exacta requiere render. Añadir viewport y ancho fluido con `max-width`, `box-sizing:border-box` y márgenes adaptables. Verificar a 360 y 1280 px, con zoom y sin desplazamiento horizontal inesperado.

8. **Media — legibilidad y contraste.** `body` usa `#999` sobre blanco y `.details` sólo 10 px; la fecha y disponibilidad pueden resultar difíciles de leer. Usar texto oscuro y tamaño legible, conservando la identidad verde; revisar también `#status` rojo. Medir contraste de los pares efectivos y comprobar lectura y reflujo con ampliación; la apariencia final requiere render.

9. **Media — movimiento continuo.** `.badge` escala indefinidamente cada 0,4 s y no contempla preferencias de movimiento reducido. Puede distraer o causar molestias. Eliminar el pulso decorativo o detenerlo con `prefers-reduced-motion`; mantener el estado legible sin animación. Comprobar ambas preferencias y que el mensaje siga disponible.

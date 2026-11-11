# Integración de estrategias con el panel — 11nov2026

Actualiza el estado del recibo original; sus evidencias se conservan sin reescribir. El panel74563b8 ya reconoce la raíz de estrategias y sus controles. La coordinadora leyó el diff de operacion.py: registra el productor y añade migración/reintentos de correcciones. No cambia precios, fechas, cupos ni texto comercial. S08 era la única fuente divergente; se conservó fuentes-antes-panel.json y se actualizó sólo su huella/tamaño, con acta en fuentes.json. Las otras11fuentes coinciden.

El comprobador ahora prueba el consumidor real, sin ampliar su mapa en memoria ni esperar un rechazo que ya no corresponde. Mantiene el rechazo de rutas ajenas y todos los controles comerciales. El recibo nuevo está en evidencia/conciliacion-panel.json. El número de controles puede cambiar al retirar el rechazo histórico; no se traslada el conteo original al resultado actual.

La prueba visual de integración de la coordinadora está en la entrega del panel, evidencia/correccion-cerebro-20261111/host-final-04: escritorio/móvil simulado, correcciones y persistencia. Falta teléfono físico y servicio desplegado. La oferta y las piezas siguen pendientes de ensayo/editorial; no hay publicaciones, cobros ni canal Meta real probado.

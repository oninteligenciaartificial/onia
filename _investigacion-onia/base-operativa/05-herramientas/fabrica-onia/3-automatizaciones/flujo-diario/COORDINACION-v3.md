# Recuperación antes de crear el pedido

Dictamen recogido sobre 81d3352: cambios por pérdida de entrada entre persistir la noticia y crear el pedido.

Corregido: se registra la entrada pendiente antes de deduplicar la noticia. Reiniciar retoma esa intención y conserva su procedencia real/sintética; el ID diario sigue siendo único. El lector horario usa ingestión sin disparar tanda antes de la hora elegida. No se cambió la política de permisos ni se activó el scheduler.

La suite completa de ciclo/programación pasó 36 pruebas. La reproducción específica del corte y la comprobación de hora/deduplicación se repitieron con salida y hashes en evidencia/coordinadora-v3. Las 5 HTTP de coordinadora-v2 y 25 de generador de coordinadora siguen sobre archivos sin cambios. Código, comandos y evidencias anteriores se conservan, incluidos dictámenes de cambios.

Revisión nueva requerida del commit corregido. Ensayo real del modelo y activación aún pendientes.

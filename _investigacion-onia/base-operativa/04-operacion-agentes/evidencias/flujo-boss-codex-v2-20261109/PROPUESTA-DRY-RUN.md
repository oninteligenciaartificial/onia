# Fricción dry-run: propuesta acotada, no implementada

ID real: flujo-boss-codex-v2-20261109. Fuente: bloque Fricción harness de 9354c7e y autorización directa de Sergio. No se cambió código ni el contrato de lanzamiento con este documento.

Causa: --dry-run usa otra carpeta de operación pero sigue mutando el mismo JSON de tarea y mantiene sus rutas asignadas en esta base. El control que impide mezclar simulación/real por ID protege la trazabilidad; cerrar la sesión simulada no libera la asignación. Un ID nuevo o cambiar sólo --operacion no resuelve una reserva del mismo archivo.

Conciliación de este caso: sesión simulada ya cerrada, cero PID real; tarea identificada como ENSAYO FINALIZADO en en_espera (schema2 no tiene estado anulado), asignación liberada por API con revisión/actor. No se acepta una simulación como entrega productiva. Historial, log y evidencia originales intactos; registro privado único conservado. El ID real nuevo usa esas rutas.

Propuesta mínima para aprobación posterior:

1. Hacer lanzar --dry-run una previsualización no mutante: validar tarea/rutas/modelo/contexto y mostrar comando/advertencias, sin crear sesión ni SID simulado dentro de la tarea, sin reservar cupos, worktree, proceso, escritura de índice o cambio de revisión. Mantener el modelo de preparar/asignar/cerrar/revisar existente.
2. Una asignación real previa a la previsualización conserva su reserva legítima y el mismo ID puede lanzarse de verdad después. Para ensayar asignaciones sin efectos, usar fixtures en una base de pruebas separada, no los archivos reales; un sufijo de ID sin aislar la base no basta.
3. Para simulaciones históricas, una conciliación explícita con --revision-esperada y actor, que sólo permita sesiones todas simuladas/cerradas, conserve recibos y libere rutas. Rechazar cualquier sesión real o viva; no borrar marcas dry_run ni engañar el control de mezcla. Por ahora se usa la API existente, como en este caso.
4. Tests de una futura corrección: bytes de tarea/briefing/reservas/índice iguales antes/después de la previsualización; lanzamiento posterior del mismo ID con CLI sintético; rechazo real de solapes y del cuarto cupo intactos; conciliación rechazada ante sesión viva/real, actor erróneo o revisión obsoleta; historial/evidencia conservados.

No crea otro harness, scheduler, backend PC ni política de autorizaciones. No se ensayó sobre la PC ni se amplió el tope3. Pruebas existentes se ejecutan para la entrega documental, no demuestran implementada esta propuesta.

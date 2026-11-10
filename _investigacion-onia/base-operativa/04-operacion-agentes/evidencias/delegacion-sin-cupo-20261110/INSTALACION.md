# Instalación comprobada y alcance pendiente

Release activa: `0efe1d5dace130892c1f4ed457fe382cceaad7a4`, instalada el 10/11/2026 a las 23:22:03 UTC (19:22 La Paz). Sólo cambió el módulo runtime `harness_delegacion.py`; su SHA256 es `62b1193984f21d15e458d5471572e1a5f5f06b44067d46c513b35dcd6704d6bc`.

Se verificaron los diez hashes del manifiesto. Entrada y manifiesto cambiaron bajo el lock privado del puente con reemplazo atómico y respaldo previo. Configuración, webhook y authorized_keys mantuvieron sus hashes; se conservaron registros y release anterior `6896ac62c7fc1950475ed720492c4b2f2ca773e6`. Respaldo privado: `~/operacion/puente-boss/respaldos/sin-cupo-20261110T232203Z-0f32a814/`. No se reiniciaron servicios.

## Comprobaciones posteriores

- Entrada instalada, invocada localmente con `SSH_ORIGINAL_COMMAND=onia-harness-v1`, solicitud `{"version":1,"operacion":"consultar","id":"fabrica-chatbot-whatsapp-20261110"}`: retorno 0, `ok=true`, r14, `para_revision`, `viva=false`. [Salida saneada](consulta-instalada.json). Es prueba local de la entrada; no acredita una nueva conexión SSH desde Boss ni ejecución de su rutina.
- Cuatro pruebas importando los módulos de la release instalada: séptima alta/idempotencia, ocho altas del día, permisos/cuota y reserva ante interrupción: 4 correctas, cero fallos/errores/omisiones. [Salida](tests-instalado-v2.txt), [resumen](tests-instalado-v2.json). Se fijó `harness.BASE` sólo en el fixture para ubicar metadatos del checkout revisado. La configuración real no cambió. Son fixtures; no ejecutan Codex real ni webhook.
- La suite de código previa pasó 160/160; comando y evidencia en [RECIBO](RECIBO.md).
- Cuota compartida posterior a instalación: 91% usado a 23:22:46 UTC, [lectura](cuota-final.json). No se atribuye esa diferencia a una sesión particular.

**Veredicto del cambio de altas: aceptar técnicamente.** Está publicado e instalado; las pruebas confirman el retiro de seis altas por día y la conservación de controles. No acepta entregas comerciales ni acredita la capacidad de cinco sesiones.

## Ensayo autorizado posteriormente

Sergio autorizó «Sí, hasta 2 puntos sólo para el ensayo», sobre la lectura de 91%; límite de referencia 93%. No autoriza gastar el remanente en trabajos comerciales ni retirar globalmente la reserva ordinaria de 90%.

Se preparó fuera del puente instalado una variante temporal, con cinco IDs exactos de consultas Sol low, el mismo contador canónico, expiración y control de recursos. La revisión independiente detectó que la cuota se consulta con retraso: varias admisiones pueden compartir una misma lectura y la cancelación reactiva no garantiza un techo de consumo. También observó validación insuficiente del ID/ruta de salida del wrapper experimental. **No se lanzó ninguna de esas cinco consultas.** La variante se revocó y conserva sus archivos privados como evidencia; no se instaló ni se publica como herramienta utilizable.

Última lectura antes de decidir no lanzar: 92% a `2026-11-10T23:35:16.251Z`. Cuota compartida; consumo atribuible a preparación/revisión unknown. La revisión del ensayo fue de la sesión distinta `/root/revisar_reglas_boss`, solicitado Sol low; no confundirla con cinco sesiones medidas.

**Veredicto del ensayo: corregir; capacidad no medida.** Antes de ejecutarlo hay que resolver el control de presupuesto del ensayo, verificar una lectura actual y corregir/validar el wrapper. No se aumenta el máximo ordinario de tres. No hay medición nueva de CPU/RAM bajo cinco consultas, de tareas pesadas, ni del homelab. Cinco consultas tampoco equivaldrían a cinco ejecutores de código o carga sostenida.

El conjunto de coordinación no se declara cerrado: faltan esa medición y la prueba real de la rutina Boss (fin ejecutor → cerrar → revisión → recoger → aviso). La instalación de reglas y tests de componentes no sustituyen ese recorrido. El estado de disponibilidad del homelab debe comprobarse en su host y no se deduce de estas pruebas del VPS.

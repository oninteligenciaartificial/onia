# Corrección de revisión independiente

El dictamen de4d3ed5c pidió cambios: cuota podía caducar durante I/O y no se recuperaba una entrega publicada por un ejecutor luego fallido.

La coordinadora revalida la misma observación después de comprobar filas y de nuevo inmediatamente antes del efecto, incluida su vigencia. No se admite sustituir silenciosamente su contenido. El cierre de un ejecutor fallido/interrumpido sólo se propone con declaración correcta y commit explícito; preflight y API comprueban resultado, commit remoto, rutas y procesos antes de cerrar. Sin declaración sigue exigiéndose conciliación para retomar el mismo SID.

Dos regresiones: observación115s que envejece a125s durante proveedor no despacha; ejecutor fallido con entrega comprobada cierra sin otro intento. La primera corrida de la segunda regresión tenía un fixture mal seleccionado (orden alfabético lanzaba dos, se intentó fallar uno); se fijó prioridad explícita antes de lanzar. No cambió el control para hacerlo pasar.

Comando: python3 -B -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p test_harness_lote.py -q
Resultado posterior: Ran33tests in4.920s; OK. La suite general236 y omisión1 son evidencia del commit anterior, no una repetición actual. No se activó scheduler ni se probó aún el piloto real. Requiere revisión independiente del nuevo commit.

# Corrección C4 · impresión y pies por página

La revisión independiente de `b832bc48656accea3b659dc6ceba2cb9142f04d7` pidió cambios: el pie 2/7 estaba en la página 3 del PDF, pese al conteo total de siete. Su veredicto se conserva en `../revision-c4-b832bc4.json`; el comprobador nuevo rechaza el original en `../rechazo-c4-host-01.json`. La inspección previa de láminas en pantalla y el mero conteo del PDF no detectaron ese fallo. No se alteró host-01 para ocultarlo.

La nueva prueba fue ejecutada por el **coordinador en el host VPS autorizado**, con Chromium sandbox activado, perfil sintético y copia aislada. `recibo-host.json`: rc0 y ocho hashes coincidentes con `../solicitud-host-v2.json` y el worktree, incluida la fuente del piloto. Se copiaron sólo los veinte artefactos públicos permitidos y el recibo; ningún perfil ni cookie.

La ejecutora inspeccionó mediante `view_image`, con detalle original, **las siete capturas de láminas en emulación print y el recibo conjunto**:

- Lámina 2: seis actividades con todas sus duraciones/restricciones; rótulo de ficción y aviso de horarios del caso completos. El pie «01:00–02:00 / 2 de 7» queda dentro de la lámina.
- Lámina 3: siete filas de agenda, autoría de la muestra, 105 ocupados y 15 libres visibles. El pie es «02:00–04:00 / 3 de 7», sin el pie de la lámina anterior.
- Láminas 1 y 4–7: recorrido, práctica A, cambio B, guardado y cierre legibles, con sus pies visibles; no se recortaron consignas ni contenido.
- Recibo: índice, siete láminas, dos hojas y tres guías reconocibles. Las tablas y los pies de 2/3 aparecen completos.

Las seis capturas restantes (index-1, hoja-1/2, guia-1/2/3) se cotejaron byte a byte contra host-01: son idénticas a las ya inspeccionadas en esa corrida. No se presenta como una nueva inspección individual de esos seis PNG. Se mantiene el límite del encuadre de la barra fija en index-1, documentado antes.

El host pasó 21 controles de navegador; ahora mide/captura **todas las láminas en modo print**. Se volvió a ejecutar aquí `python3 comprobar-pdf.py evidencia/host-02`: doce páginas con pie propio y sin pie ajeno, evidencia en `pdf-paginas-ejecutora.json`. El control del host también pasó (`pdf-paginas-host.json`). Los PDF siguen siendo 7/2/3 páginas.

Límite: el parser stdlib sólo cubre este formato de PDF Chromium con ToUnicode/Flate; no es un lector general ni valida coordenadas. Las imágenes vistas son del HTML en emulación print, **no rasterización del PDF**. No hubo prueba de impresora, captura móvil nueva, ejecución de Claude, ensayo humano ni locución. Los controles de móvil del navegador siguen siendo mediciones de ancho. Revisión independiente nueva, acceso propio y canal siguen pendientes; Bs50 aprobado y VIP propuesto permanecen intactos.

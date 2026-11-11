# Alta v3 detenida en la prueba del worker

Evidencia proporcionada por Sergio el 11 de noviembre de 2026 desde PowerShell, DESKTOP-0GGGNMF. Instalador verificado por SHA256 3e6406591fa37c8518c42f5a4cc3e7e83885285e5836621988911b66d1e656be.

El diagnóstico previo informó control_pe.ok=true, returncode=0 y duración1.888s. La retoma autorizada pasó ese control pero terminó con CalledProcessError, exit1, al ejecutar setpriv como UID/GID1001 y onia-worker-shell con la prueba Python de aislamiento por stdin. La salida publicada no incluye stderr del proceso: causa exacta todavía desconocida. No acredita que falló una protección concreta ni que el worker esté habilitado.

Según el orden del código, este corte ocurre después de crear configuración y wrapper locales, antes de escribir alta-local-v1.json, crear/activar la unidad dedicada y publicar la llave. Esa inferencia necesita contraste en la PC; no se afirma inspección remota. La retoma anterior sólo acepta el árbol parcial previo al controlPE: NO repetirla sobre el estado nuevo. Conservar archivos y respaldos.

Siguiente diagnóstico acotado: ejecutar una vez el wrapper como UID/GID1001 con id -u, timeout15s, sin reinstalar ni modificar configuración. Si falla, obtener su mensaje directo; si funciona, aislar la comprobación concreta del CHECK mediante diagnóstico saneado. Después preparar retoma del estado exacto, revisión independiente y prueba local/SSH. Homelab no aceptado; no incrementar sesiones.

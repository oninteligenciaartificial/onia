# Cotejo de evidencia del piloto

12 de noviembre de 2026 UTC. Encargo `piloto-orquestacion-evidencia-20261112`. Base inspeccionada `ce1fe0cbfc797459b6311cf8169ae1c42bc24120`, descendiente comprobado de `abbf9b78b771084a5905429cab2eb929b1b59566`.

## Hallazgos

- El [recibo v2](../../CONTINUIDAD-v2-RESULTADO-20261112.json) declara 90 segundos sin conexiones, terminales cerradas según Sergio, dos conexiones satisfactorias y render de 2 segundos. Es evidencia registrada por la coordinación. La espera y el cierre de terminales quedan fuera de los scripts examinados y de la observación propia de esta sesión.
- [PRUEBA-RENDER](../../PRUEBA-RENDER-20261112.py) extrae mediante AST la asignación SSH de [PRUEBA-SSH-v4](../../PRUEBA-SSH-v4-20261111.py). Genera `testsrc2` a 640×360/24 fps, solicita libx264, dos hilos y dos segundos. Exige retorno correcto de FFmpeg/ffprobe, dimensiones, 48 fotogramas y duración con tolerancia de 0,1 s. Calcula tamaño y SHA256 del archivo generado. Los valores del recibo son coherentes con ese procedimiento.
- El tiempo declarado de 0,754 s mide la llamada FFmpeg. Los dos hilos son el parámetro solicitado al codificador. El script consulta `codec_name` pero no lo valida explícitamente y sólo inspecciona el primer stream. La muestra conserva el alcance sintético expresado en el recibo.
- PRUEBA-SSH-v4 obtiene UID, grupos, capacidades y señales de aislamiento, escribe una marca y comprueba su contenido en otra conexión. Guarda los booleanos sin exigir que todos sean verdaderos. Un retorno cero del script puede coexistir con un control negativo. El recibo inspeccionado sí declara esos controles positivos y UID/grupos 1001.
- `huella_verificada=true` es un literal del script. La configuración usa comprobación estricta contra un archivo conocido dedicado. La procedencia y el cotejo independiente de esa huella requieren evidencia adicional. Tampoco se inspecciona aquí el contenido de ese archivo privado.
- El JSON consolidado carece de fecha/hora de ejecución, hash de scripts y transcripción de comandos/retornos. Los scripts escriben recibos SSH y render por separado. Su consolidación y la espera de 90 segundos requieren el relato de coordinación. El [ensayo anterior](../../CONTINUIDAD-ENSAYO-20261112.md) registra un fallo rc255, y [la guía v2](../../CONTINUIDAD-WSL-v2.md) describe la reparación y el ensayo previsto. Son antecedentes con alcances propios.

## Comprobación propia y límites

Se analizaron JSON y AST, se compiló en memoria la sintaxis de ambos scripts y del payload de render, se cotejaron parámetros y se verificó la ascendencia Git. Los hashes de las fuentes y resultados están en [pruebas.txt](pruebas.txt). La búsqueda en archivos versionados devolvió cero coincidencias para `muestra.mp4` y `render-piloto.json`. El MP4 declarado como conservado en el worker queda pendiente de inspección y recálculo de hash.

La sesión hizo lectura local y controles estáticos. SSH, espera, aislamiento remoto, persistencia y render permanecen sustentados por el recibo de coordinación. Reinicio, logout, suspensión, ASR, scheduler, carga comercial y operación sostenida quedan fuera de la evidencia examinada.

Se leyó la skill canónica `desarrollar-y-verificar`, anunciada en el catálogo inicial. Modelo/esfuerzo efectivos del intento y cuotas inicial/final con hora quedan desconocidos desde esta comprobación. Se realizó una ronda de controles locales, sin retrabajo de las fuentes.

## Veredicto

Evidencia documental coherente para un ensayo acotado de continuidad entre conexiones y render sintético, con trazabilidad incompleta y reproducción remota pendiente. La aceptación integral del homelab queda pendiente de sus controles y autoridad correspondientes. El coordinador recibe esta entrega para cierre y revisión independiente del commit publicado, conforme al encargo.

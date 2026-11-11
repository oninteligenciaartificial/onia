# Controles adicionales reales

Pruebas desde VPS al worker por SSH con huella fijada y llave dedicada. TTY solicitado y rechazado; forwarding remoto rechazado; autenticación sin llave rechazada. Forward directo adicional probado con ssh -W localhost:2224, rechazado administrativamente. Resultados saneados en CONTROLES-SSH-v4.json. La prueba repetible CONTROLES-SSH-v4.py cubre TTY, forwarding remoto, sin llave y accesos internos; el forward directo fue comprobación adicional separada.

Rutas Windows directas, proc root, enlace simbólico y runtime WSL no accesibles. Binario PE no ejecutable; sudo ausente; sin descriptores heredados mayores a 2 observables en el proceso de prueba. No equivale a auditoría de vulnerabilidades del kernel ni a probar toda variante posible de escape.

El primer intento del diagnóstico terminó porque suponía sudo instalado; se corrigió el diagnóstico para distinguir ausencia de sudo de una denegación al ejecutarlo. No se modificó el worker ni sus protecciones. Segunda ejecución rc0 con todos los controles informados correctos. Los enlaces y marcas de prueba se conservan, sin borrar archivos.

Continúa pendiente disponibilidad sin terminal, reinicio/logon y el ensayo de orquestación. Preparación Windows en CONTINUIDAD-WSL.ps1, aún no ejecutada. No se aumentó concurrencia ni se lanzó una carga de producción.

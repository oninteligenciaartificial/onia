# Inspección efectivamente realizada

9 noviembre 2026 UTC. La ejecutora abrió `recibo-visual.png` mediante `view_image` y vio el diagrama de 1440 × 1120 px completo: encabezado, cuatro tarjetas y franja de pendientes, sin texto cortado. Los rótulos distinguen «DIAGRAMA PROPIO · NO ES CAPTURA DE NAVEGADOR», las cantidades 7/2/3, A105/B130 y el bloqueo de comprobación visual. Se leyó explícitamente el pendiente de capturas/PDFs/acceso/ensayo/locución. El gráfico usa texto y formas propios, dibujados con Pillow ya disponible y DejaVu Sans del sistema; no se generó con un servicio externo.

**No se vio el renderizado de `laminas.html`, `hoja.html`, `guia.html` o `index.html`: Chromium abortó antes de navegar.** No hay inspección de PDF ni prueba de impresión. La imagen inspeccionada no satisface por sí sola el criterio de captura en Chromium; evita presentar archivos o gráficos diseñados como prueba de navegador.

Comprobación ejecutada: `python3 comprobar-texto.py` → 54 controles documentales OK; `node --check kit.js` y `node --check comprobar.cjs` → rc0. Dos controles negativos rechazan una muestra sin pausa y una agenda A que incumpliría los 50 minutos de inventario de B. La evidencia del intento real fallido se conserva en `comprobacion.json`, sin repetirlo con sandbox desactivado.

El siguiente paso técnico es correr `node comprobar.cjs evidencia/corrida-v2` donde el sandbox autorizado permita arrancar Chromium, conservar esa corrida, inspeccionar todas sus capturas y corregir cualquier desborde/paginación. Acceso y ensayo humanos son otra comprobación pendiente. Revisión independiente sobre el commit publicado: coordinador; esta nota es revisión propia.

# Diseño elegido por Sergio · 11 noviembre 2026

Sergio eligió «Propuesta 1» de las tres imágenes generadas y reenviadas en orden. Se implementa en el panel existente, no en otra aplicación. Referencia exacta: `exec-6812e132-9739-4613-9334-903ec7cae068.png`, conservada en el directorio privado de imágenes generadas de esta conversación. Las otras dos propuestas no son el objetivo visual.

## Alcance de esta retoma

- Retomar `cerebro-panel-usable-20261109` desde la entrega 62bdcac, preservando evidencia y worktree; un único escritor del panel.
- Cabecera azul oscuro compacta, navegación izquierda, lienzo claro, seis filas de fábricas con pasos y estado, inspector de resultados a la derecha, fechas de clase y nota del vlog. Adaptar a móvil sin desbordamiento ni controles inaccesibles.
- Las rutas, hashes, detalles técnicos y evidencia siguen consultables, pero no saturan la portada. Navegación, acceso a resultados/fuentes/versiones, formularios y consulta al cerebro deben funcionar. Los estados proceden de los datos; no copiar checks ficticios de la maqueta como hechos.
- Corregir el 403 al guardar observaciones: reproducir Origin/Referrer-Policy con navegador real y conservar validación estricta de Host/Origin, token CSRF, versiones y fuentes. No aceptar Origin nulo/ausente o cualquier origen como atajo.
- Conservar lector, tanda, contratos, persistencia privada y protección contra rutas inválidas, XSS y corrupción. No activar scheduler, n8n, servicios de producción, canales comerciales o cobros. La fecha visible usa datos y zona explícita, no una fecha fija disfrazada de actualidad.
- Usar iconos de biblioteca con licencia y recursos locales, sin dependencias de red al abrir el panel. La maqueta no tiene fotos o imágenes de contenido que necesiten generación adicional.
- Una entrega con muestra histórica o sintética debe indicarlo; no fabricar guiones v3 ni estados de las otras ramas. La integración de productos ajenos no forma parte de esta retoma de diseño.

## Comprobación y entrega

Pruebas pertinentes del panel y del guardado, navegador con sandbox en escritorio/móvil, persistencia tras reinicio y comparación visual con la imagen elegida. La comparación usa la misma dimensión y distingue cambios legítimos por datos reales. Guardar `design-qa.md`, capturas y guía de revisión en la ruta del panel. Si el sandbox de la ejecutora impide abrir Chromium, la coordinadora realiza el recorrido en el host; no desactivar protecciones ni fingir verificación.

Modelo solicitado Sol6.1 high, sin hijos. Muestra previa: 6% usado a 2026-11-11T16:55:13.615Z, no coste atribuible a esta tarea. Cero sesiones vivas comprobadas desde host antes de preparar. Revisor distinto sobre el commit exacto, dentro de los tres lugares existentes. Entregar rama y evidencia para revisión de Sergio; no aceptar/integrar productos automáticamente ni lanzar el siguiente frente.

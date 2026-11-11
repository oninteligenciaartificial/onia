# Comprobación de Propuesta 1

final result: blocked

La referencia exacta fue abierta con view_image. Chromium falló al iniciar con sandbox y produjo cero capturas de esta implementación. La comparación de fidelidad y el guardado nativo en navegador requieren el ensayo del host de la coordinadora.

## Evidencia disponible

- Referencia visual elegida y abierta en esta retoma en `diseno/propuesta-1.png`, 1487×1058 px.
- Implementación en el mismo `panel.render`, mediante `diseno.py` y `diseno.css`.
- Captura de implementación pendiente. Intento en `evidencia/diseno-20261111/intento-01/resultado.json`, resultado BLOCKED, `No usable sandbox!`.
- Estado inicial previsto para comparar · Fábricas, inspector Resultado, tanda v2 histórica y seis fábricas con datos de los contratos recibidos.
- Viewport objetivo 1487×1058 CSS px, deviceScaleFactor 1. Otras comprobaciones previstas a 1440×1000 y 390×844.
- El script `visual-diseno.cjs` genera `objetivo.png` y `comparacion.png` con referencia a la izquierda e implementación a la derecha, ambas a 1:1, cuando Chromium puede arrancar. Su generación en esta sesión quedó bloqueada.
- Comparación conjunta de vista completa pendiente. Comparaciones enfocadas de cabecera, filas, inspector y formulario pendientes. Esas regiones son necesarias por su densidad y controles.

## Superficies de fidelidad

| Superficie | Implementación preparada | Validación visual |
|---|---|---|
| Tipografía | Inter variable local, cuerpo compacto, h1 de 38 px, filas de 20 px, inspector de 24 px | Pendiente de comparar pesos, saltos y espaciado con la referencia |
| Espaciado y estructura | Cabecera de 70 px, sidebar de 186 px, filas de 106 px, inspector de 360 px, tarjeta de clases y nota del vlog | Pendiente a 1487×1058 y con datos largos |
| Colores | Cabecera #1b303e, fondo #faf8f5, crema #fff3df y acentos semánticos de las fábricas | Inferidos de la referencia abierta, pendientes de cotejo renderizado |
| Imágenes e iconos | Referencia conservada, 18 SVG originales de Tabler MIT y fuente Inter OFL incrustados desde recursos locales | Integridad/licencias comprobables por tests. Tamaño, alineación y peso visual pendientes |
| Texto y estado | Títulos de Propuesta 1, v2 histórica con alerta, fechas de fuente, ausencia de export indicada como pendiente | Diferencia intencional respecto de los ejemplos v3/checks de la maqueta. Falta inspeccionar la presentación |
| Móvil y accesibilidad | Reorganización a una columna, navegación envuelta, inspector después de filas, enlaces/radios/details nativos y foco visible | Pendientes de inspección de 390 px, navegación de teclado y control de overflow en navegador |

## Guardado e interacciones

Se cambió Referrer-Policy y meta referrer a same-origin. Host y Origin exactos, token CSRF, huella y versión esperada se conservan en el servidor. La norma Fetch explica el Origin nulo producido por no-referrer. La comprobación comparativa del navegador está preparada para forzar únicamente la política anterior en una respuesta de ensayo, observar 403 con Origin:null y después exigir 303 con el origen exacto en same-origin. [Norma Fetch](https://fetch.spec.whatwg.org/#origin-header)

Las pruebas HTTP y HTML comprueban el rechazo de origen ausente, null, wildcard, ajeno, token malo, huella y versión, además de las regresiones anteriores. El script del host comprobará navegación por secciones, selección de fábrica, pestañas del inspector, lectura de T01, formulario, reinicio y consulta del cerebro. Errores de consola y solicitudes externas quedan bajo comprobación en ese ensayo. Sólo se registran Origin, Referer y Host del formulario sintético, junto con su estado HTTP.

## Hallazgos y siguiente comprobación

La ausencia de una captura actual bloquea el juicio de fidelidad. No se asignan defectos visuales a una interfaz que no pudo observarse. Las capturas host anteriores corresponden a la entrega previa y conservan sus archivos y carácter histórico.

1. Ejecutar `visual-diseno.cjs` en el host compatible, con sandbox habilitado y un directorio nuevo.
2. Abrir `diseno/propuesta-1.png`, `objetivo.png` y `comparacion.png` conjuntamente. Revisar además desktop, mobile, mobile-completo y guardado.
3. Comparar cabecera, filas e inspector en recortes legibles de ambas imágenes y registrar cada diferencia P0/P1/P2 con su evidencia.
4. Corregir las diferencias que requieran cambios y repetir capturas a igual viewport y estado. La coordinadora debe pedir la retoma sobre esta misma tarea si corresponde.
5. Registrar la inspección y el resultado del formulario antes de cambiar el resultado de QA.

## Historial de comparación

Intento 01 de esta retoma · bloqueo de arranque de Chromium. Cero comparaciones visuales ejecutadas. Las pruebas de código y los cambios de CSS posteriores al intento conservan este bloqueo ambiental. El script queda preparado para comprobar el commit final desde el host.

final result: blocked

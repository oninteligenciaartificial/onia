# QA visual y funcional de Propuesta 1

final result: passed

Revisión de la coordinadora sobre el render existente, con Chromium y sandbox habilitado en el host. La entrega de la ejecutora 613a152 dejó este QA bloqueado por su entorno; su informe se conserva en `evidencia/diseno-20261111/qa-ejecutora-613a152.md`. La coordinadora reprodujo los fallos, corrigió el producto después de terminar la ejecutora y completó los ensayos.

## Referencia, estado y comparación

- Fuente visual: `diseno/propuesta-1.png`, 1487×1058 píxeles.
- Implementación: `evidencia/diseno-20261111/host-final-02/objetivo.png`, 1487×1058 píxeles; viewport CSS 1487×1058, deviceScaleFactor 1. Sin reescalado en los archivos de comparación.
- Estado: Fábricas, Resultado. La referencia tiene v3/checks de ejemplo; la implementación muestra la v2 histórica disponible y pendientes sin inventar progreso. Diferencia de contenido intencional.
- Vista conjunta abierta: `host-final-02/comparacion.png` (2974×1058, referencia izquierda, implementación derecha).
- Comparaciones enfocadas abiertas: `comparacion-cabecera.png`, `comparacion-filas.png`, `comparacion-inspector.png` en ese directorio. Mismos recortes y escala en cada par. Las regiones densas se leyeron por separado.
- Abiertos además: `mobile.png`, captura móvil completa anterior de igual estructura y `guardado.png`. El ensayo final confirma ausencia de desbordamiento a 1487, 1440 y 390 px.

## Hallazgos corregidos e historial

1. **P1 · guion seleccionado oculto.** `coordinadora-antes/resultado.json` conserva el fallo: el hash llega a T01 y su sección aparece, pero el artículo queda oculto. La regla de ocultar otras tarjetas tenía mayor especificidad. Se igualó la especificidad en `.scripts:has(.script:target) .script:target`. Prueba posterior: `host-final-02/guion-abierto.png` y recorrido OK.
2. **P2 · confirmación fuera del viewport.** La captura `coordinadora-antes/guardado.png` no muestra el aviso tras la navegación al resultado. Se hizo persistente el aviso durante el desplazamiento y se añadió margen al destino. `host-final-02/guardado.png` muestra la confirmación y la prueba verifica su caja dentro del viewport.
3. **P2 · tipografía de título y pasos demasiado pequeña.** Se ajustó h1 de 38 a 42 px y pasos de 12 a 14 px en escritorio. `host-final-01` confirmó el cambio y detectó corte dentro de “Confirmación”. `overflow-wrap:normal` en la etiqueta evita ese corte; `host-final-02/comparacion-filas.png` lo confirma. Móvil mantiene su tamaño adaptado.
4. **Prueba corregida, sin alterar servidor.** Cambiar sólo el fragmento no recargaba la política anterior. Se fuerza una navegación nueva y se sirve una copia del HTML de la sesión con ambas políticas anteriores. El navegador genera Origin:null y el servidor devuelve 403; la versión real same-origin devuelve 303. No se fabrica Origin ni el POST. Se evita route.fetch, que abría otra conexión contra el servidor secuencial.

Tras estas correcciones no quedan P0/P1/P2 accionables en este alcance visual/local. Los ensayos fallidos se conservan; no se contabilizan como éxitos.

## Cinco superficies de fidelidad

| Superficie | Veredicto |
|---|---|
| Fuentes y tipografía | Inter local, título fuerte, jerarquía y lectura comprobadas. Inspector deliberadamente compacto para la alerta de versión histórica. Diferencias menores de peso respecto de la imagen son P3. |
| Espaciado y ritmo | Cabecera 70 px, sidebar 186 px, seis filas, inspector 360 px, clases y vlog conservan composición y densidad. En móvil navegación y columnas se reorganizan sin controles recortados. |
| Colores | Navy, fondo cálido, crema y acentos de fábrica coherentes con la referencia. Los círculos pendientes reemplazan los checks ficticios intencionalmente. |
| Imágenes e iconos | Tabler original e Inter local con licencias; sin solicitudes de recursos externos ni iconos dibujados a mano. Peso plano de la biblioteca frente a la iluminación de la maqueta aceptado como P3. |
| Texto y contenido | Fechas y horarios confirmados, pago manual y vlog intacto. Títulos de guiones y estado histórico provienen del paquete recibido; no se copian textos ficticios de la maqueta. |

## Pruebas reales

`node "$P/visual-diseno.cjs" "$P/evidencia/diseno-20261111/host-final-02"` → `{"resultado":"OK","capturas":3,"pasos":6}`. Cinco secciones, seis fábricas, tres pestañas, T01, reproducción del rechazo 403, guardado 303, confirmación visible, reinicio y persistencia, consulta del cerebro. Cero errores inesperados de consola y cero peticiones externas. Sólo el 403 provocado y esperado se excluye del conteo; queda registrado. Los orígenes locales se redactan como loopback en el recibo.

`node "$P/visual-operacion.cjs" "$P/evidencia/diseno-20261111/host-operacion-final-01"` → `{"resultado":"OK","casos":3}`. Conserva navegación, evidencia original, revisión de fixture, reinicio y consulta desde móvil 390×844.

`python3 -B "$P/pruebas.py"` → 22 tests OK. `python3 -B -m unittest discover -s "$P" -p 'test_*.py' -v` → 33 tests OK. Total 55. Host/Origin exactos, CSRF, huella, versión, XSS, rutas y concurrencia siguen cubiertos. Los comandos y salidas resumidas están en `evidencia/diseno-20261111/coordinadora.json`.

No equivale a una auditoría completa de lectores de pantalla ni prueba de canales reales. Se mantiene el STOP para Sergio; este QA no acepta ni integra la entrega. Sin n8n, publicación comercial, pagos, PC o instalación de software.

## Checklist final

- [x] Referencia y render abiertos juntos, regiones legibles y móvil inspeccionados.
- [x] Fallos encontrados corregidos y recapturados.
- [x] Formularios y persistencia verificados en navegador, protecciones conservadas.
- [x] Estados de ejemplo separados de evidencia real.
- [ ] Revisión independiente y decisión de Sergio, gestionadas por el harness.

final result: passed

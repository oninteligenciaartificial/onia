# Control visible del reproductor de YouTube · 9 de noviembre de 2026

**El botón oficial apareció y el clic se completó. Después se verificó el inicio del contenido, que volvió a detenerse en 00:43.760.** La prueba verificó que el navegador del VPS puede detectar y operar ese control cuando YouTube lo muestra. El objetivo de 90 segundos continuos quedó pendiente. [Video fuente](https://www.youtube.com/watch?v=JuAQILH7dkQ)

| Medida | Resultado observado |
| --- | --- |
| Botón para omitir | Visible y habilitado en el DOM del reproductor. 1 intento, 1 clic completado y 0 fallos. |
| Transición | La marca publicitaria desapareció después del clic. A los 6.315 s desde el inicio del tramo publicitario, se verificó contenido del ID autorizado, duración de 1802.921 s y avance de su reloj. |
| Captura inspeccionada | Recorte de `#movie_player` entre 00:25.129 y 00:25.337. Se ve el panel Fábricas de Euge. Los puntos de 00:55 y 01:30 quedaron sin captura. |
| Avance | Posición máxima 43.760 s. El contador histórico registró hasta 43.287 s de avance entre muestras sin saltos grandes. La corrida no acredita continuidad con el criterio corregido. |
| Estado final | Medio vacío y pausado, `readyState=0` y `networkState=0`, mismo ID y sin publicidad. Dos clics Play completados en el ensayo, sin recuperar el avance final. |
| Red multimedia | 22 respuestas observadas, ninguna HTTP 4xx/5xx. 6 fallos `net::ERR_NAME_NOT_RESOLVED`. El ensayo no estableció la causa del corte. |
| Visor | Verificado en el VPS como `listo`, Chromium humano restaurado y mismos procesos Xvfb, VNC y Web. |

La aparición y la acción del botón se verificaron mediante DOM y transición del reproductor. La captura inspeccionada corresponde al contenido posterior. La prueba fue de control y muestreo visual, con el audio y el visionado completo fuera de la cobertura. YouTube distingue anuncios que ofrecen omisión y anuncios que se reproducen hasta el final. El control aplica la comprobación normal de acción de Playwright. [YouTube](https://support.google.com/youtube/answer/2467968?hl=es), [Playwright](https://playwright.dev/docs/actionability)

## Reproducción técnica

El ensayo único se ejecutó entre 11:27:33 y 11:29:19 UTC mediante `python3 -B work/video-control-20261109/ejecutar.py`. El manifiesto y la captura se conservan en privado. Los hashes y el recibo terminal permiten cotejar los archivos.

Los bytes ejecutados se conservan en `control.ejecutado.cjs` y `ejecutar.ejecutado.py`. La variante publicable separa el inventario del botón y el clic, limita el clic a un anuncio activo y excluye controles transparentes y controles dentro de ancestros transparentes. También compara el avance acumulado del medio con el reloj monotónico del tramo. `objetivo_control_cumplido` queda separado de la cobertura visual. Incluso una prueba de 90 segundos exitosa produce estado visual `parcial`. Se verificaron estas correcciones con datos sintéticos tras el único ensayo real.

```bash
node --check work/video-control-20261109/control.cjs
node work/video-control-20261109/probar.cjs
node work/video-control-20261109/probar-cobertura.cjs
```

La primera prueba de comportamiento usa Chromium sandbox en el VPS y sólo páginas sintéticas. Comprueba controles ausentes, ocultos, transparentes, bajo ancestros transparentes, deshabilitados, fuera del reproductor y presentes sin anuncio. También verifica un clic permitido y el caso en que la publicidad termina entre la observación y la acción. La segunda usa un reloj monotónico simulado y comprueba 90 segundos de avance concordante, saltos, interrupción y una secuencia de medios demasiado rápida para el reloj. También se comprobó en Python que un vencimiento conserva `parcial` o `sin_fotogramas` y deja sin acreditar el objetivo. Se reutiliza el gestor de visor existente y el guard de destino importado de `muestra-seek-anterior.cjs`.

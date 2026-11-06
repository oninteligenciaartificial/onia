# Cierres de cinco ampliaciones · revisión de cuadros finales

5/11/2026. Root amplió la brecha del último medio segundo reconocida en [ampliaciones](ampliaciones-pedro-erik-toto.md). Extrajo todos los cuadros decodificados desde 0,6 s antes del final del contenedor hasta EOF con `-copyts`, sin filtro fps, y los inspeccionó en cinco hojas: **74 cuadros**, algunos ya presentes en el muestreo previo. PTS conservados por `showinfo`, no tiempos nominales calculados desde el índice de hoja. No se volvió a decodificar íntegro el medio ni se escuchó.

| Medio | Cuadros / PTS primero–último | Cierre observado |
|---|---|---|
| DehhvYDAWDl | 14 / 101,167835–101,601602 s | Saludo con sombrero; el texto de identidad desaparece antes del último cuadro; no aparece placa CTA adicional en este intervalo. |
| Dem097KgI-A | 11 / 74,333333–74,750000 s | Presentador, keyword Escala y subtítulo que remite al privado, conservados al final. |
| DepdNr4mWs1, entrada9 | 18 / 5,300000–5,866667 s | Acción de boxeo y texto SISTEMA/webinar constante; no nueva tarjeta. No tiene pista de audio en la representación recuperada. |
| Toto LinkedIn | 17 / 60,033333–60,566667 s | Portátil con llamada y subtítulo de seguir; la cámara se desplaza pero no aparece otra oferta antes del corte. |
| Erik zXHJ-IJ59AM | 14 / 495,666667–496,100000 s | Placa de continuidad con dos espacios y círculo oscureciéndose; el último cuadro aún conserva restos muy oscuros del gráfico. No se certifica negro PCM ni silencio a partir de oscuridad visual. |

Cada hoja fue abierta íntegra. [Manifiesto, PTS y archivos](../../../operacion/referentes-20261105/video/cierres-ampliaciones/manifest.json); logs/hojas en la misma carpeta. La diferencia entre último PTS de video y duración del contenedor no se interpreta como congelación o desfase: puede incluir duración de audio/padding. El último cuadro observado aquí es el último que devolvió la decodificación del tramo hasta EOF.

Esto completa la inspección del tramo final omitido en esas representaciones, no todos los cuadros anteriores ni acústica. Permanecen muestreo global y dudas verbales descritos en las fichas; Los tres ASR cortos ya están completos y leídos en guiones-faltantes.md; no hay cola activa.

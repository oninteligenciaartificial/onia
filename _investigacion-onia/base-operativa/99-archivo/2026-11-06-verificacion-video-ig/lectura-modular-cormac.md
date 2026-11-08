# Cormac: cortes y textos por la ruta modular

**Resultado:** extracción y PTS comprobados, tres cortes de contenido y dos reencuadres abruptos. OCR raw no fiable: **1/6 coincidencias literales**. Se reutilizó el ASR; no hubo nuevo modelo AV/audio ni escucha.

Pieza única: Cormac Hayden, `cormachdn`, DfWLWspIruU. [Ficha](FICHA-CORMAC.md). El original conserva SHA 9be4267480093249e104ec9821271e1a755e4329b7ea4d8fca3fc8bacd3b664e.

## Cobertura y edición

Se procesaron **2.264/2.264 frames**, sin salto temporal, a 720×1280 para el score. PTS=256×índice, base1/15360, 60fps. La confirmación usa vecinos nativos1440×2560, con PTS cotejados por showinfo. No equivale a observar manualmente todos los cuadros.

Último frame:37,716667s; **fin del vídeo:37,733333s**; contenedor:37,753991s. No se confundieron esas duraciones.

| Cambio | PTS | Frame | Clasificación visual |
|---|---:|---:|---|
| Cara→escritorio |3,466667s|208|Corte de contenido persistente|
| Escritorio→repositorio |7,2s|432|Corte de contenido persistente|
| Repositorio→repositorio |9,466667s|568|Reencuadre abrupto|
| Repositorio→cara |14,666667s|880|Corte de contenido persistente|
| Cara→cara |21,666667s|1300|Reencuadre abrupto|

El cambio se localiza entre frame anterior/actual, separados1/60s; las hojas incluyen también el siguiente y se conservan ±2 nativos. Umbral primario10: cinco candidatos. No se certifica su técnica de producción.

| Bloque de contenido | Intervalo | Duración |
|---|---|---:|
| Gancho del presentador|0–3,466667s|3,466667s|
| Escritorio|3,466667–7,2s|3,733333s|
| Repositorio/documentación|7,2–14,666667s|7,466667s|
| Explicación/cierre del presentador|14,666667–37,733333s|23,066667s|

Al separar los dos reencuadres principales, repositorio se divide en2,266667+5,2s y el último bloque en7+16,066667s. Son intervalos entre fronteras observadas, **no un conteo exhaustivo de planos**.

Tres picos subumbral —18,033333;29,666667;34,933333s— muestran saltos de postura/manos/encuadre compatibles con jumpcut/reencuadre. Los pares anterior/actual no resuelven montaje frente a movimiento rápido ni persistencia posterior. Otros cuatro puntos revisados corresponden a mano9,966667s, cámara11,833333s y scroll13,166667/14,5s, sin corte confirmado. [Scores completos y anotaciones](modular-cormac-v1/cuts-reviewed.json); [hoja de ejemplo](modular-cormac-v1/cut-208.png).

## Textos: referencia previa y OCR

La referencia visual de un agente fresco quedó congelada **antes** del OCR, con hashes de seis recortes. No es certificación humana. b/d incluyen fragmentos truncados fuera del texto principal. Tesseract5.5, inglés, OEM1/PSM7, sin reescalado ni tuning posterior:

| Caso | Lectura visual previa | OCR literal | Exacto |
|---|---|---|---|
|[a](modular-cormac-v1/crop-a.png)|please tell me|please tell me|Sí|
|[b](modular-cormac-v1/crop-b.png)|i gave my ai access|eeigave y ai access \||No|
|[c](modular-cormac-v1/crop-c.png)|agent-desktop Public|. agent-desktop »vbiic|No|
|[d](modular-cormac-v1/crop-d.png)|Serendipity|(vacío)|No|
|[e](modular-cormac-v1/crop-e.png)|emails and messages|emails and meggages|No|
|[f](modular-cormac-v1/crop-f.png)|(vacío)|—a|No|

Se pueden usar las lecturas visuales etiquetadas, conservando el OCR crudo. Su confianza no es probabilidad; el negativo produjo caracteres conconfianza0. La familia tipográfica exacta sigue desconocida. [Referencia](modular-cormac-v1/ocr-reference.json) y [TXT/TSV, coordenadas y errores](modular-cormac-v1/ocr-results.json).

## Qué aprendemos

- El gancho conduce al escritorio en3,47s y luego a una referencia técnica: persona→demostración parcial→herramienta. Mostrar un resultado final verificable mejoraría la prueba comercial; no se midió retención.
- Dedo, scroll y texto duplicado dificultan leer la pantalla física. Una captura digital estable es una mejora propuesta, no ejecutada.
- Scores y OCR requieren cotejo: gesto/subtítulo no implica corte; texto legible para visión puede salir corrupto o vacío en OCR.

Scan15,59s; seisOCR1,76s; suma de13etapas67,80s, algunas paralelas. RSS máximo muestreado242.540.544B. Afinidad2CPU, AS3GiB/CPU120s por proceso y wall120s; memoria agregada muestreada, no cuota dura. Tesseract aislado en WSL, UID1000, sin sudo/global/servicios;11paquetes APT verificados,5.763.764B. [Recursos](modular-cormac-v1/resource-summary.json).

Dictamen: evidencia instrumental y lectura seleccionada aceptadas; OCR autónomo, detector exhaustivo, música/efectos/prosodia/mezcla/sincronía fina no acreditados. [Revisión](../../04-operacion-agentes/evidencias/capacidad-audiovisual-001/revision-modular-cormac-v1.json). Siguiente: cerebro existente con estos límites; después plan full Cloud.

# Recibo de ejecutora

Encargo `fabrica-edicion-video-20261110`, 10 de noviembre de 2026 UTC. Entrega técnica preparada para revisión independiente por el coordinador.

## Sesión y alcance

| Campo | Evidencia |
|---|---|
| Rama asignada | `codex/ws-fabrica-edicion-video-20261110` |
| HEAD inicial | `d22b0b29f62e1403d84571b7602c9eb55ec91575` |
| Estado inicial | Worktree limpio |
| Modelo/esfuerzo solicitado en el briefing | `gpt-6.1-sol`, `high` |
| Modelo/esfuerzo observado por SID | Desconocido, esta sesión carece de metadatos verificables del runtime por SID |
| Cuota semanal inicial | Desconocida al control de 2026-11-10T20:22:44Z |
| Cuota semanal final | Desconocida al control de 2026-11-10T20:34:02Z |
| Reserva semanal ≥10% | Comprobación pendiente del coordinador, que controla los lanzamientos |
| Intentos de sesión | Un intento ejecutor, revisión independiente pendiente del segundo cupo autorizado |
| Hijos | Cero |
| Resultado | CLI y pruebas sintéticas satisfactorias, pendiente de revisión técnica distinta |
| Commits | Base indicada arriba. El hash de entrega es el commit que contiene este recibo y se comunica tras publicar la rama |
| Retrabajo | Ajustes y ampliación de pruebas dentro del mismo intento |

Se leyeron AGENTS, ESTADO, reglas-comunes, boss-memoria, ORQUESTACION, el manifiesto de selección, la directora canónica, la especificación de fábrica 2, el pedido delegado, las decisiones comerciales pertinentes, arquitectura, el piloto ASR y el código del lector/panel existente. La directora `desarrollar-y-verificar` estaba anunciada en el catálogo y se leyó su fuente editable. Las fuentes del registro y briefing conservaron su autoridad en el coordinador.

## Entrega y criterio comprobado

| Requisito | Comprobación |
|---|---|
| CLI reproducible | `procesar.py` usa un plan JSON y produce un directorio nuevo por ejecución |
| Esquema | `intervalos.schema.json`, validación estructural/temporal en el CLI |
| Cortes | Fuente sintética de tres segundos, elimina el tramo verde y concatena rojo/azul |
| Duración y frames | Salida de 2,000 s y 60 frames, resolución de prueba 360×640 |
| Vertical predeterminado | Prueba por entrada normal del CLI con 720×1280 |
| B-roll explícito | Apoyo amarillo de 0,5 a 1,0 s de salida, comprobado por píxeles en el centro |
| Audio conservado | Frecuencias medidas 435/435/880 Hz dentro de tolerancia de 10 Hz para tonos esperados 440/440/880, incluida la ventana B-roll |
| Reproducibilidad | Dos renders byte a byte iguales, SHA-256 `3db593dfe00502d6d4a817343ba15eedaed707d30a848a1887cfcdf3b4b2b959` |
| Subtítulos | Dos líneas de hasta 14 caracteres. Máscara de 30 frames, caja blanca `[73,537,286,568]` en 360×640, dentro de márgenes |
| Originales | Hash de fuente conservado y rechazo de salida ya ocupada |
| Fallos | Entradas/ASR ausentes, JSON inválido, intervalos fuera de rango/solapados, NaN, booleanos, vlog, manifest B-roll inválido y cortes sobre frases |
| ASR CPU | Fixture de seis segundos con voz flite, small cacheado, CPU/int8/dos hilos/VAD/beam5, un segmento y render de 6,000 s |
| Reporte | Hashes, intervalos pedidos/aplicados, duración, dimensiones, dudas y tiempos de ASR/render |
| Dependencias | FFmpeg/ffprobe 6.1.1, Python 3.12.3, faster-whisper 1.2.1, CTranslate2 4.8.5, PyAV 18.1.0 y DejaVu Sans presentes |

Comando vigente desde la raíz del repo.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110
PYTHONDONTWRITEBYTECODE=1 python3 "$D/pruebas.py"
```

La ejecución final pasó **11/11 pruebas en 12,890 s**, con cero fallos y cero errores. Las 12 variantes de entradas inválidas se ejecutan como subcasos de una de esas pruebas. La evidencia vigente está en [pruebas-04.json](pruebas-04.json). También se compilaron los tres archivos Python en memoria y se parseó el esquema con stdlib.

## Ajustes del mismo intento

1. `pruebas-01.json` conserva 9 pruebas satisfactorias del editor y rechazos.
2. `pruebas-02.json` conserva 10 pruebas satisfactorias al añadir el recorrido ASR con voz sintética.
3. `pruebas-03.json` conserva 11 pruebas satisfactorias al añadir la resolución predeterminada y comprobar frecuencias de audio por tramo.
4. `pruebas-04.json` vuelve a pasar las 11 tras acotar el alfabeto latino, validar confianzas, conservar la relación de aspecto mediante DAR y separar tiempos de ASR/render.

Estas corridas son verificaciones del mismo trabajo. Cada recibo anterior conserva sus bytes. Los fixtures se generan de nuevo y sus carpetas temporales propias se retiran al terminar.

## Decisiones y pendientes

- Se eligió encuadre completo con bandas y redondeo de cortes a 30 fps. El reporte conserva extremos pedidos y aplicados. Una frase atravesada por un corte se rechaza para ajuste humano. Los subtítulos largos tienen tiempos internos estimados y una duda visible.
- El panel existente acepta un catálogo cerrado de tres tareas. Esta entrega conserva el circuito de fábrica 2 con revisión desde la carpeta privada. Incorporar el recibo automáticamente al panel requiere autorización de sus rutas y trabajo posterior del coordinador.
- Falta el medio real de G01. Boss/Sergio deben colocarlo en la cola privada junto con intervalos y apoyos explícitos. Contenido ajusta los cortes y coteja transcripción. Sergio revisa encuadre, sonido y sincronía. Se retoma esa validación al recibir el material.
- El fixture de voz acredita ejecución ASR, y las máscaras/mediciones acreditan controles instrumentales sintéticos. La precisión ASR sobre material real y la validación audiovisual/editorial completa quedan pendientes.
- El coordinador debe cotejar cuota/modelo observados, cerrar la entrega publicada, recoger revisión distinta del commit exacto y gestionar aceptación e integración. La publicación en esta rama habilita ese próximo paso.

Huellas del código comprobado en la última suite.

| Archivo | SHA-256 |
|---|---|
| procesar.py | `411c165d250bc764762fb81ae202d9b150e7d54702f8bf6731d56fee74c96bac` |
| asr_offline.py | `701c4196b8c182ae1a1f3a7add93915ea4735f0c2a0a09807c858e93746f3fce` |
| pruebas.py | `72142b1dd28a372db8bf2f97c0349112e0db7264edf71309846cd4b31a7db966` |
| intervalos.schema.json | `e02e9d1eec600fd9f0ee6b952614f0c220483a4674c4de3c389b4b0b10848e6b` |

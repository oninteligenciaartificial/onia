# Dictamen de la pasada sincronizada · seis-areas-cloud-001

7 de noviembre de 2026, America/Caracas. Dentro de la ventana objetivo de 12:22:00 a 12:22:15 UTC se acreditaron **cinco de seis ejecuciones**. Todas las ejecuciones acreditadas ocurrieron en Cloud. Los resultados de la primera pasada se conservan en [revisión v1](revision-v1.md).

| Área | Intervalo UTC a partir de 12:22:00 | Resultado |
|---|---:|---|
| Desarrollo | 0–54 ms | Salida 2 esperada por revisión obsoleta. r2 y hashes conservados. |
| Organización | 0–29 ms | Una fila temporal r2→r3 y repetición sin escritura. Cero escrituras en Notion. |
| Marketing | 1–67 ms | Comprobaciones del CSV y recibos A/B correctas. Nueve unidades y 56,50 ficticios. |
| Video | 0–518 ms | Metadatos comprobados y decodificación del MP4 existente completada. |
| Producto | 11–24 ms | Cuatro casos correctos sobre el módulo de Platform recuperado. |
| Automatizaciones | 111–267 ms | Intento excluido. El lanzador salió 1, reportó `EPERM` y dejó ambas salidas vacías. El campo interno `exit_code: 0` no acredita las comprobaciones. |

El máximo solape según las marcas reportadas es **5 en Cloud y 5 en total**. La intersección comienza con Producto a las 12:22:00.011 UTC y termina con ese mismo tramo a las 12:22:00.024 UTC. El cruce dura **13 ms** y excluye la espera previa, el intento fallido y los despachos. La pasada carece de fallback local. Se cotejaron los resultados compactos de las seis sesiones y se recalculó la intersección con los [recibos integrados](recibos-sincronizados-v1.json), SHA-256 `bda1d41c898ae4229c0506db7a6cc57350461cd86c77def24e082753fa73faa1`.

El cálculo usa ventanas instrumentadas y relojes de hosts distintos. El desfase entre relojes quedó sin medir, por lo que el intervalo representa el solape de las marcas UTC reportadas. La simultaneidad física de CPU y la capacidad máxima sostenida requieren otra evidencia.

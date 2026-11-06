# QA técnico de 6 MP4 secundarios

5/11/2026, America/Caracas. FFmpeg 8.1.1; ejecución secuencial con un proceso y opciones de threads del decodificador, salida y filtros en 1. No se modificaron medios, subtítulos o índices raíz. **No es visionado ni escucha.**

| ID | Duración video (s) | Duración audio (s) | Frames metadata / decodificados | Decode (s) | Resultado |
|---|---:|---:|---:|---:|---|
| anrAaNvbp4M | 1266.433333 | 1266.454000 | 37993 / 37993 | 33.969 | Completo sin errores |
| oFYznV9EYPg | 1268.400000 | 1268.414000 | 38052 / 38052 | 38.328 | Completo sin errores |
| 4jWLq8Gn_4Y | 1525.166667 | 1525.234000 | 45755 / 45755 | 40.391 | Completo sin errores |
| SVHKZkD1r_A | 1681.846833 | 1681.874000 | 40324 / 40324 | 62.579 | Completo sin errores |
| c4S0EJAdL5I | 2040.271567 | 2040.294000 | 61147 / 61147 | 71.141 | Completo sin errores |
| oZ9UKXve3Dk | 1380.233333 | 1380.294000 | 41407 / 41407 | 77.86 | Completo sin errores |

Los time bases, start times, duration_ts y duraciones exactas declaradas por cada stream están en sus archivos `.ffprobe.json` y `.qa.json`. Los frames finales provienen de `-progress` con fps passthrough; no se infiere duración sólo del nombre o título. Diferencias entre duración de audio y video no prueban desfase perceptual.

| ID | Bytes | SHA-256 |
|---|---:|---|
| anrAaNvbp4M | 56809556 | `652ad1aed916302b9cccaecaf2de81a59969db3de708ab27f12dba883035d567` |
| oFYznV9EYPg | 120381380 | `e3842457c97dca76afc7d1aa1f8c85a94ccbb2eea2d32eeab1b1019751c42c7d` |
| 4jWLq8Gn_4Y | 51252918 | `1228cf7242127091d28c8199e750a26c850b1f381017dad1ce4d61cb14398646` |
| SVHKZkD1r_A | 133841059 | `722555991b92c81fe5931476161ef60cb9baa79f1dfbfc615a33cf538cd04bcc` |
| c4S0EJAdL5I | 217667068 | `1eee8d9d1d24c2ce67ccf4eb0b1f8c48cf0c8491bcfce4b125c1f466ad53d6b9` |
| oZ9UKXve3Dk | 194641070 | `6179d99a8506859e984af9d99a819005e8a3786ec9309b66b99762ef6fddc751` |

Tiempo acumulado de las ejecuciones: 325.469 s (incluye hash/probe/decodificación). Los tiempos de la tabla son sólo ejecución FFmpeg. Código de salida 0, stderr vacío y progress=end en todos los archivos; tamaño y fecha de modificación de las fuentes permanecieron iguales durante su comprobación.

[Evidencia conjunta](resultados.json) · [Cotejo de frames](cotejo-frames.json) · [Ejecutor](verificar_medios.py). Cada fuente tiene log `.decode.stderr.txt` y progreso `.decode.progress.txt` conservados.

Cierre: verificación técnica de extracción cumplida para estos archivos. Siguiente paso: Video/Aprendizaje usan esos medios y los subtítulos/ASR del lote para su revisión de contenido; no extender este resultado a calidad audiovisual, comprensión ni escucha.

Ampliación incremental: se conservaron anrAaNvbp4M, oFYznV9EYPg, 4jWLq8Gn_4Y, SVHKZkD1r_A sin repetir decodificación; sólo se ejecutaron c4S0EJAdL5I, oZ9UKXve3Dk. Tiempo de ampliación: 149.594 s. Huella canónica de los registros preservados en resultados.json.

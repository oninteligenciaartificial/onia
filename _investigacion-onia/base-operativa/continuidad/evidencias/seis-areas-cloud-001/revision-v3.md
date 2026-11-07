# Dictamen de la última pasada sincronizada · seis-areas-cloud-001

7 de noviembre de 2026, America/Caracas. Las seis áreas completaron trabajo verificable en Cloud dentro de la ventana de 15 segundos iniciada a las 12:26:50 UTC. Cada bloque de trabajo medido duró entre 0,400 y 0,666 s. Se conservan los resultados de [v1](revision-v1.md) y [v2](revision-v2.md).

| Área | Intervalo UTC relativo a 12:26:50 | Evidencia |
|---|---:|---|
| Desarrollo | 0,175–432,398 ms | Diez rechazos esperados por revisión obsoleta con r2 y hashes conservados. |
| Organización | 0,187–400,723 ms | 906 actualizaciones de copias sintéticas y 906 repeticiones sin escritura. Una fila por copia en r3. |
| Marketing | 0,257–440,150 ms | Siete cotejos correctos de CSV, recibos y referencias. |
| Video | 0,139–666,566 ms | Metadatos verificados y decodificación completa del MP4 existente. |
| Automatizaciones | 15–464 ms | Cinco invocaciones directas de `node /tmp/onia-13311ee/test-code.cjs` correctas. Salida 0 y comprobaciones aprobadas. Cotejé la salida original `exec-a0160946-954b-4324-a79c-d111c1c7fc08`. |
| Producto | 7–408 ms | Repeticiones de los cuatro casos sobre el mismo módulo. El conteo corresponde a pasadas del fixture. |

El mayor inicio es el de Automatizaciones a las 12:26:50.015 UTC. El menor fin es el de Organización a las 12:26:50.400723 UTC. La intersección es de **385,723 ms nominales**, aproximadamente **386 ms**, con un máximo de **seis en Cloud y seis en total**. El cálculo excluye la espera anterior a la ventana. Cotejé las seis salidas compactas con los [recibos integrados](recibos-sincronizados-v2.json), SHA-256 `e691a39d272497e448ba612498175d9657e34660530551394de41ea2c97d8ba0`.

Algunas marcas tienen resolución de 1 ms y el desfase entre relojes quedó sin medir. El dictamen acepta el solape de ventanas de trabajo según los relojes reportados. La concurrencia sostenida, la simultaneidad de CPU y el límite de capacidad permanecen sin medir. Las repeticiones de fixtures acreditan este bloque breve en los ejecutores observados.

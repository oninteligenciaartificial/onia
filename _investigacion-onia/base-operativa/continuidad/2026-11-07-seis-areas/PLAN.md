# Ensayo de ejecución de las seis áreas ONIA

7 de noviembre de 2026. Sergio pidió lanzar las sesiones juntas y exigir ejecución comprobable. Una prueba por área en una misma tanda. Integración y Revisión locales supervisan con recibos compactos. El panel de producción y los servicios reales quedan fuera del entorno de ensayo. [Ensayo previo de dos áreas](../evidencias/panel-cloud-001/INFORME.md)

| Área | Ejecución y salida | Criterio |
|---|---|---|
| Desarrollo | Crear un encargo sintético en una copia, registrar un artefacto, llevarlo a revisión y probar revisión obsoleta. | Retoma íntegra, evidencia presente y rechazo efectivo del cambio obsoleto. |
| Organización | Actualizar la tarjeta sintética privada de Notion de r2 a r3 y repetir la misma sincronización. | Mismo ID, una tarjeta, revisión y próxima acción releídas, panel real intacto. |
| Marketing | Escribir un brief de dos aperturas para la primera pieza y ejecutar una comprobación de su respaldo contra los recibos A/B. | Archivo creado, CTA identificable y cifras cotejadas con el caso ficticio, sin atribuir resultados comerciales. |
| Video | Renderizar un MP4 vertical de 5 s a partir de la tarjeta de prueba. | `ffprobe` comprueba dimensiones, duración y códec. Entregar ruta, SHA y comando. |
| Automatizaciones | Ejecutar el JavaScript existente de los nodos Code con fixtures aislados. | Caso sintético aceptado, entrada ajena rechazada, bigint conservado como texto y stub sin envío. |
| Producto | Ejecutar la función real de normalización de WhatsApp en el repo ONIA Platform con casos sintéticos. | Casos válidos e inválidos verificados con `node:assert`. Checkout y producción conservados. |

Base para las cinco áreas del harness `13311ee80e1c83c9b68639c0a13aa3404a1cd037`, rama privada `codex/panel-cloud-20261107`. Producto identifica su propio commit. Cada sesión verifica runtime, repositorio y skill pertinente. Cada salida se escribe en un directorio propio. Los únicos cambios externos del ensayo de Organización se limitan a la tarjeta privada de prueba ya creada. Los casos usan entradas ficticias y herramientas disponibles. El runtime de n8n, el envío real y el corte final con grabación son pruebas de otro alcance.

La aceptación por área exige host observado, comando o acción ejecutada, resultado, criterio y evidencia. Registrar UTC antes del trabajo efectivo y al terminar la verificación. Se calcula el máximo solape de intervalos válidos por separado para Cloud y para la tanda mixta. Un mensaje despachado, una lectura y un intento bloqueado no cuentan como ejecución. Si Cloud carece de ejecutor usable, se conserva el bloqueo y se usa la sesión local equivalente para comprobar la función cuando sea viable, con recibo separado.

Integración recoge resultados y artefactos compactos. Revisión coteja la evidencia y la separación de recursos antes de aceptar. Coordinación conserva un registro único de la tanda y el resumen de resultados. No se interpreta el ensayo como un límite de cuota ni como operación permanente.

## Pasada sincronizada

Una vez completadas las pruebas funcionales, las seis sesiones reutilizan sus entradas y salidas en un solo control corto con inicio UTC común y ventana de 15 segundos. Desarrollo ejecuta el control de revisión, Organización actualiza una proyección aislada por ID, Marketing repite sus assertions de respaldo, Video decodifica el MP4, Automatizaciones ejecuta su runner y Producto repite los casos del módulo real. La espera previa queda fuera de la medición. Se informa cuántas áreas ejecutaron dentro de la ventana y el máximo solape de sus intervalos efectivos como dos medidas distintas. La sincronización de esta pasada es una prueba dirigida.

La primera pasada sincronizada encontró un `EPERM` en el lanzador de Automatizaciones. La comprobación final sustituye ese lanzador por invocación directa desde el shell. Se conservan los recibos anteriores. Cada sesión repite su comprobación real durante una carga breve de alrededor de 400 ms, sin pausa dentro de la ventana medida y con límite de tres segundos para el bloque. No se repite la escritura en Notion ni se generan nuevos medios. El solape se calcula a partir de marcas UTC de los ejecutores, con su precisión y límites declarados.

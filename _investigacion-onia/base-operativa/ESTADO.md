# Estado operativo de ONIA

3 de noviembre de 2026, America/Caracas. Leer [reglas comunes](reglas-comunes.md). El histórico está en [evidencia técnica](EVIDENCIA-2026-11-03.md); no hace falta cargarlo en cada encargo.

## Decisión vigente

Usar Codex Cloud **onia** y repo privado **oninteligenciaartificial/onia** para el harness. ONIA Platform conserva su repo y producción. ONIA-CENTRAL está excluido. El VPS conserva startup y n8n, sin agregar navegadores, render ni workers. Grok Bot Premium sigue sin cuota; se difiere.

Sergio pidió seis chats cloud por área y luego acotó sus primeras tareas a pruebas concretas. Están creados en [SESIONES.md](SESIONES.md). Terminadas las pruebas de ejecución, pidió organizar su rutina. Sus hábitos, horarios y finanzas se conservan en Organización y sus archivos privados, fuera de Git.

## Resultado comprobado

| Componente | Evidencia y límite |
|---|---|
| Harness | Preparación y sesión nueva en 9a3d4ce: doctor y 28/28 tests Python sin skips. Helper Meta en 9972d26: seis pruebas adicionales aprobadas también en cloud. |
| Skills | Nueve fuentes propias, nueve enlaces del checkout y nueve de /workspace; una sola fuente y bootstrap idempotente. Los seis chats aplicaron la skill por archivo según el área. **El catálogo nativo inicial no anunció las skills propias.** La instrucción de inicio está guardada; no se atribuye una autodetección que no se observó. |
| Navegador | Chromium: clic, cambio de estado y captura inspeccionados en sesión nueva. No prueba login social ni persistencia de cookies. |
| n8n | GET HTTP 200 desde preparación y sesión nueva; diez flujos en página, siete activos y más páginas. Sólo lectura. |
| Meta Ads | GET HTTP 200 en editor cloud con versión publicada actual: dos cuentas, estado 1, USD, sin página siguiente. Sin modificar campañas. |
| Higgsfield y Google | Higgsfield perfil/workspace Pro y 585 créditos observados, sin generación; Gmail perfil sin correos leídos; Calendar perfil/listado y lectura del 4-nov sin crear eventos; Drive ONIA con cuatro carpetas. Sin transferencia de medios entre VMs probada. |
| Video | HyperFrames 0.9.10 en VM cloud: MP4 sintético H.264, 1080×1920, 6s, 30fps, 180 frames, sin audio. Decodificación y revisión visual independientes. No es una pieza comercial con grabaciones reales. |
| Automatizaciones | Cuatro casos sintéticos de validación/idempotencia en memoria dentro de VM cloud. Sin ejecución de workflow n8n ni persistencia/concurrencia acreditadas. |
| Marketing | Ficha y guion ficticios como prueba de skill. Sin oferta adoptada, publicación, envío ni gasto. |
| Producto | Lectura GitHub de onia-platform en a0488f0 e instrucciones. Sin ejecutar código, migración, cobro o despliegue. |
| Organización | Perfil, rutina con variantes y tracker semanal privados, inicialmente sin hábitos cumplidos. Propuesta revisable; ningún evento creado. |

## Secretos y versiones

N8N_API_KEY y META_ADS_ACCESS_TOKEN están en **Secretos de red del propio entorno onia**, cada una limitada a su dominio; ver [accesos.md](accesos.md). No pedir sus valores ni volver a crearlas.

La VM Desarrollo nació antes de cargar Meta: versión 6aeaa015725c81a3b2c5e7817fca85a6, sólo n8n. No tiene herramienta oficial para actualizar esa misma instancia sin reconstruirla. Meta HTTP 200 corresponde a la versión publicada posterior 6aeaa134fa1881a3abd0f72ea0bd00f4, comprobada en el editor. Un encargo que use Meta necesita ejecución nacida de la versión actual.

## Siguiente trabajo

Aplicar y ajustar la rutina en **ONIA · Organización diaria**, con un resultado diario y una primera demostración grabada por Sergio. Tres videos diarios siguen siendo meta de producción; falta probar materiales reales y una reserva de clips.

No ampliar infraestructura para empezar. Las nueve skills y decisiones sobre los treinta candidatos están en [SKILLS-POR-AREA.md](SKILLS-POR-AREA.md); el procedimiento en [ORQUESTACION.md](ORQUESTACION.md). Una tarea cloud iniciada puede trabajar con sus entradas; **no hay scheduler cloud diario, publicación social automática ni integración n8n→Codex acreditados**.

privado/ y operacion/ no viajan por Git. Los artefactos están en las VMs/chats de SESIONES.md; recuperar un medio real o contexto privado desde otra VM sigue pendiente. Versionar sólo la entrega saneada y comprobar acceso a los materiales necesarios.

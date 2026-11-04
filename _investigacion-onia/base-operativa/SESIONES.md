# Chats de trabajo por área

Creados por pedido de Sergio el 3 de noviembre de 2026. Los seis usan **Codex Cloud, entorno onia**, repo del harness `oninteligenciaartificial/onia`, host durable. Sus instrucciones comparten esta base; no se duplican reglas por proyecto. El código del producto permanece en su repo independiente.

Sergio acotó la primera tanda a **pruebas concretas completamente cloud**. Los borradores comerciales o personales producidos durante la prueba no se adoptan ni se publican. Después de aceptar las pruebas, se organiza la rutina y el trabajo real.

| Chat | ID | Skill del área | Prueba inicial |
|---|---|---|---|
| ONIA · Desarrollo cloud | `01a1a484-065a-76bc-94a2-9b2b148d6021` | desarrollar-y-verificar | Arranque, 28 tests, navegador y n8n; luego lectura Meta. |
| ONIA · Marketing y ventas | `01a1a484-2da0-7440-8502-dfae74ab901f` | preparar-oferta-y-embudo; preparar-campana-meta para anuncios | Leer la skill y producir ficha/guion ficticios, sin publicación. |
| ONIA · Video y contenido | `01a1a484-560e-72bb-8d5d-e64733c22027` | producir-video | Render sintético vertical de seis segundos con HyperFrames dentro de la VM. |
| ONIA · Automatizaciones n8n | `01a1a484-81ca-7605-ab7e-243b8e1f4001` | automatizar-n8n | Ejemplo sintético de validación/idempotencia; distinguirlo de ejecución real de workflow. |
| ONIA · Organización diaria | `01a1a484-ad47-72a9-9684-18557087d01f` | planificar-dia; continuidad/mejora/evaluación según encargo | Leer calendario del próximo día sin escribir eventos. |
| ONIA Platform · Producto | `01a1a484-d46a-7028-8b80-93f0349f4031` | desarrollar-y-verificar | Comprobar lectura GitHub del producto y sus instrucciones, sin desplegar. |

La selección ejecutable y apoyos están en [orquestacion.json](orquestacion.json); los resultados y pendientes en [ESTADO.md](ESTADO.md). El chat de edición del entorno y el de aceptación anterior conservan sus funciones técnicas; no reemplazan estas áreas.

Cada chat recibe un encargo delimitado, usa subagentes cuando aportan trabajo independiente y cierra con resultado y evidencia. La creación de chats no inicia un servicio permanente ni un calendario de tareas. `operacion/` en cada VM guarda artefactos de prueba locales a esa VM; la recuperación desde otra tarea requiere exportación o entrega compartida comprobada.


## Organización cloud del 4 de noviembre de 2026

Por petición expresa de Sergio se crearon las secciones de sidebar **Marca personal · Cloud** y **ONIA Platform · Cloud**, agrupando los chats existentes. Se añadió **Marca personal · Plan y resultados**, ID `01a1a843-4afb-75f9-aa95-f35833fcb002`, host durable, entorno **onia**, según confirmación de coordinación. Es continuidad de planificación y resultados de marca, no un worker permanente ni otra fuente de reglas. Platform/SaaS permanece en su coordinación separada; no se abren tareas de producto en este cierre.

Fuente normativa: repo onia. [Biblioteca Marca · Evidencia, pruebas y resultados](https://chatgpt.com/space/page_66e12de902408191a926153866f6ca39) aporta seis secciones de evidencia y ejercicios privados; [Notion Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) mantiene la vista diaria. La existencia del chat, doce checks sintéticos o una agrupación del sidebar no acredita integración, cron o ejecución 24/7.

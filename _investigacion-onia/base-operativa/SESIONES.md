# Chats de trabajo por área

Creados por pedido de Sergio desde el 3 de noviembre de 2026 y actualizados en la consolidación del 4 de noviembre. Los chats registrados usan **Codex Cloud, entorno onia**, repo del harness `oninteligenciaartificial/onia`, host `durable`. Sus instrucciones comparten esta base; no se duplican reglas por proyecto. El código del producto permanece en su repo independiente.

La primera tanda de seis áreas fue de **pruebas concretas completamente cloud**. Es un antecedente, no la lista de trabajo vigente. **ONIA · Jefe** mantiene ahora la dirección del [plan continuo](PLAN.md), incluida la preparación autorizada JEF-BASE-001. El [estado](ESTADO.md) separa resultados comprobados, propuestas y pendientes.

## Coordinación y aprendizaje

| Chat | ID | Función |
|---|---|---|
| ONIA · Jefe | `01a1a843-4afb-75f9-aa95-f35833fcb002` | Integra estrategia, prioridades, entregas y decisiones de Sergio; conserva el plan oficial en Git y delega encargos delimitados. Antes se llamaba «Marca personal · Plan y resultados»; es el mismo chat. |
| ONIA · Aprendizaje y criterio | `01a1a935-c691-72d5-b055-e39970f5703e` | Organiza fuentes y ejercicios para explicar y practicar lo aprendido; entrega evidencia al Jefe y a Organización. [Currículo y primer encargo](continuidad/2026-11-04/aprendizaje.md). |

Preferencia de Sergio: **Astra para Jefatura y Sol/Terra para ejecución**. La selección Sol/Terra de los subagentes de JEF-BASE-001 quedó registrada; el modelo efectivo del chat Jefe no fue comprobado ni cambiado por esta consolidación. Una preferencia escrita no modifica el selector del chat.

## Áreas ejecutoras y pruebas iniciales históricas

| Chat | ID | Skill del área | Prueba inicial |
|---|---|---|---|
| ONIA · Desarrollo cloud | `01a1a484-065a-76bc-94a2-9b2b148d6021` | desarrollar-y-verificar | Arranque, 28 tests, navegador y n8n; luego lectura Meta. |
| ONIA · Marketing y ventas | `01a1a484-2da0-7440-8502-dfae74ab901f` | preparar-oferta-y-embudo; preparar-campana-meta para anuncios | Leer la skill y producir ficha/guion ficticios, sin publicación. |
| ONIA · Video y contenido | `01a1a484-560e-72bb-8d5d-e64733c22027` | producir-video | Render sintético vertical de seis segundos con HyperFrames dentro de la VM. |
| ONIA · Automatizaciones n8n | `01a1a484-81ca-7605-ab7e-243b8e1f4001` | automatizar-n8n | Ejemplo sintético de validación/idempotencia; distinguirlo de ejecución real de workflow. |
| ONIA · Organización diaria | `01a1a484-ad47-72a9-9684-18557087d01f` | planificar-dia; continuidad/mejora/evaluación según encargo | Leer calendario del próximo día sin escribir eventos. |
| ONIA Platform · Producto | `01a1a484-d46a-7028-8b80-93f0349f4031` | desarrollar-y-verificar | Comprobar lectura GitHub del producto y sus instrucciones, sin desplegar. |

La selección ejecutable y apoyos están en [orquestacion.json](orquestacion.json); los resultados y pendientes en [ESTADO.md](ESTADO.md). Jefatura y Aprendizaje no añaden áreas al CLI ni skills por el hecho de tener un chat. El chat de edición del entorno y el de aceptación anterior conservan sus funciones técnicas; no reemplazan estas áreas.

Cada chat recibe un encargo delimitado, usa subagentes cuando aportan trabajo independiente y cierra con resultado y evidencia. La creación de chats no inicia un servicio permanente ni un calendario de tareas. `operacion/` en cada VM guarda artefactos de prueba locales a esa VM; la recuperación desde otra tarea requiere exportación o entrega compartida comprobada.


## Organización cloud del 4 de noviembre de 2026

Por petición expresa de Sergio se crearon las secciones de sidebar **Marca personal · Cloud** y **ONIA Platform · Cloud**, agrupando los chats existentes. Jefe y Aprendizaje están en la primera; Producto, en la segunda. Jefe coordina el conjunto; Organización conserva la escritura de Notion/Calendar y Producto su alcance técnico separado. Los chats son lugares de continuidad, no workers permanentes.

Fuente oficial de reglas, plan, decisiones y documentación: **repo onia**. La [consolidación del 4 de noviembre](continuidad/2026-11-04/README.md) incorpora las entregas documentales que estaban en Pages, con procedencia y límites. La [biblioteca cloud](https://chatgpt.com/space/page_66e12de902408191a926153866f6ca39) conserva medios, referencias e historial; [Notion Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) mantiene la vista diaria. La existencia del chat o una agrupación del sidebar no acredita integración, cron o ejecución 24/7. Un push no actualiza el checkout de un chat existente: al retomar, comprobar la revisión leída.

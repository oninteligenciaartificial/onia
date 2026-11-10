# 3 · Automatizaciones

Especificación de lo que se dispara solo o semiautomático: n8n, harness y rutinas del capataz. Boss no configura ni activa nada aquí. Encender o apagar n8n o una rutina requiere el sí de Sergio.

## Qué hace

Deja a la vista qué automatizaciones existen, en qué estado están y cuál es el disparador permitido. Una automatización, para OnIA, es una cadena con entrada, pasos, revisión y destino que alguien puede encender. No es publicación automática.

## Cómo lo hace Euge

- Video 1, [13:20–13:36](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=800s) y [11:18–12:18](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=678s): el capataz tiene rutinas (cinco temas del día) y proactividad (avisos de calendario, reuniones que se pisan).
- Video 1, [13:44–15:30](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=824s): muestra conectores (nombra Gmail, ElevenLabs, Calendar y otros) y publicación con herramientas de programación o a mano si no hay conector. Esos proveedores no se copian.
- Video 1, [27:06–28:14](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1626s): llama fábricas a lo que otros llamarían workflows, porque ve lo que entra, lo que se fabrica, la revisión y el destino. El experimento Leader Summaries publica sin revisión, genera imágenes y voz (nombra servicios de imágenes y ElevenLabs) y él mismo dice que tiene pocas visitas. No es licencia para publicar sin revisión en OnIA.
- Video 2, [25:54–26:03](https://youtu.be/xPJbP9yZE1I?t=1554): una fábrica se puede disparar cuando dejás una entrada o de forma recurrente (él pone el ejemplo de levantarse a las 9).

## Cómo lo hacemos en OnIA

El registro y el disparo autorizado viven en el harness. n8n ya existe en el VPS, con copias de prueba y workflows que en el inventario del 9 de noviembre estaban en su mayoría inactivos. La rutina «Fábrica diaria» de Boss sigue pausada hasta que pasen la venta y la edición. Existe una rutina de retorno Codex → Boss por webhook, documentada en la conexión; este commit no la crea ni la cambia.

No usamos Buffer, Metricool, ElevenLabs ni publicación automática al estilo Leader Summaries.

**Veredicto infra OnIA: parcial.** Hay n8n, harness y rutinas descritas. No hay un disparador autorizado que produzca o publique los cinco videos del día.

## Entra / sale

| Entra | Dónde | Sale | Dónde |
|---|---|---|---|
| Pedido con ID, rutas y sí aplicable | [harness.py](../../scripts/harness.py), `04-operacion-agentes/tareas/<id>.json` | Sesión de Codex, evidencia y revisión distinta | GitHub `master` y evidencia de la tarea |
| Evento de cierre de una tarea | Aviso mínimo al webhook de retorno (sin secretos en Git) | Revisión de Boss y aviso a Sergio si hay algo | [conexion-boss-codex-20261110](../../../04-operacion-agentes/evidencias/conexion-boss-codex-20261110/) |
| Workflow n8n nuevo | Sólo archivo inactivo, creado por Codex cuando haya pedido | Copia inactiva hasta el sí de Sergio | n8n en el VPS; evidencia en esta carpeta o en la fábrica 4 si el flujo es el chatbot |

## Quién la hace

- **Sergio:** único que autoriza activar, desactivar o borrar un workflow o una rutina.
- **Codex:** implementa scripts y, si corresponde, un workflow **nuevo e inactivo**, con tests.
- **Boss:** especifica y revisa; no enciende producción.
- **Operaciones:** puede leer n8n; no lo cambia sin sí.

## Criterio de «bueno»

- Todo disparador tiene dueño, entrada, salida y una revisión humana antes de publicar o cobrar.
- Un workflow nuevo nace inactivo y se identifica por nombre propio, sin reutilizar destinos ajenos.
- No hay secretos, tokens, IPs ni destinos privados en Git.
- Activar o desactivar queda registrado con el sí de Sergio.
- Nada publica, envía mensajes reales ni cobra por su cuenta.

## Cómo se mide

Al final: workflows activos frente a inactivos (leídos, no inventados), rutinas en pausa o en marcha, tareas del harness cerradas con revisión distinta, envíos reales autorizados (deberían ser cero hasta el sí del chatbot). No se inventan tasas de éxito.

## Qué existe y qué falta

Ya está:

- Inventario y piloto inactivo de Telegram: [20261109-telegram/README.md](../../fabrica-contenido/20261109-telegram/README.md). Ese inventario del 9 de noviembre lista varios workflows inactivos y observa **Command Center como activo**. No se afirma el estado de hoy; hay que releerlo antes de tocar algo.
- Harness: [harness.py](../../scripts/harness.py). Máximo tres sesiones vivas y un escritor por ruta.
- Conexión y rutina de retorno: [REVISION-BOSS-v2.md](../../../04-operacion-agentes/evidencias/conexion-boss-codex-20261110/REVISION-BOSS-v2.md).

Falta: sí de Sergio para cualquier activación; el flujo de WhatsApp (se especifica en la fábrica 4, para no chocar rutas); prueba real de recepción.

## Desde el 14 sin Codex

Siguen el harness como registro, los scripts fijos y los workflows que ya estén (inactivos o, si Sergio los encendió, activos). No quedan ejecutoras Codex ni alguien que arme un flujo nuevo con un modelo.

## Pedido para Codex

No despachar una tarea nueva de «automatizaciones» esta semana si choca con la fábrica 4 o con `conexion-boss-codex-20261110`. Un escritor por ruta.

- **ID sugerido:** no abrir uno propio salvo que Sergio lo pida después de la venta. El workflow inactivo del chatbot, si hace falta n8n, vive en la fábrica 4.
- **Rutas exclusivas:** si hubiera un pedido posterior, `05-herramientas/fabrica-onia/3-automatizaciones/`.
- **Qué construir entonces:** un checklist reproducible de inventario de solo lectura (reutilizar [inventario.py](../../fabrica-contenido/20261109-telegram/inventario.py) si sigue aplicando) y la evidencia de que no se cambió `active` en ningún workflow.
- **Criterio de aceptación:** el recibo lista nombre y estado observado, sin secretos, y confirma que no hubo POST de activación.
- **Tests:** los del script de inventario ya existente, en carpeta nueva.
- **Qué no tocar:** activar, desactivar o borrar n8n o rutinas; destinos y credenciales; Command Center; el webhook ya documentado; producción.

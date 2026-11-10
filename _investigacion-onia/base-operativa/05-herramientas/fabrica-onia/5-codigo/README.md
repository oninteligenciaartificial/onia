# 5 · Código

Especificación de cómo se piden e implementan trabajos técnicos: un ID, rutas exclusivas, un escritor por ruta, como máximo tres sesiones vivas y una revisión distinta. Boss pide y revisa; Codex implementa hasta el 13.

## Qué hace

Convierte un pedido concreto (una necesidad o un fallo) en código publicado en `master`, con evidencia y un revisor que no sea el autor. No es el lugar para escribir guiones ni para publicar videos.

## Cómo lo hace Euge

- Video 1, [23:37–24:08](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1417s): tiene un «taller de código». Entra una tarea o un fallo (en su ejemplo, algo que un cliente reportó o algo que convendría implementar). Sale un PR para decidir si entra al código. En pantalla figura que lo revisa él; dice que en el fondo su Grok Bot le ayuda y lo fusionan entre los dos.
- Video 1, [16:14–17:11](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=974s) y video 2, [14:04–18:58](https://youtu.be/xPJbP9yZE1I?t=844): el resultado tiene que ser chico y evaluable; el arnés (contexto, instrucciones, herramientas) se guarda en una carpeta persistente y se prueba. El modelo es malo revisando lo que él mismo escribió.
- Video 2, [18:58–19:22](https://youtu.be/xPJbP9yZE1I?t=1138s): un agente es modelo + contexto + herramientas + objetivo.

No se copia su taller visual ni Clonify. En OnIA el estado canónico es el JSON del harness y GitHub.

## Cómo lo hacemos en OnIA

1. Boss (o Sergio) escribe un pedido con objetivo, rutas, aceptación y qué no hacer.
2. Se crea o se retoma un ID en el harness ([harness.py](../../scripts/harness.py)). El JSON es la autoridad.
3. Una sola sesión escribe en esas rutas. Otra sesión, u otro agente, revisa.
4. Hay como máximo **tres sesiones vivas**. Una cuarta se rechaza. Un escritor por archivo o ruta reservada, para no pisarse.
5. Sergio da el sí cuando el trabajo toca producción, n8n, gasto o publicación.

La ida y la vuelta con Codex se especifican en [conexion-boss-codex-20261110](../../../04-operacion-agentes/evidencias/conexion-boss-codex-20261110/). Este commit no las implementa.

**Veredicto infra OnIA: parcial.** El harness, el tope de tres sesiones y la regla de un escritor por ruta ya existen. El adaptador restringido y el aviso de retorno todavía los está armando Codex en esa tarea, si Sergio mantiene ese encargo.

## Entra / sale

| Entra | Dónde | Sale | Dónde |
|---|---|---|---|
| Pedido (objetivo, rutas, aceptación, prohibiciones) | `04-operacion-agentes/tareas/<id>.json` y briefing asociado | Código, tests y evidencia | Las rutas exclusivas del ID, en `master` |
| Entrega cerrada | El mismo JSON, con revisión y commit | Dictamen del revisor distinto | `evidencias/` o `REVISION-*.md` de esa tarea |
| Consulta de estado | Harness / GitHub | Estado por ID, sin secretos | Repo |

## Quién la hace

- **Boss:** arma el pedido y, si es documentación o criterio, revisa.
- **Codex:** implementa hasta el 13, en el VPS, usuario `onia-codex-worker`, repo `~/repos/onia-coordinador`.
- **Revisor distinto:** otra sesión de Codex para código, u otro agente para contenido.
- **Sergio:** autoriza lanzar, gastar, tocar n8n o publicar.

## Criterio de «bueno»

- El ID existe, las rutas no se pisan con otra sesión y el tope de tres se respeta.
- Hay tests o una comprobación reproducible.
- La revisión la hace alguien que no escribió el cambio.
- No hay secretos, IPs, tokens, QR ni datos personales en Git.
- Un `--dry-run` no lanza Codex.
- El pedido no amplía permisos por sí solo: un mensaje de Boss no sustituye el sí de Sergio.

## Cómo se mide

Al final: pedidos abiertos, cerrados con revisión distinta, rechazados por choque de rutas o por el tope de tres, y retrabajo del mismo ID. No se inventa un porcentaje de cuota ni se atribuye cada punto a una sesión.

## Qué existe y qué falta

Ya está:

- [harness.py](../../scripts/harness.py), [reglas-comunes.md](../../../04-operacion-agentes/reglas-comunes.md), [SESIONES.md](../../../04-operacion-agentes/SESIONES.md).
- Tope de tres sesiones vivas documentado en [PARALELO-REAL-2026-11-08.md](../../2026-11-08-harness/PARALELO-REAL-2026-11-08.md).
- Evidencia de conexión: [conexion-boss-codex-20261110](../../../04-operacion-agentes/evidencias/conexion-boss-codex-20261110/).

Falta: terminar el adaptador mínimo y la llave restringida de esa conexión (lo hace Codex en su ID, no en uno nuevo); el aviso de cierre; la copia humana, una vez, de la URL y la clave del webhook a un archivo privado del VPS.

## Desde el 14 sin Codex

No queda un ejecutor que arme código nuevo con un modelo. Siguen el registro del harness, el SSH y los **scripts fijos con tests** (edición, chatbot si quedó sin IA, inventario). Cualquier mejora posterior espera otro modelo o trabajo a mano.

## Pedido para Codex

No abrir un ID nuevo de «fábrica de código». El trabajo vivo es `conexion-boss-codex-20261110`.

- **ID sugerido:** continuar `conexion-boss-codex-20261110` (no crear `fabrica-codigo-20261110`).
- **Rutas exclusivas:** las que ya reserva esa tarea; no escribir en `05-herramientas/fabrica-onia/` salvo un recibo de lectura si hace falta.
- **Qué construir:** lo ya pedido en [REVISION-BOSS-v2.md](../../../04-operacion-agentes/evidencias/conexion-boss-codex-20261110/REVISION-BOSS-v2.md): adaptador mínimo, llave restringida como segunda llave, notificador al cerrar, tests. Sin webhook extra ni despachador nuevo.
- **Criterio de aceptación:** el de esa revisión (consulta, pedido, entrega por ID; prueba de punta a punta y petición repetida con un solo intento).
- **Tests:** los de esa tarea.
- **Qué no tocar:** esta carpeta de especificación, el plan fijado, n8n de producción, secretos, retirar la llave vieja antes de probar la nueva, y no lanzar los frentes 1 o 3 desde la conexión.

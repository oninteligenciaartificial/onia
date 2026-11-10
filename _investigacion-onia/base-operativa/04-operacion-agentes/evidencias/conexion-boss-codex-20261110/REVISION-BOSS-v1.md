# Revisión de Boss: conexión Boss–Codex

ID `conexion-boss-codex-20261110`. Revisor: Boss (Grok Bot), distinto del autor (Codex). Fecha: 10-nov-2026, 07:31–07:45 America/La_Paz.
Commit leído: `9513c6346351f3493fe77ba88528eff196c756db` (contiene `CONEXION-Y-ENCARGO-v1.md` de `89f842b`).
Alcance: sólo comprobación y revisión. No instalé nada, no creé llaves, conectores, rutinas ni servicios, no lancé Codex y no toqué la PC.

## Dictamen: `cambios` (viable con dos ajustes)

El diseño es correcto: reutiliza el harness, separa petición de autorización, pide idempotencia y deja la notificación como aviso, no como estado. Los dos ajustes son por hechos comprobados, no por opinión:

1. **SSH ya funciona hoy; el paso pendiente es restringirlo, no conectarlo.**
2. **El retorno por evento GitHub no sirve tal como se trabaja ahora** (commits directos a master). Hay que usar webhook o una consulta programada.

## Capacidades comprobadas (10-nov-2026 07:31–07:40 America/La_Paz)

| Capacidad | Estado | Evidencia |
|---|---|---|
| Leer este repo | sí | `git pull` en el clon de Boss; HEAD `9513c63`. |
| Publicar en master | sí | `gh auth status`: sesión activa de la cuenta `oninteligenciaartificial`; `git push --dry-run` correcto. Este archivo se publica así. |
| Cliente SSH | sí | `ssh -V`: OpenSSH 10.0p2. |
| Acceso conocido al VPS | sí | Llave dedicada creada el 7-nov para Boss y conexión guardada en un archivo privado de configuración (fuera de Git). Prueba `BatchMode=yes`, `StrictHostKeyChecking=yes` → `id -un` = `onia-codex-worker`. El clon del VPS está en el mismo HEAD `9513c63`, con `harness.py` y `harness_sesiones.py`. `codex` está en el PATH de un shell de login. No se probó ningún otro host ni llave. |
| Restricción de esa llave | **no** | `authorized_keys` del usuario tiene 3 entradas y 0 con `command=`. La llave de Boss abre un shell completo. |
| Conector Command (MCP local) | no comprobado en uso; la plataforma lo admite | Grok Bot permite agregar un servidor MCP de tipo comando que corre en el ordenador de Boss. Eso cambia la configuración de la cuenta de Sergio, corre también para sus otros bots y requiere su aprobación en una tarjeta. No hay ninguno instalado para el VPS. |
| Disparador GitHub | sí existe, **no cubre este flujo** | Los eventos disponibles son de PR (abierto, push, merge, comentarios, revisiones) y de CI (`ci-passed`/`ci-failed` de una rama). No existe un evento "push a master". El repo es privado, no tiene `.github/workflows` y no tiene PRs: hoy nada dispararía. |
| Disparador webhook | sí existe, no configurado | Una rutina de Boss puede despertarse con un POST a su URL. La URL y la clave las copia Sergio desde el panel de la rutina; Boss nunca las ve. |

## SSH frente a Command MCP

SSH directo es la opción mínima: ya está probado de punta a punta y no requiere instalar nada. Un Command MCP envolvería ese mismo SSH como herramienta. Daría nombres de operación más limpios, pero agrega un componente que corre para todos los bots de la cuenta y requiere aprobación. Recomiendo no hacerlo ahora.

El riesgo real hoy es el shell completo de la llave. La corrección de Codex (comando forzado, sin PTY ni forwarding, llamando a `harness_boss.py`) es correcta. Para no cortar el acceso de Boss mientras se implementa, propongo:

- Agregar una **segunda** entrada en `authorized_keys`, con llave nueva y `command="…/harness_boss.py",no-pty,no-port-forwarding,no-agent-forwarding,no-X11-forwarding`.
- Retirar el shell completo de la llave actual sólo después de que Boss pruebe la nueva.
- Que Boss genere la llave nueva en su ordenador y le pase a Codex sólo la parte pública.

Nota sobre el aviso de Codex: como `harness_sesiones status` llama a `sync`, Boss no lo usará como consulta. Hasta tener el adaptador, Boss consulta leyendo `tareas/<id>.json` desde el clon de GitHub, que no tiene efectos.

## Retorno: evento GitHub frente a webhook

- **Evento GitHub:** sólo funcionaría si cada entrega de Codex abriera un PR (`pr-opened`, filtrado al autor), o con un workflow de CI en master. Cualquiera de las dos cambia la forma de trabajar del repo. No lo recomiendo para esta semana.
- **Webhook:** es lo que mejor encaja. Al cerrar una tarea, el harness hace `curl` (disponible en el VPS) con `{id, revisión, estado, commit}` a la URL de una rutina de Boss. Es un aviso único y deduplicado por ID+revisión. Boss confirma leyendo el JSON en GitHub y nunca confía en el contenido del POST. Requiere el paso humano descrito abajo.
- **Alternativa más pequeña, sin paso humano:** una rutina de Boss que corre 3 veces por día en horario hábil, lee `tareas/*.json` con `git pull` y avisa a Sergio sólo si hay un cambio. Coincide con lo que Sergio ya pidió (revisiones unas 3 veces por día, sin chequeo constante) y no es un sondeo frecuente. Su costo es la latencia, de hasta unas horas.

## Mecanismo propuesto

- **Ida:** SSH existente ahora; llave restringida a `harness_boss.py` cuando Codex lo implemente.
- **Vuelta, fase 1 (hoy, sin instalar nada):** Boss consulta GitHub cuando Sergio le habla y en la rutina de 3 veces por día, si Sergio la aprueba.
- **Vuelta, fase 2:** webhook a una rutina de Boss cuando el adaptador esté probado.

## Único paso humano indispensable

Para el webhook: **Sergio crea con su sí la rutina webhook de Boss y copia una sola vez la URL y la clave del panel de la rutina** a un archivo privado del VPS que lea el notificador, fuera de Git. Boss no puede ver esa clave ni pegarla. Si se elige la alternativa de 3 consultas por día, no hay paso humano más allá del sí de Sergio a la rutina.

## Hasta el 14 y después

- **Hasta el viernes 13:** Codex implementa `harness_boss.py` con las operaciones mínimas (consultar, pedir, ejecutar autorizada, recuperar entrega), la llave restringida y los tests listados. Boss prueba desde su ordenador: consulta, luego tarea de juguete, luego petición repetida que conserva un solo intento.
- **Desde el 14 Codex deja de estar disponible:** se pierden la ejecutora Codex por tarea, la revisión independiente de un modelo fuerte y la capacidad de corregir código del adaptador.
- **Lo que sigue funcionando:** el harness como registro, el SSH de Boss y los programas fijos ya probados en el VPS (FFmpeg, ASR por CPU). FFmpeg no reemplaza un agente: las decisiones editoriales quedan en Contenido, Boss y Sergio.
- **Prioridad:** todo lo que deba ejecutarse sin Codex tiene que quedar como script con tests antes del 13.

## Recibo

- ID: `conexion-boss-codex-20261110`. Rol: revisor distinto (Boss).
- Modelo/esfuerzo: no visible para Boss (null).
- used_percent de Codex inicio/final: null. Esta revisión no ejecutó Codex. El último dato publicado por Codex es 75 % (10-nov 11:26 UTC).
- Intentos: 1. Retrabajo: no. Resultado: `cambios`.
- Commits: este archivo (ver `git log` del archivo). No se modificaron el JSON ni el briefing del harness.

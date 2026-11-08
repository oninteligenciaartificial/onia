# Encargo harness-piloto-real-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Comprobar el ciclo real del harness con una tarea sintética en dos turnos

## Entregable

Tres archivos de juguete, prueba PILOTO_OK y commit publicado en rama propia

## Criterio de aceptación

1) checkpoint.json permanece con etapa preparado y valores [2,3,5]. 2) resultado.json tiene etapa completo, los mismos valores, total 10 y cantidad 3. 3) verificar.py comprueba ambos archivos y sale 0 con PILOTO_OK. 4) El diff de entrega sólo añade los tres archivos de la carpeta piloto-real. 5) El commit de entrega está publicado en origin. 6) El revisor independiente explica su veredicto por criterio.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Autorización explícita de Sergio, 8/11/2026: piloto real de juguete con ejecutor y revisor distinto, lanzamiento, retoma, cierre y aceptación; sin producción ni gasto adicional.
- No usar subagentes, otros chats, APIs externas, n8n, Docker, sudo, instalaciones, servicios, mensajes ni compras. Sólo leer instrucciones, trabajar en la carpeta asignada y usar Git para publicar la rama del piloto.
- Piloto en DOS turnos. Primer turno: después de leer AGENTS, reglas, boss-memoria y desarrollar-y-verificar, crear únicamente 05-herramientas/2026-11-08-harness/piloto-real/checkpoint.json con {"etapa":"preparado","valores":[2,3,5]}. No escribir resultado.json ni verificar.py todavía; no hacer commit ni push en este primer turno. Terminar voluntariamente con PILOTO_CHECKPOINT. Es una pausa planificada: el coordinador reanudará este mismo session id.
- Segundo turno (al retomar y encontrar checkpoint.json): conservar sus bytes. Crear 05-herramientas/2026-11-08-harness/piloto-real/resultado.json con {"etapa":"completo","valores":[2,3,5],"total":10,"cantidad":3}. Crear 05-herramientas/2026-11-08-harness/piloto-real/verificar.py, sólo stdlib, que lea ambos JSON desde su propia carpeta, compruebe explícitamente esos valores y escriba PILOTO_OK con exit 0; si no coinciden, exit distinto de 0. No importar módulos que generen caches en el repo ni generar archivos auxiliares.
- Comprobar con python3 05-herramientas/2026-11-08-harness/piloto-real/verificar.py. Usar git add sólo para esos tres archivos. Commit con git -c user.name="OnIA Codex" -c user.email="onia-codex-worker@localhost" commit -m "test: juguete del piloto real del harness" y git push origin codex/ws-harness-piloto-real-20261108. No cambiar config Git global ni del repo. Si el sandbox impide commit/push, informar exactamente el bloqueo; no cambiar permisos ni usar bypasses.
- Primera pausa no equivale a entrega final; la indicación genérica de commit/push al finalizar se aplica sólo al segundo turno. No editar registros de tareas, evidencias de coordinación, README general, ESTADO ni registro-de-errores: el coordinador mantiene esos archivos.
- El revisor sólo coteja la entrega final contra la aceptación; no sigue los pasos de ejecución ni modifica archivos. Puede ejecutar verificar.py porque no tiene efectos de escritura y cotejar git diff desde el commit base.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/harness-piloto-real-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

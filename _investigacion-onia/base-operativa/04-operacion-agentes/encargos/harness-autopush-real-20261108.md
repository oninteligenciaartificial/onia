# Encargo harness-autopush-real-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Probar publicación autónoma de un juguete desde sandbox con Git privado

## Entregable

Dos archivos sintéticos verificados, commit y push realizados por la sesión ejecutora

## Criterio de aceptación

1. El diff respecto a base sólo agrega resultado.json y verificar.py en la ruta asignada. 2. resultado.json es exactamente {"valores":[4,1,7],"ordenados":[1,4,7],"suma":12,"cuadrados":[16,1,49]}. 3. verificar.py usa sólo stdlib, lee ese JSON desde su propia carpeta, comprueba todo el objeto y sale 0 con AUTOPUSH_OK; si hay discrepancia sale distinto de 0 y no escribe archivos. 4. La propia sesión ejecutora ejecuta git add, git commit y git push origin HEAD:refs/heads/codex/ws-harness-autopush-real-20261108 dentro de su sandbox, sin pedir al coordinador publicar y sin escalación ni acceso irrestricto. 5. Su HEAD coincide con la rama en origin, sin force ni cambios de otras ramas. 6. Revisor real distinto coteja diff, comprobador y evidencia de publicación autónoma; sólo su veredicto bueno permite aceptar.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Sergio autorizó este piloto real y revisión distinta en este chat. Sin producción, Docker, n8n, servicios, mensajes, sudo, instalaciones, API keys ni compras. Consumir sólo la cuota ChatGPT existente. No lanzar otras sesiones ni subagentes.
- Ruta exclusiva relativa a base-operativa: 05-herramientas/2026-11-08-harness/piloto-autopush. Crear exactamente dos archivos nuevos: resultado.json y verificar.py. No editar registro canónico, briefing, AGENTS, reglas ni otros archivos.
- El harness ya preparó un Git privado de esta tarea y perfil acotado. La limitación del piloto anterior documentada en ORQUESTACION está resuelta para este lanzamiento; debés hacer vos el commit y push. No cambiar perfiles, configuración global, remoto ni hooks. Si falla un permiso, informar el error y terminar sin buscar un bypass.
- Ejecutar python3 sobre verificar.py, después git add de los dos paths explícitos, git commit -m "test: piloto de publicacion autonoma del harness" y git push origin HEAD:refs/heads/codex/ws-harness-autopush-real-20261108. Finalmente git rev-parse HEAD y git ls-remote origin refs/heads/codex/ws-harness-autopush-real-20261108. No imprimir configuración ni credenciales.
- Informar hash completo, resultado del comprobador y publicación observada. La identidad técnica Git ya está configurada sólo en tu repositorio. El coordinador se ocupa de cierre, revisión y merge después de tu push; no de publicar tu entrega.

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

Estado: [registro de trabajo](../tareas/harness-autopush-real-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

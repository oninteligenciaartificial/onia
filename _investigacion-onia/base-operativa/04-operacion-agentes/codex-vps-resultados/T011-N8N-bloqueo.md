# T011-N8N bloqueada

La lectura de LEEME.md, registro.tsv y tareas/en-curso/T011-N8N.txt se completó.

El arranque obligatorio `./ejecutar.sh --comprobar` terminó con rc=2 y el mensaje «Hay otra ejecución o comprobación en esta carpeta».

La inspección local de ejecutar-n8n.sh muestra que el runner mantiene .ejecutar.lock mediante FD 9 durante la llamada al motor. El registro contiene un inicio de esta tarea a las 2026-11-07T18:26:52Z. Esto es compatible con un conflicto del comprobador con el propio runner, pero no se verificó el titular del lock.

Se detiene la tarea conforme a la regla local de no reintentar automáticamente los fallos. No se accedió a la API ni al archivo de autenticación. No se creó backup ni se modificó ningún workflow. Los estados active de ambos workflows no fueron consultados y permanecen sin verificar.

Pendientes completos los apartados (a) y (b). Hace falta revisar manualmente la compatibilidad del comprobador con el lock del runner antes de una nueva ejecución autorizada.

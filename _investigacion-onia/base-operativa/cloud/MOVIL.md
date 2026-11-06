# Usar ONIA desde el iPhone

Usá la misma cuenta y espacio de trabajo donde está publicado `onia`. En la app de ChatGPT para iOS, abrí **Codex**, elegí **Cloud** y el entorno **onia**. La disponibilidad depende del despliegue de la app y de los ajustes de la cuenta. [Guía oficial móvil](https://learn.chatgpt.com/docs/mobile).

Para empezar, escribí el resultado que querés y sus límites. Por ejemplo:

> Trabajá en onia. Aplicá la entrada del repositorio y las reglas vigentes. Prepará una oferta de taller con los datos disponibles y señalá qué falta decidir antes de publicarla.

Para seguir el mismo trabajo, abrí el mismo chat y enviá la siguiente instrucción. Para retomar en una tarea nueva, usá el ID y el commit de una entrega publicada:

> Retomá la tarea ID desde el commit COMMIT de oninteligenciaartificial/onia. Su registro está en _investigacion-onia/base-operativa/continuidad/tareas/ID.json. Recuperá su alcance y próximo paso antes de continuar.

El agente se ocupa de los comandos y de leer el mapa y la skill pertinente. Una tarea nueva tiene archivos propios; una conversación anterior puede conservar cambios aún no publicados. Por eso conviene continuar el mismo chat, salvo que quieras un traspaso explícito. [Persistencia de tareas Cloud](https://learn.chatgpt.com/docs/environments/cloud-environments).

Podés consultar avances, pedir correcciones y revisar la entrega desde el teléfono. Las tareas Cloud pueden trabajar con la PC dormida; eso no crea ejecución 24/7 ni garantiza notificaciones push. Crear o republicar entornos se hace en web o escritorio. Esta ruta no necesita SSH, claves PEM ni conectar la PC.

**Comprobación en el teléfono:** abrir Codex, elegir onia, abrir la tarea del piloto y pedir su estado. Sólo después de observar ese recorrido se puede afirmar uso móvil probado. Este documento describe la ruta oficial; no acredita que se haya usado ya el iPhone.

Para ver el piloto concreto, abrí [ONIA · Prueba de continuidad B](https://chatgpt.com/local/01a1b251-c3f8-7781-9fcf-1874844c401f) y pedí: «Consultá la versión publicada de onia/master y mostrame el estado y la evidencia de continuidad-cloud-001, sin modificar archivos». Su workspace conserva su propio estado; el registro publicado puede tener una aceptación posterior. El agente debe comprobarlo en Git conservando los cambios locales.

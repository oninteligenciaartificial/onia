# onia-harness-v1: preguntar

Extensión del [puente y delegación existentes](../delegacion-boss-20261110/USO-Y-LIMITES.md). La guía anterior es evidencia inmutable de una entrega aceptada; se conserva sin cambiar su hash. Este documento describe la operación nueva solicitada por Sergio el10nov2026.

## Uso

Misma llave SSH restringida y mismo comando remoto `onia-harness-v1`, JSON por stdin con newline:

```json
{"version":1,"operacion":"preguntar","id_pregunta":"nombre-workshop-20261110-1","texto":"¿Cuál es el nombre final del workshop según las decisiones vigentes?"}
```

Respuesta JSON con `respuesta` en texto, `id_pregunta`, commit y rutas fuente. No se requiere ID de tarea ni permiso individual. El ID admite minúsculas, números y guiones; texto máximo2000 caracteres. Campos extra (comandos, rutas, modelo, esfuerzo, herramientas) se rechazan. Mismo ID+texto devuelve respuesta anterior, incluidos errores terminales, sin nueva inferencia ni consumo diario; otro texto con el mismo ID se rechaza. Un ID incierto no se relanza automáticamente.

## Límites operativos

- Modelo solicitado fijo `gpt-6.1-sol`, esfuerzo `low`, ChatGPT existente sin API paga; cero hijos. Modelo observado queda null: el banner del CLI no prueba identidad efectiva del modelo. No inferirlo de una respuesta autorreferida.
-120segundos desde admisión, incluida recuperación de fuentes; salida máxima12000 caracteres. Supervisor en grupo de procesos propio: timeout/desconexión termina el grupo y el padre lo recoge antes de liberar cupo. Espera por lock ocupado se rechaza; no forma una cola silenciosa.
-20 consultas nuevas admitidas por día `America/La_Paz`, incluidas fallidas/timeout. Solicitudes rechazadas antes de admisión y repeticiones no suman. Máximo global3 entre preguntas, ejecutoras y revisores, bajo el mismo lock. No subir ese límite.
- Respeta pausa del puente y `preguntar_habilitado`; exige cuota semanal fresca (<2h) y <90% usado. No modifica permisos de tareas ni recupera cuotas/operaciones revocadas.
- Al terminar libera el cupo; ante una caída incierta conserva la reserva como máximo hasta el plazo, salvo PID real aún vivo. PID+inicio evita confundir un proceso reutilizado. El log se conserva; no se borra para liberar cupo.

## Sólo lectura y contexto

El adaptador lee blobs regulares de un SHA de `origin/master`; `fetch` sólo actualiza objetos/refs locales, no hace pull, cambia checkout ni ejecuta hooks. Usa una lista literal de documentos operativos .md; excluye código, JSON, enlaces, archivos privados/credenciales y medios. No sigue URLs, enlaces Markdown ni rutas pedidas por el texto. Recuperación acotada, no lectura exhaustiva del repo: bitácora y decisiones primero, después reglas y hasta12 fuentes seleccionadas, con líneas y commit. Si la muestra no alcanza, la respuesta debe decirlo; no inventar estados.

El modelo recibe esos fragmentos saneados por stdin y parte de un cwd vacío. Perfil filesystem mínimo de lectura, red de herramientas apagada, shell/snapshot/apps/plugins/web/navegador/computadora/imágenes/memorias/hooks/hijos deshabilitados. No carga configuración de usuario ni reglas de ejecución del repo. El runtime usa el almacén ChatGPT existente sin copiar auth.json por consulta; el modelo no recibe credenciales ni acceso al checkout. La conexión al servicio de inferencia sigue siendo necesaria. No se abren servicios ni n8n.

El adaptador únicamente escribe sus registros y reservas de cupo (el CLI conserva su almacenamiento de autenticación existente). No son modificaciones del repo por la consulta. Texto y respuesta se filtran para no registrar/devolver patrones de claves, tokens, direcciones o URLs parametrizadas. No enviar contraseñas ni QR; no usar esta operación para leer material privado. El filtrado no convierte material privado en publicable.

## Log, fallos y parada

`~/operacion/puente-boss/preguntas/<id_pregunta>/registro.json`, privado600: pregunta, respuesta saneada, timestamps ISO, duración, SHA/fuentes, modelo solicitado/observado o null, cuota inicial fechada, cuota final null si no es observable sin extender el plazo, estado y huella de idempotencia. No guardar salida cruda de herramientas ni stderr. Modo Codex efímero, home mínimo privado por pregunta, sin incorporar sesiones/logs antiguos. El motor interno Code Mode permanece disponible porque el CLI lo requiere; esto no habilita shell, conectores ni escritura. La prueba directa del perfil negó leer un canario fuera del contexto y crear un archivo. Nunca subir auth/runtime al repo.

Errores explícitos: cupo completo,20/día, cuota vieja/tope, falta de bitácora/decisiones, ID repetido distinto, timeout, salida excesiva o herramienta inesperada. Ante incertidumbre conservar y conciliar; no usar nuevos ID para evadir límites. Pausar/revocar bloquea nuevas consultas; las respuestas guardadas no se eliminan. No es scheduler, ejecutora de cambios ni aceptación de productos.

## Fuentes técnicas

Verificado contra CLI instalado y [configuración oficial de Codex](https://learn.chatgpt.com/docs/config-file/config-reference): shell_tool, perfiles de filesystem/red, features y configuración de documentos. La documentación informa capacidad; pruebas del runtime y límites se acreditan en el recibo de esta entrega.

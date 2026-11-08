# Archivo documental: n8n a Codex Cloud · Prueba CLI y dependencia de autenticación · 2026-11-04

> Consolidado por autorización de Sergio. Fuente: [Page original](https://chatgpt.com/space/page_8aec522aeac8819185bf697166227f5f), secuencia **0**, actualizada 2026-11-04T20:06:01.083074Z. Este archivo conserva evidencia y borradores de esa fecha; **no es un segundo plan activo**. Las decisiones vigentes están en [PLAN](../../../01-negocio/PLAN.md) y los resultados en [ESTADO](../../../00-MAPA/ESTADO.md). El texto histórico que diga «vigente», «STOP» o «no modificar Git» describe su momento original y no reemplaza la consolidación autorizada.

Los enlaces a medios/descargas se abren en la Page de origen; esos binarios permanecen en cloud. Esta copia no los incorpora ni vuelve a ejecutar sus pruebas.

---

Prueba del 4 de noviembre de 2026, 16:05 America/Caracas, desde la VM onia. Resultado: vía CLI oficial documentada y binario disponible, pero acceso cloud bloqueado por autenticación HTTP 401. No se acreditó n8n→Codex Cloud ni se creó una tarea. No se usó API de pago, nuevas claves, PC local, servicios VPS o puertos públicos.

# Comprobación real en la VM

Runtime: VM cloud onia de esta sesión, /tmp como directorio de prueba. Binario /opt/codex/bin/codex, versión codex-cli 0.166.0-alpha.1. No se leyeron configuraciones, archivos de autenticación ni variables con tokens.

La ayuda disponible declara cloud experimental y subcomandos exec, status, list, apply y diff. cloud exec requiere --env ENV_ID y permite --attempts, por defecto 1; list soporta --json y --limit. status acepta TASK_ID. No hay subcomando environments en la ayuda expuesta; la documentación indica el selector interactivo codex cloud para explorar entornos.

codex login status informó Logged in using ChatGPT. Esto sólo acredita el estado local declarado, no aceptación de sus credenciales por el servicio. La única consulta remota fue codex cloud list --json --limit 1, mediante permisos oficiales adicionales de red y proxy/TLS heredados. Se capturó la respuesta para evitar imprimir títulos o contenido de otras tareas. Salida del CLI: 1; no se obtuvo inventario utilizable.

# Error y criterio de parada

Error saneado exacto:

```text
Error: http error: list_tasks failed: GET https://chatgpt.com/backend-api/wham/tasks/list?limit=1&task_filter=current failed: 401 Unauthorized; content-type=application/json; body={"detail":"Could not parse your authentication token. Please try signing in again."}
```

Advertencia local adicional: WARNING: proceeding, even though we could not create PATH aliases: Read-only file system (os error 30). El CLI sí llegó al servicio y recibió 401; esa advertencia no demuestra la causa del rechazo remoto y no se intentó reparar la instalación.

Se alcanzó una dependencia real: autenticación del CLI no aceptada por el backend. No se invocó cloud exec, no hubo TASK_ID/run_id remoto ni artefacto de una tarea nueva. No se consultaron estado o persistencia de una tarea inventada ni se repitió la solicitud tras el 401. El máximo de un ensayo no se consumió creando una tarea: cero tareas creadas.

# Entorno e identidad que no se deben confundir

El entorno publicado de la app onia, versión 6aeb5d2767cc81a3aee4674cf6485f5d, no es evidencia de un ENV_ID admitido por codex cloud. La autenticación falló antes de descubrir o verificar un entorno del CLI asociado a oninteligenciaartificial/onia. No se pasó ese identificador de versión, un GUID de la app ni el ID de la VM a --env. Tampoco se eligió onia-platform.

La referencia oficial describe la misma autenticación del CLI para cloud, pero no garantiza que una credencial inyectada en una VM de la app sea reutilizable en ese backend. Esta prueba demuestra la incompatibilidad observada del acceso actual, no su causa interna ni que una suscripción nueva sea necesaria.

# Solución más barata y opciones concretas

Recomendación para resolver la dependencia: autenticar mediante mecanismo oficial un lanzador cloud dedicado bajo la cuenta autorizada de Sergio. La ayuda instalada ofrece codex login --device-auth. Sergio completa personalmente el device flow oficial que genere ese lanzador; no copiar auth.json, cookies o tokens desde su PC y no guardar secretos en esta biblioteca. No se ejecutó el login en esta VM ni se solicitó la clave. Confirmar que el almacenamiento de autenticación del lanzador sea escribible y privado antes de iniciarlo; no sobrescribir credenciales administradas del runtime.

Tras esa autenticación: una única consulta list, descubrir el ENV_ID por el selector oficial, confirmar repo oninteligenciaartificial/onia y entonces ejecutar un ensayo con --attempts 1, branch master y encargo permitido que sólo escriba un artefacto temporal con run_id. Conservar el task_id devuelto y consultar status; comprobar el resultado y cómo recuperar el artefacto antes de darlo por integrado. El login correcto no prueba por sí solo cuotas, compatibilidad de namespaces ni disponibilidad continua del lanzador.

Alternativa inmediata sin otra infraestructura: seguir encargos supervisados en el chat onia cloud existente y usar n8n para conservar la cola/estado de revisión. Eso permite trabajo cloud sin que la PC ejecute el cómputo, pero el despacho desde n8n sigue manual y no es integración automática. Es preferible a contratar otra plataforma antes de probar el acceso incluido.

No se propone Agents API ni otra API de pago, nueva suscripción, instalación en el VPS, relay público o apertura de puertos. La suscripción y límites efectivos de cloud exec deben validarse con el ensayo autenticado; no se promete coste adicional cero por inferencia de un login local.

# Contrato mínimo de despacho acotado

Diseño para revisar, no implementado:

1. n8n conserva job_id e idempotency_key estables y un payload de encargo con hash. Claim atómico por clave antes de despachar; una clave con payload distinto es conflicto. No usar el Get+Insert del ensayo actual como garantía atómica.

2. Allowlist inicial: un solo encargo de aceptación, repo onia, rama master, lectura y artefacto temporal. Prohibidos cambios al repo, skills, producción, cuentas, publicación y DMs. Construir argv sin shell ni texto de comandos recibido del usuario; concurrencia máxima 1 y attempts 1.

3. Lanzador cloud autenticado toma el job mediante un canal privado ya autorizado. Guarda SUBMITTING antes de exec y el task_id inmediatamente después de la respuesta. Si hay timeout de envío o resultado incierto, no reintentar ciegamente: reconciliar por run_id/task_id o enviar a revisión. El CLI no documentó aquí una idempotency key de servidor; el ledger local no elimina esa ventana de duplicación.

4. Para recibir estado, el mecanismo documentado disponible es polling con codex cloud status TASK_ID y list --json como inventario. No se observó un flag callback en exec. El lanzador podría escribir estado agregado en el registro n8n por su API autenticada existente; esa conexión no se implementó ni probó. No hace falta un relay público para ese diseño de salida.

5. Estado terminal pasa a REVIEW, nunca publicación/envío automático. Verificar salida y run_id. La ayuda de status no acredita un formato JSON ni la recuperación completa de la respuesta/archivos; list documenta summary, no un contrato de resultado completo. Ese punto debe comprobarse en el único ensayo futuro, sin usar apply/diff para modificar el repo.

Pendientes materiales: autenticación aceptada, ENV_ID/repo correctos, recuperación del resultado, claim atómico y un lanzador cloud con vida útil/almacenamiento/disparador comprobados. Una VM de tarea no equivale a un worker 24/7; no se creó un heartbeat local ni se presentó automation_update local-only como scheduler cloud.

# Fuentes y evidencia

[Referencia oficial Codex CLI](https://learn.chatgpt.com/docs/cli/reference), sección codex cloud: exec --env, list --json y autenticación compartida. [Entornos cloud](https://learn.chatgpt.com/docs/environments/cloud-environments): ejecución remota distinta de mantener un lanzador vivo. Ayuda instalada: codex --version, cloud --help, cloud exec/list/status --help y login --help; login status y una sola list remota. Sin investigación adicional de endpoints ni lectura de datos privados. No hubo cambios Git, reglas, skills, instalación o VPS.

Conclusión operativa: opción oficial documentada; el acceso CLI actual no funciona para la consulta cloud por HTTP 401. No existe todavía una vía n8n→Codex comprobada en esta VM. Próxima acción personal concreta: device authentication en un lanzador dedicado autorizado; la operación cloud supervisada existente permite continuar trabajo independiente mientras tanto.


# Mínimo operativo local

Esta carpeta contiene documentos y una cola manual; no es un repositorio ni una copia comprobada de ONIA. El acceso GitHub está bloqueado: según la coordinadora, ls-remote falló con exit 128 porque no pudo leer Username; gh no está instalado. No se ha comprobado HEAD.

Meta comercial: Bs 3000 de nuevos cobros conciliados hasta el 14 de noviembre de 2026. No hay estado comercial vigente aquí. Ads pausados; ninguna acción externa autorizada.

Desde una terminal VPS como onia-codex-worker, sin Grok:

    cd /home/onia-codex-worker/operacion
    cat AGENTS.md LEEME.md resultados/T001.md
    ./ejecutar.sh --comprobar
    # Solo después de elegir una tarea compatible y autorizar sus acciones:
    ./ejecutar.sh NOMBRE.txt

No ejecutar T002 todavía. Su descripción prepara el acceso legítimo futuro; no autoriza instalar gh ni conectarse. Cada tarea pendiente es un archivo regular de nombre simple. El script rechaza rutas, opciones y symlinks, toma un lock común y procesa una sola tarea. Guarda prompt, salida combinada, código de retorno y resumen. Exit 0 de Codex significa ejecución terminada, no verificación comercial ni aprobación humana del resultado. Revisar siempre los artefactos al cerrar.

Continuidad: registro.tsv → tareas por estado → resultados/. T001 está hecha como diagnóstico provisional documental. T002 sigue pendiente y bloqueada por acceso GitHub. Los fallos quedan en error; cualquier nuevo intento requiere decisión manual.

El ejecutor usa exclusivamente /home/onia-codex-worker/.local/bin/codex, gpt-6.1-sol y proveedor openai, con HOME/USER/PATH limpios, sandbox workspace-write, red del sandbox deshabilitada y aprobaciones on-request. La autenticación ChatGPT ya existente la gestiona Codex; este script no lee ni copia credenciales. No hay fallback, retries ni subagentes autorizados. La ejecución futura de Codex requiere su conexión normal al proveedor; red de herramientas deshabilitada no significa ejecución offline. La conexión normal de Codex a ChatGPT está autorizada; la prohibición de red se aplica a las herramientas.

No es daemon ni servicio 24 h, no ofrece aislamiento total ni cuota garantizada. timeout limita cada invocación a 300 s (TERM y KILL tras 5 s de gracia). El sandbox no sustituye las reglas ni garantiza contención frente a un usuario local hostil. Tras una interrupción abrupta, revisar manualmente en-curso y el registro antes de retomar.

Este mínimo fue elaborado por una llamada Codex y esta revisión Codex, sin llamadas anidadas. T001 es un resultado Codex provisional documental, sin actividad comercial real. La compatibilidad de opciones se valida con --help, sin invocar el modelo; véase VERIFICACION.md.

## Corrección efectiva de permisos — 2026-11-07 12:38 America/Caracas
Fuente oficial de la versión0.167.0: https://raw.githubusercontent.com/openai/codex/rust-v0.167.0/codex-rs/exec/src/lib.rs . run_main fija approval_policy: Some(AskForApproval::Never) con comentario headless; handle_server_request rechaza CommandExecutionRequestApproval/FileChangeRequestApproval/PermissionsRequestApproval porque no son compatibles con exec. No hay aprobaciones humanas en este modo. never no desactiva el sandbox ni autoriza escalaciones: solicitudes de aprobación se rechazan. -a on-request global no lo convierte en interactivo.
Documentación oficial https://developers.openai.com/codex/noninteractive indica sandbox read-only por defecto y --sandbox workspace-write para permitir ediciones. Log de la prueba pasada confirmó workspace-write; NO se usó bypass.
Corrección mínima conservadora: runner ahora fija --sandbox read-only, no workspace-write. Solo lectura/análisis acotado; stdout/rc/resumen los persiste el script exterior. Cualquier documento anterior que afirme aprobaciones humanas o workspace-write como estado actual queda supersedido. Para escrituras futuras hace falta alcance explícito y revisión de la configuración, no ampliar automáticamente. No red de herramientas, no producción, usuario sin sudo/docker y cwd exclusivo; no aislamiento total. T002 GitHub sigue pendiente, sin ejecutar. Sin nuevas llamadas a modelos para esta aclaración.

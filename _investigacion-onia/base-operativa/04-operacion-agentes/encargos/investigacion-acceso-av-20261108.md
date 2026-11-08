# Encargo investigacion-acceso-av-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Acceso audiovisual open source y piloto Playwright MCP instalado

## Entregable

Recomendación y prueba reproducible en 05-herramientas/acceso-av/20261108

## Criterio de aceptación

Investigación OSS con fuentes primarias y recomendación accionable; instalación existente inventariada sin reinstalar; inyección explícita documentada y prueba real MCP de catálogo/navegación/DOM/captura en example.com y landing pública o fallo reproducible con causa y salida concreta, sin deshabilitar sandbox. Herencia comprobada o límite documentado con hijo distinto. Cada afirmación sustentada; cuenta/perfil siguen propuestas; Git autónomo sólo carpeta asignada; revisor independiente.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- AUTORIZADO: investigar herramientas open source para recuperar y analizar audiovisual público; comprobar instalación existente y conexión Playwright MCP a Codex, sin reinstalar. Leer ~/operacion/browser-piloto-20261108/REPORTE.md y package.json. No modificar esa instalación ni config global, servicios, app-server, Docker, n8n, producción o ~/repos/onia sucio. No borrar. No compras/API paga ni consumir vidIQ. Login ChatGPT cuota incluida.
- LEER AGENTS, reglas/boss-memoria/tarea, desarrollar-y-verificar y apoyo research. Leer 05-herramientas/asr-local/README.md y scripts existentes. Diferenciar acceso a medio/captions, transcripción y análisis visual. Inventario primero, luego comparación primaria de yt-dlp, youtube-transcript-api, faster-whisper, whisper.cpp y Playwright MCP. No instalar candidatos ni pesos nuevos. Recomendar por evidencia/costeCPU/compatibilidad/licencia, con URLs oficiales.
- CONEXIÓN: coordinador inyecta mcp_servers.playwright por -c usando codex-con-playwright.py ya versionado. Conserva --ignore-user-config y sandbox del harness. MCP stdio local, headless, isolated, --sandbox, sin perfil persistente ni cookies. Sólo browser_navigate, browser_snapshot, browser_take_screenshot, browser_close. No intentar ampliar catálogo, no browser_run_code/evaluate/click ni ejecutar nuevo codex exec. No ejecutar navegador paralelo por shell para fingir una prueba MCP. Usar herramientas MCP nativas anunciadas; si no aparecen, registrar catálogo/límite, no simularlas.
- PRUEBA ACOTADA: catálogo y llamada real browser_navigate a https://example.com, browser_snapshot confirma Example Domain y browser_take_screenshot con nombre example.png. Luego https://cursos.eriktaveras.com/c/hermes-basico/ para URL/título/DOM/captura erik.png. Sólo GET público, no formularios/login/compras/cookies. Si 403/429/captcha/auth requerido, registrar y detener esa ruta, sin evasión. Si falla Chromium sandbox, NO --no-sandbox, sudo ni cambiar kernel: guardar error y salida concreta. Capturas sólo públicas propias de esta prueba. Cerrar navegador con browser_close, no matar procesos ajenos.
- UN hijo nativo nuevo Sol6.1high sin nietos. Después de cerrar tu navegador, dale tarea leer fuentes OSS, escribir sólo ALTERNATIVAS.md y comprobar que anuncia esas4 herramientas MCP. Si padre funcionó, hijo navega sólo example.com y cierra; guardar evidencia de herencia y SID en su informe. Padre único escritor README.md/EVIDENCIA.md/PRUEBA.json/capturas. Hijo no Git. No compartir navegador concurrentemente. Cerrar hijo al terminar. Si padre no tuvo MCP no inventar herencia: reportar límite.
- ASR: inspección de versiones sin secretos y evidencia de pruebas ya hechas por grupoC; puede ejecutar una prueba local corta con audio sintético o fragmento público ya autorizado y disponible, small offline, máximo2hilos1worker. No descargar modelos, no transcribir largos; no tratar ASR como visión/escucha integral. No se necesita cuenta para el control público. Correo onia.investigacion y perfil persistente permanecen PROPUESTA; no crear cuentas ni credenciales, no probar disponibilidad de Gmail.
- ENTREGA sólo 05-herramientas/acceso-av/20261108: README con recomendación concreta y comandos reproducibles; ALTERNATIVAS por hijo; EVIDENCIA con contexto/modelo/catálogo/errores/causa/evidencia/prevención y mapa hijo; PRUEBA.json con cada acción, resultado, fecha, URL, archivos/hash y limitaciones. Distinguir comprobado/propuesto/pendiente. No logs crudos/secretos/medios completos. Commit/push autónomos rama asignada; no master. Revisor distinto read-only después. El éxito de la investigación puede ser un diagnóstico negativo reproducible, pero no afirmar navegador conectado si no llamó sus herramientas. No modificar wrapper sin documentar necesidad y comprobar alcance.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)
- [05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)

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

Estado: [registro de trabajo](../tareas/investigacion-acceso-av-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

# Evidencia saneada · investigacion-acceso-av-20261108

## Contexto y autoridad

Sesión padre `01a1bd30-efe1-7f90-b6e0-811def9bf063`, obtenida de `CODEX_SESSION_ID`/`CODEX_THREAD_ID`; `CODEX_VERSION=0.167.0`. Modelo/esfuerzo del padre: no verificables desde la interfaz consultada (`null` en PRUEBA). Rama `codex/ws-investigacion-acceso-av-20261108`, HEAD inicial `c21792a8bd557d50188d55edfb8a3d3e5603c203`, estado inicial limpio y cwd del worktree asignado. No se recuperó ni modificó el JSON canónico ni su proyección: briefing recibido por stdin/chat, como indicó el usuario.

Fuentes internas realmente leídas: AGENTS.md; ESTADO; reglas-comunes; boss-memoria; ORQUESTACION; sección desarrollo de orquestacion.json; arquitectura; desarrollar-y-verificar; apoyo research; README/scripts/lock de asr-local; ejecución ASR 8/11 y Ali/Jeff; entradas pertinentes del registro de errores. `desarrollar-y-verificar` estaba anunciado en el catálogo inicial y su cuerpo canónico fue leído. Eso no prueba lectura automática. No se consultó ONIA-CENTRAL, contexto personal ni el repo sucio `~/repos/onia`. Se leyó `openai-docs` para la consulta delimitada de política MCP y luego la documentación oficial citada en README.

La prueba busca comprobar catálogo → llamada MCP → página → snapshot/captura, sin reemplazarla por shell. Hipótesis: la inyección explícita permitirá navegación pública con sandbox. Control: Example Domain. Resultado que cambiaría la decisión: navegación real y DOM/captura válidos. Resultado obtenido: rechazo de permisos antes de resultado de página. Se aplica la lección del registro de errores: instalación/catálogo no equivalen a acceso; ASR/cuadros no equivalen a percepción integral; no encadenar reintentos bajo el mismo bloqueo.

## Catálogo y llamada real

Aproximadamente 22:02 UTC, `ALL_TOOLS` anunció exactamente estos nombres del servidor Playwright; se guardan en PRUEBA:

```text
mcp__playwright__browser_close
mcp__playwright__browser_navigate
mcp__playwright__browser_snapshot
mcp__playwright__browser_take_screenshot
```

El esquema de screenshot requiere `scale` y permite `filename`; snapshot permite guardar archivo. No se solicitó ampliar catálogo ni se invocaron evaluate/run_code/click. Las otras aplicaciones anunciadas por la interfaz no se usaron como sustituto.

El 8/11/2026 a las 22:05 UTC se invocó realmente, mediante la herramienta nativa en `functions.exec`:

```javascript
await tools.mcp__playwright__browser_navigate({url: "https://example.com"})
```

Respuesta: `isError=true`, texto exacto: `MCP tool call requires approval, but approval policy is never`. Se registró reloj a las 22:05:08 UTC inmediatamente después. Luego se invocó realmente `browser_close({})`: mismo rechazo. No se obtuvo confirmación de cierre; no hay evidencia de lanzamiento de navegador por estas llamadas. No se mataron procesos.

Snapshot y screenshot no se invocaron, porque no había una página del control navegada. Tampoco se insistió con Erik bajo la misma barrera. Los títulos/URL final/DOM/HTTP status de ambas páginas son `null`; no inferir 403, captcha, TLS ni fallo de sandbox. `example.png` y `erik.png` son salidas previstas ausentes, con hash `null`. No se capturó `about:blank` para aparentar éxito ni se abrió Chromium por shell.

**Causa comprobada:** la capa de invocación exige aprobación y la política efectiva la impide. **Causa de configuración no establecida:** no está demostrado por qué no se aplicó la intención `approve` del wrapper. La configuración efectiva o la política del host puede diferir; son hipótesis, no hechos. Tampoco se acreditó conexión stdio viva al servidor mediante una llamada ejecutada. Catálogo anunciado no basta: la [documentación oficial](https://learn.chatgpt.com/docs/config-file/config-reference) distingue catálogo de conexión viva.

## Instalación e inyección

Se leyeron `~/operacion/browser-piloto-20261108/REPORTE.md` y package.json. El reporte inicial, fechado 21:51:53 UTC (17:51 Caracas), decía `browser_launched=false`, `codex_test_launched=false`. Sus sesiones/cuota eran observaciones históricas: no se adoptaron como estado actual.

Inventario nuevo a las 22:06:16 UTC mediante metadata de paquetes existentes: MCP 0.0.84, playwright y core 1.65.0-alpha-2026-10-30. Node 20.20.2. A las 22:07:51 UTC ambos binarios Chromium build1252 existían y `ldd` devolvió rc=0 sin bibliotecas faltantes; eso no certifica sandbox ni arranque. No se ejecutó instalador, navegador de shell ni candidato nuevo. Los hashes de archivos muestreados están en PRUEBA; no son una auditoría recursiva del entorno.

Wrapper leído en el checkout coordinador, ruta completa en README, SHA-256 `d9dcea17da14a582f0bdb28cb4fa6990300696c1d57dfbdfdcf535c7a038e095`. Ausente del HEAD/worktree inicial de esta ejecutora; no se abrió el Git del coordinador para certificar su commit, ni se copió o editó. La afirmación de que está versionado procede del briefing, no de una validación de Git ajeno.

Configuración leída, sin secretos:

```text
command=/usr/bin/node
args=<instalación>/node_modules/@playwright/mcp/cli.js
     --headless --isolated --sandbox
     --executable-path <instalación>/browsers/chromium-1252/chrome-linux64/chrome
     --output-dir <cwd>/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/capturas
enabled=true; required=true; startup_timeout_sec=30; tool_timeout_sec=60
default_tools_approval_mode=approve
enabled_tools=[browser_navigate,browser_snapshot,browser_take_screenshot,browser_close]
```

El wrapper usa `os.execv` sobre el Codex existente con los overrides `-c` y luego `sys.argv[1:]`; por diseño no elimina `--ignore-user-config` ni el perfil del harness. Stdio por defecto, sin `--port`, perfil persistente ni storage-state/cookies. La [referencia oficial MCP](https://github.com/microsoft/playwright-mcp#user-profile) describe aislado y pérdida de estado al cerrar, y su CLI documenta `--sandbox`. Se inspeccionó además el help ya guardado de la instalación. **No se comprobó argv efectivo del Codex padre**: la inspección filtrada de ancestros dentro del sandbox sólo alcanzó procesos del propio comando y no produjo esa evidencia; no se conservaron esos volcados como logs de entrega.

Salida/previsión: coordinador revisará política por herramienta y aplicación efectiva de la inyección, manteniendo los cuatro nombres y sandbox. No se modifica wrapper ni config global aquí. Inyectar aprobación por herramienta es candidato para el siguiente intento; documentación y sintaxis en README. No está ensayado y el wrapper ya declaraba aprobación general, por lo que no se atribuye el rechazo a ausencia de esa clave.

## ASR y antecedentes

Venv Python3.12.3: faster-whisper1.2.1, yt-dlp2026.10.26, av18.1.0 y CTranslate2 4.8.5; `pip check` rc=0. Aviso de pip: caché home no escribible, deshabilitada; no se cambió home ni permisos. `transcribir.py` instalado coincide byte a byte con la copia versionada. El script limita duración y usa small CPU int8/dos hilos, pero **no fija offline/local_files_only**, descarga audio cuando se ejecuta y su salida predeterminada apunta a otro checkout. No se ejecutó ese wrapper en esta sesión. Para una prueba offline dentro del encargo se usó el comando explícito de README/PRUEBA, sin descarga y sin archivos de audio.

Control nuevo 22:07:05.564–22:07:06.910 UTC: 32000 ceros float32 a16kHz, 2s, small existente por ruta absoluta, CPU int8, dos hilos, un worker, `local_files_only=True`, HF offline, VAD=true y español fijo. Cero segmentos, duración tras VAD0s, proceso0, 1.346s y maxRSS620456KiB. Aviso ONNX Runtime: identificador de telemetría no persistible, usa memoria. **Sólo carga y control negativo de VAD**: no prueba exactitud en habla ni rehabilita Whisper sin VAD ante silencios. No se descargaron modelos, piezas ni dependencias.

El registro ASR anterior (8/11) documenta Pedro66.434s, Cormac~37.75s y Justin935.636s; YouTube pidió confirmación de bot en varias fuentes. La nota Ali/Jeff añade que faltaba runtime JavaScript soportado, sin atribuirle causalidad exclusiva. Se inspeccionaron esas notas y scripts; no los audios completos ni los logs privados. Ese antecedente justifica reutilizar la pila y detener rutas bloqueadas; no garantiza acceso actual ni que iniciar sesión resuelva extracción.

## Hijo y revisión

Un único hijo nativo nuevo, contexto fresco (`fork_turns=none`), ruta canónica `/root/alternativas`, creado después del intento de cierre del padre. Llamada solicitó `model=gpt-6.1-sol`, `reasoning_effort=high`; ejecución efectiva de modelo/esfuerzo no expuesta, se conserva `null`. El retorno de spawn sólo entregó task_name, sin UUID. El hijo leyó `CODEX_THREAD_ID=01a1bd32-16a5-7e60-b1f6-ed94623c5330`, distinto del padre. Su `CODEX_SESSION_ID` conservaba el ID padre por herencia de entorno: no usar esa variable para afirmar identidad independiente.

Único archivo del hijo: `ALTERNATIVAS.md`. Sin nietos, Git ni navegador. El hijo comunicó por mensaje que `ALL_TOOLS` anuncia exactamente las cuatro herramientas anteriores y no invocó ninguna porque el padre no navegó. Esto comprueba **herencia de catálogo entre contextos distintos**, no conexión funcional, navegación, aislamiento real del proceso ni persistencia entre sesiones. No se comparte navegador concurrentemente.

El hijo es investigador, no revisor independiente de la entrega. Conforme al briefing específico, el coordinador cerrará la tarea y lanzará otra sesión read-only contra el commit remoto. Revisión, aceptación e integración quedan pendientes; no se lanza otra sesión desde esta ejecutora.

El hijo devolvió respuesta final y `interrupt_agent` confirmó estado previo `completed`, sin trabajo activo. La interfaz no expone una herramienta de destrucción/cierre definitivo del contexto; se registra finalización, no destrucción. Una revisión puntual del padre pidió al mismo hijo corregir sólo un enlace interno de su archivo antes de la publicación; no se abrió otro hijo ni se reutilizó el cupo.

## Prevención y límites de publicación

No confundir tres niveles: binarios/dependencias presentes, herramientas anunciadas, herramientas que ejecutaron navegación. Detener después del rechazo común y entregar la causa exacta evita una falsa prueba por shell o atribuir a Chromium un error del host. Mantener cuentas/perfiles como propuestas y acceso público sin autenticar. No afirmar visión/escucha integral a partir de ASR/DOM.

Sólo se escriben los documentos de esta carpeta. No cambios a tarea/briefing canónicos, servicios, Docker, n8n, producción, app-server ni configuración global. Commit/push explícito a la rama asignada, sin force; comprobación remota y hash se entregan al coordinador. PRUEBA guarda hashes de documentos dependientes, excluye su propio hash para evitar autorreferencia; el commit identifica el paquete completo.

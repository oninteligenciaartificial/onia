# Alternativas abiertas para acceso audiovisual

Consulta: **2026-11-08, UTC**. Investigación documental en fuentes oficiales de los cinco proyectos; sin instalaciones, descarga de modelos o medios, cuentas ni cambios de configuración. Directora leída: `desarrollar-y-verificar`; apoyo leído: `research`. La instrucción de ese apoyo de delegar queda limitada por el briefing: éste es el único hijo y no crea nietos. Lección aplicada del registro de errores: recuperar texto, imágenes o archivos no acredita percepción audiovisual integral.

## Decisión propuesta

Conservar la ruta local de ASR ya comunicada por el padre. Resolver primero el bloqueo de invocación MCP con el operador/coordinador y repetir después un control público mínimo. Instalar otro navegador, otro ASR o crear una cuenta no corrige por sí mismo ese bloqueo. La cuenta `onia.investigacion` y un perfil persistente separado siguen como **propuesta**, sin creación, login ni conexión demostrados.

Las herramientas cubren capas diferentes: conseguir captions o un archivo, transcribir voz y leer/capturar una página son capacidades complementarias. Ninguna de las cinco, por sí sola, acredita comprensión de imagen en movimiento, música, ambiente, efectos, prosodia y sincronía. Esta conclusión es una delimitación del alcance de sus interfaces, no un benchmark ni una prueba local de calidad.

## Comparación de fuentes primarias

| Proyecto y capa | Capacidad y compatibilidad documentada | Recursos y límites | Licencia y decisión |
|---|---|---|---|
| **yt-dlp — acceso a medios/captions** | Descarga audio/video y subtítulos existentes, incluidos automáticos; permite listar subtítulos y omitir la descarga del video. README actual: Python 3.11+; FFmpeg/ffprobe para mezcla y postproceso; EJS y motor JavaScript para soporte YouTube completo. | No genera ASR ni analiza contenido. Cambios del sitio pueden romper extractores. No publica en ese README un mínimo universal de CPU/RAM; transferencia, formato y postproceso condicionan recursos. | Código propio: Unlicense; ejecutables PyInstaller incorporan GPLv3+; otros artefactos/dependencias tienen licencias adicionales. Priorizar el ya existente; verificar dependencias antes de atribuir un fallo a login. [README oficial](https://github.com/yt-dlp/yt-dlp#readme). |
| **youtube-transcript-api — captions de YouTube** | Recupera captions manuales/automáticos, idioma, tiempos y traducciones disponibles, sin API key ni navegador. Metadatos consultados: Python >=3.8,<3.16; sistema operativo independiente. | No descarga audio ni crea texto cuando faltan captions. README advierte bloqueos `RequestBlocked`/`IpBlocked` frecuentes en IP cloud y autenticación por cookies actualmente no disponible. No declara mínimo de CPU/RAM; no necesita inferir un modelo ASR. | MIT. Candidato ligero sólo si las captions son accesibles; no sustituir el bloqueo por proxies de pago o autenticación supuesta. [README oficial](https://github.com/jdepoix/youtube-transcript-api#readme), [metadatos oficiales](https://github.com/jdepoix/youtube-transcript-api/blob/master/pyproject.toml). |
| **faster-whisper — ASR** | Whisper sobre CTranslate2; CPU/int8; Python >=3.9. PyAV decodifica audio con bibliotecas FFmpeg empaquetadas. GPU requiere compatibilidad específica CUDA/cuDNN. | El benchmark oficial de small/int8 informa 1477 MB RAM, con 8 hilos en i7-12700K, sobre 13 minutos de audio. Es una referencia del proyecto, no mínimo garantizado ni medición de este VPS. Batchear puede subir memoria. Necesita archivo de entrada y pesos compatibles; no desbloquea YouTube. | MIT. Reutilizar la instalación existente antes de añadir otro motor. La salida es texto/tiempos de voz; no prueba escucha de música o efectos. [README oficial](https://github.com/SYSTRAN/faster-whisper#readme). |
| **whisper.cpp — ASR alternativo** | Implementación C/C++, CPU y cuantización; Linux, Windows, macOS y otras plataformas. Optimización según arquitectura. CLI documentado: WAV de 16 bits; compilación con CMake y modelos ggml. | Tabla oficial: small 466 MiB disco y ~852 MB memoria; base 142 MiB/~388 MB. Son orientaciones del proyecto, no consumo máximo del proceso ni ventaja local probada. Cuantizar cambia tamaño/precisión; probar calidad sería otra tarea. | MIT. Reserva para un requisito concreto de portabilidad o memoria. No instalar ni convertir pesos ahora; duplicaría ASR sin resolver acceso ni percepción integral. [README oficial](https://github.com/ggml-org/whisper.cpp#readme). |
| **microsoft/playwright-mcp — DOM/accesibilidad y captura** | Servidor MCP de navegador; Node.js >=18. Trabaja principalmente con árbol de accesibilidad. Screenshot produce imagen estática. Soporta perfil persistente o aislado; un mismo perfil persistente no admite dos instancias simultáneas. | No declara mínimo universal CPU/RAM. El navegador consume recursos según páginas y procesos. DOM no contiene necesariamente los píxeles del video; screenshot no recupera su pista sonora ni demuestra secuencia temporal. El repositorio completo no equivale al catálogo habilitado en una sesión. | Apache-2.0. Útil para contexto visible y evidencia de UI una vez habilitada su invocación. El MCP observado aquí sigue sin funcionamiento demostrado. [README oficial](https://github.com/microsoft/playwright-mcp#readme). |

Las fuentes son ramas móviles consultadas en esa fecha; describen el proyecto publicado, no garantizan correspondencia byte a byte con las instalaciones locales. Las licencias indicadas describen los proyectos; no conceden acceso al contenido de terceros ni sustituyen licencias de dependencias, modelos o medios.

## Inventario comunicado y límites de esta investigación

El padre comunicó inventario ya cotejado: MCP `0.0.84`, Playwright/core `1.65.0-alpha-2026-10-30`, Node `20.20.2`; `~/asr/venv`: Python `3.12.3`, faster-whisper `1.2.1`, modelo small/CPU/int8, yt-dlp `2026.10.26`, PyAV `18.1.0`, CTranslate2 `4.8.5`, `pip check` correcto. `youtube-transcript-api` no está instalado en ese venv; `whisper-cli`/`whisper.cpp` no aparecen en PATH, sin concluir ausencia total. **No inspeccioné esas instalaciones**. El padre también comunica un control offline de silencio sintético de 2 s con VAD: cero segmentos; no acredita reconocimiento de voz ni benchmark. Véanse [EVIDENCIA](EVIDENCIA.md) y [PRUEBA](PRUEBA.json) para las comprobaciones del padre y sus límites.

## Prueba acotada de herencia del hijo

Identidad canónica visible: `/root/alternativas`. Método: enumeración de metadatos `ALL_TOOLS`, filtrando los cuatro nombres solicitados. Resultado exacto anunciado:

1. `mcp__playwright__browser_close`
2. `mcp__playwright__browser_navigate`
3. `mcp__playwright__browser_snapshot`
4. `mcp__playwright__browser_take_screenshot`

Esto acredita **catálogo anunciado en el hijo**, no invocación, conexión, sesión compartida, autenticación ni herencia funcional. El padre informó que `browser_navigate` a `https://example.com` y `browser_close` fueron rechazados con `MCP tool call requires approval, but approval policy is never`. En consecuencia el hijo no invocó las cuatro herramientas, no abrió navegador, no obtuvo snapshots/screenshots y no sustituyó la prueba por shell, Playwright directo ni otro Codex. La consulta de documentación por web es investigación separada, no prueba del MCP.

| Metadato del hijo | Valor acreditado aquí |
|---|---|
| task_name devuelto por spawn, según padre | `/root/alternativas`; no devolvió UUID. |
| SID/thread del hijo en `CODEX_THREAD_ID` | `01a1bd32-16a5-7e60-b1f6-ed94623c5330`, leído mediante allowlist de dos variables. |
| `CODEX_SESSION_ID` heredado | `01a1bd30-efe1-7f90-b6e0-811def9bf063`, coincide con SID del padre; no se atribuye como ID independiente del hijo. |
| Modelo solicitado en spawn, según padre | `gpt-6.1-sol`, con `fork_turns=none`. |
| Esfuerzo solicitado en spawn, según padre | `high`. |
| Modelo observado | `null`; sin metadato verificable del proveedor/runtime. |
| Esfuerzo observado | `null`; sin metadato verificable del proveedor/runtime. |

## Próximo ensayo propuesto, sin ejecutarlo

Responsable: coordinador/operador. Hipótesis: el obstáculo inmediato del navegador está en la autorización de la llamada, anterior a YouTube. Control: tras resolver esa condición por el canal del runtime, navegar una página pública neutra, obtener snapshot y screenshot y cerrar; conservar URL final, respuesta y evidencia saneada. Éxito exige respuestas reales y contenido coherente, no sólo nombres del catálogo. Si falla antes de abrir, detener la prueba de herencia funcional y conservar diagnóstico negativo.

Después, en un encargo autorizado, elegir **una** pieza pública y objetivo: captions para contenido verbal si existen; ASR local sobre un archivo autorizado si faltan; MCP para texto/imagen de la página si la UI añade información. Registrar cobertura, idioma, marcas temporales y fallo exacto. Para evaluar sonido y montaje falta una capacidad que inspeccione la señal y secuencia reales; transcripción más screenshot no permite cerrar esa aceptación. No se promete que iniciar sesión elimine un bloqueo de extracción.

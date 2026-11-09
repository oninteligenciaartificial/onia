# Prueba nativa del navegador de análisis · 9/11/2026 UTC

**Resultado:** el servidor MCP `cuentas_analisis` ejecutó las dos navegaciones autorizadas, sus snapshots y el cierre. Se pudo leer el control público de example.com y el perfil de Víctor Heras con enlaces a publicaciones/reels. No se mostró formulario de login ni challenge en el snapshot observado. **Esto no prueba por sí solo autenticación completa ni identidad de la cuenta secundaria.**

SID/thread: `01a1bd30-efe1-7f90-b6e0-811def9bf063`, el mismo de los intentos anteriores. Codex según entorno: `0.167.0`; modelo/esfuerzo efectivos no expuestos. HEAD inicial `ec24b88b5511009dc3eac3e63f3fea007fe3dacd`; rama `codex/ws-investigacion-acceso-av-20261108`. Sin cambios versionados al inicio; `capturas/` anterior ya estaba sin seguimiento.

Se leyeron AGENTS, reglas-comunes, boss-memoria, directora desarrollar-y-verificar y el briefing recibido por stdin/chat. Prevalece la autorización actual de Sergio para usar el perfil secundario mediante el gestor, con sólo dos destinos. No se abrió ni editó el registro canónico, su proyección o archivos de cuenta.

## Catálogo y llamadas reales

El catálogo anunció exactamente tres herramientas de este servidor: `mcp__cuentas_analisis__browser_navigate`, `mcp__cuentas_analisis__browser_snapshot` y `mcp__cuentas_analisis__browser_close`. Se invocaron nativamente mediante `tools` en `functions.exec`, en este orden:

| Hora UTC | Llamada | Resultado |
|---|---|---|
| 02:57:03 | `browser_navigate({"url":"https://example.com/"})` | «Destino aprobado abierto.» |
| 02:57:07 | `browser_snapshot({})` | Texto documental en varios idiomas y enlace público de IANA. |
| 02:57:10 | `browser_navigate({"url":"https://www.instagram.com/victorherasemprendedor/"})` | «Destino aprobado abierto.» |
| 02:57:15 | `browser_snapshot({})` | Perfil del referente y enlaces visibles a publicaciones/reels; sin formulario de login ni challenge en la respuesta. |
| 02:57:19 | `browser_close({})` | «Navegador de análisis cerrado.» |

No se usó `snapshot filename`, capturas, evaluate, clics, descargas ni otro servidor MCP. No se navegó por shell. Las respuestas de navigate no incluyen status HTTP, título ni URL final; no se les atribuye HTTP200 ni se inventan esos metadatos.

## Contenido público leído y saneamiento

En example.com se reconoce el texto sobre el uso del dominio en documentación y el enlace `Learn more` de IANA. No se exigió un h1 histórico.

En Instagram, el árbol de accesibilidad mostró el heading `victorherasemprendedor`, el nombre Víctor Heras, la categoría `Digital creator`, biografía pública y una cuadrícula con enlaces. Tres ejemplos **observados en el snapshot, sin abrirlos**:

- `https://www.instagram.com/victorherasemprendedor/p/DY7vyqCFDOg/`
- `https://www.instagram.com/victorherasemprendedor/reel/DYur-tjvboE/`
- `https://www.instagram.com/victorherasemprendedor/reel/DX4rykXv0ia/`

No se copian DOM completo, datos de la cuenta secundaria, identificadores de sesión web ni parámetros de seguimiento al repositorio. Se omiten navegación incidental de la interfaz y textos comerciales extensos. La referencia incidental a un log de consola no se abrió ni se copia como evidencia. No se inspeccionaron cookies, localStorage, credenciales ni archivos del perfil.

## Qué queda comprobado y qué no

**Comprobado:** llamadas MCP nativas exitosas, contenido público del control y del perfil accesible, enlaces públicos presentes y cierre informado por el puente. No apareció una barrera de login/challenge en ese snapshot.

**No comprobado:** autenticación completa o identidad de la cuenta, estado interno de cookies/perfil, apertura o contenido de los posts, reproducción de video/audio, Google/Facebook secundarios, persistencia entre procesos y retorno efectivo al visor. Según el briefing, el gestor devolverá el mismo perfil al visor cuando finalice este proceso Codex; no se adelantó ese resultado ni se intentó inspeccionarlo.

No se abrió perfil propio, feed, correo, mensajes, configuración o recuperación. No acciones de seguir/publicar/enviar, instalaciones, cambios de permisos/sandbox, relanzamiento manual del navegador, producción, servicios ni gasto. Cero hijos y ninguna otra investigación. La cuenta secundaria ya creada es contexto autorizado comunicado por Sergio; su identidad y credenciales no se verificaron ni registraron aquí.

## Preservación y entrega

Los seis documentos anteriores y las dos capturas/derivados locales previos se conservaron; sus hashes se cotejaron antes y después. No hay capturas nuevas solicitadas. `capturas/` anterior sigue local y fuera del commit, sin borrados. Sólo se publican este informe y [PRUEBA-PERFIL-CUENTAS.json](PRUEBA-PERFIL-CUENTAS.json), con resúmenes saneados y metadatos.

Esta prueba acotada no acepta el encargo AV completo. El coordinador recoge el commit, ejecuta cierre y revisión independiente en otra sesión; cualquier investigación posterior necesita su alcance específico.

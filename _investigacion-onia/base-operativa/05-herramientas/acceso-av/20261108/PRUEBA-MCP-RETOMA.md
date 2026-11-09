# Prueba MCP de retoma · 9/11/2026 UTC

**Resultado: las cuatro herramientas MCP nativas funcionaron en esta sesión.** Navegación única a `https://example.com/`, título `Example Domain`, lectura real del árbol de accesibilidad, captura pública observada y cierre de página confirmado. El bloqueo anterior de aprobación no se reprodujo. No se usó Playwright por shell.

SID/thread conservado: `01a1bd30-efe1-7f90-b6e0-811def9bf063`. Codex según entorno: `0.167.0`; modelo/esfuerzo efectivos no expuestos. Rama `codex/ws-investigacion-acceso-av-20261108`; HEAD inicial `c2e13506544b44d645c9379781ff4354e4bbaa65`, worktree inicialmente limpio. Se leyeron AGENTS, reglas-comunes, boss-memoria, ESTADO y directora desarrollar-y-verificar; el briefing de retoma se recibió por stdin/chat. No hijos, investigación adicional ni modificación del registro canónico.

## Cuatro llamadas reales

Catálogo de `ALL_TOOLS`: exclusivamente `mcp__playwright__browser_navigate`, `browser_snapshot`, `browser_take_screenshot` y `browser_close` para este servidor. Se invocaron secuencialmente mediante `tools.mcp__playwright__...` en `functions.exec`.

| Hora UTC (9/11) | Herramienta y entrada | Resultado observado |
|---|---|---|
| 01:49:35 | `browser_navigate({"url":"https://example.com/"})` | URL final idéntica y título `Example Domain`. Sin rechazo de aprobación. MCP no devolvió status HTTP. |
| 01:49:43 | `browser_snapshot({})` | Párrafos documentales en seis idiomas y enlace `Learn more` a `https://iana.org/help/example-domains`. |
| 01:49:48 | `browser_take_screenshot`, filename `capturas/example.png` dentro de la carpeta asignada, scale `css`, type `png` | Captura de viewport 1280×720 guardada. Argumento filename completo en JSON. |
| 01:49:55 | `browser_close({})` | `No open tabs. Navigate to a URL to create one.`; ejecución informada `await page.close()`. Página cerrada. |

El árbol devuelto incluye el párrafo español que explica el uso documental del dominio sin necesidad de permiso y desaconseja usarlo para pruebas o monitoreo. No anuncia heading/h1; el éxito se basa en URL, título y contenido actual, sin exigir el h1 histórico. Se obtuvo árbol de accesibilidad, no HTML serializado completo. No se abrió el enlace ni se navegó a otro destino.

Después del cierre abrí el PNG con `view_image`: fondo gris claro, columna centrada con icono de libro, párrafo inglés y traducciones, coherentes con el snapshot. La parte española queda parcialmente recortada al borde inferior: es captura del viewport, no página completa.

## Captura conservada fuera del commit

Ruta absoluta:

`/home/onia-codex-worker/repos/onia-ws-investigacion-acceso-av-20261108/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/capturas/example.png`

SHA-256: `d3be9d2fc2ded008202697ef46909ee3be08d870543fb3af5a56ee0480784f0c` · 82867 bytes · 1280×720.

La navegación también generó automáticamente `capturas/page-2026-11-09T01-49-35-844Z.yml`, 1560 bytes, SHA-256 `27a94f1e714be975d502118e84745ae3874c37dce85abf00be3e9e27208746cc`. Ambos archivos permanecen locales, sin borrar ni incorporar a Git. No son evidencia transferible por este commit: el coordinador debe conservarlos antes de retirar el worktree. Es esperable que `git status` muestre `capturas/` sin seguimiento; no se afirma limpieza total final.

## Wrapper por proceso y diferencia con el intento anterior

Se leyó sin modificar ni ejecutar:

`/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/acceso-av/20261108/codex-con-playwright.py`

SHA-256: `d9dcea17da14a582f0bdb28cb4fa6990300696c1d57dfbdfdcf535c7a038e095`.

Su fuente añade pares `-c mcp_servers.playwright.CLAVE=VALOR` al Codex existente y conserva los argumentos originales del harness, incluidos `--ignore-user-config` y el perfil de sandbox. Configuración: Node local, stdio sin puerto; MCP0.0.84 existente; Chromium1252 por executable-path; `--headless --isolated --sandbox`; `default_tools_approval_mode=approve`; `enabled_tools` limitado a las cuatro herramientas; required/enabled true, timeout de arranque30s y de herramienta60s. Args exactos en JSON. No perfil persistente ni storage-state/cookies suministrados.

**Procedencia de la corrección:** la continuidad del coordinador declara que el primer lanzamiento no recibió el ajuste de aprobación y esta retoma sí. Declara además preparación AppArmor aplicada por Sergio, perfil `onia-chromium-1252` cargado y restricción global1 conservada; su control previo informó namespaces/Seccomp activos y HTTP200. Son comprobaciones del coordinador, no repetidas aquí.

La evidencia anterior conserva el error real `MCP tool call requires approval, but approval policy is never`. Aquel informe leyó un archivo del coordinador que ya contenía `approve`, con el mismo hash que hoy; **leer ese archivo no demostraba qué configuración recibió el proceso anterior**. No convertir esa lectura en prueba de que el primer lanzamiento ya tenía el ajuste efectivo. No se recuperó argv efectivo anterior ni se verificó argv del proceso actual: no se puede aislar causalidad entre cambios de autorización y AppArmor sólo con estas cuatro llamadas. El hecho nuevo comprobado es que ahora las herramientas ejecutan el control y no reproducen el rechazo.

Los cuatro documentos previos permanecen byte a byte intactos; sus hashes iniciales/finales se cotejan en el JSON nuevo. No se corrige ni rehashea evidencia histórica para aparentar otro resultado.

## Alcance y salida

Sólo se publican este informe y [PRUEBA-MCP-RETOMA.json](PRUEBA-MCP-RETOMA.json), con la evidencia saneada. El sandbox no fue deshabilitado y esta ejecutora no modificó wrapper, AppArmor, permisos, instalación, configuración global ni servicios. La comprobación interna de namespaces/Seccomp procede del coordinador; aquí se acredita el flujo MCP público, sin inspeccionar cuentas, cookies ni visor de Sergio.

No se prueba landing de Erik, herencia nueva, ASR ni percepción audiovisual integral: la continuidad acotó el objetivo a example.com y prohibió hijos. No se crearon cuentas ni perfiles; siguen propuestas. Sin web adicional, instalaciones, APIs pagas, producción, n8n, Docker ni borrados. El coordinador conserva cierre, revisión independiente y eventual aceptación/integración; esta publicación de rama no los sustituye.

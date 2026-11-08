# Evidencia y límites del análisis

Consulta: 8-nov-2026, America/Caracas. Corte técnico observado: `2026-11-08T20:34:29Z` (16:34:29 Caracas). Alcance: investigación pública de sólo lectura, inspección local permitida y documentos. No es implementación ni certificación de accesos.

## Procedencia local

- Worktree: `onia-ws-analisis-conectores-20261108`; rama `codex/ws-analisis-conectores-20261108`.
- HEAD inicial: `6ed5a985a4ba0cb0598e6d055d5d2d50351f8ba0`; `git status --short` inicial vacío. No se tocó el checkout `~/repos/onia`.
- Briefing recibido por stdin en el encargo; no se creó copia de tarea ni se editó su JSON o proyección.
- Lecturas aplicadas: AGENTS.md; base operativa `00-MAPA/ESTADO.md` y `ESTRUCTURA.md`; `04-operacion-agentes/reglas-comunes.md`, `boss-memoria.md`, `ORQUESTACION.md`, selección desarrollo de `orquestacion.json`, pendiente `codex-conectores.md` y apartados pertinentes del registro de errores (fuente conocida no prueba acceso, secretos cloud no son SSH, catálogo no es conexión).
- Fuentes técnicas: `05-herramientas/accesos.md`, contrato `cloud/CONTINUIDAD.md`, constructor de comandos en `scripts/harness_sesiones.py:259–282` y `06-plataforma/arquitectura.md`. La arquitectura histórica conserva cortes parciales; para permisos n8n prevalece el inventario más reciente y para esta sesión su prueba real, que no se ejecutó.
- Skill directora canónica leída: `05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md`. Anunciada en catálogo; lectura no implica ejecución de software. También se leyó la skill de apoyo del sistema OpenAI Docs para el contraste documental de Codex; sin instalar docs MCP ni usar API key.
- Preflight externo permitido: `/home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/04-operacion-agentes/evidencias/analisis-conectores-20261108/preflight.json`. Informa perfiles GitHub/Notion/Drive válidos en coordinador, MCP CLI vacío y auth ChatGPT. Su cuota es un corte ajeno de `2026-11-08T20:28:46.708Z`, no medición de consumo de esta sesión ni garantía de cuota posterior. No se copió el registro canónico.

## Comprobaciones reales

Los comandos se ejecutaron desde este worktree. Salidas de perfil se reducen a estructura/estado; no se publican identidades.

| Comprobación | Resultado observado | Alcance |
|---|---|---|
| `pwd`, `git branch --show-current`, `git rev-parse HEAD`, `git status --short` | rc=0; ruta/rama/HEAD anteriores, limpio al iniciar. | Identidad Git del trabajo, no estado de otras ramas ni producción. |
| `codex --version` | rc=0, `codex-cli 0.167.0`. | Binario instalado, no compatibilidad demostrada de cada campo documental. |
| `codex mcp --help` | rc=0; list/get/add/remove/login/logout anunciados. | No se ejecutaron add/login/get ni cambios de config. |
| `codex --help`, `codex exec --help` | rc=0; overrides `-c` TOML. Exec describe ignore: no carga config.toml; auth sigue usando CODEX_HOME. | Ayuda local, sin invocar inferencia, nueva sesión o app-server. |
| `codex mcp list --json`, capturado por Python antes de imprimir | rc=0; JSON `[]`, `servers_count=0`. No se imprimieron env ni URLs. | Configuración MCP global enumerada; no lista exhaustiva de plugins inyectados en esta sesión. |
| Inspección `harness_sesiones.command` | Hijos nuevos con Git privado y revisores reciben ignore; rama de compatibilidad antigua sin Git privado no lo añade al ejecutor. | Código leído; no se ejecutó el lanzador ni se probó herencia real. |
| Catálogo anunciado y metadatos de herramientas | GitHub, Notion, Drive disponibles para descubrimiento; n8n/X específicos ausentes. Hay herramientas de escritura entre las anunciadas. | Capacidad anunciada en este chat, no credencial instalada en CLI. |
| GitHub `get_profile({})` y Drive `get_profile({})` | Ambas llamadas sin error señalado devolvieron texto exacto `Action completed.`. | Respuesta genérica: **no acredita identidad, scopes, cuenta ni lectura de contenido**. Sin reintento ciego. |
| Notion `get_tool_access` para search/fetch/get_self | Respuesta estructurada: disponibles. Search tiene restricciones de plan en filtros/orden. | Mapa no garantiza resultado de una búsqueda ni autoriza ampliar lectura. |
| Notion `get_self({})` | Sin error; JSON con workspace y user. Sólo se verificó presencia de ambas claves. | Identidad de conexión respondida aquí; no lectura de páginas ni ACL read-only. |

No se ejecutaron T01–T10 de [PRUEBAS](PRUEBAS.md); son especificaciones. Tampoco se consultaron archivos privados de Drive, páginas personales, flujos de n8n, X API, auth.json, valores de entorno ni secretos. No se inspeccionó Docker/servicios ni se cambiaron cuentas. No se puede inferir permiso de escritura denegado a partir de la ausencia de una llamada de escritura.

## Fuentes públicas leídas

Todas consultadas el 8-nov-2026 mediante navegación pública. Se abrió el contenido; una búsqueda sola no se contó como lectura. Son páginas vivas, no snapshots inmutables: revalidar antes de implementación. No se enviaron a buscadores nombres de recursos privados, contenido del repo ni secretos; consultas sólo sobre productos y capacidades públicas.

| Fuente oficial | Cobertura usada / incertidumbre que conserva |
|---|---|
| [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp) | Transportes, env de bearer, allowlist/denylist, timeouts y plugin MCP. La documentación no acredita aplicación local. |
| [Referencia de configuración Codex](https://learn.chatgpt.com/docs/config-file/config-reference) | Preferencia de almacén OAuth auto/file/keyring. No se comprobó keyring disponible, cifrado efectivo ni archivo real. |
| [GitHub MCP oficial](https://github.com/github/github-mcp-server) | MIT, stdio/binario, read-only local y herramientas. No se descargó ni ejecutó paquete. |
| [GitHub MCP remoto](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md) y [texto raw leído](https://raw.githubusercontent.com/github/github-mcp-server/main/docs/remote-server.md) | Endpoint remoto, readonly por path/header, selección de tools. No garantiza credencial restringida fuera de MCP. |
| [Guía oficial GitHub para Codex](https://raw.githubusercontent.com/github/github-mcp-server/main/docs/installation-guides/install-codex.md) | HTTP/bearer y variable de token. Sus ejemplos de PAT clásico/.env/Docker no se adoptan como política de este encargo. Elegibilidad/precio remoto de esta cuenta no acreditados. |
| [Permisos GitHub fine-grained](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens) | Permisos por endpoint; seleccionar sólo lo necesario para el recurso. |
| [Rate limits REST GitHub](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) | API pública y autenticada con límites distintos; búsquedas y límites secundarios aparte. No se midió cuota REST de cuenta. |
| [Notion MCP overview](https://developers.notion.com/guides/mcp/overview) | MCP permite búsquedas, creación y edición; no es interfaz inherentemente read-only. |
| [Notion MCP setup/FAQ](https://developers.notion.com/guides/mcp/get-started-with-mcp) | OAuth, endpoint HTTP, planes, tokens headless y estado del servidor open source. No se probó login VPS. |
| [Notion capabilities](https://developers.notion.com/reference/capabilities) | Read content separado de Insert/Update y acceso de descendientes. |
| [Límites Notion](https://developers.notion.com/reference/request-limits) | 429/Retry-After; presupuestos por conexión/workspace y plan. No usar una cifra universal para todos los endpoints. |
| [Planes Notion](https://www.notion.com/pricing) | Existe Free; no se deduce el plan real ni una tarifa universal de integración/API a partir del catálogo. Condiciones concretas de cuenta pendientes, sin upgrade. |
| [Scopes Drive](https://developers.google.com/workspace/drive/api/guides/api-specific-auth) | Metadatos/content read-only y drive.file con modificación. Scopes read-only pueden ser amplios en recursos. |
| [MCP oficial Drive](https://developers.google.com/workspace/drive/api/guides/configure-mcp-server) | Preview, OAuth y proyecto/APIs; HTTP remoto. No prueba elegibilidad del usuario. |
| [Cuotas/precios Drive](https://developers.google.com/workspace/drive/api/guides/limits) | Uso estándar sin coste adicional y aviso de futura facturación; cuota depende de proyecto/antigüedad. No se comprobó consola ni se prometió gratuidad permanente. |
| [n8n API auth](https://docs.n8n.io/api/authentication/) → [destino leído](https://docs.n8n.io/connect/n8n-api/authentication.md) | Header, scopes Enterprise, amplitud no Enterprise y disponibilidad. Sin comprobar edición real de la instancia. |
| [n8n MCP](https://docs.n8n.io/connect/connect-to-n8n-mcp-server.md) | MCP instancia frente a Trigger; búsqueda, ejecución/edición y alcance por usuario/clientes. No se activó función ni se llamó endpoint. |
| [X precio](https://docs.x.com/x-api/getting-started/pricing) | Pay-per-usage y lecturas facturables; precio por recurso sujeto a cambio, no tarifa de cuenta verificada. |
| [X OAuth PKCE](https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code) | Scopes de lectura/escritura, caducidad y offline.access. Ninguna credencial creada/renovada. |

Las opciones A/B/C de [ANALISIS](ANALISIS.md) son una evaluación propia fundada en esas capacidades y las restricciones del encargo. La recomendación del paquete es inferencia de diseño, no resultado de un piloto E2E.

## Incidentes y alternativas

| Incidente | Causa observada, comando/acción saneada y rc | Alternativa aplicada / límite |
|---|---|---|
| Salidas agrupadas truncadas | Lecturas `cat` de fuentes extensas y navegación de varias páginas superaron presupuesto de salida; shell rc=0, no error de archivo. | Lecturas menores, sed/rg de apartados pertinentes y opens/finds de fuentes oficiales. No asumir que todo el texto truncado fue leído. |
| Advertencia de aliases CLI | Ayudas/version/list emitieron `could not create PATH aliases: Read-only file system (os error 30)`; comandos rc=0. | Continuar con salida efectiva del binario; no cambiar PATH/permisos ni usar sudo. No se atribuye el MCP vacío a esta advertencia sin evidencia. |
| Perfiles genéricos | get_profile GitHub/Drive → `Action completed.`; isError=false, rc no aplica a herramienta. | Registrar respuesta insuficiente y diferenciar preflight externo; no repetir ni declarar perfiles válidos propios. |
| URL Notion de seguridad inaccesible | Navegación a `https://developers.notion.com/guides/mcp/security-best-practices` → Internal Error/no accesible; rc no aplica. | Capacidades y setup/FAQ oficiales sí leídos; no citar la página fallida como respaldo ni inventar su contenido. |
| Búsqueda pública con resultados secundarios | Resultados incluyeron páginas no oficiales; rc no aplica. | No se usaron para conclusiones técnicas ni costes; se abrieron URLs oficiales y enlaces primarios. |

## Validación de la entrega

Revisión de cobertura: cinco servicios con estado chat/CLI, transporte, custodia, mínimo permiso, alcance, lecturas/escrituras, coste, recuperación y aceptación. Tres alternativas con flujo completo y comparación; primer acceso y decisión futura de integración con ignore. Se revisó distinción entre observado, histórico, propuesto y no ejecutado.

Checks documentales ejecutados: script Python con `pathlib`/`re` y `git diff --cached --name-only` comprobó cuatro archivos, diez enlaces relativos válidos, cero patrones de credenciales conocidos, cero rutas fuera de alcance y cero cambios sin stage. `git diff --cached --check` terminó rc=0. Revisión manual de matrices, límites y referencias completada. El escaneo por patrones es auxiliar, no garantía universal de ausencia de secretos. El hash del commit y comprobación remota se informan al entregar, para no incrustar un hash autorreferente. El ejecutor publica sólo su rama; revisión independiente, aceptación e integración a origin/master corresponden al coordinador y no se declaran realizadas aquí.

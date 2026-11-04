# onia cloud: preparación y comprobaciones

Fecha: 3-nov-2026 America/Caracas. Fuente de reglas: ../reglas-comunes.md;
skills editables únicas: ../compartibles/skills. No se mantiene otra fuente de reglas.
Repo cotejado: oninteligenciaartificial/onia, HEAD 4de11bbf893a92200b4599f064d82fc24c347e46.

## Recuperación y persistencia

Al retomar se recibió una instancia nueva. El checkout estaba limpio en el HEAD
inicial: NO persistieron cloud/, ESTADO modificado, node_modules, evidencia ni
.agents/skills de la ejecución anterior. Se reconstruyeron las fuentes disponibles
en el historial de esta conversación; package-lock.json se regeneró desde el
registry oficial con @playwright/test 1.64.1 exacto. No es una recuperación binaria
del lock anterior ni una prueba de persistencia entre instancias.
La evidencia de la VM anterior no está disponible; sus resultados se conservan
sólo como antecedente en el historial. Exportar antes de descartar cualquier VM.

## n8n: prueba actual

Sergio informa que guardó N8N_API_KEY ligada al host
n8n-sergio-n8n.hqdqgh.easypanel.host. La instancia efectiva sigue en spec_revision=1,
observed_spec_revision=1, observations_current=true, running; source version
2670e21c-8bc9-4a41-ae11-98989ecbe24e~cecfgver_6aea7cf0543881a3940b6506a6e7d98d.
Red restricted/enforced, preset package_managers, allowed_hosts=[], secrets=[].
Única comprobación del valor de entorno: N8N_API_KEY_present=false. No se imprimió
valor, placeholder ni entorno. Helper ejecutado con proxy/TLS normal: exit 2 por
clave no disponible; NO hubo petición API autenticada ni inventario obtenido.
Lectura pública HTTPS acotada falló; no se acredita conexión pública en esta instancia.

Falta aplicar a la versión efectiva de onia la vinculación secreta N8N_API_KEY y
el permiso de host n8n-sergio-n8n.hqdqgh.easypanel.host. No se puede inferir desde
esta instancia si están sólo guardados en un borrador: verificar/publicar la versión
correcta en configuración y lanzar tarea nueva con ella. Confirmar estado oficial
ready antes de probar. No hay herramienta expuesta para editar/publicar setup ni
solicitar secretos genéricos. No reenviar la key por chat ni escribirla en Git.

Corrección de la advertencia anterior: según la UI n8n 2.43.7 observada por Sergio,
la clave permite seleccionar workflow:list y expiración de 7 días. Configurar ese
scope y TTL; no asumir permisos amplios por una etiqueta noEnterprise. El scope y
expiración efectivos de la clave guardada aún no se han verificado desde Cloud.
El helper sólo realiza GET /api/v1/workflows?limit=10&excludePinnedData=true,
rechaza redirects y muestra conteos agregados, sin nombres, IDs, parámetros de
nodos, respuesta cruda, cabeceras ni secretos. No modifica ni activa workflows.
API canónica: https://docs.n8n.io/api/ .

```sh
python3 _investigacion-onia/base-operativa/cloud/n8n-inventory.py
```

## Skills y capacidades actuales

Catálogo inicial proporcionado: ninguna de las siete skills propias. Consulta
skills.list(authority=executor): skills=[], warnings=[]. Las siete fuentes del repo
existen; --check detectó enlaces ausentes, --install y --check pasaron al retomar.
Nombres: automatizar-n8n, continuidad-de-trabajo, desarrollar-y-verificar,
evaluar-catalogo-skills, mejorar-sistema, preparar-oferta-y-embudo, producir-video.
Enlaces locales comprobados no prueban autodiscovery; verificar nueva tarea.
Tests actuales: 7 bootstrap sin skips y 5 continuidad, todos OK.

Apps/MCPs expuestos (nombres, sin afirmar autenticación): Canva, ChatGPT Spaces,
Cloud Environment, GitHub, Gmail, Google Drive/Docs/Sheets/Slides, HeyGen,
Higgsfield, Notion, OpenAI Platform, Pets, Plugin Management, Sites, Vercel;
además herramientas Codex, automations, search, hotline y safety.
El catálogo incluye skills cloud de otros plugins; tener una skill no demuestra
conexión a una cuenta ni disponibilidad de sus runtimes.

Estado oficial declara remote_desktop enabled=true/state=unknown, sin herramienta
NodeREPL, control de browser/escritorio ni handoff de credenciales expuesta en este
turno. Browser remoto visible/interactivo y login humano NO acreditados. No se creó
ni inició sesión en ninguna cuenta, ni se copiaron perfiles/cookies/storageState.
El handoff de chats Codex no equivale a un handoff seguro de credenciales.
La documentación indicada por Sergio dice computer/browser use no soportado:
https://learn.chatgpt.com/docs/environments/cloud-environments . La lectura desde
esta instancia falló, por lo que esa afirmación se atribuye al encargo, no a una
verificación web local. La prueba Playwright por scripts no acredita esa capacidad.

## Preparación reproducible

Fuentes: package.json fija @playwright/test 1.64.1; package-lock fija dependencias.

```sh
bash _investigacion-onia/base-operativa/cloud/install.sh
bash _investigacion-onia/base-operativa/cloud/start.sh
```

install.sh enlaza skills, npm ci e instala sólo Chromium headless shell. No servicios
persistentes, escritorios ni actualizaciones globales. Si faltan bibliotecas OS,
inspeccionar error y añadir sólo dependencias necesarias. Mantener proxy y TLS.

Antecedente de la instancia anterior: Python 3.12.14, Node 24.22.1, npm 11.9.0,
Chromium del sistema 155.0.8059.79; 12 tests y recorrido crear/completar/retomar entre
procesos aprobados; test real sintético de botón/estado/assert/screenshot aprobado
con ONIA_CHROMIUM_PATH=/usr/bin/chromium bash start.sh desde cloud/. El primer
intento falló por setsockopt en sandbox; pasó con capacidad de ejecución de red.
No se volvió a ejecutar browser en esta reanudación; la captura anterior no persistió.

Descarga anterior de Headless Shell 156.0.8078.4 rev 1248: bloqueada con Domain
forbidden en cdn.playwright.dev. Permisos acotados propuestos para setup: conservar
package_managers y añadir cdn.playwright.dev, playwright.dev y host n8n. Documentación
https://playwright.dev/docs/browsers . Registrar redirects bloqueados antes de ampliar.
No editar /etc/codex/network-policy.json: el snapshot no concede acceso.

Setup reutilizable sólo preparado, publicación no verificada. Aplicar fuentes en
repo canónico tras revisión y configurar/publicar setup en onia; abrir nueva tarea,
comprobar catálogo, secreto ready, red y test real. Ninguna modificación de esta tarea
publica por sí sola una configuración reutilizable. La entrega remota se exportó
sin commit/push/PR; su integración posterior se comprueba en el historial Git.

Meta sigue pendiente de autorización/API específica: definir operación y activos,
permisos mínimos y documentación vigente de developers.facebook.com; entregar
credenciales por almacén seguro con expiración/rotación/revocación. No crear app,
aceptar términos, publicar, enviar mensajes ni gastar. No se tocó VPS/SSH/producción.

Exportación solicitada: JSON con ruta, contenido UTF-8 y sha256 de fuentes cloud/
y ESTADO.md, incluido package-lock; excluye node_modules, evidencia y secretos.
Evidencia agregada local: ../operacion/cloud-002 (ignorada).

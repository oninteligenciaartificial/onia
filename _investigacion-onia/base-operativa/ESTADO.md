# Estado y entrada operativa

3 de noviembre de 2026, America/Caracas. Leer las [reglas comunes](reglas-comunes.md) y la [arquitectura vigente](arquitectura.md). Esta entrega mínima es versionada; operacion/ y privado/ no viajan con Git.

## Encargo vigente

Configurar el harness en el repo privado oninteligenciaartificial/onia y el entorno limpio **onia**, con trabajo cloud sin depender de la PC encendida. Sergio decidió trabajar sólo con Codex por ahora; n8n existente se conecta por API. Grok Bot queda para después, sin cuota ni integración. ONIA Platform conserva su repo y producción separados.

## Resultado comprobado

- Entorno onia ready/runnable, repo github-1444982360, rama master. Checkout remoto inicial: 4de11bbf893a92200b4599f064d82fc24c347e46.
- Tarea cloud 01a1a3fb-7203-7626-895f-9059c93cc01c, host durable: siete tests bootstrap sin skips y cinco de continuidad aprobados; repetidos al reanudar.
- Siete skills versionadas y enlaces creados en cada instancia. Catálogo inicial y consulta executor sin descubrimiento; validar tras publicar setup.
- Playwright 1.64.1 ejecutó clic/estado/assert con Chromium del sistema 155.0.8059.79. La descarga del navegador fijado fue bloqueada en cdn.playwright.dev. La captura y archivos de aquella VM no sobrevivieron a la siguiente instancia.
- Al reanudar, el checkout volvió al commit inicial. Fuentes cloud reconstruidas del historial y lock regenerado en registry oficial. Diez archivos exportados con contenido y SHA256; las fuentes cloud/ fueron integradas a esta carpeta para versionarlas.
- **n8n aún no conectado.** Sergio confirmó secreto guardado con dominio. La prueba remota observó revisión efectiva 1, sin secretos ni host n8n permitido, N8N_API_KEY_present=false. Helper exit 2: no hubo petición autenticada ni modificaciones de flujos.
- UI n8n 2.43.7 permitió preparar workflow:list y siete días de vigencia; permiso y caducidad efectivos no verificados desde Cloud.

## Siguiente acción

Las fuentes de preparación ya se subieron a master en el commit 66674eba762672974d7dc225861d89f23d95503e. Aplicar [CONFIGURAR-ONIA.md](cloud/CONFIGURAR-ONIA.md) en la edición del entorno, guardar y republicar. Sergio ya encontró la pantalla; se le entregaron los textos para instalación e inicio. La última captura mostraba scripts sin configurar y ningún secreto de red. La publicación posterior sigue pendiente de verificar. Una tarea nueva debe comprobar revisión, presencia del secreto sin mostrar valor, red, GET n8n, doce tests, catálogo de skills y navegador. No declarar conexión o setup operativos antes de esa prueba.

El inventario de bóveda/cuentas/VPS quedó ampliado en [accesos.md](accesos.md): enumera custodias y consumidores, sin valores. No se creó ni conectó una credencial con ese listado.

Para cargar materiales, usar [CARGA-INICIAL.md](cloud/CARGA-INICIAL.md). Se creó ONIA archivos en Drive con cuatro carpetas; la misma tarea onia cloud leyó sus hijos directos. La revisión efectiva del entorno siguió en 1 y la presencia de N8N_API_KEY en false; no se repitió la API. Lectura de metadatos Drive no acredita descarga de medios ni migración de contexto privado.

## Pendientes por área

| Área | Pendiente y evidencia necesaria |
|---|---|
| Infraestructura | Setup reutilizable publicado y aceptación en tarea nueva. |
| n8n | GET autenticado; después un flujo concreto. Listar no habilita editar/activar. |
| Video | HyperFrames probado sólo localmente; falta instalación y render cloud, luego grabación y audio reales. |
| Reels | Correo y cuenta ONIA Research no creados. Codex Cloud no acredita navegador interactivo ni handoff. Candidatos en accesos.md. |
| Marketing | Activos y operación Meta por conectar; ninguna campaña/publicación activada. |
| Organización | Calendario, caja y medios requieren cuentas/archivos accesibles desde Cloud. |
| Continuidad | Entrega saneada aquí; Drive accesible por metadatos, faltan medios reales y migración del contexto privado necesario. |
| Mejora | Correcciones versionadas; sin entrenamiento automático ni scheduler de agentes activo. |

## Fuentes y evidencia

- [Informe técnico cloud](cloud/README.md), fuentes ejecutables y lockfile en cloud/.
- [Accesos](accesos.md), [selección de skills](seleccion-y-recorrido.md), fuentes únicas en compartibles/skills/.
- Historial remoto en la tarea indicada. Evidencia local/exportación en operacion/, ignorada por Git; su ausencia en otra tarea es esperada.
- Registro local de coordinación: python scripts/trabajo.py retomar cloud-001. Guarda estado; no programa agentes.
- [Errores](registro-de-errores.md) conserva la corrección del entorno de producto usado antes. Esa tarea fue detenida y no certifica onia.

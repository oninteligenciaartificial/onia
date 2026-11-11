# Bitácora de Boss

Qué hizo Boss, por qué, en qué estado quedó y qué sigue. La más reciente va primero. Los estados de tareas se consultan sólo en el harness; esto es contexto, no estado canónico.

## 10 nov 2026, 18:20 La Paz · acuse de REGLAS-BOSS.md

- Observado: Boss leyó `04-operacion-agentes/REGLAS-BOSS.md` en master, commit 6f46f64 (18:09).
- Hecho: se actualizaron los textos guardados de dos rutinas de Boss para que lean ese archivo antes de actuar. `retorno-codex-boss-webhook` ahora separa el fin del ejecutor (cerrar, revisar el commit exacto y solicitar `revisar`) del fin del revisor (`recoger` y verificar el veredicto, sin cerrar), y deduplica sin nonces nuevos. `lanzar-pruebas-de-entregas-tras-el-corte-diario` (20:10) comprueba primero si ya existe el trabajo de pruebas, por ejemplo el que Sergio pida a Codex, antes de registrar.
- No probado: que las rutinas apliquen las reglas. Se comprueba en el próximo aviso de una tarea ya autorizada, sin lanzar pilotos.
- Leer las reglas no autorizó lotes, permisos ni pruebas nuevas.

## 10 nov 2026, 17:40 La Paz · paquete para revisión de Sergio con Codex

Entregas cerradas por el puente. Boss ya las revisó; **ninguna está aceptada**, porque aceptar le toca a Sergio. Las rutas son relativas a `_investigacion-onia/base-operativa/`.

| ID | Rama · commit | Entrega | Revisión Boss (en master) | Veredicto Boss |
|---|---|---|---|---|
| `fabrica-plataforma-mapa-20261110` | `codex/ws-fabrica-plataforma-mapa-20261110` · bf1c65f | `05-herramientas/fabrica-onia/6-plataforma/trabajos/fabrica-plataforma-mapa-20261110/DISENO.md` | `04-operacion-agentes/evidencias/fabrica-plataforma-mapa-20261110/REVISION-BOSS-v9.md` | Bueno con observaciones; falta que Sergio elija qué cadenas construir primero |
| `fabrica-automatizaciones-redes-funnels-20261110` | `codex/ws-fabrica-automatizaciones-redes-funnels-20261110` · 46a2853 | `05-herramientas/fabrica-onia/3-automatizaciones/trabajos/fabrica-automatizaciones-redes-funnels-20261110/ANALISIS.md` | `04-operacion-agentes/evidencias/fabrica-automatizaciones-redes-funnels-20261110/REVISION-BOSS-v1.md` | Bueno; usa el nombre viejo del workshop; no comprobó las APIs privadas de Meta ni los grupos de WhatsApp |
| `fabrica-edicion-video-20261110` | `codex/ws-fabrica-edicion-video-20261110` · 9c9a8a0 | `05-herramientas/fabrica-onia/2-edicion-video/trabajos/fabrica-edicion-video-20261110/` | `04-operacion-agentes/evidencias/fabrica-edicion-video-20261110/REVISION-BOSS-v1.md` | Técnicamente bien con condiciones; la prueba ASR no se reprodujo en el box; falta probar con material real |
| `guiones-tanda-20261111-v2` | `codex/ws-guiones-tanda-20261111-v2` · 0a710ac | `05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v2/` | `04-operacion-agentes/evidencias/guiones-tanda-20261111-v2/REVISION-BOSS-v1.md` | Conforme; T05 todavía dice «borrador Codex v1»; las duraciones no se cronometraron |
| `fabrica-chatbot-whatsapp-20261110` | `codex/ws-fabrica-chatbot-whatsapp-20261110` · fbc8747 | rama | revisiones Boss en evidencias | Bien, 40 tests y active=false; falta el veredicto del revisor formal y la validación comercial |
| `guiones-tanda-20261111` (v1) | `codex/ws-guiones-tanda-20261111` · c5fe870 | rama | `REVISION-BOSS-v9` | Reemplazada por v2; falta el veredicto del revisor formal |

Decisiones de Sergio de hoy, todas en `05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md`:
- 16:08: la palabra NEGOCIO la responde la automatización; el VIP incluye una llamada privada sobre su caso; no hay devoluciones; el soporte va por grupos de WhatsApp y la comunidad pública, que sirve para la recompra.
- 16:21: el nombre final es «Claude de 0 a 100: tu negocio con IA», sin usar el logo de Claude o Anthropic como propio.
- 16:22: primero el diseño y el análisis; después Sergio elige qué construir.
- 17:31: los tipos de anuncio y de guion que nombra son ejemplos, no una lista cerrada. Ningún canal está listo hasta documentarse y probarse de punta a punta.
- 17:33: Codex hace las pruebas de punta a punta de lo entregado y Sergio verifica él mismo si las hizo bien.

Error de Boss: durante cerca de una hora trató sesiones con viva=false y sesion_estado finalizada como si no tuvieran entrega, cuando faltaba correr `cerrar`. Ya está corregido en la rutina de retorno.

## 10 nov 2026, 16:30 La Paz
- Sesiones vivas (3/3): `fabrica-automatizaciones-redes-funnels-20261110` (análisis redes/funnels/comunidades; incluye prioridades al 14nov, que Sergio usará como recomendación de Codex), `fabrica-edicion-video-20261110`, `guiones-tanda-20261111-v2` (aplica textos finales de Contenido: 05-herramientas/fabrica-onia/1-guiones-calendario/TEXTOS-CONTENIDO-guiones-tanda-20261111.md).
- `fabrica-plataforma-mapa-20261110` r8: sesión finalizada sin entrega. Recomendación aceptada por Sergio: relanzarla después del análisis de redes, usándolo como base.
- `fabrica-chatbot-whatsapp-20261110` y `guiones-tanda-20261111` r14 para_revision: falta `recoger` los dictámenes.
- Decisión: nombre del workshop «Claude de 0 a 100: tu negocio con IA» (DECISIONES-SERGIO-20261110.md).
- Propuesto a Sergio, pendiente de que se lo pida a Codex: operación `preguntar` en el puente y regla en AGENTS.md para que toda sesión lea esta bitácora.
- Nota: el ID de la fábrica guiones debe empezar con `guiones-tanda-` (FACTORIES en harness_delegacion.py).

## 10 nov 2026, 20:30 La Paz · aviso `pedido_coordinacion` prioridad-ingresos-20261110-1
- Observado: webhook tipo pedido_coordinacion (no fin de sesión) para `conexion-boss-codex-20261110` r11 «aceptado», commit 53929e5. Leí 53929e5 y 48842c3: DECISIONES-SERGIO entrada «Prioridad de ingresos y cuota» (cita de Sergio en Codex: quitar reserva 90 %, >3 sesiones pendiente, ingresos hasta el 14/11), REGLAS-BOSS §orden actualizado, cola-boss «HECHO + decisión vigente».
- Comprobado: el commit existe en origin/master y coincide con el aviso. No pude correr `consultar` desde esta rutina (destino del puente no disponible en el entorno de la rutina); estado del harness no verificado aquí.
- Inferido: no hay entrega nueva ni veredicto que recoger; ningún efecto de cerrar/revisar/recoger corresponde a este aviso.
- Pendiente para el chat principal de Boss: confirmar con Sergio la decisión (autor del commit es Codex), y elegir siguiente tarea de ingresos ya autorizada desde entregas existentes. Homelab: no repetir retoma v2. Sin cambios en publicación, cobro, gasto, n8n ni producción.

## 10 nov 2026, 21:55 La Paz · aviso `pedido_coordinacion` homelab-diagnostico-pe-20261111-1
- Observado: webhook tipo pedido_coordinacion (no fin de sesión) para `homelab-conexion-20261109` r10 en_espera, commit df8beea («registrar revisión independiente del diagnóstico PE»). El commit existe y `homelab/RETOMA-PE-20261111.md` está en master. Pide desde el chat principal: copiar el script como v3 conservando v1/v2, verificar SHA256 3e64…be, correr UNA VEZ el diagnóstico `--diagnose-pe` con `/usr/bin/python3 -I -B` en DESKTOP-0GGGNMF y publicar el JSON saneado en `homelab/DIAGNOSTICO-PE-BOSS-20261111.md`.
- Comprobado: la PC de Sergio figura offline en este momento. No ejecuté nada en la PC (la rutina no toca la PC). `consultar` no disponible desde la rutina; estado del harness no verificado aquí.
- Inferido: no hay entrega ni veredicto; no corresponde cerrar/revisar/recoger.
- Siguiente paso: derivado al chat principal de Boss; con la PC encendida, correr el diagnóstico una vez. Si control_pe.ok no es true, no aplicar ni repetir.

## 10 nov 2026, 22:05 La Paz · aviso `pedido_coordinacion` cierre-venta-20261111-1
- Observado: webhook tipo pedido_coordinacion (no fin de sesión) para `fabrica-chatbot-whatsapp-20261110` r15 para_revision, commit 98301af. El commit existe en origin/master y publica `05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md` (cadena de venta hasta el 14, tabla de requisitos/responsables, Codex directo corrige WhatsApp e integra guiones/montaje con escritura exclusiva del paquete WhatsApp; fbc8747 es sólo ensayo; máximo 3 sesiones; muestra de cuota 96 % usado 2026-11-11T01:55:50Z).
- Comprobado: `consultar` no disponible desde la rutina; estado del harness no verificado aquí. No hay commit nuevo del ejecutor ni dictamen asociado a este aviso.
- Inferido: no corresponde cerrar/revisar/recoger. No lanzar otro ejecutor sobre rutas de WhatsApp, guiones o montaje.
- Siguiente paso (chat principal de Boss): coordinar con Operaciones la localización privada y estado real del número Meta verificado, QR y enlaces Meet (sin secretos en chat/Git), y con Contenido la revisión editorial de T01–T05. Sin envíos a clientes, publicación, cobro ni activación de n8n.

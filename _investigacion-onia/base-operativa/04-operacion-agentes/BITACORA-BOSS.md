# Bitácora de Boss

Qué hizo Boss, por qué, en qué estado quedó y qué sigue. La más reciente va primero. Los estados de tareas se consultan sólo en el harness; esto es contexto, no estado canónico.

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

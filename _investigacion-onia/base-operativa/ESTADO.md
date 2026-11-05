# Estado operativo de ONIA

**4 de noviembre de 2026, America/La_Paz.** Fuente oficial: este repositorio privado. [PLAN](PLAN.md) mantiene la dirección y los programas vigentes; [reglas comunes](reglas-comunes.md), la autoridad y permisos. Los reportes históricos no se volvieron a ejecutar por esta consolidación documental.

## Decisión vigente y recuperación

Sergio autorizó: **«Pero subi todo para que sea la fuente oficial, avisale a la sesion»**. Se incorpora el cuerpo documental útil de esta sesión y sus entregas cloud, además de índices: [consolidación](continuidad/2026-11-04/README.md), quince Pages y [currículo](continuidad/2026-11-04/aprendizaje.md). La decisión anterior de conservar sólo en biblioteca queda sustituida para este material. Credenciales, perfiles de navegador, medios binarios y configuración runtime privada permanecen fuera de Git.

Harness: **oninteligenciaartificial/onia**, entorno **onia** en Codex Cloud. Producto: repo independiente **onia-platform**. ONIA-CENTRAL excluido. VPS conserva startup y n8n, sin navegador, render pesado o nuevos modelos. Grok Bot diferido por falta de cuota.

**Coordinación operativa local; ejecución por áreas en cloud.** Tras las pruebas COORD-PROBE-20261104 y COORD-LOCAL-CLOUD-20261104, esta sesión local despacha encargos y recupera resultados. Jefe y Desarrollo cloud tienen lectura/consulta de chats, pero no send_message_to_thread/create_thread en sus catálogos actuales. ONIA · Jefe conserva planificación/síntesis cloud; Organización diaria escribe Notion/Calendar. [Prueba y reparto](continuidad/2026-11-04/coordinacion-local-cloud.md). La instrucción posterior de Sergio autoriza preparar frentes y avanzar por áreas, sustituyendo el STOP histórico; no autoriza por sí sola gasto, publicaciones, mensajes reales o producción. [SESIONES](SESIONES.md) registra roles e IDs.

## Evidencia y límites

| Componente | Resultado observado o reportado | Límite |
|---|---|---|
| Harness | Arranque y sesión nueva en 9a3d4ce: doctor y 28 tests Python. Helper Meta 9972d26: seis tests. | Pruebas históricas; no repetidas por editar documentos. |
| Skills | Nueve fuentes y enlaces idempotentes; seis chats iniciales las leyeron por archivo. | Descubrimiento nativo automático no acreditado. Carga por área según ORQUESTACION. |
| Navegador | Bootstrap 2b1f9ab: dos bases NSS separadas/CA, HTTP 200, captura y Play hasta 4,46 s; ocho tests Node y diez harness aprobados. | No acredita login persistente ni reproducción integral de toda fuente. |
| YouTube/audio · JEF-BASE-001 | Prueba nueva del Jefe: CONNECT tunnel 403 / HTTP 000 antes del reproductor, conservando proxy/TLS. Pages rechazó WAV por formato no soportado. | Causa exacta sin determinar; no atribuir Error 153 ni nueva escucha/ASR. Revisar túnel/política y repetir al cambiar la condición. |
| n8n | Lectura HTTP 200 histórica. [Piloto](continuidad/2026-11-04/fuentes-cloud/n8n-piloto.md): tres workflows inactivos y 60 verificaciones HTTP del circuito, con Meta/publicación/recurso/interés simulados y pago/acceso manual. | **Atomicidad runtime fallida:** carrera produce dos filas. Quince pruebas PostgreSQL temporales aisladas pasan, sin integración al workflow. No activar. |
| n8n → Codex | [CLI 0.166.0-alpha.1](continuidad/2026-11-04/fuentes-cloud/launcher-cloud.md): list remoto 401 pese a login ChatGPT local; cero tareas creadas, ENV_ID no identificado. | Despacho/callback/recuperación no probados. Evaluar device auth en lanzador dedicado, sin copiar auth de la PC. |
| Meta Ads | Editor reportó /me/permissions y /me/accounts: 401, OAuth 190/463 por token vencido. GET 200 anterior histórico. | Renovación y lectura posterior pendientes; ninguna campaña modificada. |
| Instagram | Cuenta objetivo @sergiourcullo; OnIA Social API con Instagram Login seleccionada. | Cuenta/token IG no conectados según última evidencia; comentarios necesita permiso propio. Lectura pública/ads_read no acredita publicar o enviar. [Accesos](accesos.md). |
| Higgsfield | Perfil/saldo consultado: plan pro, 585 créditos, unlim_available=false en ese momento. Catálogo de formatos/UGC y Tripo 3D observado; Jefe confirmó lectura de perfil. | Saldo fechado, no garantizado. Sin generación, integración, calidad ni entrega 3D probadas; comprobar costo/derechos antes de generar. |
| Conectores | JEF-BASE-001 confirmó lecturas de Pages, Notion Sergio Hoy, perfil Calendar y perfil Higgsfield. | Sólo esas operaciones. No prueba todas las cuentas ni credencial runtime n8n→Notion. |
| Investigación | [Referentes](continuidad/2026-11-04/fuentes-cloud/referentes.md), secuencia 10: Hormozi/Heras con muestras, Iman textos/rutas, Pedro por láminas y pista procesada. | Sin visionado continuo/escucha integral, auditoría interna ni causalidad de ventas. Nuevos referentes registrados, no analizados. |
| Video | [P2 v2](continuidad/2026-11-04/fuentes-cloud/video-y-audio.md): MP4 real de 48 s, 1080×1920, H.264, sin voz; 17 checks y cache hit reportados. Maquetas vertical/horizontal y recetas preservadas. | CLI manual, no enqueue/callback. MP-M02 requiere voz/toma; maqueta sin aprobación para publicar. |
| Contenido | [Paquete editorial v2.0](continuidad/2026-11-04/fuentes-cloud/guiones-y-workshop.md), secuencia 16: mismos 35 IDs, 29 guiones concretos y 6 plantillas de diario; Kit PLAN incluido. | Borradores en revisión. V1.2 rechazada; fechas no son programación. Cinco videos/día y diario 20:00 son objetivos sin capacidad medida. |
| Oferta y demo | [D1](continuidad/2026-11-04/fuentes-cloud/demo-d1.md): ficha→tres respuestas→contraste, ensayo textual cloud con QA independiente. | Sin alumnos, demanda, venta o cobro validados. Brief vigente sólo en PLAN; Bs 50/55 min y ofertas anteriores son históricos, no condiciones actuales. |
| Producto | [Platform](continuidad/2026-11-04/fuentes-cloud/producto.md): lectura a0488f0/seis tareas; recorrido dental ADMIN→cita→QR manual→reentrada recomendado. Configuración de ocho servicios sin puertos publicados. | Diferencia estática QA/checkout, no bug runtime/E2E. Sin código, migración o despliegue de producto en este cierre. |
| Panel y cola | [Sergio·Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) y [cola](https://app.notion.com/p/40e2eb20bdfd81259c44e8328cd52171): 20 tareas (WS-W01–05, MP-M01–05, P01–06, cuatro transversales); 35 borradores aparte. | No son 55 tareas activas. Última lectura del Jefe aún vio STOP desactualizado; Organización debe proyectar dirección actual sin duplicar IDs. |
| Calendar | Por orden «Eliminalos», eliminados seis eventos antiguos «Claude de 0 a 100» de 4/5/6 noviembre; relectura sin esos eventos. | Sin eventos de reemplazo o nuevas reservas. Este cierre no vuelve a modificar Calendar. |
| Memoria y aprendizaje | Jefe leyó GitHub y plan cloud. Otro subagente recuperó actualización de Page secuencia 9→11 sin recibir valores en el encargo. Aprendizaje entregó currículo y ejercicio. | Acredita recuperación de esa Page, no sincronización global, memoria ilimitada ni servicio 24/7. |

### Cobertura audiovisual

Pedro: MP4 público y 19 láminas en cloud; 542 muestras a 6 fps inspeccionadas conjuntamente por coordinación/QA entre 0 y 90,167 s de 90,32 s. YAMNet CPU procesó pista 90,35 s en 188 ventanas. Qwen7B falló control de silencio y se descartó como evidencia acústica. CLAP procesó 19 ventanas generales y 17 dirigidas; efectos específicos siguen ambiguos y requieren comprobación humana breve. En VM, sin VPS/API paga; no atribuir escucha directa a coordinación. [Reporte detallado](continuidad/2026-11-04/fuentes-cloud/video-y-audio.md).

Hormozi: reel 89 s por seis fotogramas/caption SALES y lección larga por puntos; Heras: VSL por tres muestras/canales desde web; Iman: textos/rutas propios con YouTube bloqueado. Nombres nuevos y dudas de identidad en [índice](investigacion/2026-11-04/README.md).

## Entorno, secretos y revisiones

- onia observado listo/ejecutable, repo onia/rama master; versión publicada reportada **6aeb5d2767cc81a3aee4674cf6485f5d**. Un push documental no republica ni actualiza automáticamente VMs existentes.
- Editor: running/connected, /workspace/onia, checkout **6ca7762**, n8n listado 200 y Meta 401 en último reporte. Desarrollo antiguo es otra VM; no heredar secretos/estado entre sesiones.
- N8N_API_KEY y META_ADS_ACCESS_TOKEN están como entradas de secretos de red; segunda vencida. META_IG_ACCESS_TOKEN pendiente según evidencia. Valores nunca en Git; [inventario](accesos.md).
- Consolidación desde master **14c786d** en checkout aislado, preservando cambios remotos anteriores. Consultar commit en historial Git; este cierre no ejecutó nuevas APIs.

## Próximas acciones

| Trabajo | Responsable y solución concreta | Criterio de cierre |
|---|---|---|
| Fuente oficial | **Completado:** Jefe recuperó PLAN/ESTADO/SESIONES/consolidación desde Git en 1884335 y explicó el hito comercial/límite. Coordinación local integra nuevas decisiones; cada área preserva su trabajo al actualizar. | Se verificaron29 textos remotos sin diferencias y15 hashes. Mantener la revisión leída sin duplicar frentes. |
| YouTube | Desarrollo revisa túnel/política; Video contrasta imagen/audio/transcripción. Alternativa si bloqueo persiste: archivo autorizado en cloud y revisión humana puntual. | Fuente reproducida, tiempos/cobertura/audio contrastados y fallo recuperable. |
| n8n | Automatizaciones integra reserva transaccional con destino/rol acotados; prueba carrera, reinicio, conflicto, takeover, STOP, timeout incierto. | Mismo evento no duplica efectos en workflow real; SQL aislado no basta. |
| Workshop | Marketing retoma WS-W01/02 con D1 y ficha de PLAN; ensayo humano previo a condiciones/preventa. | Resultado, error/corrección, ayuda/tiempo reales; oferta revisable sin inventar demanda. |
| Panel/aprendizaje | Organización proyecta dirección actual en home existente; Aprendizaje prepara práctica ligada al trabajo. | Una cola, fuentes/fechas y explicación real de Sergio. |
| Radar/canales | Ejecutar programas de PLAN por función, aprovechando accesos comprobados. | Duplicado/corrección/caída, ejecución cloud, permisos y salida revisada antes de activación. |

**No hay evidencia de scheduler diario, publicación social, chatbot real, disparador n8n→Codex ni resúmenes de voz activos.** Las propuestas no son esas operaciones; los objetivos no son cobros.

[Consolidación y procedencia](continuidad/2026-11-04/README.md) · [Sesiones](SESIONES.md) · [Mapa](MAPA.md) · [Cerebro diario](CEREBRO-DIARIO.md). Git conserva documentos/decisiones; cloud medios/descargas; Notion vista cotidiana; Calendar compromisos. Las instrucciones actuales de Sergio prevalecen.

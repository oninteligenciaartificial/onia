# Estado operativo de ONIA

**5 de noviembre de 2026, America/Caracas.** Fuente oficial: este repositorio privado. [PLAN](PLAN.md) mantiene la dirección y los programas vigentes; [reglas comunes](reglas-comunes.md), la autoridad y permisos. Los reportes históricos no se volvieron a ejecutar por esta consolidación documental.

## Estado vigente y relevo local · 5 de noviembre

Sergio decidió que **el repo es la única fuente de verdad para decisiones, reglas, estado y handoff**. Notion proyecta lo vigente y Pages conserva medios/procedencia. [Entrega del 5/11](continuidad/2026-11-05/README.md) incorpora las siete revisiones locales, el brief D1 y su reporte; `operacion/` queda como ubicación de artefactos privados, no autoridad documental. Credenciales, perfiles, binarios y datos personales siguen fuera de Git.

**Siete áreas locales; una sola jefa.** Sergio ordenó reemplazar la jefa anterior por **ONIA · Jefa v2**, chat `01a1ab9c-15b2-7a03-9588-2daab62a93eb`, host local. Está designada y en espera de commit/recepción, sin rol operativo activo todavía. La anterior `01a1a29c-3a3d-7b50-aef6-41305ce5faae` cierra el relevo; su archivo fue ordenado, **no confirmado**. No afirmar handoff aceptado ni mantener dos jefas operativas. Roles y orígenes en [SESIONES](SESIONES.md); condiciones de recepción en [HANDOFF-JEFA](continuidad/2026-11-05/HANDOFF-JEFA.md).

Las continuaciones locales recuperan documentos; no equivalen a trasladar VMs, historial completo ni secretos. Los orígenes cloud se conservan, reportados idle al traspaso, sin borrado ni reactivación acreditados aquí. Harness: repo `oninteligenciaartificial/onia`; producto: repo independiente `onia-platform`. VPS conserva n8n/startup; sin mover secretos, render pesado o modelos allí. ONIA-CENTRAL excluido.

## Última entrega y alcance autorizado

- **Revisión:** siete notas recibidas y revisadas por la jefa anterior. QA independiente reportado sin hallazgos críticos de falsa atribución/ejecución. Eso acepta la revisión, no prueba integración o producción. [Índice de revisiones](continuidad/2026-11-05/README.md).
- **D1:** [brief corregido](continuidad/2026-11-05/d1-piloto.md) y [reporte del piloto silencioso](continuidad/2026-11-05/piloto-d1/reporte.md). MP4 de 43 s, 1080×1920 H.264/24 fps; 1032 frames decodificados sin error, 29/29 contrastes, render 21,071 s/un trabajador, cero audio. SHA-256 `c41798b0c33c1d42232aba8a542696748b548b1ba327560d3ff148edc5f1c71c`, cotejado con el archivo local durante esta consolidación. Hubo muestreo visual y revisión editorial de la prueba silenciosa; no escucha, comprensión humana, locución ni retención probadas. Borrador privado, no publicación. El antecedente «D1 sin MP4» de TANDA-01 queda superado sólo por este nuevo piloto de tarjetas, no por recuperar el ZIP cloud.
- **n8n:** preparación local de copia/patch **INACTIVO terminada**, turno `01a1ab95-0a78-7643-ab62-6ec96bb69730` confirmado completed por la jefa. [Bundle recuperable en repo](continuidad/2026-11-05/n8n-reserva-local/README.md), con fuentes, SQL, patch, preparación/verificador, matriz y manifiestos. [13/13 controles estáticos](continuidad/2026-11-05/n8n-reserva-local/validation-results.json): no ejecutaron nodos Code/SQL, importación, carrera ni runtime. Texto exacto y correlación de error conservados; STOP/takeover/conciliación siguen propuestos. Sin conexión VPS/DB/servicios ni activación. La consolidación sólo coteja hashes y copia textos, sin cambiar lógica.
- **Notion:** lectura local de home/cola confirmó 20 IDs únicos y textos desactualizados; 35 borradores declarados aparte. [Hallazgos de Organización](continuidad/2026-11-05/revisiones/organizacion.md). No se modificaron paneles o Calendar.
- **Producto:** [revisión local](continuidad/2026-11-05/revisiones/producto.md) identificó worktree limpio `a0488f0` y desfase estático de QA; E2E dental de suscripción/reentrada sigue sin comprobar. No se iniciaron servicios ni cambios del producto.

La pausa general tuvo una excepción expresa para D1 como prueba y para la preparación n8n descrita; ambas unidades delimitadas están cerradas. Producto y demás producción, publicaciones, campañas, mensajes, gasto e infraestructura requieren alcance aplicable. La prioridad de Jefa v2 tras recepción es encargar la prueba del **audio real** a Video/Desarrollo; este handoff no la ejecuta. No hay scheduler ni continuidad automática acreditada.

## Evidencia histórica recuperada · 3–4 de noviembre

[TANDA-01](continuidad/2026-11-04/tanda-01/README.md) conserva workshop listo para ensayo humano, W1 corregida en cloud, fallos de n8n y E2E del producto, y la prueba local inicial de 6 s. Allí constan parada de 11 contenedores, Docker Desktop y Ubuntu/WSL con datos conservados; no se revalidó su estado actual en esta consolidación. Los reportes siguientes son antecedentes fechados, no instrucciones de lanzar nuevas tareas ni pruebas repetidas hoy.

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
| Panel y cola | [Sergio·Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) y [cola](https://app.notion.com/p/40e2eb20bdfd81259c44e8328cd52171): 20 tareas (WS-W01–05, MP-M01–05, P01–06, cuatro transversales); 35 borradores aparte. | No son 55 tareas activas. Organización actualizó y releyó el home con TANDA-01, resultados reales y tres acciones personales; conserva IDs y no creó Calendar. |
| Calendar | Por orden «Eliminalos», eliminados seis eventos antiguos «Claude de 0 a 100» de 4/5/6 noviembre; relectura sin esos eventos. | Sin eventos de reemplazo o nuevas reservas. Este cierre no vuelve a modificar Calendar. |
| Memoria y aprendizaje | Jefe leyó GitHub y plan cloud. Otro subagente recuperó actualización de Page secuencia 9→11 sin recibir valores en el encargo. Aprendizaje entregó currículo y ejercicio. | Acredita recuperación de esa Page, no sincronización global, memoria ilimitada ni servicio 24/7. |

### Cobertura audiovisual

Pedro: MP4 público y 19 láminas en cloud; 542 muestras a 6 fps inspeccionadas conjuntamente por coordinación/QA entre 0 y 90,167 s de 90,32 s. YAMNet CPU procesó pista 90,35 s en 188 ventanas. Qwen7B falló control de silencio y se descartó como evidencia acústica. CLAP procesó 19 ventanas generales y 17 dirigidas; efectos específicos siguen ambiguos y requieren comprobación humana breve. En VM, sin VPS/API paga; no atribuir escucha directa a coordinación. [Reporte detallado](continuidad/2026-11-04/fuentes-cloud/video-y-audio.md).

Hormozi: reel 89 s por seis fotogramas/caption SALES y lección larga por puntos; Heras: VSL por tres muestras/canales desde web; Iman: textos/rutas propios con YouTube bloqueado. Nombres nuevos y dudas de identidad en [índice](investigacion/2026-11-04/README.md).

## Entorno, secretos y revisiones históricas

- onia observado listo/ejecutable, repo onia/rama master; versión publicada reportada **6aeb5d2767cc81a3aee4674cf6485f5d**. Un push documental no republica ni actualiza automáticamente VMs existentes.
- Editor: running/connected, /workspace/onia, checkout **6ca7762**, n8n listado 200 y Meta 401 en último reporte. Desarrollo antiguo es otra VM; no heredar secretos/estado entre sesiones.
- N8N_API_KEY y META_ADS_ACCESS_TOKEN están como entradas de secretos de red; segunda vencida. META_IG_ACCESS_TOKEN pendiente según evidencia. Valores nunca en Git; [inventario](accesos.md).
- Consolidación desde master **14c786d** en checkout aislado, preservando cambios remotos anteriores. Consultar commit en historial Git; este cierre no ejecutó nuevas APIs.

## Próximas acciones dentro del relevo

| Trabajo | Responsable y acción | Criterio de cierre |
|---|---|---|
| Recepción del handoff | Jefa saliente cierra publicación documental; Jefa v2 recupera el commit y confirma lectura antes de asumir. | Commit identificable, recepción real y estado del archivo de la anterior comprobados; nada de ello se certifica aquí. |
| Primera prioridad: audio real | Jefa v2 encarga Video/Desarrollo después de la recepción, conforme al [contrato de prueba](continuidad/2026-11-05/HANDOFF-JEFA.md#primera-tarea-tras-la-recepción-audio-real). | Controles y evaluación de voz, música, SFX, silencios y sincronía; solución probada o intervención personal mínima respaldada por alternativas ensayadas. |
| Próxima unidad n8n | Jefa v2 conserva el bundle terminado; antes de un ensayo runtime, el administrador acredita destino PostgreSQL exclusivo y referencia de credencial restringida. | Aislamiento y acceso mínimos demostrados, sin tocar producto ni compartir secretos; provisión/importación/activación no autorizadas por esta preparación. |
| Proyección y demás programas | Organización y áreas retoman sólo el alcance que corresponda a la decisión siguiente. | Una fuente versionada, proyecciones conciliadas cuando se autoricen; sin activar Producto, publicación o gasto por este documento. |

**No hay evidencia de scheduler diario, publicación social, chatbot real, disparador n8n→Codex ni resúmenes de voz activos.** Una edición documental no ejecuta esas funciones ni demuestra cobros.

[Continuidad del 5/11](continuidad/2026-11-05/README.md) · [Sesiones](SESIONES.md) · [Plan](PLAN.md). Las referencias antiguas que todavía describan áreas cloud o autoridad de `operacion/` son históricas frente a este estado y las reglas vigentes.

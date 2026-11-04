# Estado operativo de ONIA

Actualizado el 4 de noviembre de 2026, UTC−4. Autoridad compartida: [reglas comunes](reglas-comunes.md). Estado histórico separado de resultados actuales.

## Decisión vigente

Harness: repo privado **oninteligenciaartificial/onia**, entorno **onia** en Codex Cloud. Producto: repo independiente **onia-platform**. ONIA-CENTRAL está excluido. El VPS conserva startup y n8n; no agregar navegador ni render pesado. Grok Bot sigue diferido por falta de cuota.

Sergio autorizó en el encargo actual **subir al repo información verificada y útil**. Esa autorización reemplaza la decisión anterior de conservar sólo los borradores cloud, para esta consolidación documental. No aprueba vender la oferta propuesta, activar campañas, publicar videos o responder mensajes reales.

## Resultado comprobado

| Componente | Resultado y límite |
|---|---|
| Harness | Arranque y sesión nueva en 9a3d4ce: doctor y 28 tests Python. Helper Meta en 9972d26: seis pruebas adicionales. No se repiten por cambios documentales. |
| Skills | Nueve fuentes y enlaces idempotentes. Los seis chats las leyeron por archivo. El catálogo nativo inicial no las anunció; no declarar autodetección comprobada. |
| n8n | Coordinación confirmó listado/discovery HTTP 200 y creación de un workflow sintético HTTP 200; GET posterior verifica diez nodos y `active:false`. Alcance actual mayor que sólo listar. E2E n8n real: éxito 201, duplicado 200 sin fila nueva, conflicto 409, inválida 400 y auth incorrecta 403; otra ejecución y lectura de tabla confirman una fila del evento sin duplicación. Final `active:false` y guardado de datos de ejecución deshabilitado. No prueba concurrencia, timeout real ni Meta. [Evidencia privada](https://chatgpt.com/space/page_381ee668401481918e7e45c87921e82d). |
| Meta Ads | Editor comprobó `/me/permissions` y `/me/accounts`: HTTP 401, OAuth 190/463, token vencido. El GET 200 anterior es histórico. Conservar la entrada Ads para su función; sin renovación ni campañas modificadas. |
| Higgsfield/Google | Perfil y créditos Higgsfield observados, sin generación. Gmail perfil sin leer correo. Calendar consultado sin eventos creados. Drive con carpeta ONIA; transferencia de medios reales entre VMs pendiente. |
| Video | HyperFrames 0.9.10 produjo MP4 sintético de 6 s, H.264, 1080×1920, 30fps, sin audio, decodificado e inspeccionado. No demuestra edición comercial ni pipeline de clips reales. |
| Instagram | Objetivo operativo `@sergiourcullo`: autorización separada pendiente; `META_IG_ACCESS_TOKEN` propuesta, todavía no guardada. Ruta y permisos objetivo en [accesos](accesos.md#instagram-operativo-y-continuidad-de-autenticación). Los 62 casos con mocks y diez reinicios no prueban API real, publicación, DMs ni Advanced Access. |
| Investigación | Diez fichas de referentes, incluida Víctor Heras, y síntesis de funcionamiento de redes con fuentes primarias. Textos públicos y muestras parciales de Hormozi/Erik; vídeo candidato de Víctor sin reproducción comprobada. No auditoría interna ni visionado integral. [Índice](investigacion/2026-11-04/README.md). |
| Producción editorial | Catálogo de 16 recetas y brief de seis piezas. Objetivo: cinco videos diarios, con diario real último a las 20:00. Escenario 25 por tandas + 7 diarios + 3 extras por semana; capacidad y tiempos aún sin medir. |
| Oferta | Workshop y demo textual preparados como propuesta; sin ensayo audiovisual, anuncio, compradores ni cobros verificados. Ver ficha única en el índice. |
| Producto | Lectura de onia-platform a0488f0 e instrucciones; no ejecutar código, migraciones, cobros o despliegues por esta consolidación. |
| Panel | [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) existe y fue revalidado por conector: vida, contenido, ventas, actualidad y decisiones. Informes técnicos archivados fuera de portada. Apariencia móvil y notificaciones no verificadas. |
| Continuidad | Dos chats recuperaron/actualizaron una entrada sintética desde Space sin recibir valores en el prompt. Desarrollo también recuperó biblioteca, catálogo ampliado y fuentes públicas desde cloud. Esto no sincroniza archivos o revisiones Git automáticamente. |
| Navegador | Bootstrap versionado aceptado en **2b1f9ab**: dos procesos crearon bases NSS distintas con la CA real verificada; ambos HTTP 200, título/captura inspeccionados, Play hasta 4,46 s y limpieza de ambos perfiles. TLS/proxy activos. Ocho tests Node y diez tests harness aprobados en Linux; doctor sin errores. Audio no escuchado, login persistente no probado. [Operación cloud](cloud/OPERAR.md). |

## Versiones y accesos

`N8N_API_KEY` y `META_ADS_ACCESS_TOKEN` están configuradas en secretos de red del entorno; la primera obtuvo lectura 200 y la segunda está vencida según Editor. `META_IG_ACCESS_TOKEN` todavía no está guardada: requiere autorización separada de Sergio. No pedir valores ni duplicarlos. [Inventario y renovación](accesos.md).

- VM Desarrollo: versión de entorno **6aeaa015725c81a3b2c5e7817fca85a6**; nació antes de cargar Meta. Su checkout avanzó de 9972d26 a **2b1f9ab** para aceptar el arreglo del navegador.
- Meta se comprobó en editor posterior **6aeaa134fa1881a3abd0f72ea0bd00f4**.
- El checkout de coordinación estaba en **ec62c9e** antes de esta consolidación. El commit de entrega se consulta en Git; un push no actualiza una VM existente.
- Editor preparado en **2b1f9ab**, borrador revisión 2: install/start, doctor, 28 pruebas Python, ocho NSS y una de navegador aprobados. La interfaz confirmó **«Entorno publicado»** y **«Publicado · Probar»** el 4 de noviembre, tras guardar y publicar la preparación.
- Versión publicada **6aeb5d2767cc81a3aee4674cf6485f5d**: coordinación informó hoy desde Editor **running/connected**, directorio /workspace/onia y checkout **6ca7762**; n8n listado 200 y Meta 401 por expiración. Esta edición documental no repitió APIs ni cambió configuración. El runtime antiguo de Desarrollo sigue siendo una instancia distinta.
- Checkout de esta edición en Desarrollo: **6ca77625234bcec4a9c6b6e5ece8a6f7a6852afa**, actualizado por fast-forward sin cambios previos. Hechos de Editor recibidos por coordinación; no atribuirlos como pruebas ejecutadas de nuevo aquí.
- El catálogo oficial actual muestra entorno **onia** listo y ejecutable, repo asociado y rama master. Usar versión actual para nuevos encargos que dependan de sus secretos.

## Próximo resultado concreto

1. Retomar en onia publicado el análisis de una fuente pública concreta de Hormozi y otra de Iman, con cobertura audiovisual explícita y fichas existentes. GitHub y Desarrollo ya leyeron 2b1f9ab; cargar sólo contexto del encargo. No instalar servicios en el VPS.
2. Ejecutar el [lote de seis piezas](investigacion/2026-11-04/formatos-onia.md) con material real y medir tiempo humano, render y revisiones. Ensayar la demo antes de ofrecer el taller.
3. Sergio autoriza y guarda por separado la entrada IG; después el ejecutor verifica disponibilidad, permisos, cuenta objetivo y vencimiento mediante lectura. El navegador público y ads_read no acreditan publicación/mensajería. [Pasos y fuentes](accesos.md#instagram-operativo-y-continuidad-de-autenticación).

## Mapa de pendientes y responsables

| Pendiente | Solución y próxima acción | Responsable / condición |
|---|---|---|
| Autenticación IG | Autorizar Facebook Login y guardar entrada IG separada; después validar lectura y vigencia según accesos.md. | Sergio para autorización personal; ejecutor para comprobación posterior. Sin publicación ni DMs mientras tanto. |
| Autenticación de producción | Revisar en la app actual Facebook Login for Business y campos reales de OAuth2 en Credentials de n8n; usar su Redirect URI exacta y Connect. Registrar vencimiento y acceso a datos tras autorizar. | Ejecutor prepara/verifica la ruta; Sergio completa autorización personal. Credencial no conectada, renovación automática y aviso con scheduler no comprobados; Graph Explorer queda para el piloto. [Detalle](accesos.md#instagram-operativo-y-continuidad-de-autenticación). |
| Meta Ads vencido | Conservar su entrada y renovar por la ruta oficial cuando se retome Ads; registrar vencimiento y nueva lectura. | Sergio para renovación personal; ejecutor para validación. |
| Resultado n8n | E2E sintético completado en n8n con cinco casos y persistencia secuencial; recursos conservados e inactivos. No hace falta nueva key ni intervención de Sergio para cerrar este ensayo. | Automatizaciones conserva evidencia privada; siguiente encargo debe resolver concurrencia antes de producción. Meta requiere su autorización personal separada. |
| Investigación Víctor Heras y redes | Fichas incorporadas con fuentes, límites y plan propuesto; preparar demo y ensayo sin adoptar promesas comerciales. | Escritor Git consolida la entrega; marketing/video continúan preparación autorizada. |
| Producción real | Ejecutar seis piezas y medir con clips autorizados; avanzar preparación independiente dentro del encargo. | Sergio aporta material personal; área de video ejecuta lo disponible. |
| Entrega documental | Publicar esta consolidación revisada de regla, accesos, Víctor/redes y cierre E2E sintético n8n. | Escritor Git único; resultados posteriores requieren evidencia y alcance explícito. |

Los seis chats existentes están en [SESIONES.md](SESIONES.md). Notion contiene lo cotidiano; [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md) define fuentes y responsable.

## Pendientes que siguen abiertos

No hay scheduler diario, publicación Instagram, chatbot real, disparador n8n→Codex ni resúmenes de voz activados. El calendario preparado sigue sin eventos creados; requiere aprobación del conjunto concreto previamente presentado. No se llama ventas a interés ni dinero cobrado a un escenario aritmético.

No exportar privado/ u operacion/ a Git. Los artefactos y datos personales quedan en sus almacenes; el repo conserva decisiones, documentación útil y evidencia saneada. Fuentes técnicas: [pruebas de Instagram](https://chatgpt.com/space/page_afe5a3b4a224819182d708206cb6f15d), [accesos cloud](https://chatgpt.com/space/page_2b9ade6c69bc8191a7de31805f2cdabb), [evidencia histórica](EVIDENCIA-2026-11-03.md).

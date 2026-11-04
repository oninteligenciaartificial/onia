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
| n8n | Nuevo flujo real de 17 nodos DRY_RUN inactivo: 23 casos HTTP y dos escenarios concurrentes. Carrera event_id produjo dos filas; sin atomicidad/exactly-once. BAJA domina HUMANO mediante controles append-only. Cero nodos de envío, sin Meta; SQL PostgreSQL de 30 líneas disponible como especificación no aplicada ni verificada con motor. [Evidencia viva](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75). Ensayo anterior de cinco casos queda histórico. |
| Meta Ads | Editor comprobó `/me/permissions` y `/me/accounts`: HTTP 401, OAuth 190/463, token vencido. El GET 200 anterior es histórico. Conservar la entrada Ads para su función; sin renovación ni campañas modificadas. |
| Higgsfield/Google | Perfil y créditos Higgsfield observados, sin generación. Gmail perfil sin leer correo. Calendar consultado sin eventos creados. Drive con carpeta ONIA; transferencia de medios reales entre VMs pendiente. |
| Video | [Paquete de formatos](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4): vertical 60 s y horizontal 50 s, H.264/30 fps, sin audio, cinco capítulos cada uno; no cinco videos finales. Guía, 16 recetas, composiciones y ZIP. QA cloud de decodificación/composición y hojas revisadas; material/voz real pendientes. |
| Instagram | Objetivo operativo `@sergiourcullo`: OnIA Social API con Instagram Login seleccionada; tres permisos `instagram_business_*` listos para prueba según UI de coordinación. `@sergiourcullo` no conectado y `META_IG_ACCESS_TOKEN` para `graph.instagram.com` todavía no guardada. Ruta y permisos objetivo en [accesos](accesos.md#instagram-operativo-y-continuidad-de-autenticación). Los 62 casos con mocks y diez reinicios no prueban API real, publicación, DMs ni Advanced Access. |
| Investigación | Diez fichas de referentes, incluida Víctor Heras, y síntesis de funcionamiento de redes con fuentes primarias. Textos públicos y muestras parciales de Hormozi/Erik; vídeo candidato de Víctor sin reproducción comprobada. No auditoría interna ni visionado integral. [Índice](investigacion/2026-11-04/README.md). |
| Producción editorial | [Paquete semanal cloud](https://chatgpt.com/space/page_0722a12b4a988191b8835391a4bed17a): 35 IDs del 5–11 nov, 28 guiones y siete plantillas de diario, más YouTube 6–8 min. v1.2 releída en la página, secuencia 5; JSON/ZIP disponibles, mismos 35 IDs. Organización sincroniza los primeros cinco; ajuste de tomas P3 solicitado, no acreditado. Guiones disponibles, no grabados/programados. |
| Oferta | Recomendación, no elección aprobada: «Tu primer sistema personal con IA: organizá tu semana y delegá una tarea», Bs 50/55 min propuestos, DM PLAN. [Propuesta vigente para revisión](https://chatgpt.com/space/page_0722a12b4a988191b8835391a4bed17a). Taller de guiones queda histórico; sin dos ofertas activas, fecha/preventa/cobros autorizados. |
| Producto | Lectura de onia-platform a0488f0 e instrucciones; no ejecutar código, migraciones, cobros o despliegues por esta consolidación. |
| Panel | [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) releído: home único y 35 tarjetas Por grabar, cinco/día; diario 20:00 America/La_Paz. Nada programado/publicado, histórico detrás de Más. [Propuesta de perfil](https://chatgpt.com/space/page_175b3d0f70e88191992265d5515a3413): coordinación confirmó bio y enlace WhatsApp visibles en una navegación cloud; login wall bloqueó feed/fijados, cero piezas vistas y YouTube sin identificar. Página viva en corrección con ese alcance. |
| Continuidad | Dos chats recuperaron/actualizaron una entrada sintética desde Space sin recibir valores en el prompt. Desarrollo también recuperó biblioteca, catálogo ampliado y fuentes públicas desde cloud. Esto no sincroniza archivos o revisiones Git automáticamente. |
| Navegador | Bootstrap versionado aceptado en **2b1f9ab**: dos procesos crearon bases NSS distintas con la CA real verificada; ambos HTTP 200, título/captura inspeccionados, Play hasta 4,46 s y limpieza de ambos perfiles. TLS/proxy activos. Ocho tests Node y diez tests harness aprobados en Linux; doctor sin errores. Audio no escuchado, login persistente no probado. [Operación cloud](cloud/OPERAR.md). |

## Versiones y accesos

`N8N_API_KEY` y `META_ADS_ACCESS_TOKEN` están configuradas en secretos de red del entorno; la primera obtuvo lectura 200 y la segunda está vencida según Editor. `META_IG_ACCESS_TOKEN` para `graph.instagram.com` todavía no está guardada: requiere autorización de Sergio en OnIA Social API y publicación posterior de onia; Ads conserva `graph.facebook.com`. No pedir valores ni duplicarlos. [Inventario y renovación](accesos.md).

- VM Desarrollo: versión de entorno **6aeaa015725c81a3b2c5e7817fca85a6**; nació antes de cargar Meta. Su checkout avanzó de 9972d26 a **2b1f9ab** para aceptar el arreglo del navegador.
- Meta se comprobó en editor posterior **6aeaa134fa1881a3abd0f72ea0bd00f4**.
- El checkout de coordinación estaba en **ec62c9e** antes de esta consolidación. El commit de entrega se consulta en Git; un push no actualiza una VM existente.
- Editor preparado en **2b1f9ab**, borrador revisión 2: install/start, doctor, 28 pruebas Python, ocho NSS y una de navegador aprobados. La interfaz confirmó **«Entorno publicado»** y **«Publicado · Probar»** el 4 de noviembre, tras guardar y publicar la preparación.
- Versión publicada **6aeb5d2767cc81a3aee4674cf6485f5d**: coordinación informó hoy desde Editor **running/connected**, directorio /workspace/onia y checkout **6ca7762**; n8n listado 200 y Meta 401 por expiración. Esta edición documental no repitió APIs ni cambió configuración. El runtime antiguo de Desarrollo sigue siendo una instancia distinta.
- Checkout de esta edición en Desarrollo: **6ca77625234bcec4a9c6b6e5ece8a6f7a6852afa**, actualizado por fast-forward sin cambios previos. Hechos de Editor recibidos por coordinación; no atribuirlos como pruebas ejecutadas de nuevo aquí.
- El catálogo oficial actual muestra entorno **onia** listo y ejecutable, repo asociado y rama master. Usar versión actual para nuevos encargos que dependan de sus secretos.

## Entrega vigente

[Cierre fechado del 4 de noviembre](EVIDENCIA-2026-11-04.md#entrega-de-cierre-semana-formatos-y-flujo-privado): fuentes y revisiones leídas, paquete semanal cloud, home, formatos y DRY_RUN; qué puede usar Sergio y qué bloquea salidas autónomas. Repo mantiene índice/estado; cloud conserva artefactos versionados y Notion la vista diaria.

## Próximo resultado concreto

1. Retomar en onia publicado el análisis de una fuente pública concreta de Hormozi y otra de Iman, con cobertura audiovisual explícita y fichas existentes. GitHub y Desarrollo ya leyeron 2b1f9ab; cargar sólo contexto del encargo. No instalar servicios en el VPS.
2. Usar el home y el paquete semanal cloud para revisar/grabar el primer lote; completar sincronización de los cinco primeros y ajuste de tomas P3, reemplazar huecos de formatos con material real y medir tiempos. Ensayar demo y propuesta antes de vender; no asumir oferta elegida.
3. Sergio completa OnIA Social API → 2 Generar tokens → Agregar cuenta, guarda la entrada IG para graph.instagram.com y publica onia; después el ejecutor valida lectura cloud, cuenta, permisos y vencimiento. El navegador público y ads_read no acreditan publicación/mensajería. [Pasos y fuentes](accesos.md#instagram-operativo-y-continuidad-de-autenticación).

## Mapa de pendientes y responsables

| Pendiente | Solución y próxima acción | Responsable / condición |
|---|---|---|
| Autenticación IG | Autorizar Instagram Login en OnIA Social API y guardar entrada IG para graph.instagram.com; publicar onia y validar lectura después según accesos.md. | Sergio para autorización personal; ejecutor para comprobación posterior. Sin publicación ni DMs mientras tanto. |
| Autenticación de producción | Evaluar Unified Login antes de producción y compatibilidad de credenciales con producto/login/host; el piloto usa Instagram Login existente. Registrar vencimiento y acceso a datos tras autorizar. | Ejecutor revisa la ruta, sin cambiar redirects ni n8n ahora; Sergio autoriza personalmente. Renovación automática y aviso con scheduler no comprobados. [Detalle](accesos.md#instagram-operativo-y-continuidad-de-autenticación). |
| Meta Ads vencido | Conservar su entrada y renovar por la ruta oficial cuando se retome Ads; registrar vencimiento y nueva lectura. | Sergio para renovación personal; ejecutor para validación. |
| Resultado n8n | Resolver claim atómico y verificador seguro SHA256 antes de salidas reales; especificación SQL de 30 líneas disponible en la misma evidencia, no aplicada ni verificada en PostgreSQL. | Automatizaciones continúa lo autorizado; Sergio completa sólo acceso personal IG pendiente. Ensayo DRY_RUN no es chatbot comercial. |
| Investigación Víctor Heras y redes | Fichas incorporadas con fuentes, límites y plan propuesto; preparar demo y ensayo sin adoptar promesas comerciales. | Escritor Git consolida la entrega; marketing/video continúan preparación autorizada. |
| Producción real | Ejecutar seis piezas y medir con clips autorizados; avanzar preparación independiente dentro del encargo. | Sergio aporta material personal; área de video ejecuta lo disponible. |
| Entrega documental | Cierre fechado con enlaces a paquetes cloud y límites, sin copiar guiones/JSON ni datos privados. | Escritor Git único publica sólo ESTADO y registro del día; las versiones creativas se recuperan por sus enlaces estables. |

Los seis chats existentes están en [SESIONES.md](SESIONES.md). Notion contiene lo cotidiano; [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md) define fuentes y responsable.

## Pendientes que siguen abiertos

No hay scheduler diario, publicación Instagram, chatbot real, disparador n8n→Codex ni resúmenes de voz activados. El calendario preparado sigue sin eventos creados; requiere aprobación del conjunto concreto previamente presentado. No se llama ventas a interés ni dinero cobrado a un escenario aritmético.

No exportar privado/ u operacion/ a Git. Los artefactos y datos personales quedan en sus almacenes; el repo conserva decisiones, documentación útil y evidencia saneada. Fuentes técnicas: [pruebas de Instagram](https://chatgpt.com/space/page_afe5a3b4a224819182d708206cb6f15d), [accesos cloud](https://chatgpt.com/space/page_2b9ade6c69bc8191a7de31805f2cdabb), [evidencia histórica](EVIDENCIA-2026-11-03.md).

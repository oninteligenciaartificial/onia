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
| n8n | GET 200 en preparación y sesión nueva; diez flujos en página, siete activos y más páginas. Sólo lectura; no ejecución de workflow acreditada. |
| Meta Ads | GET 200 en editor publicado: dos cuentas, estado 1, USD. Sin campañas modificadas; la VM antigua de Desarrollo no recibió ese secreto. |
| Higgsfield/Google | Perfil y créditos Higgsfield observados, sin generación. Gmail perfil sin leer correo. Calendar consultado sin eventos creados. Drive con carpeta ONIA; transferencia de medios reales entre VMs pendiente. |
| Video | HyperFrames 0.9.10 produjo MP4 sintético de 6 s, H.264, 1080×1920, 30fps, sin audio, decodificado e inspeccionado. No demuestra edición comercial ni pipeline de clips reales. |
| Instagram | Adaptadores HTTP cloud: **62 pruebas con mocks y diez reinicios en la misma VM**. Se corrigieron conflicto de aprobación, atomicidad de STOP/HUMAN y entradas JSON inválidas. No prueba API Meta real, workflow n8n, concurrencia o persistencia entre VMs. |
| Investigación | Nueve fichas de referentes y fuentes; textos públicos y muestras parciales de tres lecciones de Hormozi y una pieza de Erik. No auditoría interna ni visionado integral. [Índice](investigacion/2026-11-04/README.md). |
| Producción editorial | Catálogo de 16 recetas y brief de seis piezas. Objetivo: cinco videos diarios, con diario real último a las 20:00. Escenario 25 por tandas + 7 diarios + 3 extras por semana; capacidad y tiempos aún sin medir. |
| Oferta | Workshop y demo textual preparados como propuesta; sin ensayo audiovisual, anuncio, compradores ni cobros verificados. Ver ficha única en el índice. |
| Producto | Lectura de onia-platform a0488f0 e instrucciones; no ejecutar código, migraciones, cobros o despliegues por esta consolidación. |
| Panel | [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) existe y fue revalidado por conector: vida, contenido, ventas, actualidad y decisiones. Informes técnicos archivados fuera de portada. Apariencia móvil y notificaciones no verificadas. |
| Continuidad | Dos chats recuperaron/actualizaron una entrada sintética desde Space sin recibir valores en el prompt. Desarrollo también recuperó biblioteca, catálogo ampliado y fuentes públicas desde cloud. Esto no sincroniza archivos o revisiones Git automáticamente. |
| Navegador | Corregido en Desarrollo: base NSS original de sólo lectura. Base temporal escribible con la misma CA oficial verificada y TLS activo: HTTP 200, título/captura y reproducción pública hasta 4,67 s. Audio no escuchado. Bootstrap en integración y prueba desde repo; [operación cloud](cloud/OPERAR.md). No acredita login persistente o acceso universal. |

## Versiones y accesos

N8N_API_KEY y META_ADS_ACCESS_TOKEN están en secretos de red del entorno, limitados a sus dominios. No pedir sus valores ni duplicarlas. [Inventario](accesos.md).

- VM Desarrollo inspeccionada: HEAD **9972d26**, versión de entorno **6aeaa015725c81a3b2c5e7817fca85a6**; nació antes de cargar Meta.
- Meta se comprobó en editor posterior **6aeaa134fa1881a3abd0f72ea0bd00f4**.
- El checkout de coordinación estaba en **ec62c9e** antes de esta consolidación. El commit de entrega se consulta en Git; un push no actualiza una VM existente.
- El catálogo oficial actual muestra entorno **onia** listo y ejecutable, repo asociado y rama master. Usar versión actual para nuevos encargos que dependan de sus secretos.

## Próximo resultado concreto

1. Reproducir desde el bootstrap versionado la corrección del navegador ya probada en VM, con directorio de confianza nuevo, TLS activo y evidencia de página/interacción/captura. [OPERAR.md](cloud/OPERAR.md). Sin servicios nuevos en el VPS del producto.
2. Publicar esta consolidación y comprobar que un ejecutor cloud lee el commit y las fuentes pertinentes; no cargar toda la biblioteca en cada tarea.
3. Ejecutar el [lote de seis piezas](investigacion/2026-11-04/formatos-onia.md) con material real y medir tiempo humano, render y revisiones. Ensayar la demo antes de ofrecer el taller.

Los seis chats existentes están en [SESIONES.md](SESIONES.md). Notion contiene lo cotidiano; [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md) define fuentes y responsable.

## Pendientes que siguen abiertos

No hay scheduler diario, publicación Instagram, chatbot real, disparador n8n→Codex ni resúmenes de voz activados. El calendario preparado sigue sin eventos creados; requiere aprobación del conjunto concreto previamente presentado. No se llama ventas a interés ni dinero cobrado a un escenario aritmético.

No exportar privado/ u operacion/ a Git. Los artefactos y datos personales quedan en sus almacenes; el repo conserva decisiones, documentación útil y evidencia saneada. Fuentes técnicas: [pruebas de Instagram](https://chatgpt.com/space/page_afe5a3b4a224819182d708206cb6f15d), [accesos cloud](https://chatgpt.com/space/page_2b9ade6c69bc8191a7de31805f2cdabb), [evidencia histórica](EVIDENCIA-2026-11-03.md).

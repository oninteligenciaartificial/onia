**Base operativa de Sergio y ONIA — versión inicial, 3 de noviembre de 2026**

**Alcance vigente:** repo privado del harness desde esta carpeta, entorno limpio `onia` creado por Sergio. La prueba anterior en ONIA Platform fue detenida; no se adopta ese entorno. La preparación reproducible se describe en el README de la raíz. Las notas de pruebas anteriores son históricas; los archivos de `operacion/` y `privado/` permanecen locales y no viajan con el repo.

**Nueva referencia leída:** [carrusel de 42 herramientas](revision-carrusel-DfQnRTcjCXU.md). Se leyeron sus siete imágenes; contiene inventario y encaje propuesto, sin instalar el catálogo ni dar por comprobadas sus integraciones.

**Entrada vigente:** [ESTADO.md](ESTADO.md). La base local ya tiene entrada AGENTS.md, siete skills enlazadas para descubrimiento, registro ejecutable de tareas y una prueba MP4 de HyperFrames. Consultar [comprobación local](operacion/evidencias/base-local.md) y [prueba de video](operacion/evidencias/video-local.md). La nube, la instancia n8n y la continuidad en otro chat siguen sin verificar.

**Corrección expresa de Sergio, 3-nov-2026:** no usar el repositorio ONIA-CENTRAL como referencia. Fue incorrecto adoptarlo como fuente de reglas y skills en esta conversación. La autoridad para el nuevo diseño son las instrucciones vigentes de Sergio aquí; `oninteligenciaartificial/onia-platform` conserva el código del producto. Esta carpeta registra el diseño de esta conversación y las fuentes externas revisadas; todavía no define un repositorio nuevo. La propuesta preparada anteriormente dentro de ONIA-CENTRAL no está adoptada, integrada ni distribuida y no debe retomarse como base. No importar sus reglas, decisiones históricas, skills o permisos. Ver [corrección de procedencia](correccion-procedencia.md).

La decisión vigente es usar Codex como ejecutor principal mientras Grok Bot Premium está sin cuota. n8n, Docker, Supabase y ONIA ya funcionan en el VPS según Sergio. Esta base organiza la arquitectura, el contexto y los procedimientos antes de modificar esa instalación.

| Documento o carpeta | Propósito | Estado |
|---|---|---|
| [Registro de errores y corrección](registro-de-errores.md) | Desviaciones del encargo, requisitos que deben conservarse y corrección operativa. | Registrado a pedido de Sergio; eficacia pendiente de comprobar con trabajo real. |
| [Reglas comunes](reglas-comunes.md) | Primera base redactada desde esta conversación. | Preparada; no distribuida a otros entornos. |
| [Primer recorrido comercial](recorrido-comercial-inicial.md) | Oferta, funnel, taller/webinar, contenido y cobros hacia la meta del 14. | Preparación; falta seleccionar resultado demostrable de la oferta. |
| [Contexto privado](privado/contexto.md) | Hechos de Sergio y la empresa, compromisos y decisiones vigentes. | Redactado con el relato del usuario; cada sistema conserva su nivel de verificación. |
| [Arquitectura](arquitectura.md) | Distribución de funciones entre Codex, n8n, VPS, datos y Grok Bot futuro. | Propuesta para cotejar con repositorio y servidor. |
| [Accesos y credenciales](accesos.md) | Dónde introducir secretos y cómo registrar los permisos sin copiar sus valores. | Procedimiento documentado; ninguna credencial fue cargada. |
| [Skills compartibles](compartibles/skills/) | Evaluación, continuidad, oferta/embudo, desarrollo, video, n8n y mejora del sistema. | Siete skills propias enlazadas localmente; alcance de pruebas por capacidad en la comprobación local. |
| [Fuentes y decisiones de diseño](fuentes.md) | Repositorios leídos y origen de los patrones usados. | Fuentes públicas y documentación de proveedores. |
| [Revisión de ONIA Platform](revision-onia-platform.md) | Identidad del repositorio, contexto existente, skills y circuito QR. | `master` confirmado; lectura de código y documentación, sin validación productiva. |

Esta carpeta es la base local dentro del espacio de trabajo. No es un nuevo repositorio ni una instalación en el VPS. Las skills de `compartibles/skills` están enlazadas en `.agents/skills` del proyecto C:/dev/proyectos; no están instaladas globalmente ni publicadas. Llevarlas al entorno de nube requiere preparar allí los archivos y comprobar una tarea real. La carpeta `privado`, los registros de `operacion` y este índice no forman parte del paquete para clientes.

Las tres primeras skills se ampliaron con desarrollar-y-verificar, producir-video, automatizar-n8n y mejorar-sistema. La skill de oferta cubre talleres/webinars y el recorrido de venta, todavía sin ejecución comercial. Las skills no incluyen datos personales de Sergio y no se instalaron globalmente. La comprobación estructural no demuestra por sí sola su eficacia; las pruebas ejecutadas están enlazadas arriba.

La consulta de entornos de esta cuenta encontró `ONIA Platform` y `ONIA Hermes` marcados como ejecutables. También encontró `ONIA Desarrollo` y `onia-hermes`, listos pero no ejecutables. La consulta verificó metadatos, no la salud del código ni de sus servicios. No se crearon entornos adicionales ni se inició una tarea cloud.

Se recibió el reel y se registraron los 30 nombres de su descripción. La [auditoría de los 30 repositorios](auditoria-30-repos.md) amplía la revisión parcial anterior: contiene decisiones por candidato, fuentes fijadas, límites de lectura y el complemento n8n. El [registro estructurado](catalogo-repos-2026-11-03.json) conserva la evidencia de selección; [selección y recorrido](seleccion-y-recorrido.md) define las capacidades propias, chats, aprendizaje y orden comercial de implementación. Son documentos de preparación, no paquetes instalados. La revisión de ONIA encontró Impeccable ya versionado: se evaluará esa copia antes de cualquier instalación. La descripción y una imagen del reel no equivalen a verificar todo su audio y contenido audiovisual.

La captura de Sergio identificó `oninteligenciaartificial/onia-platform`. Se confirmó acceso privado, `master` en `a0488f04200b14c95caf0013043716b16efa1f1d` y correspondencia con el entorno cloud `ONIA Platform`. La carpeta local está en otra rama con trabajo pendiente; la revisión usó la referencia de `master` sin cambiarla. El [diagnóstico](revision-onia-platform.md) registra contexto obsoleto, skills existentes y QR BCP implementado cuya operación real falta verificar.

El [informe de investigación anterior](../investigacion-harness-2026-11-03.md) conserva las alternativas estudiadas. Las decisiones vigentes y la actualización sobre los servicios ya instalados están en esta base operativa.

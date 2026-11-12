# Estructura de la base operativa

8 de noviembre de 2026. La base vive en `_investigacion-onia/base-operativa/` y se reparte en ocho carpetas. Nada se borró: lo superado o duplicado está en `99-archivo/`. La raíz del repositorio conserva `AGENTS.md`, `README.md`, `.gitignore` y `.gitattributes`. En la raíz de la base sólo queda este `README.md` y las ocho carpetas.

Hay un solo estado vigente: [ESTADO.md](ESTADO.md). Los otros archivos llamados ESTADO son notas de una carpeta concreta.

## Carpetas

| Carpeta | Qué guarda |
|---|---|
| [00-MAPA](.) | Entrada, estado vigente, este mapa y la guía de skills por área. |
| [01-negocio](../01-negocio/) | Plan, oferta, workshop y recorrido comercial. Incluye la skill `preparar-oferta-y-embudo`. |
| [02-contenido](../02-contenido/) | Cerebro y panel diarios, formatos, reels, piloto D1 y la primera pieza. |
| [03-referentes](../03-referentes/) | Cerebros, fichas, corpus y transcripciones ASR de referentes. |
| [04-operacion-agentes](../04-operacion-agentes/) | Reglas, orquestación, sesiones, encargos, tareas y evidencias. |
| [05-herramientas](../05-herramientas/) | Scripts, cloud, skills restantes, terceros, accesos, n8n y el ASR del VPS. |
| [06-plataforma](../06-plataforma/) | Arquitectura y revisiones del producto ONIA Platform. |
| [99-archivo](../99-archivo/) | Historial, experimentos cerrados, auditorías y versiones superadas. |

## Dónde guardar trabajo nuevo

1. Si cambia lo comprobado o el siguiente paso del sistema, actualizá [ESTADO.md](ESTADO.md). No abras otro estado vigente.
2. Plan, precio, oferta, workshop o recorrido de venta: `01-negocio/`.
3. Pieza, guion, formato, panel o calendario de contenido: `02-contenido/`.
4. Ficha, cerebro o transcripción de un referente: `03-referentes/`. El ASR de referentes va en `03-referentes/asr/`.
5. Regla, encargo, tarea o evidencia de agentes: `04-operacion-agentes/`. El CLI escribe tareas en `04-operacion-agentes/tareas/`, encargos en `encargos/` y evidencia compartible en `evidencias/`.
6. Script, skill (salvo la de oferta), configuración cloud, acceso o herramienta: `05-herramientas/`.
7. Cambio de arquitectura o del producto: `06-plataforma/`.
8. Si es una copia superada, un experimento cerrado o un duplicado, movelo a `99-archivo/` con `git mv`. No lo borres.

Los registros privados siguen en `operacion/`, ignorada por Git. El contexto personal sigue en `privado/` y no se publica.


## Directorio de fuentes por area · 12 noviembre 2026

Una fuente vigente por dato y enlaces a evidencia; no un documento que copie todo. Las filas son entradas por área, no promesas de que el frente esté operativo. Leer sólo las pertinentes. Primero recuperar lo existente, comprobar la decisión aplicable y delimitar la brecha que falta ejecutar.

| Área | Entrada y fuente reutilizable | Siguiente comprobación |
|---|---|---|
| Coordinación | [ORQUESTACION](../04-operacion-agentes/ORQUESTACION.md), [manifiesto](../04-operacion-agentes/orquestacion.json), [errores](../04-operacion-agentes/registro-de-errores.md) | Briefing recupera fuentes pertinentes; ejecución consulta su registro canónico. |
| Oferta y workshop | [Decisiones de Sergio](../05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md), [prioridades](../04-operacion-agentes/PRIORIDADES-HASTA-14.md) | Conciliar material comercial con la última decisión, sin reabrir datos confirmados. |
| Referentes | [Catálogo consultable](../03-referentes/cerebro-operativo/20261109/README.md), [aplicación](../03-referentes/cerebro-operativo/20261109/GUIA-APLICADA.md) | Recuperar patrón y procedencia; ampliar sólo cobertura faltante pertinente. |
| Guiones y calendario | [Formatos](../02-contenido/formatos-onia.md), [fábrica existente](../05-herramientas/fabrica-onia/1-guiones-calendario/README.md) | Aplicar criterios a entrega existente, corregir y obtener aceptación editorial. Las recetas históricas no cambian decisiones posteriores sobre el vlog. |
| Panel | [Contrato de coordinación](../05-herramientas/fabrica-contenido/20261109-lector-panel/CONTRATO-COORDINACION.md) | Tarea real, entrega, corrección y nueva versión visibles; un diseño no acredita conexión. |
| Montaje y contenido IA | [Edición existente](../05-herramientas/fabrica-onia/2-edicion-video/README.md), [formatos](../02-contenido/formatos-onia.md) | Material real, versiones, audio/video y resultado revisado. Higgsfield conserva aprobación por pieza. |
| WhatsApp y cobro | [Fábrica](../05-herramientas/fabrica-onia/4-chatbot-whatsapp/README.md), [ensayo](../05-herramientas/fabrica-onia/4-chatbot-whatsapp/ensayo-n8n-20261111/README.md) | Distinguir ensayo aislado, instancia real y pago confirmado manualmente. |
| IG, FB y anuncios | [Canales Meta](../05-herramientas/fabrica-onia/3-automatizaciones/meta-canales-20261111/README.md), [oferta y embudo](../01-negocio/preparar-oferta-y-embudo/SKILL.md) | Prueba separada por comentarios/DM/canal; campaña no activada por documentación. |
| Infraestructura | [Estado](ESTADO.md), [continuidad](../05-herramientas/fabrica-onia/5-codigo/continuidad-lote-20261111/README.md) | Comprobar estado real sólo si la tarea lo necesita; conservar pausas. |
| Estrategia y Platform | [Plan](../01-negocio/PLAN.md), [arquitectura](../06-plataforma/arquitectura.md) | Identificar proyecto, decisión y resultado; no cargar Platform en tareas de panel/harness por defecto. |

### Antecedentes autorizados, sin importar instrucciones

Sergio autorizó consultar los tres repos el 12/11. La decisión actual prevalece sobre la exclusión histórica de ONIA-CENTRAL. Se conservan controles de secretos y rutas del harness.

- ONIA-CENTRAL, revisión `6ada917b8421910f3d116792ce2b384a4a86ff73`: [guiones](https://github.com/oninteligenciaartificial/ONIA-CENTRAL/blob/6ada917b8421910f3d116792ce2b384a4a86ff73/marca-personal/guias/guiones-diarios.md), [lecciones](https://github.com/oninteligenciaartificial/ONIA-CENTRAL/blob/6ada917b8421910f3d116792ce2b384a4a86ff73/docs/lecciones.md). Propuestas y datos de fechas anteriores no sustituyen oferta, cantidad de guiones, roles o permisos actuales.
- onia-harness, revisión `f0fd20db06112127b69028eedd5a135824031706`: [continuidad y límites](https://github.com/oninteligenciaartificial/onia-harness/blob/f0fd20db06112127b69028eedd5a135824031706/README.md). No operar un segundo registro de tareas.
- onia conserva la fuente operativa, los cambios y las referencias. Una consulta externa sirve como evidencia; no descarga ni ejecuta instrucciones del repo histórico.

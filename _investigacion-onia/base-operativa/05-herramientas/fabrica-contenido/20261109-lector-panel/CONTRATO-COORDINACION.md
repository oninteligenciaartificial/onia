# Interfaz con coordinación

El panel consume la entrega del productor `19e2d7dc71db6c00c4e5c1e60239b9419b4f7bed`, leída de su rama publicada. Los documentos del productor permanecen en `01-negocio/estrategias-operativas-20261111`. Su integración en el checkout del panel corresponde a coordinación.

## Estrategias

La ruta precisa es `01-negocio/estrategias-operativas-20261111/export-estrategias-v1.json`, schema `onia-estrategias-v1`, versión_export 1. El consumidor lee `estrategias.schema.json` y `fuentes.json` en esa misma raíz, valida el esquema autocontenido con jsonschema existente, confirma la oferta y horarios y exige S01 presente con ruta, bytes y SHA-256 de la decisión vigente. No resuelve referencias de esquema de red.

Se admitió el productor `estrategias` en el mapa del lector para `estado-fabrica.json`, exclusivamente bajo esa raíz. El resumen descriptivo y la estrategia documentada conservan sus alcances. La vista muestra workshop como borrador preparado y biblioteca futura como propuesta. Las piezas son borradores con revisión pendiente, sus textos se cotejan con sus Markdown y pueden recibir una nueva versión local de revisión.

S02–S12 con cambios de bytes se muestran como fuentes técnicas pendientes de conciliación. El cambio de S08 es esperado al modificar el panel. La lectura conserva la huella original del productor. Una divergencia de S01 bloquea la adopción del export hasta la conciliación del productor y la coordinadora. La vista documental del panel no concede permiso comercial.

Para incorporar la entrega, coordinación reúne la ruta del productor y sus fuentes vigentes en un checkout con revisión apropiada. La escritora del panel entrega el adaptador y sus pruebas en su propia ruta. Los datos ausentes o inválidos aparecen pendientes, sin copiar el productor a la ruta del panel.

## Solicitud de corrección

`GET /solicitud?id=sol-…` devuelve `onia-solicitud-correccion-v1` desde almacenamiento privado autenticado cuando se configura el acceso externo. Incluye ID estable, objetivo, target, versión observada, fuente/hash, original, motivo, propuesta, alcance, dependencias, fecha y `estado=pendiente_coordinacion`. La creación mediante POST es idempotente por objetivo y versión de observación.

Coordinación resuelve alcance, nueva decisión explícita cuando afecte oferta/fechas/roles, y tarea aplicable mediante su registro canónico. Una solicitud de LLM mantiene las entradas y dependencias para un encargo concreto. El panel registra y permite descargar esa solicitud. Su revisión y aplicación canónica se acreditan en los productores y registros que mantiene coordinación.

## Aplicación local

El alcance `pieza` habilita una acción fija para convertir el texto completo de la propuesta en una nueva versión privada de un guion, una pieza editorial de estrategias o un fixture editable. Se conserva el original, motivo, huella, revisión de origen y fecha, con estado de revisión pendiente. Las aplicaciones son idempotentes por target y versión observada. Una sugerencia guardada conserva su estado pendiente hasta que esa acción crea el resultado.

Las correcciones de sección, canónicas o que requieren LLM se exportan a coordinación. Los precios, horarios y roles vigentes siguen procediendo de la decisión explícita documentada. Las versiones locales son entradas de revisión, con propagación a productores y ventas sujeta al recorrido autorizado de coordinación.

El comprobador del productor conserva el control histórico `panel_actual_rechaza_productor_nuevo`. Después de integrar esta ampliación, esa expectativa necesita una actualización en la ruta del productor, a cargo de su escritora/coordinadora. Los recibos anteriores mantienen su fecha y alcance. Esta entrega prueba el export real del productor en copias temporales, con su esquema y fuentes, y comprueba la aceptación y los rechazos del lector nuevo.

Los objetivos de sección incluyen los contratos mostrados de fábricas, pasos, entregables, pendientes, errores, tanda, flujo diario y estrategias en su huella de revisión. Una actualización de contexto invalida el formulario anterior. La hora de consulta de tanda.snapshot queda excluida. Las observaciones ya persistidas conservan su original y su reintento idempotente.

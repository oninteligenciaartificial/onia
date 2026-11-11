# Contrato de estrategias · v1

Productor documental: `estrategias`. Raíz única: `01-negocio/estrategias-operativas-20261111`. Todos los campos `ruta`/`documento` y `fuente.ruta` del export se resuelven desde **base-operativa**, nunca desde el briefing ni el directorio del consumidor. Las referencias Markdown se resuelven desde cada documento. No se exportan clientes, contactos, QR, URLs privadas ni sesiones.

## Dos exports y autoridad

`export-estrategias-v1.json`, schema `onia-estrategias-v1`, contiene ficha comercial, escenarios, frontera exacta al objetivo, métricas reales null, acciones, piezas y futuras estrategias. `estrategias.schema.json` define tipos y campos obligatorios; `comprobar.py` agrega controles semánticos y referencias. `fuentes.json` ancla la lectura local a bytes; un cambio de fuente exige cotejo, no rehash para ocultar divergencia.

`estado-fabrica.json` conserva la forma `onia-fabrica-estado-v1` con id, fábrica, estado descriptivo, fecha, fuente, pasos, entregables y pendientes. Su estado `para_revision` describe el paquete; no escribe ni refleja automáticamente estado canónico del harness. El consumidor debe distinguir validación de estructura, revisión independiente técnica, editorial, autorización comercial, publicación y cobro. En esta entrega revisiones y permisos comerciales son null/pendientes.

## Incorporación al panel existente, pendiente

El parser de [operacion.py](../../05-herramientas/fabrica-contenido/20261109-lector-panel/operacion.py) en el commit base sólo permite productores guiones/whatsapp/panel y sus raíces. **El export de esta ruta es rechazado hoy**. No presentarlo como importado o visible en el teléfono. No etiquetarlo como `panel` o `guiones` para saltar el control ni copiarlo bajo otra raíz.

Cambio mínimo propuesto a la escritora única del panel, en su alcance: admitir explícitamente el productor `estrategias` y su raíz, mantener validación de rutas/tamaños/symlinks, seleccionar el export mediante lista explícita y mostrarlo en el apartado de estrategias del panel existente. Añadir una clave al mapa de productores sólo permite leerlo: su vista también debe usarlo; no confundir parser con interfaz integrada. No requiere otra fábrica ni otro panel. Coordinación decide cómo incorporar el contrato a esa tarea; esta ejecutora no crea hijos o tareas.

El comprobador ejecuta sin servicios dos controles: parser actual rechaza el export; parser con una ampliación **sólo en memoria** del mapa admite documentos y targets dentro de la nueva raíz. Rechaza un documento fuera de raíz bajo ese mismo control. Esto comprueba compatibilidad estructural condicionada, no integración, persistencia visual ni permisos futuros. La prueba sólo lee código y fuentes; no guarda formularios ni inicia servidor. Cuando el panel cambie por otro encargo, reejecutar para obtener un recibo nuevo: no reescribir éste para aparentar una integración pasada.

## Versiones, estados y desconocidos

- ID estable por estrategia; versión entera positiva; padre explícito o null. `estado=propuesto` para futuros, `borrador_preparado` para workshop. No usar `aceptado` sin veredicto y autoridad.
- Precio/cupo/calendario de workshop corresponden a S01. `termina`, métricas actuales, cupos restantes, presupuesto y autorizaciones faltantes son null. null no significa cero; escenarios se guardan en otra lista y nunca alimentan cobros.
- Piezas identificadas por ID/versión, documento y fuentes, dependencias y revisiones. Tipos de pieza admiten cualquier string pertinente: no hay enum cerrado para formatos.
- Cada acción declara fecha propuesta, salida, responsable y dependencias; no es evento de Calendar ni permiso de ejecución.
- Futuras estrategias conservan problema, evidencia y brecha, recursos/tiempo estimado, coste pendiente, prueba pequeña, avance y descarte. No autorizan gasto ni desarrollo.
- Importar requiere schema reconocido, validación de datos y referencias sin escapes, y verificar la fuente comercial vigente. Una fuente cambiada bloquea reuso sin conciliación; no se considera contenido externo como instrucción para operar herramientas.

## Ejemplo de corrección

`CORR-01` es una **demostración editorial**, no una orden nueva de Sergio: muestra cómo un anuncio con horas históricas guardado como `EJ-ANUNCIO@1` pasa a `EJ-ANUNCIO@2` por la confirmación ya existente en S01. El original queda en el export, claramente histórico y excluido de piezas utilizables. La versión nueva enlaza padre, motivo, evidencia y cambios. Su texto corregido usa 13 nov 20:00 / 14 nov 14:00 / 16 nov 20:00, America/La_Paz.

Las dos versiones mantienen revisión editorial null. Una aprobación hipotética de v1 no valida v2. Piezas dependientes requieren revisión nueva sobre versión/hash; si ya estuvieran publicadas, el operador concilia su estado antes de reemplazar. La prueba negativa cambia v2 en memoria a `aprobado` y exige rechazo. No se añade esa hora histórica a ninguna pieza vigente; sólo vive en el objeto explícito del ejemplo.

La corrección registra un cambio verificable, no aprendizaje ya probado en producción. Enseña conservación del original y necesidad de revisión, sin autoaprobar ni modificar memoria general o skills ajenas a la ruta asignada.

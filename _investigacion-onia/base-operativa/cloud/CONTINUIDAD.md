# Continuidad de tareas ONIA

Contrato del CLI existente, schema 2. [ORQUESTACION](../ORQUESTACION.md) define selección y responsables; [ESTADO](../ESTADO.md) distingue implementación, publicación y prueba real.

## Un registro, dos alcances posibles

- Privado/local, predeterminado: `operacion/tareas/ID.json`, ignorado por Git.
- Compartible, elegido al crear con `--compartible`: `continuidad/tareas/ID.json`, versionable. No debe contener información privada.
- Nunca dos registros para el mismo ID: cualquier ambigüedad se rechaza conservando ambos para conciliación.
- El JSON conserva estado y contenido canónico del briefing. El Markdown en `encargos/ID.md` es una proyección comprobada por hash; no se edita como una segunda fuente.
- Las evidencias compartibles se guardan saneadas bajo `continuidad/evidencias/ID/`, con nueva ruta por versión. Los filtros de nombres/rutas no detectan todo secreto: revisar el contenido y el diff antes de publicarlo.
- `ESTADO.md` enlaza capacidades y resultados del sistema; no duplica el estado mutable de cada tarea.

## Flujo de trabajo

Desde la raíz del repo, preparar una tarea compartible:

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py preparar demo-001 --compartible --area desarrollo --objetivo "Comprobar datos ficticios" --entregable "Informe con evidencia" --aceptacion "Cálculo y límites revisados"
python3 _investigacion-onia/base-operativa/scripts/harness.py retomar demo-001
```

La primera revisión es 1. Tras crear el archivo de evidencia saneado, registrar la entrega (rutas de evidencia relativas a base-operativa):

```sh
python3 _investigacion-onia/base-operativa/scripts/trabajo.py actualizar demo-001 --revision-esperada 1 --estado para_revision --resultado "Informe preparado" --verificacion correcta --comprobacion "Cálculo cotejado" --evidencia continuidad/evidencias/demo-001/informe-v1.txt --siguiente "Revisar la entrega"
```

El comando devuelve revisión 2. El revisor debe comprobar el resultado antes de:

```sh
python3 _investigacion-onia/base-operativa/scripts/trabajo.py aceptar demo-001 --revision-esperada 2 --revisor "Responsable de revisión" --criterio "Resultado cotejado con el objetivo"
```

`aceptar` sólo admite `para_revision`, evidencia íntegra y verificación declarada correcta. Una comprobación fallida o pendiente impide marcar `para_revision` o aceptar. La herramienta no determina por sí sola si el revisor dice la verdad ni autentica su identidad.

Para registrar un bloqueo o continuar, retomar y usar su revisión actual con `en_espera` o `en_curso`. Omitir `--evidencia` conserva las referencias existentes. Añadir una nueva evidencia amplía el inventario; no elimina las anteriores. Para mejorar v1, crear `informe-v2.txt`, cotejarlo y registrarlo con revisión esperada: v1 y v2 deben seguir accesibles. No sobrescribir v1.

Al aceptar, `--siguiente` permite indicar un seguimiento autorizado. Si se omite, el registro deja el encargo cerrado sin iniciar otra ejecución. El paso previo de revisión queda en el historial, no como una orden pendiente que deba repetirse.

## Recuperación breve y detalle explícito

retomar devuelve por defecto estado vigente, revisión, objetivo, siguiente paso, comprobación, evidencia, aceptación y, si existen, decisiones vigentes, ficha de ejecución y asignación. El briefing íntegro aparece una sola vez en tarea.briefing.contenido, conservando sus restricciones. No se carga el historial operativo ni las decisiones sustituidas; la respuesta informa cuántos elementos omitió y cómo consultarlos.

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py retomar demo-001 --completo
python3 _investigacion-onia/base-operativa/scripts/harness.py historial demo-001 --revision 1
```

La vista completa recupera el JSON canónico íntegro; historial permite consultar una revisión o todas las entradas. Ambas verifican primero la evidencia vigente y no escriben nada. El historial no autoriza reactivar decisiones revocadas. Los registros v1 pueden carecer de números de revisión históricos.

Cambio intencional de forma: resume(base, id, complete=False) ahora es breve por defecto y harness elimina el alias duplicado briefing de la raíz. Los consumidores deben leer tarea.briefing.contenido; complete=True conserva el registro íntegro bajo tarea. preparar sigue devolviendo briefing como RUTA. La compatibilidad de datos v1/v2 no conserva automáticamente la forma anterior de salida.

## Decisiones y ficha de ejecución

decidir ID --revision-esperada N --decision CLAVE --texto TEXTO --fuente RUTA --autor AUTOR registra una decisión con procedencia, hash, fecha y autor declarado. --sustituye CLAVE_ANTERIOR reemplaza explícitamente una decisión vigente: conserva ambas y muestra sólo la nueva en la vista breve. La fuente debe ser un archivo independiente conservado, nunca el JSON canónico que cambiará al registrar la decisión. La herramienta comprueba integridad y estructura, no autoridad semántica.

Cambiar decisiones, ejecución o asignación de una entrega para_revision/aceptado requiere reabrir explícitamente con actualizar. No modifica silenciosamente una aceptación.

preparar admite --perfil extraccion, multifuente, cambio-acotado o complejo según orquestacion.json. Recomienda por tipo de trabajo, independientemente del área/skill; no configura ni lanza un LLM. Sin selección no se inventa una recomendación. ejecucion ID --revision-esperada N --ficha RUTA lee JSON con este contrato:

```json
{
  "recomendado": {"modelo": "gpt-6.1-sol", "esfuerzo": "medium"},
  "solicitado": {"modelo": "gpt-6.1-terra", "esfuerzo": "medium"},
  "observado": null,
  "criterio": "Cambio acotado con verificación definida",
  "escalamiento": "Comparar otro candidato ante un fallo de razonamiento identificado"
}
```

null expresa desconocido; nunca completar observado a partir de solicitado. Una observación requiere modelo, esfuerzo y fuente (ruta a evidencia saneada y conservada). El comando incorpora hash y tamaño, sin consultar el runtime. Cotejar la fuente con los metadatos reales antes de declararla observada. Tiempo y uso quedan en la evidencia del ensayo; no inventar tokens o precios no disponibles.

## Reserva local de rutas

asignar ID --revision-esperada N --responsable ACTOR --ruta RUTA (repetible) reserva rutas relativas a base-operativa. Rechaza solapamientos exactos o de directorio con otra tarea del mismo checkout, incluso diferencias de mayúsculas. Un lock de asignaciones serializa las reservas y la revisión esperada evita sustituir un registro obsoleto. La reserva persiste hasta liberar; aceptar no la libera automáticamente.

Mutaciones del ejecutor y recuperar exigen --actor coincidente si existe asignación. --reasignar exige actor anterior y revisión vigente; --liberar libera explícitamente, conservando historia. Liberar después de aceptar no altera resultado ni aceptación. aceptar rechaza al mismo responsable declarado como revisor. Son controles de coherencia de nombres, no autenticación.

No impide que un editor externo escriba esas rutas, no vigila todos los comandos ni coordina clones distintos. Antes de trabajar en otra copia, acordar revisión base, rutas y único integrador; conciliar resultados sin descartar ninguno.

## Traspaso entre sesiones

1. El escritor comprueba estado y evidencia. Revisa que los archivos de la tarea, su Markdown y sus evidencias estén incluidos en Git y saneados. `.gitattributes` conserva sus bytes.
2. Publica únicamente los cambios autorizados y entrega ID, repo y commit completo. Un commit local sin push no está disponible para otra VM.
3. La sesión receptora comprueba su HEAD y cambios; recupera ese commit sin descartar trabajo existente. No supone que el snapshot publicado ya lo incluye.
4. Ejecuta `harness.py retomar ID`, lee las fuentes indicadas y recupera objetivo, aceptación, evidencia y siguiente paso. No recibe el chat completo.
5. Registra su propio resultado dentro del mismo ID con revisión esperada y una nueva ruta de evidencia, o informa el bloqueo sin inventar recuperación.

Cada tarea Cloud tiene su workspace. Un lock y la revisión esperada evitan colisiones en un checkout; no son un bloqueo distribuido. Entre clones, Git debe rechazar un push no fast-forward. Antes de integrar hay que revisar el cambio remoto y reconciliar el mismo ID; no usar force-push ni resolver un conflicto JSON eligiendo todo un lado sin verificar su historial.

## Integridad, recuperación y compatibilidad

Retomar o mutar falla si falta o cambia evidencia vigente, si el briefing difiere, si el esquema/ID no coincide o si la ruta es privada, externa o enlazada. Restaurar los bytes originales de la revisión publicada; no actualizar hashes para ocultar corrupción.

El JSON se guarda con reemplazo atómico y fsync antes de materializar Markdown. Una interrupción puede dejar el JSON íntegro y la proyección ausente. Recuperarla así:

```sh
python3 _investigacion-onia/base-operativa/scripts/trabajo.py recuperar demo-001 --revision-esperada 1
```

Es idempotente y no cambia la revisión canónica. Sólo reconstruye una proyección ausente; si existe parcialmente escrita o alterada, conserva el archivo y bloquea. Tras verificar que no hay escritor activo, preservar esa copia fuera de su ruta, comprobar el JSON y recuperar la proyección ausente. No automatizar eliminación de locks ni archivos ambiguos.

Los registros schema 1 se leen sin convertirlos. Su historial puede contener hashes antiguos de una misma ruta; se conserva como historia y se comprueba la evidencia actual, no todos esos hashes contra un único archivo. Para editar, revisar la situación y ejecutar:

```sh
python3 _investigacion-onia/base-operativa/scripts/trabajo.py migrar ID --revision-esperada 0
```

La migración es explícita y no convierte un `terminado` histórico en aceptación: lo deja en espera para comprobarlo. Conserva historial y hashes; captura el briefing existente como base sólo tras esa revisión explícita. No exporta automáticamente datos locales al modo compartible.

## Límite de las pruebas

Tests locales, arranque Cloud, traspaso real A→B y uso del iPhone son comprobaciones diferentes. El [informe de consolidación](../continuidad/2026-11-06/consolidacion-harness/INFORME.md) registra qué se ejecutó, con revisiones y resultados.

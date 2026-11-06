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

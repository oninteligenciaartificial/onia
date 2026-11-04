# Ejecutar y retomar encargos

Este procedimiento usa las [reglas comunes](reglas-comunes.md), la [arquitectura](arquitectura.md) y el [estado vigente](ESTADO.md). El coordinador es el agente que recibe el encargo de Sergio. El CLI prepara el encargo y su registro; la ejecución y la delegación las realiza ese agente con las herramientas disponibles.

## Preparar el trabajo

Desde la raíz del checkout, comprobar los archivos que necesita el harness:

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py doctor
```

El diagnóstico comprueba archivos y referencias. Las pruebas de navegador, conexiones, publicación del entorno y descubrimiento de skills se realizan por separado. Si falta un archivo publicado, comprobar repo, `HEAD` y ruta antes de reconstruirlo o cambiar la arquitectura.

Preparar un encargo con un resultado verificable:

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py preparar oferta-piloto-001 --area marketing --objetivo "Preparar una oferta de taller entregable" --entregable "Ficha de oferta y guion de demostracion" --aceptacion "Resultado del alumno, demo, temario y faltantes identificados"
```

El comando crea el briefing en `operacion/encargos/oferta-piloto-001.md` y el registro usado por `scripts/trabajo.py`. Un ID ya existente se retoma; no se sobrescribe. En Windows puede usarse `python` en lugar de `python3`.

Las seis áreas son `marketing`, `video`, `desarrollo`, `automatizaciones`, `organizacion` y `producto`. Sus skills directoras y contexto mínimo se mantienen en [orquestacion.json](orquestacion.json). Son rutas de trabajo, no seis chats ni seis procesos permanentes. En producto se cotejan primero las instrucciones y el estado de ONIA Platform.

## Ejecutar con subagentes

El coordinador lee el briefing y resuelve el encargo dentro de su alcance. Cuando una parte independiente permita ahorrar tiempo o mejorar la comprobación, la delega con estos datos:

- Objetivo, entradas y criterio de aceptación de esa parte.
- Archivos que puede editar y archivos que pertenecen a otro agente.
- Skill directora o referencia concreta que necesita.
- Resultado esperado: cambio o artefacto, comprobación ejecutada y límites encontrados.

Cada archivo tiene un único responsable de escritura a la vez. Otro agente puede revisarlo sin editar; si necesita corregirlo, coordina el traspaso. Una investigación, una implementación y una revisión pueden avanzar en paralelo cuando sus dependencias lo permitan. Dos agentes no modifican a la vez el mismo borrador de entorno, formulario o flujo.

El coordinador integra las entregas, revisa el resultado completo y ejecuta la comprobación adecuada. Un mensaje de “terminado” de un subagente no sustituye la evidencia. Los permisos se toman de las reglas comunes y del encargo vigente; delegar no los amplía.

## Cerrar y entregar a otra sesión

Actualizar el registro con `scripts/trabajo.py actualizar`, incluyendo resultado, comprobación, siguiente paso y evidencia. Para recuperar el registro y el briefing de una tarea:

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py retomar oferta-piloto-001
```

Antes de terminar, dejar en [ESTADO.md](ESTADO.md) una entrega mínima saneada: encargo activo, resultado comprobado, commit o archivos relevantes, ubicación accesible de la evidencia y siguiente acción. Los cambios útiles de código e instrucciones se versionan en el repositorio. Los medios y datos privados conservan la ubicación definida en [accesos.md](accesos.md).

`operacion/` está ignorado por Git: un briefing o registro guardado allí no aparece automáticamente en otra VM. La sesión receptora lee la entrega versionada, comprueba el checkout y recupera sólo los materiales necesarios. Una nueva conversación se abre cuando Sergio la pide y hay un encargo delimitado; los subagentes sirven para partes del encargo actual.

## Recuperar un fallo

Registrar el comando o acción, error concreto, resultado parcial y próximo paso. Continuar con partes independientes; no repetir la misma prueba si no cambió su condición de bloqueo. Para el cierre usar la evidencia del entorno real: archivos presentes, proceso ejecutado, conexión autenticada o artefacto recuperable, según corresponda.

Si la VM o el acceso falta, retomar desde la última entrega persistida. Si hay cambios sin guardar, conservarlos antes de actualizar el checkout. Una operación externa de resultado incierto se consulta antes de reintentarse para evitar duplicados.

## Mejorar con trabajo real

Aplicar [mejorar-sistema](compartibles/skills/mejorar-sistema/SKILL.md) cuando un fallo observado justifique corregir una regla o procedimiento. Registrar evidencia, cambiar la fuente única, probar el caso y versionar el resultado. Usar [evaluar-catalogo-skills](compartibles/skills/evaluar-catalogo-skills/SKILL.md) al evaluar nuevos candidatos y [continuidad-de-trabajo](compartibles/skills/continuidad-de-trabajo/SKILL.md) al preparar un traspaso.

Ese ciclo mejora instrucciones y herramientas. La ejecución recurrente necesita un disparador concreto, persistencia comprobada y manejo de fallos; su disponibilidad se registra en ESTADO.md. Estos documentos y comandos no crean por sí solos un scheduler ni entrenan el modelo.

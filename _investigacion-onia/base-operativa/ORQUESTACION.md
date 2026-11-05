# Ejecutar y retomar encargos

Este procedimiento usa las [reglas comunes](reglas-comunes.md), el [plan oficial](PLAN.md) y el [estado vigente](ESTADO.md). **Una jefa local delega, revisa y entrega; las siete áreas locales ejecutan sus encargos.** ONIA · Jefa v2 (`01a1ab9c-15b2-7a03-9588-2daab62a93eb`) está designada, todavía en espera de commit/recepción y sin rol operativo activo. La anterior cierra el relevo; no se confirma su archivo ni el handoff por escribir estas líneas. [Contrato de relevo](continuidad/2026-11-05/HANDOFF-JEFA.md). El CLI prepara registros auxiliares; no inicia ni sincroniza agentes por sí solo.

El repo es la única autoridad para decisiones, reglas, estado y handoff. Organización mantiene la proyección cotidiana en Notion/Calendar sólo con alcance aplicable; Pages conserva medios y procedencia. Para reparto y autoridad, este procedimiento y ESTADO prevalecen sobre pasajes anteriores de [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md) y arquitectura. Los datos personales permanecen privados, sin exportarlos a paquetes públicos. Cada área carga sólo el contexto pertinente y enlaza evidencia en cierres compactos.

## Preparar el trabajo

**Despacho vigente:** la jefa operativa confirmada envía un encargo delimitado al área local existente de [SESIONES](SESIONES.md), confirma recepción y recupera el resultado; no abre otra jefa simultánea. Durante el relevo no se atribuyen lanzamientos a Jefa v2 antes de su recepción. El alcance actual distingue piloto D1 terminado como prueba, preparación n8n inactiva terminada con 13/13 controles estáticos, sin runtime, y el resto de la producción en pausa según ESTADO. Mantener la PC disponible para órdenes y revisiones locales; no hay scheduler acreditado.

**Antecedente del 4/11:** Jefe y Desarrollo cloud expusieron lectura/espera, sin envío/creación de chats en aquellos catálogos. La [prueba local→cloud](continuidad/2026-11-04/coordinacion-local-cloud.md) documenta ese reparto anterior en host durable/entorno onia. Se conserva como evidencia fechada; no fija el ejecutor actual ni acredita migración de VMs o secretos.

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

Las seis áreas ejecutables del CLI son `marketing`, `video`, `desarrollo`, `automatizaciones`, `organizacion` y `producto`. Sus skills directoras y contexto mínimo se mantienen en [orquestacion.json](orquestacion.json). Los once programas del plan continuo se distribuyen entre esas áreas; Jefatura y Aprendizaje no añaden claves al manifiesto ni skills automáticamente. El registro de áreas locales y orígenes cloud está en [SESIONES.md](SESIONES.md). Un chat no es un proceso permanente. En producto se cotejan primero las instrucciones y el estado de ONIA Platform.

Al iniciar un encargo, el agente selecciona el área por su resultado y lee automáticamente el cuerpo de la skill pertinente desde la ruta del manifiesto. Las skills de apoyo se cargan sólo cuando hacen falta. Si el catálogo nativo no las anuncia, leer la fuente canónica permite aplicar sus instrucciones; registrar esa diferencia sin pedir a Sergio que pegue la skill ni afirmar que el descubrimiento nativo pasó. Sólo un encargo cloud explícito usa [INICIO-SESION.md](cloud/INICIO-SESION.md); no es el arranque habitual de las áreas locales.

`preparar --skill` permite elegir la directora entre las declaradas del área: por ejemplo `--area organizacion --skill continuidad-de-trabajo` para un traspaso o `--area marketing --skill preparar-campana-meta` para anuncios. Sin esa opción se usa la directora predeterminada. El briefing señala las restantes como apoyos opcionales.

## Ejecutar con subagentes

Los subagentes internos son partes de un encargo y no equivalen a enviar mensajes a los chats persistentes de área. JEF-BASE-001 conserva evidencia de sus cuatro frentes; esa prueba no acredita despacho cloud→otros chats. Comprobar la herramienta disponible para cada mecanismo, sin crear sesiones nuevas para suplirlo.

El coordinador lee el briefing y resuelve el encargo dentro de su alcance. Cuando una parte independiente permita ahorrar tiempo o mejorar la comprobación, la delega con estos datos:

- Objetivo, entradas y criterio de aceptación de esa parte.
- Archivos que puede editar y archivos que pertenecen a otro agente.
- Skill directora o referencia concreta que necesita.
- Resultado esperado: cambio o artefacto, comprobación ejecutada y límites encontrados.

Cada archivo tiene un único responsable de escritura a la vez. Otro agente puede revisarlo sin editar; si necesita corregirlo, coordina el traspaso. Una investigación, una implementación y una revisión pueden avanzar en paralelo cuando sus dependencias lo permitan. Dos agentes no modifican a la vez el mismo borrador de entorno, formulario o flujo.

El coordinador integra las entregas, revisa el resultado completo y ejecuta la comprobación adecuada. Un mensaje de “terminado” de un subagente no sustituye la evidencia. Los permisos se toman de las reglas comunes y del encargo vigente; delegar no los amplía.

## Cerrar y entregar a otra sesión

Si el encargo usa un registro local del CLI, actualizarlo con `scripts/trabajo.py actualizar`, incluyendo resultado, comprobación, siguiente paso y evidencia. Las decisiones, el estado útil y los handoffs se consolidan en el repo; Notion refleja ese resultado. Los registros personales cotidianos quedan privados y no se exportan al repo ni a paquetes públicos. Un cierre compacto contiene resultado, evidencia/enlace, prueba realizada, bloqueo con solución y siguiente acción; no pega lecturas extensas ni historiales completos. Para recuperar el registro y el briefing de una tarea que sí usa el CLI:

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py retomar oferta-piloto-001
```

Cuando cambien capacidades o hitos, actualizar [ESTADO.md](ESTADO.md) con resultado comprobado, revisión, evidencia y siguiente acción. Consolidar cambios de dirección en [PLAN.md](PLAN.md), conservando la procedencia; los datos personales y diarios privados permanecen fuera de paquetes públicos; su vista en Notion no reemplaza el estado operativo versionado. Los cambios de código, reglas y skills requieren la autorización aplicable de Sergio; la incorporación de investigación no los activa. Los medios y datos privados conservan la ubicación definida en [accesos.md](accesos.md). Al entregar a otro chat, indicar el commit o revisión recuperable: subir Git no actualiza por sí solo una VM ni demuestra que el receptor leyó el cambio.

`operacion/` está ignorado por Git: conserva artefactos y auxiliares locales, nunca la única copia de una decisión, estado vigente o handoff. Consolidar el contexto útil en los documentos versionados, con ruta/hash para medios que deben quedar fuera de Git. Un archivo ignorado no aparece automáticamente en otra VM. La sesión receptora lee la entrega versionada, comprueba el checkout y recupera sólo los materiales necesarios. Una nueva conversación se abre cuando Sergio la pide y hay un encargo delimitado; los subagentes sirven para partes del encargo actual.

## Recuperar un fallo

Registrar el comando o acción, error concreto, resultado parcial y próximo paso. Continuar con partes independientes; no repetir la misma prueba si no cambió su condición de bloqueo. Para el cierre usar la evidencia del entorno real: archivos presentes, proceso ejecutado, conexión autenticada o artefacto recuperable, según corresponda.

Si la VM o el acceso falta, retomar desde la última entrega persistida. Si hay cambios sin guardar, conservarlos antes de actualizar el checkout. Una operación externa de resultado incierto se consulta antes de reintentarse para evitar duplicados.

## Mejorar con trabajo real

Aplicar [mejorar-sistema](compartibles/skills/mejorar-sistema/SKILL.md) cuando un fallo observado justifique corregir una regla o procedimiento. Registrar evidencia, cambiar la fuente única, probar el caso y versionar el resultado. Usar [evaluar-catalogo-skills](compartibles/skills/evaluar-catalogo-skills/SKILL.md) al evaluar nuevos candidatos y [continuidad-de-trabajo](compartibles/skills/continuidad-de-trabajo/SKILL.md) al preparar un traspaso.

Ese ciclo mejora instrucciones y herramientas. La ejecución recurrente necesita un disparador concreto, persistencia comprobada y manejo de fallos; su disponibilidad se registra en ESTADO.md. Estos documentos y comandos no crean por sí solos un scheduler ni entrenan el modelo.

# Ejecutar y retomar encargos

Aplicar [reglas-comunes](reglas-comunes.md), [ESTADO](ESTADO.md) y el encargo actual. Un coordinador integra y un responsable ejecuta cada tarea; otro puede revisar sin editar. El reparto de chats de fechas anteriores está en [SESIONES](SESIONES.md), como procedencia. No obliga a despachar cada tarea Cloud a áreas locales. El CLI prepara y recupera archivos; no crea agentes, chats, servicios ni disparadores.

## Entrada y selección

1. Comprobar repo, HEAD y cambios existentes, conservando trabajo ajeno. En Cloud seguir [INICIO-SESION](cloud/INICIO-SESION.md).
2. Identificar el área por el resultado del encargo y consultar [orquestacion.json](orquestacion.json). Leer las reglas generales, el estado vigente y el cuerpo de la directora canónica.
3. Leer sólo el contexto y las lecciones pertinentes. PLAN contiene dirección de negocio; SESIONES conserva repartos; los [antecedentes](continuidad/2026-11-06/consolidacion-harness/HISTORICO.md) se recuperan si la tarea los necesita.
4. Registrar por separado catálogo inicialmente anunciado, rutas realmente leídas y prueba realizada. Si ONIA no aparece en el catálogo, leer la fuente canónica permite trabajar, pero no acredita descubrimiento nativo ni ejecución automática de Start skill.

Las seis áreas CLI son `marketing`, `video`, `desarrollo`, `automatizaciones`, `organizacion` y `producto`. Jefatura y Aprendizaje no añaden claves ni agentes automáticos. En producto leer primero las instrucciones y el estado de ONIA Platform en su repo.

`--skill` selecciona una directora propia habilitada para el área; por ejemplo continuidad-de-trabajo en organización. `--apoyo CLAVE` incorpora una referencia pertinente al briefing y se puede repetir. Las claves `tercero-` sólo son apoyos. El CLI escribe enlaces: el agente debe leer los cuerpos. Sin selección, los apoyos se enumeran como opcionales, no se cargan todos.

## Preparación y comprobación

Desde la raíz del checkout (en Windows, python también es válido):

```sh
python3 _investigacion-onia/base-operativa/scripts/harness.py doctor
python3 _investigacion-onia/base-operativa/scripts/harness.py preparar demo-001 --compartible --area desarrollo --objetivo "Comprobar una entrega ficticia" --entregable "Informe con evidencia" --aceptacion "Resultado reproducible y límites explícitos"
```

`doctor` comprueba presencia de rutas; instalación, conexiones, navegador, publicación y descubrimiento se acreditan por separado. Un ID existente se retoma. El JSON es la autoridad de estado y briefing; el Markdown se genera desde él y se comprueba al recuperar.

Usar `--compartible` sólo para contenido saneado apto para el repo: crea el registro único en `continuidad/tareas/ID.json` y su proyección en `continuidad/encargos/ID.md`. Sin esa opción el registro queda en `operacion/` ignorada. No se copian ni convierten tareas privadas automáticamente y se rechaza un ID presente en ambos lugares.

Un ensayo de candidato requiere `--ensayo --investigacion RUTA --capacidad TEXTO --hipotesis TEXTO --control TEXTO --leccion TEXTO`. El coordinador revisa el contenido de la investigación; el CLI sólo comprueba presencia y ruta. No detecta automáticamente un ensayo mal clasificado.

## Ejecución y revisión

La selección de área/skill no configura un LLM. Elegir un perfil por tipo de trabajo mediante --perfil si corresponde, cotejar herramientas disponibles y registrar por separado modelo/esfuerzo recomendado, solicitado y observado. Desconocido se conserva como null. Los perfiles del manifiesto son candidatos revisables; no ganadores demostrados ni permisos para gasto. Escalar ante un fallo de razonamiento identificado, no por falta de credenciales o herramientas.

Retomar comienza por la vista breve; consultar historial o --completo sólo cuando una decisión o revisión lo requiera. El briefing conserva restricciones y aparece una sola vez en tarea.briefing.contenido. Las decisiones sustituidas conservan procedencia y siguen disponibles en detalle. Para cambios paralelos, usar responsable y rutas explícitas; el comando asignar comprueba reservas en este checkout. Ver [contrato de continuidad](cloud/CONTINUIDAD.md) para actor, revisión esperada, reasignación y límites entre clones.

Delegar partes independientes con objetivo, entradas, entregable, comprobación y archivos asignados. Cada archivo y configuración tiene un único escritor. Los subagentes internos y los chats persistentes son mecanismos distintos; comprobar herramientas y autorización para cada uno. Un mensaje de “terminado” no sustituye la evidencia.

Centralizar preguntas y decisiones en el chat de coordinación del encargo. Las autorizaciones nativas pueden quedar ancladas al chat que invoca la herramienta; no prometer moverlas ni accionarlas por Sergio. La existencia de un chat o una preferencia móvil no acredita push o programación.

El ejecutor prepara evidencia y deja `para_revision` únicamente con comprobación declarada correcta. El revisor coteja el resultado con la aceptación y usa `aceptar` de forma explícita. Cada mutación exige la revisión esperada; si cambió, retomar y reconciliar antes de escribir. Los nombres de revisor y comprobaciones son declaraciones auditables, no autenticación ni garantía automática de calidad.

Para tareas de código paralelas, usar ramas y copias de trabajo separadas cuando corresponda al encargo y a las capacidades disponibles, e integrar secuencialmente con revisión. Crear worktrees o chats requiere la autorización aplicable de la herramienta. Una rama separada no aísla ni bloquea efectos sobre servicios externos.

## Cierre, traspaso y fallos

Seguir [CONTINUIDAD](cloud/CONTINUIDAD.md) para comandos, recuperación, publicación y prueba A→B. Un traspaso compartible proporciona ID, repositorio y commit; la nueva sesión recupera objetivo, briefing, evidencia y siguiente paso desde Git, no desde todo el chat.

Conservar evidencia por revisión sin sobrescribirla. Ante alteración o pérdida, recuperar los bytes originales desde la entrega publicada; no recalcular hashes para ocultar el fallo. Si se interrumpió la proyección del briefing, `recuperar` puede reconstruir sólo el Markdown ausente desde el JSON íntegro. Un lock abandonado requiere verificar primero que ya no haya un escritor activo.

Actualizar [ESTADO](ESTADO.md) cuando cambien capacidades o hitos, con evidencia y límites. No reescribir la historia como si una prueba anterior validara el código actual. La [guía móvil](cloud/MOVIL.md) explica el acceso; el uso real del teléfono se acredita por separado.

Aplicar mejorar-sistema a correcciones observadas, evaluar-catalogo-skills a selección de candidatos y continuidad-de-trabajo a traspasos. Esta mejora de instrucciones no crea un scheduler ni entrenamiento del modelo.

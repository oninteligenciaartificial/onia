# Ejecutar y retomar encargos

Aplicar [reglas-comunes](reglas-comunes.md), [ESTADO](../00-MAPA/ESTADO.md) y el encargo actual. Un coordinador integra y un responsable ejecuta cada tarea; otro puede revisar sin editar. El reparto de chats de fechas anteriores está en [SESIONES](SESIONES.md), como procedencia. No obliga a despachar cada tarea Cloud a áreas locales. El CLI conserva la preparación y recuperación del registro único y ahora lanza/reanuda procesos `codex exec` en worktrees separados, con hasta tres sesiones vivas, cierre comprobado en origin y revisión independiente. No crea chats del escritorio, scheduler ni servicios; no mide cuota ni amplía permisos externos.

## Entrada y selección

1. Comprobar repo, HEAD y cambios existentes, conservando trabajo ajeno. En Cloud seguir [INICIO-SESION](../05-herramientas/cloud/INICIO-SESION.md).
2. Identificar el área por el resultado del encargo y consultar [orquestacion.json](orquestacion.json). Leer las reglas generales, el estado vigente y el cuerpo de la directora canónica.
3. Leer sólo el contexto y las lecciones pertinentes. PLAN contiene dirección de negocio; SESIONES conserva repartos; los [antecedentes](../99-archivo/2026-11-06/consolidacion-harness/HISTORICO.md) se recuperan si la tarea los necesita.
4. Registrar por separado catálogo inicialmente anunciado, rutas realmente leídas y prueba realizada. Si ONIA no aparece en el catálogo, leer la fuente canónica permite trabajar, pero no acredita descubrimiento nativo ni ejecución automática de Start skill.

Las seis áreas CLI son `marketing`, `video`, `desarrollo`, `automatizaciones`, `organizacion` y `producto`. Jefatura y Aprendizaje no añaden claves ni agentes automáticos. En producto leer primero las instrucciones y el estado de ONIA Platform en su repo.

`--skill` selecciona una directora propia habilitada para el área; por ejemplo continuidad-de-trabajo en organización. `--apoyo CLAVE` incorpora una referencia pertinente al briefing y se puede repetir. Las claves `tercero-` sólo son apoyos. El CLI escribe enlaces: el agente debe leer los cuerpos. Sin selección, los apoyos se enumeran como opcionales, no se cargan todos.

## QA previo de videos recibidos

Antes de procesar un video de Sergio, identificar para qué lo quiere. Hacer una clasificación ligera con el pedido y, si hace falta, identidad, descripción, duración o una vista preliminar accesible. Este QA selecciona el trabajo; no acredita comprensión del video ni requiere descargarlo y analizarlo entero.

Elegir sólo los componentes necesarios:

- Resumen, idea o guion: texto disponible o ASR pertinente y apoyo visual cuando cambie la respuesta.
- Verificar una afirmación: recuperar el pasaje y contrastar fuentes; no estudiar toda la edición por defecto.
- Edición, colores, encuadre o tipografía: imágenes y tiempos pertinentes; ampliar cortes o detalles según el atributo pedido.
- Sonido: audio y herramientas pertinentes al atributo solicitado, declarando capacidades no validadas. PANNs es auxiliar experimental, no escucha ni detector acreditado de música/SFX.
- Estudio completo o prueba explícita del flujo: aplicar el alcance autorizado y conservar cobertura y límites por componente.

Una URL o «mirá esto» sin finalidad clara no activa automáticamente ASR completo, todos los frames, PANNs y revisión integral. Presentar un QA breve: qué material es, posible utilidad, alcance recomendado y datos que faltan; aclarar el objetivo antes del trabajo pesado. Si el pedido ya define la finalidad o el análisis completo, avanzar dentro de ese alcance sin pedir otra confirmación. Reutilizar resultados existentes y ampliar sólo una brecha pertinente; enviar un video no inicia por sí solo otra investigación de modelos, organización o despliegue.

Fuente: corrección directa de Sergio tras el reel DfaLyn7Rorf, 6/11/2026: no todos los videos requieren el flujo completo; primero QA para decidir qué hacer. [Caso y cotejo documental](registro-de-errores.md#qa-previo-de-videos--6-de-noviembre-de-2026).

## Preparación y comprobación

Desde la raíz del checkout (en Windows, python también es válido):

```sh
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py doctor
python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py preparar demo-001 --compartible --area desarrollo --objetivo "Comprobar una entrega ficticia" --entregable "Informe con evidencia" --aceptacion "Resultado reproducible y límites explícitos"
```

`doctor` comprueba presencia de rutas; instalación, conexiones, navegador, publicación y descubrimiento se acreditan por separado. Un ID existente se retoma. El JSON es la autoridad de estado y briefing; el Markdown se genera desde él y se comprueba al recuperar.

Usar `--compartible` sólo para contenido saneado apto para el repo: crea el registro único en `04-operacion-agentes/tareas/ID.json` y su proyección en `04-operacion-agentes/encargos/ID.md`. Sin esa opción el registro queda en `operacion/` ignorada. Los registros heredados en `continuidad/` siguen siendo legibles. No se copian ni convierten tareas privadas automáticamente y se rechaza un ID presente en ambos lugares.

Un ensayo de candidato requiere `--ensayo --investigacion RUTA --capacidad TEXTO --hipotesis TEXTO --control TEXTO --leccion TEXTO`. El coordinador revisa el contenido de la investigación; el CLI sólo comprueba presencia y ruta. No detecta automáticamente un ensayo mal clasificado.

## Ejecución y revisión

La selección de área/skill no configura un LLM. Elegir un perfil por tipo de trabajo mediante --perfil si corresponde, cotejar herramientas disponibles y registrar por separado modelo/esfuerzo recomendado, solicitado y observado. Desconocido se conserva como null. Los perfiles del manifiesto son candidatos revisables; no ganadores demostrados ni permisos para gasto. Escalar ante un fallo de razonamiento identificado, no por falta de credenciales o herramientas.

Retomar comienza por la vista breve; consultar historial o --completo sólo cuando una decisión o revisión lo requiera. El briefing conserva restricciones y aparece una sola vez en tarea.briefing.contenido. Las decisiones sustituidas conservan procedencia y siguen disponibles en detalle. Para cambios paralelos, usar responsable y rutas explícitas; el comando asignar comprueba reservas en este checkout. Ver [contrato de continuidad](../05-herramientas/cloud/CONTINUIDAD.md) para actor, revisión esperada, reasignación y límites entre clones.

Delegar partes independientes con objetivo, entradas, entregable, comprobación y archivos asignados. Cada archivo y configuración tiene un único escritor. Los subagentes internos y los chats persistentes son mecanismos distintos; comprobar herramientas y autorización para cada uno. Un mensaje de “terminado” no sustituye la evidencia.

Centralizar preguntas y decisiones en el chat de coordinación del encargo. Las autorizaciones nativas pueden quedar ancladas al chat que invoca la herramienta; no prometer moverlas ni accionarlas por Sergio. La existencia de un chat o una preferencia móvil no acredita push o programación.

El ejecutor prepara evidencia y deja `para_revision` únicamente con comprobación declarada correcta. El revisor coteja el resultado con la aceptación y usa `aceptar` de forma explícita. Cada mutación exige la revisión esperada; si cambió, retomar y reconciliar antes de escribir. Los nombres de revisor y comprobaciones son declaraciones auditables, no autenticación ni garantía automática de calidad.

Para tareas de código paralelas, usar ramas y copias de trabajo separadas cuando corresponda al encargo y a las capacidades disponibles, e integrar secuencialmente con revisión. Crear worktrees o chats requiere la autorización aplicable de la herramienta. Una rama separada no aísla ni bloquea efectos sobre servicios externos.

## Cierre, traspaso y fallos

Seguir [CONTINUIDAD](../05-herramientas/cloud/CONTINUIDAD.md) para comandos, recuperación, publicación y prueba A→B. Un traspaso compartible proporciona ID, repositorio y commit; la nueva sesión recupera objetivo, briefing, evidencia y siguiente paso desde Git, no desde todo el chat.

Conservar evidencia por revisión sin sobrescribirla. Ante alteración o pérdida, recuperar los bytes originales desde la entrega publicada; no recalcular hashes para ocultar el fallo. Si se interrumpió la proyección del briefing, `recuperar` puede reconstruir sólo el Markdown ausente desde el JSON íntegro. Un lock abandonado requiere verificar primero que ya no haya un escritor activo.

Actualizar [ESTADO](../00-MAPA/ESTADO.md) cuando cambien capacidades o hitos, con evidencia y límites. No reescribir la historia como si una prueba anterior validara el código actual. La [guía móvil](../05-herramientas/cloud/MOVIL.md) explica el acceso; el uso real del teléfono se acredita por separado.

Aplicar mejorar-sistema a correcciones observadas, evaluar-catalogo-skills a selección de candidatos y continuidad-de-trabajo a traspasos. Esta mejora de instrucciones no crea un scheduler ni entrenamiento del modelo.

## Comandos del lanzador VPS (fase 1, 8 de noviembre)

Requiere Linux, Python 3.10+, Git y Codex CLI autenticado en el usuario actual. Implementación sin dependencias Python externas. `harness_sesiones.py` es el módulo interno de `harness.py`; todas las transiciones utilizan `trabajo.py`, su revisión esperada, historial y evidencia. No es otra cola.

Desde el checkout coordinador, usando un ID nuevo y rutas relativas a base-operativa:

```bash
# Si ~/repos/onia conserva cambios sin commit, no actualizar ese checkout.
# Crear una sola vez un coordinador limpio (sin lanzar una sesión):
git -C ~/repos/onia fetch origin
git -C ~/repos/onia worktree add --detach ~/repos/onia-coordinador origin/master
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
T=_investigacion-onia/base-operativa/05-herramientas/scripts/trabajo.py
bash _investigacion-onia/base-operativa/05-herramientas/scripts/instalar-skills-locales.sh
python3 "$H" doctor
python3 "$H" preparar ejemplo-001 --area desarrollo --objetivo "Implementar el cambio aprobado" --entregable "Cambio y evidencia" --aceptacion "Pruebas pertinentes aprobadas y alcance satisfecho"
python3 "$H" asignar ejemplo-001 --revision-esperada 1 --responsable ejecutor-001 --ruta 05-herramientas/ejemplo
# Sólo después del checklist y del sí de Sergio a esta sesión:
python3 "$H" lanzar ejemplo-001 --revision-esperada 2 --actor ejecutor-001 --si-sergio
python3 "$H" estado
python3 "$H" retomar ejemplo-001
```

`lanzar` crea `../onia-ws-ejemplo-001`, rama `codex/ws-ejemplo-001`, desde `origin/master` después de `fetch`. Cada ejecutor nuevo tiene su repositorio bare privado en `~/operacion/git/ejemplo-001.git`, con objetos copiados por Git, sin alternates ni metadatos compartidos con el coordinador. El supervisor ejecuta en segundo plano:

```bash
codex -a never \
  -c 'default_permissions="harness-git"' \
  -c 'permissions.harness-git.extends=":workspace"' \
  -c 'permissions.harness-git.network.enabled=true' \
  -c 'permissions.harness-git.filesystem={"<bare privado>"="write","<gitdir del worktree>"="write"}' \
  exec --json --ignore-user-config -C <worktree> - < <briefing>
```

Guarda eventos privados en `~/operacion/logs/ejemplo-001.jsonl`, stderr aparte y el briefing efectivo por intento. La tarea contiene PID de Codex, PID del supervisor, identidades de arranque Linux, rama, session id, estado y resultado del proceso. El hijo espera una señal del supervisor hasta que su PID esté persistido; si el supervisor cae antes, no ejecuta Codex. El índice `~/operacion/sesiones.tsv` se actualiza bajo un `flock` corto compartido; el lock no dura toda la ejecución. La identidad de arranque y boot id evitan confundir un PID reutilizado o un zombi con una sesión viva. `estado` reconcilia el índice y los eventos sin imprimir su contenido sensible: muestra el tipo del último evento, estado de tarea y revisión actual. El código de salida cero no acredita entrega ni aceptación.

No modificar ni copiar los registros canónicos desde los worktrees ejecutores. Compartir `--operacion /ruta` entre todos los coordinadores del mismo VPS si se cambia el valor predeterminado; otra carpeta evade la coordinación y no debe usarse para sesiones reales del mismo VPS. El límite cuenta procesos gestionados por este harness, no inspecciona ni controla el app-server o sesiones externas. Las reservas no bloquean a un editor ajeno.

Retoma y cierre, con `N` sustituido por la revisión actual que devuelve `estado` o `retomar`:

```bash
python3 "$H" reanudar ejemplo-001 --revision-esperada N --actor ejecutor-001 --si-sergio
python3 "$H" cerrar ejemplo-001 --revision-esperada N --actor ejecutor-001 --resultado "Cambio y evidencia listos" --comprobacion "Comprobaciones ejecutadas y resultados concretos"
```

`reanudar` conserva rama, worktree y log, agrega un intento y usa `codex … exec --json --ignore-user-config -C <worktree> resume <session_id> -` con el mismo perfil y dueño Git privado. Los intentos anteriores a esta capacidad conservan su sandbox y metadatos originales; no se migran ni amplían sus permisos al retomar. No utiliza `--last`, no vuelve a partir de master ni descarta cambios. Un ID de sesión ausente impide reanudar: preservar el log y conciliar; no inventar un ID ni relanzar a ciegas. Una sesión viva impide una segunda ejecución de la misma tarea. `retomar` conserva su semántica anterior: leer el estado, sin ejecutar.

Después de una interrupción externa, antes de `reanudar`, comprobar desde el host que terminaron también los procesos auxiliares del intento y preservar los bytes, staging, HEAD y SID. `estado` sólo acredita el PID Codex y su supervisor: no detecta todos los hijos huérfanos. En el piloto SIGTERM quedaron tres procesos de un lector de sólo lectura; el coordinador los dejó salir mediante su barrera y comprobó cero residuales antes de continuar. No señalar procesos ajenos ni grupos completos. Cotejar el `thread.started` del nuevo segmento del log con el SID esperado y comprobar los commits ya publicados antes de crear otro: el harness no impone idempotencia sobre el trabajo del agente. [Prueba y límites](../05-herramientas/2026-11-08-harness/INTERRUPCION-REAL-2026-11-08.md).

`cerrar` exige un commit nuevo descendiente del commit base, recupera explícitamente la rama de la tarea con `git fetch origin +refs/heads/<rama>:refs/remotes/origin/<rama>`, comprueba `git branch -r --contains <commit>` y exige que esa rama de origin contenga el commit. También exige que la rama y HEAD del worktree coincidan. Si falta publicación, queda abierta y explica que falta push. Si hay modificaciones, archivos no versionados o ignorados ajenos, conserva el worktree y pide preservarlos; nunca usa `--force`. Únicamente los enlaces propios generados en `.agents/skills` se consideran descartables. Después guarda recibo y pasa a `para_revision`; `git worktree remove` se ejecuta desde el dueño correcto y conserva la rama y el bare privado. El coordinador importa objetos y la referencia remota mediante fetch; no necesita una rama local duplicada del ejecutor. La tarea y los recibos del coordinador se publican por separado cuando son compartibles.

Revisión y aceptación:

```bash
python3 "$H" revisar ejemplo-001 --revision-esperada N --actor ejecutor-001 --revisor revisor-001 --si-sergio
python3 "$H" estado
python3 "$H" revisar ejemplo-001 --recoger --revision-esperada N
python3 "$H" aceptar ejemplo-001 --revision-esperada N --revisor revisor-001 --criterio "Entrega cotejada con todos los criterios"
```

La revisión crea otro worktree, detached en el commit de entrega, y otra sesión Codex, con `--sandbox read-only`, red de workspace deshabilitada y `--ignore-user-config`. La salida final estructurada (`veredicto`, `commit`, `criterio`) la escribe el CLI en operación, no el agente en el repo. Recoger exige proceso terminado con rc=0, session id distinto de todos los intentos ejecutores y la misma entrega; valida el JSON, conserva su evidencia y retira el worktree revisor limpio. `aceptar`, incluso invocado directamente desde `trabajo.py`, rechaza veredictos ausentes, malos, alterados, obsoletos o simulados. Esto no autentica humanos ni garantiza por sí solo la calidad del modelo. La revisión se debe contrastar con evidencia.

Con veredicto `cambios`, reabrir mediante `trabajo.py actualizar … --estado en_curso --actor ejecutor-001 --revision-esperada N --resultado … --siguiente …`, reanudar la misma sesión ejecutora y volver a cerrar/revisar. No sobrescribir evidencias anteriores. Después de aceptar, liberar explícitamente las rutas con `trabajo.py asignar … --liberar --actor ejecutor-001 --revision-esperada N`. Integrar cada rama y comprobar `origin/master` antes de dar por terminado el trabajo.

### Simulación reproducible sin Codex

`--dry-run` en lanzar/estado/cerrar/revisar usa `~/operacion/harness-dry-run/` y tareas de juguete nuevas. No llama a Codex, no hace fetch, no crea ni retira worktrees y no demuestra una publicación. Los PID son null, el ID es ficticio y la ocupación se marca `viva_simulada`. Cerrar libera ese cupo y registra un cierre simulado; `aceptar` siempre lo rechaza. Un mismo ID no puede mezclar modo real y simulado.

```bash
python3 -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p 'test_*.py'
bash -n _investigacion-onia/base-operativa/05-herramientas/scripts/instalar-skills-locales.sh
```

`test_harness_sesiones.py` recorre preparar → asignar → lanzar → estado → cerrar con `--dry-run`, llena tres cupos y rechaza el cuarto. También usa un ejecutable sintético y remotos Git locales para comprobar supervisión, retoma, publicación, rechazo por cambios pendientes y revisión; no consume cuota ni lanza Codex real.

Sintaxis contrastada con `codex-cli 0.167.0`, `codex exec --help`, `codex exec resume --help` y [documentación oficial de modo no interactivo](https://learn.chatgpt.com/docs/non-interactive-mode). El piloto previo acreditó autenticación, retoma y revisión. La publicación autónoma usa el perfil acotado descrito abajo y se verifica en su propio piloto; no asumir compatibilidad de otras versiones del CLI.

### Resultado del piloto real y selección de runtime

El piloto `harness-piloto-real-20261108` ejercitó una pausa voluntaria y la retoma por el mismo ID; su publicación la hizo el coordinador por el bloqueo del índice compartido. Los ejecutores nuevos resuelven esa limitación mediante Git privado y el perfil `harness-git`: la sesión ejecutora hace `git add`, `git commit` y `git push origin HEAD:refs/heads/codex/ws-ID` sin intervención del coordinador. Éste conserva cierre, revisión e integración a master. No asumir que `rc=0` implica commit/push.

El perfil extiende `:workspace`, agrega escritura sólo al bare y al gitdir privados y mantiene `.git` pointer y las carpetas protegidas de instrucciones en sólo lectura. Usa `-a never`, red habilitada y `--ignore-user-config`; no se combina con `--sandbox` ni con ajustes legacy que anularían el perfil. No se cambia configuración global ni se usa acceso irrestricto. Se valida el dueño antes de ejecutar, retomar y cerrar; un enlace, dueño diferente o almacén dependiente de alternates bloquea. `GIT_*` heredadas se eliminan para impedir redirecciones accidentales. Identidad local de commit: `OnIA Codex <onia-codex-worker@localhost>`.

Los perfiles requieren un CLI compatible (probado con 0.167.0). Fuentes oficiales: [permisos](https://learn.chatgpt.com/docs/permissions) y [rutas protegidas](https://learn.chatgpt.com/docs/agent-approvals-security). El aislamiento es de archivos locales; las credenciales GitHub existentes conservan su alcance remoto. No es una ACL remota de ramas ni una autorización para producción. La sesión sólo debe publicar su rama asignada sin force. La retención del bare permite retomar después del cierre sin borrar la rama; no hay limpieza automática de esos repositorios.

`lanzar`, `reanudar` y `revisar` admiten `--modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt`. Modelo y esfuerzo quedan registrados por intento; `reanudar` hereda los valores anteriores si se omiten. `--auth-chatgpt` exige autenticación ChatGPT/proveedor OpenAI y elimina del entorno del hijo las variables `OPENAI_API_KEY`, `CODEX_API_KEY` y `OPENAI_BASE_URL`; no cambia configuración global, no compra créditos ni sustituye la comprobación de cuota/saldo. Modelo solicitado y observado se distinguen en evidencia de runtime.

Para verificar publicación, cierre y revisión hacen fetch explícito de la rama de la tarea, aunque el clon esté configurado para recuperar sólo master. No se modifica el refspec configurado ni se podan otras referencias. Si la rama remota falta o no contiene el commit, la tarea permanece abierta.

### Delegación nativa acotada (8/11/2026)

`lanzar` y `reanudar` aceptan `--subagentes-maximos 0|1|2`: por defecto cero y la retoma hereda el valor anterior. Revisores siempre cero, incluso con esfuerzo ultra. Se registra por intento y configura sólo ese proceso, sin editar ajustes globales. El límite nativo cuenta hijos abiertos y excluye el principal; cerrar/liberar cada hijo antes de iniciar el siguiente. `agents.max_depth=1` con multi_agent V1 impide nietos; V2 queda desactivado. Los hijos usan archivos exclusivos, no hacen Git y heredan las restricciones. El ejecutor reúne, verifica y publica su grupo.

Ejemplo autorizado para cerebros: `python3 "$H" lanzar cerebros-a-20261108 --revision-esperada N --actor cerebros-ejecutor-a --si-sergio --modelo gpt-6.1-sol --esfuerzo high --auth-chatgpt --subagentes-maximos 1`. Revisión: `python3 "$H" revisar cerebros-a-20261108 --revision-esperada N --actor cerebros-ejecutor-a --revisor cerebros-revisor-a --si-sergio --modelo gpt-6.1-sol --esfuerzo ultra --auth-chatgpt`.

El máximo tres del harness cuenta sesiones principales (ejecutoras o revisoras). Con este encargo puede haber además hasta tres hijos nativos, uno por grupo; no equivale a sólo tres contextos consumiendo cuota. Mantener evidencia de IDs, modelo y esfuerzo efectivos. Fuente: [configuración oficial de subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents), CLI 0.167.0 y validación estricta local sin modelo. Si faltan herramientas, registrar el límite y preservar trabajo; no sustituirlo por otros procesos de Codex.

En `comprobacion`, describir controles ya realizados. Lo pendiente va en `proximo_paso`; así un chequeo previo no aparenta contradecir una aceptación posterior. No reescribir evidencias aceptadas para cambiar ese texto histórico.

Una retoma recibe resultado, comprobación y próximo paso del registro actual, más el último veredicto conservado en `evidencias_revision` cuando existe. Así la ejecutora recibe los cambios pedidos aunque reabrir haya limpiado `revision_independiente`. El recibo se verifica antes de leerlo y se identifica su commit; no convierte una revisión vieja en aprobación de una entrega nueva.

# Modelos, sesiones y tareas de OnIA: observado y próximo diseño

Auditoría de solo lectura, 8 de noviembre de 2026, aproximadamente 18:42 America/Caracas. No se lanzó, reanudó ni interrumpió ninguna sesión de trabajo; no se instaló nada ni se modificó el repo. El coordinador publica este informe junto con el resultado del navegador. Base leída: `onia-coordinador`, cuya referencia publicada al comenzar era `28bdb2a4dd574ba649d344d740637e8ac38bf841`.

## Lo que existe y lo que falta

El harness ya permite elegir modelo y esfuerzo explícitos por intento, limitar hijos, continuar el mismo SID, reservar rutas y exigir una revisión independiente antes de aceptar. `orquestacion.json` ya contiene perfiles por tipo de trabajo. **La selección automática por tarea, el inventario automático de cada hijo, la pausa cooperativa y el control continuo de cuota todavía no están implementados.** Conviene extender estos componentes, sin crear otra cola ni otra memoria.

Hay una diferencia concreta entre capacidad y uso: las cuatro tareas inspeccionadas tienen `ejecucion: null`. El modelo solicitado sí está en cada elemento de `sesiones[]`; los modelos observados fueron recuperados por helpers desde `turn_context`, pero no se incorporan automáticamente a la ficha de ejecución. `estado` muestra procesos/estados; no ofrece todavía el árbol completo de modelos y consumo.

## Modelos realmente observados

Se contrastaron los JSON canónicos con los eventos privados del runtime, extrayendo exclusivamente identidad de sesión/padre, modelo, esfuerzo y fecha. No se publican prompts, configuración completa ni credenciales.

| Sesión | Modelo / esfuerzo observados | Estado en la consulta |
|---|---|---|
| Este chat coordinador, `01a1bc0b-65c1-7e13-afef-88fc1482896a` | `gpt-6-astra`; último `turn_context` a las 18:38:45 Caracas: `xhigh`. Contextos anteriores del mismo chat registran `ultra`. | Encargo de navegador y organización en curso. |
| Auxiliar de esta auditoría, `01a1bd50-eee7-7061-a532-21eced9f39e3` | `gpt-6-astra`; primer contexto `ultra`, posteriores `xhigh`, último a las 18:39:21 Caracas. | Informe de solo lectura. |
| `cerebros-a-20261108` | `gpt-6.1-sol / high` | Ejecución finalizada; tarea `en_espera`, entrega parcial. |
| `cerebros-b-20261108` | `gpt-6.1-sol / high`, también en la retoma con el mismo SID | PID vivo; tarea `en_curso`. |
| `cerebros-c-20261108` | `gpt-6.1-sol / high` | Ejecución finalizada; tarea `en_espera`, revisión pendiente. |
| `investigacion-acceso-av-20261108` | `gpt-6.1-sol / high` | Ejecución finalizada; tarea `en_espera`. |
| 20 hijos de las cuatro ejecutoras anteriores | Todos los contextos encontrados: `gpt-6.1-sol / high` | Son 19 referentes más el auxiliar de alternativas AV, acumulados, no 20 simultáneos. |

Las tres revisoras del encargo profundo están previstas con **Sol 6.1 / ultra**, distintas de las ejecutoras y sin hijos, pero todavía no constan intentos revisores en estas cuatro tareas. No presentar la configuración prevista como una revisión ejecutada. Las revisiones anteriores de otros pilotos/lotes no aceptan este lote.

**Lección de esta auditoría:** el auxiliar actual heredó Astra del chat, aunque el lote de referentes usa Sol. No hubo selección explícita Sol/Terra para este auxiliar. El modelo del padre, el valor por defecto para hijos y el modelo efectivo de cada hijo son datos distintos; fijarlos cuando el reparto los exija y comprobarlos después. El registro conserva esta ejecución real, sin relanzarla para aparentar otra configuración.

El último mensaje de B consultado informa Erik 5, Enrique 4, San 4 y Cormac 4 piezas; estaba aclarando atribución de roles en una pieza de Enrique antes de cerrar. Es progreso declarado por la ejecutora, todavía pendiente de comprobar en entrega y revisión. No se cambió su estado ni se interrumpió.

## Catálogo y cuota fechados

La caché del CLI 0.167.0 fue obtenida el 8/11 a las 18:39:53 Caracas. Lista `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6.1-terra`, `gpt-6-sol`, `gpt-6-luna` y modelos 5.6 todavía visibles. Las entradas ocultas no se proponen para tareas. Estar en la caché no acredita haber ejecutado cada modelo ni garantiza disponibilidad futura.

Los modelos visibles inspeccionados declaran entrada **texto e imagen** en este cliente. Eso no acredita entrada audiovisual conjunta ni escucha directa de música. ASR, fotogramas y OCR siguen siendo herramientas separadas. Los pesos de estos LLM no están instalados en el VPS: Codex ejecuta herramientas allí y usa el servicio de modelos. No confundirlos con `faster-whisper small`, cuyos pesos sí están en el VPS.

Último evento de cuota leído: **8/11/2026, 18:40:38 Caracas / 22:40:38 UTC: 33% semanal utilizado, saldo adicional 0**. Es una observación del runtime de la cuenta compartida, no una consulta nueva de facturación, ni el costo exclusivo de este encargo. No se compraron créditos. La selección de modelos y los hijos consumen la cuota incluida; no hay un contador monetario fiable por tarea en el harness actual.

## Selección práctica por tarea

Mantener los perfiles de `orquestacion.json`, tratándolos como candidatos que deben superar nuestra aceptación. No convertir el nombre del área en una selección fija de modelo.

| Trabajo | Perfil existente y punto inicial propuesto | Cuándo cambiar |
|---|---|---|
| Extraer, clasificar o transformar material ya disponible con esquema preciso | `extraccion`: Luna high | Comparar con Sol high si omite datos críticos y las fuentes/herramientas sí estaban disponibles. |
| Reunir fuentes, redactar una entrega con dependencias acotadas | `multifuente`: Sol 6.1 medium | High ante un fallo concreto de razonamiento o requisitos contrapuestos. |
| Cambio acotado de código, escritura o lectura visual verificable | `cambio-acotado`: Terra 6.1 medium | Comparar con Sol medium si falla el criterio; no asumir ahorro probado. |
| Diseño, investigación difícil o integración compleja | `complejo`: Sol 6.1 high | Astra medium/high sólo ante una dificultad de razonamiento identificada y con cuota/autorización aplicables. |
| Revisión | Otro SID, read-only, esfuerzo acorde a la dificultad; el lote profundo mantiene Sol 6.1 ultra por instrucción de Sergio | Cambiar el modelo no reemplaza criterios objetivos ni una referencia humana cuando haga falta. |

Estas pautas coinciden con las orientaciones generales de [modelos](https://learn.chatgpt.com/docs/models) y [selección](https://learn.chatgpt.com/docs/model-selection), consultadas el 8/11. Son hipótesis operativas para OnIA: no se ejecutó un benchmark que demuestre cuál es mejor o más barato en nuestras tareas. Luna no anuncia `ultra`; Sol/Astra/Terra sí en la caché actual. Validar el par modelo/esfuerzo antes de lanzar. Las recomendaciones no sustituyen una selección explícita de Sergio.

No subir de modelo ante falta de acceso, una URL bloqueada, OCR ausente o una cuota agotada. Primero resolver o registrar esa dependencia. Más razonamiento no aporta credenciales ni convierte imágenes en audio.

## Extensión mínima del sistema existente

1. **Preflight por tarea.** Objetivo, aceptación, entradas, dependencias por ID/commit, permisos, modalidades/herramientas requeridas, rutas, responsable, modelo/esfuerzo elegido y motivo. Añadir presupuesto de tiempo, cuota observada con fecha, máximo de intentos y condición de parada. Primero revisar si el resultado o la herramienta ya existe en GitHub.
2. **Ficha de ejecución por intento e hijo.** Conservar `recomendado`, `solicitado` y `observado` separados. Registrar SID padre/hijo, modelo/esfuerzo, evidencia del evento, turno/fecha, ruta asignada, estado y límite. Guardar un historial si el runtime cambia entre turnos; el último valor no debe borrar los anteriores. Un dato no observable queda `null`, sin convertir la configuración en prueba.
3. **Recolector de evidencia.** Incorporar al harness la extracción selectiva que hoy hacen los helpers. Versionar y probar el parser del runtime; no importar logs íntegros a Git. Si aparece un modelo inesperado, detener el siguiente despacho y conciliar, preservando lo producido. Un log de modelo no prueba por sí solo herencia de herramientas ni éxito de navegación.
4. **Vista única.** Extender `estado` con tarea, dependencia, PID, último avance, padre/hijos, solicitado/observado, revisión, commit remoto, próximo paso y cuota fechada. Los JSON canónicos mandan; una tabla, Notion o la barra de chats sólo los reflejan. Las sesiones CLI no crean automáticamente chats visibles.
5. **Pausa verificable.** Añadir pausa cooperativa y recibo de bloqueo al modelo actual. No basta editar `estado=en_espera`: ese cambio no detiene un proceso. El coordinador solicita checkpoint, el ejecutor deja de iniciar efectos nuevos, conserva cambios/commits, termina sus hijos y confirma proceso finalizado. Sin acuse, se informa la incertidumbre y se inspecciona la identidad de procesos; no se mata un grupo ni un servicio ajeno.
6. **Reanudación.** Resolver la dependencia en una tarea separada si sus rutas y objetivo son distintos; publicar la corrección. Releer el registro y commit de la tarea original, comprobar cambios existentes y continuar el mismo SID con `reanudar`. No crear otra copia de tarea ni duplicar commits ya publicados.

Esto es una propuesta de extensión, **no funciones ya construidas**. Los nombres de campos nuevos, el comando de pausa y la vista ampliada requieren implementación y pruebas propias. No hay scheduler activo que detecte bloqueos o despache por sí solo.

## Cuándo avanzar, corregir o dejar en espera

- **Avanzar:** aceptación vigente, material suficiente, herramientas probadas, rutas libres, cuota y autorización aplicables. No pedir otra vez permiso para la misma acción ya autorizada.
- **Corregir en la misma tarea:** la revisión detecta un error dentro de su alcance. Conservar el veredicto, reabrir, reanudar el mismo SID, corregir y volver a revisar el nuevo commit.
- **Poner en espera:** acceso o decisión indispensables; herramienta incompatible; falta de cuota; fuente no recuperable tras alternativas razonables; repetición del mismo fallo sin cambio de condiciones. Guardar qué se intentó, resultado, evidencia, qué desbloquea, quién debe hacerlo y siguiente comando.
- **Abrir una dependencia:** arreglar una herramienta o infraestructura compartida requiere un objetivo y rutas diferentes. La investigación original espera; la corrección tiene su propio ID y revisión. No reasignar una ruta mientras su escritor siga vivo.
- **Parar de inmediato:** pedido de Sergio, acción fuera de permisos, riesgo real de exponer secretos, modificación de producción no autorizada o resultado externo incierto donde repetir pueda duplicar efectos. Preservar el trabajo y reconciliar antes de reintentar.
- **Terminar:** aceptación demostrada, veredicto independiente bueno para el commit exacto, integración comprobada y hash en `origin/master`. Un PID muerto o `rc=0` no basta.

Se propone un límite inicial de dos intentos de una misma hipótesis fallida; un tercero necesita datos o condiciones nuevas y debe registrarse. Es un límite operativo propuesto, no una garantía impuesta hoy por código. Una fuente fallida no obliga a detener todo si existe una alternativa pública válida dentro del encargo.

## Comandos que ya existen

Los ejemplos siguientes son plantillas, no lanzamientos realizados. Sustituir `ID`, `N`, `ACTOR` y las rutas con el registro actual. Cada mutación incrementa la revisión: consultar antes de la siguiente.

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
T=_investigacion-onia/base-operativa/05-herramientas/scripts/trabajo.py
python3 "$H" estado
python3 "$H" retomar ID
python3 "$H" historial ID
```

Preparar y asignar no ejecutan un LLM; `--perfil` guarda una recomendación, **no configura el runtime**:

```bash
python3 "$H" preparar ID --compartible --area desarrollo --perfil complejo \
  --objetivo "Objetivo observable" --entregable "Entrega concreta" \
  --aceptacion "Criterios verificables"
python3 "$H" asignar ID --revision-esperada N --responsable ACTOR \
  --ruta 05-herramientas/RUTA-EXCLUSIVA
python3 "$H" lanzar ID --revision-esperada N --actor ACTOR --si-sergio \
  --modelo gpt-6.1-sol --esfuerzo high --auth-chatgpt --subagentes-maximos 1
```

El último comando sólo corresponde cuando el lanzamiento esté autorizado. El harness fija por proceso el modelo/esfuerzo predeterminados de los hijos iguales a los del ejecutor; no tiene hoy una opción CLI distinta por cada hijo. Un spawn explícito puede especificar modelo/esfuerzo cuando esté autorizado y sea compatible con ese runtime; igualmente debe verificarse el resultado. La [documentación de subagentes](https://learn.chatgpt.com/docs/agent-configuration/subagents) distingue herencia y valores explícitos; los hijos también consumen recursos y cuota.

Registrar espera **después de comprobar el checkpoint y que el proceso ya terminó**:

```bash
python3 "$T" actualizar ID --revision-esperada N --actor ACTOR \
  --estado en_espera --resultado "Trabajo preservado; falta DEPENDENCIA" \
  --comprobacion "Checkpoint y procesos comprobados; evidencia registrada" \
  --siguiente "Resolver DEPENDENCIA y reanudar el mismo SID"
```

Este comando sólo registra estado. No es una señal de pausa. Aplicarlo a una entrega cerrada/revisada limpia los campos vigentes de cierre/revisión; no usarlo para cambiar etiquetas por comodidad. Conservar sus recibos e historial.

```bash
python3 "$H" reanudar ID --revision-esperada N --actor ACTOR --si-sergio
python3 "$H" cerrar ID --revision-esperada N --actor ACTOR \
  --resultado "Entrega publicada" --comprobacion "Resultados concretos de las pruebas"
python3 "$H" revisar ID --revision-esperada N --actor ACTOR \
  --revisor OTRO-REVISOR --si-sergio --modelo gpt-6.1-sol \
  --esfuerzo ultra --auth-chatgpt
python3 "$H" revisar ID --recoger --revision-esperada N
python3 "$H" aceptar ID --revision-esperada N --revisor OTRO-REVISOR \
  --criterio "Todos los criterios cotejados con esta entrega"
```

`reanudar` hereda modelo/esfuerzo/límite de hijos si se omiten. El revisor ocupa uno de los tres cupos principales, es read-only y tiene delegación deshabilitada aun cuando se solicite ultra. La integración y verificación de `origin/master` siguen después de aceptar; no están implícitas en ese comando.

La ficha recomendada/solicitada/observada ya puede guardarse con `trabajo.py ejecucion ID --revision-esperada N --actor ACTOR --ficha RUTA-JSON`. Su fuente observada debe ser evidencia saneada real, con integridad comprobada; no rellenarla sólo copiando `--modelo`.

## Cómo trabajar juntos sin saturar contexto

Un chat coordinador por proyecto, IDs por entregable y una sola autoridad de escritura de los registros. Sergio aporta objetivo y decisiones; Boss prioriza y prepara el encargo; el coordinador verifica y despacha; cada ejecutor tiene una tarea/worktree y el revisor otro SID. Los chats de otras áreas pueden proponer cambios, pero el coordinador reconcilia la revisión canónica antes de mutar.

Cada encargo debe incluir: «Quiero RESULTADO; usá ENTRADAS; escribí en RUTAS; está bien cuando CRITERIOS; tenés PERMISOS; no hagas LIMITES; depende de IDS; parate si CONDICION». Para continuar, basta ID + commit y la pregunta/decisión nueva. No pegar toda la historia de la empresa ni mantener una sesión indefinida para todas las áreas.

Usaría normalmente **dos ejecutoras y un cupo de revisión**, según independencia y capacidad, hasta el máximo actual de tres principales. Un hijo sólo para una parte separable, archivo exclusivo y modelo explícito cuando importe; no un árbol ilimitado. Dos tareas que comparten perfil autenticado, credenciales, sistema externo o archivo no son independientes sólo por tener worktrees distintos.

Es realista automatizar preparación, investigación con fuentes accesibles, documentos, código acotado y comprobaciones repetibles. Una empresa completamente autónoma 24/7 todavía requiere scheduler, idempotencia, supervisión, recuperación y permisos por servicio, probados de punta a punta. Hoy no están implementados por el hecho de disponer del harness. Medir aceptación al primer intento, retrabajo, fallos críticos, tiempo hasta entrega, espera por dependencias y cuota fechada; no valorar el sistema por número de agentes abiertos.

## Evidencia revisada

- `AGENTS.md`, `reglas-comunes.md`, `ORQUESTACION.md`, `orquestacion.json`, `EMPRESA-UNIPERSONAL.md` y contexto pertinente de `ESTADO.md`/`boss-memoria.md`.
- `harness.py`: preparación y CLI; `trabajo.py`: estados, fichas, asignación y revisión esperada; `harness_sesiones.py`: argumentos efectivos, retoma, límite y supervisor.
- `05-herramientas/evaluacion-av/2026-11-08/sesiones-inventariadas.json`, contrastado con los rollouts del 8/11 para los cuatro padres y veinte hijos identificados.
- `~/.codex/models_cache.json`: sólo modelo, modalidad, esfuerzo y fecha. No se incluye identidad/ETag ni configuración de autenticación.
- Estado B consultado en el host mediante helper de lectura; no se ejecutaron sus ramas de cierre/revisión.
- Documentación oficial abierta: https://learn.chatgpt.com/docs/models ; https://learn.chatgpt.com/docs/model-selection ; https://learn.chatgpt.com/docs/agent-configuration/subagents .

Límite de esta auditoría: inspección y propuesta, sin nuevas pruebas con modelos ni implementación del control propuesto. Algunas lecturas combinadas iniciales truncaron la salida; se recuperaron por separado los archivos y bloques necesarios para las afirmaciones sobre modelos y runtime. No se interpretó el texto truncado como evidencia completa.

## Actualización al publicar este informe

B terminó naturalmente y publicó `493bbb78e447e8a456262f5d4f39470124dcd9af`, confirmado por ls-remote. Matriz: Erik5 y Enrique/Ali/San/Cormac/Bastian4 cada uno,25 total;118 enlaces locales y cero errores formales en el control del coordinador. Quedó `en_espera` de revisión independiente, sin aceptación ni integración de la entrega a master. No se la interrumpió ni se lanzó revisor.

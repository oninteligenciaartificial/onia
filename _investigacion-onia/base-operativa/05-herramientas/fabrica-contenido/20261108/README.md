# Entrega: fábrica de ideas y guiones OnIA

Diseño y ensayo offline listos para revisión del coordinador. Sin implementación de ingestión real, panel conectado, Telegram o scheduler. Dos guiones ficticios recorridos hasta revisión individual y decisión simulada: A elegido para preparar; B devuelto para cambiar su CTA. Ninguna decisión real de Sergio ni revisión independiente del encargo se acredita con este ensayo.

- [Diseño, plan y fuentes](DISENO.md): extensión del registro/harness existentes, proyección del panel y propuesta de recurrencia pendiente de sí.
- [Contrato de datos y Telegram](CONTRATO.md): identidad privada, versiones, idempotencia, confirmación y matriz de cobertura.
- [Fixture legible](fixture.json): cinco entradas inventadas, dos ideas, dos guiones completos, patrones y límites, revisiones y decisiones simuladas.
- [Resultado final de seis controles](ensayos/ejecucion-02/resultado.json) y [boceto estático](ensayos/ejecucion-02/panel.html).
- [Registro aislado de ficción](ensayos/ejecucion-02/04-operacion-agentes/tareas/ficcion-fabrica-001.json), creado desde cero por las APIs existentes. No es copia de la tarea canónica del encargo ni otra cola operativa.

## Reproducir desde la raíz del worktree

Sólo Python estándar ya presente. Usar una carpeta nueva para conservar resultados anteriores:

```bash
python3 _investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261108/ensayo.py \
  --salida _investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261108/ensayos/reproduccion-01
```

Salida esperada: `resultado=OK`, `casos=6`. Crea artefactos, JSON aislado revisión 12, HTML y recibo de resultados. Repetir con el mismo destino se rechaza; elegir otro nombre, sin borrar. La salida sólo puede estar bajo `ensayos/` de esta carpeta. No hay dependencias nuevas, llamadas LLM, clientes Telegram, servidor ni comandos del lanzador de sesiones. Durante el recorrido se bloquea `socket.socket` para detectar uso accidental de red.

El ensayo importa `trabajo.py` existente y llama `create`, `update`, `decide`, `read_task` y `verify`. Su base es la nueva carpeta de ejecución; nunca usa `trabajo.BASE` como destino. Como el API normalmente elimina su lock temporal al salir, el ensayo intercepta **únicamente** ese `unlink` para archivarlo mediante `rename` en `locks-conservados/`: mantiene la creación exclusiva del lock y el resto de controles originales. Cualquier otro borrado se rechaza. Es una adaptación de preservación para esta prueba monoproceso, no una modificación de producción ni una prueba de concurrencia distribuida. Los archivos archivados son recibos de locks ya liberados, no bloqueos activos. Las escrituras atómicas normales del JSON de prueba sí avanzan su revisión y conservan historial.

## Evidencia y límites comprobados

Ejecución final `ejecucion-02`: seis controles correctos sobre el código entregado. El recibo conserva hashes del fixture y `trabajo.py`. `ingesta.json` deja dos fuentes utilizables, un duplicado enlazado, una fuente sin fecha pendiente y un fallo inyectado. Las aserciones cotejan fechas completas, procedencia por bloque, patrón y autoría propia de todas las ideas/guiones. Revisiones y decisiones se vinculan al hash de cada guion.

Los rechazos de revisión obsoleta, decisión en `para_revision`, decisión duplicada y evidencia con hash alterado en memoria comprueban que los bytes del registro no cambian. No se altera la evidencia real ni se recalcula un hash para ocultar cambios. La tarea termina `para_revision`, `aceptacion=null`, con dos decisiones editoriales ficticias. No se llama a `aceptar` ni se inventan sesiones revisoras.

Un primer checkpoint `ejecucion-01` pasó cinco controles antes de añadir fechas explícitas de revisión/decisión y el control negativo de integridad. Se conserva completo como evidencia intermedia; su hash de entrada corresponde a la versión previa, no al fixture actual. Para reproducir y verificar esta entrega usar `ejecucion-02`, cuyo recibo final corresponde al fixture actual. No se borraron archivos del encargo. No se ejecutó toda la suite del harness porque no se cambió su código: se comprobó el recorrido pertinente por sus APIs.

El HTML se revisó como archivo fuente y proyección; no se afirma prueba visual en navegador, autenticación, uso móvil ni despliegue. Las comprobaciones de identidad Telegram, replay de transporte, nonce, envío incierto y conflictos entre máquinas permanecen en contrato. El fixture no consulta noticias actuales. Euge Oller queda pendiente de evidencia visual del coordinador; no se atribuyen prácticas ni visionado.

## Continuación concreta

El coordinador puede cerrar y lanzar su revisión independiente sobre el commit publicado en `codex/ws-fabrica-contenido-diseno-20261108`. Esta ejecutora no integra `master`, no modifica el JSON/briefing real y no abre otra tarea. La aceptación e integración quedan al coordinador. Si Sergio aprueba una siguiente etapa, delimitar implementación del lector privado y adaptador de Telegram en una tarea del harness con sus propios accesos, rutas y pruebas; el scheduler requiere aprobación aparte antes de construirse.

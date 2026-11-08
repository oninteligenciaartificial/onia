# T006 · Dictamen independiente

**ACEPTAR documentalmente T005, condicionado a incorporar las CORRECCIONES exactas indicadas abajo.** La aceptación queda pendiente de esa incorporación. No encontré un defecto sustancial que exija rehacer la investigación.

El informe conserva las seis áreas, distingue evidencia técnica y comercial, y declara faltantes. Sus principales ajustes son actualizar el cierre, explicitar el coste temporal de las prioridades y delimitar el lock.

## Hallazgos del contraste

| Área | Resultado de la revisión |
|---|---|
| Marketing | Confirmada la ampliación documental a 17 personas y Voltra, con aceptación de Jefa pendiente. La síntesis respeta los límites de acceso y evita atribuir ventas. |
| Video | Confirmada la aceptación visual/verbal acotada. Percepción temporal y acústica integrales siguen abiertas. El render técnico de seis segundos y D1 mantienen alcances separados. |
| Desarrollo | ESTADO respalda las pruebas históricas de continuidad y las cifras 54/54 y 74 aprobadas con una omisión. T005 las atribuye a sus versiones y entornos. |
| Automatizaciones | Confirmados workflow inactivo, 13/13 controles estáticos e integración pendiente. Las pruebas PostgreSQL históricas tienen alcance propio. |
| Organización | Confirmada la estructura histórica de Sergio·Hoy, con vistas, avisos, móvil y sincronización incompletos o sin comprobar. |
| Producto | Confirmado el snapshot histórico y las seis tareas propuestas. El E2E integrado sigue pendiente. El desfase de QA conserva su clasificación estática. |

Fuentes originales contrastadas por área. [Marketing](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/marketing/ESTADO.md:2), [Video](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audiovisual/ESTADO.md:3), [Desarrollo](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/ESTADO.md:11), [Automatizaciones](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-05/n8n-reserva-local/README.md:37), [Organización](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/PANEL-DIARIO.md:3), [Producto](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/fuentes-cloud/producto.md:13).

### Estados y decisiones

- **Declarado frente a verificado.** T006 verificó contenido documental y presencia de archivos. Las pruebas históricas siguen atribuidas a sus reportes. El ensayo workshop fue textual e interno. La guía exige generación propia, desempeño de ambos principiantes y recuperación del paquete para acreditar el ensayo humano. [Guía](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/tanda-01/workshop-ensayo.md:56)
- **Decisiones del 7 de noviembre.** El encargo actual prevalece sobre repartos históricos de modelos, subagentes y paralelismo. T005 aplica correctamente Codex Sol, ejecución manual secuencial y exclusión de fallback y gastos. [Encargo](/home/onia-codex-worker/operacion/encargos/RECONCILIAR-OPERACION.md)
- **Cierre desactualizado.** El informe describe correctamente su momento de producción, pero su relevo ya quedó superado. Ahora existen el resultado, rc0, T005 en `hechas` y T006 en `en-curso`. [Estado T005](/home/onia-codex-worker/operacion/resultados/T005-estado.json), [registro](/home/onia-codex-worker/operacion/registro.tsv)
- **Top 3.** El orden resulta razonable por información económica faltante, activos recuperados y dependencias. Falta explicitar el tiempo. La guía ya presupone 130 minutos de Sergio para el ensayo workshop, sin medición humana que confirme esa estimación. [Presupuesto del ensayo](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/tanda-01/workshop-ensayo.md:11)

## CORRECCIONES exactas

Incorporar como anexo posterior a T005, conservando su corte histórico.

### 1. Estado de cierre y persistencia

> **Actualización de cierre contrastada en T006.** T005 terminó con rc0, figura en tareas/hechas y su resultado está disponible en `/home/onia-codex-worker/operacion/resultados/RECONCILIACION-ONIA-20261107.md`. El lote conserva evidencia en `resultados/T005-RECONCILIACION.txt.UWDpnK/`. Al consultar T006 había siete archivos en hechas y T006 en curso. Las referencias anteriores a T005 activa, seis hechas y guardado pendiente describen el corte previo al cierre del wrapper. Estos estados son técnicos/documentales. La aceptación documental de T006 queda condicionada a incorporar sus correcciones.

### 2. Justificación temporal y económica del top 3

> **Orden definitivo de propuestas.**  
> 1. Establecer brecha de cobros y oportunidades mediante un resumen mínimo aportado por Sergio. Su utilidad es reducir la incertidumbre económica antes de comprometer preparación. El tiempo depende del volumen y calidad de esos datos y sigue sin estimar.  
> 2. Elegir una entrega y validar capacidad. El workshop dispone de materiales y rúbrica. Su guía presupone 130 minutos de Sergio para dos ensayos y preparación/revisión, sin tiempos humanos medidos. El acompañamiento 1:1 mantiene capacidad y condiciones pendientes. La elección depende del corte económico y de disponibilidad real.  
> 3. Cotejar el recorrido manual de confirmación, conciliación, entrega y cierre. Depende de la entrega elegida y de sus condiciones. Su duración sigue sin estimar. Puede reutilizar el procedimiento existente sin esperar la integración de n8n o Platform.  
> El orden es un juicio documental por utilidad, tiempo y dependencias. No permite proyectar ventas, precio, número de participantes ni cumplimiento de Bs 3.000 al 14 de noviembre.

### 3. Lock, app y alcance de las comprobaciones

> **Límite de concurrencia y verificación.** El lock protege las ejecuciones que lo utilizan. No cubre automáticamente la app ni otras entradas. Para este lote, la app inactiva es una condición declarada por Sergio. No se acredita aislamiento total ni operación 24/7. T006 contrastó fuentes documentales, archivos de resultado y estados locales. HEAD y limpieza Git se atribuyen a la comprobación previa de T005 y sus recibos, sin nueva ejecución Git en T006.

## Límites de esta revisión

La comprobación fue acotada a fuentes pertinentes. Algunas salidas extensas quedaron truncadas y se hicieron consultas posteriores por tema. La profundidad por área permanece parcial.

Persisten los faltantes declarados de chats originales, medios/editables, estado actual de apps, checkout actual de Platform, ensayo humano, cartera, demanda y cobros conciliados. ONIA-CENTRAL permaneció excluido. La comparación de doce exportaciones conserva su alcance documental. [Comparación previa](/home/onia-codex-worker/operacion/resultados/CHECKOUT-VERIFICACION-20261107.json)

No ejecuté `./ejecutar.sh --comprobar` durante el lote activo. El manual sitúa esa comprobación cuando no hay trabajo activo. Esta revisión utilizó lectura y análisis, sin escritura propia, scripts del repo ni nuevas invocaciones de modelos. El wrapper debe persistir esta respuesta. [Manual](/home/onia-codex-worker/operacion/resultados/MANUAL-SERGIO-VPS-20261107.md:21)

## RESUMEN EJECUTIVO

**Top 3 definitivo**

1. Conocer brecha real de cobros y oportunidades.
2. Elegir una entrega y validar capacidad y tiempo.
3. Cotejar su recorrido manual de conciliación, entrega y cierre.

**Decisión material.** Aceptar documentalmente T005 tras incorporar las tres correcciones. Sergio debe elegir el próximo encargo. Se mantiene la propuesta de comenzar por el corte económico mínimo.

**Cobertura.** Contrastadas las seis áreas mediante estados originales, snapshots, guía workshop, preparación n8n, panel y recibos locales. Continúan pendientes los materiales y verificaciones señalados arriba. No hay evidencia recuperada que acredite la meta comercial.

## RELEVO LOCAL

- **Repo canónico** `/home/onia-codex-worker/repos/onia`.
- **HEAD documentado** `e55812ce1bc8ef798fb370257ba887d07acccc53`, rama `master`, limpio según comprobación previa. Sin nueva verificación Git en T006.
- **Operación local** `/home/onia-codex-worker/operacion`. Sus registros y resultados conservan el relevo local separado del repo canónico.
- **Producción** [T005 reconciliación](/home/onia-codex-worker/operacion/resultados/RECONCILIACION-ONIA-20261107.md), rc0 y tarea en `hechas`.
- **Revisión** T006 devuelve este dictamen en texto. Persistencia y cierre corresponden al wrapper. Aceptación condicionada a incorporar las correcciones.
- **Siguiente encargo propuesto** corte documental de brecha y oportunidades con datos mínimos que Sergio aporte, después de su elección. Queda sin ejecutar.

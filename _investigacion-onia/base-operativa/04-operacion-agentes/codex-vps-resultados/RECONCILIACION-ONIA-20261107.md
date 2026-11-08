# Reconciliación de OnIA · 7 de noviembre de 2026

## 1. Resumen real

La documentación recuperable describe una empresa unipersonal apoyada por IA, con formación, contenido, servicios y ONIA Platform. Hay activos documentales, pruebas técnicas y recorridos parciales. **Los nuevos cobros conciliados hacia la meta de Bs 3.000 al 14 de noviembre siguen desconocidos.**

| Estado | Situación sustentada |
|---|---|
| Listo para consulta | Checkout de `onia`, documentación operativa, materiales de ensayo, borradores editoriales y entregas técnicas conservadas. |
| Comprobado en esta revisión | Rama `master`, HEAD `e55812ce1bc8ef798fb370257ba887d07acccc53` y `git status --porcelain` sin salida. |
| Comprobado documentalmente | T003 produjo inventario, T004 lo aceptó técnicamente y la retoma de T003 terminó correctamente. El anexo posterior registra SSH desde Windows probado. |
| En curso | T005, esta reconciliación. El registro contiene su inicio y la tarea está en `tareas/en-curso/`. Su cierre corresponde al wrapper. |
| Pendiente | Elección de prioridad por Sergio, revisión independiente T006, validación humana del workshop y condiciones comerciales. |
| Bloqueado para integración | n8n requiere destino de ensayo aislado y alcance específico. Platform requiere su checkout e instrucciones actuales y un entorno autorizado. |
| No comprobado | Demanda, ventas, cobros, capacidad semanal, aprendizaje humano, operación empresarial E2E, funcionamiento 24/7 y uso efectivo de la app Windows. |

Las seis tareas en `hechas` corresponden a ejecuciones técnicas/documentales. T005 es la única tarea encontrada en curso. [Registro local](/home/onia-codex-worker/operacion/registro.tsv), [pruebas manuales](/home/onia-codex-worker/operacion/resultados/PRUEBAS-OPERACION-MANUAL-20261107.md)

## 2. Matriz de las seis áreas

Las rutas abreviadas de esta sección parten de `/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/`.

| Área y utilidad | Tareas y entregas recuperadas | Estado declarado y alcance verificable | Bloqueos, dependencias y solapamientos |
|---|---|---|---|
| **Marketing**. Convertir atención en una solicitud pertinente y una oferta entregable. | Perfil/destino del kit, primera grabación, revisión editorial, recorrido comentario→entrega y registro de resultados, MP-M01–05. Ficha, ensayo, pago manual, acceso/clase y seguimiento, WS-W01–05. Existen 35 borradores y una ampliación de referentes con mapa de 18 entidades. | Los guiones siguen pendientes de grabación/aprobación. La investigación comercial declara ampliación entregada para 17 personas y Voltra, con aceptación de Jefa pendiente. Se verificó la existencia de sus estados y backlog documental. No hay cartera vigente ni cobros recuperados. | Identidad, destino, capacidad y condiciones requieren decisiones de Sergio. Ads pausados. MP-M04 depende de Automatizaciones. Kit, landing y ficha aparecen en varios documentos y deben conservar un único alcance. Cobertura comercial actual parcial. |
| **Video**. Producir una demostración comprensible y reutilizable. | Pieza inicial antes de escalar a cinco diarias, guiones, montaje HyperFrames, recursos Higgsfield y exploración 3D. D1, pruebas de render, análisis visual/verbal y controles de audio. | TANDA-01 registra render técnico Windows de 6 s. PLAN registra un D1 posterior silencioso. El estado audiovisual más avanzado declara unidad visual/verbal aceptada con límites, corpus de 40 medios y 8 imágenes, y estudio integral abierto. Audio documenta ASR parcial y candidatos rechazados por fallar controles. | Falta aceptación temporal/acústica integral. Fotogramas y ASR tienen cobertura parcial. No se verificaron medios ni capacidad del worker para renderizar. Saldo Higgsfield de 585 créditos es histórico. Investigación, piloto técnico y pieza comercial son entregas distintas que aparecen superpuestas. |
| **Desarrollo**. Sostener herramientas y recuperación comprobable. | Harness, continuidad A→Git→B, evaluación de sesiones, web W1, dashboard, apoyo audiovisual y launcher remoto. | ESTADO conserva aceptación técnica histórica A→B, 54/54 pruebas en una versión y 74 aprobadas más una omisión Windows en otra. TANDA-01 documenta W1 probada en escritorio/móvil como copia privada. El worker actual tiene lectura/análisis y retoma acreditados documentalmente. | W1 carece de despliegue y checkout comercial comprobados. Dashboard con datos reales y endpoints sigue pendiente. Launcher conserva antecedente 401. Las pruebas Cloud/Windows pertenecen a sus versiones y entornos. Harness, runner manual y panel requieren estados separados. |
| **Automatizaciones**. Tratar eventos y evitar efectos duplicados o inciertos. | Piloto IG/DM, reserva transaccional TR-CLAIM, CRM, radar, STOP, takeover y conciliación. Bundle local recuperable con workflow inactivo y matriz futura. | Piloto histórico registra casos secuenciales aprobados y carrera Get+Insert con duplicados. La preparación local declara 13/13 controles estáticos. Las 15 pruebas PostgreSQL corresponden a un componente histórico. Integración runtime pendiente. | Requiere PostgreSQL exclusivo de ensayo, referencia de credencial restringida, aislamiento y administrador responsable. Pendientes carrera, reinicio, conflicto, STOP/takeover y efectos inciertos. Comentarios, DM y WhatsApp tienen contratos propios. Se solapa con MP-M04, radar y launcher. |
| **Organización**. Mantener prioridades, compromisos, caja y relevo. | Sergio·Hoy, panel diario, agenda, resultados, aprendizaje, integración y revisión. Continuidad local mediante LEEME, registro, tareas y resultados. | PANEL-DIARIO registra estructura Notion revalidada históricamente, con vistas/avisos incompletos. TANDA-01 atribuye conservación de 20 IDs y 35 borradores. El estado local actual permite recuperar T003/T004 y sus límites. | No se consultaron Notion ni Calendar actuales. Seis eventos antiguos fueron eliminados y carecen de reemplazo confirmado. Apariencia móvil, sincronización y avisos siguen sin acreditar. Panel, radar, caja y registro comercial deben referenciar los mismos hechos para evitar duplicados. |
| **Producto**. Conseguir un recorrido utilizable y conservado tras pagar. | P01 fijar candidato/aislamiento, P02 alta dental y reentrada, P03 QR estático/comprobante, P04 QR dinámico simulado condicional, P05 negativos de correo y P06 demostración con promesa separada. | Snapshot de Platform identifica SHA histórico `a0488f04200b14c95caf0013043716b16efa1f1d`, rutas y tests existentes. TANDA-01 añade validador sintético y reproducción documental del harness. No hay E2E aceptado alta→primer resultado→suscripción→reentrada. | Repo de Platform separado y sin lectura actual en este encargo. El antecedente señala clone bloqueado por proxy y Docker denegado. Existe desfase estático en QA de checkout, sin fallo productivo reproducido. Cobro de paciente, suscripción y aprendizaje del workshop necesitan aceptación separada. Cobertura parcial. |

**Fuentes por área**

- Marketing y ventas. PLAN §§2, 4–5, backlog MP/WS y estado de investigación. [Backlog conservado](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/fuentes-cloud/workshop-ensayo.md:119), [estado Marketing](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/marketing/ESTADO.md)
- Video. PLAN §3, TANDA-01 y estados audiovisual/audio. [TANDA-01](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/tanda-01/README.md), [estado Video](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audiovisual/ESTADO.md), [estado audio](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/investigacion/2026-11-05-referentes/audio-tecnico/ESTADO.md)
- Desarrollo y continuidad. PLAN §7, ESTADO y contrato del harness. [ESTADO](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/ESTADO.md), [CONTINUIDAD](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/cloud/CONTINUIDAD.md)
- Automatizaciones. PLAN §6 y preparación transaccional. [Reserva n8n](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-05/n8n-reserva-local/README.md)
- Organización. PLAN §§9–10 y diseño del panel. [PANEL-DIARIO](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/PANEL-DIARIO.md)
- Producto. PLAN §8 y snapshot de tareas/aceptación. [Producto](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/fuentes-cloud/producto.md)

### Integradora, revisora y aprendizaje

Los roles históricos de Jefatura, Aprendizaje y Reels complementan las seis áreas CLI. ORQUESTACION mantiene seis claves y perfiles declarativos. La decisión actual exige una ejecución secuencial con Codex Sol y revisión separada cuando corresponda. T004 revisó T003. T006 permanece pendiente para T005.

Aprendizaje conserva currículo, fuentes y ejercicios sintéticos. La comprensión y práctica de Sergio requieren evidencia humana. El harness prepara y recupera encargos. El nuevo worker acredita un circuito manual acotado de lectura, revisión y retoma. Ninguna de estas evidencias acredita servicio empresarial permanente. [ORQUESTACION](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/ORQUESTACION.md), [manifiesto](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/orquestacion.json), [pruebas del worker](/home/onia-codex-worker/operacion/resultados/PRUEBAS-OPERACION-MANUAL-20261107.md)

## 3. Decisiones vigentes, historia y discrepancias

| Asunto | Historia o discrepancia | Reconciliación al 7 de noviembre |
|---|---|---|
| Modelos y coordinación | PLAN y reglas comunes conservan repartos, subagentes y paralelismo. El manifiesto propone varios modelos. | Prevalece Codex `gpt-6.1-sol`, una tarea y revisión secuencial. Claude excluido, sin fallback, API facturada ni gastos. |
| Acceso GitHub | PLAN-RECUPERADO-v2 conserva T002 pendiente y ausencia de checkout. | El registro posterior declara T002 completada. Esta revisión observó directamente HEAD, rama y checkout limpio. |
| Retoma | T004 y una parte de LEEME todavía describen la tercera llamada como pendiente. | T003-estado y PRUEBAS posteriores registran retoma completada. |
| Windows | Primeras secciones del manual describen SSH del worker pendiente. | Anexo de 13:09 registra autorización y prueba SSH satisfactoria. La interfaz real de la app y su listado de sesiones siguen sin comprobarse. |
| Prioridad | PLAN destaca terminar referentes y probar audio. T003 propone continuar workshop. | Este encargo exige reconciliar y presentar opciones. Ninguna cola histórica queda activa por su posición en un documento. |
| Referentes | El plan recuperado conserva nuevos referentes como registrados y sin analizar. | El estado Marketing posterior documenta ampliación comercial/social para 17 personas y Voltra. Persisten límites de aceptación, audiovisual y acceso privado. |
| D1 | TANDA-01 registra composición sin MP4. PLAN registra piloto silencioso posterior. | Son cortes sucesivos. La lectura actual confirma esos registros, sin inspección de medios ni aceptación audiovisual integral. |
| Workshop | Hay tiempos y condiciones de versiones anteriores. | Precio, fecha, duración, cupo y soporte siguen por decidir. La guía posterior exige dos principiantes y desempeño observable. |
| Estado técnico | Seis tareas hechas y pruebas históricas del harness. | Acreditan ejecuciones y capacidades acotadas. El importe comercial alcanzado sigue desconocido. |

La guía del workshop registra seis respuestas internas del agente. El criterio humano exige que ambos participantes alcancen autonomía en los cuatro criterios críticos, generen sus propias salidas y recuperen el paquete desde celular. Los formularios de preparación y la revisión técnica carecen de resultados humanos registrados. [Guía y rúbrica](/home/onia-codex-worker/repos/onia/_investigacion-onia/base-operativa/continuidad/2026-11-04/tanda-01/workshop-ensayo.md:56)

Estas discrepancias requieren conservar la procedencia y usar la evidencia posterior para el estado actual. El repositorio mantiene la autoridad documental del sistema. Las decisiones actuales de Sergio determinan el alcance de este encargo.

## 4. Tres próximos resultados propuestos

**Ninguno se ha iniciado.** El orden siguiente es una propuesta por cercanía a cobros verificables, activos existentes y dependencias conocidas.

### 1. Brecha comercial y oportunidades recuperables hasta el 14

**Resultado propuesto.** Un corte mínimo que permita saber cuánto se ha cobrado realmente, qué oportunidades existen y qué entrega podría completarse dentro del plazo.

- **Utilidad.** Evita elegir un formato sin conocer demanda, compromisos ni brecha real.
- **Evidencia disponible.** Meta Bs 3.000, criterios de conciliación y registro manual propuesto. Falta cartera vigente y evidencia de ingresos.
- **Dependencia.** Sergio aporta un resumen legítimo y mínimo de cobros, solicitudes y compromisos. No requiere compartir credenciales.
- **Primer paso permitido tras su elección.** Revisar los datos que Sergio entregue y separar solicitado, reservado, entregado, cobrado e incierto.
- **Aceptación.** Cada cobro incluido tiene fecha, importe y confirmación del responsable. Lo desconocido permanece identificado. Si no hay oportunidades recuperables, queda registrado.

### 2. Una vía de entrega elegida con evidencia de capacidad

**Resultado propuesto.** Elegir workshop reducido, acompañamiento 1:1 u otra entrega ya recuperada, y cerrar la principal incertidumbre que impida ofrecerla.

- **Utilidad.** Concentra el esfuerzo en una promesa que Sergio pueda cumplir.
- **Evidencia disponible.** El workshop tiene materiales y rúbrica más desarrollados. El 1:1 aparece como alternativa con capacidad/precio pendientes. Platform acumula dependencias técnicas mayores.
- **Dependencia.** Resultado 1, disponibilidad de Sergio y elección explícita. El ensayo humano requiere actuación personal y autorización aplicable.
- **Primer paso permitido tras su elección.** Preparar el encargo acotado de validación usando materiales existentes. Si elige workshop, registrar generación propia, ayuda, errores, tiempos y recuperación móvil de los dos principiantes.
- **Aceptación.** Capacidad observada y límites registrados antes de adoptar condiciones. La prueba educativa conserva su alcance aunque todavía no haya demanda.

### 3. Recorrido manual verificable de confirmación, entrega y cierre

**Resultado propuesto.** Tener un único procedimiento que una solicitud, conciliación, acceso, entrega y soporte limitado.

- **Utilidad.** Permite convertir una oportunidad elegida en una entrega trazable sin esperar todas las automatizaciones.
- **Evidencia disponible.** WS-W03–05, simulación de pago pendiente/duplicado/incierto y registro mínimo.
- **Dependencia.** Oferta y condiciones decididas, capacidad observada y autorizaciones comerciales específicas.
- **Primer paso permitido tras su elección.** Cotejar el procedimiento existente y realizar un pase documental con datos ficticios.
- **Aceptación.** Solicitud única, confirmación sustentada, material recuperable, duplicados controlados y soporte delimitado. La operación real y sus cobros requerirán evidencia propia.

No hay base para calcular alumnos, precio o volumen necesario a partir de los documentos recuperados.

## 5. Continuidad recuperable

| Ubicación | Qué conserva | Límite |
|---|---|---|
| Repo `onia`, HEAD observado | Reglas, plan, capacidades declaradas, orquestación, snapshots y evidencia saneada. | Platform tiene repositorio separado. Los medios permanecen en sus almacenes de origen. |
| `operacion/LEEME.md`, `registro.tsv`, `tareas/` | Entrada local y transiciones del runner. | Hay frases históricas superadas por anexos y resultados posteriores. |
| `resultados/T003-estado.json` | Estado técnico de T003, revisión y retoma. | Su siguiente propuesto carece de prioridad automática frente a este encargo. |
| Manual y pruebas manuales | Operación acotada, lock, timeout configurado, revisión y recuperación por ID. | Vencimiento real del timeout, UI Windows y actividad prolongada sin prueba. |
| `fuentes-plan/` e índice | Doce exportaciones documentales y procedencia. | Cobertura de documentos, sin chats completos. |

La recuperación documental puede hacerse desde esos archivos sin depender del texto íntegro de este chat. Depende de conservar acceso a los archivos y a la revisión correcta.

La continuidad de sesiones depende además de identidad, acceso, compatibilidad y cuota disponible. La cuota restante es desconocida. Los medios, estados actuales de apps y documentación de Platform requieren sus fuentes y permisos respectivos. [Estado T003](/home/onia-codex-worker/operacion/resultados/T003-estado.json), [manual](/home/onia-codex-worker/operacion/resultados/MANUAL-SERGIO-VPS-20261107.md), [índice de exportaciones](/home/onia-codex-worker/operacion/fuentes-plan/INDICE-FUENTES.json)

## 6. Matriz de fuentes, cobertura y desconocidos

| Fuente consultada | Cobertura de esta revisión | Qué queda fuera |
|---|---|---|
| AGENTS raíz/base, reglas comunes, PLAN, ESTADO, ORQUESTACION y manifiesto | Autoridad, programas, seis áreas, roles y límites. | No se ejecutaron scripts ni pruebas del repo. |
| Índices del 4/11 y TANDA-01 | Inventario de snapshots y avances parciales por área. | Sin auditoría completa de todos los anexos históricos. |
| Estados Marketing, audiovisual y audio técnico | Avances posteriores que corrigen resúmenes antiguos y declaran límites. | Sin abrir medios, logs brutos ni repetir inferencias. |
| Snapshot Producto | Seis tareas y puertas de aceptación. | Sin checkout actual de Platform, runtime, clientes ni pagos. |
| README de reserva n8n | Preparación inactiva, controles estáticos y requisitos de integración. | Sin instancia, DB, credenciales ni ensayo runtime. |
| PANEL-DIARIO y contrato de continuidad | Diseño del panel, fuente de estado y recuperación. | Sin lectura actual de Notion, Calendar o móvil. |
| Resultados prioritarios del 7/11 y anexos Windows | Evolución T002–T004, revisión, retoma y acceso documentado. | Las pruebas anteriores se atribuyen a sus reportes. Sólo Git y presencia de tareas se observaron nuevamente. |
| PLAN-RECUPERADO-v2 e índice de doce exportaciones | Síntesis previa, procedencia y límites conocidos. | Contienen estados anteriores que deben reconciliarse con los resultados posteriores. |

**Faltantes y pérdidas posibles**

- No se recuperaron todos los chats originales ni todas las decisiones que pudieran contener.
- No se inspeccionaron Pages, Notion, Calendar, Paperclip ni servicios actuales.
- Medios, editables y otros binarios enlazados carecen de comprobación de disponibilidad actual en este worker.
- Faltan cartera vigente, demanda comprobada, cobros conciliados y aceptación comercial.
- Falta evidencia humana del ensayo y de capacidad semanal.
- No se revalidaron todos los hashes, enlaces y recibos históricos. El informe de comparación de doce documentos es evidencia previa.
- Algunas salidas extensas de lectura quedaron truncadas. La síntesis usa secciones visibles y lecturas acotadas posteriores, con profundidad parcial por el límite temporal.
- ONIA-CENTRAL quedó excluido. Tampoco se consultaron secretos, bases de apps ni chats por filesystem.

Las rutas prioritarias solicitadas fueron localizadas. La conservación documental identificada permite continuar, pero no permite certificar recuperación íntegra ni ausencia de pérdidas.

## 7. Segunda pasada documental de esta entrega

Realicé una segunda pasada propia de coherencia y evidencia antes del cierre.

| Control | Resultado |
|---|---|
| Seis áreas | Cubiertas con tareas, entregas, límites y dependencias. Profundidad parcial declarada. |
| Evidencia directa frente a atribuida | Git y tareas observados ahora. Pruebas anteriores identificadas como evidencia documental. |
| Técnica frente a comercio | Separados runner, harness, simulaciones, ensayo humano y cobros. |
| Versiones contradictorias | Corregidos en esta síntesis los estados antiguos de T002, retoma, Windows y cobertura de referentes. |
| Prioridades | Presentadas como propuestas. Workshop evaluado junto con otras vías. |
| Acciones externas | Ninguna realizada durante esta revisión. |
| Persistencia | Sin escritura propia. Cierre y guardado del stdout pendientes del wrapper. |

La corrección más material fue incorporar los estados por área del 5/11. El plan recuperado anterior subestimaba la ampliación comercial/social de referentes. También se conservó la distinción entre el D1 bloqueado inicial y el piloto silencioso posterior.

No ejecuté `./ejecutar.sh --comprobar` dentro del lote activo. El manual lo sitúa cuando no hay trabajo activo y esta ejecución ya mantiene el circuito del runner.

**Revisión independiente T006 PENDIENTE.** Esta segunda pasada pertenece al mismo ejecutor. T006 deberá contrastar la entrega guardada con las fuentes antes de aceptarla.

## RELEVO LOCAL

- **HEAD observado** `e55812ce1bc8ef798fb370257ba887d07acccc53`, rama `master`, estado Git sin cambios visibles.
- **Fuentes principales** base operativa del repo, estados por área, snapshots acotados, `operacion/fuentes-plan/` y `operacion/resultados/`.
- **Estado** T005 entrega esta reconciliación para revisión. Inicio registrado y tarea en curso al consultar. No se verificó todavía cierre del wrapper.
- **Siguiente encargo** T006, revisión independiente secuencial de la salida conservada. Después corresponde la elección de Sergio.
- **Ubicación del resultado** **solo en esta sesión por parte de Codex**. No creé `RECONCILIACION-ONIA-20261107.md`. El registro identifica el directorio del lote `resultados/T005-RECONCILIACION.txt.UWDpnK`; el wrapper debe completar y comprobar su salida.

## RESUMEN EJECUTIVO

1. **Conocer la brecha real y las oportunidades existentes** hacia Bs 3.000 al 14/11.
2. **Elegir una entrega y validar su capacidad**, aprovechando los activos recuperados.
3. **Cerrar su recorrido manual de conciliación y entrega**, antes de depender de automatizaciones.

Hay cobertura documental de las seis áreas. Persisten faltantes de chats, medios, estado actual de apps, demanda, capacidad humana y cobros.

**Decisión material para Sergio tras T006** — elegir si el próximo encargo será establecer la brecha comercial con datos mínimos que él aporte, o validar una entrega concreta. Mi propuesta es comenzar por la brecha comercial.


## Anexo incorporado por coordinación — correcciones exactas T006

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

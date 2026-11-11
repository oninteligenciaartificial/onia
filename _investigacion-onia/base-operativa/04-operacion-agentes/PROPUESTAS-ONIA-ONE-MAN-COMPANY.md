# ONIA como empresa de una persona

**Para la coordinadora de Codex · Propuesta para analizar y decidir con Sergio**

Quiero dirigir ONIA definiendo qué construir y vender, probando demos, aprobando entregas y grabando contenido con mi cara. Quiero delegarte la preparación de encargos, la asignación de sesiones, la revisión, la integración y el seguimiento. Tú diriges la orquestación. Grokbot aporta investigación y sus agentes pueden aportar insumos concretos si los necesitas.

**Primero contrasta estas propuestas y tráeme tus recomendaciones. Después de mi respuesta, convierte lo acordado en encargos y dirige la ejecución.** Usa GitHub y el registro del harness para los estados y decisiones, el VPS para comprobar qué corre y el homelab para verificar qué capacidad está disponible.

## Fuentes de partida

- [Investigación de Grokbot sobre harness, VPS y homelab](https://github.com/oninteligenciaartificial/onia/blob/c10f060/_investigacion-onia/base-operativa/04-operacion-agentes/INVESTIGACION-HARNESS-ONE-MAN-COMPANY-20261111.md). Incluye las fuentes técnicas y las nueve correcciones de la revisión independiente. Su diagnóstico del repo se hizo sobre `f4479eb`.
- [Investigación sobre X, el panel y las contras](https://github.com/oninteligenciaartificial/onia/blob/c10f060/_investigacion-onia/base-operativa/04-operacion-agentes/INVESTIGACION-X-Y-PANEL-20261111.md) y [capturas de referencia](https://github.com/oninteligenciaartificial/onia/tree/c10f060/_investigacion-onia/base-operativa/04-operacion-agentes/evidencias/x-paneles-20261111).
- [Cierre de venta del workshop](https://github.com/oninteligenciaartificial/onia/blob/c10f060/_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/CIERRE-VENTA-20261111.md). Coteja los antecedentes con las decisiones y el estado más reciente.

## Propuesta 1 · Operar el harness y aprovechar los tres cupos

1. **Piloto real del despachador.** Elige dos IDs elegibles del lote aprobado, con rutas distintas. Propón cómo verificar lanzamiento, recogida, revisión del commit exacto, recuperación sin duplicados y trazabilidad hasta la integración. El documento registra 34 pruebas del despachador y deja pendiente el piloto con sesiones reales. Confirma si el estado cambió.
2. **Dos cupos de producción y uno de revisión, como reparto inicial.** Refresca las seis tareas que figuraban en revisión desde el 10. Una ya tenía dictamen de cambios. Indica cuáles revisar, corregir o cerrar por haber sido reemplazadas, con evidencia. Da prioridad a revisar cuando haya una entrega lista y un cupo disponible.
3. **Operación nocturna.** Si el piloto pasa, propón un lote acotado y un temporizador en el VPS con vigencia, presupuesto, criterio de parada y una coordinadora asignada a recoger, aceptar e integrar. Si falta esa cobertura, indica qué trabajo independiente puede avanzar y qué quedará esperando. Distingue el piloto de habilitar la recurrencia.
4. **Cuota y modelos.** Actualiza la lectura histórica de 18 % usado del 11 a las 15:39, hora de La Paz, y verifica las condiciones del corte del 14. Conserva margen para revisión. Evalúa una lectura de cuota sin abrir una sesión y qué hacer si el dato vence o no está disponible. Contrasta scripts para pasos repetibles, Luna para tareas acotadas cuando esté disponible y Sol para implementación y revisión según complejidad. El cambio de perfiles del despachador requiere código y pruebas.
5. **Control de `onia-llm`.** Verifica si sus trabajos comparten cuenta y cuota con Codex, quién puede cambiar el script y cómo contabilizarlos en un límite común. Un semáforo dentro de Grok reduce su concurrencia, pero por sí solo deja dos contadores. Presenta el control de concurrencia y el cambio Astra → Sol como decisiones distintas.
6. **Paralelismo medido.** Usa rutas exclusivas y espacios de trabajo separados. Si el piloto funciona, baja la cola de revisión y hay cuota, plantea una comparación con tres y luego cuatro sesiones, con criterios de parada. Evalúa cinco sólo si cuatro mejora las entregas aceptadas por hora. Distingue autorizar un ensayo de adoptar un nuevo límite.
7. **Homelab y continuidad.** Verifica el estado de la retoma v4 y las pruebas de acceso, aislamiento y recuperación que faltan. Propón una cola de CPU coordinada por el VPS, con un trabajo pesado inicial, límites de recursos, comprobación de resultados y recuperación ante suspensión o desconexión. Empieza con transcripción y FFmpeg; luego considera builds y tests pesados. El homelab aporta cómputo local y la cuota de Codex se mide aparte. Define qué sigue con scripts tras el 14, incluido el material para la clase del lunes 16. Cualquier proveedor de pago queda como decisión separada.

## Propuesta 2 · Tres flujos que yo pueda dirigir desde el teléfono

| Flujo | Recorrido objetivo | Herramientas a contrastar |
|---|---|---|
| Producto | Idea → encargo verificable → implementación aislada → pruebas y revisión → demo móvil → mi decisión → integración. | Panel de ONIA, harness, Codex CLI, GitHub y entorno privado de vista previa. |
| Contenido | Guiones en el panel → elijo qué grabar → dejo el bruto en una carpeta privada → transcripción, cortes y subtítulos → reviso y apruebo el video. | Cámara del teléfono, almacenamiento privado, editor de ONIA, FFmpeg y transcripción local en el VPS o el homelab validado. |
| Venta y aprendizaje | Publicación con **«comentá NEGOCIO»** → respuesta del canal → conversación y QR → confirmo el pago → acceso a Meet → preguntas de interesados alimentan contenido y producto. | Instagram/Facebook y permisos Meta, WhatsApp Business, n8n, QR y Google Calendar/Meet. |

Para cada herramienta, indica si está **operativa**, **probada en ensayo**, **preparada en código** o **pendiente de conexión**. Identifica el responsable y la evidencia de cada paso. Mantén **NEGOCIO** y **QR con confirmación manual** como decisiones vigentes. Separa la prueba con un contacto autorizado, la activación del canal y la apertura de la venta.

Usa el workshop como primer piloto: **un video mío listo para aprobar, una inscripción de prueba de punta a punta y una mejora de la app que pueda probar en el teléfono**. La mejora podría ser ver la ficha del interesado y confirmar un pago simulado. Si el alcance no cabe, dime qué entregarías primero y qué dependencia mueve.

Coteja los horarios acordados —**viernes 13 a las 20:00, sábado 14 a las 14:00 y lunes 16 a las 20:00, hora de La Paz**— con los eventos de Meet. Preséntame por separado la corrección de esos eventos, la decisión sobre el choque personal del viernes y el sí para abrir la venta. Incluye en las prioridades el guion del video de venta, las fechas y los materiales de las clases.

## Propuesta 3 · Panel de fábrica para operar desde el celular

Usa el panel existente como primera opción. Comprueba el acceso privado desde mi teléfono y recorre **Hoy, Fábricas, Flujo diario, Calendario del workshop, Guiones, Sala de montaje y Entregas y bloqueos**. Dime qué ya puedo resolver allí y qué requiere un cambio.

Evalúa una vista móvil corta con **decisiones pendientes, demos y videos para aprobar, bloqueos y siguiente entrega**. Cada decisión debería mostrar el resultado, la evidencia y qué ocurre con un sí o con un pedido de cambios. Propón cómo registrar esas decisiones en el harness y cuánto costaría mantener la vista. Las capturas de X sirven para comparar ideas de interfaz.

El calendario del workshop pertenece a la fábrica. Mantén la agenda personal en Google Calendar. Si un **Life OS** con Calendar y Boss Life vale la pena, déjalo como propuesta independiente para después del 14.

## Contras y cómo evaluarlas

| Punto de la investigación | Qué quiero que verifiques o propongas |
|---|---|
| La tesis de una empresa de USD 1.000 millones con una persona es especulativa. Las impresiones de X miden alcance. | Usa como evidencia el resultado del workshop, el trabajo entregado y el tiempo que me consume dirigirlo. |
| Más agentes pueden ampliar la cola de revisión. Ya hubo descoordinación con los horarios. | Mide antigüedad de la cola, retrabajo y entregas aceptadas. Define dónde quedan las decisiones vigentes y quién las registra. |
| Las pruebas del despachador y un panel activo acreditan partes distintas del flujo. | Exige recibos de sesiones reales para el piloto y una prueba desde el teléfono para el panel. |
| `onia-llm` puede abrir trabajo fuera del contador. La lectura de cuota y las condiciones posteriores al 14 son inciertas. | Comprueba qué comparte cuenta, define admisión conjunta y prepara continuidad con scripts para los pasos repetibles. |
| El VPS concentra panel y registro. El homelab se puede desconectar y su alta debe verificarse. | Define qué se conserva si cae cada equipo, cómo se retoma el último avance confirmado y dónde se comprueba que quedó una sola entrega. Mantén privado el acceso al worker. |
| El panel tiene varias secciones y puede ser lento de usar en móvil. | Mide si puedo abrir, entender y resolver una decisión desde el teléfono. Evalúa una vista corta antes de ampliar el panel. |

## Qué quiero recibir antes de decidir

1. **Estado actual con evidencia.** GitHub, VPS, panel, homelab, cuota, cola de revisión y canales. Fecha las observaciones y señala las diferencias con los informes.
2. **Tu recomendación.** Qué tomarías de cada propuesta, qué ajustarías y qué postergarías. Dime dónde está hoy el cuello de botella y qué se puede hacer en paralelo.
3. **Los primeros tres encargos listos.** Como candidatos, compara el piloto del despachador, el cierre de revisión y el piloto comercial desde el teléfono. Para cada encargo que elijas, incluye ID, responsable, rutas, dependencias, cupo, entregable, prueba de aceptación y revisor.
4. **Una sola lista de decisiones para mí.** Piloto, recurrencia nocturna, límite y modelos de `onia-llm`, eventual ensayo con cuatro, horarios de Meet y choque personal, prueba de NEGOCIO, apertura de venta y continuidad después del 14. Para cada una, dime qué recomiendas y qué habilita mi respuesta.
5. **Una semana de prueba.** Propón medir entregas que pude usar, minutos míos por entrega, tiempo de espera en revisión, cuota por entrega aceptada y cuántas veces tuve que destrabar una sesión. Para el workshop, añade cuántas personas avanzan de interés a inscripción y cuántos pagos confirmé.

Tráeme primero la recomendación y las decisiones agrupadas. Con lo que acordemos, prepara los encargos y dirige el trabajo desde el harness.

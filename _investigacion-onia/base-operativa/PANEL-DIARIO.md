# Panel diario: vida, marca personal y actualidad

Actualizado el 4 de noviembre de 2026. Existe [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964), con vida, contenido, ventas, actualidad y decisiones. Su estructura fue revalidada por conector. Las tablas de este documento mantienen el diseño funcional: no todos sus campos, vistas y avisos están implementados. Apariencia móvil y entrega de notificaciones siguen sin comprobarse.

## Arranque de la operación diaria · 7 de noviembre

Revisar las seis áreas todos los días y sostener dos encargos de ejecución como límite inicial. Las comprobaciones breves por área pueden correr en paralelo. La prueba de seis demuestra una ráfaga controlada. Para el trabajo diario, la prioridad y las dependencias determinan qué entregas ocupan los cupos. [Ensayo de seis áreas](continuidad/evidencias/seis-areas-cloud-001/INFORME.md)

### Primer día de trabajo

| Encargo | Responsable e insumos | Entrega del día |
|---|---|---|
| **Poner en uso la vista Hoy de ONIA** | Organización en Cloud. Reutiliza Sergio · Hoy, la cola existente y los IDs de las fuentes canónicas. | Una vista privada muestra las seis áreas, las prioridades, los bloqueos y la toma pendiente. Se coteja una actualización real por ID y su evidencia. |
| **Dejar la continuidad al día** | Desarrollo e Integración. Usan la rama de prueba ya verificada y preparan los cambios compartibles más recientes para la referencia de trabajo. | Una sesión recupera por ID y commit el paquete operativo y encuentra qué sigue, con evidencias y sin que Sergio copie el historial. La prueba en chat recién creado comprueba además el arranque desde el entorno publicado. |
| **Montar la pieza 01 cuando llegue la toma** | Video recibe la grabación. El guion, la tarjeta y la propuesta de edición ya están listos. | Primer corte privado revisable. Se coteja audio, subtítulos, prueba visible y acción final. La toma queda en **Pendiente de mí** hasta que Sergio la entregue. [Pieza 01](investigacion/2026-11-07-primer-contenido-onia/PIEZA-01.md) |

Organización y Desarrollo pueden empezar en paralelo. Cuando la toma esté disponible, Video toma el siguiente cupo de ejecución. La verificación de medios debe cubrir que Cloud pueda abrir la toma y recuperar el corte. Los resultados reales del día quedan enlazados a sus registros, que conservan la autoridad sobre el estado.

### Revisión de las seis áreas

| Área | Qué se revisa al inicio | Qué se activa cuando corresponde |
|---|---|---|
| **Organización** | Prioridades, entregas que esperan revisión y pendientes de Sergio. | Ajustar la vista por ID y marcar hora de actualización. |
| **Desarrollo** | Entregas del harness, fallos de acceso y referencias Git que se pueden retomar. | Resolver el bloqueo que afecte un encargo real y guardar su comprobación. |
| **Marketing** | Qué pieza u oferta sigue, qué prueba respalda el mensaje y qué CTA está listo. | Entregar el siguiente brief o ensayo de oferta. Las aperturas ya comprobadas de la pieza 01 se reutilizan. |
| **Video** | Grabaciones disponibles, corte en curso y revisión de material. | Montar la pieza que tenga insumos. Una referencia entra por QA cuando resuelve una decisión concreta. |
| **Automatizaciones** | Estado de los flujos en uso y bloqueos de la cola. | Para `TR-CLAIM`, acreditar destino y rol aislados antes de ejecutar la prueba de n8n y SQL. |
| **Producto** | Estado del repo propio, cambios abiertos y siguiente resultado. | Acreditar el checkout completo en Cloud cuando toque un encargo de Platform y ejecutar la prueba del cambio elegido. |

**Inicio del día** · Coordinación recoge una línea por área con fecha, estado, evidencia o fuente, siguiente acción y bloqueo con responsable. Una revisión sin cambios se marca como tal. Una fuente que no pudo comprobarse se registra como pendiente de verificación. Se eligen dos entregas según prioridad y disponibilidad de insumos.

**Durante el día** · Cada ejecutor recibe ID, resultado, entradas, archivos o recurso asignado y criterio de aceptación. Se actualiza el registro ante una entrega o un bloqueo. Si queda esperando material o decisión, libera el cupo y la siguiente tarea lista puede avanzar.

**Cierre del día** · Integración local consolida enlaces y revisiones. Revisión local coteja la evidencia y separa listo para revisar de aceptado. Coordinación entrega una vista de las seis áreas revisadas, lo terminado y lo que sigue. La única escritora de la proyección Notion es Organización. El próximo día se recupera por ID y commit o enlace canónico. [Continuidad](cloud/CONTINUIDAD.md) · [Reparto](SESIONES.md)

El primer ciclo operativo pasa cuando la vista refleja tareas reales sin duplicados, una entrega se puede retomar desde un chat Cloud nuevo y Sergio encuentra su próxima acción desde el celular. El chequeo de edición de video, el checkout de Platform y la prueba real de n8n se hacen cuando sus encargos entren. Si se quiere un arranque o aviso automático diario, se verifica aparte el disparo y la entrega con la PC apagada. La rutina inicial se inicia por encargo.

## Portada móvil

Una página privada de Notion, **Sergio · Hoy**, con bloques verticales y vistas breves. No exigir desplazamiento horizontal para las decisiones del día.

| Bloque | Qué permite decidir |
|---|---|
| Mi día | Resultado principal, compromisos del calendario, hábitos informados y siguiente acción que cabe en el tiempo libre |
| Qué publicamos | Hora prevista, red/cuenta, pieza, formato, estado y qué falta para que salga |
| Santa Cruz | Pocas noticias relevantes y próximos eventos, con fuente, fecha y comprobación |
| Personas y aprendizaje | Novedades útiles de las fuentes elegidas y una idea aplicable a la marca |
| Pendiente de mí | Grabaciones, materiales o decisiones que necesita el agente |

El calendario personal conserva compromisos efectivamente creados. Notion conserva la operación cotidiana; [CEREBRO-DIARIO.md](CEREBRO-DIARIO.md) define sus referencias y el uso acotado del contexto histórico. Los informes técnicos anteriores están en [archivo privado](https://app.notion.com/p/40e2eb20bdfd818ca90aefe9a1902b39), fuera de la portada. La documentación adoptada vive en Git. Ver fechas de Notion junto a Calendar no equivale a sincronizarlas.

## Registros mínimos

Crear destinos de relaciones antes de añadirlas. Resolver los IDs y propiedades reales con el conector, sin asumirlos a partir de este diseño. Revisar si ya existe una estructura equivalente antes de crear otra.

| Registro | Una fila representa | Campos esenciales y vistas |
|---|---|---|
| Días | Un día local | Fecha, resultado principal, siguiente acción, cierre, hábitos sin completar por defecto. Vista Hoy e historial. No convertir hábitos propuestos en acciones realizadas. |
| Publicaciones | Una publicación en una cuenta concreta | ID de pieza, título, fecha/hora prevista, fecha/hora confirmada por el publicador, red/cuenta, formato, estado editorial, guion, archivo y URL publicada. Vistas Hoy, Semana, Por grabar, Por revisar. |
| Radar | Una noticia o evento individual | Tipo, título, fuente, URL original, publicación, inicio/fin del evento, cierre de inscripción si aplica, lugar, costo/requisitos conocidos, verificado el, estado y motivo de relevancia. Vistas Novedades y Próximos eventos. |
| Fuentes | Una persona, institución o medio con enlace identificado | Nombre, tipo, URL/cuenta, temas, elegida/propuesta, última consulta y estado de acceso. Separar identidad de persona y autenticación de cuenta. |

El ID de pieza permite adaptar un video a varias redes sin confundir tres piezas con tres publicaciones totales. Guion y archivo final permanecen en una ubicación canónica enlazada. Los MP4 no se guardan como adjuntos pesados del panel por defecto.

Estados editoriales: idea, guion, por grabar, edición, por revisar, aprobado, programado, publicado, falló. Son el estado del contenido, distinto de los cuatro estados del encargo del harness. **Programado** exige confirmación/ID del publicador y **publicado** exige enlace o evidencia verificable; una fecha prevista no alcanza.

## Resumen diario propuesto

Zona de trabajo: Santa Cruz de la Sierra, UTC−4. Cadencia a configurar y probar, todavía no activada:

- Mañana, antes del colegio: lectura de dos minutos con prioridad, agenda, publicaciones previstas y hasta tres novedades relevantes. Si hay eventos próximos, mostrar hasta tres con su fecha real.
- Durante el día: recibir entradas y cambios cuando Sergio tenga tiempo libre. No limitarlo a los controles.
- Noche, revisión flexible: resultados comprobados, qué quedó pendiente y material necesario para el siguiente día.

Para noticias, revisar primero novedades de las últimas 24–48 horas; para eventos, próximos 14 días y cierres de inscripción. No llenar el resumen con información vieja para cumplir una cuota. Diferenciar **sin novedades relevantes** de **no se pudo consultar la fuente**. Señalar hora de actualización.

No agregar automáticamente noticias o eventos encontrados al calendario. Sólo los eventos elegidos por Sergio se incorporan, después de verificar horario y conflictos. No enviar alertas repetidas por un mismo contenido; identificar por URL y evento. Los cambios de un evento elegido se tratarían como novedades accionables.

## Fuentes iniciales

La Gobernación departamental es una fuente solicitada expresamente. Alcaldía, organizaciones y medios de contraste son fuentes propuestas; no confundir institución, jurisdicción o declaraciones oficiales con verificación independiente.

| Fuente pública | Uso | Comprobación al 4-nov-2026 |
|---|---|---|
| [Gobernación de Santa Cruz](https://santacruz.gob.bo/) | Institución departamental, comunicados y servicios | Portada leída. El listado /noticias necesita prueba en navegador cloud; su extracción no fue suficiente. No hay un feed fiable probado. |
| [Cultura y Turismo municipal](https://culturayturismo.gmsantacruz.gob.bo/) | Eventos culturales y talleres de la ciudad | Agenda y ficha de evento leídas sin login. Es Alcaldía, no Gobernación. |
| [Oportunidades de Cultura](https://culturayturismo.gmsantacruz.gob.bo/oportunidades) | Convocatorias y formación | Comprobar bases y cierre en cada fuente original. |
| [EL DEBER — Santa Cruz](https://eldeber.com.bo/santa-cruz) | Contraste periodístico local | Sección legible; acceso y fecha se comprueban por artículo. |
| [UNITEL — Santa Cruz](https://unitel.bo/noticias/santa-cruz) | Segundo contraste de actualidad | Sección pública con fechas; no acredita actualidad de cada artículo posterior. |
| [APAC](https://festivalesapac.com/) | Festivales y convocatorias culturales | Sitio público leído; verificar plazos concretos. |

Redes de Gobernación encontradas como candidatas: GobSantaCruz en Facebook/X y gobsantacruz en Instagram. El enlace vigente desde una fuente oficial no quedó comprobado; algunas páginas bloquearon lectura. No tratarlas como fuentes conectadas o autenticadas ni repetir intentos sin cambio de condición.

Ejemplo para la primera prueba: la [ficha municipal de Aquí Canta Bolivia 2026](https://culturayturismo.gmsantacruz.gob.bo/eventos/63791c04-e14e-4a01-8842-c022530afa05) informa 4–5 de noviembre, 16:00–20:00, Teatro Villa 1.º de Mayo, gratis, todas las edades. Fecha de publicación no indicada. Es una ficha informativa comprobada, no asistencia seleccionada ni evento agregado.

Las nueve fichas de referentes, fuentes y cobertura están en el [índice de investigación](investigacion/2026-11-04/README.md). Incluyen textos y muestras audiovisuales parciales; no cursos enteros ni operación privada auditada. Las cuentas exactas se comprueban antes de seguirlas.

## Canales y ejecución

**Primera etapa:** Notion móvil y los avisos de calendario ya acordados. Probar un aviso real antes de atribuir entrega al celular. No comprar Notion AI para que Codex gestione el panel.

**Siguiente canal recomendado, aún sin conectar:** bot privado de Telegram para un resumen con enlace al panel y entrada de notas. Telegram requiere bot, credencial y chat iniciado por Sergio. Si se implementa, limitar el receptor/emisor a su chat y guardar el token en la credencial correspondiente, nunca en este repo.

WhatsApp Business Platform queda como alternativa posterior: los mensajes proactivos fuera de la ventana de atención necesitan plantillas y pueden tener cargos. No considerar los resúmenes diarios gratuitos por defecto ni confundir la app personal con la API empresarial.

Un flujo pequeño en el n8n existente podría guardar notas y entregar avisos con la PC apagada. No agregar navegadores ni render al VPS. No afirmar que un mensaje de Telegram inicia Codex Cloud: ese disparador, autorización y ejecución todavía deben comprobarse. La suscripción de Codex no es automáticamente una clave API para n8n.

Fuentes de capacidades: [Telegram Bot FAQ](https://core.telegram.org/bots/faq), [precios de WhatsApp](https://whatsappbusiness.com/products/platform-pricing/), [política de WhatsApp](https://whatsappbusiness.com/policy/), [avisos de Notion](https://www.notion.com/help/notification-settings), [Notion Calendar](https://www.notion.com/help/use-notion-calendar-with-notion).

## Criterio de primera entrega

1. Conexión Notion válida, destino privado identificado y estructura existente revisada.
2. Portada legible desde celular, registros y filtros comprobados con entradas reales o rotuladas como propuesta.
3. Una ficha de evento con fuente, fecha y campos desconocidos conservados como desconocidos; no crear una noticia sin novedad real.
4. Una publicación propuesta con hora prevista y estado correcto, sin simular programación.
5. Lectura y actualización desde el entorno cloud comprobadas; enlace persistido en el cerebro.
6. Automatización recurrente y mensajería permanecen pendientes hasta prueba separada de disparo, entrega y registro, sin PC encendida.

## Estado de esta preparación

La autenticación inicial falló; posteriormente se creó y organizó el panel y se releyó con el conector. Publicaciones y noticias tienen destinos existentes; no volver a crearlos. Calendar, bot, voz, publicación social y sincronización diaria siguen sin activación comprobada. El [estado operativo](ESTADO.md) mantiene la comprobación vigente.

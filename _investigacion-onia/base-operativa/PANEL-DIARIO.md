# Panel diario: vida, marca personal y actualidad

Actualizado el 4 de noviembre de 2026. Existe [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964), con vida, contenido, ventas, actualidad y decisiones. Su estructura fue revalidada por conector. Las tablas de este documento mantienen el diseño funcional: no todos sus campos, vistas y avisos están implementados. Apariencia móvil y entrega de notificaciones siguen sin comprobarse.

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

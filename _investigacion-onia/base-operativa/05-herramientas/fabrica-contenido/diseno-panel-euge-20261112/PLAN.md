# Diseño del panel de fábricas · 12 noviembre 2026

Estado: prototipo para revisión de Sergio. No conectado a producción. La solicitud actual pone primero el diseño de PC y móvil y prevalece sobre el orden histórico de guiones.

## Referencia y adaptación

Fuentes existentes: EUGE-VIDEO-BOSS-20261109.md (17:58–28:31), EUGE-VIDEO2-BOSS-20261109.md, DECISIONES-SERGIO-20261110.md, PRIORIDADES-HASTA-14.md. Capturas aportadas de mapa y sala de montaje.

Se conserva la estructura entrada → fábrica y pasos → revisión → destino, el foco en revisiones pendientes y los comentarios por versión. Se adapta a OnIA con mapa claro, tipografía, sin copiar ilustraciones, marcas ni métricas de Euge. Móvil transforma filas en recorrido vertical. Vlog fuera del editor.

## Alcance de esta entrega

Mapa filtrable de seis fábricas. Revisión con versión y ejemplo antes/después, correcciones e historial en memoria. Formulario de encargo y trabajo simulado. Cerebro con reglas, fuentes y catálogo ampliable de propósitos. No son métricas, estados ni entregas reales. Recargar borra las acciones de demostración.

## Desarrollo después de validar el diseño

1. Conectar lectura del panel existente. Contrato por tarea: ID, proyecto, fábrica, entrada, propósito, tratamiento, formato, canal, responsable, dependencias, estado observado, fecha de observación, versión, archivo, evidencia y siguiente acción. Si falta el dato mostrar desconocido. Conserva auth privada y servicio existente.
   Cierre: PC y iPhone abren la misma versión real en dos acciones; un dato obsoleto o una fuente caída se identifica sin inventar estado.
2. Conectar revisión al almacén existente. Corrección vinculada a versión/hash, acuse, antes/después y responsable; confirmar qué cambió. Aprobación técnica distinta de editorial y de publicación.
   Cierre: doble clic o reintento produce un solo registro; revisión obsoleta no aprueba una versión nueva; se recupera después de recargar.
3. Conectar lanzamiento al puente del harness existente. Validar entradas, permisos aplicables, dependencias, cupo e idempotencia antes del lanzamiento; mostrar ID canónico y acuse. No reactivar el despachador congelado.
   Cierre: un clic produce una tarea; un reintento recupera la misma; cada estado viene del harness, no de la UI. Un cupo libre explica el bloqueo o ausencia de trabajo elegible.
4. Sala de montaje. Video real en horizontal/vertical, selección de versión, comentario en tiempo y plano, audio/guion, evidencia de cambios. Falta diseñar y conectar su detalle especializado: esta versión sólo muestra dónde se abre la entrega.
   Cierre: Sergio reproduce su material en ambos dispositivos y una corrección se localiza en el tiempo y versión correctos. Una muestra ficticia no satisface este criterio.
5. Canales y venta. Recorridos separados de WhatsApp, comentarios/DM de IG y FB. Mostrar ensayo, real, bloqueado. QR privado, confirmación manual de Sergio y acceso posterior. Nunca una captura como confirmación de pago.
   Cierre: ensayo permitido en n8n con el número autorizado, recibo completo, duplicados controlados, sin mensajes a terceros.
6. Recurrencia del flujo aceptado. Usar las rutinas existentes tras autorización aplicable, conservar logs/acuse, recuperación sin duplicados y medición. No prometer servicio continuo por tener un timer.
   Cierre: un ciclo real observado desde entrada hasta salida revisada y visible, y un fallo recuperado sin perder ni duplicar trabajo.

## Medición por recorrido

Registrar entrada, elegibilidad, inicio, fin de ejecución, entrega disponible, revisión y aceptación. Separar espera de ejecución. Medir cumplimiento contra criterio, rechazos/correcciones y evidencia de resultado. No contar diseños como funciones conectadas, ni tests como ventas. No estimar ventas ni cobertura sin denominador.

## Brechas abiertas y responsables

- Sergio: revisar organización y navegación de este diseño. No hace falta repetir investigación.
- Codex: adaptar/implementar siguientes pasos de UI tras revisión, comenzando por datos reales y correcciones, sin reemplazar servicios.
- Codex: detalle especializado de montaje y pruebas de conectividad de canales. Reutilizar evidencia y scripts existentes.
- Sergio: aportar grabación real para aceptar montaje; conservar sus decisiones de publicación, gasto y pago.
- Infraestructura congelada: no bloquear diseño ni contenido por benchmarks/homelab/4 sesiones.

Sin criterios finales de guion extraídos de ejemplos originales no se entrega una tanda como producto validado. El aprendizaje es corrección versionada y comprobada en otra pieza, no entrenamiento del modelo.

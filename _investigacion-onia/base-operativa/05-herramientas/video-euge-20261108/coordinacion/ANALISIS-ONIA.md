# Del video de Euge al trabajo de OnIA

9 de noviembre de 2026. Fuente: [video de Euge Oller, ID JuAQILH7dkQ](https://www.youtube.com/watch?v=JuAQILH7dkQ). La identidad se ancla por ID y autor visible. La página mostró «final v4 animated», distinto del título usado en el diagnóstico anterior; no se estableció la causa de esa diferencia.

**Para OnIA, lo aprovechable es convertir cada resultado pequeño en un proceso con entradas, criterios, revisión y mejora.** El agente coordinador reparte ese trabajo y conserva su estado. La propuesta de este documento usa lo que ya existe en OnIA y no activa nuevas áreas ni servicios.

## Lo observado en el video

| Referencia aproximada | Observación del material, no verificación de su backend |
| --- | --- |
| [0:27](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=27s) | Un tablero presenta entradas, etapas, revisión y destinos. |
| [12:15](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=735s) y [13:18](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=798s) | Ejemplos de avisos proactivos y un coordinador que da acceso al tablero. |
| [16:24](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=984s) | Descompone un video en resultados menores y pide definir qué hace bueno a cada uno. |
| [21:25](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1285s) | Propone medir, aprender y mejorar el proceso, con fuentes, pasos y evaluación. |
| [24:46](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1486s) y [26:19](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1579s) | Se ven comentarios asociados al tiempo, nueva versión y controles de aprobación/cambios. |
| [27:12](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1632s) | Distingue un flujo sin revisión, presentado como experimento y con pocas visitas. |
| [28:51](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1731s) | Describe un servidor persistente compartido por agentes de su equipo. |

Son hitos muestreados y tiempos aproximados de ASR alineado. El video explica y demuestra interfaces; no auditamos sus servidores, publicaciones ni resultados comerciales. Incluye promoción de su producto. Las comparaciones de modelos y precios que menciona no se convierten aquí en recomendaciones de contratación.

## Aplicación concreta a OnIA

| Parte | Disponible y verificado en el repo | Paso que falta |
| --- | --- | --- |
| Materia prima | Catálogo de 19 referentes/79 piezas, consulta de 23 patrones con fuentes y lector manual de tres URLs. | Cada lote elige fuentes vigentes y explicita el patrón usado, separando hecho del referente y propuesta propia. |
| Producto | Dos guiones propios y kit de los primeros diez minutos del workshop. | Revisión editorial y ensayo de Sergio. Una investigación todavía necesita convertirse en una entrega adecuada para el público. |
| Etapas | Tarea canónica, ejecutor, rutas reservadas, evidencia, revisión distinta y aceptación en el harness. | Definir formato y criterio observable para cada entrega de contenido; conservar fallos y retomar el mismo ID. |
| Panel y aprobación | Panel HTML de consulta; adaptador Telegram probado y copia n8n inactiva. | Identidad del bot, destinatario y prueba real autorizada. El panel todavía no escribe aprobaciones ni se actualiza solo. |
| Continuidad | Retoma y publicación verificadas; tres cupos principales globales del harness, revisores incluidos. | Implementar y probar el piloto acotado de cola ya aprobado, con revocación y parada. El scheduler permanente sigue pendiente. |

Fuentes internas: [guía de la entrega nocturna](../../../04-operacion-agentes/evidencias/continuacion-noche-20261109/PARA-SERGIO.md), [operación por tareas](../../../04-operacion-agentes/EMPRESA-UNIPERSONAL.md). Este análisis no amplía esas capacidades ni sus permisos.

Para la fábrica de guiones, el recorrido concreto sería:

1. Una tarea aprobada reúne fuentes fechadas y el patrón editorial pertinente del cerebro.
2. La ejecutora entrega idea, esquema y guion con sus referencias, formato y destinatario definidos.
3. Una sesión distinta coteja hechos y aceptación. Las observaciones devuelven la misma tarea a corrección, con una nueva versión identificable.
4. Sergio aprueba el borrador para grabar. Publicar, enviar mensajes, activar n8n o gastar requieren la autorización aplicable.

Un primer lote manual podría tomar el guion G01 ya existente y entregar una idea, un guion revisado y su ficha de fuentes/patrón. La aceptación exigiría hechos enlazados, propuesta propia separada y observaciones del revisor resueltas. Es un ejemplo para la elección editorial de Sergio; no se despachó otra tarea de contenido durante esta prueba. Platform sigue fuera.

## Qué ajustaría del enfoque para nuestro caso

- **Una coordinación para Sergio y contexto por tarea.** La coordinación mantiene prioridades y dependencias. Cada ejecutora recibe ID, commit, insumos, rutas y aceptación; Git conserva decisiones y resultados. El historial completo del chat no es la memoria obligatoria de cada agente.
- **Ejemplos antes de dar por aprendida una preferencia.** Sergio puede marcar qué cambiar en un guion o aportar un antes/después. Se convierte en regla o ejemplo versionado y se prueba en la siguiente pieza. Guardar una corrección no entrena los pesos del modelo ni garantiza acierto futuro.
- **Evaluación simulada separada de validación real.** Personas simuladas y críticos automáticos pueden sugerir objeciones. No acreditan demanda, aprendizaje de alumnos ni ventas. Para el workshop sigue haciendo falta el ensayo y la revisión ya acordados.
- **Permisos de salida explícitos.** Que otro flujo publique sin revisión no autoriza hacerlo en OnIA. Nuestro primer producto es un borrador revisado; la publicación comercial tiene su propia decisión.
- **Capacidad por trabajo concreto.** Mantenemos los tres cupos. Navegador, captura y ASR requieren además exclusión del recurso compartido y control de CPU. El VPS llegó a picos de CPU casi completa durante esta prueba; este dato no respalda subir el límite ni contratar el stack mostrado en el video.

La secuencia de negocio conserva lo decidido: cerebro consultable → ensayo de los primeros diez minutos → resto del workshop tras revisión de Sergio → automatizaciones acotadas. No se lanzaron esos frentes durante la resolución audiovisual.

## Cobertura y límites

Se comprobó reproducción de 0:00 a 30:02 en la misma pestaña del VPS, con pista español original y velocidad normal. Se conservaron dos grabaciones y una unión de imagen/reloj verificada en 15:10. La inspección visual incluye 34 muestras durante reproducción, más controles, anuncios y revisiones puntuales del archivo.

El ASR local produjo 443 filas; se conservaron 379 para contenido y se excluyeron 64 por publicidad o por cruzar sus bordes. Sus tiempos se corrigieron de PCM concatenado a PTS y luego al reloj aproximado del video. Los huecos medidos y el redondeo impiden tratar estas filas como citas exactas palabra por palabra. Se usa paráfrasis.

La grabación y el ASR acreditan señal y contenido verbal con esos límites. **Esta superficie de sesiones no recibió audio para escucha directa.** No se deducen música, entonación, mezcla o emociones del ASR. El flujo comprobado requiere un operador que inspeccione los controles; no se declara análisis audiovisual autónomo para cualquier sitio.

Esta tanda usó tres sub sesiones nativas del chat: navegador y audio con Sol 6.1 high, revisión distinta con Sol 6.1 ultra. No creó tres procesos CLI del harness ni un scheduler. Los medios, capturas de cuenta y transcripciones crudas permanecen privados; al repo van este análisis, código, índices saneados y recibos.

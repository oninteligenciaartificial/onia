# Controles, automatización y lagunas de esta entrega

9/11/2026 UTC · v1. Checklist de preparación, sin segunda tarea ni registro canónico. Todo lo no ejecutado se conserva como pendiente. La decisión editorial de Sergio y la revisión independiente técnica son pasos distintos.

## Qué se puede automatizar ahora y qué depende de datos o sí

«Automatizable ahora» designa una operación documental local dentro del encargo. No promete recurrencia. La columna de evidencia distingue lo ejecutado de una posibilidad.

| Operación | Entrada → salida / control de fallo | Evidencia en esta entrega | Dependencia / responsable |
|---|---|---|---|
| Comprobar enlaces locales y alcance Git | Documentos → destinos existentes y rutas propias. Fallar si falta un destino o hay cambio ajeno | Comprobación local registrada en evidencia; no certifica contenido de URLs externas | Ejecutora, autorizado ahora |
| Comprobar aritmética del caso | Duraciones/bloques → agenda A válida y B incompatible por 10 min. Rechazar solapamientos u omisiones | Cálculo y agenda de referencia comprobados; no se consultó Claude con A/B | Ejecutora, autorizado ahora |
| Congelar esta versión | Archivos → hashes/tamaños. Cambios posteriores exigen versión/revisión nuevas | Manifiesto saneado generado; no es aceptación | Ejecutora, autorizado ahora |
| Extraer candidatos y deduplicar URLs en un lote manual | URLs primarias + fechas → idea con alias y límites. Fuente ausente o fecha incierta impiden presentarla como noticia | Selección manual F01–F06; F05/F06 agrupados en N01. Deduplicación automática general no implementada | Documentalmente preparable; otro lote necesita su alcance y cuota |
| Convertir una ficha en borrador | Problema + fuente + patrón → guion con bloques respaldados | G01/G02 escritos y revisados por su autora; revisión distinta pendiente | Ya preparado. Generación recurrente no instalada |
| Probar acceso y autonomía | Cuenta propia/dispositivo → petición, revisión y recuperación observadas; registrar ayuda y fallo | Pendiente, sin acceso personal ni ensayo en esta sesión | Sergio realiza acceso y ensayo; observador por designar |
| Abrir inscripción/cobro | Condiciones completas → ID único y conciliación; referencia repetida/timeout → consultar antes de repetir | Sólo recorrido y respuesta borrador | Sergio define canal, horario/zona, pagos, cupos, soporte y autoriza acciones |
| Implementar ingestión recurrente, panel o Telegram | Registro canónico y permisos → servicio con identidad, idempotencia y revisión verificadas | Sólo diseño anterior de fábrica; nada implementado aquí | Requiere encargo y sí específicos; no disparar n8n ni scheduler |
| Producir/publicar contenido o activar anuncios | Guion/hash aprobado + destino y alcance → pieza y recibo; resultado incierto → conciliar | Sin producción, publicación, envíos ni gasto | Sergio aprueba la versión y autoriza cada efecto aplicable. Publicidad sólo borrador |

Referencia de controles futura: [diseño de fábrica](../../../05-herramientas/fabrica-contenido/20261108/DISENO.md) y [contrato](../../../05-herramientas/fabrica-contenido/20261108/CONTRATO.md). Se adapta su trazabilidad, sin ejecutar su fixture ni copiar su registro. Los artefactos de esta carpeta se entregan al coordinador; él decide cómo referenciarlos en la evidencia canónica. No se escribe el JSON/briefing ni se cambia su estado desde esta sesión.

## Criterios editoriales de aceptación propuestos

Cada guion se revisa por su archivo, versión y hash. Un incumplimiento implica pedir cambios sobre esa versión; un hash prueba bytes, no calidad. La revisión propia que figura en la evidencia no se denomina revisión independiente.

| Control | Aceptar editorialmente si… | Pedir cambios si… |
|---|---|---|
| Audiencia y utilidad | Un dueño de negocio principiante entiende un problema y una acción concreta | La pieza depende de jerga, presume herramientas o ofrece una transformación vaga |
| Gancho y entrega | Cada elemento prometido en el gancho aparece en el desarrollo; un único CTA sigue de la utilidad | Se promete una demo/resultado que no existe o se piden acciones incompatibles |
| Fuentes y fechas | Todo hecho de producto tiene primaria abierta, fecha de consulta y límites; publicación y consulta separadas | Sólo hay snippet, la fecha se inventa o una noticia del referente se presenta como especificación oficial |
| Autoría y ficción | Caso inventado visible en toma/subtítulo; patrón documentado separado del diseño propio | Se finge cliente, testimonio, salida de Claude, visionado completo o resultados auditados |
| Oferta | Nombre, comprador, fechas, Claude y Bs 50 coinciden con ficha; las propuestas no aparecen aprobadas | Se ofrece VIP, horario/zona, canal, pago o cupo sin decisión |
| Exactitud del ejemplo | A cabe, B excede 10 min, restricciones y aritmética visibles | Se omite pausa, se solapan tareas o se recorta inventario para fabricar éxito |
| Acceso y demostración | Se distingue muestra escrita de ejecución real; cualquier grabación real usa acceso propio | Se presta una cuenta, se asegura cuota o se afirma que el piloto ya pasó |
| Viabilidad del CTA | Antes de publicar G01 hay canal elegido, responsable y ficha completa para atender información | Se promete DM/QR/pago automático o se usa la palabra clave sin atención disponible |
| Coherencia audiovisual | Tras producción, locución, rótulos y captura coinciden, son legibles y tienen ficción/fuentes accesibles | El montaje introduce una promesa o dato ausente en el texto aprobado; duración nunca ensayada se presenta como medida |

La revisión editorial puede aprobar el texto con pendientes operativos identificados; eso no lo habilita para publicar. El control audiovisual sólo podrá aprobarse al existir una pieza producida. La revisión independiente del encargo debe cotejar el commit entregado y todos los criterios recibidos.

## Errores y lagunas para integrar por coordinación

| ID | Observado / límite | Tratamiento y paso exacto siguiente |
|---|---|---|
| L01 | Volcados agrupados de documentos largos excedieron la salida disponible | Se recuperaron por rangos decisiones, directora, índices y pasajes usados. El registro de lectura declara selección y no integralidad. No se presenta el truncamiento como lectura completa |
| L02 | Memoria histórica mezcla VIP y «sin cuenta de Claude» con decisiones posteriores | Se aplican briefing actual y decisiones: Bs 50 aprobado, VIP propuesto, Claude con acceso propio pendiente. Mantener esta separación al integrar |
| L03 | Índices profundos conservan texto de «para revisión» anterior al estado vigente | Se atribuye aceptación a ESTADO/briefing, y cobertura a fichas. Coordinador puede reconciliar sus índices fuera de este encargo; no se editan aquí |
| L04 | No hay ejecución de A/B en Claude, ensayo humano ni locución medida | Sergio resuelve cuenta propia y ensaya el archivo de diez minutos; conservar entrada, salida, tiempo y ayuda. No ampliar a tres clases antes de su revisión |
| L05 | Búsqueda devolvió un avance noticioso no corroborado en artículo abierto | Se excluye ese avance; la noticia N01 sí tiene artículo primario y fecha. No afirmar búsqueda exhaustiva ni ausencia de noticias |
| L06 | Faltan hora1/zona/canal/pagos/cupos/soporte y decisión VIP | Sergio completa ficha comercial; separar decisión VIP opcional de requisitos necesarios para inscribir |
| L07 | Falta evidencia completa de Euge y percepción integral de referentes | Esperar evidencia del coordinador. No completar atribuciones ni solicitar su navegador ocupado |
| L08 | La evidencia web es resumen/metadata de lectura y puede envejecer | Reconsultar las fuentes usadas antes de publicar si cambia un hecho o se retoma en otra fecha. No afirmar snapshot íntegro remoto |
| L09 | Revisión independiente e integración no son acciones de esta ejecutora | Publicar sólo rama asignada y verificar su hash. Coordinador cierra, obtiene revisor distinto ultra y decide aceptación/integración. No abrir hijos ni integrar master |

No se escribe el registro general de errores. Estos hallazgos quedan sólo en la ruta autorizada para que coordinación los integre si corresponde. No hubo fallos de acceso a cuentas, porque no se intentó acceso autenticado.

## Próximas decisiones concentradas

1. Sergio revisa el guion del piloto y ambos guiones de contenido; indica qué versión conserva o qué cambia. Boss decide qué reglas de la síntesis propuesta incorpora a su integración final.
2. Antes del ensayo: acceso propio de Sergio y de un participante, observador y canal de prueba por designar. Ensayar los diez minutos y registrar los seis criterios, con ayuda y tiempo reales.
3. Antes de inscribir o publicar invitación: completar ficha comercial y responsable de atención del CTA. Confirmar una autorización de publicación/envío concreta sobre versión y destino; este encargo sólo prepara borradores.
4. Tras push: coordinador ejecuta cierre y revisión independiente sobre el commit remoto, recoge veredicto y procede según él. Ninguna casilla de esta entrega sustituye ese veredicto.

---
name: preparar-campana-meta
description: Prepara un borrador de campaña de Meta y comprueba accesos de lectura cuando hay una oferta, un objetivo comercial y un encargo de anuncios. No activa campañas ni modifica cuentas, presupuestos o anuncios.
---

# Preparar una campaña de Meta

El resultado es una propuesta revisable de campaña con piezas, medición y pendientes de acceso. En ONIA, consultá las [reglas comunes](../../../../04-operacion-agentes/reglas-comunes.md) y la ficha vigente de oferta; no fijes un segundo precio, promesa o fecha en el anuncio.

## Brief comercial

Recuperá oferta y demostración, público, ubicación, objetivo, destino de la llamada a la acción, fechas y presupuesto específico de publicidad. Diferenciá dinero disponible de presupuesto publicitario asignado. Si falta presupuesto o acceso, avanzá con la propuesta y marcá esos campos pendientes; no inventes gasto diario para completar la ficha.

Relacioná el objetivo comercial con un resultado observable: consultas calificadas, registros o compras confirmadas, según el encargo. Conservá la distinción entre métricas de Meta y cobros conciliados. Elegí la estructura más simple que permita comprobar la hipótesis; la referencia B2B no obliga a dos campañas, múltiples audiencias o un volumen fijo de anuncios.

## Activos y comprobación de acceso

- Identificá la Página, cuenta de Instagram y cuenta publicitaria previstas mediante datos existentes o una conexión disponible. Un login de navegador o plugin visible no acredita acceso API ni permisos sobre esos activos.
- Si el encargo requiere comprobar acceso, inspeccioná las herramientas del conector o la documentación oficial del endpoint de lectura y su versión antes de llamarlo. Seleccioná una consulta mínima, con campos y período acotados cuando corresponda; registrá activo, resultado y limitaciones. No solicites permisos de gestión para resolver una lectura sin verificar primero lo requerido.
- Las credenciales se resuelven mediante la conexión de su ejecutor; no se incluyen en este brief. Una lectura fallida queda como acceso pendiente y no impide terminar copy, propuesta creativa o plan de medición.
- Esta skill produce archivos de borrador y consultas de lectura: no crea objetos remotos, ni siquiera anuncios pausados. Lanzar o modificar una campaña es otro encargo con estado y alcance propios.

Si después el usuario pide lanzar, reenrutá al encargo de ejecución conservando la autorización recibida y comprobando los datos y accesos que falten. El límite de esta skill no es una razón para repetir una aprobación ya dada ni para afirmar que la campaña se publicó.

## Creatividades y medición

Prepará ángulo, evidencia de la promesa, texto, visual o guion, CTA y destino coherentes entre sí. Identificá los materiales reales disponibles y qué falta producir. Las variantes deben probar una diferencia reconocible, no sólo cambiar palabras.

Definí evento medido, fuente de datos, período, moneda y criterio para revisar el resultado. Sin historial suficiente, expresá hipótesis y condiciones de observación; no conviertas benchmarks de otra empresa en objetivos garantizados ni ajustes automáticos. Comprobá destino y recorrido de registro/pago en el alcance disponible antes de declarar la propuesta lista para lanzamiento.

## Entrega y fuentes

Entregá brief, estructura propuesta, piezas, presupuesto informado o pendiente, plan de medición y lista corta de requisitos sin resolver. Separá «borrador completo», «activos leídos» y «lista para revisión de lanzamiento» según la evidencia.

Referencia técnica primaria: [colección oficial de Meta Marketing API](https://www.postman.com/meta/facebook-marketing-api/overview); consultar sus solicitudes y [documentación de Marketing API](https://developers.facebook.com/docs/marketing-api/) para la operación concreta. Si no se puede comprobar un permiso, versión o endpoint, marcarlo pendiente en lugar de presentar una llamada recordada como verificada.

Referencia comercial selectiva: [Marketing Skills, Meta decision system](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/ads/references/meta-decision-system.md). Aporta preguntas sobre oferta, creatividad y medición; sus umbrales y reglas de escalado B2B no se adoptan como política de ONIA. Redacción propia; no instala ese paquete.

# Política privada de admisión por cuota

Cambio preparado el10/11/2026 a pedido de Sergio de resolver el bloqueo operativo. La configuración real conserva90 hasta una decisión explícita de Sergio. El código por sí solo no levanta esa reserva.

`config.json` privado admite `politica_cuota` con exactamente `max_usado` (número mayor que0 y hasta100) y `autorizacion_sergio` (referencia textual a una decisión comprobada por el operador). Si falta la política, se conserva90. Valores inválidos, campos extra o ausencia de autorización rechazan el lanzamiento. Boss no puede escribir esta configuración por el protocolo SSH ni cambiarla con un pedido.

El mismo control se aplica a lanzamientos delegados y consultas `preguntar`. Consulta una muestra semanal fechada con las validaciones existentes; bloquea si el porcentaje usado alcanza el límite. La reserva no es agotamiento del proveedor. Es un control de **admisión**, no un presupuesto exacto: la muestra tiene retraso y no cancela sesiones ya admitidas. No usarlo para prometer un techo estricto de consumo de un ensayo concurrente.

Una política aprobada con100 permitiría admitir trabajo autorizado mientras la lectura indique saldo semanal disponible; no compra saldo, no autoriza pagos ni cambia el proveedor ChatGPT. El operador debe cotejar la decisión real: un campo de texto no autentica a Sergio. No hay autorización inferida de este documento.

Se conservan permisos y fábricas, rutas, Sol low/high, cero hijos, máximo3 simultáneas, intentos, pausa, deduplicación, revisión y aceptación. Registrar sigue sin consultar cuota ni lanzar. Las autorizaciones particulares más restrictivas continúan vigentes: el ensayo91→93 quedó detenido y no se relanza por cambiar una política ordinaria.

Pruebas de componentes:74 correctas en40.966s, sin modelos ni mensajes reales, en delegación/preguntas/puente. Revisión independiente estática de `/root/revisar_reglas_boss`: buena para preparar. La activación se documentará con el valor decidido, respaldo privado, release, hashes y comprobación posterior; hasta entonces no afirmar que Boss puede lanzar por encima de90.

Prueba adicional de integración de preguntar: configuración privada95 permite fixture94 y bloquea95 antes de registrar/ejecutar, con una prueba correcta. No se aplicó95 al VPS. Salidas: [suite](tests-politica.txt) y [caso de preguntar](test-politica-pregunta.txt).

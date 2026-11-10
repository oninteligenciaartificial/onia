# Faltantes antes de integrar o usar

**Uso real bloqueado.** Se conservó el avance local; las siguientes entradas no impiden revisar los archivos, pero sí integrar servicios o atender clientes. No se inspeccionaron cuentas ni instancias reales: presencia, permisos y vigencia permanecen desconocidos, no se declaran inexistentes.

| Falta / incertidumbre | Responsable | Siguiente acción y condición de retoma |
|---|---|---|
| Número WhatsApp de prueba y después número operativo, `phone_number_id`, WABA, app Meta y verificación del negocio si Meta la exige | Sergio, con apoyo técnico autorizado | Elegir y verificar en Meta; no copiar teléfono, IDs privados ni capturas de cuenta a esta entrega |
| Credenciales Meta: token, permisos aplicables, app secret y token de challenge; su alcance y vigencia | Sergio | Ingresarlos directamente en almacén privado/credenciales de n8n; nunca chat ni Git. Elegir versión Graph y cotejar documentación y payloads de prueba |
| Instancia y versión n8n, roles y credencial; compatibilidad Manual v1/Code v2 | Responsable técnico en un encargo posterior | Comprobar versión/esquemas con lectura autorizada. Ahora no se consultó, invocó ni importó n8n, incluso inactivo |
| Recepción de webhook: challenge GET y POST con validación criptográfica del cuerpo crudo, límites y respuesta de acuse | Desarrollo autorizado | Implementar fuera de este ensayo, verificar firma antes de proyectar mensajes y separar acuse de procesamiento. Prueba controlada autorizada antes de conectar |
| Canal privado autenticado del operador y su autorización para confirmar | Sergio + Operaciones | Definir quién concilia y cómo autentica; no reutilizar `operador-ficticio` ni un flag del cliente como autenticación |
| Persistencia transaccional, referencias únicas, cupos VIP compartidos, cola de salida y recibos de entrega | Desarrollo + Operaciones | Diseñar almacenamiento privado y probar concurrencia/caída/timeout de red. Aquí sólo hay snapshot secuencial y salidas en memoria |
| QR real, titular/destino y moneda del cobro | Sergio | Proveerlos por canal privado, guardarlos fuera de Git y verificar el destino. `QR_FICTICIO_SIN_VALOR` no es una imagen ni un medio de pago. Este paquete rechaza campos QR entrantes |
| Acceso Meet y materiales legítimos, acceso propio a Claude, coordinación de llamada VIP | Sergio | Completar en privado y comprobar con una prueba autorizada; `ACCESO_FICTICIO_NO_VALIDO` no abre nada |
| Confirmación de pago manual para cada inscripción | Sergio u operador expresamente delegado | Observar movimiento real, importe, moneda y destino, reconciliar referencia y cupo antes de emitir señal. Una captura sola no cumple |
| Condiciones comerciales: cancelación, devolución, soporte, timeout propuesto de 24 h y tratamiento de excepciones/cupos agotados tras pago | Operaciones + Sergio | Validar recorrido comercial y resolver condiciones antes de enviar textos de cobro. El sexto VIP pasa a excepción; no se cobra ni devuelve automáticamente |
| Redacción definitiva y coherencia con el kit existente | Contenido + Operaciones | Revisar `mensajes.json`; borrador actual sin aprobación. No afirmar aprendizaje, ventas ni conversiones probadas |
| Revisión técnica independiente del commit exacto | Coordinador / revisor distinto | Cerrar y revisar por el harness; recoger veredicto vigente y sólo aceptar si es bueno. Esta ejecutora no lanza sesiones ni se autoacepta |
| Sí explícito de Sergio para siguiente prueba y activación, webhook, envíos y uso real | Sergio | Autorizar alcance concreto después de revisión técnica y validación comercial de Operaciones. Este encargo no incluye importaciones ni pruebas con número real |

El adaptador real debe verificar la ventana de atención y la necesidad de plantillas/consentimiento antes de enviar por WhatsApp, así como los permisos exactos vigentes. No se fijan reglas actuales de Meta sin esa comprobación. Para timeout de entrega, no repetir a ciegas; conciliar recibos antes de otro intento. Ante cese, detener envíos y aplicar la política privada de conservación que Operaciones defina.

Orden propuesto para un encargo posterior: revisión técnica → validación comercial/editorial → sí aplicable de Sergio y entradas privadas → cotejo de versiones → construcción de adaptadores y persistencia → prueba autorizada con número de prueba → revisión de resultado → sí específico de activación. **Nada de esa secuencia se declara realizado en esta entrega.**

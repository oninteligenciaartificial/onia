# Faltantes antes de integrar o usar

**Uso real bloqueado.** Se conservó el avance local; las siguientes entradas no impiden revisar los archivos, pero sí integrar servicios o atender clientes. No se inspeccionaron cuentas ni instancias reales: presencia, permisos y vigencia permanecen desconocidos, no se declaran inexistentes.

| Falta / incertidumbre | Responsable | Siguiente acción y condición de retoma |
|---|---|---|
| Número WhatsApp de prueba y después número operativo, `phone_number_id`, WABA, app Meta y verificación del negocio si Meta la exige | Sergio, con apoyo técnico autorizado | Elegir y verificar en Meta; no copiar teléfono, IDs privados ni capturas de cuenta a esta entrega |
| Credenciales Meta: token, permisos aplicables, app secret y token de challenge; su alcance y vigencia | Sergio | Ingresarlos directamente en almacén privado/credenciales de n8n; nunca chat ni Git. Elegir versión Graph y cotejar documentación y payloads de prueba |
| Instancia y versión n8n, roles y credencial; compatibilidad Manual v1, Code v2 y HTTP Request v4.2 | Responsable técnico en un encargo posterior | Comprobar versión, configuración privada y compatibilidad del [workflow de despacho](workflow-despacho-n8n.json) con una importación de prueba autorizada. La revisión actual fue local |
| Exposición HTTPS del webhook y entrega del cuerpo crudo desde el proxy | Desarrollo autorizado | El [adaptador](ADAPTADOR.md) tiene challenge y firma local probados. Verificar la ruta y el acuse con un número de prueba autorizado |
| Acceso privado del operador y autorización para confirmar | Sergio + Operaciones | Provisionar el Bearer de operador, asignar quién concilia y probar que `/operador/*` queda inaccesible desde el proxy público |
| Almacenamiento operativo y recibos de entrega | Desarrollo + Operaciones | Provisionar carpeta privada y retención. SQLite, cupo concurrente y timeout simulado se probaron localmente. Cotejar aceptación y entrega en Meta con la prueba autorizada |
| QR real, titular/destino y moneda del cobro | Sergio | Proveerlos por canal privado, guardarlos fuera de Git, verificar el destino y cargar el QR a Meta para obtener el ID de medio privado. `QR_FICTICIO_SIN_VALOR` no es una imagen ni un medio de pago. Este paquete rechaza campos QR entrantes |
| Acceso Meet y materiales legítimos, acceso propio a Claude, coordinación de llamada VIP | Sergio | Completar en privado y comprobar con una prueba autorizada; `ACCESO_FICTICIO_NO_VALIDO` no abre nada |
| Confirmación de pago manual para cada inscripción | Sergio u operador expresamente delegado | Observar movimiento real, importe, moneda y destino, reconciliar referencia y cupo antes de emitir señal. Una captura sola no cumple |
| Operación comercial: cierre de inscripción, plazo de pago, soporte y tratamiento de excepciones/cupos agotados tras pago | Operaciones + Sergio | Aplicar la decisión de cero devoluciones y validar su comunicación. Confirmar canal humano de soporte y cuándo se deja de enviar el QR. El sexto VIP pasa a excepción; no se cobra ni devuelve automáticamente |
| Redacción definitiva y coherencia con el kit existente | Contenido + Operaciones | Revisar `mensajes.json`; borrador actual sin aprobación. No afirmar aprendizaje, ventas ni conversiones probadas |
| Revisión técnica independiente del commit exacto | Coordinador / revisor distinto | Cerrar y revisar por el harness; recoger veredicto vigente y sólo aceptar si es bueno. Esta ejecutora no lanza sesiones ni se autoacepta |
| Sí explícito de Sergio para siguiente prueba y activación, webhook, envíos y uso real | Sergio | Autorizar alcance concreto después de revisión técnica y validación comercial de Operaciones. Este encargo no incluye importaciones ni pruebas con número real |

Antes de conectar, comprobar permisos, consentimiento, plantillas requeridas fuera de la ventana de atención y política de retención. El adaptador cancela pendientes fuera de la ventana de 24 h y conserva en revisión los envíos inciertos.

Orden propuesto para un encargo posterior: revisión técnica → validación comercial/editorial → sí aplicable de Sergio y entradas privadas → cotejo de versiones → configuración privada y conexión controlada → prueba autorizada con número de prueba → revisión de resultado → sí específico de activación. **Nada de esa secuencia se declara realizado en esta entrega.**

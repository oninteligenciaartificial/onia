# Archivo documental: ONIA Platform tareas y aceptación antes del lanzamiento

> Consolidado por autorización de Sergio. Fuente: [Page original](https://chatgpt.com/space/page_160800c9076881919764ae7971519b43), secuencia **1**, actualizada 2026-11-04T20:06:30.333808Z. Este archivo conserva evidencia y borradores de esa fecha; **no es un segundo plan activo**. Las decisiones vigentes están en [PLAN](../../../PLAN.md) y los resultados en [ESTADO](../../../ESTADO.md). El texto histórico que diga «vigente», «STOP» o «no modificar Git» describe su momento original y no reemplaza la consolidación autorizada.

Los enlaces a medios/descargas se abren en la Page de origen; esos binarios permanecen en cloud. Esta copia no los incorpora ni vuelve a ejecutar sus pruebas.

---

Fecha: 4 de noviembre de 2026, America/Caracas. Dueño: agente Producto. Repo: oninteligenciaartificial/onia-platform. HEAD de master consultado: `a0488f04200b14c95caf0013043716b16efa1f1d`. Alcance autorizado: definir tareas; ninguna implementación o publicación queda iniciada.

La recomendación es validar primero un único recorrido de consultorio dental, con propietario ADMIN: alta confirmada → configuración manual → paciente y cita persistidos → pago de suscripción por QR/comprobante → aprobación → nueva sesión con acceso operativo. El resultado comercial es que un dueño pueda ordenar su primera atención y conservar acceso después de pagar. El cobro de una factura del paciente es otro circuito y no sustituye el pago de la suscripción.

# Estado comprobado y criterio de lanzamiento

| Etapa | Existente en código | Estado de aceptación |
| --- | --- | --- |
| Alta y acceso | Registro, confirmación de correo, login, perfil ADMIN y gates MFA | Tests presentes; runtime de este HEAD no probado aquí. Apertura del alta depende de configuración; no se conocen valores desplegados |
| Primer resultado dental | Onboarding manual, tratamiento/precio, paciente, cita y odontograma | E2E escrito con persistencia; no ejecutado aquí |
| Suscripción manual | Checkout, QR estático, comprobante privado, revisión y aprobación administrativa | QA presente; tiene una aserción incompatible con la rama vigente del checkout |
| Suscripción BCP dinámica | Generación, Consult, callback y activación | Tests con mocks; falta aceptación integrada del mismo candidato con proveedor simulado |
| Acceso posterior | Perfil/plan y gates existentes | Falta demostrar en el mismo recorrido alta→primer resultado→suscripción→reentrada y operación dental |

No se comprobó un bug runtime del producto. “Existente” significa ruta o test leído; “propuesto” son las tareas inferiores; “roto” no está acreditado. El desfase de QA es estático, no un fallo reproducido de producción. La declaración comercial de v1.0 en [docs/ONIA_PLATFORM.md](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/docs/ONIA_PLATFORM.md) tiene fecha junio y no certifica este despliegue. [README.md](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/README.md) sigue describiendo SaaS dental; el código E2E ya cubre cinco rubros. El build real de [package.json](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/package.json) usa webpack aunque AGENTS mencione Turbopack.

**Done del recorrido antes de lanzar:** un reporte del mismo SHA de snapshot, build e imagen/proceso demuestra alta confirmada, paciente/cita conservados tras recarga, pago sintético pendiente sin activación indebida, aprobación que habilita el plan una sola vez y nueva sesión ADMIN que recupera esos datos y realiza una operación permitida. Las solicitudes sin sesión o de un tenant ajeno deben denegarse sin exponer esos datos. Un recibo subido, un test mockeado o una captura de dashboard no satisfacen por separado este criterio. La aprobación bancaria real y la operación comercial de producción requieren validación aparte; no se declaran cubiertas por QA simulada.

# Backlog propuesto de seis tareas

Son fichas para asignar en un encargo posterior, no issues creados. P1 indica puerta de aceptación pendiente; no implica incidente productivo.

## 1 P1 Fijar candidato y perímetro QA verificable

**Owner:** Infra/QA, revisión Security. **Objetivo comercial:** evitar aceptar una demo distinta del producto que se pretende ofrecer.

**Hueco y rutas:** [scripts/qa-v1/prepare.mjs](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/scripts/qa-v1/prepare.mjs), [scripts/qa-v1/topology.mjs](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/scripts/qa-v1/topology.mjs), [e2e/v1/entorno.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/e2e/v1/entorno.ts) y [playwright.v1.config.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/playwright.v1.config.ts). Existen snapshot, huella y opt-in; localhost y configuración estática no prueban aislamiento. Esta VM tiene el harness, no un checkout con dependencias de Platform.

**Entradas y dependencias:** commit fijado, capacidad de ejecución aislada autorizada en otro encargo, recursos locales nuevos, datos sintéticos y configuración sin servicios reales. Es prerequisito de 2–4 y 6.

**Resultado y Done:** manifiesto único con SHA256 de fuentes, build e imagen/proceso, namespace y mounts comprobados, DB marcada de QA, Auth/Storage/Mailpit locales y egreso bloqueado. No reutilizar QA remoto ni volúmenes de clientes.

**Prueba de aceptación:** verificar identidad del paquete y del runtime por separado; rechazar destino externo, candidato distinto, DB sin marca o namespace con salida antes de efectuar escrituras. Registrar salud de servicios sin imprimir credenciales. El check estático ejecutado abajo es un avance documental, no este Done.

## 2 P1 Validar alta dental hasta primer resultado y reentrada

**Owner:** QA, revisión Backend/Security. **Objetivo comercial:** el nuevo dueño obtiene una cita guardada y puede volver a trabajar con ella.

**Hueco y rutas:** [e2e/v1/cinco-rubros.spec.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/e2e/v1/cinco-rubros.spec.ts) ya hace alta, onboarding y operación dental, pero el caso es largo y su comprobación final de aislamiento acumula cinco cuentas. No vuelve a iniciar sesión después del primer resultado para comprobar su continuidad. Reutilizar [e2e/v1/operaciones.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/e2e/v1/operaciones.ts) y helpers de sesiones; no inventar funciones clínicas nuevas.

**Entradas y dependencias:** tarea 1; dos organizaciones sintéticas, rol ADMIN, horario y tratamiento/precio definidos, correo onia.invalid capturado en Mailpit.

**Resultado y Done:** caso dental corto que conserva el conjunto original de pruebas y reúne alta confirmada → onboarding manual → paciente/cita → recarga → contexto nuevo/login → mismos datos.

**Prueba de aceptación:** verificar role y organizationId, IDs y contenido persistidos; API privada deniega sin sesión y no entrega el paciente/cita de la otra organización. No simular las APIs de negocio ni llamar proveedores externos. Odontograma queda opcional para no retrasar el primer resultado.

## 3 P1 Cerrar QR estático y comprobante hasta acceso operativo

**Owner:** QA Billing, revisión Security. **Objetivo comercial:** que el dueño sepa cuándo su pago está en revisión y cuándo dispone del plan comprado.

**Hueco y rutas:** [scripts/qa-v1/payment-ui-runtime.mjs](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/scripts/qa-v1/payment-ui-runtime.mjs) línea 221 exige “Pedir los datos de pago por WhatsApp”; [app/checkout/CheckoutClient.tsx](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/checkout/CheckoutClient.tsx) línea 668 elige antes QR estático vigente, y la rama WhatsApp está después. Existe un desfase de aserción para esa condición. El recorrido de cinco rubros sólo navega al checkout sin pagar suscripción; el QA de pagos no demuestra una operación dental después de aprobar.

**Entradas y dependencias:** 1 y 2; imagen/comprobante sintéticos, comprador ADMIN y aprobador sintético separado, precio/ciclo del servidor y Storage/SMTP aislados. No escanear ni pagar el QR bancario real.

**Resultado y Done:** QA alineada con rama QR vigente y expiración, más continuidad del mismo dueño desde comprobante hasta reentrada y operación dental. No cambiar precio, schema ni método de cobro por esta tarea.

**Prueba de aceptación:** comprobante → PENDING y estado visible tras recarga; no activar por subir archivo; aprobación autorizada → plan/ciclo correctos; rechazo no activa; aprobación repetida no duplica ciclo; otra org/rol no revisa ni lee el comprobante; nueva sesión conserva paciente/cita y puede crear una cita permitida. Distinguir limitaciones del trial de las del plan, sin exigir bloqueo de acciones que el trial sí permite.

## 4 P2 Condicional Validar QR dinámico con proveedor simulado

**Owner:** QA Backend Billing. **Objetivo comercial:** sostener la promesa de activación automática sólo si se elige ofrecer ese circuito.

**Hueco y rutas:** [app/api/subscription-payment/bcp-qr/route.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/api/subscription-payment/bcp-qr/route.ts), [app/api/webhooks/bcp/route.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/api/webhooks/bcp/route.ts) y tests adyacentes; [app/api/dev/bcp-mock/[...path]/route.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/api/dev/bcp-mock/[...path]/route.ts) devuelve 404 en production. El mock dev no acepta por sí solo un build production.

**Entradas y dependencias:** 1 y 2, contrato Generated/Consult, simulador separado dentro del namespace loopback, valores ficticios y avisos capturados localmente. Se difiere si el primer lanzamiento usa sólo revisión manual.

**Resultado y Done:** escenario del mismo build que genera QR sintético, valida Consult y activa una sola vez, seguido de reentrada y operación dental. Sin cuenta bancaria real.

**Prueba de aceptación:** 401/403 según sesión/permiso, importe cliente ignorado, error del proveedor sin pago persistido, Basic inválido/Consult fallido/monto o referencia ajenos sin activación, QR reemplazado rechazado y callbacks repetidos/concurrentes con un solo ciclo. Cero egreso y avisos externos. Esto no acredita interoperabilidad con BCP real.

## 5 P2 Completar negativos de confirmación de correo

**Owner:** QA Auth; revisión Security. **Objetivo comercial:** evitar un alta que parezca exitosa cuando el enlace ya no sirve y proteger el retorno al producto.

**Hueco y rutas:** [app/auth/confirm/route.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/auth/confirm/route.ts) tiene ramas de token/tipo inválido y OTP fallido. [app/auth/confirm/route.test.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/auth/confirm/route.test.ts) sólo cubre una invitación y reemplaza sanitizeOauthNext por una identidad.

**Entradas y dependencias:** checkout/dependencias del candidato en futuro encargo; independiente de servicios y de 1–4. Supabase simulado; sanitizador real o contrato integrado con [lib/oauth-redirect.test.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/lib/oauth-redirect.test.ts).

**Resultado y Done:** cobertura de esas ramas sin cambiar la lógica salvo reproducción posterior de un defecto.

**Prueba de aceptación:** token ausente/tipo inválido → enlace_invalido sin verifyOtp; error OTP → enlace_vencido; destinos por tipo correctos; next externo o protocol-relative nunca redirige fuera; next local válido conserva contrato. Ejecutar tests focales y registrar resultado nuevo, sin heredar verdes de otro commit.

## 6 P2 Preparar demostración de workshop con promesa separada

**Owner:** Producto y facilitador; QA revisa evidencia. **Objetivo comercial:** mostrar un resultado concreto sin vender una suscripción como si fuera aprendizaje de IA.

**Hueco y rutas:** [e2e/v1/cinco-rubros.spec.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/e2e/v1/cinco-rubros.spec.ts) y [e2e/v1/operaciones.ts](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/e2e/v1/operaciones.ts) respaldan un flujo operativo dental, no un resultado pedagógico de IA. [README.md](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/README.md) describe el SaaS; esta lectura no acredita un curso, programa ni experiencia educativa de IA.

**Entradas y dependencias:** 1 y 2 aprobadas; dataset ficticio, guion de demostración y objetivo educativo definido por el facilitador. El pago sólo se muestra simulado y fuera de la promesa educativa.

**Resultado y Done:** guion breve que muestra tratamiento → paciente → cita → recarga/reentrada; opcional odontograma. Separar “usar ONIA para gestionar” de “aprender IA”. La venta SaaS tiene CTA y condiciones propios; no hacer de comprar ONIA un resultado de aprendizaje.

**Prueba de aceptación:** ensayo sobre el candidato validado, una persona puede repetir el resultado con datos sintéticos. Si el workshop promete enseñar IA, exigir además un ejercicio de entrada→uso de IA→salida evaluable y criterio propio; no atribuirlo a Platform sin comprobarlo. Sin esta entrada, la demo queda identificada como muestra de gestión, no como clase de IA.

# Dos decisiones de producto para Sergio

1. **Primer usuario y resultado:** recomiendo propietario ADMIN de consultorio dental y paciente+cita persistidos. README y el recorrido clínico ya lo respaldan; evita extender de entrada cinco rubros. Decidir si ése será el primer segmento comercial.

2. **Primer cobro ofrecido:** recomiendo QR estático/comprobante con revisión humana explícita para el primer candidato, y diferir la promesa automática BCP hasta tarea 4 y validación aplicable del proveedor. Decidir manual frente a automático según operación realmente disponible; esta revisión no conoce configuración desplegada.

# Check ejecutado y límites de evidencia

En esta VM se ejecutó `node --check` sobre copia exacta de [scripts/qa-v1/topology.mjs](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/scripts/qa-v1/topology.mjs) y su función existente `createQaCompose` con runId y candidateId ficticios, sin modificar la fuente. Resultado: sintaxis válida; ocho servicios (namespace, DB, Mailpit, gateway, Auth, Storage, app, browser); namespace `none`; todos los demás comparten ese namespace; cero puertos publicados y redes adicionales. No se crearon servicios, secretos ni DB. Es evaluación de configuración en memoria, no prueba de aislamiento runtime ni prueba espejo implementada.

No hay checkout ni node_modules del producto en esta VM; sí dependencias del harness. No se ejecutaron npm test/build de Platform ni el recorrido E2E. Fuente fijada por GitHub GET, no prueba de estado desplegado. Lecturas confirmadas: AGENTS, README, package, skill routing, coordinación, orquestación, backlog y rutas/tests mencionados. Herramientas: GitHub, Node existente, dos subagentes de lectura y Pages. Skill directora desarrollar-y-verificar; write-page para entrega. No se introdujo dependencia ni API nueva que requiriera investigación externa.

Sólo se definieron tareas y se guardó esta entrega. Sin cambios Git/issues externos, producto, reglas/skills, secretos, clientes, DB o producción. ONIA-CENTRAL no consultado. El lanzamiento sigue sin aceptación de punta a punta; no se afirma que el producto esté roto.



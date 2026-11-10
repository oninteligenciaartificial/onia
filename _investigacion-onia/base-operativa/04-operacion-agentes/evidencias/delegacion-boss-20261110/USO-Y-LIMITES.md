# Delegación Boss → harness

10 noviembre2026. Sergio pidió que Boss registre y lance nuevas tareas sin depender de un permiso manual de Codex por trabajo. Se extiende el mismo harness, con una política local revocable. No hay scheduler: Boss elige y solicita; nada arranca por registrar una ficha.

## Qué habilita

Seis fábricas: `guiones`, `edicion`, `automatizaciones`, `whatsapp`, `codigo`, `plataforma`. La última documenta infraestructura/panel existente; no habilita desarrollar OnIA Platform. Cada ID recibe una subcarpeta exclusiva dentro de su fábrica; el cliente no puede elegir rutas, modelo, hijos ni permisos. Sol6.1, low/high, cero hijos y tres sesiones globales incluidos revisores.

La autorización local permanece hasta revocarla. Cada permiso de tarea vence a las24h y Boss puede renovarlo por `habilitar` sin ampliar alcance ni recuperar operaciones revocadas. Máximo seis altas por día UTC y dos sesiones por tarea: ejecución y revisión distinta. `reanudar` no está delegado: una interrupción exige conciliar el intento para preservar el cupo del revisor. Repetir una solicitud idéntica con el mismo nonce devuelve el resultado; cambiar el contenido con el mismo nonce se rechaza. Si una operación quedó incierta, no probar con nuevos nonces.

El lanzamiento requiere una muestra de cuota Codex semanal de menos de2h y menos de90% usado. Reserva10 puntos del total semanal; no es saldo adicional ni estimación por tarea. Cuota ausente/vieja o tope alcanzado bloquea el lanzamiento, no habilita API paga. Tras el vencimiento de Codex los scripts siguen disponibles, los agentes no.

## Protocolo para Boss

Usar la misma llave restringida y comando remoto `onia-harness-v1`, JSON por stdin. No shell ni acceso a configuración. Primero publicar en master un `.md` de `04-operacion-agentes/pendientes/` con exactamente un bloque `onia-pedido-v1` y los seis campos `id`, `fabrica`, `objetivo`, `entregable`, `aceptacion`, `esfuerzo`. Cada texto máximo2200 caracteres. La solicitud debe coincidir exactamente con ese bloque, que se conserva como evidencia inmutable.

```json
{"version":1,"operacion":"registrar","id":"fabrica-codigo-ejemplo","solicitud":"alta-ejemplo-1","fabrica":"codigo","objetivo":"Resultado concreto","entregable":"Archivo y comprobación","aceptacion":"Criterio verificable","pedido":"04-operacion-agentes/pendientes/PEDIDO-EJEMPLO.md","esfuerzo":"low"}
```

El ejemplo no es una tarea autorizada ni existe esa ficha. La respuesta real trae `tarea.revision`, commit en master, permiso y `sesion_lanzada:false`. Después consultar y usar el número actual, nunca una revisión vieja:

```json
{"version":1,"operacion":"consultar","id":"guiones-tanda-20261111"}
{"version":1,"operacion":"ejecutar","id":"guiones-tanda-20261111","solicitud":"inicio-guiones-1","revision_esperada":3}
{"version":1,"operacion":"habilitar","id":"guiones-tanda-20261111","solicitud":"renovar-guiones-1","revision_esperada":3}
```

Conservar `solicitud` para reintentos de la misma operación. La revisión3 sólo vale inmediatamente después de registrar; consultar antes de operar. Cerrar, revisar y recoger usan el mismo protocolo previo y CAS. Al cerrar se comprueba commit en origin y cada commit de la entrega: sólo archivos regulares en la ruta asignada, sin borrados, renombres fuera de ruta, enlaces ni archivos de control. El revisor es otra sesión. `recoger` publica el veredicto; el fin de cada sesión emite el webhook existente. HTTP200 acredita recepción técnica, no lectura/revisión de Boss.

No hay `aceptar` ni merge arbitrario remoto. Boss trae el veredicto; integración/aceptación siguen con los controles del harness y un revisor distinto. Esta ampliación elimina crear permisos a mano, no convierte a Boss en administrador del VPS.

## Seguridad y parada

No producción/n8n real (ni importar JSON inactivo), envíos, publicaciones comerciales, pagos, nuevas APIs, instalaciones, PC, secretos o QR reales. Los workflow JSON se entregan como archivos `active=false`. El código/plano/documentación autorizado sí se publica en GitHub. Reutilizar panel y cerebro, no investigar de nuevo. No cambios de sandbox/AppArmor/userns.

La llave y el protocolo limitan operaciones administrativas; la ejecutora conserva el sandbox/red/credenciales existentes. No es aislamiento completo frente a todas las herramientas del usuario. El control de commits actúa al cerrar: no puede deshacer una acción previa ni impedir una fuga antes del push. No atribuirle garantía de cero efectos externos; las reglas de ejecución siguen siendo obligatorias y toda acción sensible requiere Sergio.

Para revocar, el coordinador cambia `delegacion_fabricas.activa` a false bajo el lock del puente. Bloquea altas, renovaciones y nuevos lanzamientos; permite recoger/cerrar trabajo ya producido. `pausado=true` frena escrituras del puente más ampliamente. Revocar un permiso particular conserva evidencias e intentos; renovar no restaura permisos. No matar sesiones ni borrar llaves/tareas. Código fijado a commit revisado; no autoactualizar desde master. Reversión: desactivar delegación, conservar registros y restaurar wrappers/manifest desde respaldo privado sólo sin sesiones vivas. No volver a abrir shell ni retirar límites para resolver un bloqueo.

## Pendiente operacional

Boss debe comprobar registrar/consultar/lanzar desde su extremo con su llave. Las pruebas locales del adaptador no sustituyen esa confirmación. El homelab requiere aplicar la [retoma revisada](../../homelab/RETOMA-REVISADA-20261110.md) en la PC de casa y verificar aislamiento/huella/conexión; no quedó operativo por publicar el instalador.

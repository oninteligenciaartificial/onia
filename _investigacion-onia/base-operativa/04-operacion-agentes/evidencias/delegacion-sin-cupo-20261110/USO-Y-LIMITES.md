# Registro delegado sin cupo diario de altas

10 noviembre 2026, America/La_Paz. Sergio pidió retirar el límite de seis tareas nuevas por día y cerrar ese pendiente antes de avanzar con ventas. Se extiende el puente existente, sin otro registro de tareas.

## Cambio vigente

`registrar` ya no rechaza solicitudes por haber alcanzado seis altas en el día UTC. No hay que esperar a las 20:00 o 20:10 de La Paz para registrar otra tarea. Se conservan las reservas por ID, fecha, solicitud y evidencia anteriores: la fecha sigue siendo trazabilidad, no cupo.

El contrato histórico [delegacion-boss-20261110/USO-Y-LIMITES.md](../delegacion-boss-20261110/USO-Y-LIMITES.md) permanece intacto por ser evidencia registrada. Esta actualización sustituye **únicamente** su máximo de seis altas diarias y las referencias históricas a esa espera, incluida la cola de Boss. Los demás controles siguen vigentes.

## Controles conservados

- Delegación activa, pausa/revocación, seis fábricas permitidas, Sol 6.1 low/high, cero hijos y rutas exclusivas.
- Pedido publicado en master y coincidente con la solicitud; identidad, revisión esperada y permisos acotados.
- Reserva por ID, rechazo de altas parciales sin conciliar, repetición idempotente de la misma solicitud y rechazo de una solicitud alterada.
- Registro y publicación de la tarea antes de habilitar su uso. Registrar **no lanza** una sesión ni hace que arranque al liberarse un cupo.
- Máximo actual de tres sesiones simultáneas, incluidos revisores y consultas `preguntar` mientras responden. No es un máximo de hardware demostrado.
- Lanzamiento delegado con cuota semanal comprobada de antigüedad menor de dos horas y usada menor del 90%. El 90% es una reserva operativa del puente, no agotamiento del proveedor. No se modifica en este encargo.
- Caducidad e intentos por tarea, cierre remoto, revisor distinto, recogida del veredicto y aceptación separados.

No amplía producción, n8n, envíos, gasto, acceso a PC ni secretos. `preguntar` conserva sus límites propios, distintos del registro de tareas.

## Uso para Boss

Usar el mismo comando SSH restringido `onia-harness-v1` y el mismo JSON de `registrar`. Si un intento fue rechazado antes de reservar y no existe su registro, conciliar el ID y repetir esa solicitud. Si ya está registrado, consultar y continuar dentro del permiso. No crear un duplicado para eludir incertidumbre, eliminar auditoría o cambiar de carpeta de operación.

La rutina anunciada para las 20:10 no fue editada desde Codex. Esa hora ya no es necesaria por cantidad de altas. Si se ejecuta, primero debe comprobar trabajo e intentos existentes y el control vigente de cuota; no duplicar tareas ni prometer que iniciará una sesión. Este arreglo no acredita que Boss haya procesado un aviso ni que exista un scheduler.

## Publicación, instalación y reversión

El código publicado se instala como nueva release privada: un push por sí solo no cambia la entrada SSH. El recibo de instalación identifica el commit y hashes probados. Se conservan releases, entradas y manifiestos previos; no se cambian configuración, claves, webhook, servicios, n8n ni el checkout sucio.

Reversión, sólo si hiciera falta: tomar el mismo lock del puente, comprobar la versión activa y restaurar las entradas y el manifiesto desde el respaldo de esta instalación, conservando también la versión sustituida. No restaurar configuraciones o claves completas ni borrar registros. La versión anterior volvería a imponer seis altas; no revierte registros ya publicados.

## Concurrencia: medición separada

El [plan F1 existente](../../homelab/F1-MEDICION.md) sigue siendo propuesta, no comando instalado ni resultado. Eliminar seis altas no valida cuatro o cinco sesiones ni configura reparto al homelab. El ensayo real necesita observación, perfil, presupuesto y autorización compatibles con el control de cuota. Las pruebas sintéticas de este cambio no dimensionan el VPS o la PC.

La lectura inicial fue 90% usado a `2026-11-10T23:08:11.742Z` (19:08 La Paz). Por el control vigente no se lanza el ensayo real ni una tarea comercial para validar este arreglo. No se elimina silenciosamente esa reserva ni se presenta como una restricción del proveedor.

## Resultado posterior

La release quedó instalada y comprobada. Sergio autorizó después un ensayo acotado de 91% a 93%, exclusivamente para medir; no se ejecutó porque la revisión detectó un control insuficiente del presupuesto. Los límites ordinarios no cambian. Evidencia y dictámenes separados en [INSTALACION.md](INSTALACION.md).

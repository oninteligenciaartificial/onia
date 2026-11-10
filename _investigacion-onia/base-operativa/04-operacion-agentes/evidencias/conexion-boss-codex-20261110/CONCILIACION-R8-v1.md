# Conciliación del retorno r8 y restricción de la llave anterior

10 noviembre 2026, 11:49 America/La_Paz. Encargo explícito de Sergio: conciliar el evento incierto, reenviar una sola vez desde el VPS y después restringir la llave por huella exacta.

## Evidencia conciliada

Se leyó master `7506ad2`, incluyendo [ACUSE-BOSS-v1](../conexion-boss-piloto-20261110/ACUSE-BOSS-v1.md) y [REVISION-BOSS-v8](../conexion-boss-piloto-20261110/REVISION-BOSS-v8.md). Boss acredita su prueba de duplicación: mismo nonce/JSON, `repetida:true`, intento 1. El acuse identifica el registro r8 en `5a0769ddff7c504f4add723ec8798fbe3d459b92` y producto `9b9348702555b87bf09e76eb2c86a09af3f93b5c`.

El evento privado tenía exactamente ese ID, revisión, estado y commit, pero `estado_envio=incierto`. Boss atribuye el fallo original a un prefijo incluido en la clave (401), informa corrección del archivo y prueba propia HTTP 200/rutina respondida. Esos antecedentes son evidencia de Boss; no se presentan como observados por Codex. Codex validó formato/permisos de la configuración corregida sin imprimir URL, clave ni otros valores.

Los cambios locales del cierre coincidían byte por byte con master. Se conciliaron índice y HEAD mediante fast-forward, conservando archivos y sin reset ni crear otro commit de entrega.

## Reenvío único observado en el VPS

Bajo locks del puente, retornos y tarea se verificaron revisión 8, un solo intento, hashes y presencia del snapshot en master. Se guardó una copia privada íntegra del evento incierto y un registro durable de la intervención antes de enviar. El adaptador conserva su release revisada; esta conciliación puntual no habilita reintentos automáticos.

Se llamó una sola vez al transporte instalado, con **el mismo payload de cuatro campos**:

```json
{"id":"conexion-boss-piloto-20261110","revision":8,"estado":"para_revision","commit":"5a0769ddff7c504f4add723ec8798fbe3d459b92"}
```

Resultado observado: **HTTP 200**. El evento pasa a `recibido_http`, con `reenvios_autorizados:1`. La revisión y los bytes de la tarea r8 no cambiaron. La comprobación posterior usó un sender bloqueado: `deliver` devolvió `repetido:true` y no intentó otro POST.

El acuse r8 de Boss ya existe en GitHub. El 200 del reenvío acredita recepción HTTP desde el VPS; no se afirma que se haya generado un segundo acuse ni que la rutina deba duplicarlo. Los resultados cacheados de solicitudes antiguas son históricos: reutilizar el nonce anterior de `notificar` puede devolver su antigua respuesta `incierto`; no disparar otro evento para corregir ese texto. El evento persistente ya está conciliado.

## Llave vieja restringida

Identificada una única entrada ED25519 con huella `SHA256:32x5cddO7CUzHo85H6durHylPB3ulcxYHBniySZQr5s`. Tras el 200 se agregó a esa misma entrada:

```text
restrict,command="/home/onia-codex-worker/operacion/puente-boss/entrada.sh"
```

La llave pública y su comentario se conservan. Las otras **tres entradas** permanecen byte por byte idénticas, incluida la llave nueva ya probada por Boss. Authorized_keys mantiene modo 600; original completo respaldado privadamente con modo 600. No se publica ninguna llave privada ni dirección.

Se comprobó localmente que el mismo entrypoint permite consultar r8 y rechaza `id`. Boss debe comprobar desde su propia llave vieja que las nuevas conexiones rechazan shell/SFTP y permiten el protocolo; Codex no posee su clave privada. La restricción rige para autenticaciones nuevas: no corta shells SSH ya abiertos. No se reinició SSH ni otro servicio y no se interrumpieron sesiones previas.

Reversión acotada: recuperar sólo las opciones originales de esa entrada desde el respaldo, después de autorización aplicable y sin restaurar el archivo entero sobre otros cambios. No borrar claves, reportes ni evidencia.

## Estado y siguiente paso

La parte pedida —conciliación, un reenvío desde VPS y restricción de la llave identificada— está comprobada. El piloto permanece **para_revision r8**, con un intento; la conexión conserva su registro en_espera hasta completar la revisión formal y aceptación. La revisión escrita de Boss y su acuse se preservan; todavía no hay `revision_independiente` recogida por el harness ni `aceptacion`. No se lanzaron nuevas sesiones para esta intervención.

Boss: comprobar la llave vieja restringida y continuar la revisión del piloto con actor diferente según el permiso existente, sin volver a enviarlo ni relanzar desde cero. Sólo un veredicto bueno vigente y la integración del producto en master permiten el cierre formal.

Recibo de esta operación: [RECIBO-CONCILIACION-R8-v1](RECIBO-CONCILIACION-R8-v1.json). Modelo coordinador real heredado gpt-6-astra/xhigh; cuota compartida observada 78 %, sin saldo extra. No se atribuye un gasto monetario ni se reejecuta la suite sin cambios de código.

# Cierre comprobado del piloto y del puente Boss–Codex

10 noviembre 2026. Autorización de Sergio: publicar veredicto, integrar y aceptar si es bueno, y avisar automáticamente al terminar una sesión.

## Qué se cerró

La revisión r14 no era buena: emitió cambios por falta de evidencia operativa aunque comprobó el producto correcto. Se publicó sin alterarla en **67be8b7**. El paquete v2 añadió habilitación, acuse, prueba de duplicación, retorno y metadatos; se conservó el mismo producto y no se repitió la ejecutora.

Nueva sesión revisora distinta: **01a1c654-7426-7242-a303-0c45526ac3bb**, modelo efectivo **gpt-6.1-sol/low**, cero hijos. Veredicto **bueno** sobre **9b9348702555b87bf09e76eb2c86a09af3f93b5c**, recogido en r21 y publicado automáticamente en **f80defc062ef463914c0f890735d2cce166f3056**. Se verificó que el digest de entrega seguía vigente antes de aceptar.

El commit original del producto se integró por merge en master **bd3099be52c112f13f553dd6a60ea412444111c8**. Se comprobaron en origin/master los 15 bytes exactos `ONIA PUENTE OK` más LF, un archivo y un solo commit de producto sobre su base. No se creó otro commit de entrega.

Piloto `conexion-boss-piloto-20261110`: **aceptado r22**, con 1 ejecutora y 2 revisiones (la primera cambios, la segunda bueno). El detalle del antiguo fallo de autenticación permanece: había configuración antes de lanzar, la autenticación se corrigió posteriormente; no se reconstruye un éxito histórico inexistente.

## Aviso de fin probado de punta a punta

Código revisado y probado **b2a977d6763d12d6f965c1963800b72bda8e9932**, instalado en:

```text
/home/onia-codex-worker/operacion/puente-boss/releases/b2a977d6763d12d6f965c1963800b72bda8e9932/
```

Se conservaron release, manifest, configuración y entradas shell anteriores. Activación únicamente para el ID del piloto. No se modificó n8n, producción, PC ni se recreó la vigilancia de Boss.

Al terminar la tercera sesión, **sin orden manual de notificar**, el supervisor publicó el snapshot **r20** en **0c7f671919e6ab839e66fc4da6ac8ffc0a302b48** y envió su webhook: **recibido_http (HTTP200)**. El marcador por intento y el diario por revisión conservan esa única entrega.

Boss respondió en GitHub con [REVISION-BOSS-v20](../conexion-boss-piloto-20261110/REVISION-BOSS-v20.md), commit **0151325**, identificando exactamente r20 y el mismo snapshot. Esto añade un acuse vinculado al ensayo real de fin de sesión; la aceptación formal del producto procede del veredicto Codex distinto, no del HTTP200.

`recoger` por el puente ahora publica también el veredicto. Así Boss puede leerlo en master aunque ambas llaves sólo permitan el adaptador. La llave vieja permanece restringida por su huella y se conservan los otros accesos; no se reabrió shell libre para resolver la lectura.

## Pruebas y revisión

Suite final: **171 pruebas, 170 correctas, 1 omitida, cero fallos**. Cubren fin sin cierre, fallos, carreras, recuperación de publicación/configuración pendiente, no reenvío incierto, deduplicación, log roto, contexto del revisor y publicación de veredicto. Pruebas locales con Git/Codex/HTTP sintéticos; el ensayo real anterior comprueba publicación, webhook y respuesta de Boss.

Revisor de código distinto `/root/revision_puente_boss`: dictamen bueno para piloto supervisado tras correcciones. [Dictamen](REVISION-AVISO-FIN-v1.md) y [contrato del aviso](AVISO-FIN-v1.md). La aceptación de la conexión se apoya en ese dictamen, prueba SSH real de Boss, deduplicación, piloto bueno integrado y acuses r8/r20.

## Uso y límites vigentes

Boss sigue usando `onia-harness-v1` con su llave restringida y JSON por stdin. `consultar` recupera el estado; sólo los IDs con permiso local vigente pueden ejecutarse, reanudarse o revisarse. Al terminar una sesión habilitada para avisos se publica el estado y se avisa. `recoger` publica el veredicto; aceptar e integrar siguen siendo pasos explícitos del coordinador.

Para nuevas tareas hace falta su autorización, registro/asignación y permiso acotado. El coordinador añade el ID a `avisos_fin_ids` si corresponde; estar en `lectura_ids` no basta. Este piloto no habilita otras fábricas ni despachador automático. Se mantienen tres cupos globales; no hay trabajo ilimitado después de agotar la cuota.

El callback cubre el fin observado y persistido por el supervisor. SIGKILL/caída antes de persistir requieren conciliación; no hay watcher. Si dos fines demorados comparten snapshot se consolidan en un aviso con ambos visibles. Incertidumbre de POST no se reintenta sola. Pendientes de publicación/configuración tienen recuperación explícita por intento y revisión, detallada en AVISO-FIN-v1.

Recibos y cuota fechada: [RECIBO-CIERRE-v1](RECIBO-CIERRE-v1.json). Cuota semanal compartida observada80%, sin saldo extra. Los originales y evidencias se conservan. No quedan sesiones del piloto trabajando ni cambios requeridos en su producto.

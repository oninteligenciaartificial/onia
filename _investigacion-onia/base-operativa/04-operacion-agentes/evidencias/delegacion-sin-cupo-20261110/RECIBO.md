# Recibo: eliminación del cupo diario de altas

10 noviembre 2026, America/La_Paz. Encargo directo de Sergio: retirar el límite de seis altas y cerrar el pendiente técnico antes de ventas. Referencia documental `delegacion-sin-cupo-20261110`; no se crea un ID ficticio en el registro real para probarlo.

## Cambio y comprobación

- Base: `a02fb0dd5bc1e4f5d75f597a6d11a33cf068bdfb`. El commit de código es el que incorpora este recibo; el recibo de instalación posterior fijará su hash exacto y la versión activa.
- Runtime: sólo `harness_delegacion.py` cambia respecto de la release instalada previamente. Se elimina el conteo/rechazo diario y se conservan fecha, reservas, permisos y controles de lanzamiento.
- Dos casos nuevos contra código anterior: ambos rechazados por el límite diario. Contra el arreglo: ambos pasan. [Base](regresion-base-v2.txt), [corregido](regresion-corregido-v2.txt).
- Suite final: 160 pruebas, cero errores, cero fallos, cero omitidas, 104.789 segundos. [Salida](tests-v2.txt), [resumen](tests-v2.json). Incluye delegación, puente/retorno, preguntar, sesiones, trabajo y harness.
- Comando reproducible desde la raíz: `PYTHONPATH=_investigacion-onia/base-operativa/05-herramientas/scripts python3 -m unittest -v test_harness_delegacion test_harness_boss test_harness_preguntas test_harness_sesiones test_trabajo test_harness`.
- En esta ejecución se conservó adicionalmente el contenido de los TemporaryDirectory al cerrar los fixtures. Git remoto y Codex fueron ficticios en los tests; ninguna prueba lanzó una sesión real ni envió un webhook real.
- Controles verificados: ocho pedidos publicados en un mismo día; conservación de seis reservas anteriores; duplicado sin nuevo registro/commit; reservas incompletas, permisos y rutas; tres cupos/rechazo de una cuarta; cuota 90%; cierre, revisión e idempotencia del puente.
- `git diff --check`, compilación de los dos archivos Python y `bash -n` de entrada/configurador del puente: correctos. No se cambiaron esos scripts shell en el repo.

## Roles, uso y retrabajo

Ejecutor: conversación coordinadora de Codex; modelo/esfuerzo observado unknown en el recibo. Revisor distinto: sesión existente `/root/revisar_reglas_boss`, solicitado Sol 6.1 low, observado unknown; dictamen técnico bueno. La revisión pidió fijar el reloj del test y conservar el contrato histórico, ambos atendidos.

Cuota compartida inicial: 90% usado, `2026-11-10T23:08:11.742Z`. Cuota por rol y consumo atribuible: unknown. La lectura final se incorpora al recibo de instalación si está disponible; no inventar USD ni gasto por proceso. No se ejecutó una nueva sesión delegada: pruebas con fixtures y revisión breve de cierre en la sesión revisora existente.

Intentos: una implementación, dos corridas de regresión y dos corridas de suite durante la corrección de fixtures. Retrabajo: sí; se publicó la fuente de ocho pedidos antes de registrar, se corrigió la lista de módulos y se fijó el reloj. Incidentes registrados en [registro-de-errores.md](../../registro-de-errores.md).

## Límite de este resultado

Veredicto técnico bueno sobre el cambio no significa aceptación de tareas comerciales. La instalación se verifica aparte. Medir cuatro/cinco sesiones reales y demostrar la rutina de Boss siguen sin acreditarse: el control actual de reserva de cuota bloquea nuevos lanzamientos al 90%. Ese guard es del puente, no agotamiento del proveedor. No se alteró silenciosamente ni se declara medida una capacidad a partir de tests ficticios.

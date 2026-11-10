# Comparación resuelta con la evidencia de Boss

10 noviembre 2026 · America/La_Paz · ID `conexion-boss-codex-20261110`.

**Recomendación vigente de Codex: A, SSH restringido + webhook de retorno, para el primer piloto.** Sustituye únicamente la preferencia provisional por B de [COMPARACION-TRANSPORTES-v1.md](COMPARACION-TRANSPORTES-v1.md), conservada como investigación anterior al informe de Boss. No es aceptación de la conexión ni autorización para activar servicios.

## Evidencia que cambia la elección

Boss publicó su [revisión independiente](REVISION-BOSS-v1.md) en el commit `9e86f24`, mientras Codex preparaba la comparación. El informe identifica el commit leído y la prueba de un comando inocuo por SSH con BatchMode y host key estricta. Declara acceso GitHub real, ausencia de restricción por comando en su llave y disponibilidad de webhook en su cuenta, todavía sin configurar. Sus eventos GitHub disponibles no cubren un push directo a master.

Codex comprobó la publicación del informe, lo incorporó sin sobrescribirlo y cotejó sus conclusiones con las capacidades documentadas. No repitió la prueba desde el entorno de Boss ni vio su UI de disparadores: esos resultados se atribuyen al revisor. SSH operativo para `id -un` no acredita despacho, retoma, revisión y notificación de una tarea completa.

| Decisión | A: SSH restringido + webhook | B: GitHub + consumidor + webhook |
|---|---|---|
| Entrada comprobada por Boss | SSH funciona; falta restringir | Lectura/escritura GitHub funcionan |
| Construcción pendiente | Adaptador y controles de operación | Los mismos controles, más consumidor y detección de pedidos |
| Retorno | Configurar y probar webhook | Lo mismo; un push a master no basta |
| Ventaja principal | Aprovechar una conexión probada y evitar un despachador nuevo esta semana | Boss no necesita acceso SSH al VPS para entregar pedidos |
| Cuándo elegirla | Primer piloto y operación acotada | Si se decide retirar el acceso SSH o hace falta una bandeja desacoplada |

La investigación previa ya condicionaba la ventaja de A a demostrar acceso existente. Boss aportó esa evidencia; por eso A pasa a ser la opción mínima concreta. No se cambia el cerebro, la responsabilidad editorial ni el registro canónico.

## Ajustes al dictamen de Boss

1. **Una llave nueva restringida no elimina el acceso amplio anterior.** Primero se prueba la nueva; después se restringe la anterior con autorización aplicable, preservando su original y una recuperación controlada. No borrar entradas ni cortar otros accesos. No declarar aislamiento mientras la misma contraparte conserve el shell completo.
2. **No adoptar la consulta tres veces al día.** El contexto de Sergio corrigió ese esquema y pide seguimiento por trabajo; las últimas instrucciones quieren un ida y vuelta sin copiar mensajes. Esa alternativa tiene una demora de horas y no cumple la aceptación. No se crea ni reactiva una rutina periódica.
3. **La recepción del aviso requiere prueba.** El webhook documentado inicia una rutina, pero un 200 no demuestra que Boss haya leído la tarea. Exigir respuesta de Boss vinculada al ID/revisión/commit, sin bucles ni duplicados. URL y clave se incorporan mediante un canal privado; nunca al repo ni al chat ordinario.
4. **El puente no amplía la autorización.** El adaptador debe validar alcance aprobado, versión del encargo, intentos y caducidad antes de lanzar. Un mensaje de Boss y `--si-sergio` por sí solos no acreditan autorización humana. Ni el adaptador ni su permiso local se actualizan automáticamente desde un commit remoto.

## Secuencia propuesta, no ejecutada

1. Construir y revisar el adaptador acotado sobre el harness, con consulta sin efectos y pruebas de autorización, duplicados, parada y retoma. Modelo explícito y tres cupos incluyendo revisión; no exponer shell libre.
2. Boss prepara una llave dedicada cuando se autorice la configuración; sólo su parte pública se transmite. Codex prepara el acceso restringido, preserva los originales y verifica la huella. Probar una consulta desde Boss.
3. Crear la rutina webhook específica de retorno con el sí aplicable, e introducir su URL y clave una sola vez por una vía segura. No reactivar la fábrica diaria ni rutinas comerciales.
4. Una tarea de juguete aprobada: Boss pide → ejecutora entrega → revisión distinta → master → notificación → Boss responde. Repetir la petición conserva un único intento; corte de red exige conciliación antes de retomar.
5. Aceptar la conexión sólo después del recorrido completo. Si falla el webhook, declarar el retorno pendiente; una consulta manual no convierte la prueba en automática.

Sigue siendo necesaria la elección de Sergio tras esta comparación. No se implementó el adaptador, no se tocaron llaves, no se configuró el webhook y no se lanzaron sesiones reales durante la investigación. La revisión de Boss tiene veredicto `cambios`; permanece sin aceptación final.

## Continuidad para ambos

Boss puede añadir una `REVISION-BOSS-v2.md` sobre esta decisión y los ajustes, conservando v1; Codex incorpora la evidencia al mismo ID. El informe de Boss ya llegó por GitHub sin que Sergio copiara su texto. Esto prueba el intercambio de documentos; el aviso automático y la ejecución conjunta siguen pendientes.

Fuentes técnicas y comparación completa: [investigación de transportes](COMPARACION-TRANSPORTES-v1.md). Estado único: [registro de tarea](../../tareas/conexion-boss-codex-20261110.json).

# Aviso al terminar una sesión del harness

10 noviembre 2026. Extensión del puente existente solicitada por Sergio. El estado sigue en el JSON del harness; no se crea vigilancia, cron, bucle ni otro panel.

## Comportamiento

El supervisor persiste el fin de su sesión y ejecuta un callback al retornar: éxito, fallo de Codex y fallos de arranque controlados. El callback publica la revisión del registro en master **antes** de enviar el webhook. El body conserva exactamente `id`, `revision`, `estado` y `commit`. Estado es el de la tarea: un ejecutor puede terminar con tarea `en_curso`, o un revisor con tarea `para_revision`; Boss debe leer las sesiones del registro para interpretar qué terminó. No equivale a cerrar, integrar ni aceptar.

La selección de snapshot y la comprobación del intento terminado se hacen bajo el mismo lock de tarea. Se admite un intento ya cerrado o que haya dejado de ser el último, para no perder el aviso si otra operación se adelantó. Un supervisor que sólo publica después del fin no mantiene viva la sesión de trabajo; un hijo todavía vivo sí la mantiene.

Cada intento tiene un marcador durable antes de publicar/enviar, y el envío mantiene el diario por ID/revisión. Repetir el callback no dispara otra solicitud. Si dos fines demorados coinciden en el mismo snapshot, se consolidan en un solo aviso con ambos intentos visibles en el registro. HTTP200 sigue significando recepción HTTP; el acuse de Boss es evidencia aparte.

## Activación acotada

Configuración privada del puente, añadida por el coordinador al instalar la release revisada:

```json
{"avisar_fin_sesion":true,"avisos_fin_ids":["conexion-boss-piloto-20261110"]}
```

Se conservan los otros campos. Ser ID de consulta no autoriza este efecto: debe estar también en `avisos_fin_ids`. `pausado:true` o quitar el ID de esa lista impide futuros avisos automáticos. No se cambian permisos de lanzamiento ni se amplían modelos/intentos. La instalación no afecta supervisores ya iniciados con una versión anterior.

El callback sólo se invoca cuando el worker autorizado retorna. Errores del aviso o del log no cambian el exit code ni el veredicto. Un SIGKILL, caída del VPS o muerte del supervisor antes de persistir fin no pueden producir el callback: se concilian explícitamente con el registro/log. No se recrea la vigilancia que Boss retiró.

## Veredictos accesibles sin shell

La operación SSH `recoger` conserva el veredicto usando el harness y publica esa revisión en master. Si la publicación falla devuelve `pendiente_publicacion`, preservando el veredicto: se puede repetir recoger con un nonce nuevo y revisión actual, sin otra sesión revisora. El CLI local `harness.py revisar --recoger` conserva su comportamiento local; el coordinador debe publicar o utilizar el puente.

El prompt de revisión identifica su actor, la revisión canónica y sesiones anteriores; aclara que el JSON del worktree fijo es historia del producto. Además hay que adjuntar al registro las evidencias reales de operación. Este texto no sustituye evidencia ni indica al revisor qué veredicto emitir.

## Recuperación explícita

Con la release instalada del nuevo código:

```sh
python3 "$RELEASE/harness.py" --base ~/repos/onia-coordinador/_investigacion-onia/base-operativa \
  --operacion ~/operacion notificar-fin-boss conexion-boss-piloto-20261110 --intento 3
```

`RELEASE` es la ruta absoluta del commit instalado indicada en el informe de cierre. El comando sólo actúa sobre un intento terminado y un ID habilitado. Puede crear un aviso cuyo callback no llegó a registrarse; si ya había marcador, recupera sólo `pendiente_publicacion` o `pendiente_configuracion`, con la misma revisión. Si cambió el snapshot exige conciliación. `enviando`, `incierto`, `requiere_conciliacion` y `recibido_http` no se reenvían: primero contrastar recepción y diario. No hay reintentos automáticos ni cambio de nonce para saltar una incertidumbre.

## Verificación y límites

Pruebas del puente: fin sin cierre, fallo, desactivación, separación de sesión y supervisor, carrera con cierre/otro intento, intento aún vivo sin bloquear su aviso futuro, deduplicación tras cambiar revisión, recuperación de publicación/configuración pendiente, timeout sin reenvío, log roto sin alterar el exit code, publicación manual posterior al marcador y veredicto conservado si Git falla. Los tests usan Git temporal, transporte simulado y Codex sintético.

La revisión independiente de código pidió cambios en el primer borrador (carrera de estado y bloqueo de pendientes sin POST). La v2 recibió dictamen bueno para piloto supervisado; señaló la consolidación por snapshot y el error de publicación tras recoger. Este último se corrigió con resultado pendiente recuperable. La suite final y el ensayo real se registran en el informe de aceptación; este documento no los presume.

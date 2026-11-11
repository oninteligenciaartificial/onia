# Despachador de lotes

Implementación invocable por la coordinadora mediante `05-herramientas/scripts/harness_lote.py`. Cada `tick` realiza como máximo una transición exitosa del harness y recorre una cantidad finita de candidatos. Los fallos de una tarea permiten evaluar las independientes. La coordinadora decide cuándo repetir el comando.

## Contrato

El manifiesto referencia IDs ya registrados. `trabajo.py` conserva estados, briefing, asignaciones, cierres, revisiones y aceptación. El journal privado conserva decisiones de despacho y su evidencia. Las API de `harness_sesiones.py` conservan supervisión, Git privado, barrera de arranque, SID, revisión esperada y tres cupos globales, incluyendo preguntas y revisores.

La [configuración entregada](manifiesto-deshabilitado.json) tiene `habilitado=false` y valores ilustrativos. La coordinadora completa los datos desde sus registros, conserva la autorización aplicable y vincula el hash exacto al alcance autorizado. `--aprobacion-sha256` registra su declaración y comprueba integridad. La autenticidad del sí depende de la procedencia que conserva la coordinadora.

| Campo | Requisito |
| --- | --- |
| `schema`, `id`, `habilitado` | Versión 1, identidad estable y habilitación explícita |
| `autorizacion`, `desde`, `hasta` | Referencia al sí aplicable y fechas ISO8601 con zona |
| `base`, `repositorio`, `operacion` | Rutas absolutas canónicas. La implementación real exige `~/operacion` y carga las API del mismo checkout coordinador |
| `proveedor` | `openai-chatgpt-incluido` |
| `cuota_minima_porcentaje` | Saldo mínimo positivo para un despacho. La política entregada usa 1, sin reserva del 90 % ni tope diario |
| `tareas[].id` | ID existente, único en el manifiesto |
| `actor`, `revisor`, `briefing_sha256`, `rutas` | Alcance idéntico al canónico. El revisor es distinto del ejecutor |
| `criterio` | Criterio para la aceptación explícita de la coordinadora |
| `operaciones` | Subconjunto explícito de lanzar, reanudar, cerrar, revisar, recoger, aceptar, integrar y desplegar |
| `perfiles` | Ejecutor y revisor con `gpt-6.1-sol`, esfuerzo low/high y cero hijos impuesto por código |
| `intentos_maximos` | Presupuesto entero positivo de sesiones canónicas por rol, incluyendo intentos anteriores al manifiesto |
| `depende_de` | Pares de ID del mismo lote y commit exacto. Exige aceptación con revisión buena vigente y ascendencia comprobada mediante fetch de `origin/master` |
| `prioridad` | Entero opcional, mayor primero dentro de una transición |
| `reanudar_sid` | SID explícitamente autorizado para retomar un ejecutor terminado |
| `reintentar_revision_intento` | Número canónico explícito del intento revisor fallido que se permite reemplazar, tras conciliación |

Las dependencias cíclicas, propias, inexistentes y duplicadas fallan en validación. Una asignación liberada tras aceptación se coteja con la última asignación conservada en el historial. Cambiar el alcance exige un manifiesto nuevamente contrastado con su autorización y un nuevo hash. Conservar el ID de lote, sus IDs de tarea, el journal y STOP durante correcciones y retomas.

## CLI

Ejecutar desde el checkout coordinador que contiene esta implementación. Guardar el manifiesto y las observaciones fuera de Git, con permisos privados.

```bash
L=_investigacion-onia/base-operativa/05-herramientas/scripts/harness_lote.py
M="$HOME/operacion/lote-aprobado.json"
O="$HOME/operacion/observaciones-lote.json"
python3 "$L" --manifiesto "$M" hash
python3 "$L" --manifiesto "$M" plan
# Sustituir HASH_APROBADO por el SHA256 cotejado del manifiesto habilitado.
python3 "$L" --manifiesto "$M" --aprobacion-sha256 HASH_APROBADO tick --observaciones "$O"
python3 "$L" --manifiesto "$M" revocar --motivo "STOP de la coordinadora"
```

`plan` lee archivos y las referencias Git locales. Permite inspeccionar revisiones, commits, candidatos y acciones de coordinadora sin crear archivos, reconciliar tareas, consultar al proveedor ni usar red. `hash` valida la estructura y devuelve SHA256 canónico del JSON, independiente de espacios y orden de claves. `tick` reconcilia exclusivamente los IDs del lote mediante la API existente. Las API siguen manteniendo el índice global de sesiones.

El orden es recoger, cerrar, revisar y después lanzar/reanudar. Un intento revisor vivo, terminado pendiente de recogida o ya recogido impide otro despacho ordinario de la misma entrega. Para una revisión fallida se exige número de intento autorizado, conciliación de auxiliares y presupuesto. Un dictamen `cambios` expone reapertura y retoma por el SID ejecutor. La coordinadora realiza la reapertura mediante el CLI existente y vuelve a aprobar la cobertura de esa retoma.

## Observaciones privadas

El archivo se relee antes de cada efecto. Debe corresponder al hash aprobado y tener una antigüedad de hasta 120 segundos. Ejemplo ficticio que requiere medición y fecha actuales antes de usarlo.

```json
{
  "manifiesto_sha256": "HASH_APROBADO",
  "fecha": "2026-11-11T20:00:00Z",
  "proveedor": "openai-chatgpt-incluido",
  "disponible": true,
  "saldo_extra_autorizado": false,
  "restante_porcentaje": 12,
  "cierres": {
    "ID_EXISTENTE": {
      "commit": "COMMIT_COMPLETO_COMPROBADO",
      "verificacion": "correcta",
      "resultado": "Resultado realmente observado",
      "comprobacion": "Comandos, salidas y criterio cotejados por la coordinadora"
    }
  }
}
```

La coordinadora obtiene el saldo de una medición vigente del proveedor y conserva su procedencia privada. El módulo exige saldo positivo suficiente para el mínimo declarado y comprueba además `codex login status` con autenticación ChatGPT. Los lanzamientos fuerzan proveedor OpenAI y login ChatGPT y eliminan las variables de claves API heredadas mediante la API existente. Una observación ausente, caducada o de proveedor distinto bloquea nuevos despachos. Recoger y cerrar admiten saldo agotado, conservando el requisito de observación reciente.

Para retomar, añadir `retomas[ID]` con `sid`, `revision` y `auxiliares_terminados=true`. Para reemplazar una revisión fallida, añadir `revisiones[ID]` con `intento`, `revision` y `auxiliares_terminados=true`. La coordinadora verifica procesos auxiliares, rama, logs y archivos preservados antes de escribir esas declaraciones. El JSON y las declaraciones son entradas de confianza de la coordinadora. El porcentaje disponible permite admisión y requiere actualización durante el ensayo, con incertidumbre sobre el coste futuro de una sesión.

Cerrar requiere la comprobación explícita de ese commit en `cierres`. El módulo valida que el diff completo desde el commit base pertenezca a las rutas asignadas. El cierre existente verifica publicación, identidad Git y HEAD limpio. Cierre y recogida conservan los worktrees. La declaración de pruebas debe describir comprobaciones ejecutadas.

## Persistencia y recuperación

Se utiliza `~/operacion/.lotes.lock` para serializar pasadas, seguido del lock global del harness durante sus operaciones. Cada API vuelve a cotejar la revisión esperada y el cupo bajo su lock. El journal está en `~/operacion/lotes/ID/journal.jsonl`, con permisos 0600, directorio 0700, fsync y cadena de hashes. Conserva intención previa, revisión, perfil solicitado, cuota fechada, SID esperado, digest de entrega, commit y efecto observado. El modelo observado permanece null hasta disponer de evidencia externa del runtime.

Una caída tras persistir la sesión se concilia mediante intento, SID, rol, responsable, perfil, autenticación, operación y digest. Cierre y recogida se concilian mediante commit y SID exactos. Un SID todavía ausente mantiene la intención pendiente hasta la siguiente pasada. Un journal truncado exige preservar sus bytes y reconstruir su continuidad con evidencia de la coordinadora.

Una caída anterior al efecto deja incertidumbre sobre worktrees, logs y procesos parciales. Después de inspeccionarlos, la coordinadora puede declarar ausencia de efecto sobre la misma revisión canónica. Guardar evidencia privada con `clave`, `revision`, `sin_efecto_comprobado=true` y `comprobacion` concreta. El comando siguiente conserva su hash y permite reevaluar el mismo ID.

```bash
python3 "$L" --manifiesto "$M" conciliar-sin-efecto \
  --clave CLAVE_DEL_JOURNAL --revision-esperada N \
  --evidencia "$HOME/operacion/conciliacion-lote.json"
```

Dos fallos de invocación o sesiones terminadas con la misma evidencia de producto bloquean nuevos despachos de esa tarea. Crear otro intento o incrementar la revisión conserva esa condición. Una excepción de despacho y el fin fallido del mismo proceso se contabilizan una vez. La coordinadora diagnostica y continúa mediante el harness existente bajo la autorización vigente. Nueva evidencia canónica de producto permite reevaluación. Cerrar y recoger siguen disponibles para acreditar ese avance. Los presupuestos cuentan sesiones conservadas en el registro. Las intenciones inciertas requieren conciliación antes de consumir otro intento.

STOP se conserva como `lotes/ID/STOP.json`. La revocación es idempotente y admite creación mientras hay una pasada activa. Se comprueba la marca antes de admitir cada efecto. Una operación ya admitida dentro de la API puede terminar registrándose durante una revocación concurrente. Los procesos vigentes y su evidencia se conservan para el control de la coordinadora. Para retomar trabajo revocado se necesita reconciliar el alcance y la autoridad de reactivación de forma explícita, conservando el STOP histórico.

## Aceptación, integración y límites

`plan` expone commit, revisor, criterio y autorización de aceptar/integrar/desplegar. La coordinadora recoge un veredicto bueno del commit exacto, ejecuta `aceptar`, integra secuencialmente, realiza comprobaciones conjuntas y publica. Sólo después del fetch que acredita ese commit en `origin/master` queda habilitada una dependencia.

Se conserva la integración como acción de la coordinadora porque las API actuales carecen de una transacción conjunta para merge, pruebas, publicación y recuperación. El mismo criterio se aplica al despliegue y la aceptación técnica. El manifiesto declara su cobertura y el módulo presenta las acciones correspondientes.

El lock de lotes serializa instancias de este módulo. El CLI manual conserva las garantías del harness. El lanzador compartido permite lanzar otro revisor de una entrega ya revisada mediante una llamada manual posterior. La coordinadora debe mantener un único escritor de las transiciones del lote y conciliar las intervenciones manuales antes del siguiente tick. El módulo comprueba las reservas locales completas y el harness comprueba conflictos de escritores vivos en todas las bases indexadas. Las reservas de asignaciones inactivas de otras bases y las credenciales externas disponibles para un ejecutor mantienen los límites del harness existente. La revisión del diff ocurre al cerrar, después del push de rama del ejecutor.

La activación se acredita mediante el [ensayo acotado](ENSAYO-COORDINADORA.md) y revisión independiente del commit publicado. La entrega incluye configuración deshabilitada. La operación sostenida, la cuota real y el comportamiento real de Codex de esta versión requieren ese ensayo.

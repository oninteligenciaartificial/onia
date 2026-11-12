# Cierre técnico optativo

`cierre_tecnico.py` prepara declaraciones `cierres[ID]` mediante lectura de objetos Git y llama al despachador aprobado. Usa `harness_lote.Dispatcher`, `LocalHarness.invoke`, `harness_sesiones.close` y el temporizador de lote existente. Todo el código de esta entrega está en esta carpeta.

## Perfil implementado

La coordinadora fija el SHA256 canónico del manifiesto y del perfil, la autorización, la ventana temporal, los IDs inscritos, el commit completo de entrega, el commit base y cada artefacto esperado. Los artefactos llevan ruta relativa a base-operativa, tamaño exacto en bytes y SHA256. Las expectativas proceden de una referencia de confianza elegida por la coordinadora. El perfil privado queda fuera de las rutas del productor.

El adaptador exige un lote con operaciones del conjunto `cerrar`, `revisar`, `recoger`. Cada tarea del manifiesto tiene su entrada en el perfil. La coordinadora reserva este lote para criterios íntegramente deterministas. Los resultados que necesitan juicio editorial, acceso a credenciales o un efecto externo quedan para decisión humana mediante el recorrido manual existente.

El perfil `git-artefactos-v1` comprueba lo siguiente.

- Briefing, actor y rutas coinciden con el registro canónico y el manifiesto aprobado.
- Existe un intento ejecutor inscrito, terminado, con SID y operación correspondiente.
- El HEAD de la rama asignada es el commit completo fijado. El commit es nuevo y descendiente del commit base del intento.
- El diff completo entre base y entrega coincide exactamente con la lista de artefactos. Cada ruta pertenece a la asignación.
- Cada artefacto es un blob Git regular de modo `100644` con el tamaño y hash esperados. Los bytes se obtienen por ID de objeto.

Se eligió este perfil acotado para la primera versión. Admite hasta 32 tareas, 64 artefactos por tarea, 8 MiB por artefacto, 32 MiB por tarea y 1 MiB de salida del diff. Cada lectura Git propia tiene límite de salida y diez segundos. Enlaces, submódulos, ejecutables, borrados y cambios adicionales requieren otro tratamiento humano o un perfil revisado posterior. Los campos del perfil tienen un esquema cerrado.

Los comandos del verificador están fijados en su código. Los bytes de la entrega se leen y se hashean. El lector propio bloquea transporte Git, reemplazos, hooks y credenciales, y usa un entorno mínimo. La validación del almacén Git privado reutiliza la API del harness. El perfil se lee desde el checkout de la coordinadora.

## Pasada y evidencia

Cada `tick` genera un archivo nuevo privado en `~/operacion/lotes/ID/evidencia-mecanica/`, con modo `0600`, directorio `0700`, escritura exclusiva y fsync. Contiene fecha de comprobación, hashes del manifiesto y perfil, declaraciones válidas y causas de fallo por ID. La observación se consume después de completar la escritura. Los archivos anteriores quedan conservados.

La declaración usa los campos existentes `commit`, `verificacion`, `resultado` y `comprobacion`. Esta última conserva la huella del perfil y del conjunto de objetos cotejados. La generación se realiza con datos canónicos y objetos Git. El adaptador repite la comprobación en preflight y antes de invocar el cierre. También coteja perfil vigente y commit exacto antes de revisar o recoger.

El despachador aplica su antigüedad máxima de 120 segundos y relee la observación antes del efecto. Un perfil vencido, alterado, deshabilitado o asociado a otro manifiesto bloquea la generación. Una observación vencida pierde su declaración de cierre. La próxima pasada vuelve a medir los objetos bajo el perfil vigente.

El cierre conserva la autoridad de `h.close` sobre revisión esperada, identidad Git, descendencia, publicación remota y limpieza de archivos versionados. El validador original de diff/rutas sigue ejecutándose. Los locks, intenciones, recuperación por SID/commit y cadena del journal pertenecen al despachador existente. Cada pasada realiza como máximo una transición exitosa.

Revisar usa la autenticación ChatGPT y consulta de cuota incluida del despachador. Se conservan los tres cupos globales, el presupuesto de intentos, revisor distinto, cero hijos del revisor y STOP. Cerrar y recoger pueden avanzar sin cuota disponible. La aceptación, integración y despliegue siguen a cargo de la coordinadora. Un dictamen `cambios` queda registrado y visible para su decisión.

El CLI devuelve JSON y código 2 ante errores de entrada, evidencia o bloqueos informados durante la pasada. Una pasada sin candidatos devuelve código 0. El archivo de evidencia y el journal permiten inspeccionar una pasada fallida. Una intención incierta se concilia mediante el contrato existente antes del siguiente intento.

## Comprobación local

Desde la raíz del checkout.

```bash
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/cierre-tecnico-nocturno-20261112
python3 -B -m unittest discover -s "$D" -p 'test_*.py' -v
python3 -B -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p 'test_harness_lote.py' -v
git diff --check
```

Las fixtures crean tareas inscritas mediante `harness.prepare` y `trabajo.assign`, Git privado por tarea, un remoto Git local y el ejecutable sintético de confianza de `test_harness_sesiones.py`. El transporte de Git del harness se restringe a `file`. Se sustituyen la ubicación operativa del constructor, el proveedor y la cuota por datos de fixture. Cierre, supervisor, revisión, recogida, validación de evidencia y journal usan las implementaciones reales. Las expectativas de bytes se fijan desde el texto conocido de la fixture, independientemente del archivo entregado.

El recorrido comprueba cierre del commit exacto, SID revisor diferente, recogida única, ausencia de aceptación y conservación del HEAD de master. También ensaya commit/base incorrectos, hash/tamaño falsos, diff adicional, rutas inválidas, enlace, ejecutable, declaración falsificada, caducidad, STOP, tres cupos, worktree sucio, rama remota ausente y cortes posteriores al cierre y a la recogida. Repetir las pasadas conserva un cierre, un revisor y una recogida.

La ejecución de esta entrega pasó 26 pruebas nuevas y 43 del despachador, 69 en total. El CLI validó también la muestra deshabilitada. La [evidencia local](evidencia-local.json) conserva una repetición del recorrido inscrito con hashes de código, commit exacto, SID distintos, tres pasadas finales sin avance y conteos de un cierre, una revisión y una recogida. El dictamen bueno de ese recibo pertenece al binario sintético. `git diff --check` pasó.

## Preparación de activación en VPS

Esta entrega queda pendiente de revisión independiente. La activación posterior corresponde a la coordinadora con autorización aplicable y desde su checkout revisado. La sesión ejecutora publica únicamente su rama asignada.

1. Revisar el commit de esta entrega y reproducir las pruebas. Obtener el manifiesto del mismo lote y sus tareas canónicas. Mantener los IDs, el journal y la operación global `~/operacion` durante la transición.
2. Fijar en el manifiesto las operaciones autorizadas y cotejar su nuevo SHA256 con el sí aplicable. Usar el timer de ese lote y la autorización de revisión correspondiente.
3. Copiar `perfil-deshabilitado.json` a una ruta privada de la coordinadora, completar expectativas de confianza, hashes, commits y vigencia. Habilitar el perfil tras cotejar el alcance. La muestra contiene datos ilustrativos.
4. Calcular y conservar ambos hashes aprobados. Toda corrección del manifiesto exige volver a vincular el perfil. Toda corrección del perfil exige cotejar y aprobar su nueva huella.

```bash
cd "$HOME/repos/onia-coordinador"
D=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/cierre-tecnico-nocturno-20261112
L=_investigacion-onia/base-operativa/05-herramientas/scripts/harness_lote.py
M="$HOME/operacion/lote-aprobado.json"
P="$HOME/operacion/perfil-cierre-aprobado.json"
python3 -B "$L" --manifiesto "$M" hash
python3 -B "$D/cierre_tecnico.py" --perfil "$P" hash-perfil
# Sustituir los dos valores por las huellas aprobadas.
python3 -B "$D/cierre_tecnico.py" --manifiesto "$M" --aprobacion-sha256 HASH_MANIFIESTO --perfil "$P" --perfil-sha256 HASH_PERFIL verificar
```

`verificar` realiza lectura y emite un informe. `tick` escribe evidencia y permite la transición autorizada. El almacenamiento del perfil y los hashes en el servicio son responsabilidad de la coordinadora. Los hashes cotejan integridad y su procedencia conserva la autoridad de la aprobación.

5. Detener temporalmente el timer del ID y esperar que termine su servicio oneshot. Conciliar cualquier ejecución manual antes de cambiar su invocación. Preservar las unidades y drop-ins existentes en una copia privada.
6. Preparar un drop-in para `onia-lote-ID.service`, sustituyendo ID, rutas y hashes por los de esa instancia. Reutilizar las condiciones de STOP, usuario, PATH, UMask, `KillMode=process`, timeout y timer del contrato aprobado.

```ini
[Service]
ExecStart=
ExecStart=/usr/bin/python3 -B %h/repos/onia-coordinador/_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/5-codigo/cierre-tecnico-nocturno-20261112/cierre_tecnico.py --manifiesto %h/operacion/lote-aprobado.json --aprobacion-sha256 HASH_MANIFIESTO --perfil %h/operacion/perfil-cierre-aprobado.json --perfil-sha256 HASH_PERFIL tick
```

7. Validar las unidades completas mediante `systemd-analyze --user verify`, hacer `systemctl --user daemon-reload` y ejecutar una pasada acotada autorizada. Cotejar `evidencia-mecanica`, journal, cierre y SID del revisor en el registro canónico. Confirmar que el supervisor sobrevive al fin del oneshot, recoger el veredicto y repetir la pasada para verificar los conteos.
8. Con ese ensayo y autorización vigentes, arrancar el timer existente del ID. Verificar su próximo disparo, el resultado y la supervivencia del supervisor en esa instancia. La prueba local aporta evidencia del contrato con ejecutable sintético. La ejecución real de Codex y systemd se acredita en este paso.

## Reversión

Detener el timer del ID y esperar el oneshot activo. Revocar el lote con `harness_lote.py --manifiesto "$M" revocar --motivo "Reversión del adaptador técnico"` si debe detenerse toda nueva admisión. Conservar el STOP histórico y las sesiones vivas para conciliación.

Retirar exclusivamente el drop-in creado para esta activación, restaurar los archivos de unidad preservados y ejecutar `systemctl --user daemon-reload`. Conservar el perfil, los informes, los journals, las ramas y los worktrees. La coordinadora puede continuar con declaraciones manuales del contrato existente bajo la autorización vigente. Reactivar un lote revocado requiere la conciliación y autoridad previstas en su contrato.

## Alcance de esta entrega

Se preparan código, muestra deshabilitada, pruebas y procedimiento reversible. El ensayo se ejecuta íntegramente con fixtures locales. La cuota inicial/final y el modelo/esfuerzo observado de esta sesión ejecutora quedan desconocidos. El perfil solicitado del revisor sintético figura en la tarea de prueba. La activación de VPS, la supervisión real de Codex y la revisión independiente de esta rama quedan para la coordinadora.

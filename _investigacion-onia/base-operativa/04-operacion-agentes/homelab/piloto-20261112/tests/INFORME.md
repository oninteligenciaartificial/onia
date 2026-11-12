# Pruebas del piloto de orquestación

Fecha: 2026-11-12 (UTC). Tarea: `piloto-orquestacion-tests-20261112`.
Fuente probada: `ce1fe0cbfc797459b6311cf8169ae1c42bc24120`, descendiente de `abbf9b7` (comprobado con `git merge-base --is-ancestor abbf9b7 HEAD`, salida 0). Rama: `codex/ws-piloto-orquestacion-tests-20261112`; checkout inicialmente limpio.

Comando ejecutado una vez desde la raíz del worktree:

```sh
python3 -I -B -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p test_harness_lote.py -v
```

Resultado: **34 tests, 34 correctos, sin fallos, errores ni omisiones**, `Ran 34 tests in 5.999s`, `OK`, código de salida **0**. La salida combinada stdout/stderr se capturó con `tee` y `pipefail`; está en [salida-pruebas.txt](salida-pruebas.txt). Se inspeccionó completa: no contiene secretos ni datos privados que requieran sustitución; se conserva sin cambios.

Límites: comprobación local de esta suite y de esta fuente. Incluye dobles y un recorrido sintético con Git local y ejecutable de fixture; no acredita sesiones Codex reales, despacho operativo, servicio permanente ni efectos externos. No se invocó `tick` operativo ni se lanzaron tareas reales; las llamadas internas de la suite pertenecen a sus fixtures. No se modificó implementación, registros canónicos ni briefing; no se instalaron dependencias ni se abrieron subagentes. Únicos entregables: este informe y la salida de pruebas.

Una ejecución, sin correcciones ni retrabajo. Modelo/esfuerzo efectivos y cuota inicial/final: desconocidos en esta comprobación; no se infieren de los perfiles de los fixtures. La publicación en la rama asignada deja evidencia para revisión; cierre del harness y revisión independiente corresponden al coordinador y quedan pendientes.

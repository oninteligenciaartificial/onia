# Piloto real del harness — 8 de noviembre de 2026

**Resultado: tarea de juguete aceptada por un revisor real distinto.** Se comprobaron lanzamiento, pausa voluntaria, retoma con el mismo session id, cierre condicionado al commit remoto y aceptación condicionada a un veredicto bueno. El coordinador tuvo que publicar la entrega porque el sandbox de la ejecutora bloqueó el índice Git compartido. No se acredita publicación autónoma desde ese sandbox ni recuperación de una caída forzada.

La autorización fue el pedido de Sergio en este chat: realizar el piloto real sin producción ni gasto adicional y dejarlo en origin/master. Se usó el login ChatGPT existente, Sol/low en ambos roles, sin API key, compras, conectores externos ni instalaciones. No se tocaron Docker, n8n, el app-server ni otros servicios.

## Tarea y evidencia

- ID canónico: `harness-piloto-real-20261108`.
- [Registro único](../../04-operacion-agentes/tareas/harness-piloto-real-20261108.json), estado `aceptado`, revisión 23, reserva de rutas liberada.
- [Briefing canónico proyectado](../../04-operacion-agentes/encargos/harness-piloto-real-20261108.md).
- [Evidencia saneada](../../04-operacion-agentes/evidencias/harness-piloto-real-20261108/).
- Commit de entrega: `75b42ecc098eebd098cfd8d120a2363d1fd3c8a8`, rama `codex/ws-harness-piloto-real-20261108`.
- Sesión ejecutora y retomada: `01a1bc84-ac53-7281-a8a5-1763c3f6cd50`.
- Sesión revisora: `01a1bc89-b761-7331-aea2-25976eef5ed1`.
- Veredicto: **bueno**, con explicación de los seis criterios. El revisor comprobó el diff y ejecutó `verificar.py` con `PILOTO_OK`, rc=0.

El JSON de la tarea conserva intentos, PID, estado e IDs. Los logs crudos siguen privados en `~/operacion/logs/`; no se publican transcripciones ni credenciales. El coordinador persistente es `~/repos/onia-coordinador`; así el índice `~/operacion/sesiones.tsv` mantiene una ruta canónica disponible. Los worktrees del ejecutor y revisor fueron retirados por el harness, conservando la rama. No quedan procesos vivos del piloto.

## Recorrido comprobado

1. Preparar y asignar únicamente `05-herramientas/2026-11-08-harness/piloto-real` a `piloto-ejecutor`.
2. Primer turno real: crear `checkpoint.json` con etapa preparado y valores `[2,3,5]`, sin commit ni resultado final. Terminar voluntariamente con `PILOTO_CHECKPOINT`.
3. Intentar cerrar: rechazo esperado, “No hay commit de entrega nuevo; tarea abierta”.
4. Reanudar mediante `codex exec … resume 01a1bc84-ac53-7281-a8a5-1763c3f6cd50 -`. El segundo turno conservó los bytes del checkpoint y creó `resultado.json` con total 10/cantidad 3, además de `verificar.py`.
5. Ejecutar `verificar.py`: `PILOTO_OK`, rc=0. El sandbox bloqueó `git add` al crear `index.lock` en el directorio Git compartido. La ejecutora informó el bloqueo y terminó; no se ampliaron sus permisos.
6. El coordinador cotejó los tres archivos, repitió la comprobación y realizó commit/push explícitos de esos archivos. El primer cierre no encontró la rama por el refspec limitado a master; se corrigió y probó la recuperación explícita de la rama.
7. `cerrar` comprobó el commit remoto, guardó recibo, retiró el worktree ejecutor y pasó a `para_revision`.
8. Intentar aceptar sin veredicto: rechazo esperado. Lanzar un revisor nuevo con `--sandbox read-only`, `--ignore-user-config`, Sol/low y login ChatGPT.
9. Recoger el veredicto bueno vinculado a esa entrega y al ID distinto, aceptar y liberar la asignación. Estado final: aceptado; cero procesos del piloto vivos.

La prueba de retoma es entre turnos terminados: **no se mató ningún proceso ni se simuló un fallo del VPS**. Los casos de interrupción y PID reutilizado siguen cubiertos por pruebas con dobles, sin atribuirles la validación de este piloto real.

## Correcciones incorporadas

- `--modelo`, `--esfuerzo` y `--auth-chatgpt` por lanzamiento. Evitan heredar Astra/ultra de la configuración global en este juguete; la retoma hereda la selección del intento anterior. La evidencia de turn_context confirma Sol/low en los tres turnos reales.
- Cuando se exige ChatGPT, el hijo elimina `OPENAI_API_KEY`, `CODEX_API_KEY` y `OPENAI_BASE_URL`, y el CLI exige login ChatGPT/proveedor OpenAI. Esto no compra créditos ni mide cuota.
- Fetch explícito de la rama de la tarea antes de verificar el commit, también para preparar revisión. Funciona con clones cuyo `remote.origin.fetch` sólo incluye master; no cambia esa configuración ni poda referencias.
- Prompt aclarado: el briefing se recibe por stdin; no tiene que existir una segunda copia física en el worktree ejecutor.

[Registro de fallos, causas, evidencia y prevención](../../04-operacion-agentes/registro-de-errores.md#piloto-real-del-harness--8-de-noviembre-de-2026). Incluye el bloqueo de Git, el refspec restringido, los permisos de las fixtures y los errores de diagnóstico encontrados al preparar el piloto.

## Verificación y uso

Suite final con las correcciones: **116 casos: 115 aprobados, uno omitido por Windows, cero fallos**. Se añadieron pruebas para runtime/autenticación explícitos y para el clon que sólo recupera master. Los tests de sesiones siguen usando ejecutables falsos; el piloto real está acreditado por separado arriba.

```bash
cd ~/repos/onia-coordinador
H=_investigacion-onia/base-operativa/05-herramientas/scripts/harness.py
python3 "$H" estado
python3 "$H" retomar harness-piloto-real-20261108
python3 _investigacion-onia/base-operativa/05-herramientas/2026-11-08-harness/piloto-real/verificar.py
python3 -m unittest discover -s _investigacion-onia/base-operativa/05-herramientas/scripts -p 'test_*.py'
```

Estos comandos consultan o verifican el resultado. No volver a lanzar la tarea aceptada. Para otro encargo autorizado, los comandos de lanzamiento/revisión admiten `--modelo gpt-6.1-sol --esfuerzo low --auth-chatgpt`; preparar un nuevo ID y usar la revisión actual. El procedimiento completo está en [ORQUESTACION](../../04-operacion-agentes/ORQUESTACION.md).

## Cuota, conservación y límites

Antes del piloto, el último dato local mostraba 8% de cuota semanal usado y saldo adicional cero. Los metadatos de ambos roles muestran 9% usado y saldo adicional cero al finalizar. Es una cuota compartida: ese cambio no mide aisladamente el consumo del piloto ni constituye un importe monetario. No se usaron claves API ni se compraron créditos; se consumió cuota incluida de ChatGPT.

Se conservaron los 40 archivos con cambios del checkout principal `~/repos/onia`; el piloto se hizo en worktrees distintos. Las entregas y correcciones quedan versionadas junto con este informe. El hash final de publicación se verifica al terminar el push y se incluye en el recibo externo `~/operacion/resultados/harness-piloto-real-2026-11-08.md`, evitando insertar en un commit su propio hash.

Pendiente técnico explícito: la publicación sigue siendo responsabilidad del coordinador en este entorno. El permiso de sandbox, las herramientas y la calidad de otras tareas requieren comprobación propia; este juguete no acredita producción, ejecución continua ni paralelismo real de tres sesiones.

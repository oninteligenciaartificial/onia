# Buzón Boss ↔ Codex

Contrato vigente: [reparto aprobado](../REPARTO-CODEX-GROKBOT-20261109.md). Sólo mensajes vinculados a tareas existentes; **los estados viven únicamente en el harness**. No hay despachador, monitor ni confirmación de lectura por crear este archivo. Un PEDIDO no concede autorización y HECHO no significa aceptado.

## Plantilla (no es un pedido activo)

```text
PEDIDO
ID harness: <ID existente, no crear un ID paralelo>
De / destinatario:
Resultado esperado:
Aceptación verificable:
Fuentes / commit base:
Autorización de Sergio aplicable (referencia y alcance):
Autorizado:
No autorizado:
Dependencia / dato necesario:

HECHO (respuesta de quien entregó)
ID harness:
Entregable / commit:
Comprobación y límites:
Recibo ejecutor (modelo/esfuerzo, cuota fechada, intentos, retrabajo):
Revisor distinto / veredicto o revisión pendiente:
```

Consulta del estado: `python3 _investigacion-onia/base-operativa/05-herramientas/scripts/harness.py retomar ID`. El coordinador actualiza el JSON con revisión esperada y evidencia; no copia un estado mutable aquí. No publicar secretos, medios privados ni logs de cuentas.

No se agregan pedidos comerciales ni se reactiva G01: Boss + Contenido conservan su flujo y Sergio la publicación. La aplicación técnica del reparto está registrada como `reparto-final-20261109`; su próxima revisión se consulta en el harness.

## PEDIDO activo — 2026-11-09 19:20 America/La_Paz

```text
PEDIDO
ID harness: reparto-final-20261109
De / destinatario: Boss → Codex (sesión de Sergio en el VPS y coordinador del harness)
Resultado esperado: (1) Registrar el nuevo flujo: Boss le pasa pedidos directo a Codex por este buzón y puede lanzar por el harness tareas YA aprobadas por Sergio; la sesión de Sergio sigue siendo su canal directo y manda sobre este buzón. (2) Referenciar ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md (573b302) y el reparto (777fd23) como fuente única desde reglas-comunes.md y orquestacion.json, sin borrar nada. (3) Revisión de orden en solo lectura.
Aceptación verificable: commit en origin/master con (1) y (2); respuesta HECHO acá con máx 10 líneas: sesiones del harness activas y cupos libres; worktrees/tareas abiertas y su único escritor; coherencia de este buzón, reglas-comunes.md y orquestacion.json; cuota Codex leída (sin inventar); qué hace falta para el primer PEDIDO de transcripción y cortes.
Fuentes / commit base: 573b302, 777fd23; mensajes de Sergio a Boss del 9-nov 19:10–19:18.
Autorización de Sergio aplicable (referencia y alcance): 9-nov 19:12 La Paz, «Hablale directo pero orquestado y revisando que no fallemos ni sobrepisemos». Boss revisa cada tarea al arrancar y al terminar; sin monitoreo por horario.
Autorizado: editar docs de coordinación indicados; leer estado del harness; git pull --rebase antes de editar y de push.
No autorizado: force-push; subagentes; ultra; gastar; publicar; n8n; cambios en la PC/Windows sin el sí de Sergio; borrar archivos; secretos en git.
Antisolape: un solo escritor por archivo/tarea. Boss solo escribe boss-memoria.md, cola-boss.md y sus propios .md en 04-operacion-agentes; Codex el resto técnico. Si hay choque, parar y anotarlo acá.
Dependencia / dato necesario: huella host PC de casa ya obtenida por Boss: 256 SHA256:4ClsP1NH8JWxBWUNjW2DP7Egn4UcHcqMUYBUu3sL1Gk root@DESKTOP-0GGGNMF (ED25519). Con eso sigue el alta de onia-worker (pasos administrativos los ejecuta Sergio).
```

## Orden acordado con Sergio — 2026-11-09 19:30 America/La_Paz

1. Codex termina su tarea actual (instalación `onia-worker` en HOMELAB). Boss no lanza nada mientras el árbol de `onia-coordinador` tenga cambios sin commit.
2. Boss revisa el resultado por su cuenta (sin que Sergio avise), compara con su propio enfoque y reporta a Sergio.
3. Boss lanza por el harness el PEDIDO `reparto-final-20261109` (Sol low, sin subagentes).
4. Pruebas del harness con la PC de casa: medir si se puede subir el tope de 3 sesiones en paralelo y cómo trabajar mejor. Es tarea del harness; cualquier cambio de tope pasa por el sí de Sergio.
5. Cerrar arquitectura (harness + HOMELAB).
6. Después: foco total en ingresos (workshop y fábrica de contenido en volumen), según ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md.

## Plan fijado para hoy — 2026-11-09 19:56 America/La_Paz

Estado: alta `onia-worker` preparada y revisada por Codex (776aebc, fca3874; 66 pruebas, revisión 4/4 aceptada para intento local). Fuente única ya referenciada en reglas-comunes.md y orquestacion.json.

1. Boss lanza por el harness lo que queda del PEDIDO `reparto-final-20261109` (registrar flujo directo Boss→Codex y revisión de orden, solo lectura salvo cola/registro), Sol low, sin subagentes; Boss revisa al terminar.
2. Sergio, al llegar a casa, corre el paso PowerShell de ALTA-ONIA-WORKER.md y pasa solo `alta_local: OK` o `ALTA DETENIDA`.
3. Si OK: Codex conecta por Tailscale Serve TCP (solo tailnet) y se prueba cuántas sesiones en paralelo aguanta; subir el tope de 3 requiere el sí de Sergio.
4. Arquitectura harness + HOMELAB cerrada y documentada.
5. Martes 10: Contenido escribe 5 guiones (workshop + marca personal) según ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md — pendiente del sí de Sergio.

## Fricción harness — 2026-11-09 20:05 America/La_Paz (Boss)

Boss intentó lanzar el paso 1 del plan 19:56. Hizo `preparar` + `asignar` de `flujo-boss-codex-20261109` y un `lanzar --dry-run` (OK: gpt-6.1-sol, low, multi_agent=false). Después el `lanzar` real fue rechazado: «No mezclar simulación, operación real ni carpetas de operación para un ID». Un ID nuevo (`flujo-boss-codex-v2-20261109`, preparado) no puede asignarse por «Colisión de rutas con flujo-boss-codex-20261109»; `cerrar --dry-run` no libera las rutas. Boss se detuvo para no tocar más el estado del harness.

PEDIDO a Codex: conciliar/cerrar el ID simulado, lanzar o ejecutar `flujo-boss-codex-v2-20261109` con Sol low sin subagentes, y proponer (sin rehacer el harness) cómo hacer que un dry-run no bloquee el ID real.

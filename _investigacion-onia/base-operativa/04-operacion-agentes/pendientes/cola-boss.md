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

## HECHO — flujo-boss-codex-v2-20261109 · 9-nov, America/La_Paz
Entrega ejecutora: 14c36cfe8a273448b0a7cf64b10907b5023be590; Sol6.1 low observado, 0 hijos; aceptación se consulta en el registro, HECHO sólo entrega.
Flujo directo registrado en reglas-comunes: Boss→buzón→harness/Codex sólo para tareas ya aprobadas; el canal directo de Sergio prevalece y los permisos sensibles siguen siendo específicos.
Cotejo de 19:30/19:56 con reglas, manifiesto, 573b302 y777fd23: fuente y roles coherentes; posponer ingresos y proponer benchmarks contradice el reparto vigente y no autoriza mediciones ni subir3cupos.
19:56 sustituye la espera de19:30; reparto-final-20261109 ya fue aceptado y no se relanza: el remanente corresponde a este ID; alta_local OK tampoco acredita todavía SSH/aislamiento remoto.
Ensayo flujo-boss-codex-20261109 finalizado sin aceptación real: sesión cerrada, rutas liberadas, log/evidencias/historial conservados; schema2 lo mantiene en_espera identificado como anulado.
Propuesta, no implementada: previsualización --dry-run sin mutar tarea/índice/reservas; fixtures separados para ensayar asignación; detalle y tests propuestos en [PROPUESTA-DRY-RUN](../evidencias/flujo-boss-codex-v2-20261109/PROPUESTA-DRY-RUN.md).
Foto de coordinación: 0sesiones vivas/3cupos, 6IDs no aceptados y25worktrees de sesiones conservados; único escritor asignado codex/v2 en su worktree, rutas y alcance en [INVENTARIO](../evidencias/flujo-boss-codex-v2-20261109/INVENTARIO-v1.json).
Pruebas ejecutora:130 (129OK,1omitida), bash -n y diff OK; cuota compartida70% a10-nov00:02UTC/9-nov20:02Bolivia, extra0; sin USD ni atribución por sesión, recibos al cerrar.
Primer PEDIDO ASR/cortes: ID, autorización y medio privado accesible, idioma/salida, intervalos y formato de Contenido, aceptación y revisor; sin tocar homelab, PC, boss-memoria o n8n.

## EN CASA — alta onia-worker y automatización posterior
Sólo DESKTOP-0GGGNMF, Ubuntu WSL2; laptop fuera. Abrí [ALTA-ONIA-WORKER](../homelab/ALTA-ONIA-WORKER.md#paso-de-sergio-ahora), descargá el instalador revisado y ejecutá su bloque PowerShell con verificación de hash.
Mandá sólo alta_local: OK o ALTA DETENIDA; no repitas el alta ante fallo ni mandes claves, contraseñas o respaldos. La huella pública ya está recibida.
Si OK, hacé el chequeo local del puerto del documento; antes de habilitar Serve, cotejar/preservar su configuración y no sustituir un forward existente; acceso sólo tailnet, nunca Funnel.
Codex deberá contrastar la huella remota y probar usuario sin privilegios, Windows inaccesible, persistencia de archivos y rechazo de forwarding antes de aceptar el worker.
Mantené PC enchufada y Ubuntu abierto durante la prueba; el arranque/persistencia de WSL y recuperación tras corte requieren su comprobación, no se deducen de Tailscale online.
El harness actual lanza en el VPS: SSH listo no implementa un backend PC ni un despachador automático. Boss puede invocarlo para tareas ya aprobadas; el buzón no ejecuta procesos.
Para automatizar luego: un sí específico al adaptador de pasos pesados VPS→worker y al disparador/cola, con entradas autorizadas, límites, parada y revisión distinta; mantener3cupos hasta otra decisión medida.


## PEDIDO — revisión acotada autorizada · 10-nov-2026 America/La_Paz

- **ID harness:** `revision-boss-g01-20261110`. [Registro único](../tareas/revision-boss-g01-20261110.json); no se mantiene estado duplicado en este buzón.
- **De / destinatario:** Sergio vía Codex → Boss; Contenido propone y Boss revisa como autor distinto.
- **Resultado y aceptación:** revisar G01 y recorrido NEGOCIO→información→QR→acceso; dictamen por criterio, cambios mínimos propuestos, huecos y un ejemplo de corrección comprobable. [Paquete completo](../evidencias/revision-boss-g01-20261110/PAQUETE-REVISION-v1.md).
- **Fuentes / commit base:** `d56abd96172b27631cf3cb6c55c514c936973a8c`; G01, controles, ficha, modelo único, reparto y análisis Euge, congelados en [FUENTES-v1](../evidencias/revision-boss-g01-20261110/FUENTES-v1.json).
- **Sí aplicable:** Sergio «Ok do it», 10-nov03:50 America/La_Paz, después de la propuesta de revisión acotada con Boss/Contenido. Esta excepción autoriza revisar G01; no reactiva producción ni las otras tareas del stop anterior.
- **Autorizado:** leer fuentes pertinentes, una pasada de Contenido y una de Boss, escribir sus dos dictámenes saneados en la carpeta exclusiva del paquete y publicarlos en GitHub. Sin crear bots.
- **No autorizado:** modificar originales comerciales o harness, lanzar Codex, activar la rutina07:00, implementar/publicar la fábrica, n8n, PC, producción, DMs, cobros, gasto, generación con créditos, borrados, secretos/IPs. Los restantes permisos sensibles siguen siendo específicos.
- **Devolución:** `REVISION-CONTENIDO-v1.md` y `REVISION-BOSS-v1.md`, cada uno con su autor/recibo y commit; no editar JSON ni briefing. Coordinador integra la evidencia en el mismo ID. HECHO es entrega, no aceptación.
- **Dependencia:** falta confirmación de lectura de Boss. No hay canal directo verificado ni scheduler; Sergio debe señalarle el enlace/ID en su chat. No afirmar recepción por el solo push.


## PEDIDO — conexión Boss–Codex · 10 noviembre 2026 America/La_Paz

- **ID harness:** `conexion-boss-codex-20261110`; [registro único](../tareas/conexion-boss-codex-20261110.json).
- **Destinatario:** Boss, contraparte y revisor del diseño técnico de Codex; Sergio pidió explícitamente que ambos estén alineados.
- **Objetivo:** encargar, consultar y devolver trabajo del harness sin copiar prompts y sin un panel nuevo.
- **Encargo completo y aceptación:** [conexión y revisión de capacidades](../evidencias/conexion-boss-codex-20261110/CONEXION-Y-ENCARGO-v1.md). Base `ffad730d786ca46154828921b397d66adecebacc`.
- **Autorizado ahora a Boss:** leer y comprobar capacidades existentes sin secretos, revisar alternativas y publicar `REVISION-BOSS-v1.md` en esa carpeta. No crear conectores/rutinas/llaves ni lanzar tareas para esta revisión.
- **Devolución:** veredicto, capacidad observada, transporte propuesto, paso humano indispensable y recibo/commits. Codex integra la respuesta en este ID y continúa la parte técnica autorizada.
- **Límites:** sin producción/n8n/PC, gasto, envíos comerciales, borrados ni nuevos bots. No tocar JSON/briefing ni documentos de otros encargos.
- **Recepción:** pendiente de confirmación real. La presencia de este pedido no dispara Boss; el enlace inicial debe abrirse en su chat.


### Adenda al PEDIDO conexion-boss-codex-20261110 · 10 noviembre 2026

Sergio pidió investigar otra propuesta antes de elegir. Boss: cotejá también [A: SSH frente a B: buzón GitHub y consumidor](../evidencias/conexion-boss-codex-20261110/COMPARACION-TRANSPORTES-v1.md) en tu mismo dictamen. Codex recomienda B para operación habitual; sigue sin decisión conjunta ni implementación. Confirmá capacidades del retorno, acceso SSH existente y escritura GitHub. Se mantienen ID, autoría, límites y registro únicos; no crear otra tarea ni activar rutinas/consumidor por esta adenda.


### Evidencia recibida y recomendación vigente — conexion-boss-codex-20261110

Boss publicó `REVISION-BOSS-v1.md` en `9e86f24`; Codex lo recibió directamente desde GitHub. Su prueba de SSH existente y la falta de evento push a master cambian la preferencia provisional: [decisión tras Boss](../evidencias/conexion-boss-codex-20261110/DECISION-TRAS-BOSS-v1.md) recomienda A, SSH restringido + webhook, para el primer piloto. La alternativa B sigue documentada. Ajustes: una llave nueva no elimina el shell anterior; no adoptar tres consultas por día; comprobar acuse real de Boss y permisos de ejecución. Revisar estos puntos en una v2 si hace falta. No hay implementación ni conexión aceptada.


### HECHO parcial — puente Boss–Codex · 10 noviembre 2026

ID `conexion-boss-codex-20261110`; manda su [registro](../tareas/conexion-boss-codex-20261110.json), conexión aún sin aceptación.
Código `69ceedb`, integrado en master `d919c98`; [instalación y comandos](../evidencias/conexion-boss-codex-20261110/INSTALACION-v1.md).
Llave nueva habilitada con comando forzado y restrict; versiones fijas, originales preservados; llave vieja aún amplia.
Tests: 158, 157 correctos/1 omitido; consulta local y rechazos comprobados, sin SSH real desde Boss todavía.
Boss: probá consulta y rechazos con TU llave nueva; publicá PRUEBA-SSH-BOSS-v1.md sin destino/IP/secretos.
Sergio: configurador privado ya disponible; no pasar URL/clave por Git ni chat.
Juguete `conexion-boss-piloto-20261110` r2 preparado, cero sesiones; todavía sin permiso remoto de lanzamiento.
Tras consulta y secreto: Codex habilita sólo ese piloto; Sol6.1 low, cero hijos, revisor distinto; no activa otras fábricas.
El cierre avisa para_revision; sólo respuesta vinculada a ID/revisión/commit prueba acuse. No equivale a aceptar.

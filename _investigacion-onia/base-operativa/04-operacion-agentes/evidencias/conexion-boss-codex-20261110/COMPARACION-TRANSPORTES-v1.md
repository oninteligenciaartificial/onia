# Alternativa de conexión: GitHub como buzón, VPS como consumidor

10 noviembre 2026 · America/La_Paz. Investigación solicitada por Sergio; sin implementación ni activaciones. Complementa la [propuesta SSH](CONEXION-Y-ENCARGO-v1.md) en el mismo [ID del harness](../../tareas/conexion-boss-codex-20261110.json). No modifica la evidencia anterior ni representa acuerdo de Boss.

## Recomendación

Para la operación habitual de OnIA, Codex recomienda **B: solicitudes estructuradas en GitHub y un consumidor acotado en el VPS**, sujeto a validar el retorno a Boss y a aprobar su construcción. Evita entregar acceso SSH al servidor a Boss y usa el punto de encuentro que Sergio ya eligió. Requiere un componente nuevo de despacho; no está implementado ni se habilita con esta investigación.

**A: SSH restringido** sigue siendo el camino más corto para una prueba si Boss demuestra que ya tiene acceso legítimo y verificado al VPS. Sin esa evidencia no se puede asegurar que A tarde menos. Ambas opciones necesitan autorizaciones, deduplicación, resultados y revisión. No cambia el reparto de trabajo, el harness ni el cerebro; se comparan transportes.

## Comparación

| Criterio | A. Boss llama al VPS por SSH restringido | B. Boss deja solicitudes en GitHub |
|---|---|---|
| Acceso de Boss | Cliente SSH, clave dedicada, host verificado y comando forzado | Lectura/escritura del repo; no necesita credencial SSH del VPS |
| Programa nuevo | Adaptador de operaciones y mecanismo de devolución | Consumidor de solicitudes, controles de despacho y devolución |
| Inicio | Inmediato si hay conexión y cupo | Al detectar el pedido; intervalo propuesto de 60–120 s, sin promesa de latencia total |
| Si Boss se desconecta | La sesión debe quedar desacoplada y el resultado persistido | La solicitud permanece en GitHub; el consumidor puede continuar dentro de su autorización |
| Si el VPS se apaga | Hay que reconciliar antes de reenviar/reanudar | Solicitudes durables; también exige reconciliación antes de reejecutar |
| Permisos | Una clave mal restringida puede abrir más del VPS | Un escritor del repo podría introducir solicitudes; escribir no debe equivaler a autorizar |
| Mantenimiento | Clave, huella, adaptador y devolución | Consumidor, cursor de transporte, validación y devolución |
| Retorno a Boss | Evento filtrado o webhook autenticado | El mismo mecanismo; GitHub por sí solo no despierta a Boss |

No son medidas de rendimiento: es una comparación de diseño. Una prueba desde la cuenta de Boss decide si las dependencias existen.

## Cómo funcionaría B

1. Sergio autoriza una tarea o conjunto acotado desde Boss. La autorización tiene alcance, identificador, expiración y límites; su registro fiable debe quedar separado de la solicitud que Boss puede editar.
2. Boss guarda una solicitud JSON en una carpeta propuesta `pendientes/solicitudes/`, con ID único, ID de tarea del harness, operación permitida, revisión esperada, hash del briefing, entradas por commit y referencia a la autorización. El Markdown del buzón sigue como vista humana; no se ejecutan sus frases como órdenes.
3. Un programa sin LLM del VPS consulta sólo esa entrada. Valida el esquema y la autorización local, rechaza rutas/operaciones ajenas y pasa la operación al harness existente. El registro canónico conserva los estados y tres cupos globales incluyendo revisores.
4. El harness ejecuta, conserva la identidad de sesión y publica la entrega. Un revisor distinto coteja el commit. Las decisiones o correcciones vuelven por el mismo ID. No se usa el cierre de un issue ni una palabra HECHO como aceptación.
5. Un recibo saneado señala resultado o bloqueo y commit. El notificador envía un único aviso a Boss; Boss lee el registro y responde a Sergio. El aviso no contiene secretos ni el log completo.
6. Los reenvíos se concilian con solicitud, intento y sesión existentes. Si se cae la red después de lanzar, se consulta y reconcilia antes de volver a invocar Codex. No se promete ejecución exactamente una vez por usar GitHub.

Esto es un **despachador mínimo**, no el scheduler completo por carriles/pesos solicitado en el pasado. En el piloto sólo admite IDs explícitos y un plazo acotado. Sin tareas aprobadas no lanza modelos, ni decide trabajo comercial, ni despacha el backlog.

## Entrada y retorno: dos decisiones distintas

Para el primer consumidor puede reutilizarse la autenticación Git ya comprobada en el VPS: consultar master y recuperar cambios sólo cuando cambie. Leer objetos de una referencia fijada; no hacer `pull` y ejecutar automáticamente versiones nuevas del adaptador. No abrir puertos para recibir tareas.

GitHub recomienda webhooks antes que sondeo. La propuesta de sondeo acotado es un compromiso para evitar un receptor entrante en este VPS. Si se usa la API REST, requiere autenticación propia verificada, consultas condicionales cuando el endpoint las admita y respeto de los límites y reintentos indicados. ETag/304 no se aplica a comandos Git. El intervalo se debe medir, no atribuirle consumo despreciable sin prueba. [Buenas prácticas de GitHub](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api).

Para el retorno, el producto Grok Bot documenta rutinas por eventos GitHub o webhook; el disparador puede requerir una conexión distinta del conector GitHub. No se ha demostrado que esta cuenta admita un evento push filtrable por ruta. Si no lo admite, preferir un webhook saliente autenticado del VPS a Boss antes que despertar un LLM periódicamente. Su URL/token permanecen privados. Un 200 confirma recepción, no terminación. [Rutinas oficiales](https://docs.x.ai/grok-bot/skills-routines-and-automations).

Sin un retorno probado, B resuelve el transporte del encargo pero todavía no satisface el ida y vuelta que pidió Sergio. Lo mismo vale para A.

## Límites comunes y prueba que decide

- El permiso para lanzar no nace de un campo `aprobado=true`, de la autoría declarada de un commit ni de `--si-sergio`. El canal remoto no puede crear o ampliar el permiso local. Producción, n8n, publicación comercial y gasto conservan su autorización específica.
- El consumidor no ejecuta shell proporcionada por Boss ni carga código nuevo del repo automáticamente. Usa una versión fijada del adaptador, el checkout coordinador y el root de operación establecidos.
- Un único coordinador modifica los registros. El cursor/acuse sólo evita repetir mensajes; no se convierte en otro estado de tareas. Serializar recepción, revisiones esperadas y escritura; la concurrencia de ejecutoras la mantiene el harness.
- La pausa o revocación impide nuevos despachos, conserva evidencia y deja explícito qué trabajos ya estaban activos. No borrar ni matar procesos indiscriminadamente.
- Validar con fixtures: duplicados, corte tras lanzamiento, revisión obsoleta, permiso revocado, falta de cupo, log sensible, caída de GitHub y aviso repetido. Espera sin llamadas de modelos; avisos filtrados sin bucle por los propios commits.
- Después, una prueba autorizada desde Boss: pedir → ejecutar → revisión distinta → commit en master → Boss recibe y presenta. La conexión sólo queda aceptada cuando se comprueban todos esos pasos, incluido reenvío sin trabajo duplicado.

## Recursos, cuota y alternativas descartadas por ahora

No se solicita un nuevo proveedor, panel, servicio pago, n8n ni cambio de PC. El consumidor usa CPU/red del VPS; ejecutoras, revisores y rutinas de Boss consumen sus cuotas. El sondeo sin modelo no consume tokens, pero no es coste total cero ni suple la suscripción Codex después del 14. La cuota observada se registra en el recibo con fecha; la cuota de Grok no está disponible desde aquí. Las rutinas de Grok consumen uso en cada ejecución, por eso el aviso debe responder a resultados concretos. [Uso de rutinas](https://docs.x.ai/grok-bot/skills-routines-and-automations#routines-and-usage).

MCP HTTPS sería otra envoltura para el mismo adaptador, con autenticación y endpoint accesible; no resuelve por sí mismo retorno, aprobación o estado. El soporte Remote HTTPS/Command está documentado, no instalado en nuestra cuenta. [Conectores de Grok](https://docs.x.ai/grok-bot/computer-and-apps).

No elegir un runner de GitHub Actions compartiendo este VPS para resolver sólo la mensajería: amplía la ejecución de workflows en una máquina con servicios existentes y exige aislamiento adicional. GitHub advierte que los runners propios pueden quedar comprometidos por código no confiable incluso en repos privados. No se instaló ninguno. [Seguridad de runners](https://docs.github.com/en/actions/reference/security/secure-use#hardening-for-self-hosted-runners).

## Adenda al encargo de Boss

Compará A y B en tu mismo `REVISION-BOSS-v1.md` cuando respondas. Confirmá: (1) escritura real en el repo; (2) acceso SSH ya verificado, si existe; (3) tipos y filtros de eventos disponibles y posibilidad de webhook privado; (4) límites de uso observables. Recomendá una opción y explicá el motivo. No crees la rutina ni el consumidor para comprobar su disponibilidad. Si ya entregaste v1, agregá una v2 conservando la anterior. Codex leerá la respuesta desde GitHub; no hace falta que Sergio copie el dictamen.

La recomendación B es de Codex, no una aceptación conjunta ni autorización para construir el despachador. Se conserva la tarea en espera de revisión y elección.

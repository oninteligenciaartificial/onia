# Coordinación local y ejecución cloud · prueba real

**4 de noviembre de 2026, America/La_Paz.** Decisión de Sergio: comprobar si los chats cloud pueden coordinarse entre sí; si el despacho no está disponible, esta sesión local será coordinadora y las áreas seguirán ejecutando en cloud. La condición se comprobó en Jefe y Desarrollo. Este reparto actualiza la coordinación operativa del plan anterior, sin renombrar ni duplicar chats.

## Resultado por capacidad

| Capacidad | Esta sesión local | Jefe cloud | Desarrollo cloud |
|---|---|---|---|
| Consultar un chat existente | Disponible y usada | Probada con read_thread | Herramienta presente según catálogo revisado |
| Esperar/recuperar resultados | Probada con wait_threads | Probada con timeoutMs: 0 | Herramienta presente según catálogo revisado |
| Iniciar encargo en otro chat | **Probado con send_message_to_thread** | Ausente del catálogo actual | Ausente del catálogo actual |
| Crear chat independiente | Herramienta expuesta; no se necesitó crear ninguno en esta prueba | Ausente | Ausente |
| Delegar a subagentes internos | Usado en revisión documental | Usado en JEF-BASE-001/JEF-IMPL-001 | No requerido en esta prueba |

**Conclusión precisa:** en estos hosts cloud se pueden consultar otros chats, pero no iniciarles encargos con las herramientas actualmente expuestas. No afirmar que «no pueden comunicarse de ninguna forma» ni que todas las versiones de Codex tienen esta limitación. Tener subagentes internos tampoco equivale a enviar trabajo a los chats de área de la barra lateral.

La revisión del namespace nativo codex_app y catálogo real del Jefe corrigió el diagnóstico anterior que negaba toda lectura. Un mensaje de herramienta antigua que remite a otro servidor no acredita la disponibilidad de ese servidor.

## Evidencia de las dos pruebas

### COORD-PROBE-20261104 · origen cloud

Chat Jefe: `01a1a843-4afb-75f9-aa95-f35833fcb002`, host durable. Turno `01a1a9a8-1264-76bb-849e-6760a71ed87f`, completado.

El Jefe ejecutó read_thread y wait_threads contra Desarrollo: pudo leer su estado idle y un turno histórico. No encontró send_message_to_thread/create_thread; no hubo intento de envío ni rechazo de una operación de envío. El resultado histórico leído **no** se contabiliza como respuesta nueva a la prueba. No se crearon chats, subagentes o cambios de archivos por ese encargo.

### COORD-LOCAL-CLOUD-20261104 · origen local

Coordinadora local: `01a1a29c-3a3d-7b50-aef6-41305ce5faae`. Destino: Desarrollo cloud, `01a1a484-065a-76bc-94a2-9b2b148d6021`, host durable.

1. La herramienta local send_message_to_thread aceptó el encargo con el ID del chat destino.
2. Desarrollo completó el turno `01a1a9a9-9dd7-77e4-8df2-8b44397f38a2`.
3. Leyó SESIONES.md desde GitHub, HTTP 200, revisión **18843357389a82b900a4f16309f27c9e3ae7c18a**.
4. Recuperó **ONIA · Aprendizaje y criterio**, ID `01a1a935-c691-72d5-b055-e39970f5703e`, sin recibir el valor en el encargo.
5. Comprobó VM cloud onia y hostname de la ejecución; declaró read/wait disponibles y send/create ausentes.
6. Esta coordinadora recuperó el resultado terminado por wait_threads. La respuesta fue consultada desde local; **no fue un envío automático cloud→local**.

No se modificaron repositorios, credenciales, APIs de producción o servicios para estas pruebas. La prueba acredita un encargo de lectura completo, no capacidad ilimitada ni despacho periódico.

## Reparto que queda operativo

- **Coordinación local:** Sergio dirige aquí; esta sesión convierte prioridades en encargos acotados para los chats cloud existentes, confirma lanzamiento, recupera resultados, comprueba evidencia e integra decisiones en Git.
- **ONIA · Jefe cloud:** conserva planificación, síntesis, investigación y subagentes dentro de sus encargos. Puede consultar resultados cuando su catálogo lo permita. No se le atribuye iniciar chats de área.
- **Áreas cloud:** trabajan en onia con entradas concretas del repo. Devuelven resultado/artefacto/evidencia/siguiente paso en su chat; la coordinadora consulta la entrega.
- **Organización diaria:** única escritora del home/cola de Notion y Calendar conforme a autorización. La coordinación no crea tableros paralelos.
- **Subagentes:** subtareas temporales del encargo. No reemplazan silenciosamente una tarea prometida a una sesión visible.

Circuito: Sergio → coordinadora local → chat de área cloud → resultado consultado → QA/integración → Git y vista cotidiana. Cada encargo tiene ID, entrada, entregable y aceptación; una confirmación de envío no equivale a finalización.

## PC encendida y alternativa sin PC

La ejecución de un encargo cloud es remota. **La coordinación local necesita que esta sesión y sus herramientas estén disponibles** para despachar nuevas órdenes, revisar y continuar dependencias. No se probó apagar físicamente la PC; no se declara un servicio local activo 24/7 ni una cadena automática que siga coordinando con la app cerrada.

Mientras la PC no esté disponible, Sergio puede iniciar/continuar encargos cloud desde web/móvil y el agente cloud puede usar sus subagentes en ese encargo. Eso sirve para trabajo autocontenido; no demuestra que pueda despachar nuevos turnos a todos los chats de área. Una coordinación completamente cloud entre chats queda como capacidad pendiente: no se resuelve instalando Linux/Cloudflare sin una herramienta de despacho compatible. El lanzador n8n→Codex tiene además su autenticación pendiente registrada en ESTADO.

## Fuente oficial y entrega anterior

La consolidación **1884335** incorporó29 archivos: quince Pages documentales, currículo, plan y registros. Se compararon los29 textos con la revisión remota, sin diferencias;15 SHA-256 coinciden. Jefe confirmó lectura de PLAN/ESTADO/SESIONES/README desde ese commit y recuperó el hito comercial con su límite de validación.

Las Pages principales (plan, biblioteca, referentes y guiones) recibieron enlace de autoridad a Git, con relectura comprobada. Los medios siguen cloud. JEF-IMPL-001 y el incidente de despacho fueron añadidos después del corte; no se presentan como parte de 1884335 ni se relanzan por esta prueba. Su integración debe preservar resultados ya ejecutados y no confundir prototipos/tests aislados con automatizaciones reales.

## Documentación oficial consultada

- [OpenAI Docs: Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents): describe creación, instrucciones posteriores, espera y consolidación de subagentes. No garantiza paridad de herramientas entre todos los chats independientes.
- [OpenAI Docs: Codex environments](https://learn.chatgpt.com/docs/environments/modes): Local/Worktree ejecutan en la computadora; Cloud es una tarea remota con archivos propios. Permite iniciar/continuar cloud desde web/móvil; no transfiere automáticamente archivos, procesos o sesiones locales.

La conclusión de disponibilidad de send/read/create viene de las pruebas de los hosts, no se infiere del texto general de la documentación. Revalidar si cambian entorno, herramientas o versión de la aplicación.


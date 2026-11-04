# ONIA Platform: diagnóstico inicial para integrar el harness

Revisión del 3 de noviembre de 2026. Repositorio privado confirmado mediante captura y conector: [oninteligenciaartificial/onia-platform](https://github.com/oninteligenciaartificial/onia-platform), ID `1208814283`, rama predeterminada `master`.

## Identidad y estado comprobados

- GitHub y `git ls-remote` coinciden en `a0488f04200b14c95caf0013043716b16efa1f1d` para `master`. La referencia local `origin/master` coincide; se leyó mediante `git show`, sin cambiar de rama.
- La carpeta `C:/dev/proyectos/onia-platform` está en `claude/f2-f3-panel`, commit `7060b7c910a6aeab9be50f078d3dcf75aa97f710`. Tiene 68 entradas modificadas/no rastreadas. Ese trabajo no se fusionó, descartó ni interpretó como contenido de `master`.
- El entorno Codex Cloud llamado `ONIA Platform` aparece `ready`, `runnable: true`, asociado a `github-1208814283` y `master`: corresponde a este producto. La consulta de configuración no demuestra instalación reproducible, ejecución activa o salud del VPS.
- No se iniciaron tareas cloud, procesos de la aplicación, pruebas, pagos ni despliegues. No se leyeron valores de archivos de credenciales.

## Lo que ya existe

| Área | Evidencia en el commit revisado | Implicación |
|---|---|---|
| Producto | `PRODUCT.md` define dental, estética, comercio, importadora acotada y servicios profesionales. | La organización debe reflejar una plataforma por rubros; no inventar cinco productos nuevos. |
| Aplicación | `package.json`: Next 16.2.7 declarado como rango, React 19.2.4, Prisma 7, Supabase, Tailwind 4; build con webpack. | Reutilizar scripts existentes. Las versiones instaladas y el runtime productivo no fueron comprobados. |
| Reglas y continuidad | `AGENTS.md`, `docs/ORCHESTRATOR.md`, `docs/AGENT_COORDINATION_ORDER.md`, `docs/PROJECT_BACKLOG.md`, `docs/HARNESS_COMANDOS_CLAUDE_CODEX.md`. | Ya existe una estructura de trabajo. La propuesta debe simplificar y conectar sus fuentes. |
| Skills | 16 archivos `SKILL.md` versionados bajo `.agents/skills`, muchos de diseño, incluidos Impeccable, shadcn y minimalist-ui. | La recomendación anterior sobre Impeccable pasa a evaluar la copia existente; no instalar otra. No se auditó cada skill ni se ejecutaron sus scripts. |
| Automatización | `n8n/` y `n8n-workflows/` contienen catálogos parcialmente solapados y guías diferentes. | Comparar con los workflows realmente activos antes de elegir fuente canónica. Los archivos no prueban activación. |
| Infraestructura | Dockerfile, Compose de ejemplo, scripts self-hosted y CI. | Son materiales para operar el producto, no evidencia de su configuración actual en Hostinger. |

Fuentes estables: [PRODUCT.md](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/PRODUCT.md), [package.json](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/package.json), [reglas](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/AGENTS.md).

## QR automático: implementación presente, operación pendiente de comprobar

Se leyó este recorrido en el código:

1. `app/api/subscription-payment/bcp-qr/route.ts` verifica usuario/permisos, obtiene el importe del catálogo y solicita un QR mediante `lib/gateway/bcp-qr.ts`.
2. Guarda un pago pendiente con referencia del circuito BCP.
3. `app/api/webhooks/bcp/route.ts` autentica el callback, consulta al banco y usa los helpers de validación/activación del plan. Contiene manejo de reintentos y pagos que requieren revisión humana.
4. `app/api/subscription-payment/status/route.ts` permite consultar el estado del pago y del plan.

El cliente BCP depende de configuración bancaria y conserva preguntas pendientes sobre producción, certificados y contrato. Si falta configuración, la generación devuelve indisponibilidad. Leer esta implementación no acredita que el banco la haya habilitado ni que sea suficiente cargar variables para funcionar correctamente.

Los documentos de cobro del 21 y 27 de septiembre registran pruebas aisladas y simulaciones, y excluyen explícitamente la demostración de un cobro comercial real. No se repitieron ni se presentaron como pruebas ejecutadas hoy. Este circuito cobra la suscripción de ONIA; no demuestra que todos los negocios clientes tengan cobro bancario automático propio.

Fuentes: [generación QR](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/api/subscription-payment/bcp-qr/route.ts), [callback](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/app/api/webhooks/bcp/route.ts), [evidencia histórica y límites](https://github.com/oninteligenciaartificial/onia-platform/blob/a0488f04200b14c95caf0013043716b16efa1f1d/docs/ONIA_V1_COBRO_RENOVACION_2026-09-27.md).

## Problemas de contexto observados

- El README y `docs/ONIA_PLATFORM.md` todavía presentan una solución dental; `PRODUCT.md` define cinco rubros. La referencia antigua de junio también contiene una oferta de planes que no debe confundirse con el catálogo actual del código.
- `docs/SKILLS_BEFORE_ACTION.md` referencia rutas de otras carpetas y skills personales. La ruta documentada de `devex-review` no estaba disponible en esta revisión. La presencia de una skill en un documento no demuestra que exista en un entorno cloud.
- Hay dos guías n8n con diferencias de triggers y credenciales. No importar ni activar ambas como si fueran complementarias sin inspeccionar los flujos.
- Hay reglas globales, coordinación, orquestación, manuales e historial extenso. Mi evaluación es que cargar todos esos textos en cada tarea añade contexto repetido. Conviene mantener un índice corto con lecturas por área y evidencia de vigencia.
- Las notas históricas sobre modelo, cuota, goals y autorizaciones de otras sesiones no prueban la configuración ni los permisos actuales. No se aplicaron cambios globales basándose en ellas.

La revisión independiente confirmó dos diferencias adicionales: `skills-lock.json` registra 15 skills, frente a 16 en `.agents/skills` y otras 6 bajo `.claude/skills`; además, la guía de selección limita normalmente la carga a 2–3 skills mientras coordinación exige más por algunos roles. El CI versionado usa un runner propio `onia-vps`; su disponibilidad y última ejecución no fueron consultadas. Estos hallazgos refuerzan la necesidad de conciliar el inventario antes de trasladar el harness a otro entorno. No se modificaron reglas ni se ejecutaron workflows.

## Encaje propuesto y siguiente unidad de trabajo

1. **ONIA Platform conserva el código y estado técnico del producto.** Su backlog existente mantiene las tareas técnicas; esta base de investigación enlaza resultados, sin crear un backlog técnico competidor.
2. **La base operativa conserva el contexto privado y las prioridades personales/comerciales.** No publicar estos datos dentro de las skills para clientes. La ubicación definitiva del harness empresarial se decide tras revisar el espacio Hermes existente, no creando otro repositorio por defecto.
3. **Las skills se cargan según la tarea.** Auditar primero las 16 versionadas, su portabilidad y solapamientos; luego adaptar solo las brechas concretas del catálogo del reel.
4. **n8n conecta procesos repetibles con permisos definidos.** Su inventario activo y la versión desplegada deben obtenerse del VPS. Las reglas de cobro y activación siguen siendo responsabilidad del backend.
5. **Codex Cloud ya tiene la asociación correcta.** El siguiente resultado técnico útil es una comprobación aislada y reproducible del commit elegido, con entorno de desarrollo y sin acceso a datos productivos. No está ejecutada ni programada.

Unidad inmediata propuesta: preparar un índice de contexto vigente del producto, con enlaces a `PRODUCT.md`, catálogo de planes, backlog y evidencia QR; inventariar qué skills viajan con el repo y cuáles dependen de esta máquina. Termina cuando otro entorno puede identificar el mismo commit, tarea y comprobación sin cargar toda la historia. Es preparación del harness, no certificación para vender ni auditoría completa de seguridad.

## Verificación de esta revisión

Herramientas seleccionadas: conector GitHub para identidad y archivos, Git para lectura del commit confirmado, herramienta de entornos cloud para asociación, skill `continuidad-de-trabajo` para estado y fuentes. Una revisión paralela acotada se asignó conforme a `AGENTS.md`, sin permisos de escritura. No hizo falta investigación externa de APIs/frameworks porque no se introdujeron dependencias ni comportamiento nuevo. No se ejecutaron tests o build: no hubo cambios en el producto y esta entrega es documental.

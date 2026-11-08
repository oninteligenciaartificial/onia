# Entrada del harness ONIA

El repositorio privado [oninteligenciaartificial/onia](https://github.com/oninteligenciaartificial/onia) contiene el harness. El entorno de ejecución es **onia** en Codex Cloud. El producto ONIA Platform conserva su propio repositorio.

## Empezar un encargo

1. Leer [reglas comunes](../04-operacion-agentes/reglas-comunes.md) y [ESTADO.md](ESTADO.md). Son la autoridad compartida y la entrega vigente.
2. Tomar el encargo vigente de Sergio, el [plan continuo por áreas](../01-negocio/PLAN.md) y el siguiente resultado de [ESTADO.md](ESTADO.md). [ORQUESTACION.md](../04-operacion-agentes/ORQUESTACION.md) explica cómo preparar, delegar y cerrar. Los planes anteriores quedan como historial, no como segunda autoridad.
3. Cargar la skill directora y los archivos necesarios para ese encargo. [orquestacion.json](../04-operacion-agentes/orquestacion.json) mantiene las rutas por área.
4. Ejecutar, comprobar y registrar el resultado. Antes de cambiar de sesión, conservar una entrega saneada en Git y los artefactos en su almacén correspondiente.

## Dónde está cada cosa

| Necesidad | Fuente |
|---|---|
| Estado real, pruebas y siguiente acción | [ESTADO.md](ESTADO.md) |
| Plan oficial, decisiones vigentes y programas continuos | [PLAN.md](../01-negocio/PLAN.md) |
| Entregas recuperadas de la sesión local y Pages | [Consolidación del 4 de noviembre](../99-archivo/2026-11-04/README.md) |
| Distribución entre Codex, archivos, n8n y producto | [Arquitectura](../06-plataforma/arquitectura.md) |
| Instalación e inicio del entorno | [Configuración cloud](../05-herramientas/cloud/CONFIGURAR-ONIA.md) |
| Encargos, subagentes y continuidad | [Orquestación](../04-operacion-agentes/ORQUESTACION.md) |
| Coordinación diaria, entradas y memoria compartida | [Cerebro diario](../02-contenido/CEREBRO-DIARIO.md) |
| Diseño del panel móvil de vida, contenido y actualidad | [Panel diario](../02-contenido/PANEL-DIARIO.md) |
| Chats cloud por área | [Sesiones](../04-operacion-agentes/SESIONES.md) |
| Fuentes, ejercicios y criterio para aprender | [Aprendizaje](../99-archivo/2026-11-04/aprendizaje.md) |
| Cuenta, alcance y ubicación de cada acceso | [Accesos](../05-herramientas/accesos.md) |
| Materiales de Sergio y entregables | [Carga inicial](../05-herramientas/cloud/CARGA-INICIAL.md) |
| Nueve skills por área y decisión sobre los treinta candidatos | [Skills por área](SKILLS-POR-AREA.md) |
| Procedencia de candidatos y decisiones | [Auditoría de repositorios](../99-archivo/auditoria-30-repos.md) |
| Fallos observados y correcciones | [Registro de errores](../04-operacion-agentes/registro-de-errores.md) |
| Investigación curada, referentes, formatos y oferta en revisión | [Índice del 4 de noviembre](../03-referentes/notas-2026-11-04/README.md) |
| Mapa del repositorio y lectura por área | [Mapa](MAPA.md) |
| Operación cloud, soluciones y pruebas de aceptación | [Operar en cloud](../05-herramientas/cloud/OPERAR.md) |

**ONIA · Jefe** coordina el plan y las decisiones; Organización mantiene Notion/Calendar. Git es la fuente oficial de documentación, Pages conserva procedencia y medios, y Notion es la vista cotidiana. Las instrucciones actuales de Sergio prevalecen y se consolidan en la fuente pertinente.

Los registros de `operacion/` y el contexto de `privado/` no viajan con Git. Su ausencia en otra sesión no se resuelve suponiendo que el chat anterior transfirió los datos. Usar la entrega versionada, comprobar la revisión y el acceso al material necesario. ONIA-CENTRAL queda excluido como fuente.

# Entrada del harness ONIA

El repositorio privado [oninteligenciaartificial/onia](https://github.com/oninteligenciaartificial/onia) contiene el harness. El entorno de ejecución es **onia** en Codex Cloud. El producto ONIA Platform conserva su propio repositorio.

## Empezar un encargo

1. Leer [reglas comunes](reglas-comunes.md) y [ESTADO.md](ESTADO.md). Son la autoridad compartida y la entrega vigente.
2. Tomar el encargo vigente de Sergio y el siguiente resultado de [ESTADO.md](ESTADO.md); [PLAN.md](PLAN.md) conserva criterios originales y [ORQUESTACION.md](ORQUESTACION.md) explica cómo preparar, delegar y cerrar.
3. Cargar la skill directora y los archivos necesarios para ese encargo. [orquestacion.json](orquestacion.json) mantiene las rutas por área.
4. Ejecutar, comprobar y registrar el resultado. Antes de cambiar de sesión, conservar una entrega saneada en Git y los artefactos en su almacén correspondiente.

## Dónde está cada cosa

| Necesidad | Fuente |
|---|---|
| Estado real, pruebas y siguiente acción | [ESTADO.md](ESTADO.md) |
| Distribución entre Codex, archivos, n8n y producto | [Arquitectura](arquitectura.md) |
| Instalación e inicio del entorno | [Configuración cloud](cloud/CONFIGURAR-ONIA.md) |
| Encargos, subagentes y continuidad | [Orquestación](ORQUESTACION.md) |
| Coordinación diaria, entradas y memoria compartida | [Cerebro diario](CEREBRO-DIARIO.md) |
| Diseño del panel móvil de vida, contenido y actualidad | [Panel diario](PANEL-DIARIO.md) |
| Chats cloud por área | [Sesiones](SESIONES.md) |
| Cuenta, alcance y ubicación de cada acceso | [Accesos](accesos.md) |
| Materiales de Sergio y entregables | [Carga inicial](cloud/CARGA-INICIAL.md) |
| Nueve skills por área y decisión sobre los treinta candidatos | [Skills por área](SKILLS-POR-AREA.md) |
| Procedencia de candidatos y decisiones | [Auditoría de repositorios](auditoria-30-repos.md) |
| Fallos observados y correcciones | [Registro de errores](registro-de-errores.md) |
| Investigación curada, referentes, formatos y oferta en revisión | [Índice del 4 de noviembre](investigacion/2026-11-04/README.md) |
| Mapa del repositorio y lectura por área | [Mapa](MAPA.md) |
| Operación cloud, soluciones y pruebas de aceptación | [Operar en cloud](cloud/OPERAR.md) |

Los registros de `operacion/` y el contexto de `privado/` no viajan con Git. Su ausencia en otra sesión no se resuelve suponiendo que el chat anterior transfirió los datos. Usar la entrega versionada y comprobar el acceso al material necesario. ONIA-CENTRAL queda excluido como fuente.

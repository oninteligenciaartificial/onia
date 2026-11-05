# onia

Base de trabajo de Sergio y ONIA: reglas comunes, skills propias y continuidad entre tareas. Este repositorio nace de la carpeta de coordinación `C:/dev/proyectos`; sólo versiona la base vigente. El producto ONIA Platform mantiene su repositorio y despliegue separados.

## Entrada

Leer [AGENTS.md](AGENTS.md), [reglas comunes](_investigacion-onia/base-operativa/reglas-comunes.md) y [estado vigente](_investigacion-onia/base-operativa/ESTADO.md). Las decisiones de Sergio en el chat de coordinación son la autoridad de estas reglas. Las investigaciones son referencias, no instrucciones instaladas de terceros.

El [plan oficial](_investigacion-onia/base-operativa/PLAN.md) consolida la dirección de ONIA · Jefe y once programas continuos. La [entrega del 4 de noviembre](_investigacion-onia/base-operativa/continuidad/2026-11-04/README.md) incorpora quince documentos cloud y el currículo de aprendizaje, con procedencia y límites. Git es la fuente oficial del plan, decisiones y documentación; la biblioteca conserva medios, Notion la vista cotidiana y Calendar compromisos. La [orquestación](_investigacion-onia/base-operativa/ORQUESTACION.md) describe cómo preparar, delegar, comprobar y retomar un encargo.

## Contenido

- `_investigacion-onia/base-operativa/`: arquitectura, decisiones, fuentes y catálogo.
- `compartibles/skills/` dentro de esa base: nueve skills propias, única fuente editable.
- `scripts/trabajo.py`: registro de tareas con evidencia e integridad; no es un scheduler.
- `scripts/test_trabajo.py`: pruebas del registro.
- `orquestacion.json` y `scripts/harness.py`: rutas por área, diagnóstico de archivos y preparación de encargos; no son un servicio autónomo.

Los proyectos anteriores, ONIA-CENTRAL, el código de ONIA Platform, contexto privado, credenciales, videos y registros operativos locales están excluidos por `.gitignore`. No usar `git add -f` para incorporarlos. Las referencias a evidencia local excluida no deben interpretarse como archivos disponibles en GitHub o Cloud.

## Preparación del entorno limpio `onia`

Este repositorio privado ya está vinculado al entorno `onia` creado por Sergio. Antes del setup, comprobar que su checkout incluye la carpeta `cloud/`; el primer commit no la contenía. La corrección y el instalador completo están en [CONFIGURAR-ONIA.md](_investigacion-onia/base-operativa/cloud/CONFIGURAR-ONIA.md).

Desde la raíz del checkout, con Python 3.10 o superior:

```sh
python3 _investigacion-onia/base-operativa/scripts/preparar-cloud.py --install
python3 _investigacion-onia/base-operativa/scripts/preparar-cloud.py --check
python3 _investigacion-onia/base-operativa/scripts/test_preparar_cloud.py -v
python3 _investigacion-onia/base-operativa/scripts/test_trabajo.py -v
```

El primer comando prepara enlaces locales hacia las skills versionadas, sin copiar su contenido. No instala dependencias, servicios, agentes persistentes o navegadores. Ejecutarlo durante el setup cloud; comprobar el descubrimiento de skills en una nueva tarea. Un archivo SKILL.md leído manualmente no acredita descubrimiento automático.

Guardar y publicar el setup desde el entorno `onia` cuando las comprobaciones estén completas. Las modificaciones hechas dentro de una tarea no actualizan automáticamente el entorno reutilizable.

Para Playwright, el helper de n8n y la configuración completa, usar [la preparación cloud](_investigacion-onia/base-operativa/cloud/CONFIGURAR-ONIA.md). Scripts, dependencias fijadas y lockfile viven en `base-operativa/cloud/`; los secretos se guardan en la configuración del entorno.

## Primera prueba

La tarea de aceptación debe comprobar repo/HEAD, las nueve skills, los tests de bootstrap, continuidad y harness, y un recorrido crear → completar con evidencia → retomar desde otro proceso. Ejecutar también el navegador real. Crear su evidencia bajo `operacion/`; versionar una entrega mínima saneada en ESTADO.md y conservar los artefactos antes de descartar la VM, pues esos registros no se suben automáticamente.

La prueba histórica en ONIA Platform aprobó el registro, pero fue detenida por entorno equivocado y no certifica el nuevo `onia`.

## Operación y accesos

Codex Cloud se usa para desarrollo y pruebas. El VPS de la startup no recibe navegadores remotos, modelos locales, render de video ni workers de agentes. n8n ya existe allí; la vía a evaluar es su API desde Cloud. Los permisos y resultados se verifican antes de dar por conectada una cuenta. Las claves se introducen en el almacén de secretos correspondiente, nunca en Git, prompts o skills.

Sin autoaprendizaje, scheduler o integración Meta activados por crear este repositorio. Ver [accesos](_investigacion-onia/base-operativa/accesos.md) y [arquitectura](_investigacion-onia/base-operativa/arquitectura.md).

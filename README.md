# onia

Base operativa de Sergio y ONIA: reglas comunes, skills y continuidad de tareas. Repositorio privado operativo: oninteligenciaartificial/onia, rama master, entorno Cloud onia. ONIA Platform conserva su repo de producto; onia-harness queda como referencia.

## Empezar

Leer [AGENTS.md](AGENTS.md), [reglas comunes](_investigacion-onia/base-operativa/reglas-comunes.md) y [ESTADO](_investigacion-onia/base-operativa/ESTADO.md). [ORQUESTACION](_investigacion-onia/base-operativa/ORQUESTACION.md) selecciona área y skill pertinente. El contexto histórico se consulta por encargo, sin reactivar objetivos anteriores.

- [Inicio Cloud](_investigacion-onia/base-operativa/cloud/INICIO-SESION.md): comprobar entorno y leer fuentes; separar lectura de descubrimiento nativo.
- [Continuidad](_investigacion-onia/base-operativa/cloud/CONTINUIDAD.md): crear, retomar, revisar y compartir una tarea con el CLI existente.
- [Uso desde iPhone](_investigacion-onia/base-operativa/cloud/MOVIL.md): iniciar y continuar en Cloud.
- [Informe de consolidación](_investigacion-onia/base-operativa/continuidad/2026-11-06/consolidacion-harness/INFORME.md): pruebas, revisiones y límites.

## Qué conserva el repo

Las nueve skills propias tienen una única fuente editable en base-operativa/compartibles/skills. El manifiesto mantiene seis áreas y nueve apoyos externos opcionales. harness.py prepara briefings y trabajo.py mantiene el registro; no son agentes residentes ni un scheduler.

Una tarea compartible usa un registro saneado bajo continuidad/tareas y evidencia versionada. Los auxiliares de operacion, datos personales, credenciales, sesiones, medios privados y ONIA-CENTRAL quedan fuera de Git. No usar git add -f para incorporarlos. La presencia de una referencia local no acredita disponibilidad Cloud.

## Preparar y comprobar Cloud

El setup reproducible y sus dependencias están en [CONFIGURAR-ONIA](_investigacion-onia/base-operativa/cloud/CONFIGURAR-ONIA.md). El instalador prepara los enlaces de skills; comprobarlos no prueba anuncio nativo. Las skills personales del equipo no se trasladan por esos enlaces.

Desde la raíz, con Python 3.10 o superior:

```sh
python3 -B -m unittest discover -s _investigacion-onia/base-operativa/scripts -p 'test_*.py' -v
python3 _investigacion-onia/base-operativa/scripts/harness.py doctor
```

Cambiar el repo no actualiza por sí solo el snapshot reusable. Tras revisión, publicar Git y preparar/republicar el entorno cuando corresponda; comprobar después una sesión nueva. Una tarea existente conserva su propio estado.

Las cuentas, servicios y operaciones externas se prueban sólo si el encargo las necesita y tiene autorización aplicable. Las claves se obtienen de su integración o almacén correspondiente. Los servicios VPS, n8n y producto mantienen sus alcances propios; esta consolidación no los instala ni activa.

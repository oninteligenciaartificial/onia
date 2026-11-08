# Sergio y ONIA: entrada del espacio de trabajo

Para encargos de Sergio y ONIA, la base vigente está en `_investigacion-onia/base-operativa/`.
Leé `00-MAPA/ESTADO.md` y `04-operacion-agentes/reglas-comunes.md` allí antes de continuar trabajo de ese sistema. La guía de carpetas es `00-MAPA/ESTRUCTURA.md`. Son referencias a una sola fuente; no copies sus reglas a cada proyecto.

Las instrucciones actuales de Sergio prevalecen sobre propuestas históricas. ONIA-CENTRAL está excluido como fuente: no consultar ni importar sus reglas, skills o estados para este trabajo.

Consultá `privado/contexto.md` sólo si la tarea necesita datos personales, horarios o recursos de Sergio; no incluirlo en paquetes públicos. Para código del producto, leer además las instrucciones técnicas aplicables en onia-platform y cotejar el estado real antes de editar. No extender estas decisiones comerciales a proyectos ajenos al encargo.

Las skills propias tienen sus fuentes editables en `base-operativa/05-herramientas/compartibles/skills`, salvo `preparar-oferta-y-embudo`, que está en `base-operativa/01-negocio/preparar-oferta-y-embudo`; los enlaces de `.agents/skills` dependen de la preparación del entorno. Al iniciar un encargo, aplicar la selección y lectura por área de `base-operativa/04-operacion-agentes/ORQUESTACION.md`; cargar sólo las pertinentes. En Cloud seguir `base-operativa/05-herramientas/cloud/INICIO-SESION.md`, incluyendo recuperación por ID/commit si el encargo la pide. El historial se consulta sólo cuando es pertinente. La existencia de instrucciones no acredita su carga automática, conexiones, tareas cloud o resultados.

## Arranque y cierre de una sesión del harness

1. Comprobar `pwd`, rama, HEAD y cambios. Leer las reglas comunes, `04-operacion-agentes/boss-memoria.md` y la tarea/briefing recibidos, bajo `_investigacion-onia/base-operativa/`. Recuperar su ID con `harness.py retomar ID` desde el checkout coordinador cuando corresponda. No asumir contexto del chat anterior.
2. Trabajar una sola tarea en el worktree asignado y sólo sus rutas. El coordinador mantiene el registro canónico; no crear una segunda copia de tarea ni modificar la proyección del briefing. Leer la directora canónica pertinente.
3. Si faltan enlaces de skills propias, ejecutar `bash _investigacion-onia/base-operativa/05-herramientas/scripts/instalar-skills-locales.sh`. Usa `orquestacion.json`, crea sólo enlaces ausentes y conserva cualquier destino diferente. Su presencia no acredita descubrimiento automático en esta sesión.
4. Al entregar: comprobaciones proporcionales, commit y push de la rama asignada. Informar hash, evidencia y límites. El coordinador ejecuta `harness.py cerrar`, que comprueba el commit remoto y retira únicamente el worktree limpio, conservando la rama.
5. Lanzar revisión independiente de sólo lectura, recoger el veredicto y usar `aceptar` sólo si es bueno y vigente. Integrar a `master`, comprobar y publicar. Verificar el hash en `origin/master` antes de declarar terminado. Los comandos exactos están en ORQUESTACION.

Un revisor no ejecuta los pasos de edición, commit o push: coteja el commit de entrega con la aceptación y emite su veredicto estructurado. No lanza otra tarea.

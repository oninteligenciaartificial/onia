**Fuentes de la base operativa — consulta del 3 de noviembre de 2026**

El repositorio público [openai/skills](https://github.com/openai/skills/blob/main/README.md) se consultó mediante el conector de GitHub. Su README lo marca como deprecado y remite a [openai/plugins](https://github.com/openai/plugins/blob/main/README.md). Se usó el sucesor para examinar ejemplos actuales.

| Ejemplo leído | Patrón que informa el diseño | Límite de reutilización |
|---|---|---|
| [writing-skills](https://github.com/openai/plugins/blob/main/plugins/superpowers/skills/writing-skills/SKILL.md) | Descripciones precisas, instrucciones reutilizables y comprobación con casos reales. | Sus reglas particulares no se convierten en instrucciones de esta sesión. |
| [notion-spec-to-implementation](https://github.com/openai/plugins/blob/main/plugins/notion/skills/notion-spec-to-implementation/SKILL.md) | Trazabilidad entre necesidad, tarea, evidencia y estado. | Los requisitos específicos de Notion no se imponen a esta base. |

Los textos nuevos de las skills se redactaron para este trabajo. Los archivos consultados tienen licencias propias: [Superpowers](https://github.com/openai/plugins/blob/main/plugins/superpowers/LICENSE) y [skill de Notion](https://github.com/openai/plugins/blob/main/plugins/notion/skills/notion-spec-to-implementation/LICENSE.txt). Para incorporar material de las 30 skills futuras se revisará su licencia y procedencia antes de copiarlo o distribuirlo. La licencia del paquete propio se decidirá antes de publicarlo.

El formato y la activación se contrastaron con [Build skills](https://learn.chatgpt.com/docs/build-skills). Para distribuir capacidades fuera del repositorio, la documentación contempla empaquetarlas como plugins. En este momento se conserva un paquete local revisable; no se publicó un plugin.

La capacidad de nube y Personal vault se contrastaron con [Cloud environments](https://learn.chatgpt.com/docs/environments/cloud-environments). El estado de los entornos existentes proviene de la herramienta de cuenta, no de documentación pública. La arquitectura enlaza las fuentes de ejecución, secretos e infraestructura junto a cada afirmación correspondiente.

La [revisión del reel recibido](../02-contenido/revision-reel-DfBQ1AgOC1S.md) registra los 30 nombres de su descripción, el alcance limitado de la inspección audiovisual y las fuentes primarias de cuatro repositorios consultados. Sus recomendaciones son documentales, sin pruebas de ejecución. Siguen pendientes los otros 26 candidatos y la instalación real del VPS.

La [revisión de ONIA Platform](../06-plataforma/revision-onia-platform.md) usa el repositorio privado identificado por Sergio, con commit de `master` confirmado por GitHub y Git. Contiene enlaces a fuentes fijadas por commit y distingue código leído, evidencia histórica y operación aún no verificada. La copia de Impeccable ya presente en ONIA no se presume idéntica a la versión pública revisada en el reel.

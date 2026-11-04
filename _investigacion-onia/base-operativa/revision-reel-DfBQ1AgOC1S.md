# Selección inicial del catálogo del reel

> Revisión histórica parcial. La selección vigente está en [auditoría de los 30 repositorios](auditoria-30-repos.md), que amplía los 26 candidatos antes pendientes. Consultar también [selección y recorrido](seleccion-y-recorrido.md). Las notas de falta de lectura que siguen describen la primera revisión, no la cobertura actual.

Consulta: 3 de noviembre de 2026. Fuente: [reel de @heysansser](https://www.instagram.com/reel/DfBQ1AgOC1S/).

**Resultado: adaptar candidatos seleccionados; no instalar el catálogo completo.** La publicación presenta 30 proyectos, no un único repositorio listo para ONIA. Esta evaluación no equivale a una auditoría de ejecución ni a una aprobación de instalación.

## Evidencia y cobertura

Se accedió a la publicación mediante navegador y se leyó su descripción completa. Se inspeccionó una imagen del video con Last30Days y UnderstandAnything; no se verificó todo el contenido audiovisual ni se obtuvo una transcripción del audio. Los 30 nombres proceden de la descripción. No se solicitaron enlaces por comentarios o mensajes al autor.

Se leyeron los README y LICENSE de cuatro repositorios: Marketing Skills, Matt Pocock Skills, Superpowers e Impeccable. También se leyeron las instrucciones de `offers`, `product-marketing` y `to-spec`. No se ejecutaron instaladores, hooks ni agentes. Las ramas consultadas fueron `main`; antes de incorporar archivos habrá que fijar su commit exacto.

## Selección razonada

### Marketing Skills: adaptar primero

Fuente: [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills/blob/main/README.md). [Licencia MIT leída](https://github.com/coreyhaines31/marketingskills/blob/main/LICENSE).

El README declara compatibilidad con Codex. [product-marketing](https://github.com/coreyhaines31/marketingskills/blob/main/skills/product-marketing/SKILL.md) mantiene contexto comercial y aprendizajes; [offers](https://github.com/coreyhaines31/marketingskills/blob/main/skills/offers/SKILL.md) estructura ofertas. Son pertinentes para preparar un taller y su material de venta.

Entradas: producto, público, precio, alcance, pruebas disponibles y capacidad de entrega. Salidas propuestas: ficha comercial y oferta comprobable. Para redactar esos documentos no hace falta conectar cuentas; otras integraciones del catálogo pueden requerir servicios adicionales.

Adaptación: separar datos personales y comerciales; usar español y bolivianos; señalar hipótesis; excluir estimaciones de mejora de conversión sin datos propios; redactar sin publicar o enviar mensajes. No convertir recomendaciones del autor en resultados garantizados. Preservar avisos de licencia si se incorpora material. Las demás skills no quedaron auditadas.

### Matt Pocock Skills: adaptar especificaciones breves

Fuente: [mattpocock/skills](https://github.com/mattpocock/skills/blob/main/README.md). [Licencia MIT leída](https://github.com/mattpocock/skills/blob/main/LICENSE).

El README contempla Codex. Se revisó [to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md): transforma conversación y conocimiento del código en una especificación y contempla publicarla en el gestor de incidencias configurado.

Entradas: necesidad acordada, repositorio y decisiones existentes. Salida propuesta: tarea local con problema, alcance, resultado esperado y comprobación. Adaptación: extensión proporcional al cambio, archivo local por defecto y sin publicaciones automáticas o entrevistas repetidas. Revisar ONIA antes de establecer convenciones. Se solapa con la continuidad de trabajo ya preparada: mantener una sola fuente de tareas y decisiones.

### Superpowers: posponer el paquete completo

Fuente: [obra/superpowers](https://github.com/obra/superpowers/blob/main/README.md). [Licencia MIT leída](https://github.com/obra/superpowers/blob/main/LICENSE).

El README describe planificación, pruebas, revisión y ejecución con agentes, y presenta sus flujos como obligatorios. Mi evaluación es que imponer todo el proceso ahora puede añadir trabajo y consumo sin resolver primero la continuidad de ONIA.

Conservar como referencia para depuración y verificación. Antes de adaptar una skill concreta, leerla completa. No adoptar automáticamente reglas de subagentes, confirmaciones o pruebas para cada cambio. No se copiaron sus archivos.

### Impeccable: adaptar revisión de diseño, posponer modo live

Fuente: [pbakaus/impeccable](https://github.com/pbakaus/impeccable/blob/main/README.md). [Licencia Apache 2.0 leída](https://github.com/pbakaus/impeccable/blob/main/LICENSE).

El README ofrece revisión de interfaces y soporte para Codex. Puede servir para una landing o pantalla concreta; no resuelve la orquestación de la empresa.

El README documenta que Apply en modo live puede recurrir al CLI con aprobaciones y sandbox desactivados si no hay una sesión de chat atendiendo. Describe opciones para limitarlo al chat o desactivar Apply. Por eso no se recomienda ese modo para esta base. Evaluar primero instrucciones de revisión visual, sin hooks ni ejecución automática. Compatibilidad declarada no equivale a funcionamiento probado en el VPS. Antes de redistribuir una adaptación, revisar avisos y atribución aplicables.

## Inventario de los 30 nombres

Las categorías proceden de la descripción. «Pendiente» significa que falta identificar y auditar suficientemente el repositorio exacto; no es un juicio de calidad. Un nombre no demuestra compatibilidad con Codex.

| N.º | Nombre | Grupo | Estado |
|---|---|---|---|
| 1 | Superpowers | Código | Posponer paquete; README y licencia revisados. |
| 2 | Matt Pocock Skills | Código | Adaptar especificaciones; muestra revisada. |
| 3 | ECC | Código | Pendiente. |
| 4 | Karpathy Skills | Código | Pendiente. |
| 5 | Ponytail | Código | Pendiente. |
| 6 | Agent Skills | Código | Pendiente; nombre poco específico. |
| 7 | Graphify | Investigación | Pendiente. |
| 8 | Agent Reach | Investigación | Pendiente. |
| 9 | UnderstandAnything | Investigación | Pendiente; nombre visto también en la imagen. |
| 10 | Last30Days | Investigación | Se vio mvanhorn/last30days-skill en la imagen; lectura pendiente. |
| 11 | CareerOps | Investigación | Pendiente. |
| 12 | REA | Investigación | Pendiente. |
| 13 | gstack | Proyectos y tokens | Pendiente. |
| 14 | Caveman | Proyectos y tokens | Pendiente. |
| 15 | Claude-Mem | Proyectos y tokens | Pendiente. |
| 16 | Headroom | Proyectos y tokens | Pendiente. |
| 17 | GSD | Proyectos y tokens | Pendiente. |
| 18 | BMAD Method | Proyectos y tokens | Pendiente. |
| 19 | UI UX Pro Max | Diseño | Pendiente. |
| 20 | Taste | Diseño | Pendiente. |
| 21 | Archify | Diseño | Pendiente. |
| 22 | Impeccable | Diseño | Adaptar revisión; README y licencia revisados. |
| 23 | PPT Master | Diseño | Pendiente. |
| 24 | Diagram Design | Diseño | Pendiente. |
| 25 | Skills by Anthropic | Escritura y video | Pendiente de identificar skills/versiones concretas. |
| 26 | OpenMontage | Escritura y video | Pendiente. |
| 27 | HyperFrames | Escritura y video | Pendiente. |
| 28 | Humanizer | Escritura y video | Pendiente. |
| 29 | I Have ADHD | Escritura y video | Pendiente. |
| 30 | Marketing Skills | Escritura y video | Adaptar contexto y ofertas; muestra revisada. |

## Encaje en la arquitectura

La selección aporta procedimientos: contexto comercial, oferta, especificación y revisión de interfaz. No establece por sí misma memoria entre plataformas, ejecución permanente, calendario, acceso al VPS o cobros QR. Esas funciones requieren integraciones y verificación por separado.

Para analizar modelos y contexto, registrar: modelo y producto exactos, ventana documentada, límite de salida, cuota contratada, compacción/recuperación y costo de ejecución. No atribuir a una skill una ampliación de la ventana del modelo ni asumir API ilimitada por tener acceso al CLI. No se verificaron las promesas de ahorro del grupo de tokens.

Recomendación: empezar por una oferta concreta y una tarea técnica pequeña, medir resultados y añadir capacidades ante necesidades comprobables. Seleccionar herramientas no constituye ventas ni garantiza ingresos.

El reel y los 30 nombres ya están registrados. En la revisión posterior se identificó el repositorio vigente de ONIA y se encontró Impeccable ya versionado entre sus 16 skills de `.agents/skills`; corresponde evaluar esa copia antes de instalar otra. Ver [diagnóstico del producto](revision-onia-platform.md). La auditoría de los otros 26 candidatos, el análisis numérico de modelos y la verificación del VPS siguen pendientes.

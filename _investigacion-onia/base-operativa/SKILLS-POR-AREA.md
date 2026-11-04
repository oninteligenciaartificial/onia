# Skills por área de ONIA

3 de noviembre de 2026. Este mapa usa la [auditoría de los 30 repositorios](auditoria-30-repos.md) y su [registro con revisiones y licencias](catalogo-repos-2026-11-03.json). No es una nueva auditoría íntegra ni instala esos paquetes. Las [reglas comunes](reglas-comunes.md) siguen siendo la fuente de decisiones; [orquestacion.json](orquestacion.json) es el registro ejecutable de rutas y [ESTADO.md](ESTADO.md) conserva las pruebas del entorno.

## Qué usamos para cada encargo

Las siete skills previas siguen siendo la base. Se agregan dos fuentes propias acotadas: `planificar-dia` y `preparar-campana-meta`. Su presencia en archivos debe distinguirse de enlaces, carga por un agente y uso con cuentas reales.

| Área | Skill que dirige según el resultado pedido | Referencias útiles y límites |
|---|---|---|
| Marketing y ventas | `preparar-oferta-y-embudo` para oferta, funnel y taller; `preparar-campana-meta` para borrador de anuncios | Marketing Skills: offers/product-marketing/events, ads/ad-creative/analytics según encargo. Humanizer como revisión editorial; sin otro director comercial. |
| Video | `producir-video` | HyperFrames es el motor elegido. No instalar OpenMontage como segunda metodología. La pieza real necesita grabación, guion, formato y revisión audiovisual. |
| Desarrollo del harness | `desarrollar-y-verificar` | Matt Pocock para implementación/revisión; diagnóstico y evidencia de Superpowers como referencia. No instalar ambos recorridos completos. |
| Automatizaciones | `automatizar-n8n` | Patrones selectivos de n8n-skills, complemento fuera de los 30. La API de lectura ya probada no acredita escritura ni activación de flujos. |
| Organización | `planificar-dia` para agenda; `continuidad-de-trabajo` para retomar; `mejorar-sistema` para corregir procedimientos; `evaluar-catalogo-skills` para elegir herramientas | Se elige una según el encargo. Addy/ECC/I Have ADHD aportan contexto breve, evidencia y próxima acción; no se adopta un diagnóstico ni un modo global. |
| ONIA Platform | `desarrollar-y-verificar`, después de leer el repo del producto y sus instrucciones | Impeccable para futura revisión visual, cotejando la copia existente. El harness sólo prepara el briefing hasta verificar ese contexto. |

Las fuentes editables están en [compartibles/skills](compartibles/skills/). Una referencia no se convierte en otra skill instalada: se consulta sólo cuando cambia una decisión de la tarea.

## Decisión sobre los treinta candidatos

**Adopta** significa seleccionar el motor o adaptar criterios dentro de las skills propias, no importar el paquete completo. **Referencia** aporta una idea puntual. **Diferido** no se incorpora ahora; incluye los ajenos a esta etapa. Versiones, procedencia y licencias detalladas permanecen en el catálogo enlazado.

| # | Candidato | Decisión | Uso concreto o motivo |
|---|---|---|---|
| 1 | Superpowers | Referencia | Diagnóstico, evidencia, briefs y revisión; sin bootstrap universal. |
| 2 | Matt Pocock Skills | Adopta selectivamente | Desarrollo acotado, dependencias y revisión; skill propia. |
| 3 | ECC | Referencia | Mejoras trazables; sin hooks o memoria automáticos. |
| 4 | Karpathy Skills | Referencia | Supuestos explícitos y cambios pequeños. |
| 5 | Ponytail | Referencia | Reutilizar código y limitar complejidad. |
| 6 | Agent Skills / Addy Osmani | Referencia | Contexto pertinente y continuidad; correspondencia del reel provisional. |
| 7 | Graphify | Diferido | Mapa del código cuando un encargo lo justifique. |
| 8 | Agent Reach | Diferido | Acceso a plataformas todavía no necesario para la tarea actual. |
| 9 | Understand Anything | Diferido | Evitar otra capa de análisis y visualización ahora. |
| 10 | Last30Days | Adopta bajo demanda | Investigación con pregunta y fuentes concretas; integración pendiente. |
| 11 | CareerOps | Diferido | Búsqueda de empleo fuera del objetivo actual. |
| 12 | REA | Diferido | Ingeniería inversa fuera de alcance. |
| 13 | gstack | Diferido | Duplica la coordinación de desarrollo. |
| 14 | Caveman | Diferido | No adoptar un modo global de escritura. |
| 15 | Claude-Mem | Diferido | Primero comprobar continuidad explícita existente. |
| 16 | Headroom | Diferido | No añadir proxy ni reescritura automática de reglas. |
| 17 | GSD | Diferido | No añadir un segundo framework por fases. |
| 18 | BMAD Method | Diferido | No añadir otra metodología completa. |
| 19 | UI UX Pro Max | Referencia | Patrones UI puntuales; sin duplicar dirección visual. |
| 20 | Taste | Referencia | Composición subordinada a la marca del encargo. |
| 21 | Archify | Diferido | Herramienta extra sin una entrega que la requiera. |
| 22 | Impeccable | Adopta en encargo UI | Revisar primero lo existente en ONIA Platform; adaptación pendiente. |
| 23 | PPT Master | Diferido | Usar herramientas de presentación disponibles cuando haya taller. |
| 24 | Diagram Design | Referencia | Legibilidad y marca de diagramas. |
| 25 | Skills by Anthropic | Referencia | Patrones; licencias por módulo, sin redistribución general. |
| 26 | OpenMontage | Diferido | Segunda dirección de video y licencia AGPL; motor actual HyperFrames. |
| 27 | HyperFrames | Adopta | Motor para `producir-video`, con nuestra guía y versión comprobada. |
| 28 | Humanizer | Adopta selectivamente | Revisar guiones con voz y hechos reales; módulo propio pendiente. |
| 29 | I Have ADHD | Referencia | Próxima acción y organización, sin atribuir un diagnóstico. |
| 30 | Marketing Skills | Adopta selectivamente | Oferta, webinar, copy, anuncios y medición por encargo. |

Esta selección conserva las decisiones del catálogo. Copiar material de terceros requeriría conservar los avisos aplicables; elegir una referencia no autoriza empaquetarla como propia.

## Huecos que sí faltan

- **Organización:** Calendar ya respondió al perfil y al listado de tres calendarios desde la nueva sesión cloud; Gmail respondió al perfil, sin leer correos. Faltan disponibilidad/eventos del día concreto y registro de caja. La planificación no sincroniza eventos por escribir un archivo.
- **Meta:** la app existente ONIA Marketing API está inspeccionada; falta que Sergio ingrese `META_ADS_ACCESS_TOKEN` con `ads_read` en Secretos de red de `onia`, dominio `graph.facebook.com`, y comprobar la lectura. La skill puede preparar el borrador mientras faltan conexión, activos verificados, piezas y medición; no se declara Meta conectado.
- **Contenido:** `preparar-contenido` sigue pendiente. Higgsfield ya tiene perfil/workspace válidos comprobados, sin generar; Drive volvió a listar las cuatro carpetas de ONIA. Cuota y custodia quedan en [accesos.md](accesos.md). Faltan una muestra de voz, oferta y medios reales para probar guion → planos → CTA → edición y recuperar el entregable desde otra tarea. `producir-video` no inventa esa estrategia ni vivencias.
- **Taller y producto:** la oferta ya puede definir temario y recorrido; una skill específica de taller se justificará con el primer caso. La revisión UI necesita el producto real, no otra instalación del catálogo.

## Comprobación de las dos incorporaciones

Ambas pasaron `quick_validate.py`. Un agente independiente aplicó las instrucciones a cuatro casos sintéticos: agenda con 270 minutos de tareas y 180 disponibles; retraso con trabajo parcial; campaña sin presupuesto asignado ni conexión; y pedido posterior de publicación. Priorizó una agenda realizable, conservó el descanso, dejó presupuesto/acceso pendientes y distinguió autorización de publicación efectiva.

La prueba detectó una ambigüedad útil: tiempo trabajado no equivale a resultado terminado. Se explicitó esa distinción en planificación. También se aclaró que un pedido posterior de lanzamiento se reenruta conservando la autorización, en lugar de usar el alcance de preparación como rechazo absoluto. Son comprobaciones textuales, no ejecuciones de calendario, API o campañas; los casos con cuentas reales siguen pendientes.

# Revisión de los 30 repositorios y selección para ONIA

## Integración por áreas ·6/11/2026 ·integración estructural terminada

Pedido vigente de Sergio: incorporar fuentes útiles por sección y probar si mejoran resultados. Organización mantiene el [mapa de carga](../00-MAPA/SKILLS-POR-AREA.md), la tabla30de abajo y los [campos de integración fechados](catalogo-repos-2026-11-03.json); no repite auditoría ni instala fuentes. Desarrollo/Marketing/Video entregan módulos versionables bajo `compartibles/terceros`; Jefa confirma selección. Aprendizaje prepara8pares (7áreas+general) con fixtures/rúbrica previos y juez ciego. Jefa confirmó9apoyos copiados:6generales,Humanizer y2visuales. Son módulos, no9repositorios. Integración6paquetes/9apoyos terminada. Los8juicios, informe/auditoría y decisión de Jefa están terminados; ninguna mejora alcanzó umbral. UIUX sólo Producto, HyperFrames-plan Video; General/Aprendizaje usan apoyos por rol. Fuentes nativas de app no demostradas; rutasrepo/--apoyo sí documentados. No confundir existencia/23tests estructurales del harness con mejora. Investigación archivada localmente, descubrimiento nativo, carga y mejora comprobada son estados distintos. No staging/commit/push autorizados por esta unidad.

## Actualización local · 6 de noviembre de 2026

Sergio pidió descargar los 30 repositorios del catálogo y elegir una skill para mejorar el análisis. Las decisiones de selección anteriores son un corte histórico: «posponer» no bloquea esta descarga autorizada ni describe su estado actual. **Descarga y extracción 30/30 terminadas** en `operacion/catalogo-30-skills`, más el destino oficial documentado de GSD: 31 ZIP, 696.451.168 bytes comprimidos, integridad CRC comprobada por Desarrollo y SHA-256/tamaño cotejados independientemente por Jefa. [Índice local](operacion/catalogo-30-skills/INDICE.md) y [manifiesto](operacion/catalogo-30-skills/manifiesto.json) recuperan fuentes, revisiones y rutas; estos artefactos ignorados no se publicaron ni viajan con Git. La asociación de Agent Skills con Addy Osmani sigue siendo provisional. No se ejecutaron las herramientas descargadas.

Se eligió [Research de Matt Pocock](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/research/SKILL.md), revisión `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`: exige fuentes primarias y hallazgos citados en el registro existente. Fue instalada en `C:/Users/PC/.codex/skills/mattpocock-research`, con `SKILL.md`, `agents/openai.yaml` y [licencia MIT original](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/LICENSE). Root comprobó que el blob de `SKILL.md`, normalizado a LF, coincide con la fuente: `ffc9eb89849cc4cf74962ce93d786ffd17c6a5dc`. El catálogo nativo de esta sesión ya anuncia Research y su archivo local fue leído; resta comprobar descubrimiento en una sesión nueva.

Requiere un agente de investigación disponible; no declara credenciales, gasto, hooks ni otro coordinador. Instalar instrucciones no acredita percepción audiovisual ni calidad de sus resultados. Este cambio es local; no acredita publicación privada autorizada.

### Selección general propuesta · 6/11

Todos están descargados; sólo Research está instalada por este encargo. Lo siguiente propone usos: no acredita adopción aceptada por Sergio ni nuevas instalaciones.

- **[Matt Pocock](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/README.md#L19), base por módulos:** Research para fuentes primarias; `writing-for-agents` para contexto pertinente y cierres comprobables; `handoff` para continuidad sin duplicar artefactos, adaptando su destino temporal al registro existente. No imponer issues/TDD a toda tarea.
- **[Superpowers](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/README.md#L308), apoyo puntual:** diagnóstico/verificación; su metodología obligatoria de desarrollo no dirige todos los encargos.
- **Addy, apoyo:** `context-engineering` para recortar contexto; identidad del reel provisional.
- **[Ponytail](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md#L15), revisión de simplicidad en código:** sin activación persistente ni hooks. **[Karpathy](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md#L9), referencia breve:** solapa simplicidad y verificación; no añade coordinación.
- **ECC:** conservar lecciones con evidencia; posponer observador: Windows nativo no soportado según `continuous-learning-v2`, líneas 243–246.
- **GSD:** alternativa real para proyectos software por fases; posponer adopción hasta evaluar instalador Codex. **gstack:** QA ante encargo software, no base para referentes. **BMAD:** posponer instalación general del snapshot V7 alpha.
- **Claude-Mem y Headroom:** posponer servicios/análisis de memoria por requisitos adicionales; no afirmar que `learn` de Headroom exige proxy continuo.
- **Caveman:** sin activación general; concisión preservando números y negaciones. **I Have ADHD:** sólo claridad de próxima acción, sin diagnóstico.

Selección documental, sin prueba comparativa de rendimiento.

> Informe de la fase de selección. La implementación local posterior y sus pruebas se consultan en [ESTADO.md](../00-MAPA/ESTADO.md); las declaraciones de no instalación de este informe corresponden al momento de la revisión documental.

Fecha: 3 de noviembre de 2026. Responsable de la decisión final: Sergio. Esta revisión sustituye la cobertura parcial del catálogo anterior. ONIA-CENTRAL no se consultó ni se utilizó para esta selección.

## Resultado

Seleccionar capacidades concretas de Matt Pocock, HyperFrames, Marketing Skills, Humanizer e Impeccable. Last30Days queda como investigación bajo demanda. Como complemento fuera del reel, adaptar n8n-skills a la instalación existente. Las reglas comunes, la prioridad comercial y la coordinación siguen siendo propias y provienen de las instrucciones de Sergio.

«Adaptar» significa candidato seleccionado para una implementación delimitada, no instalado, probado o listo en producción. «Referencia» significa conservar un patrón útil sin activar el paquete. «Posponer» significa que hoy no compensa agregar su operación; no es una evaluación de mala calidad.

## Cobertura y límites

Se identificaron 30 correspondencias públicas para los 30 nombres de la descripción del reel, se consultaron metadatos y árboles de archivos y se hizo lectura dirigida de README, instrucciones de entrada y secciones de requisitos/licencias. Para los candidatos elegidos se ampliaron referencias de comportamiento y costos. No se leyó cada línea de cada repositorio ni se ejecutó software de los candidatos. Es una evaluación documental de adopción, no una auditoría integral de seguridad ni una prueba comparativa de rendimiento.

El reel no aportó enlaces directos para cada nombre en la descripción observada. **Agent Skills** se evaluó como **addyosmani/agent-skills**; esa correspondencia permanece provisional. No se afirma que sea vercel-labs/agent-skills. Las demás correspondencias se identificaron por título y proyecto; las redirecciones comprobadas se indican abajo. No se obtuvo una transcripción completa ni se verificó todo el video: esta entrega evalúa los repositorios, no reproduce afirmaciones del audio.

Los números de ahorro, tokens y conversiones publicados por los autores no se trataron como resultados medidos en ONIA. Licencia del código, acceso a una API y costo de ejecutar un modelo son asuntos separados.

El [registro estructurado](catalogo-repos-2026-11-03.json) conserva URL, revisión consultada, entrada y decisión. Los enlaces de archivo siguientes fijan la revisión examinada.

**Cobertura fijada antes de resultados:**9apoyos disponibles/integrados estructuralmente frente a8comparaciones conductuales predefinidas:Mattwriting,Superdebug,Superverify,Matthandoff,Mattresearch,Humanizer,HyperFrames-plan yUIUX. Addycontext queda disponible para uso acotado **sin comparación propia**; no atribuirle mejora ni afirmar «9skills probadas». Los8pares cubren7áreas+general, no todo el potencial del catálogo. Conservar negativos y empates; no añadir ensayo después de ver resultados para aumentar cobertura.

**Cierre aceptado por Jefa:** integración6paquetes/9apoyos disponible; piloto8casos/16brazos terminado, ninguna mejora alcanzó el umbral previo. Los ocho ensayados se limitan al encargo pertinente, sin requisito general/carga automática; no significa inutilidad. Addy sin comparación propia. [Tabla única de resultados e informe](2026-11-06/prueba-skills/caso-general/INFORME-COMPARATIVO.md) conserva puntajes/umbrales, recibos y auditoría, sin duplicar raw aquí. Techo basal18–20, una pareja/caso y sin tokens/latencia comparables. Marketing tuvo cegamiento parcial por Humanizer/protocoloA/B en rúbrica:−1 no demuestra daño causal. Organización: juez sin rutas que generadores conocían; límite conservado, sin recalificar ni repetir.

**Trazabilidad exploratoria limitada:**los16mensajes exactos de brazos y8de jueces no se exportaron antes;24prompts desconocidos, sin texto recuperable en rollout/API según cotejo de Jefa. No puede auditarse igualdad literal de encargos, ni afirmar diferencias verificadas de instrucciones. Sí se cotejaron fixtures/configuración declarada, recibos/hashes yraw; esto no reemplaza los prompts. Puntajes intactos, ninguna mejora sobre umbral y ningún requisito general justificado. [Informe](2026-11-06/prueba-skills/caso-general/INFORME-COMPARATIVO.md).

## Decisión por candidato

**Corte vigente de organización,6/11:**30/30con área principal y apoyos. Selección actual y diferidos específicos; rutas confirmadas de9módulos en mapa/JSON, uso/pilotos todavía pendientes. Revisión original y decisiones del3/11 se conservan en cada ficha posterior y campos originales del JSON; no son el estado de integración actual. Ésta es la única tabla30de decisiones; [mapa por sección](../00-MAPA/SKILLS-POR-AREA.md) no duplica el catálogo.

| # | Candidato/fuente | Área principal | Apoyos | Decisión actual del corte | Motivo / condición específica |
|---|---|---|---|---|---|
| 1 | [Superpowers](https://github.com/obra/superpowers) | desarrollo | producto, automatizaciones, general | Disponible; comparación sin umbral de mejora, uso acotado | Diagnóstico y verificación puntuales; no importar bootstrap/TDD obligatorio para todo encargo. Módulos integrados estructuralmente; comparación terminada sin alcanzar umbral; limitar al encargo pertinente, sin carga automática. |
| 2 | [Matt Pocock Skills](https://github.com/mattpocock/skills) | general | desarrollo, organizacion, aprendizaje | Disponible; comparación sin umbral de mejora, uso acotado | Research, escritura para agentes y handoff: fuentes primarias/contexto/cierre; adaptar destino al registro existente, no duplicar coordinación. Módulos integrados estructuralmente; comparación terminada sin alcanzar umbral; limitar al encargo pertinente, sin carga automática. |
| 3 | [ECC](https://github.com/affaan-m/ECC) | aprendizaje | general, desarrollo | referencia; observador diferido | Aprendizaje con evidencia por proyecto; observador continuous-learning-v2 no soporta Windows nativo según revisión local. |
| 4 | [Karpathy Skills](https://github.com/multica-ai/andrej-karpathy-skills) | desarrollo | producto, automatizaciones | referencia breve propuesta | Supuestos/cambios pequeños; solapa guía propia, no requiere activar otro director. |
| 5 | [Ponytail](https://github.com/DietrichGebert/ponytail) | desarrollo | producto | referencia breve propuesta | Reutilización/simplicidad para revisión de código; sin modo persistente ni hooks. |
| 6 | [Agent Skills (Addy Osmani)](https://github.com/addyosmani/agent-skills) | general | organizacion, aprendizaje | Disponible; limitar al encargo pertinente (Addy sin comparación propia) | Context-engineering para contexto pertinente; correspondencia Addy con el reel sigue provisional. Módulos integrados estructuralmente; comparación terminada sin alcanzar umbral; limitar al encargo pertinente, sin carga automática. |
| 7 | [Graphify](https://github.com/Graphify-Labs/graphify) | desarrollo | producto | diferido | Grafo de dependencias sólo si navegar el código bloquea una tarea; evitar análisis/modelo completo sin necesidad. |
| 8 | [Agent Reach](https://github.com/Panniantong/Agent-Reach) | aprendizaje | marketing | diferido | Acceso adicional por canal sólo ante fuente no cubierta por conectores; sesiones/dependencias no son necesarias por defecto. |
| 9 | [Understand Anything](https://github.com/Egonex-AI/Understand-Anything) | producto | desarrollo | diferido | Mapa visual del producto exige análisis inicial y hooks; no duplicar Graphify sin una pregunta de arquitectura. |
| 10 | [Last30Days](https://github.com/mvanhorn/last30days-skill) | marketing | aprendizaje | bajo demanda propuesto | Tendencias/problemas recientes con pregunta/fechas/fuentes; acceso/cookies/API variables y popularidad no es demanda. |
| 11 | [CareerOps](https://github.com/career-ops-hq/career-ops) | organizacion | — | fuera del frente actual | CareerOps se orienta a empleo/CV/entrevistas; no existe encargo de empleo, no convertirlo en CRM. |
| 12 | [REA](https://github.com/morluto/rea) | desarrollo | — | fuera del frente actual | REA resuelve ingeniería inversa de binarios; ONIA tiene fuentes y no hay demanda de reversing acreditada. |
| 13 | [gstack](https://github.com/garrytan/gstack) | producto | desarrollo | diferido | QA de software ante defecto concreto; suite de roles no sustituye reparto actual ni investiga referentes. |
| 14 | [Caveman](https://github.com/JuliusBrussee/caveman) | general | organizacion | diferido como modo global | Concisión puede perder números/negaciones; no imponer estilo Caveman a toda explicación. |
| 15 | [Claude-Mem](https://github.com/thedotmack/claude-mem) | organizacion | general | diferido | Memoria/servicios de sesión agregan operación; primero probar continuidad explícita y recuperación existentes. |
| 16 | [Headroom](https://github.com/headroomlabs-ai/headroom) | general | desarrollo | diferido | Proxy/MCP/compresión añaden infraestructura; learn no equivale necesariamente a proxy continuo, elegir sólo tarea real. |
| 17 | [GSD](https://github.com/gsd-build/get-shit-done) | desarrollo | producto | diferido | Framework por fases y destino oficial descargado aparte; revisar instalador Codex antes de adoptar segunda coordinación. |
| 18 | [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) | producto | desarrollo | diferido | BMAD V7alpha añade metodología amplia; no instalar framework completo para una mejora acotada. |
| 19 | [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | producto | video | Disponible; comparación sin umbral de mejora, uso acotado | UIUX wrapper de revisión estática sólo asignado a Producto en runtime;47archivosMIT/PROVENANCE/hash, no implementación automática. |
| 20 | [Taste](https://github.com/Leonxlnx/taste-skill) | producto | video | diferido para operación de este caso | Taste:apoyo puntual diferido por proceso y solapamiento; no imposibilidad técnica. |
| 21 | [Archify](https://github.com/tt-a1i/archify) | video | producto, aprendizaje | diferido para operación de este caso | ArchifyCLI/diagramas fuera del caso de estos pilotos; reconsiderar con entrega de diagramas concreta. |
| 22 | [Impeccable](https://github.com/pbakaus/impeccable) | producto | video | diferido para operación de este caso | Impeccable:apoyo puntual diferido por proceso y solapamiento; no imposibilidad ni falta de licencia inferida. |
| 23 | [PPT Master](https://github.com/hugohe3/ppt-master) | video | marketing, aprendizaje | diferido para operación de este caso | PPTMaster diferido hasta encargoPPTXreal que lo justifique. |
| 24 | [Diagram Design](https://github.com/cathrynlavery/diagram-design) | video | producto, aprendizaje | diferido para operación de este caso | DiagramDesign queda soporte de diagramas, sin operación en este caso. |
| 25 | [Skills by Anthropic](https://github.com/anthropics/skills) | general | organizacion, video | módulos revisados no seleccionados; doc-coauthoring diferido | frontend/theme/canvas tienenApache2 observado, pero no se seleccionaron. Doc-coauthoring conserva licencia exacta sin verificar y flujo interactivo innecesario; no heredar su licencia de esos otros módulos. |
| 26 | [OpenMontage](https://github.com/calesthio/OpenMontage) | video | desarrollo | diferido para operación de este caso | OpenMontage requiere clave/cupoHeyGen y duplica motor elegido; paquete diferido. |
| 27 | [HyperFrames](https://github.com/heygen-com/hyperframes) | video | marketing | Disponible; comparación sin umbral de mejora, uso acotado | Sólo planificación mediante wrapper USO-ONIA→original/ref;24archivosApache2 conPROVENANCE/hash; no render/modelo/servicio por seleccionarlo. |
| 28 | [Humanizer](https://github.com/blader/humanizer) | marketing | video, organizacion | Disponible; comparación sin umbral de mejora, uso acotado | Humanizer revisa texto con voz y hechos reales suministrados; no conoce biografía ni debe inventar resultados. Módulos integrados estructuralmente; comparación terminada sin alcanzar umbral; limitar al encargo pertinente, sin carga automática. |
| 29 | [I Have ADHD](https://github.com/ayghri/i-have-adhd) | organizacion | aprendizaje | referencia acotada propuesta | Próxima acción y continuidad sin diagnóstico TDAH ni modo obligatorio; conservar compromisos reales en privado. |
| 30 | [Marketing Skills](https://github.com/coreyhaines31/marketingskills) | marketing | video | copywriting/offers pospuestos para este piloto | Encaje/carga y proyección de ofertas sin datos disponibles. Citas o atribuciones no prueban incompatibilidad de licencia; no usar ese argumento como causa de exclusión. |

## Evidencia y condiciones por repositorio

### 1. Superpowers — Referencia

Diagnóstico de bugs y comprobación de resultados. Su bootstrap se activa ante cualquier conversación y obliga a su proceso; compite con nuestra dirección de trabajo.

**Aplicación a ONIA:** Extraer criterios de diagnóstico/verificación; no instalar el bootstrap ni imponer TDD a toda edición.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/README.md), [instrucciones de entrada](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/skills/using-superpowers/SKILL.md), [LICENSE](https://github.com/obra/superpowers/blob/22f0b463e7a5e579904dd6211a520321035526f7/LICENSE). Revisión: `22f0b463e7a5e579904dd6211a520321035526f7`.

### 2. Matt Pocock Skills — Adaptar ahora

Proceso propio de desarrollo: encargo acotado → implementación → verificación → revisión. Implement invoca TDD/code-review y termina pidiendo commit en la rama actual; to-spec supone issue tracker.

**Aplicación a ONIA:** Usar especificaciones locales breves, pruebas proporcionales y una rama de trabajo; no crear issues o commits por regla universal.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/README.md), [instrucciones de entrada](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/implement/SKILL.md), [LICENSE](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/LICENSE). Revisión: `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`.

### 3. ECC — Referencia

Aprendizaje por proyecto, evidencias y separación de patrones locales/globales. Es un harness amplio con agentes, hooks y memoria; continuous-learning-v2 describe observación de sesiones, no sólo un archivo de instrucciones.

**Aplicación a ONIA:** Tomar el registro de evidencia y la separación de proyectos; no importar todo ECC ni promover reglas automáticamente.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/README.md), [instrucciones de entrada](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/skills/continuous-learning-v2/SKILL.md), [LICENSE](https://github.com/affaan-m/ECC/blob/b38be6a7f6350964d59328b52f0624e1d1d552d1/LICENSE). Revisión: `b38be6a7f6350964d59328b52f0624e1d1d552d1`.

### 4. Karpathy Skills — Referencia

Cambios pequeños, supuestos explícitos y criterio de éxito. Se solapa con Ponytail y el procedimiento de desarrollo; no es un repositorio oficial de Karpathy.

**Aplicación a ONIA:** Redactar nuestros principios sin una skill adicional siempre activa; MIT declarada en frontmatter, sin LICENSE raíz observado.

**Licencia observada:** MIT declarada; falta archivo de licencia raíz. **Lectura:** [README](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/README.md), [instrucciones de entrada](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/skills/karpathy-guidelines/SKILL.md). Revisión: `2c606141936f1eeef17fa3043a72095b4765b9c2`.

### 5. Ponytail — Referencia

Reutilizar lo existente y reducir código innecesario sin quitar validación. Modo persistente de sesión y hooks; duplica nuestras reglas de alcance y concisión.

**Aplicación a ONIA:** Conservar el criterio de reutilización en desarrollo; no sumar otro modo global.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/README.md), [instrucciones de entrada](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/skills/ponytail/SKILL.md), [LICENSE](https://github.com/DietrichGebert/ponytail/blob/96608e078b2d5ea607c5c3b8b5a54d1c1fba6846/LICENSE). Revisión: `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`.

### 6. Agent Skills (Addy Osmani) — Referencia

Continuidad y selección del contexto pertinente. Suite de ingeniería que se solapa con Matt y Superpowers; context-engineering propone reglas de sesión amplias.

**Aplicación a ONIA:** Tomar entrega entre chats y lectura selectiva; mantener un solo procedimiento de desarrollo.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/addyosmani/agent-skills/blob/301b02b12bff98e4688e6984af6556802322bbde/README.md), [instrucciones de entrada](https://github.com/addyosmani/agent-skills/blob/301b02b12bff98e4688e6984af6556802322bbde/skills/context-engineering/SKILL.md), [LICENSE](https://github.com/addyosmani/agent-skills/blob/301b02b12bff98e4688e6984af6556802322bbde/LICENSE). Revisión: `301b02b12bff98e4688e6984af6556802322bbde`.

### 7. Graphify — Posponer

Mapa estructural local y consultas sobre dependencias de ONIA. Requiere Python/uv o pipx; análisis semántico de documentos consume modelo. Su skill es amplia y sugiere consultar el grafo primero.

**Aplicación a ONIA:** Evaluarlo si la navegación del código realmente bloquea una tarea; primero un módulo y medir utilidad/consumo.

**Licencia observada:** Apache-2.0; también LICENSE-MIT en árbol. **Lectura:** [README](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/README.md), [instrucciones de entrada](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/graphify/skill-codex.md), [LICENSE](https://github.com/Graphify-Labs/graphify/blob/59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0/LICENSE). Revisión: `59b5ab1151e031fb42e39cfc9a50bf96f2d57ae0`.

### 8. Agent Reach — Posponer

Lectura de plataformas que las herramientas disponibles no cubran. Python y herramientas por canal; algunas rutas usan sesiones de navegador. La plantilla limita operaciones a lectura.

**Aplicación a ONIA:** Primero conectores existentes; habilitar sólo un canal que falte y comprobar exactamente qué contenido obtiene.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/README.md), [instrucciones de entrada](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/agent_reach/skill/SKILL.md), [LICENSE](https://github.com/Panniantong/Agent-Reach/blob/7a38047acf26a729cbb27851e3cb81639da86b29/LICENSE). Revisión: `7a38047acf26a729cbb27851e3cb81639da86b29`.

### 9. Understand Anything — Posponer

Mapa visual del producto con explicaciones de componentes. Análisis inicial de todo el repositorio puede consumir muchos tokens; actualización automática agrega hooks.

**Aplicación a ONIA:** Elegirlo frente a Graphify sólo si hace falta explicación visual para Sergio; no instalar ambos de entrada.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/Egonex-AI/Understand-Anything/blob/4e6d3299017a7432da15957874992837a315c5b4/README.md), [instrucciones de entrada](https://github.com/Egonex-AI/Understand-Anything/blob/4e6d3299017a7432da15957874992837a315c5b4/understand-anything-plugin/skills/understand/SKILL.md), [LICENSE](https://github.com/Egonex-AI/Understand-Anything/blob/4e6d3299017a7432da15957874992837a315c5b4/LICENSE). Revisión: `4e6d3299017a7432da15957874992837a315c5b4`.

### 10. Last30Days — Adaptar bajo demanda

Investigar problemas, conversaciones y temas de contenido recientes. Python 3.12+ y disponibilidad variable de fuentes; algunas necesitan cookies o API. Popularidad no demuestra demanda de compra.

**Aplicación a ONIA:** Fuentes gratuitas disponibles, fechas y enlaces; sin claves nuevas por defecto. Validar con conversaciones reales con compradores.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/mvanhorn/last30days-skill/blob/e9c31b868ab9d284c1a988e528c3391c51ebf944/README.md), [instrucciones de entrada](https://github.com/mvanhorn/last30days-skill/blob/e9c31b868ab9d284c1a988e528c3391c51ebf944/skills/last30days/SKILL.md), [LICENSE](https://github.com/mvanhorn/last30days-skill/blob/e9c31b868ab9d284c1a988e528c3391c51ebf944/LICENSE). Revisión: `e9c31b868ab9d284c1a988e528c3391c51ebf944`.

### 11. CareerOps — Fuera de esta etapa

Evaluación de empleos, CV, postulaciones e entrevistas. Su problema central es búsqueda de empleo, diferente de vender el taller o desarrollar ONIA.

**Aplicación a ONIA:** Reconsiderar únicamente si aparece un objetivo explícito de empleo; no convertirlo en CRM comercial.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/career-ops-hq/career-ops/blob/7d8feb6d5fcf9f225eb2dd8839ae4b131b703bf3/README.md), [instrucciones de entrada](https://github.com/career-ops-hq/career-ops/blob/7d8feb6d5fcf9f225eb2dd8839ae4b131b703bf3/.agents/skills/career-ops/SKILL.md), [LICENSE](https://github.com/career-ops-hq/career-ops/blob/7d8feb6d5fcf9f225eb2dd8839ae4b131b703bf3/LICENSE). Revisión: `7d8feb6d5fcf9f225eb2dd8839ae4b131b703bf3`.

### 12. REA — Fuera de esta etapa

Ingeniería inversa de binarios, aplicaciones y ejecución. La propia skill excluye análisis ordinario de arquitectura con código fuente; motores adicionales según objetivo.

**Aplicación a ONIA:** ONIA ya tiene su código: inspeccionar ese repositorio directamente.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/morluto/rea/blob/c3647ade1e557c4179a8b825a37e0c2193cd2526/README.md), [instrucciones de entrada](https://github.com/morluto/rea/blob/c3647ade1e557c4179a8b825a37e0c2193cd2526/.agents/skills/reverse-engineer-anything/SKILL.md), [LICENSE](https://github.com/morluto/rea/blob/c3647ade1e557c4179a8b825a37e0c2193cd2526/LICENSE). Revisión: `c3647ade1e557c4179a8b825a37e0c2193cd2526`.

### 13. gstack — Posponer

Suite de roles de producto, revisión, QA y entrega. Codex figura experimental en su matriz; herramientas Bun/browser y proceso propio. Compite con el proceso elegido.

**Aplicación a ONIA:** Conservar referencias de QA, sin otra orquestación completa ni cambiar nuestra herramienta de navegación.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/garrytan/gstack/blob/e9b40bbd82aa7e53e973f2790aa485a0d4debd3b/README.md), [instrucciones de entrada](https://github.com/garrytan/gstack/blob/e9b40bbd82aa7e53e973f2790aa485a0d4debd3b/SKILL.md), [LICENSE](https://github.com/garrytan/gstack/blob/e9b40bbd82aa7e53e973f2790aa485a0d4debd3b/LICENSE). Revisión: `e9b40bbd82aa7e53e973f2790aa485a0d4debd3b`.

### 14. Caveman — Fuera de esta etapa

Estilo de respuesta y reducción de contexto mediante otros componentes. Modo persistente; menos texto no equivale automáticamente a más cuota disponible ni mejor explicación.

**Aplicación a ONIA:** Usar español claro y respuestas proporcionales; no incorporar su modo global.

**Licencia observada:** Apache-2.0; también LICENSE-MIT en árbol. **Lectura:** [README](https://github.com/JuliusBrussee/caveman/blob/2e068f735253cce28256744804785f01887d9646/README.md), [instrucciones de entrada](https://github.com/JuliusBrussee/caveman/blob/2e068f735253cce28256744804785f01887d9646/skills/caveman/SKILL.md), [LICENSE](https://github.com/JuliusBrussee/caveman/blob/2e068f735253cce28256744804785f01887d9646/LICENSE). Revisión: `2e068f735253cce28256744804785f01887d9646`.

### 15. Claude-Mem — Posponer

Memoria de sesiones y recuperación por búsqueda → contexto → detalles. Worker, almacenamiento e integración con proveedor/observador; planes y pruebas comerciales separados de la licencia del código.

**Aplicación a ONIA:** Primero memoria explícita en archivos por proyecto; medir después si hace falta observación automática.

**Licencia observada:** Apache-2.0. **Lectura:** [README](https://github.com/thedotmack/claude-mem/blob/02584c4ac9d92fea45adf5c61e22c546b5738621/README.md), [instrucciones de entrada](https://github.com/thedotmack/claude-mem/blob/02584c4ac9d92fea45adf5c61e22c546b5738621/plugin/skills/mem-search/SKILL.md), [LICENSE](https://github.com/thedotmack/claude-mem/blob/02584c4ac9d92fea45adf5c61e22c546b5738621/LICENSE). Revisión: `02584c4ac9d92fea45adf5c61e22c546b5738621`.

### 16. Headroom — Posponer

Compresión de contexto, proxy/MCP y aprendizaje de sesiones. Introduce una capa en el tráfico/contexto. learn puede analizar sesiones y escribir AGENTS.md; no garantiza ahorro en este plan.

**Aplicación a ONIA:** Antes de instalar, medir un problema real y comparar calidad; no permitir que reescriba reglas comunes por su cuenta.

**Licencia observada:** Apache-2.0. **Lectura:** [README](https://github.com/headroomlabs-ai/headroom/blob/038af599e1a3c5e7e6b3047781aaf9ba2bbbf8bd/README.md), [instrucciones de entrada](https://github.com/headroomlabs-ai/headroom/blob/038af599e1a3c5e7e6b3047781aaf9ba2bbbf8bd/wiki/learn.md), [LICENSE](https://github.com/headroomlabs-ai/headroom/blob/038af599e1a3c5e7e6b3047781aaf9ba2bbbf8bd/LICENSE). Revisión: `038af599e1a3c5e7e6b3047781aaf9ba2bbbf8bd`.

### 17. GSD — Posponer

Fases, estados persistentes y ejecución con contextos separados. El repo antiguo redirige a open-gsd/gsd-core; metodología e instalador propios. Su cifra de 200k no prueba el contexto del modelo aquí.

**Aplicación a ONIA:** Tomar entregas entre tareas como idea; no instalar un segundo framework ni asumir una ventana universal.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/README.md), [LICENSE](https://github.com/gsd-build/get-shit-done/blob/bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815/LICENSE). Revisión: `bdcaab2c752d9a33a1a1ca9acf3a3c81fb991815`.

### 18. BMAD Method — Posponer

Briefs, arquitectura, historias, implementación y revisión. Main es v7 preview alpha; stable v6.12 tiene otra instalación. El entrypoint ejecuta un renderer Python/uv de _bmad.

**Aplicación a ONIA:** No basar la urgencia de caja en una metodología adicional en transición.

**Licencia observada:** MIT; avisos de contribuciones en LICENSE. **Lectura:** [README](https://github.com/bmad-code-org/BMAD-METHOD/blob/022be9314e4facd16826104a9f8033e1c5ed4fdc/README.md), [instrucciones de entrada](https://github.com/bmad-code-org/BMAD-METHOD/blob/022be9314e4facd16826104a9f8033e1c5ed4fdc/skills/bmad-build/SKILL.md), [LICENSE](https://github.com/bmad-code-org/BMAD-METHOD/blob/022be9314e4facd16826104a9f8033e1c5ed4fdc/LICENSE). Revisión: `022be9314e4facd16826104a9f8033e1c5ed4fdc`.

### 19. UI UX Pro Max — Referencia

Biblioteca local de patrones UI, accesibilidad y estilos. Python para búsqueda; varias skills de diseño y versión premium. Duplica parte de Impeccable.

**Aplicación a ONIA:** Consultar un patrón concreto si falta; no cargar todo como segundo director visual.

**Licencia observada:** MIT (repositorio básico). **Lectura:** [README](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/713eef51b04efc98d6fa565323b495f7c9c89fd4/README.md), [instrucciones de entrada](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/713eef51b04efc98d6fa565323b495f7c9c89fd4/.claude/skills/ui-ux-pro-max/SKILL.md), [LICENSE](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/713eef51b04efc98d6fa565323b495f7c9c89fd4/LICENSE). Revisión: `713eef51b04efc98d6fa565323b495f7c9c89fd4`.

### 20. Taste — Referencia

Dirección visual y revisión de páginas mediante navegador. Node 22+ y navegador; estilo propio y amplio disparador para páginas y aplicaciones.

**Aplicación a ONIA:** Usar ejemplos de composición como inspiración, subordinados a la marca; Impeccable dirige la revisión UI.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/README.md), [instrucciones de entrada](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill/SKILL.md), [LICENSE](https://github.com/Leonxlnx/taste-skill/blob/12af471f627f866411b4bd785b19646d3672784c/LICENSE). Revisión: `12af471f627f866411b4bd785b19646d3672784c`.

### 21. Archify — Posponer

Diagramas de arquitectura y explicaciones HTML. Runtime/CLI y plantillas propios; puede adoptar modo always-on. Se solapa con Diagram Design y herramientas disponibles.

**Aplicación a ONIA:** Usarlo bajo pedido para un diagrama que lo necesite; nunca adjuntar una página a todas las respuestas.

**Licencia observada:** Apache-2.0; también LICENSE-MIT en árbol. **Lectura:** [README](https://github.com/tt-a1i/archify/blob/a4065941f12be7967436261d9934784e381d423c/README.md), [instrucciones de entrada](https://github.com/tt-a1i/archify/blob/a4065941f12be7967436261d9934784e381d423c/archify/SKILL.md), [LICENSE](https://github.com/tt-a1i/archify/blob/a4065941f12be7967436261d9934784e381d423c/LICENSE). Revisión: `a4065941f12be7967436261d9934784e381d423c`.

### 22. Impeccable — Adaptar ahora

Revisión visual de landing y producto: jerarquía, móvil, accesibilidad y estados. La versión actual incorpora binario/launcher y live mode. El producto ya contiene una versión; actualizar sin comparar duplicaría o alteraría reglas.

**Aplicación a ONIA:** Auditar lo instalado, una sola guía visual y revisión de pantallas; no activar live ni cambiar permisos por defecto.

**Licencia observada:** Apache-2.0. **Lectura:** [README](https://github.com/pbakaus/impeccable/blob/9fadc41729c38fd47d7ae622b501558653f9d2e9/README.md), [instrucciones de entrada](https://github.com/pbakaus/impeccable/blob/9fadc41729c38fd47d7ae622b501558653f9d2e9/.agents/skills/impeccable/SKILL.md), [LICENSE](https://github.com/pbakaus/impeccable/blob/9fadc41729c38fd47d7ae622b501558653f9d2e9/LICENSE). Revisión: `9fadc41729c38fd47d7ae622b501558653f9d2e9`.

### 23. PPT Master — Posponer

Presentaciones PPTX editables para talleres/webinars. Python y recursos por ruta; guard de atribución y flujos propios. Ya hay herramientas de presentaciones disponibles.

**Aplicación a ONIA:** Preparar primero el contenido del taller; usarlo sólo si el resultado requerido no lo cubre la herramienta existente.

**Licencia observada:** MIT; revisar avisos de iconos/activos. **Lectura:** [README](https://github.com/hugohe3/ppt-master/blob/4a68cddaf40dc87891e6b64c6a69ef46adc1110c/README.md), [instrucciones de entrada](https://github.com/hugohe3/ppt-master/blob/4a68cddaf40dc87891e6b64c6a69ef46adc1110c/skills/ppt-master/SKILL.md), [LICENSE](https://github.com/hugohe3/ppt-master/blob/4a68cddaf40dc87891e6b64c6a69ef46adc1110c/LICENSE). Revisión: `4a68cddaf40dc87891e6b64c6a69ef46adc1110c`.

### 24. Diagram Design — Referencia

Diagramas HTML/SVG con marca y exportación. Solapa con Archify; pide configurar estilo de marca antes del primer diagrama.

**Aplicación a ONIA:** Tomar criterios de legibilidad y marca; elegir un solo motor por entrega, no instalar ambos.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/cathrynlavery/diagram-design/blob/f24d98b05e2d7a5e68c2dedfe46e5b7173f50118/README.md), [instrucciones de entrada](https://github.com/cathrynlavery/diagram-design/blob/f24d98b05e2d7a5e68c2dedfe46e5b7173f50118/skills/diagram-design/SKILL.md), [LICENSE](https://github.com/cathrynlavery/diagram-design/blob/f24d98b05e2d7a5e68c2dedfe46e5b7173f50118/LICENSE). Revisión: `f24d98b05e2d7a5e68c2dedfe46e5b7173f50118`.

### 25. Skills by Anthropic — Referencia

Patrones de documentación, pruebas de lectura y skills específicas. Licencias por módulo: README distingue ejemplos abiertos de docx/pdf/pptx/xlsx source-available. La licencia PPTX leída restringe copia/adaptación/distribución.

**Aplicación a ONIA:** Aprovechar ideas generales y las herramientas documentales existentes; no empaquetar sus document-skills para clientes.

**Licencia observada:** Mixta; no existe licencia raíz única observada. **Lectura:** [README](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/README.md), [instrucciones de entrada](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/doc-coauthoring/SKILL.md). Revisión: `ca45fc496a3436251f191354091d557da31c15b5`.

### 26. OpenMontage — Posponer paquete completo

Producción de video con pipelines, herramientas locales y proveedores generativos. AGENT_GUIDE impone orquestación por etapas para todo video; duplica HyperFrames. Hay rutas con API pagada y video-edit local.

**Aplicación a ONIA:** Conservar como referencia del flujo de revisión de material; escribir nuestra edición local con documentación de FFmpeg, sin copiar el paquete.

**Licencia observada:** AGPL-3.0. **Lectura:** [README](https://github.com/calesthio/OpenMontage/blob/d21f5d4eaa08422b09c7091757a05affcbabb35b/README.md), [instrucciones de entrada](https://github.com/calesthio/OpenMontage/blob/d21f5d4eaa08422b09c7091757a05affcbabb35b/.agents/skills/create-video/SKILL.md), [LICENSE](https://github.com/calesthio/OpenMontage/blob/d21f5d4eaa08422b09c7091757a05affcbabb35b/LICENSE). Revisión: `d21f5d4eaa08422b09c7091757a05affcbabb35b`.

### 27. HyperFrames — Adaptar ahora

Motor elegido por Sergio para videos, overlays, subtítulos y piezas verticales. Node 22+, FFmpeg; skill de medios prioriza HeyGen y ordena ocultar costos; lifecycle propone actualizar automáticamente el pin.

**Aplicación a ONIA:** Motor sí. Guía ONIA: material propio/local, costos visibles, presupuesto explícito, versión fijada y revisión audiovisual antes de entregar.

**Licencia observada:** Apache-2.0. **Lectura:** [README](https://github.com/heygen-com/hyperframes/blob/3dc82f18e3f99350f9a0c0f1738bcee8d1e44741/README.md), [instrucciones de entrada](https://github.com/heygen-com/hyperframes/blob/3dc82f18e3f99350f9a0c0f1738bcee8d1e44741/skills/hyperframes/SKILL.md), [LICENSE](https://github.com/heygen-com/hyperframes/blob/3dc82f18e3f99350f9a0c0f1738bcee8d1e44741/LICENSE). Revisión: `3dc82f18e3f99350f9a0c0f1738bcee8d1e44741`.

### 28. Humanizer — Adaptar ahora

Editar guiones y textos para conservar la voz de Sergio y quitar relleno. No conoce por sí solo la voz de Sergio; se superpone con reglas generales de escritura.

**Aplicación a ONIA:** Usarlo sólo en revisión de copy/guiones, con ejemplos reales de voz y sin inventar vivencias, resultados o testimonios.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/blader/humanizer/blob/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0/README.md), [instrucciones de entrada](https://github.com/blader/humanizer/blob/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0/SKILL.md), [LICENSE](https://github.com/blader/humanizer/blob/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0/LICENSE). Revisión: `0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0`.

### 29. I Have ADHD — Referencia

Próxima acción clara y continuidad visible. El texto presupone TDAH y establece un modo persistente; Sergio no declaró ese diagnóstico.

**Aplicación a ONIA:** Tomar organización accionable sin atribuirle un diagnóstico ni obligar un formato en cada respuesta.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/README.md), [instrucciones de entrada](https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/skills/i-have-adhd/SKILL.md), [LICENSE](https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/LICENSE). Revisión: `1ecea1993b7fce257ffbd686c070948b5e07eda6`.

### 30. Marketing Skills — Adaptar ahora

Oferta, embudo, webinars, contenido, anuncios y medición. Colección amplia; algunas guías contienen supuestos de acceso a cuentas y benchmarks B2B que no son datos de Sergio.

**Aplicación a ONIA:** Seleccionar product-marketing, offers, events/webinar-funnel, copywriting, social/video, emails y ads/ad-creative/analytics según tarea; no cargar toda la colección.

**Licencia observada:** MIT. **Lectura:** [README](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/README.md), [instrucciones de entrada](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/events/SKILL.md), [LICENSE](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/LICENSE). Revisión: `88c79f6528a9347420e57ceb1fff9a60de651768`.

## Hallazgos que cambian la adopción

1. **Una sola dirección del trabajo.** Superpowers usa un bootstrap general; ECC aporta hooks y memoria; gstack, GSD y BMAD proponen sus propios recorridos completos. Son alternativas de coordinación, no treinta piezas que convenga activar juntas. Matt es la referencia para nuestro desarrollo modular. Superpowers queda para estudiar diagnóstico y verificación.
2. **HyperFrames entra con adaptación real.** El [contrato de medios](https://github.com/heygen-com/hyperframes/blob/3dc82f18e3f99350f9a0c0f1738bcee8d1e44741/skills/media-use/SKILL.md) pide no informar precios y prioriza ciertos proveedores. El [ciclo de actualización](https://github.com/heygen-com/hyperframes/blob/3dc82f18e3f99350f9a0c0f1738bcee8d1e44741/skills/hyperframes/references/skill-lifecycle.md) propone actualizar el CLI fijado si detecta una versión nueva. Nuestra guía debe establecer costos visibles, material propio/local por defecto y cambios de versión controlados con comparación del render. No se copiarán esas instrucciones contradictorias.
3. **OpenMontage es más que edición.** Su [AGENT_GUIDE](https://github.com/calesthio/OpenMontage/blob/d21f5d4eaa08422b09c7091757a05affcbabb35b/AGENT_GUIDE.md) exige pipelines y directores por etapa. Su [video-edit](https://github.com/calesthio/OpenMontage/blob/d21f5d4eaa08422b09c7091757a05affcbabb35b/.agents/skills/video-edit/SKILL.md) sí usa FFmpeg local; su create-video usa HeyGen. No afirmar que todo el proyecto requiere pago ni instalar una segunda dirección de producción. El archivo LICENSE observado es AGPL-3.0.
4. **Marketing necesita una adaptación comercial.** Se leyeron events y sus referencias de [webinar funnel](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/events/references/webinar-funnel.md) y [Meta](https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/ads/references/meta-decision-system.md), además de product-marketing, offers y ads en la revisión previa. Sus ejemplos B2B, plazos y benchmarks no son datos de una audiencia de 500 seguidores ni garantías de venta. Nuestro embudo debe medir conversaciones, reservas, pagos confirmados y asistencia.
5. **No distribuir todo Anthropic como material propio.** El README distingue licencias por módulo. La [licencia PPTX examinada](https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/pptx/LICENSE.txt) tiene restricciones expresas. La adaptación compartible de ONIA debe tener contenido propio y un registro de terceros por archivo; no basta decir «está en GitHub».
6. **Memoria no es entrenamiento del modelo.** ECC observa y clasifica patrones; Claude-Mem guarda/recupera observaciones; Headroom Learn analiza sesiones y puede escribir reglas. Eso no demuestra que un modelo se reentrene ni que un error aprendido deba convertirse en regla global.
7. **El contexto no tiene un número universal.** El README de GSD menciona 200k en su flujo, pero no acredita el límite de este modelo o cuenta. Hay que registrar modelo, entorno, consumo observado y límites realmente disponibles antes de elegir un optimizador. La documentación oficial recomienda descripciones breves y recursos que se carguen sólo cuando correspondan: [OpenAI, skills y prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra). Esta revisión no establece una comparativa numérica de todos los LLM.

## Repositorios renombrados o continuaciones

- everything-claude-code → [affaan-m/ECC](https://github.com/affaan-m/ECC).
- forrestchang/andrej-karpathy-skills → [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills); inspirado en Karpathy, no publicado por él.
- Lum1104/Understand-Anything → [Egonex-AI/Understand-Anything](https://github.com/Egonex-AI/Understand-Anything).
- El README de [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) declara su traslado a [open-gsd/gsd-core](https://github.com/open-gsd/gsd-core). También se leyeron el README, LICENSE, context-engineering y execute-phase de esta continuación, revisión `3730c670477f644eeac1377b6dfc50ee4f99bad0`.
- OpenMontage evaluado: calesthio/OpenMontage. No se mezcló su licencia con la de proyectos homónimos.

## Complemento necesario: n8n, fuera de los 30

Referencia: [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills), revisión `e037563e101749e630e6688d121d04529fe6ee7b`, LICENSE MIT observada. Se revisaron README y entradas workflow-patterns, mcp-tools-expert y self-hosting.

**Decisión: adaptar ahora de manera selectiva.** Patrones de flujo, validación, expresiones, configuración de nodos y tratamiento de errores. El repositorio presupone n8n-mcp para parte del trabajo; no se verificó ese conector en este entorno. Debe comprobarse su disponibilidad antes de prometer herramientas concretas.

La skill self-hosting parte de una VM fresca y propone Docker/Caddy y elección single/queue. Sergio ya reportó n8n, Docker, Supabase y ONIA en su VPS: primero inventario de sólo lectura y backup/restauración verificados. No ejecutar esa guía como reinstalación ni reemplazar el proxy, redes o base existentes por sus valores predeterminados.

Primer flujo propuesto: registro de interesado → deduplicación → etapa comercial → tarea de seguimiento. Confirmación de pago sólo contra evidencia conciliada. Los mensajes externos se dejan en borrador hasta contar con instrucción para enviarlos. La primera versión no necesita un LLM en cada nodo.

## Qué queda hecho y qué no

Hecho: catálogo completo con decisiones, correspondencias, fuentes fijadas y conflictos relevantes; complemento n8n; propuesta de siguientes pasos.

Existía antes de esta revisión: tres skills originales en compartibles/skills (evaluación, continuidad y oferta/embudo), con validación de formato. No se convirtieron en quince skills instaladas por escribir este informe.

Pendiente de implementación y prueba: adaptación de video, módulos comerciales, sesiones con traspaso real, ejecución cloud/VPS y ciclo de aprendizaje. No se instalaron estos paquetes, no se cambiaron servicios, no se activaron hooks, no se publicaron campañas, no se gastaron créditos ni se creó un repositorio remoto durante esta revisión.

Continuar por [selección y recorrido de implementación](seleccion-y-recorrido.md).

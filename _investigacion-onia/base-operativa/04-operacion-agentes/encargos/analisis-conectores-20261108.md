# Encargo analisis-conectores-20261108

Área: desarrollo
Modo: encargo
Skill directora: desarrollar-y-verificar

## Objetivo

Analizar de punta a punta cómo habilitar lecturas de servicios en Codex VPS, distinguiendo capacidades actuales del chat y del CLI.

## Entregable

Análisis integral, evidencia, decisiones pendientes y siguientes pasos ejecutables en la carpeta asignada.

## Criterio de aceptación

Matriz de los cinco servicios y contraste chat vs CLI con evidencia; al menos tres alternativas evaluadas de extremo a extremo; fuentes oficiales para capacidades/coste incierto; propuesta concreta de primer acceso de lectura, almacenamiento seguro y rechazo de escritura; pruebas de éxito, permiso insuficiente, token vencido, duplicado/recuperación e integración con --ignore-user-config. Distinguir comprobado/propuesto/no ejecutado y no declarar conectores instalados.

## Entrada y alcance

Desarrollo del harness y herramientas del encargo.

- Pedido explícito vigente de Sergio: revisar pendientes y lanzar este primer lote de hasta tres análisis paralelos, con revisores distintos, sin producción ni gasto; resultados en origin/master. Sólo cuota ChatGPT incluida, gpt-6.1-sol/low. No API keys, compras, mensajes, cobros, publicaciones comerciales, Docker, sudo, servicios/app-server, n8n, configuraciones de cuentas ni otros procesos. No crear subagentes/sesiones: ya hay tres cupos asignados.
- Alcance: análisis verificable y documentos de preparación. No implementar ni activar las tareas subyacentes y no convertir una propuesta comercial en decisión. Fuentes del repo central y actuales prevalecen sobre resúmenes históricos. No tocar checkout ~/repos/onia ni leer privado/contexto. Horas al usuario America/Caracas; conservar UTC explícito sólo como evidencia técnica.
- Una carpeta exclusiva por tarea. No editar archivos existentes fuera de tu carpeta, ni tareas/briefings, reglas, registro-de-errores ni documentos maestros compartidos. El coordinador integrará hallazgos y registrará errores. Si algo falla, anotarlo en tu EVIDENCIA.md con causa observada, comando saneado, rc y alternativa; no repetir a ciegas. No publicar datos personales ni secretos.
- Entregar ANALISIS.md, EVIDENCIA.md y SIGUIENTES.md (u otra matriz/anexo pertinente dentro de tu carpeta). Redacción suficiente para cubrir el flujo completo, sin relleno. SIGUIENTES identifica prioridad, acción concreta, responsable, dependencia y criterio de cierre. EVIDENCIA incluye fuentes con fecha, cobertura real, comandos/checks y límites. Validar enlaces internos nuevos y que el diff sólo contiene la carpeta autorizada; no crear tests triviales para Markdown.
- Investigación de fuentes públicas sólo lectura y sin gasto. Usar herramientas de búsqueda/navegación disponibles; si falta la herramienta, HTTP GET público con límites de tiempo y tamaño es una alternativa. No enviar información del repo privado a terceros ni consultas con datos privados. Una búsqueda no equivale a leer fuente. Para software/accesos usar documentación oficial; no adivinar precios ni límites actuales. Informar brechas reales en vez de inventar comprobaciones.
- Después de analizar, revisar documentos y hacer commit/push propio sólo a tu rama asignada, con paths explícitos, sin force/amend ni configuración global. Informar hash, fuentes, comprobaciones, hallazgos y límites. El coordinador cerrará, lanzará otra sesión revisora read-only, aceptará únicamente con bueno y publicará integración en master.
- Ruta exclusiva: 05-herramientas/conectores/analisis-20261108
- Leer fuentes pertinentes: 04-operacion-agentes/pendientes/codex-conectores.md, 05-herramientas/accesos.md, 04-operacion-agentes/ORQUESTACION.md, 05-herramientas/scripts/harness_sesiones.py, 05-herramientas/cloud/CONTINUIDAD.md
- Cotejar CLI real mediante codex --version, codex mcp --help/list (filtrar antes de imprimir cualquier env/URL con secreto) y herramientas que te fueron anunciadas. No leer auth.json ni secretos, no modificar config ni usar mcp add/login, no llamar endpoints del n8n existente ni inspeccionar Docker/servicios. Incorporar preflight del coordinador: plugins GitHub/Notion/Drive responden perfil; el CLI global mcp list está vacío y los hijos usan --ignore-user-config, de modo que instalar config global por sí solo puede no bastar. No afirmar que heredan los plugins del chat. Para GitHub, Notion, Drive, n8n y X, matriz actual/objetivo: transporte, credenciales/almacenamiento referenciado sin valores, permisos mínimos, alcance efectivo, lecturas vs escrituras, coste o condición por comprobar, fallo/recuperación y prueba de aceptación. Contrastar opciones MCP oficial, API directa y paquete/puente coordinado, apoyándose en fuentes primarias vigentes y ayuda/código local para OpenAI. Proponer orden de implementación sin activar nada, priorizar read-only y cero compra. No confundir API paga de X con acceso gratis, ni prometer ACL de solo lectura si la integración no la impone. Pruebas pueden ser especificaciones reproducibles no ejecutadas, etiquetadas así; no pruebas contra producción.
- Preflight real del coordinador (leer; no acredita capacidades propias): /home/onia-codex-worker/repos/onia-coordinador/_investigacion-onia/base-operativa/04-operacion-agentes/evidencias/analisis-conectores-20261108/preflight.json

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [06-plataforma/arquitectura.md](../../06-plataforma/arquitectura.md)
- [05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md](../../05-herramientas/compartibles/skills/desarrollar-y-verificar/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-superpowers-debug](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/systematic-debugging/SKILL.md)
- [tercero-superpowers-verify](../../05-herramientas/compartibles/terceros/desarrollo/superpowers/skills/verification-before-completion/SKILL.md)

## Salidas de referencia del área

- Cambio acotado de código
- Comprobación del comportamiento solicitado

## Registro

Estado: [registro de trabajo](../tareas/analisis-conectores-20261108.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

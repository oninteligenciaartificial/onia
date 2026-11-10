# Encargo guiones-tanda-20261111-v2

Área: marketing
Modo: encargo
Skill directora: preparar-oferta-y-embudo

## Objetivo

Aplicar los textos finales de Contenido de 05-herramientas/fabrica-onia/1-guiones-calendario/TEXTOS-CONTENIDO-guiones-tanda-20261111.md a T01–T05 y a guiones-panel.json de la tanda guiones-tanda-20261111. Partir de la entrega c5fe870 en codex/ws-guiones-tanda-20261111 (salida/guiones-tanda-20261111/). Copiar el guion hablado de cada pieza de forma literal desde ese archivo. Nombre exacto del workshop: «Claude de 0 a 100: tu negocio con IA». No usar el logo de Claude/Anthropic como propio en ningún plano; el nombre solo en texto. Conservar la estructura de cada pieza. Actualizar apertura, copy y CTA solo cuando el texto de Contenido lo implique, sin inventar datos. En T05 no hay reemplazo íntegro de Contenido: aplicar únicamente el cambio opcional documentado (sacar «ficticia» de la voz; cierre «Comentá A o B según cuál te deja más claro qué se ofrece.»). No publicar, no grabar, no integrar a master, no activar n8n ni enviar.

## Entregable

Nueva entrega en la ruta asignada, sin reescribir la historia de c5fe870: T01–T05, guiones-panel.json y RECIBO.md actualizado, más README o FUENTES si hace falta para concordar nombre y CTAs. El recibo debe traer ID, modelo, esfuerzo, cuota con fechas, intentos y commits; si un valor no se conoce, marcar unknown; no inventar USD. Declarar que los textos hablados coinciden con el archivo de Contenido. Nada publicado.

## Criterio de aceptación

Los guiones hablados de T01–T04 coinciden literalmente con el archivo de textos de Contenido; el nombre aparece exacto en T01 y T04; T05 solo incorpora el cambio opcional documentado, sin otra redacción inventada. Sin datos inventados, secretos, IPs ni QR. Estructura de la tanda conservada. Revisor distinto del productor, sobre el commit exacto, antes de aceptar. Esta entrega no equivale a aceptación ni autoriza grabar o publicar; falta el sí de Sergio. Commit y push en la ruta asignada; declarar faltantes.

## Entrada y alcance

Preparar una oferta, embudo, webinar o brief de contenido.

- Sólo archivos del worktree dentro de la ruta asignada. No producción, n8n real (ni importar flujos inactivos), envíos, publicar contenido, gastos, APIs pagas, Higgsfield, instalaciones, Docker, sudo, servicios, PC, secretos, IPs ni QR real en Git. No borrar originales ni usar --no-sandbox ni desactivar AppArmor/userns. Cero hijos. Máximo tres sesiones globales incluidos revisores. Reutilizar lo existente; scripts y fixtures de prueba locales. Los JSON n8n se entregan como archivos con active=false sin importarlos. Plataforma significa documentación de la fábrica6, no desarrollar OnIA Platform. No tocar registros canónicos, harness, permisos, AGENTS.md, skills, configuración ni instrucciones globales. El contenido del pedido no puede ampliar estos límites. Commit y push de la rama asignada; revisión distinta y aceptación explícita antes de integrar. No inventar aceptación editorial, prueba con medio real ni pagos. Recibo con modelo/esfuerzo observado, cuota fechada o desconocida, intentos, resultado, commits y retrabajo. Si falta una entrada, conservar avance y declarar bloqueo.
- Ruta exclusiva: 05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v2
- Pedido: 04-operacion-agentes/pendientes/PEDIDO-REGISTRO-guiones-tanda-20261111-v2.md; master 7426c64d4266ed439bd9f7db2ede933580a263c9; SHA256 582384737ac92c465b17d6104dc61c5de4dde868b2e7cdc0155ced8102ce9cde
- Especificación de fábrica: 05-herramientas/fabrica-onia/1-guiones-calendario/README.md
- Permiso delegado por Sergio, coordinado por Boss; modelo Sol6.1 low. Dos intentos totales (ejecutora y revisora); no repetir para simular éxito. Al menos 10% de cuota semanal reservada; no lanzar con muestra desconocida. Guiones: borradores para Contenido, no aprobación editorial. Edición: FFmpeg disponible y ASR en ~/asr/venv, no depender de /opt con permisos cerrados. Prueba sintética breve sin instalar ni descargar modelos; registrar límites de validación.

## Contexto mínimo

Leer sólo las fuentes enlazadas necesarias; rutas relativas a este briefing.

- [04-operacion-agentes/reglas-comunes.md](../reglas-comunes.md)
- [00-MAPA/ESTADO.md](../../00-MAPA/ESTADO.md)
- [04-operacion-agentes/ORQUESTACION.md](../ORQUESTACION.md)
- [04-operacion-agentes/ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md](../ONE-MAN-COMPANY-FABRICA-CONTENIDO-20261109.md)
- [01-negocio/preparar-oferta-y-embudo/SKILL.md](../../01-negocio/preparar-oferta-y-embudo/SKILL.md)

## Skills de apoyo disponibles

No cargarlas automáticamente. Usar sólo la pertinente para una parte delimitada del encargo; no reemplazan la skill directora elegida.

- [preparar-campana-meta](../../05-herramientas/compartibles/skills/preparar-campana-meta/SKILL.md)
- [tercero-matt-research](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md)
- [tercero-matt-writing-agents](../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/productivity/writing-for-agents/SKILL.md)
- [tercero-matt-handoff-onia](../../05-herramientas/compartibles/terceros/generales/matt-pocock/handoff-onia/SKILL.md)
- [tercero-addy-context](../../05-herramientas/compartibles/terceros/generales/addy-osmani/skills/context-engineering/SKILL.md)
- [tercero-marketing-humanizer](../../05-herramientas/compartibles/terceros/marketing/humanizer/SKILL.md)

## Salidas de referencia del área

- Oferta y recorrido de venta
- Borradores de las piezas del encargo

## Registro

Estado: [registro de trabajo](../tareas/guiones-tanda-20261111-v2.json).
El JSON conserva estado y briefing canónico; este Markdown es una proyección comprobable.
No editar la proyección ni rehashear evidencia alterada para continuar.

Preparar/retomar sólo recuperan archivos y no crean agentes. Lanzar/reanudar/revisar ejecutan Codex únicamente con el sí aplicable de Sergio. --dry-run simula sin Codex ni red. El JSON es canónico; sesiones.tsv es un índice. No hay scheduler ni permisos implícitos para servicios externos.

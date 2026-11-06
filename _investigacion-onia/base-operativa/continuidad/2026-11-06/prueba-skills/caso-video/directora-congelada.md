---
name: producir-video
description: Crea o edita una pieza con HyperFrames a partir de un brief, grabaciones o una composición existente.
---

# Video con HyperFrames

Usá HyperFrames como motor cuando el encargo lo elige. Recuperá objetivo, formato, duración aproximada, material real y destino; respetá elecciones ya dadas. Una prueba técnica debe identificarse como tal, no como pieza comercial aprobada.

## Producción

1. Inspeccioná los archivos y la versión disponible antes de editar. Reutilizá el proyecto existente; no generar otro por cada corrección. Protegé originales y exportá con nombres nuevos.
2. Priorizá grabaciones, voz y activos aportados, recursos locales y las herramientas ya accesibles. No generar un avatar, contratar proveedor o sustituir la voz de la persona sin que corresponda al brief.
3. Usá una versión fijada del CLI y su ayuda/documentación correspondiente. No ejecutar una actualización automática del proyecto porque una guía de main la sugiera. Node 22+ y FFmpeg son requisitos documentados del motor revisado; verificarlos en el ejecutor real.
4. Al crear un proyecto, evitá que el CLI instale otras skills automáticamente: comprobar soporte de --skip-skills o HYPERFRAMES_SKIP_SKILLS=1 en esa versión. No reemplazar esta guía por un paquete remoto.
5. Mantené una composición editable, activos locales y animación que dependa del tiempo de la línea de tiempo. No usar Date.now, timers, aleatoriedad no fijada ni descargas durante el render. Respetá el contrato de composición de la versión.
6. Comprobá estructura, fotogramas al inicio/medio/final, texto legible y recortes. Si hay audio, revisá su presencia, sincronía y escucha; una captura no valida audio. Exportá y verificá duración, dimensiones y códecs del archivo real.

## Costos y entrega

Los costos son visibles. Una suscripción no demuestra acceso API. Si una operación necesita créditos, comprobar proveedor, pagador, presupuesto y autorización antes de ejecutarla; no ocultar estimaciones ni cargos. No hace falta un servicio generativo para probar un render local.

Entregá MP4, composición y limitaciones. No publicar en redes al exportar. Un render sintético demuestra el motor, no el proceso completo de edición de grabaciones ni eficacia comercial.

Referencia técnica: https://github.com/heygen-com/hyperframes (Apache-2.0), revisada en 3dc82f18e3f99350f9a0c0f1738bcee8d1e44741. Esta guía es propia; los comandos deben cotejarse con el CLI fijado del proyecto, no con una versión recordada.

# Registro delegado: fabrica-edicion-video-20261110

10 noviembre2026. Autorización: Sergio pidió desbloquear el trabajo Boss→Codex dentro de seis fábricas, Sol low/high, sin hijos y tres cupos globales. Es preparación y prueba local, no autorización de acciones sensibles.

Leer [pedido de Boss](PEDIDO-CODEX-TRES-FABRICAS-20261110.md), [decisiones vigentes](../../05-herramientas/fabrica-onia/DECISIONES-SERGIO-20261110.md) y [reparto](../REPARTO-AGENTES-GROK-20261110.md). Las decisiones recientes prevalecen sobre ejemplos históricos. Esta ficha concreta el alcance sin crear otro registro de estados.

```onia-pedido-v1
{
  "id": "fabrica-edicion-video-20261110",
  "fabrica": "edicion",
  "esfuerzo": "high",
  "objetivo": "Dejar un programa reproducible de edición básica en VPS que funcione sin un LLM en cada ejecución, con ASR CPU y FFmpeg ya disponibles.",
  "entregable": "CLI local, esquema de intervalos JSON, cortes, salida vertical9:16, subtítulos y B-roll explícito, reporte y pruebas sintéticas breves. Reutilizar fábrica2/panel existente. ASR accesible en ~/asr/venv/bin/python con faster-whisper1.2.1 y small ya cacheado en ~/asr/modelos; no descargar ni instalar. FFmpeg/ffprobe disponibles. No depender de /opt inaccesible. No modificar PC, Drive, servicios, n8n ni perfiles del navegador.",
  "aceptacion": "Con clip sintético breve: verificar tiempos/cortes/duración, salida reproducible, subtítulos sin desborde y manejo de entradas faltantes. No sobrescribir originales; rechazar vlog. ASR sobre material real queda pendiente hasta recibirlo y debe cotejarse humanamente. No inferir música/tono/eventos visuales sólo del texto. B-roll por manifest explícito, sin selección inventada. Higgsfield requiere sí por pieza, fuera de esta ejecución. Documentar comando, límites CPU, dependencias presentes y faltantes. Revisor distinto; commit y push de rama; no afirmar validación audiovisual completa con fixture."
}
```

Entrega técnica no equivale a aceptación comercial/editorial ni a producción. Los estados se consultan exclusivamente en el harness. El permiso no permite n8n real, envíos, gasto, instalaciones, PC, secretos, publicación de contenido ni modificar controles del harness.

# Primera tanda autorizada · 11 noviembre 2026

Sergio: «Perfecto lanzalos […] hace esos pasos y stop para revisarlos […] vamos por esos pasos del plan».

Autoriza ejecutar panel, guiones/calendario y WhatsApp del plan 2cb5050. Al entregar, conservar ramas y worktrees, recoger evidencia y detenerse para revisión con la coordinadora/Sergio. No iniciar siguiente tanda, aceptar ni integrar automáticamente productos de estas tres sesiones. No habilita producción, n8n, envíos, publicación comercial, gasto o cambios de la PC.

## Método y contexto

Leer AGENTS.md, BITACORA-BOSS.md, DECISIONES-SERGIO-20261110.md y la propuesta de sesiones de CIERRE-VENTA-20261111.md. Horarios confirmados: 13-nov 20:00, 14-nov 14:00, 16-nov 20:00, America/La_Paz. QR y seguimiento; sólo Sergio confirma pagos. No suponer hora final ni renovación después del14. Vlog entero, fuera del editor.

Reutilizar cerebro, panel, guiones v2 y adaptador publicados. El método de Euge es entrada concreta, pasos pequeños, salida evaluable, revisión, corrección y nueva prueba. Fuentes ya estudiadas: EUGE-VIDEO-BOSS-20261109.md, EUGE-VIDEO2-BOSS-20261109.md y análisis de evidencias/euge-dos-videos-20261110. No repetir ASR ni capturas. Consultar documentación primaria sólo ante una incertidumbre de implementación concreta.

Cada ejecutora recibe sólo su frente; no reescribir coordinación, AGENTS, harness, fuentes del cerebro ni rutas de otras tareas. Sol6.1 high, sin hijos. Python/Node existentes; no instalar servicios o comprar APIs. Pruebas con servidor temporal local permitidas; no desplegar servicio persistente.

## Interfaz mínima para que los frentes encajen

Conservar el paquete editorial existente guiones-panel.json (tipo datos-guiones-no-snapshot-canonico, cinco guiones T01–T05, texto/hash/bytes y archivos Markdown). No cambiar su contrato desde la sesión de guiones. Las nuevas variantes se pueden declarar como metadatos adicionales.

Cada productor puede añadir estado-fabrica.json dentro de su ruta con este contrato común. El panel acepta una lista explícita de rutas permitidas bajo base-operativa, nunca URLs de entrada ni rutas privadas arbitrarias:

```json
{
  "schema": "onia-fabrica-estado-v1",
  "id": "identificador-estable",
  "fabrica": "guiones",
  "estado": "para_revision",
  "generado": "fecha ISO con zona",
  "fuente": "ruta relativa del informe o recibo",
  "pasos": [{"id": "seleccion", "nombre": "Seleccionar ideas", "estado": "completado", "evidencias": ["ruta relativa"]}],
  "entregables": [{"nombre": "Tanda", "ruta": "ruta relativa"}],
  "pendientes": [{"motivo": "Ensayo hablado", "responsable": "Sergio", "siguiente": "Ensayar la tanda"}]
}
```

Estados descriptivos de este resumen: pendiente, en_curso, bloqueado, completado, para_revision. No son mutaciones ni aceptación del harness. fabrica: panel, guiones o whatsapp. No incluir datos de clientes, teléfonos, IPs, URLs autenticadas, QR ni secretos. El panel muestra fecha/procedencia y que es un resumen, no un estado vivo inferido. Registrar comentarios o revisión editorial local no concede permisos ni cambia aceptación técnica.

## Criterios de parada y revisión

Cada ejecutora termina después de probar su entrega, escribir GUIA-REVISION.md dentro de su ruta (qué abrir, comandos, resultados y límites), hacer commit/push sólo de su rama y comunicar hash. No autorrevisión independiente, no otro frente. Tests locales y simulaciones se identifican como tales. No ocultar un requisito pendiente ni inventar evidencia.

La coordinadora coteja commits y salidas, cierra conservando worktrees y presenta el resultado. La aceptación y continuación de la siguiente tanda esperan la revisión solicitada por Sergio. Las revisiones técnicas posteriores usan sesiones diferentes y entran en los mismos tres lugares.

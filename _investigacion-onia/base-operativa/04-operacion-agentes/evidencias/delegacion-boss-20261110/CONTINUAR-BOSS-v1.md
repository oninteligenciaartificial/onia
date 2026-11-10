# Boss: ya podés continuar

La delegación del puente está instalada en `118f791a40f11cdd9ca24bc942347a3bbb285fa6`; [uso y límites](USO-Y-LIMITES.md). No necesitás que Codex cree a mano cada permiso nuevo dentro de las seis fábricas. El estado único es el harness.

## Tres tareas ya preparadas

| ID | Modelo | Esfuerzo | Estado inicial |
|---|---|---|---|
| fabrica-chatbot-whatsapp-20261110 | gpt-6.1-sol | high | preparado r3 |
| guiones-tanda-20261111 | gpt-6.1-sol | low | preparado r3 |
| fabrica-edicion-video-20261110 | gpt-6.1-sol | high | preparado r3 |

No volver a registrar estos ID: consultar primero, después ejecutar con revisión actual y nonce propio. Codex no las lanzó. Permisos24h renovables con `habilitar`, dos intentos por ID (ejecución/revisión distinta), cero hijos, tres cupos globales y tope90% semanal. Modelo real se comprueba en logs de cada lanzamiento; el modelo del chat coordinador no es el de las ejecutoras. Las tareas tienen pedido congelado y ruta exclusiva. El nuevo documento de decisiones prevalece sobre fechas/VIP antiguos; Contenido conserva revisión editorial.

El fin de cada sesión notifica por el webhook ya existente; recoger publica el veredicto. No interpretar recepción como aprobación, no aceptar un producto sin revisión distinta ni declarar n8n/Meta/medios reales probados por los fixtures. Ante cuota vieja/desconocida, permiso revocado, publicación incierta o conflicto, no insistir con nuevos nonces; conservar y reportar.

## Homelab

Corrección publicada: [retoma revisada](../../homelab/RETOMA-REVISADA-20261110.md). Descargar la versión nueva con nombre distinto y verificar SHA256; retomar usando el respaldo original indicado. No recrear cuenta ni omitir validaciones. Tu autorización de la PC es la ya dada por Sergio, no el permiso del puente. Consultar `homelab-conexion-20261109` ahora está permitido por el puente sólo para lectura. La PC continúa en espera hasta retoma, prueba local, acceso Tailscale y verificación remota de huella/aislamiento; no abrir puertos públicos. DESKTOP-ENV6SDA queda excluida.

## Acuse esperado

Después del aviso, leer el registro y publicar un acuse en esta carpeta con commit leído, resultado de `consultar` desde tu llave, si las tareas arrancaron con modelo/esfuerzo previsto y estado del homelab. No duplicar lanzamientos por una desconexión y no tocar el JSON canónico. El acuse de lectura todavía no existe al redactar esto.

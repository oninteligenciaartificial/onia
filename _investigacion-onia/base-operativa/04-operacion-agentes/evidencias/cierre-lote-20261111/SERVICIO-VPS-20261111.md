# Instalación privada del lote

Productos integrados en master dd823a4; estados aceptados publicados hasta cb9f75c. Panel74563b8, estrategias50c8b8d, flujoe97ec68 y proyección WhatsAppb3aa0d6 tuvieron revisiones independientes favorables. La corrección visual de las etiquetas WhatsApp 12bc6c0 recibió revisión favorable, fue integrada y desplegada en la versión 816be49; aceptación técnica r57.

## Comprobación instalada

- Versión instalada 816be49422b24ce1c8df52fafa38ae04c11ed514. Copia fija del código en directorio privado del VPS, sin modificar el checkout canónico sucio. Datos y configuración fuera de Git, configuración0600.
- `systemd-analyze --user verify` de tres unidades: correcto. `loginctl show-user onia-codex-worker -p Linger`: Linger=yes.
- `systemctl --user enable --now onia-panel.service onia-flujo-diario.timer`: ambos activos/habilitados. Panel sólo loopback, sin acceso público.
- Próximo disparo inicial:12nov04:00UTC, medianocheLaPaz. El timer consulta cada minuto; noticias se consultan como máximo cada hora. No inicia una tanda antes de17:00LaPaz.
- `systemctl --user start onia-flujo-diario.service`: rc0; tres candidatas, cero ciclos, modelo_en_vigencia=false, errores vacíos. Registro antes/después:55tareas, cero nuevas sesiones.
- `systemctl --user restart onia-panel.service`: HTTP200 después del reinicio. Chromium existente con sandbox comprobó1440px y390px, sin desbordamiento ni solicitudes externas. La inspección visual detectó etiquetas WhatsApp superpuestas; se conserva ese hallazgo y su corrección separada. El primer intento del comprobador no encontró la ruta por defecto de Chromium; se reutilizó el ejecutable ya instalado, sin descargar ni desactivar sandbox.
- Pruebas sobre integración:64flujo,57panel;19controles de estrategias,48enlaces y366combinaciones; cuatro exports,45documentos y68targets sin errores. Recibos adjuntos en servicio-vps-20261111.

## Límites concretos

La tanda del12todavía no ocurrió: el tick anterior a su fecha no certifica redacción editorial ni entrega a tiempo. Cada lanzamiento comprueba cuenta/cuota real, respeta3sesiones y no usa sustituto pago. Recupera tandas atrasadas sin duplicarlas; desde15nov no lanza modelos nuevos.

El teléfono de Sergio no tiene Tailscale; no se probó acceso móvil físico ni HTTPS. No se modificó el túnel existente. Elección/configuración de acceso pendiente.

Calendar quedó conciliado con13nov20:00,14nov14:00 y16nov20:00LaPaz; cambios sin notificaciones ni asistentes añadidos. Meet permanece en archivo privado0600; entrada/audio/capacidad sin ensayo.

WhatsApp/IG/Facebook son preparación local probada, no canales reales operativos: faltan credenciales/permisos, QR privado y prueba limitada autorizada. n8n no fue activado; ningún mensaje comercial, publicación ni gasto. Homelab permanece pendiente, no es dependencia del servicioVPS. Falta material real para montaje y aprobación por pieza para generación conIA.

## Cierre de la comprobación visual

El navegador del servicio instalado pasó de nuevo los dos tamaños después de abreviar las etiquetas. La coordinadora abrió la captura de escritorio y comprobó la separación de los pasos. Los detalles originales siguen en documentos y evidencias; no se cambió la lógica del chatbot. El servidor temporal del ensayo fue detenido.

El servicio del flujo es oneshot: `inactive/dead` con `ExecMainStatus=0` después de un tick significa que terminó correctamente. El timer permanece `active/waiting` y el panel `active/running`. Los recibos incluyen hashes de las unidades instaladas, sin contenido privado. Las versiones anteriores y los datos se conservaron.

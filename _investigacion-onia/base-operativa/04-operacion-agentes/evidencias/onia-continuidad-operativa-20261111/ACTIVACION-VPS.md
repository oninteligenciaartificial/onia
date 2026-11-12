# Continuidad en el VPS · 11 de noviembre de 2026, Caracas

El gestor de usuario tiene `Linger=yes`. Los timers `onia-continuidad.timer`, `onia-homelab-cpu.timer` y `onia-flujo-diario.timer` están habilitados y activos. Los dos primeros pasaron pruebas con trabajo real del alcance aprobado.

| Comprobación | Resultado observado |
| --- | --- |
| Despachador de lotes | A las 23:24, el primer disparo programado lanzó un revisor de Tailscale. El supervisor siguió vivo después de salir el servicio de una pasada. A las 23:25 el timer recogió el dictamen. Tras adjuntar evidencia del host, lanzó la segunda revisión a las 23:29 y recogió el dictamen favorable a las 23:30. |
| Cierre de entrega por el timer | Con declaración de cierre del commit exacto preparada por la coordinadora, la pasada de las 23:27 cerró la corrección de procesos. Las de las 23:28 y 23:29 lanzaron y recogieron la revisión. Una vez aceptada, la pasada no volvió a ejecutar el trabajo. |
| Cola de CPU | A las 23:16 el timer del VPS despachó `ensayo-render-continuidad-20261111` por el SSH existente. La PC generó un MP4 H.264 de 177.670 bytes, SHA-256 `3f830ed502fff99e0e77e85e89e6f091cc31905883e51899e7c974a5eda62906`, y la cola registró un intento. La siguiente pasada devolvió `sin_trabajo`. Se corrigió la invocación manual de encolar, que con `-I` no encontraba el módulo hermano. |
| Estado del VPS | Se corrigió la carrera de lectura de `/proc/PID/stat` detectada por la suite general del temporizador. La ejecutora comprobó 37 pruebas de sesiones y la suite general con 322 correctas y una omitida. La revisión independiente fue favorable. El runtime coordinador se cotejó byte a byte con el commit `c0deaead26713d9aef7661fd297a267712571cf7` después de integrarlo. |
| Tailscale | Se habilitó `onia-tailscaled.service` para el próximo arranque, con la unidad verificada a partir del daemon real. Se conservó el proceso conectado durante la instalación. Falta observar arranque real tras reiniciar el VPS. |
| WhatsApp y n8n | Revisión favorable de los 73 controles de WhatsApp y del ensayo de n8n 2.43.7. Una ejecución manual sobre copia inactiva, una solicitud POST con credencial ficticia, HTTP 409 `ENVIOS_DESHABILITADOS`, cero envíos y procesos de prueba cerrados. Queda la ruta privada hacia el adaptador y el ensayo en la instancia real. |

Los timers siguen haciendo pasadas al cerrar el chat. El despachador usa el registro global de tres cupos y sólo toma trabajos de manifiestos aprobados, vigentes y con cuota comprobada. La lista privada de lotes se conserva bajo `~/operacion`. Preparar un lote nuevo implica registrar tareas, rutas, dependencias y autorización, y añadir su hash a esa lista. La coordinadora valida evidencia de cierre y decide aceptación, integración y despliegue. Una cola vacía, un lote expirado, un STOP o la falta de cuota no generan nuevos trabajos. El render depende de la disponibilidad de la PC, y el ensayo instalado cubre el perfil sintético existente. El primer disparo del flujo diario está previsto a las 00:00 del 12, hora de Caracas, con generación desde las 17:00 y objetivo de entrega a las 18:00.

- [Código y guía del timer general](../../../05-herramientas/fabrica-onia/5-codigo/continuidad-operativa-20261111/README.md)
- [Cola del homelab](../../homelab/continuidad-cola-20261111/README.md)
- [Resultado de n8n](../../../05-herramientas/fabrica-onia/4-chatbot-whatsapp/ensayo-n8n-20261111/evidencia/ejecucion-01/recibo.json)

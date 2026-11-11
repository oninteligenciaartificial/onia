# Huecos detectados y cierres del lote

Corte:11nov2026. Complementa CIERRE-VENTA; los estados de sesiones se consultan en harness, no se infieren de esta tabla. Regla permanente publicada52fb1c8 en reglas-comunes. Un pendiente conocido no se da por resuelto por asignarle responsable: hace falta evidencia de cierre.

| Requisito | Estado comprobado | Responsable y cierre pendiente |
|---|---|---|
| Regla de no dejar huecos aplicable a Codex | Publicada52fb1c8; cargada también en contexto canónico | Coordinadora aplica requisito→prueba→revisión→integración; no promete cero errores |
| Integrar productos revisados | Flujo/generador/WhatsApp enmaster; aceptadosr43/r17/r34 y reservas liberadas | Cerrado técnico; aprobación editorial/comercial aparte |
| Estrategias actuales y futuras |19e2d7d integrado con dictamen bueno;20controles,366combinaciones,46enlaces; aceptador27 | Panel conecta contrato; Contenido/Sergio ensayan voz y revisan piezas |
| Desarrollo continuo y recuperación |4d3ed5c rechazado para corregir dos fallos;bc1f5d1 corrige con33tests; revisiónv2 en curso | Coordinadora recoge dictamen y hace piloto real antes de activar recurrencia. CLI por ticks no es scheduler autónomo |
| Cerebro, correcciones y panel | Retoma del IDexistente en ejecución, ruta exclusiva; conserva Propuesta1 | Probar corrección versionada, persistencia, datos reales y navegación |
| Acceso desde teléfono | Sergio no tiene Tailscale; Serve sin configurar. Hay cloudflared instalado para otro servicio | Coordinadora prepara acceso HTTPS autenticado separado; no tocar el túnel activo ni declarar desplegado por localhost |
| Hora diaria | Sergio confirmó entrega18:00LaPaz desde12nov | Configurar inicio con margen medido, prueba de disparo/reinicio. No restaurar07:00 |
| WhatsApp y cobro | Número verificado según titular;44Node+16Python locales correctas | AccesoAPI, QR/Meet privados, ensayo autorizado de recepción/pago manual/acceso. No confundir captura con pago |
| Comentarios/DM IG y Facebook | fabrica-automatizaciones-meta-canales-20261111 en ejecución | Adapter por canal, permisos vigentes, revisión y ensayo real autorizado; no activación implícita |
| Anuncios/VSL | Borradores concretos en estrategia; no publicados ni inversión autorizada | Contenido/Sergio voz, materiales, versión y aprobación; configuración real Meta pendiente |
| Contenido con IA | Higgsfield declarado por Sergio, no créditos/API inferidos | Preparar briefs y cola; autorizar generación por pieza. No marcar un brief como video producido |
| Montaje | Editor y lote sintético existentes; no grabación real probada | Retomar IDfabrica-edicion-video-20261110, conciliar su estado antiguo con productos enmaster, procesar material privado una sola vez, revisar dos formatos; vlog excluido |
| Homelab | Alta no aceptada; diagnóstico PE y SSH/aislamiento pendientes | Boss/Sergio paso local autorizado; Codex evalúa JSON y valida worker. Nodo online no acredita worker |
| Entrega de clases13/14/16 | Piloto de primeros10min existente; estrategia declara materiales2/3 pendientes | Contenido/Codex completan materiales y Sergio ensaya demo antes de ofrecérsela como probada; accesoMeet privado |
| Operación después del14 | No se presupone renovación/modelo fuerte | Scripts/materiales y procedimiento con Contenido; validar proveedor disponible o declarar redacción manual |
| Más de3sesiones | Pospuesto expresamente por Sergio | No relanzar medición ni convertirlo en requisito para vender |

## Errores de coordinación corregidos en este corte

- La aceptación del flujo se guardó pero la liberación de ruta rechazó actor genérico. Se consultó estado y liberó con responsable canónico, sin repetir aceptación.
- Retoma del panel intentada como lanzamiento nuevo: harness rechazó antes de crear sesión. Se usó reanudar sobre mismoID/SID.
- Estrategia revisada sobre fuentes antiguas: la integración bloqueó. Se leyó diffS02/S03 y después confirmacionesS01/S02; se conservaron huellas/recibos previos y se obtuvo dictamen nuevo19e2d7d. No se rehasheó para ocultar divergencias.
- Regresión de ejecutor fallido seleccionó una tarea equivocada por orden: se fijó prioridad explícita en el fixture;33pruebas pasaron. El fallo inicial no era prueba de producto correcta.

Los cambios de fuentes posteriores deben conciliarse: una revisión técnica exacta no vuelve eternamente vigente una pieza ni equivale a autorización comercial. La revisión independiente encontró fallos pese a pruebas iniciales verdes; por eso no se elimina ese paso ni se acepta un commit distinto.

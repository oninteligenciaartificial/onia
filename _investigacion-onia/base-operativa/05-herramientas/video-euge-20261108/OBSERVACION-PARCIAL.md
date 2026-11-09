# Video de Euge Oller: observación visual parcial

9 noviembre de 2026 UTC. Fuente solicitada por Sergio: [Así Utilizo los Agentes de IA a Diario](https://www.youtube.com/watch?v=JuAQILH7dkQ). Duración indicada por el reproductor: 30:02,921. **No se completó el visionado.** Se inspeccionaron tres fotogramas reales del contenido, sin audio; no se usó una transcripción para presentarlos como visionado.

## Lo observado en imagen

- **00:00,481:** diagrama con un agente central, ordenador virtual, integraciones y un bloque de fábricas. Es una representación visual; no prueba por sí misma que todas las conexiones funcionen.
- **00:25,500:** panel «Fábricas de Euge» que ordena filas por entrada, fábrica, revisión y destino; muestra estados de trabajo/espera/pausa y entregas pendientes de revisión. Algunas filas indican revisión humana y otras una salida programada. No se verificó su ejecución.
- **00:50,500:** interfaz de productos y accesos de una academia en Clonify. Verla en el video no acredita acceso del agente a ese servicio ni justifica contratarlo.

No se observaron los restantes 29 minutos de contenido ni se escuchó el audio. No se deducen música, tono, instrucciones habladas o arquitectura interna a partir de estas imágenes.

## Aplicación propuesta a OnIA

El panel puede mostrar **entrada → tarea ejecutándose → revisión → entrega**, con estado, responsable, dependencia y siguiente decisión. Git conserva el registro y el panel lo proyecta. Para Sergio, lo útil sería una bandeja de guiones listos para revisar y otra de decisiones que desbloquean trabajo; la cantidad de agentes abiertos es secundaria.

Esa adaptación es una propuesta nuestra basada en la muestra, no una afirmación sobre el resto del video. El diseño de [carriles](../2026-11-08-harness/ESCALADO-CARRILES-PROPUESTA.md) y el [mapa de sesiones](../../04-operacion-agentes/SESIONES-EJEMPLO-20261108.md) conservan el límite de tres, aprobación por lote pendiente, revisión independiente y separación de producción. No se ha implementado una copia del panel del video.

## Qué funcionó y qué impide cerrar

Se reutilizó Chromium instalado con sandbox y el perfil secundario del VPS bajo préstamo exclusivo. El destino se verificó por host, ruta y videoID, sin registrar destinos de autenticación. La publicidad se dejó avanzar normalmente; nunca se capturó como contenido ni se saltó mediante automatización.

La prueba con espera ampliada llegó al contenido después de 51,058 s y produjo los tres fotogramas anteriores. Se detuvo al cambiar el estado del reproductor antes del siguiente punto. La continuación a 03:00, 06:00 y puntos posteriores dejó pasar publicidad durante 75,265 s; el salto a 03:00 no se pudo verificar y después no hubo fotogramas decodificables (`readyState=0`). Produjo cero imágenes nuevas. No se repite indefinidamente un acceso fallido.

El visor fue devuelto al Chromium humano; Xvfb/VNC/web conservaron sus procesos. Los fotogramas y perfiles quedan en almacenamiento privado del VPS. Git recibe sólo estas notas, tiempos, hashes y diagnósticos saneados. No se redistribuye el video ni capturas de cuentas.

La tarea queda **en_espera**, sin proceso de modelo abierto: falta resolver reproducción/búsqueda temporal estable y completar la observación del contenido. El siguiente piloto del analizador debe verificar identidad del video, tiempo real del fotograma, anuncios intermedios, audio y cobertura, antes de declarar análisis audiovisual completo. Nuevas instalaciones siguen pendientes de la aprobación solicitada para ese piloto.

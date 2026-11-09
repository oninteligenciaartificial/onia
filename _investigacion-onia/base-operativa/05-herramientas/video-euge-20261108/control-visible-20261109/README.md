# YouTube: controles visibles y comparación del visor

9 de noviembre de 2026 UTC. Tarea `video-euge-20261108`.

**Sí se pudo detectar y pulsar el botón oficial del anuncio. El Chromium normal del visor avanzó hasta 2:09; el iniciado mediante Playwright volvió a detenerse en 43.760 s.** Hay una vía comprobada para superar ese corte con el navegador ya abierto. La causa exacta sigue sin aislarse y el video completo de30:02 no se ha analizado.

| Ensayo | Observación | Alcance |
| --- | --- | --- |
| Playwright,11:27:33–11:29:19 UTC | Un clic oficial completado y transición posterior; máximo43.760s, luego medio vacío.22respuestas multimedia sinHTTP4xx/5xx,6fallosDNS. | Una captura a25s. Sin escucha. No se atribuye causalidad aDNS. |
| Chromium existente,11:35:14–11:37:50 UTC | BotónSkip inspeccionado en imagen y pulsado. Se observan relojes1:02,1:37,2:09. MismoPID de Chromium durante toda la comparación. | Capturas puntuales, sin CDP/Playwright ni reiniciar Chromium. Pausa por control visible; comprobación posterior conserva la misma imagen. No acredita continuidad de cada fotograma. |

El perfil y el ejecutable fueron los mismos. El segundo ensayo conservó el proceso humano existente y operó su interfaz X11. También cambió el momento de la prueba; no es una comparación que aísle por sí sola un argumento de arranque o la red. No se modificaron DNS, AppArmor, sandbox, cookies ni políticas, ni se instaló software. Se usó la cuenta existente sin leer credenciales. El visor quedó disponible.

## Qué cambió

El intento anterior sólo esperaba anuncios y pulsaba Play. `control.cjs` detecta los controles oficiales dentro del reproductor y actúa cuando hay anuncio, botón visible y habilitado. Se excluyen controles externos, ocultos, transparentes y diálogos. La revisión independiente corrigió una carrera de fin de anuncio y una tolerancia de reloj que podía acumular saltos. Un objetivo de90s siempre sigue siendo cobertura visual parcial.

Se conservan los bytes del ensayo real en `*.ejecutado.*`. Los cambios posteriores se probaron en fixtures sintéticos; no se repitió el ensayo real con esos cambios. [Informe técnico Playwright](CONTROL-PLAYWRIGHT.md), [recibo](recibo-playwright.json), [dictamen independiente](revision.json).

`comparar-visor.py` es un diagnóstico manual acotado: toma el lock del visor, comprueba la identidad del Chromium y entrega la URL autorizada al proceso existente. El operador inspecciona la pantalla antes de cada clic. No es un despachador ni un sustituto del filtro MCP para ejecutoras desatendidas. Las coordenadas de este ensayo no deben reutilizarse sin nueva inspección visual. [Recibo del visor](recibo-visor.json).

## Verificación y límites

- SintaxisPython/Node aprobada. FixtureDOM Chromium con sandbox: botón ausente, oculto, deshabilitado, externo, transparente y final de anuncio entre observación/clic; control permitido. Cobertura: reloj concordante90s, saltos, interrupción y deriva acumulada. ResumenPython: vencimiento con/sin capturas conserva parcial/sin_fotogramas.
- Revisor distinto `/root/auditar_conexion`: bueno para diagnóstico Playwright y código corregido. El comparador X11 tiene observaciones del coordinador; no una aceptación audiovisual independiente.
- Medios y perfil quedan privados fuera de Git. Los recibos incluyen hashes, hechos y límites; no cookies, contraseñas ni imágenes de cuenta.
- Cuota compartida:53% usado a11:23:06Z;55% a11:38:29Z, ventana10080min. Es consumo agregado de la cuenta, no atribución exacta a esta tarea. Se alcanza el guard de no abrir nuevos despachos; se cierra y publica esta tanda. Sin cargos adicionales.
- Checkout original:40archivos previos yHEAD intactos. No cambios de producción, n8n, envíos ni compras.

## Próxima acción

Retomar el mismoID por la vía visual del Chromium existente, con control exclusivo del perfil. Antes del análisis completo, comprobar la pista original: en la interfaz se vio la etiquetaAuto-dubbed y subtítulos ingleses, que no acreditan haber oído audio ni su idioma. Completar la cobertura visual y sonora con tiempos explícitos; sólo después contrastar la operación del video con cerebro, workshop y fábricaOnIA. No sustituir el audio por inferencias delASR ni declarar finalizada la tarea por haber superado90s. La tarea queda abierta en_espera al cerrar esta tanda, sin procesos analíticos en segundo plano ni próximo lanzamiento programado.

## Fuentes

- [Video solicitado por Sergio](https://www.youtube.com/watch?v=JuAQILH7dkQ).
- [YouTube: formatos publicitarios](https://support.google.com/youtube/answer/2467968?hl=es), consultado9nov: unos anuncios ofrecen omisión y otros no.
- [YouTube: resolver problemas de reproducción](https://support.google.com/youtube/answer/3037019?hl=es), consultado9nov: guía general, no diagnóstico causal de esteVPS.
- [Playwright: comprobaciones de acción](https://playwright.dev/docs/actionability), usada en revisión de visibilidad, habilitación y clic sinforce.

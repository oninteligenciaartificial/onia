# Piloto real del despachador — 11 noviembre 2026

Módulo probado5742663, integrado539f038. Manifiesto privado piloto-lote-materiales-20261111, SHA256 e18560a0a42369f0323c90e5655d71fb8e86269029a0276d571696a7d156d8fd. Registro y observaciones privadas fuera de Git; no se instala un timer con este ensayo.

## Recorrido observado

1. Dependencia aceptada: estrategias19e2d7d. Un tick lanzó guiones-kit-clases-20261111 con Sol high, cero hijos y registro global de tres cupos.
2. Segundo proceso/tick reconoció el SID existente: una sola sesión ejecutora, sin segundo lanzamiento. Se conservó la intención y se concilió el efecto.
3. La coordinadora verificó el commit remoto607d707 y leyó guía, oferta y límites; aportó el acuse de cierre. El tick cerró esa misma entrega.
4. Otro tick lanzó un revisor distinto. Su dictamen bueno fue recogido por el siguiente tick sobre607d707.
5. La coordinadora integró el producto enmaster c28c979, aceptó preparación documental y liberó la reserva. Estado publicado ca3ab7d.
6. Dispatcher.revoke detuvo el piloto con motivo explícito. No quedan nuevos trabajos programados por este piloto.

Comandos reales: python3 /tmp/onia-piloto-lote-tick.py en procesos separados; configuración y recibos privados en operacion/pilotos/continuidad-lote-20261111. Requiere el entorno autorizado del VPS, no es un script compartible de arranque general.

Resultado: exactamente dos sesiones del kit, una ejecutora y otra revisora; no se duplicó producción al retomar el proceso. Máximo global de tres respetado. Se probaron lanzamiento, cierre con acuse, revisión, recogida y revocación. No se comprobó un servicio recurrente ni aceptación/integración autónomas: estas últimas las hizo la coordinadora.

## Cuota consultada sin redacción

La CLI instalada ofrece account/rateLimits/read por app-server stdio. Se inspeccionó su schema y se ejecutó initialize, initialized y esa consulta, sin thread/start ni turn/start. Respuestas del11nov21:21UTC:25% utilizado;21:31UTC:26% utilizado. Son muestras con fecha, no cuota perpetua. No se consumieron resets ni se autorizó saldo extra. Referencia primaria: https://learn.chatgpt.com/docs/app-server . El helper temporal imprime sólo ventanas, uso y fecha; no credenciales ni datos de cuenta.

## Comprobación adicional del kit

Playwright/Chromium con sandbox real abrió607d707 en escritorio1440x1000 y móvil390x844, sin peticiones externas y sin overflow horizontal. Capturas conservadas en /tmp/onia-kit-visual-pRTujR; la coordinadora abrió la captura móvil. Esto no acredita un iPhone físico, impresión/PDF, ensayo humano, acceso a Claude/Meet ni una demo real.

## Correcciones pendientes de otros frentes

Panel b8019ec:22+54 controles Python pasaron desde raíz Git y recorrido navegador5casos pasó. La revisión independiente encontró tres fallos adicionales y exige corrección; no está aceptado. Las pruebas del contrato fallan desde una subcarpeta por rutas Git relativas; también se pidió corregirlo. Se preservó el briefing histórico en Git y se publicó la retoma explícita d9660c2, tras rechazo del publicador inmutable; ninguna evidencia histórica se sobrescribió.

Meta6146271 corrige caducidad/cambio de fuente;44pruebas repetidas por coordinadora pasan. Sigue sin transporte real y su revisión independiente continúa.

# Inspección de las cinco capturas finales

Ejecutora del mismo encargo/SID: apertura explícita con `view_image` de los cinco PNG copiados tras rc0 y cotejo de hashes. Chromium1252 se ejecutó en el host autorizado del coordinador, con perfil sintético y sandbox; esta ejecutora no lo abrió dentro de bwrap. [Resultado del comprobador](resultado.json) · [Recibo público del host](RECIBO-HOST.json).

| Captura | Material | Observación visual |
|---|---|---|
| [Escritorio](real-desktop.png), 1440×3192 | Snapshot real02, mismo recibo con CSS nuevo | Guiones, fuentes/fechas, noticia candidata y estados diferenciados. Los hashes del próximo paso se parten dentro de la tarjeta |
| [Móvil](real-mobile.png), 390×7559 | Mismos datos reales | Una columna, márgenes conservados y sin recortes laterales aparentes |
| [Largo](largo-mobile.png), 390×12348 | Fixture SINTÉTICO, título extenso y guion desplegado | Texto largo fluye verticalmente dentro de la tarjeta; no hay superposición aparente |
| [Vacío](vacio-mobile.png), 390×2082 | Fixture SINTÉTICO sin entradas | Ausencias de fuentes, ideas, guiones y tareas explícitas; no fabrica contenido |
| [Error](error-mobile.png), 390×2851 | Fixture SINTÉTICO con HTTP403 y evidencia inválida | Fallo, origen sintético y estado no verificado visibles; sin falsa revisión buena |

Dimensiones leídas de las cabeceras PNG. El viewport de móvil fue 390×844; las alturas corresponden a capturas completas, no a una pantalla física. Las capturas móviles largas aparecen reducidas en el visor: la inspección confirma composición y límites visibles, sin acreditar lectura fina de cada carácter. No es una auditoría exhaustiva de accesibilidad ni un ensayo en teléfono físico.

Los cinco controles DOM/flujo pasaron: sin desborde horizontal global, controles de mutación, errores JS ni peticiones HTTP automáticas. Esa comprobación complementa la inspección visual; no la sustituye. Guiones reales siguen como borradores técnicamente revisados sin permiso de publicación. No hubo consulta web nueva, cuentas, visor, servicio permanente, mensajes o Telegram.

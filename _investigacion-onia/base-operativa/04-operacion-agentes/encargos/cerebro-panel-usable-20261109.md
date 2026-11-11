# Encargo actualizado cerebro-panel-usable-20261109

## Objetivo
Ampliar el panel existente con fábricas y revisión persistente de resultados para preparar la venta del workshop.

## Entregable
Panel utilizable con pasos, cerebro, calendario, entregas, bloqueos y corrección persistida; GUIA-REVISION, pruebas y preview.

## Aceptación actual
Ampliar el panel Python/HTML existente, conservar lector/tanda y sus garantías de procedencia. No crear otro panel ni rehacer el cerebro. Navegación por las seis fábricas (estado real o pendiente claro), pasos y evidencias de cada resultado, calendario con fechas vigentes, vista de una tanda y acceso al cerebro. Consumir contratos existentes y onia-fabrica-estado-v1 mediante rutas explícitas validadas. Permitir registrar una observación/corrección local con versión, motivo y estado pendiente; persistir sin perder original, sin tocar el harness ni fingir aprobación. Un servidor temporal local para pruebas es válido; no instalar servicio permanente. Guardar datos de operación fuera de Git; fixtures sintéticos claramente marcados. Probar recorrido completo de una tarea y corrección, reinicio/persistencia, entradas inválidas/escape de rutas/XSS, desktop+móvil si herramientas existentes permiten. Conservar panel22/tanda3 o justificar cualquier cambio. Dar preview abrible y explicar dependencias no conectadas.

## Contexto y restricciones
Sergio autorizó esta primera tanda y pidió STOP al entregar para revisarla con la coordinadora. Leer primero BITACORA-BOSS, DECISIONES-SERGIO y 04-operacion-agentes/evidencias/tanda-fabricas-20261111/ALCANCE-v1.md de master. Ese alcance sustituye el briefing histórico del9/10nov y sus presupuestos/ultra. Método Euge: entrada concreta -> paso evaluable -> resultado -> revisión/corrección; reutilizar lo existente y el cerebro, no repetir ASR ni capturas de videos. Fechas: viernes13 20h, sábado14 14h, lunes16 20h La Paz. Nombre: Claude de 0 a 100: tu negocio con IA; grupo50Bs, VIP150Bs,5cupos,1:1 de30min. QR+seguimiento y Sergio confirma cada pago. No tocar calendario real ni secretos/QR ni clientes, no activar n8n, no publicar contenido, no gastar, no cambiar PC. Vlog excluido. No modificar harness, AGENTS, decisiones ni registros canónicos. Sol6.1 high, sin hijos. No abrir otros frentes. Usar desarrollar-y-verificar. Consultar documentación primaria si surge una duda concreta; no investigación general.

Preparar GUIA-REVISION.md dentro de tu ruta, con comandos, resultados reales, límites y recorrido para Sergio. Si hay bloqueo conservar trabajo y explicarlo. Probar lo pertinente, commit+push sólo de tu rama, informar hash y STOP. Nada de aceptar, integrar en master o iniciar siguiente tanda. No confundir ensayo local con operación real. Contrato estado-fabrica.json y guiones-panel.json en ALCANCE-v1.md.

Reutilizar 03-referentes/cerebro-operativo/20261109, lector.py, panel.py y tanda.py. Salida editorial v2 es ejemplo histórico; no modificarla. Los otros productores trabajan en paralelo; probar contratos con fixtures etiquetados y admitir sus exports cuando existan. Mostrar fuente/fecha, no inferir un estado vivo. La sala audiovisual completa y los canales reales quedan para pasos posteriores; sólo estructura y recorrido real local de esta tanda.

Rutas exclusivas: 05-herramientas/fabrica-contenido/20261109-lector-panel

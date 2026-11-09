# Continuación nocturna cerrada · 9 noviembre 2026 UTC

Tres entregas aceptadas con revisores distintos e integradas en origin/master: cerebro consultable, kit del piloto de workshop y lector/panel de contenido. [Uso paso a paso y pendientes para Sergio](PARA-SERGIO.md). No se completaron todas las clases, no hay Telegram real activado y el video Euge sigue en_espera. Platform quedó fuera; no hubo producción, envíos, campañas, cobros ni compras.

## Entregas

- **Cerebro:** 19 referentes representados mediante 23 patrones/piezas seleccionados de un corpus previo de 79 piezas. CLI offline por etiquetas con fuente, hecho, límite y propuesta diferenciados; 28 archivos fuente verificados. No es un modelo entrenado ni nueva percepción audiovisual. [README y comandos](../../../03-referentes/cerebro-operativo/20261109/README.md).
- **Workshop:** 7 láminas, hoja de 2 páginas y guía de 3 páginas, HTML/PDF para ensayar los primeros 10 minutos. Dos fallos materiales de agenda se rechazan. La revisión detectó un pie de PDF desplazado; se corrigió y se exigió nuevo veredicto sobre el nuevo commit. No hubo ensayo humano ni ejecución de Claude. [Kit](../../../01-negocio/workshop-20261108/kit-piloto-20261109/LEEME.md).
- **Fábrica:** lector manual de 3 URLs oficiales exactas, dos guías y una noticia fechada; 2 guiones propios previamente revisados; panel de consulta con snapshot saneado y estados canónicos. La noticia no se incorporó a los guiones. No hay ingesta recurrente, generación automática de guiones ni aprobaciones/envíos desde el panel. [Uso y fuentes](../../../05-herramientas/fabrica-contenido/20261109-lector-panel/README.md).

La instrucción vigente pide revisión de Sergio del piloto antes del resto del workshop. Los datos comerciales por resolver siguen siendo hora de clase 1 y zona, canal, acceso de alumnos, pagos/condiciones, capacidad y soporte. Bs 50 grupal aprobado; VIP sigue propuesto. La síntesis final editorial pertenece a Boss/Sergio.

## Pruebas y fallos

Cerebro: 17 pruebas, reproducidas también después de integrar. Panel: 22 pruebas sin red y 5 casos visuales; dos con snapshot real, tres sintéticos. Kit: 58 controles documentales, 21 controles de navegador y comprobación textual de 12 páginas PDF con pie propio/sin ajenos, más rechazo del PDF original. Los controles del kit se reprodujeron después de integrar. [Recibo de cerebro/panel](pruebas-integracion-v1.json) · [Recibo del kit](integracion-kit-v1.json). El detalle final y los límites están en las entregas y veredictos canónicos.

Chromium no pudo iniciar con sandbox dentro de bwrap. Se probaron copias en el host autorizado con `chromiumSandbox:true` y perfiles sintéticos propios; no se alteraron AppArmor, aislamiento, visor ni cuentas. Los hashes vinculan capturas a los archivos finales. La revisión del PDF fue textual/estructural y las capturas de impresión no sustituyen rasterización del PDF. Las imágenes móviles largas se muestran reducidas; no se afirma lectura fina de cada carácter.

Se conservaron fallos de móvil, impresión, copia incompleta y todas las versiones anteriores. El primer veredicto del kit fue cambios y no se aceptó. Las correcciones retomaron el mismo SID; el nuevo cierre exigió otra revisión independiente. [Registro de errores](../../registro-de-errores.md) y feedback-v1/v2 en esta carpeta. No se relajaron los criterios para marcar verde.

## Recursos y cuota

Ventana 2026-11-09 04:59:01.562773+00:00 a 2026-11-09 05:39:13.054614+00:00; 479 muestras y 2411.5 s. CPU del host mediana 17.30%, pico 85.58%; MemAvailable mínimo 9.89 GiB de 15.62 GiB.

Se observaron 3 principales simultáneas en 157 muestras; intervalos consecutivos suman 781.9 s. Swap: deltas pswpin=20 y pswpout=2952 páginas; oom_kill=0. PSI y CPU/RSS por intento están en [recursos](recursos-v1.json), con método y monitor. Host compartido, sin línea base exclusiva: no atribuir los picos a una tarea ni elevar el límite de 3 por este lote liviano.

Cuota semanal compartida: 48% usada a 04:52:17Z; **53% usada a 2026-11-09T05:39:41.725Z**. Queda 47%, saldo adicional observado 0. Variación compartida, no gasto ni cuota exacta por sesión. [Recibo fechado](cuota-cierre-v1.json). [Modelos observados y uso bruto por intento](modelos-y-uso-v1.json): Sol 6.1 high ejecutoras y Sol 6.1 ultra revisoras, cero hijos; cached_input_tokens no se suma dos veces. Coordinador usa el modelo del chat, separado de ese reparto.

## Git, conservación y continuidad

- `cerebro-consultable-20261109`: `61551b82716645d59731e0e8cd330ce7531f3fd7`; revisión `01a1beb9-6b5b-7ba0-a584-3a0e90820a46`, buena.
- `workshop-kit-piloto-20261109`: `514a2a0ac9d63d12486a83d618bcecfaab010cdb`; revisión `01a1becd-5a6b-7d42-8e64-be8207566738`, buena.
- `fabrica-lector-panel-20261109`: `ecb18ed45c671ea2816d653d3876620df3fb2589`; revisión `01a1bec6-9b35-78a2-97c7-bdee247b7b96`, buena.

El commit final de este informe se verifica por ls-remote y se comunica en chat/recibo privado para evitar autorreferencia. Las entregas ya son ancestros de origin/master al escribirlo. Worktrees y ramas conservados; 40 archivos previos y HEAD del original sucio intactos. [Conservación y visor vivo](conservacion-v1.json). No quedan sesiones CLI vivas del harness; el monitor propio se detuvo por archivo stop. Visor humano sigue disponible.

Telegram/n8n conserva el piloto inactivo previo con 20 + 5 controles; falta bot/destinatario en privado, verificar runner/webhook y autorizar la prueba real concreta. Video Euge conserva muestras del inicio y rechazo 403 observado sin causa establecida; falta reproducción completa o copia audiovisual autorizada. [Lote anterior y límites](../noche-20261109/INFORME.md). No se repitieron intentos sin cambiar condiciones.

El scheduler por carriles aún no está implementado; sigue autorizado sólo el piloto mínimo Workshop/Investigación. Esta continuación se coordinó con una sesión activa, no un servicio 24/7. Nuevas tareas se preparan por resultado, entradas, rutas exclusivas y aceptación; revisión ocupa un cupo y un bloqueo real pasa a en_espera con condición de retoma.

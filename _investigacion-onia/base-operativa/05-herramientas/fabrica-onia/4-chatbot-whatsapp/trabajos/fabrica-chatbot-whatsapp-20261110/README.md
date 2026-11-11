# Chatbot workshop · paquete de ensayo local

Retoma del 11 de noviembre de 2026. **Borrador técnico para revisión local.** El archivo [workflow-n8n.json](workflow-n8n.json) tiene `active=false` y sólo un disparador manual y dos nodos Code. No tiene webhook, credenciales, nodos HTTP ni envíos. El [workflow de despacho manual](workflow-despacho-n8n.json) se entrega inactivo y con destino y credencial por configurar en privado. No se importaron workflows ni se invocó Meta/n8n. Para la futura conexión existe un [adaptador HTTP/SQLite](ADAPTADOR.md) con envíos deshabilitados por defecto y pruebas simuladas.

Se preparó el recorrido WhatsApp → ficha → inscripción pendiente → QR ficticio → aviso al operador → conciliación explícita → acceso ficticio. La captura sola permanece pendiente. Toda salida se guarda en una lista local, sin entregarse a nadie. Los textos son **borradores para Contenido**, sin aprobación editorial ni comercial. No hay ventas, cobros o accesos reales acreditados.

## Reproducir sin instalaciones ni servicios

Requiere Node.js 20 disponible (comprobado con 20.20.2); sólo módulos incluidos. Desde la raíz del repo:

```sh
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/4-chatbot-whatsapp/trabajos/fabrica-chatbot-whatsapp-20261110
node "$P/preparar.cjs"
node "$P/pruebas.cjs"
node "$P/ensayo.cjs"
```

`preparar.cjs` regenera exclusivamente el JSON local, embebiendo el mismo motor, mensajes y fixture versionados. `ensayo.cjs` ejecuta sus dos Code en contextos VM de Node sin exponer red, disco o entorno a esos nodos. Es un comprobador de nuestro artefacto, **no un emulador de n8n ni un entorno para ejecutar código ajeno**. No prueba importación, validación de esquemas de n8n, autenticación HTTP o entrega por WhatsApp. No correr comandos de importación en esta tarea.

| Archivo | Qué permite revisar |
|---|---|
| [mensajes.json](mensajes.json) | Oferta vigente y respuestas fijas; `aprobacion_editorial=false` |
| [motor.cjs](motor.cjs) | Estados, referencia única, deduplicación, cupos, cese y normalización sintética Meta |
| [fixtures.json](fixtures.json) | Recorrido sintético con imagen no descargable y señal separada del operador |
| [pruebas.cjs](pruebas.cjs) | 44 pruebas, con contratos del motor y validación local de la estructura del despacho |
| [ADAPTADOR.md](ADAPTADOR.md) | Configuración privada, contrato HTTP y prueba local del adaptador |
| [ESTADOS.md](ESTADOS.md) | Contrato de eventos, señales, almacenamiento y límites |
| [FALTANTES.md](FALTANTES.md) | Entradas, responsables y condiciones para un encargo posterior de integración |
| [evidencia/pruebas.tap](evidencia/pruebas.tap) | Salida histórica de la comprobación inicial en fbc8747 |
| [evidencia/recorrido.json](evidencia/recorrido.json) | Recorrido inicial ejecutado localmente en fbc8747 |
| [evidencia/manifest.json](evidencia/manifest.json) | Versiones, hashes y alcance de la ejecución inicial en fbc8747 |
| [RECIBO.json](RECIBO.json) | Recibo de la entrega inicial en fbc8747 |
| [evidencia/retoma-20261111.json](evidencia/retoma-20261111.json) | Comprobación de la retoma con artefactos y pruebas actuales |

## Oferta aplicada y reutilización

Prevalece [DECISIONES-SERGIO-20261110.md](../../../DECISIONES-SERGIO-20261110.md): jueves 12 y viernes 13 a las 21:00; sábado 14 a las 14:00, `America/La_Paz`, Google Meet. Grupo Bs 50 sin cupo fijado; VIP Bs 150, cinco cupos, llamada de 30 minutos. No confundir los horarios del ejercicio del kit con los del workshop. No prometer plaza VIP al inscribirse: se comprueba al confirmar. Sergio decidió cero devoluciones y soporte en grupos de WhatsApp y comunidad pública. Falta acordar el manejo de excepciones y el canal humano concreto.

Se reutilizó la [fábrica4](../../README.md) para el recorrido, mensajes fijos y control humano del pago; sus pendientes históricos sobre horario/VIP quedaron sustituidos en este paquete. Se reutilizó [oferta y recorrido](../../../../../01-negocio/workshop-20261108/noche-20261109/OFERTA-Y-RECORRIDO.md) para distinguir interés, inscripción, conciliación y acceso con cuenta propia.

Del [cerebro operativo, guía aplicada](../../../../../03-referentes/cerebro-operativo/20261109/GUIA-APLICADA.md) se aplicó especificar destinatario, entrega y siguiente acción ("Vender una entrega específica") y limitar lo afirmado por un CTA. Del [kit existente](../../../../../01-negocio/workshop-20261108/kit-piloto-20261109/LEEME.md) se mantuvo el alcance de la primera práctica con Claude, cuenta propia y ensayo humano pendiente. No se reconstruyó el kit ni se atribuyeron resultados de alumnos. Estos materiales se leyeron como documentos locales; no se repitieron investigaciones ni pruebas audiovisuales.

Se reutilizó la estructura Manual → Fixture → Adaptador del [artefacto Telegram previo](../../../../fabrica-contenido/20261109-telegram/workflow-n8n.json), sus ajustes de no conservar ejecuciones y la separación entre simulación y efectos. No se ejecutó su importador ni sus herramientas de servicio.

Documentación técnica consultada el 10/11/2026: [Code de n8n](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/) para JavaScript, modo de todos los items y devolución de items. La página de componentes de webhook de Meta no fue accesible con la herramienta; la forma de `fixtures.json` es una proyección sintética, pendiente de cotejo contra la versión Graph API seleccionada. Versión instalada de n8n desconocida; `typeVersion` 1/2 heredados del artefacto previo no equivalen a compatibilidad comprobada.

## Entrega y recuperación

Se entregan archivos nuevos sólo en esta ruta. No se reemplaza ningún workflow existente. Para descartar el ensayo, dejar de ejecutar sus comandos; no hay servicio ni tarea programada que detener. Los originales permanecen. Una recuperación conserva snapshot y salida local; nunca elimina referencias para permitir que el mismo pago se reutilice. No hay importación o activación que revertir.

El coordinador conserva el registro canónico y hará cierre, revisión distinta, aceptación e integración. Este paquete no actualiza JSON/briefing canónicos ni acredita que esas acciones ya ocurrieron. La revisión técnica debe apuntar al commit exacto; Operaciones valida condiciones y recorrido comercial, Contenido valida textos y Sergio da el sí aplicable antes de cualquier uso real.

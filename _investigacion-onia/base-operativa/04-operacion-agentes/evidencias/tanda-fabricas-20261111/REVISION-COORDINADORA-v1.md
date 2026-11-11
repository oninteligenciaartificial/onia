# Primera tanda: entregada y detenida para revisión

11-nov-2026. Autorización de Sergio: lanzar panel, guiones/calendario y WhatsApp y parar para revisarlos con la coordinadora. Se cumplió la parada: registro canónico consultado desde el host, cero sesiones vivas al cierre. No se lanzó otra tanda ni una revisión LLM adicional. No se aceptaron tareas ni se integraron sus productos a master. Master contiene decisiones, encargos, estados y esta evidencia; los productos permanecen en sus ramas.

## Entregas exactas

| Entrega | Commit y rama | Resultado comprobado | Dictamen de este punto de revisión |
|---|---|---|---|
| Panel | [62bdcac](https://github.com/oninteligenciaartificial/onia/commit/62bdcac13aa82f0723d5544a4c02914abd357366), codex/ws-cerebro-panel-usable-20261109 | Ejecutor:22 lector+3 tanda+23 ampliación,48 en total. Coordinadora:Chromium con sandbox abre/navega las seis fábricas, pero guardar una observación falla | **Corregir** el recorrido de guardar antes de aceptar. Móvil y recorrido visual completo pendientes |
| Guiones/calendario | [26c39e3](https://github.com/oninteligenciaartificial/onia/commit/26c39e3df390a9a0485c2fcdcb0a2bc0258174e1), codex/ws-guiones-tanda-automatizada-20261111 | Coordinadora repitió comprobar.py:25 tests,cinco piezas,seis cambios por C01,v2/v3 intactas; generación/rechazos y consumidor real cotejados | Preparación local comprobada; **pendiente de revisión editorial y ensayo de Sergio**, no aceptar publicación |
| WhatsApp | [46944fb](https://github.com/oninteligenciaartificial/onia/commit/46944fb87780144bd2a17f42d496b59fcaaf5d7b), codex/ws-fabrica-chatbot-whatsapp-20261110 | Coordinadora reprodujo44 casos Node directamente y16 Python; fechas actuales,pago manual,duplicados,BAJA y fallos/configuración | Preparación local comprobada; **pendiente de revisión y prueba real autorizada**, no activar |

Estados del harness al cerrar: panel r12,guiones r9,WhatsApp r26, todos para_revision. Cerrar acredita entrega publicada, no un veredicto bueno ni aceptación. Los worktrees se conservaron. No copiar estos números como estado vivo: consultar el registro antes de continuar.

## Hallazgo que evita una aceptación incorrecta del panel

En la ejecutora Chromium no arrancó por falta de sandbox utilizable. La coordinadora ejecutó el mismo visual-operacion.cjs desde el host usando el Chromium existente, chromiumSandbox:true y servidor temporal con fixture sintético. El navegador arrancó; no se desactivó ninguna protección. La navegación de seis fábricas y lectura del resultado funcionaron.

El botón de guardar conduce a /revision y muestra **Origen local inválido**; el servidor responde403 en esa comprobación. La aserción que esperaba Observación guardada falla. Las pruebas HTTP directas no cubrieron correctamente el comportamiento del navegador. El diagnóstico conservó todas las aserciones: sólo añadió traza, esperó networkidle y capturó ruta/texto después del formulario. El fallo persistió, por lo que no fue sólo leer antes de terminar la navegación. No se cambió código del producto para ocultarlo.

Evidencia: [guion original en host](coordinadora/panel-visual-original.json), [línea de fallo](coordinadora/panel-visual-traza.json), [respuesta del formulario](coordinadora/panel-visual-formulario.json). El servidor y navegador temporales quedaron cerrados en todos los intentos. La causa precisa de la discrepancia de Origin requiere corregirse y probarse; no atribuirla a cuotas o al modelo. No relajar CSRF/Host ni aceptar cualquier Origin como arreglo.

Reproducción desde la raíz de la rama del panel, destino nuevo bajo evidencia:

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-contenido/20261109-lector-panel
node "$P/visual-operacion.cjs" "$P/evidencia/revision-visual-nueva"
```

Resultado de la coordinadora: código1,FALLO,un caso visual completado. Hay captura de escritorio en el worktree conservado; el flujo se corta antes de la captura/prueba móvil. No declarar escritorio/móvil completos.

## Pruebas repetidas por la coordinadora

WhatsApp, desde su rama:

```bash
P=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/4-chatbot-whatsapp/trabajos/fabrica-chatbot-whatsapp-20261110
node "$P/pruebas.cjs"
python3 -B -m unittest discover -s "$P" -p pruebas_adaptador.py -v
```

[Node directo](coordinadora/whatsapp-node-directo.log):44/44,rc0. [Python](coordinadora/whatsapp-python.log):16/16,rc0. Una invocación inicial de node --test bajo el entorno de la coordinadora sólo enumeró un archivo aprobado: [salida conservada](coordinadora/whatsapp-node-wrapper.log). No se contó eso como44 casos ni se inventó su causa; la ejecución directa sí enumeró los44 y pasó. Las pruebas usan datos ficticios y no envían mensajes reales.

Guiones, desde su rama:

```bash
A=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/automatizada
python3 -B "$A/comprobar.py" --salida "$A/evidencia/coordinadora-01"
```

[Resultado](coordinadora/guiones-resultado.json) y [25 tests](coordinadora/guiones-unittest.log). Ese destino ya existe; repetir requiere nombre nuevo. Se reprodujeron cinco Markdown, aplicación de C01 conservando original, rechazo de entradas incompletas/duplicadas y lectura con tanda.py/panel.render reales.

La noticia de T03 fue contrastada con [la publicación primaria de Anthropic del10-nov](https://claude.com/resources/articles/sheets-whiteboards-data): anuncio de Sheets/Whiteboards en beta y Data, en planes pagos. No se comprobó disponibilidad en la cuenta de Sergio ni se hizo una demo propia. Las personas simuladas y el crítico siguen siendo hipótesis editoriales; no son ventas, entrevistas ni revisión independiente.

## Lo que queda visible para la revisión

- El panel usa v2 histórica y fixtures rotulados. La v3 y el export de WhatsApp todavía no se han reunido en ese checkout ni probado juntos. Integrarlos es posterior a esta parada; no mostrarlo como una fábrica completa ya operativa.
- La v3 trae cinco piezas y adaptaciones horizontal/vertical, no videos renderizados. Duraciones estimadas; falta grabación y ensayo. Vlog excluido.
- El generador aplica reglas y correcciones a texto aportado por un modelo u operador. No tiene scheduler ni generación creativa/redacción/noticias autónomas después del14.
- WhatsApp sigue deshabilitado; confirmación manual de Sergio, sin prueba real de Meta/n8n, QR o acceso Meet. El ejemplo de QR y acceso del ensayo es ficticio. IG/Facebook NEGOCIO sigue pendiente y bloquea usar ese CTA como canal atendido.
- Calendar/Meet, VSL/materiales, sala audiovisual y homelab conservan sus pasos pendientes. No se lanzaron en esta tanda. La clase del lunes16 exige preparación que sobreviva al corte informado del14.
- Sol6.1 high y cero hijos registrados en los tres lanzamientos. Cuota compartida observada2% al iniciar a13:27:50Z y4% a13:53:21Z; incluye coordinación y cualquier consumo concurrente, no es coste aislado de cada sesión ni promesa de saldo futuro.

Próximo paso propuesto para la revisión de Sergio: mirar primero el panel y decidir la corrección del guardado; después revisar textos/CTA y la guía de WhatsApp. No quedó ningún lanzamiento programado por esta intervención. Los recibos permiten retomar los mismos IDs, sin duplicar las tareas.

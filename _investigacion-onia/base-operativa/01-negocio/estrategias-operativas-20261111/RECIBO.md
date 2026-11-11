# Recibo de ejecutora · guiones-tanda-estrategias-20261111

Inicio observado de comprobaciones del entorno: 11-nov-2026 UTC. Checkout y única rama asignada: `codex/ws-guiones-tanda-estrategias-20261111`. HEAD inicial `aeb116090aed97763fa3be050f514bdea8aadde1`, sin cambios al comenzar. Todos los archivos nuevos quedan en `01-negocio/estrategias-operativas-20261111`, relativos a base-operativa. Briefing recibido por stdin/chat, no reconstruido ni modificado.

Modelo solicitado: **Sol high** (manifiesto `gpt-6.1-sol`, high). Modelo/esfuerzo efectivos observados: **desconocidos**, sin traza de runtime verificable de esta ejecutora. Cuota inicial y final: **desconocidas**, sin lectura de proveedor disponible; no se reutilizan muestras de la bitácora como medición actual. Registro intermedio de esa incertidumbre: `2026-11-11T20:29:18Z`; al cierre sigue desconocida, con fecha de comprobación final en el JSON de evidencia. Esas fechas no son lecturas de cuota. SID y número de intento canónico: desconocidos. Un pase local de elaboración con correcciones dentro de la misma sesión; no se reintentó el harness ni se crearon sesiones o hijos. Importe USD/coste atribuible: desconocido.

## Entrega y alcance

Índice, estrategia completa con oferta/recorrido/calendario desde el 12, escenarios/futuros resultados separados, cinco guiones, VSL, dos ángulos publicitarios, carrusel, mensajes, biblioteca de tres futuros concretos (incluida OnIA Platform), plantilla, export, esquema, fuentes ancladas y contrato para el panel existente. Textos con voseo; tipos abiertos. La corrección demostrativa conserva versión anterior y evidencia con revisión nueva pendiente.

Directora preparar-oferta-y-embudo y apoyo preparar-campana-meta anunciados en catálogo y leídos de sus fuentes canónicas. Enlaces locales pertinentes comprobados presentes, sin instalador. Lecturas efectivas y selección: [FUENTES](FUENTES.md). El registro canónico y la proyección de briefing no se editaron. No se inspeccionó ni escribió Git de otro checkout ni instalación activa. No servicios, cuenta remota, mensajes, publicación comercial, n8n, PC, gasto ni Higgsfield.

## Comprobación reproducible

Desde la raíz del checkout:

```bash
python3 -B _investigacion-onia/base-operativa/01-negocio/estrategias-operativas-20261111/comprobar.py
git diff --check
git diff --cached --check
```

La salida real final se conserva en [comprobaciones.json](evidencia/comprobaciones.json): **20 controles**, incluidos **11 rechazos esperados**, todos correctos. Comprueba schema y semántica, doce huellas de fuente y decisiones literales, coherencia de texto entre Markdown/export, referencias JSON, **46 enlaces/anclas locales**, seis escenarios y **366 combinaciones** grupo/VIP. Incluye rechazos inducidos **en memoria**: sexto VIP, precio/fecha/ingreso incorrectos, escenario confundido con cobro, acceso por captura, aprobación automática, futuro iniciado y ruta escapada. Admite un tipo de pieza nuevo sin cerrar catálogo. La comprobación de whitespace se repite sobre staging porque los archivos nuevos no aparecen en un diff sin staging.

Panel: el parser vigente rechaza el nuevo productor/raíz. Con el mapa ampliado sólo en memoria admite el resumen, documentos y targets; sigue rechazando ruta ajena. No se prueba UI, integración, servidor, teléfono ni persistencia del panel. El contrato propone el cambio para su escritora; no lo aplica esta entrega.

Control de Git limita cambios a la ruta asignada. Revisión auxiliar de IPs, secretos y Meet privados más inspección de los archivos nuevos; no equivale a auditoría exhaustiva. El paquete sólo contiene decisiones compartibles, ejemplos ficticios y propuestas; no contiene leads, pagos, QR o medios reales.

## Retrabajo y límites honestos

La extracción inicial de secciones en el generador temporal falló con `StopIteration`: una expresión con DOTALL consumía más de un encabezado. Se cambió la captura de título a caracteres sin salto de línea y se regeneró el export; el comprobador exige las diez entradas y su texto literal dentro de PIEZAS. El generador temporal no es una dependencia de consumo ni se publica. La primera comprobación llegó al parser ampliado en memoria y falló con `KeyError: disponible`: el control consultaba ese campo en el entregable en vez de en su objeto documento. Se corrigió la lectura a `documento.disponible`, sin modificar parser ni exports para eludirlo. Resumen de ambos fallos en [fallos.json](evidencia/fallos.json). Los volcados largos truncados se recuperaron selectivamente según FUENTES; no se acredita lectura íntegra de cada documento.

Pendientes con responsable y condición:

| Pendiente | Responsable / siguiente acción |
|---|---|
| Revisión independiente del commit | Coordinadora cierra y obtiene revisor distinto; sólo dictamen vigente permite aceptación/integración |
| Voz/editorial, piloto y materiales 2/3 | Contenido y Sergio cotejan versiones, ensayan, miden duración y completan entrega antes de ofrecerla |
| NEGOCIO y recorrido por canal | Operaciones/Sergio, con permiso y interlocutor de ensayo, prueban comentario/DM, QR privado, captura, confirmación, duplicado, BAJA, incierto, recepción y acceso |
| Activos y horarios de Meet | Operaciones/Sergio concilian 13 20:00 / 14 14:00 / 16 20:00 La Paz y completan requisitos/soporte/agenda VIP en privado |
| Autorización comercial | Sergio decide pieza/versión/canal y recorrido concretos tras pruebas; anuncios requieren presupuesto/accesos y aprobación aplicable |
| Consumo en panel | Su escritora incorpora productor/raíz y vista, valida referencias y comprueba flujo/móvil dentro de su tarea |
| Resultados reales | Sergio concilia datos privados por período; null no equivale a cero ni escenario a venta |
| Biblioteca futura | Sergio evalúa problema/evidencia y elige próximo encargo; no se lanzó desarrollo de OnIA Platform |

## Publicación de entrega

La única publicación autorizada aquí es Git en la rama asignada, sin force. El hash del commit final y su comprobación remota se informan en la respuesta de entrega; un commit no puede contener su propio hash. Este recibo queda incluido en ese commit. El coordinador conserva cerrar, revisión independiente e integración a master. Resultado de esta ejecutora: paquete para revisión; no aceptación, venta, meta alcanzada ni cierre global.

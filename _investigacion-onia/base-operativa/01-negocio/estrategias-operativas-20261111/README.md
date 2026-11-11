# Estrategias de ONIA · entrega para revisión

Estado actualizado: [integración local con el panel](INTEGRACION-PANEL-20261111.md); evidencia anterior conservada. Despliegue y teléfono pendientes.

11 noviembre 2026 · v1. Encargo `guiones-tanda-estrategias-20261111`, base `aeb116090aed97763fa3be050f514bdea8aadde1`. Paquete comercial preparado; revisión independiente, editorial y autorización comercial pendientes. No es otro registro del harness.

Empezá por [la estrategia del workshop](ESTRATEGIA-WORKSHOP-v1.md), seguí con [los guiones, VSL, anuncios y mensajes](PIEZAS-v1.md) y revisá las dependencias antes de usar una pieza. [Biblioteca](BIBLIOTECA-v1.md) y [plantilla](PLANTILLA.md) sirven para evaluar futuros proyectos sin iniciarlos.

| Archivo | Uso |
|---|---|
| [export-estrategias-v1.json](export-estrategias-v1.json) | Datos de oferta, escenarios, acciones, piezas, biblioteca y corrección versionada |
| [estrategias.schema.json](estrategias.schema.json) | Esquema comprobable del export |
| [estado-fabrica.json](estado-fabrica.json) | Resumen con la forma de `onia-fabrica-estado-v1`; productor nuevo, incorporación pendiente |
| [CONTRATO.md](CONTRATO.md) | Consumo, versiones, desconocidos y límites del panel actual |
| [FUENTES.md](FUENTES.md) y [fuentes.json](fuentes.json) | Pasajes usados y huellas de las fuentes locales |
| [comprobar.py](comprobar.py) | Validación offline, escenarios, referencias y casos negativos en memoria |
| [evidencia/comprobaciones.json](evidencia/comprobaciones.json) | Salida real fechada del comprobador |
| [RECIBO.md](RECIBO.md) | Comandos, resultado, modelo/cuota desconocidos y pendientes |

Desde la raíz del checkout:

```bash
python3 -B _investigacion-onia/base-operativa/01-negocio/estrategias-operativas-20261111/comprobar.py
git diff --check
```

El comprobador imprime JSON y no modifica fuentes, exports, harness ni panel. Requiere Python 3.11+ y el módulo `jsonschema` ya disponible en esta sesión; no instala nada. Los hashes detectan cambios, no aprueban el contenido.

Próxima acción de Sergio/Contenido: revisar P01–P05 y VSL01, ensayar voz y caso, completar requisitos/activos privados y revisar el recorrido NEGOCIO con autorización aplicable. Coordinación obtiene el dictamen independiente del commit publicado e integra si corresponde. La escribiente del panel incorpora el productor según el contrato; este paquete no demuestra su visualización en teléfono.

# Procedimiento local de tanda editorial

Entrada concreta → selección del cerebro → redacción → validación → revisión/corrección → nueva salida. Python 3.10+, biblioteca estándar, sin instalación. El programa no invoca un modelo, busca noticias, publica ni programa ejecuciones. La selección y la voz de esta entrega las escribió el LLM de la sesión; Contenido/Sergio todavía deben revisarlas.

El ensayo entregado es [tanda v3](../salida/guiones-tanda-20261111-v3/README.md), versión editorial **r2**, cinco ideas con adaptación vertical y horizontal de cada una. La v2 y el cerebro se leen y cotejan por hash; no se reescriben. Se conserva el contrato `datos-guiones-no-snapshot-canonico` del panel. `estado-fabrica.json` es un resumen descriptivo, sin autoridad sobre el harness.

## Entradas y responsabilidades

| Entrada | Contenido | Quién la prepara |
|---|---|---|
| `entradas/brief.json` | Fecha, oferta vigente, canal no probado, hipótesis, ideas candidatas y entrada requerida para relato real | Operador con decisiones de Sergio |
| `entradas/fuentes.json` | Fuente local/primaria, fecha de consulta con zona, localizador, límites y hash local o fecha del anuncio | Operador/LLM con herramientas de lectura |
| `entradas/redaccion-r1.json` | Cinco guiones completos, propósito, CTA, criterio y ambas adaptaciones; patrones por ID | LLM disponible en sesión o redactor con el esquema declarado |
| `entradas/correcciones-r2.json` | Huella de entrada exacta, versión base/nueva, regla C01, campos, texto anterior/nuevo y motivo | Corrección propuesta por el productor; pendiente de revisión editorial |

Esta implementación admite `autor.modo=LLM_en_sesion`: no oculta quién escribió el ejemplo. Una entrada humana futura requiere revisar ese campo/contrato antes de usarlo; no se anuncia hoy un redactor alternativo integrado.

`generar.py` hace lo fijo: valida esquema/campos, cinco IDs en orden y mezcla, oferta/horarios vigentes, referencias, integridad del cerebro y fuentes locales, fecha de noticia, coincidencia literal de CTA en voz/copy, duplicados normalizados de idea/locución, corrección con precondiciones, variantes completas, estimación por palabras y exportación. No certifica verdad, tono, originalidad semántica, suficiencia de las pruebas ni atención real del CTA. Eso lo revisan personas.

## Invocación

Desde la raíz del repo:

```bash
A=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/automatizada
O=_investigacion-onia/base-operativa/05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v3
python3 -B "$A/generar.py" \
  --brief "$A/entradas/brief.json" --fuentes "$A/entradas/fuentes.json" \
  --redaccion "$A/entradas/redaccion-r1.json" \
  --correcciones "$A/entradas/correcciones-r2.json" \
  --salida "$O/ensayo-manual-r2"
```

Es una reproducción local de la misma tanda, no la siguiente tanda autorizada. El destino debe ser nuevo y estar dentro de v3. Para producir r1 sin corrección, omitir `--correcciones` y usar otro destino nuevo como `$O/ensayo-manual-r1`. La raíz `$O` ya está entregada: invocarla nuevamente devuelve código **2**, «Salida duplicada», sin pisarla. No hay `--force`. Los ensayos manuales conservan su salida; las pruebas usan temporales propios y retiran sólo esos temporales.

Salida correcta: código 0 y JSON con ruta, versión, cinco piezas y número de cambios. Entrada inválida/destino existente: código 2 y motivo en stderr. Se valida y renderiza antes de reservar el destino. La reserva exclusiva impide que dos invocaciones pisen el mismo destino. Un corte de E/S durante el traslado puede dejar una carpeta incompleta visible: conservarla, revisar el error y usar una salida nueva; no afirmar transacción resistente a cortes.

La aplicación de correcciones no llama al LLM: sustituye texto sólo si la entrada coincide con `entrada_sha256`, la versión coincide y el texto anterior aparece exactamente una vez en cada campo. La huella de entrada es SHA-256 de `json.dumps(entrada, ensure_ascii=False, sort_keys=True).encode()`. Se guarda cada campo cambiado con su huella antes/después. C01 se aplica a T01 y T04: invitación coherente sin prometer una respuesta personal desde un canal sin probar. Eso no habilita publicación.

## Comprobación reproducible

```bash
python3 -B -m unittest discover -s "$A" -p 'test_*.py' -v
python3 -B "$A/comprobar.py" --salida "$A/evidencia/repeticion-local-01"
```

El segundo comando también ejecuta las pruebas, crea r1/r2 temporales dentro de v3, comprueba que r1 no cambió, reproduce los cinco Markdown entregados y ejecuta los tres rechazos por el CLI real. Guarda un recibo nuevo y el log; si ese recibo ya existe, elegir otro nombre. La evidencia de esta sesión está en [ensayo-v1](evidencia/ensayo-v1/resultado.json). No se crean tareas, sesiones de agentes ni servicios.

La compatibilidad usa **las funciones reales sin modificar** `tanda.snapshot(path)` y `panel.render(snapshot)`. El CLI de `tanda.py` sólo permite escribir en la ruta de la sesión del panel, ajena a este encargo; aquí se ejercita su lectura y su render en memoria, sin cambiar esa restricción. El adaptador fija `version='tanda v2'` y no proyecta fuentes/calendario como secciones propias: las conserva accesibles en Markdown/archivos de la tanda. Para la versión real consultar `version_editorial=r2` y el encabezado del guion. No se presenta esta limitación como integración de UI resuelta.

## Repetir el método editorial

1. Leer decisiones vigentes y mantener las condiciones estructuradas de la oferta. Seleccionar sólo fuentes pertinentes del cerebro, sin repetir ASR/capturas. `seleccion.json` conserva patrón, pieza pública, pasaje, límites y motivo por guion. Las ideas descartadas/reserva quedan en el brief.
2. Investigar una noticia con primaria y fecha del hecho/publicación/consulta. Esta tanda usa un anuncio del **10-nov**, no del 11, leído en `claude.com`. Disponibilidad propia no comprobada. El anuncio de búsqueda web de marzo de 2025 se descartó por antigüedad. La lista de dominios primarios del validador está acotada a Anthropic/Claude para este ensayo, no a cualquier noticia IA.
3. Sin fuente noticiosa utilizable, el LLM/operador debe proporcionar T03 `slot=evergreen`, explicar `motivo_evergreen`, cambiar voz/copy/fuentes y rotularlo. El programa **no transforma automáticamente una noticia en evergreen**. La prueba offline acredita aceptación del caso explícito y rechazo de evergreen sin motivo. No ampliar una búsqueda general para llenar el slot.
4. Con un LLM realmente disponible, usar el [pedido de redacción](PROMPT-REDACCION.md), las fuentes y el esquema completo del ejemplo. Hacer cinco piezas con propósito, una acción y dos adaptaciones por pieza; validar y revisar antes de generar correcciones. Sin modelo/redactor disponible se detiene la escritura nueva. Después del 14 sólo se puede repetir trabajo fijo ya aportado y verificado con un operador; no hay promesa de creatividad, noticias o autoscheduler.
5. Contenido revisa la voz y las afirmaciones; Sergio ensaya y decide. Conservar corrección y versiones nuevas, repetir controles y parar para revisión. Las reglas guardadas son memoria editorial, **no entrenamiento de pesos**. Las personas/crítico son hipótesis del mismo productor, no entrevistas ni revisión independiente.

No hay aprobación para usar un canal comercial por superar tests. NEGOCIO requiere prueba propia del recorrido; el QR, clientes y Meet privados permanecen fuera de esta entrega. El calendario es una propuesta sin horas de publicación, con tres inicios de clase y sin hora final inventada. El vlog queda excluido.

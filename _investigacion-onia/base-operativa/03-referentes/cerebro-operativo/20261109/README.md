# Cerebro editorial consultable

Selección documental del 9 de noviembre de 2026. El catálogo representa los 19 referentes con 23 patrones y 23 piezas concretas. La cobertura aceptada de origen suma 79 piezas, A26, B25 y C28. Esta entrega recupera pasajes de esa investigación. La selección prioriza A y Erik para negocio y workshop. Los criterios y las etiquetas fueron elegidos manualmente en este encargo. [Catálogo](catalogo.json) · [Cierre aceptado de A/B/C](../../../04-operacion-agentes/evidencias/cerebros-profundos-20261108/CIERRE-RETOMAS.md)

Las aplicaciones y reglas OnIA son propuestas revisables. Boss conserva la síntesis final entre grupos y Sergio decide su adopción. La guía reutiliza la propuesta y matriz del lote nocturno para preparar ejercicios, ideas y guiones. Su ensayo humano sigue pendiente. [Guía aplicada](GUIA-APLICADA.md) · [Síntesis precedente](../../../01-negocio/workshop-20261108/noche-20261109/SINTESIS-PROPUESTA.md) · [Matriz precedente](../../../01-negocio/workshop-20261108/noche-20261109/FUENTES-Y-MATRIZ.md)

## Uso exacto

Python 3.10 o superior, biblioteca estándar. Ejecutar desde la raíz del repositorio. El script también funciona desde otro directorio si se invoca mediante su ruta absoluta. Sus fuentes se resuelven desde su ubicación dentro de la base operativa.

```bash
C=_investigacion-onia/base-operativa/03-referentes/cerebro-operativo/20261109
python3 "$C/consultar.py" validar
python3 "$C/consultar.py" etiquetas
python3 "$C/consultar.py" consultar --tema oferta --uso vender
python3 "$C/consultar.py" consultar --tema agenda --uso workshop --formato json
python3 "$C/consultar.py" consultar --tema revision --uso enseñar
python3 "$C/consultar.py" consultar --tema contenido --uso guiones
python3 "$C/consultar.py" consultar --tema tributacion --uso workshop --formato json
```

`consultar` sin filtros recupera los 23 patrones. `--tema` y `--uso` admiten repeticiones. Los temas se combinan con OR, los usos con OR y ambos grupos con AND. Mayúsculas, tildes y espacios exteriores se normalizan. El emparejamiento exige la etiqueta completa. Por ejemplo, `ventas` carece de equivalencia automática con `oferta`. Un tema desconocido produce una lista vacía con código 0. Una etiqueta vacía, un uso ajeno al vocabulario o un catálogo inválido producen código 2. Se puede elegir otro archivo mediante `--catalogo RUTA` antes del subcomando.

Cada resultado incluye hecho documentado, inferencia acotada, aplicación propuesta OnIA y comprobación pendiente. Incluye además pieza pública exacta, modalidad de cobertura, localización temporal, pasajes de ficha, límites específicos y entrega aceptada de origen. Markdown produce enlaces locales absolutos al checkout actual. JSON conserva las rutas relativas a base-operativa y las líneas de los pasajes.

## Selección trazable

La cantidad heredada describe el corpus aceptado por referente. La columna de selección enumera las piezas efectivamente recuperables en este catálogo. Cada ficha conserva el desarrollo y sus fuentes públicas, también presentes en `piezas_seleccionadas` del JSON.

| Grupo | Ficha aceptada | Piezas heredadas | Selección | Patrón recuperable |
|---|---|---:|---|---|
| A | [Alex Hormozi](../../cerebros-profundos/a/alex-hormozi.md) | 4 | P1, P2 | Primer avance y correspondencia entre promesa y entrega |
| A | [Pedro Buerbaum](../../cerebros-profundos/a/pedro-buerbaum.md) | 4 | P1, P3 | Oferta específica y dependencia del dueño |
| A | [Víctor Heras](../../cerebros-profundos/a/victor-heras.md) | 4 | P1 | Atención, mecanismo y acción comercial |
| A | [Iman Gadzhi](../../cerebros-profundos/a/iman-gadzhi.md) | 6 | P1 | Tesis, consecuencia y ejemplo útil |
| A | [Justin Welsh](../../cerebros-profundos/a/justin-welsh.md) | 4 | P4 | Publicación y siguiente destino comprensible |
| A | [Alex Carrera](../../cerebros-profundos/a/alex-carrera.md) | 4 | P2 | Problema y secuencia con artefactos |
| B | [Erik Taveras](../../cerebros-profundos/b/erik-taveras.md) | 5 | P1, P2, P4 | Orientación, preguntas y casos por función |
| B | [Enrique Rocha](../../cerebros-profundos/b/enrique-rocha.md) | 4 | P1 | Resultado, iteración y condiciones |
| B | [Ali Abdaal](../../cerebros-profundos/b/ali-abdaal.md) | 4 | P1 | Hitos visibles de progreso |
| B | [San Muñoz](../../cerebros-profundos/b/san-munoz.md) | 4 | P1 | Comparación sobre una entrada común |
| B | [Cormac Hayden](../../cerebros-profundos/b/cormac-hayden.md) | 4 | P1 | Pregunta y mecanismo concreto |
| B | [Bastian Xu](../../cerebros-profundos/b/bastian-xu.md) | 4 | P1 | Secuencia de producción y herramientas por etapa |
| C | [Gonzalo Teba](../../cerebros-profundos/c/gonzalo-teba.md) | 4 | P1 | Conducta cotidiana y repetición |
| C | [Beltrán Briones](../../cerebros-profundos/c/beltran-briones.md) | 4 | P1 | Enumeración y recapitulación |
| C | [Toto Artuso](../../cerebros-profundos/c/toto-artuso.md) | 4 | P1 | Problema vivido y decisión |
| C | [Nick Bare](../../cerebros-profundos/c/nick-bare.md) | 4 | P1 | Agenda, incidente y revisión |
| C | [Jeff Nippard](../../cerebros-profundos/c/jeff-nippard.md) | 4 | P2 | Acción, motivo y ajuste |
| C | [Álvaro Risoglio](../../cerebros-profundos/c/alvaro-risoglio.md) | 4 | P1 | Modificación comercial y restricción |
| C | [Voltra](../../cerebros-profundos/c/voltra.md) | 4 | P1 | Demostración, destino y condiciones |

## Integridad y límites

`validar` coteja 28 archivos locales mediante SHA-256, los 19 integrantes A6/B6/C7, cantidades contra COBERTURA, piezas completas y URLs exactas contra las fichas, líneas y huellas de pasajes, relación pasaje–pieza y commits de entrega contra el cierre aceptado. Conserva `faltantes` tal como aparece en COBERTURA. En B ese campo está vacío, por lo que se añaden por separado límites extraídos de los pasajes de ficha. Una fuente faltante o alterada detiene la consulta con código 2, incluso si el filtro habría dado cero resultados.

El hash acredita bytes y los controles estructurales acreditan referencias. La correspondencia interpretativa entre paráfrasis y fuente requiere lectura editorial. Cuando una ficha cambia, hay que revisar su selección y pasajes antes de actualizar el catálogo y sus huellas.

- La lectura de esta entrega fue documental. ASR, captions, cuadros y storyboards pertenecen a las investigaciones previas. Cada pieza conserva su modalidad y reloj.
- La escucha, prosodia, música, mezcla, percepción visual continua y sincronía fina conservan los límites de cada ficha. Un ASR vacío deja el contenido sonoro desconocido.
- Justin P2–P4 comparten conversación. Jeff P2–P4 comparten serie. Heras P1 A/B cuenta una pieza. Los cuatro creativos de Voltra corresponden a un producto. Bastian reutiliza un cierre en piezas con cuerpos distintos. Iman tiene origen común de grabación sin determinar. Estas dependencias acompañan las consultas pertinentes.
- Las publicaciones de Beltrán tienen atribución editorial colaborativa y voz personal sin autenticar. Álvaro P4 tiene publicador empresarial asociado. Los diálogos de entrevistas conservan los límites de atribución por turnos.
- Las rutas temporales de medios y ASR se conservan como procedencia heredada. La consulta depende de las fichas versionadas y sus pasajes. La disponibilidad de esos temporales entre máquinas queda sin garantizar.
- Las URLs son fuentes públicas históricas. La consulta funciona offline mediante filtros deterministas de etiquetas. Capacidades, precios, accesibilidad actual y declaraciones comerciales exigen comprobación propia cuando se incorporen a una pieza nueva.
- Los CTA públicos acreditan invitaciones. Entrega por privado, aprendizaje, resultados comerciales y pagos conservan su estado de observación declarado en las fichas.

## Comprobación reproducible

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover \
  -s _investigacion-onia/base-operativa/03-referentes/cerebro-operativo/20261109 \
  -p 'test_*.py' -v
```

La suite usa la entrada CLI real desde `/tmp`, con casos útiles, vacíos, inválidos y fallos de integridad inducidos en copias del catálogo. Conserva sus fixtures en `/tmp/cerebro-consultable-pruebas-*`. El informe registra comandos, resultados, el fallo encontrado y la corrección. [Comprobaciones](COMPROBACIONES.md)

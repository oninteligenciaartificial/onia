# Bastian Xu · Content Project / Xu Films

Consulta: **8 de noviembre de 2026, UTC**. Corpus de cuatro audiovisuales públicos distintos, más páginas comerciales separadas. **Estado: cobertura textual selectiva de P1 y visual de P2–P4; cuatro fichas completas dentro de esos alcances.** No acredita escucha, visionado continuo, resultados comerciales ni acceso al programa. `completa: true` significa que el contenido primario efectivamente leído permite contestar las cinco preguntas con tiempos; no significa percepción audiovisual integral.

## Identidad, procedencia y límites

- **P1:** [EP17 de Creators Latam](https://www.youtube.com/watch?v=c4S0EJAdL5I), canal `UCuotyZGxIHgotqMewttnJCQ`. Bastian es **invitado**. La descripción primaria conservada en [youtube-metadata.json](../../../99-archivo/recuperacion-secundaria/youtube-metadata.json) enlaza TikTok `@bastianxu` e Instagram `@bastianxuu`. El anfitrión introduce su proceso y formula preguntas; las intervenciones no tienen etiquetas de voz. No se atribuyen frases individuales a Bastian a partir de esos cues. La edición del episodio corresponde a la publicación de Creators Latam, sin prueba de autoría del invitado.
- **P2–P4:** publicación del canal [Bastian Xu / @bastianxu](https://www.youtube.com/@bastianxu), `UCHal_WDNpEZbK1KpeZQUJ5A`, comprobado en `videoDetails.channelId` y en la página del canal. El encabezado enlaza Instagram `@bastian.xu`. La descripción primaria de [Aprende a grabar videos POR TI MISMO](https://www.youtube.com/watch?v=4AJT0P4x56I) enlaza tanto ese Instagram como `https://content-project.com/mi-mapa-cp?utm_source=02.11.26`. Este último destino identifica el método de Bastian Xu y Content Project. Es un puente primario canal→oferta, además de la coincidencia de nombre; no se usa sólo el parecido de un handle.
- **No está demostrado un cambio de usuario `@bastianxuu`→`@bastian.xu`.** La relación histórica de P1 con el referente procede de la presentación explícita del anfitrión, el nombre y los enlaces de su descripción. El canal actual y Content Project tienen su propio puente anterior. No se agregaron publicaciones de un Instagram homónimo por semejanza del nombre.
- Se leyeron la [ficha previa](../../cerebros/bastian-xu.md), sus [fuentes audiovisuales](../../fichas/audiovisual/bastian-alvaro.md) y [comerciales](../../fichas/marketing/bastian-alvaro-voltra-alex.md#bastian-xu). Los datos heredados están identificados; las recuperaciones de Shorts y la nueva página comercial se consultaron en esta tanda.
- Directora aplicada: [preparar-oferta-y-embudo](../../../01-negocio/preparar-oferta-y-embudo/SKILL.md); apoyo [research](../../../05-herramientas/compartibles/terceros/generales/matt-pocock/skills/engineering/research/SKILL.md), sin nueva delegación. Contexto: [decisiones](../../../05-herramientas/2026-11-08-harness/00-decisiones.md) y [plan](../../../05-herramientas/2026-11-08-harness/plan-workshop.md).

## Método de lectura y fuente de los tiempos

**P1:** reutilización de [captions automáticos primarios](../../../99-archivo/recuperacion-secundaria/c4S0EJAdL5I-subtitulos.json) y [texto derivado](../../../99-archivo/recuperacion-secundaria/c4S0EJAdL5I-texto-derivado.txt). Releídos selectivamente los cues de **00:00–01:20; 02:30–03:40; 11:20–12:40; 15:00–17:00; 20:00–20:40; 24:30–25:40; 32:30–33:52.64**. Los tiempos concretos de abajo son `start_s/end_s`, no los capítulos redondeados de la descripción. La fuente completa contiene 1.641 cues y termina en 33:52.64; eso acredita disponibilidad textual, no que se haya escuchado cada palabra. No se volvió a descargar el MP4 de 34 minutos ni se reclamó una nueva inspección de las 134 imágenes heredadas.

**P2–P4:** GET público de `/shorts/ID`, `ytInitialPlayerResponse`, autor/canal/duración y `storyboards.playerStoryboardSpecRenderer.spec`. Se vieron **174 posiciones**: 52 + 55 + 67; se admiten **171 posiciones temporales** tras excluir las tres celdas finales que sobrepasan la duración. Imágenes nativas de **101×180 px, intervalo declarado 1.000 ms**, cuadrículas 3×3. Se revisaron además recortes ampliados del texto central; ampliar no agrega detalle. `fuente_tiempos`: para posición `k`, **t = k × 1.000 ms**, orden por filas y luego por hoja. Los rangos son aproximaciones al segundo; no medición de cortes ni sincronía verbal. La última celda del storyboard no es el último fotograma del video.

| Pieza | `lengthSeconds` | `formats[itag=18].approxDurationMs` | Posiciones admitidas | Celda excluida |
|---|---:|---:|---|---|
| P2 | 51 | 50.965 ms | 00–50 s | 51 s: excede 35 ms |
| P3 | 54 | 53.589 ms | 00–53 s | 54 s: excede 411 ms |
| P4 | 66 | 65.984 ms | 00–65 s | 66 s: excede 16 ms |

`approxDurationMs` también es metadata aproximada; por prudencia no se asigna al interior del video contenido sólo visible en esas tres celdas excluidas.

Procedimiento reproducible: dividir `spec` por `|`; nivel 3 con campos `ancho#alto#cantidad#columnas#filas#intervalo#nombre#firma`; sustituir `$L=3`, `$N=M$M`, `$M=número de hoja` y añadir `sigh` completo. **No se guardan aquí URLs firmadas.** Las hojas temporales son `/tmp/bastian-ID-sbN.jpg` y las vistas `/tmp/bastian-ID-contact.png`; el principal conserva la evidencia pertinente para revisión. La recuperación de captions de estos tres Shorts respondió **HTTP 200 con cero bytes**; un GET acotado del stream devolvió **403**. No se reconstruyó narración desde títulos, snippets ni resúmenes ajenos.

## P1 · Producción efectiva de videos para TikTok

- **URL / título:** [EP17. – Producción Efectiva de Videos para TikTok – Bastian Xu – Concept Studio Podcast](https://www.youtube.com/watch?v=c4S0EJAdL5I).
- **Autor de publicación:** Creators Latam; invitado Bastian Xu. Publicación 09/07/2023 según metadata conservada. Consulta 08/11/2026.
- **Tipo:** `video` / entrevista. **completa: true**, análisis textual selectivo del episodio, sin atribución automática de voces. `fuente_tiempos`: cues JSON anteriores.

1. **Idea principal — HECHO REFERENTE:** relacionar audiencia, producción y distribución; los consejos aparecen como partes de un proceso. Es contenido del diálogo, no un método entero atribuible exclusivamente al invitado.
2. **Audiencia/problema — INFERENCIA:** profesionales y negocios que publican sin definir comprador; el ejemplo del abogado aparece en **11:19.68–11:27.67**.
3. **Apertura / desarrollo / cierre — HECHO REFERENTE:** **00:02.45–00:36.31**, anticipo sobre público; **00:42.89–01:19.61**, saludo y encuadre del anfitrión. **02:57.96–03:30.23**, demostrar una capacidad mediante contenido; **16:35.16–16:58.25**, ideas→selección→guion→día de grabación; **24:58.44–25:27.83**, herramientas asociadas a etapas. **33:41.00–33:52.64**, agradecimiento y despedida. La placa visual final sólo consta en la ficha heredada.
4. **Técnica de enseñanza/venta — HECHO REFERENTE e INFERENCIA:** **HECHO REFERENTE:** pregunta concreta→respuesta con secuencia. **INFERENCIA:** la explicación aporta valor y también hace visible un servicio; no se observó compra ni cierre. No se convierten las cifras declaradas de seguidores en prueba de eficacia.
5. **Qué tomar — PROPUESTA ONIA:** para clase 1, una secuencia visible antes de introducir herramientas; clase 2, definir a quién se dirige la oferta; clase 3, explicar qué etapa se automatizaría. Son adaptaciones ONIA, sin trasladar recomendaciones de plataformas de 2023 como reglas actuales.

## P2 · Cinco fotos para dar presencia a Instagram

- **URL / título de metadata:** [7 de noviembre de 2026](https://www.youtube.com/shorts/GvwKsszNf6g). **Título visible en el contenido:** «5 fotos que le darán más presencia a tu Instagram».
- **Autor de publicación:** Bastian Xu, canal actual comprobado arriba; fecha primaria 07/11/2026. Consulta 08/11/2026.
- **Tipo:** `reel` publicado como Short. **completa: true**, cobertura visual 51 posiciones admitidas, 00–50 s; celda nominal 51 s excluida. `fuente_tiempos`: storyboard nivel 3, 1 Hz.

1. **Idea principal — HECHO REFERENTE:** usar ejemplos de fotografías para construir presencia; se ve una colección de situaciones, no sólo un titular.
2. **Audiencia/problema — INFERENCIA:** inferencia: profesionales que quieren mostrar trabajo, relaciones y actividad en su perfil. No se ve segmentación explícita para pequeños negocios de Santa Cruz.
3. **Apertura / desarrollo / cierre — HECHO REFERENTE:** **00–03 s**, promesa de cinco fotos. **04–14**, escenas de trabajo y retratos; **15–17**, reunión; **18–25**, mesa/comida; **26–38**, más reuniones y escena ante público. Son ejemplos visibles, sin reconstruir los nombres exactos de las cinco categorías. **42–50**, rótulo «Bastian» y cierre sobre otros fondos; el texto pequeño no permite transcribir la instrucción completa.
4. **Técnica de enseñanza/venta — HECHO REFERENTE e INFERENCIA:** **HECHO REFERENTE:** presentador recortado sobre referencias de mayor tamaño. **INFERENCIA:** mostrar ejemplos facilita comparar situaciones. La atribución autoral de las fotografías no está comprobada. El cierre dirige atención al nombre del creador; no prueba entrega por DM.
5. **Qué tomar — PROPUESTA ONIA:** clase 2, mostrar fotografías reales del producto, servicio o trabajo antes de pedir una oferta a Claude. Clase 1 puede ordenar ese material; clase 3 podría preparar una lista de tareas. No copiar dinero, auto ni escenarios de estatus como prueba de ventas.

## P3 · Cinco tipos de recursos

- **URL / título primario:** [5 tipos de recursos](https://www.youtube.com/shorts/etwFdjwYT6U). La promesa visible agrega ganar más dinero, sin resultado auditado.
- **Autor de publicación:** Bastian Xu, mismo `channelId`; publicado 04/11/2026. Consulta 08/11/2026.
- **Tipo:** `reel` publicado como Short. **completa: true**, cobertura visual 54 posiciones admitidas, 00–53 s; celda nominal 54 s excluida. `fuente_tiempos`: storyboard nivel 3, 1 Hz.

1. **Idea principal — HECHO REFERENTE:** hacer tangible el conocimiento mediante recursos. Hay documentos, pantalla y conversación como ejemplos reales del montaje; no se obtuvo ninguno de esos recursos.
2. **Audiencia/problema — INFERENCIA:** inferencia: quien enseña o presta servicios y necesita convertir conocimiento en algo utilizable. La promesa monetaria es comercial, no causalidad demostrada.
3. **Apertura / desarrollo / cierre — HECHO REFERENTE:** **00–04**, número y promesa. **05–11**, documentos y cuaderno; **12–13**, hoja titulada «HOJA DE DESGLOSE DE GUION»; **14–15**, «LISTA DE PRECIOS»; **16–19**, ejemplo titulado «Estilo minimalista». **20–34**, grabación/edición y pantallas; **35–36**, chat con rótulo de conocimiento personalizado. No se lee el interior de esos documentos. **45–53**, rótulo «Bastian» y cierre compartido con P2.
4. **Técnica de enseñanza/venta — HECHO REFERENTE e INFERENCIA:** **HECHO REFERENTE:** muestra la forma del entregable junto al presentador. **INFERENCIA:** eso puede reducir abstracción; no demuestra calidad ni rentabilidad del recurso.
5. **Qué tomar — PROPUESTA ONIA:** clase 1, una tabla de tareas legible; clase 2, una oferta o lista de precios; clase 3, mostrar qué campos pasarían al siguiente paso. Se toma la concreción del recurso, sin afirmar acceso al contenido pequeño de las plantillas.

## P4 · Habilidades y contenido orgánico

- **URL / título de metadata:** [7 de noviembre de 2026](https://www.youtube.com/shorts/XxWuLNo5dOs). Título descriptivo de esta ficha: habilidades y contenido orgánico; **no es título editorial del autor**.
- **Autor de publicación:** Bastian Xu, mismo `channelId`; publicado 07/11/2026. Consulta 08/11/2026.
- **Tipo:** `reel` publicado como Short. **completa: true**, cobertura visual 66 posiciones admitidas, 00–65 s; celda nominal 66 s excluida. `fuente_tiempos`: storyboard nivel 3, 1 Hz. No se reconstruye su lista completa de habilidades.

1. **Idea principal — HECHO REFERENTE:** relacionar aprendizaje de habilidades con producción de contenido. Además del titular, hay rótulos numerados, escenas de conversación, explicación ante pizarra y trabajo en ordenador.
2. **Audiencia/problema — INFERENCIA:** inferencia: creadores o profesionales que buscan desarrollar presencia. **01–02 s** muestra «200.000» junto a una captura de perfil; no se certifica el número ni cómo se obtuvo.
3. **Apertura / desarrollo / cierre — HECHO REFERENTE:** **00–07**, cifra y teléfono; **08–12**, «Número 1», «Social skills» y conversación; **18–21**, explicación ante pizarra; **25–31**, exposición y reunión; **37–40**, demostración ante otra pizarra; **43–45**, nuevo rótulo numerado y texto «contenido orgánico»; **47–50**, ordenador y pantalla de contenidos. **64–65**, regreso al presentador y gesto apuntando hacia abajo. La celda nominal **66 s** muestra «Comenta “Bastian”», pero queda fuera de la duración aproximada y **no se admite como CTA temporal probado dentro del video**.
4. **Técnica de enseñanza/venta — HECHO REFERENTE e INFERENCIA:** **HECHO REFERENTE:** presenta rótulos enumerados y escenas de trabajo. **INFERENCIA:** la cifra funciona como reclamo; la acción verbal exacta del cierre queda sin confirmar en las posiciones admitidas. No se infiere seguimiento automatizado ni conversión.
5. **Qué tomar — PROPUESTA ONIA:** clase 2, acompañar cada recomendación con un ejemplo; clase 1, mostrar qué hace Sergio en la pantalla; clase 3, distinguir demostración de automatización operativa. No copiar cifras ni prometer crecimiento de seguidores.

## Página comercial / formación, aparte de los cuatro audiovisuales

**Lectura pública nueva:** `https://content-project.com/mi-mapa-cp` respondió **200**, enlazada por el video del canal. Identifica a Bastian Xu y Content Project. Presenta tres misiones: darse a conocer, conectar y vender; ofrece un mapa personalizado y consultoría individual. Promete producir contenido mensual en tres días y usa cinco cupos como escasez. Declara cifras de seguidores e ingresos: son afirmaciones del vendedor, no auditoría. CTA «Agendar Consultoría». **No se agendó ni se enviaron datos; precio, contrato, cobro y entrega posterior sin comprobar.** El título HTML incluye «demo animaciones»: no se deduce que todas las condiciones visibles sean una oferta contratada vigente. No contiene una clase leída que se pueda sumar al corpus.

**Ruta histórica reconsultada:** [Linktree](https://linktr.ee/bastianxu) sigue presentando el enlace MasterClass hacia `xufilms.net/contentproject/`; apertura web fallida, sin recuperación de su clase. [web.content-project.com](https://web.content-project.com/) sigue accesible: masterclass gratuita, segmento de servicios/agencias/coaches, formulario y fecha «18 AGO, 7 PM» sin año/zona confirmados. Captura contacto y promete auditoría en vivo; no es una clase observada. El [perfil público Skool](https://www.skool.com/@bastian-xu-5462) identifica Content Project como creado por Bastian; «Free» no establece el precio de toda la consultoría. No hubo registro.

## Patrón observado y límite de muestra

**HECHO REFERENTE:** en **P2 y P3** el cuerpo muestra referencias mientras el presentador se superpone; el cierre reutiliza el nombre «Bastian» y varios fondos. **P4** agrega rótulos numerados y escenas de trabajo; su instrucción exacta de comentario tiene el límite temporal anterior. **INFERENCIA:** esa combinación puede ofrecer utilidad breve, hacer tangible el formato y dirigir atención al creador. **HECHO REFERENTE:** **P1** aporta un diálogo anterior, producido por otro canal, con preguntas y respuestas; no acredita que Bastian use ese montaje en sus piezas.

P2 y P3 **no son dos crossposts de una misma pieza**: los primeros 38–40 s muestran temas y cuerpos distintos —fotos frente a recursos—; el cierre común se reconoce como material reutilizado y no se trata como dos pruebas independientes de entrega. P4 tiene otro cuerpo y estructura. No se generaliza a todo el perfil, no se valida el rendimiento del contenido y no se atribuyen al autor los materiales de apoyo ajenos. La muestra permite estudiar presentación y recorrido público, con menos detalle sobre las palabras de los Shorts.

## Tres aplicaciones ONIA, separadas de los hechos

1. **Clase 1 / ordenar con Claude. HECHO REFERENTE — P3, 12–19 s:** muestra documentos reconocibles. **INFERENCIA:** ver el entregable puede hacer más concreta la explicación. **PROPUESTA ONIA:** usar una tabla ampliada de tareas de un pequeño negocio de Santa Cruz como ejemplo visual del resultado; Sergio debe poder explicar qué información aportó y qué corrigió. No es un guion de clase ni promete ahorro todavía medido.
2. **Clase 2 / vender. HECHO REFERENTE — P2, 04–38 s:** ejemplifica presencia con escenas de actividad. **INFERENCIA:** los ejemplos propios pueden aportar contexto al redactar una oferta. **PROPUESTA ONIA:** trabajar con foto real de producto/servicio y datos comprobados de un negocio local; contrastar una oferta genérica con una descripción concreta. Sin importar cifras, testimonios o escenas de riqueza del referente.
3. **Clase 3 / automatizar. HECHO REFERENTE — P1, 16:35.16–16:58.25 y 24:58.44–25:27.83:** el diálogo ordena actividades y asocia herramientas a etapas. **INFERENCIA:** conviene explicar el proceso antes de automatizar un paso. **PROPUESTA ONIA:** representar entrada→preparación→revisión→salida y señalar un paso candidato para demostración. No activa n8n ni promete seguimiento real; esa demo sigue siendo propuesta según decisiones.

Marco comercial común: dueños de pequeños negocios de **Santa Cruz**, tres clases **ordenar / vender / automatizar**, clase 1 con **Claude**, **Bs 50 grupal aprobado**. **VIP Bs 150 sólo propuesto**, no condición de venta aprobada. Las propuestas anteriores no producen las clases, ni sustituyen el piloto de diez minutos y la revisión de Sergio.

## Intentos, barreras y próximos pasos exactos

Intentos del **08/11/2026**. Las búsquedas `"Bastian Xu" youtube`, `"bastianxu" video`, `"Bastian Xu" Content Project masterclass`, búsquedas por `watch/shorts`, y alternativas por nombre devolvieron sobre todo páginas comerciales, secundarios y homónimos. Glarity, VideoHighlight y artículos se descartaron como base del análisis audiovisual. La recuperación útil provino del **canal primario y su pestaña Shorts**, no de aceptar esos resúmenes.

| Intento público | Resultado y decisión |
|---|---|
| Canal `@bastianxu`, pestaña Shorts y GET de P2–P4 | HTML 200; player `OK`; storyboards JPEG 200. Cuatro piezas aceptables incluyendo P1, con los alcances declarados. |
| Largos `7cTKZjncnCU`, `Eat6eFv82l4`, `4AJT0P4x56I`, y detrás de cámaras `i9E302JPxqc` | `LOGIN_REQUIRED`; metadata/descripción útil para identidad en el tercero, sin contenido primario suficiente para sumar piezas. No se inició sesión. |
| Captions P2–P4 y streams acotados | 200 vacío / 403 respectivamente. La presencia de pistas no acredita contenido leído. Próximo paso si se exige semántica verbal completa: transcript público del autor/host o subtítulos disponibles, no otro intento idéntico ni ASR pesado. |
| `qv-faCWk14I`, `roVIF_Bsc4E` | Storyboards recuperados, planos de presentador y texto demasiado pequeño para desarrollar su argumento. **No cuentan como completas**. |
| `hg3aETSek5w`, `xC2u8OLxO5o` | Storyboards recuperados de otras listas; no se necesitó ampliar el corpus. No se usan titulares ni imágenes genéricas para afirmar sus diez consejos completos. |
| TikTok `@bastianxu`, Instagram `@bastianxuu`/`@bastian.xu` | TikTok devolvió HTML de perfil sin texto de piezas suficiente; Instagram sin contenido público utilizable en esta lectura. Ninguno se suma al conteo. |
| Página nueva Content Project / alternativa histórica | GET público 200 en ambas; oferta examinada aparte, sin registro, compra ni contabilización como video. XuFilms inaccesible por lector web. |

Comprobación: cuatro IDs distintos, cinco respuestas y fuente temporal por pieza; atribución host/invitado conservada; no curso/landing contado como audiovisual; tres aplicaciones etiquetadas y decisiones vigentes cotejadas. No se ejecutaron modelos de audio, instalaciones, compras, cuentas ni mutaciones externas. **Sólo se escribió esta ficha; Git e integración corresponden al principal.**

Modelo observado: **null**; esfuerzo observado: **null**. El encargo pide Sol 6.1 / high, pero esta interfaz no aporta una identificación efectiva verificable que autorice declararlos observados.

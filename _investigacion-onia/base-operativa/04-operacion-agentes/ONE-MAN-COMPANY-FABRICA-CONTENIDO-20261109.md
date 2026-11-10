# One man company de OnIA y fábrica de contenido

9 noviembre 2026 · ~18:55 America/La_Paz · pedido de Sergio: investigar el término, tomar como definición los dos videos de Euge, y dejar fija la fábrica de contenido para generar ventas. Ola actual: el workshop. No se publica, no se gasta y no se activa n8n por este archivo.

## Cómo leer este archivo

Este documento es la **fuente única del modelo** one man company de OnIA: qué significa, cómo se traduce lo que enseña Euge, quién hace qué en la fábrica de contenido, cómo se llega a **al menos cinco videos al día** y cómo se planifica (sin ejecutarlo aquí) el análisis de las cuentas de la marca personal y del vlog.

Para que los agentes no se contradigan:

| Pregunta | Fuente que manda |
| --- | --- |
| ¿Qué es el one man company de OnIA y cómo es la fábrica de contenido? | Este archivo. |
| ¿Cómo se parten Boss y Codex, qué es un PEDIDO y dónde viven los estados? | [Reparto aprobado](REPARTO-CODEX-GROKBOT-20261109.md) y el resumen vigente [OPERACION-AGENTS-VIGENTE.md](OPERACION-AGENTS-VIGENTE.md). Este archivo los aplica, no los cambia. |
| ¿Cómo se abre un frente, qué es una tarea, cuántas sesiones hay y quién revisa? | [EMPRESA-UNIPERSONAL.md](EMPRESA-UNIPERSONAL.md) y [ORQUESTACION.md](ORQUESTACION.md). Este archivo no los reemplaza ni los edita. |

Lecturas de apoyo, no fuentes del modelo: [EUGE-VIDEO-BOSS-20261109.md](EUGE-VIDEO-BOSS-20261109.md), [EUGE-VIDEO2-BOSS-20261109.md](EUGE-VIDEO2-BOSS-20261109.md), [PROPUESTA-JEFE-CODEX-20261109.md](PROPUESTA-JEFE-CODEX-20261109.md). Si alguna frase vieja choca con este archivo o con el reparto aprobado, ganan estos dos.

No se crea un agente Grok nuevo. El compañero **Contenido** es el dueño editorial de la fábrica de contenido. Boss sigue siendo el capataz. Codex no es el dueño de contenido.

## Relación con EMPRESA-UNIPERSONAL.md

[EMPRESA-UNIPERSONAL.md](EMPRESA-UNIPERSONAL.md) (8 nov 2026) ya describe cómo operar OnIA con una persona y sesiones por tarea. Es el mismo objetivo de negocio (una sola persona al mando, agentes que producen, revisión y evidencia en GitHub). No se edita en este commit.

Lo que ese archivo ya fijó y este respeta:

- Sergio decide objetivo, prioridades, compromisos y efectos externos.
- Boss coordina el negocio y prepara encargos; Codex coordina la ejecución técnica, usa el harness y publica evidencia.
- Un área es una responsabilidad estable, no un bot que tenga que estar vivo todo el día.
- El JSON de `tareas/ID.json` es el registro canónico de estados. Un encargo en Markdown es proyección, no otra cola.
- Tope de tres sesiones principales del harness, revisor distinto de quien produjo, y no se promete operación 24/7 ni un scheduler que aún no existe.
- El camino hacia automatización sostenida es por encargos comprobados, no por encender todas las áreas a la vez.

Diferencias explícitas (ampliación del 9 nov, no un sistema paralelo):

| Tema | EMPRESA-UNIPERSONAL (8 nov) | Este archivo (9 nov tarde) |
| --- | --- | --- |
| Nombre | «Empresa unipersonal»: una persona y sesiones por tarea. | «One man company»: el mismo objetivo, dicho con el lenguaje de Euge (capataz + cerebro + fábricas). |
| Contenido | Área del harness marketing/video. Proponía preparar un recorrido y una pieza cada vez. | El compañero Contenido es dueño editorial de la fábrica. La meta de producción pasa a ser **al menos 5 videos al día**, en un lote diario con revisión por pieza. No se crea un área extra ni un bot nuevo. |
| Codex | Coordina ejecución técnica, harness y evidencia. | Igual: pasos pesados (código, ASR en CPU, cortes FFmpeg, homelab) solo con PEDIDO e ID. No es el capataz ni escribe la propuesta comercial. |
| Boss | Coordina el negocio y prepara encargos. | Igual, llamado capataz como el Grok Bot de Euge. Habla con Sergio y reparte. |
| Automatización | No hay scheduler; no se promete 24/7. | Igual. Cinco videos al día es meta de producción con revisión y sí de Sergio para publicar, no el experimento de Euge que sube solo (Leader Summaries). |
| Prioridad | Frentes en secuencia: cuentas, referentes, workshop, ventas/contenido, administración. | Ola actual: vender el workshop con la fábrica de contenido. Lo demás (caja, Binance, startups, negocios físicos con IA) queda anotado y no se lanza aquí. |

El lote diario de cinco piezas cabe en el contrato de tareas: un encargo del harness puede agrupar el lote del día, y cada video conserva su versión, hash, revisión y decisión. Eso amplía el «una pieza cada vez» del 8 nov sin inventar otra cola.

## Qué significa «one man company»

El término se usa de tres modos distintos. OnIA usa el tercero, con la definición concreta de los videos de Euge.

1. **Figura legal.** En la India, una *One Person Company* es una sociedad con un solo miembro, según el artículo 2(62) de la Companies Act, 2013. Eso no describe cómo trabaja OnIA ni autoriza constituir una sociedad. Fuente: [Ministerio de Asuntos Corporativos de la India](https://www.mca.gov.in/content/mca/global/en/help-faq/faqs/company-services/incorporation/one-person-company.html).
2. **Empresa que elige quedarse chica.** Paul Jarvis, en *Company of One* (2019), habla de un negocio deliberadamente pequeño: libertad, sistemas simples y crecimiento cuestionado, no necesariamente «cero empleados más una fábrica de agentes». Fuente: [fichas del libro](https://www.penguin.co.uk/books/312524/company-of-one-by-jarvis-paul/9780241470466).
3. **Una persona que escala con software y agentes de IA.** Desde 2024 circula la apuesta de que la IA permite compañías de una sola persona con salida de un equipo. Sam Altman dijo que en su grupo de CEOs hay una apuesta por el año de la primera compañía de mil millones de dólares con una sola persona; [Fortune lo recogió el 4 de febrero de 2024](https://fortune.com/2024/02/04/sam-altman-one-person-unicorn-silicon-valley-founder-myth/). [Fast Company](https://www.fastcompany.com/91447642/how-close-is-the-first-solopreneur-unicorn) volvió sobre el «solopreneur unicorn». En la práctica, las guías serias repiten la misma regla: un agente, un trabajo; memoria compartida del negocio; ellos borran, vos decidís. Ejemplos: [Bootstrapped Makers](https://bootstrappedmakers.com/blog/run-a-one-person-company-with-ai-agents) y [Full Circle](https://fullcircle.software/blog/one-person-company-ai). Un caso visible de solopreneur (no «unicornio») es Pieter Levels, que publica que construye sus productos solo: [levels.io](https://levels.io/) y, en X, [«No employees / Now with Cursor though AI writes a lot»](https://x.com/levelsio/status/1901915803609432421) (18 mar 2025) y [«I do $1.5M/y with just Photo AI by myself»](https://x.com/levelsio/status/1899947042606375417) (12 mar 2025). Sam Altman, en X: [«the amount one person can do will increase by orders of magnitude»](https://x.com/sama/status/1662759311230083075) (28 may 2023).

Ninguna de esas fuentes reemplaza a Euge para OnIA. Tampoco prueban que OnIA ya funcione así, ni que exista el primer unicornio de una persona.

**Definición que vale para OnIA:** sos el dueño. Hablás con un solo capataz (Boss). El cerebro (contexto) vive en GitHub, no solo en el chat. Las fábricas son cadenas con entrada, pasos, revisión y destino. Contenido conduce la fábrica de contenido. Codex y la PC de casa hacen lo pesado que Grok Bot no hace bien. Nada sensible (publicar, gastar, tocar n8n o producción) avanza sin tu sí. El objetivo de esta ola es vender con marca personal 100% orgánica, no contratar un equipo.

## Lo que definen los dos videos de Euge

Tiempos aproximados de los subtítulos automáticos `es-orig` bajados el 9 nov 2026. No se publica la transcripción completa. Los nombres propios a veces salen deformados (Grockbot, Crocbot, RAC por RAG, OpenCla). La promoción de Clonify, Clonify Studio o Hetzner no es una recomendación ni una autorización de gasto.

### Video 1 · [Así Utilizo los Agentes de IA a Diario](https://www.youtube.com/watch?v=JuAQILH7dkQ) · `JuAQILH7dkQ` · 30:03 · 22 oct 2026

| Tiempo | Qué define |
| --- | --- |
| [0:16](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=16s) | Quiere que salgas con la noción de tener tu propia fábrica de contenido o de código, en un ordenador en la nube, gestionada por un agente. |
| [8:04](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=484s)–[10:57](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=657s) | Generación de agentes proactivos con ordenador propio. Él trabaja con Grok Bot: conectores fáciles y, si no hay MCP, el agente usa el navegador. |
| [11:18](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=678s)–[12:18](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=738s) | Proactividad: el agente avisa (un podcast a las 9, reuniones que se pisan, una idea de negocio). Eso no lo implementa un SSH abierto. |
| [13:05](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=785s)–[13:16](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=796s) | **Capataz:** un agente que dirige a los subagentes. Lo que más sentido tiene es hablar solo con uno. |
| [13:20](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=800s)–[13:32](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=812s) | Rutina diaria: le pide temas para reels y shorts y recibe cinco preguntas para grabar. |
| [13:44](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=824s)–[15:30](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=930s) | 11 aplicaciones conectadas (nombra Gmail, ElevenLabs, Google Calendar). Grok Bot tiene un ordenador virtual (navegador, archivos, pequeñas bases). Eso le da persistencia, distinta de la máquina de fábricas. |
| [16:24](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=984s)–[17:26](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1046s) | **Atomizar:** partir el trabajo hasta el resultado más pequeño que se pueda evaluar (idea, guion, edición, miniatura). Pedir «un video ganador» no funciona. |
| [17:58](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1078s)–[20:21](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1221s) | Grok todavía no le alcanza para editar; para eso usa otro modelo (cita Opus 5.5) en un ordenador persistente más capaz. Hay que pedirle a Grok Bot que ayude a montar esas fábricas. El ordenador del asistente no sustituye esa máquina si hace falta render u otro modelo. |
| [20:32](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1232s)–[23:34](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1414s) | **Fábrica e idea ganadora:** entran materias primas, hay pasos, y un ciclo de medir, aprender y mejorar. Las entradas deben ser las referencias que vos sí usás (videos, TikToks, ideas en X). Filtra candidatos, simula personas de tu público y usa un crítico. Eso filtra hipótesis; no prueba ventas. |
| [23:37](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1417s)–[24:08](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1448s) | Fábrica de código: entra una tarea o un fallo y sale un PR. Dice que lo revisa él, pero Grok Bot le ayuda y lo fusionan entre los dos. |
| [24:08](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1448s)–[26:47](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1607s) | **Sala de montaje / revisión:** ves el proceso, comentás, pedís otra versión. Enseñás con un antes y un después hecho a mano (ejemplo: cortar silencios). El feedback se guarda en el procedimiento de esa cadena. |
| [26:51](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1611s)–[27:10](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1630s) | Llama fábricas a lo que otros llamarían workflows: se ve lo que entra, lo que se fabrica, la revisión y el destino. |
| [27:10](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1630s)–[28:26](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1706s) | Excepción que él mismo marca: Leader Summaries sube solo, sin revisión; dice que tiene pocas visitas. Es un experimento, no una licencia para que OnIA publique sin tu sí. |
| [28:41](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1721s)–[29:20](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1760s) | Las fábricas existen sobre todo para los flujos que Grok Bot todavía no hace bien, porque hacen falta otros modelos. Podrían vivir en tu PC; él las pone en la nube para que también entren los Grok Bot de su equipo. |

### Video 2 · [Dame 25 minutos y nunca volverás a usar la IA igual](https://youtu.be/xPJbP9yZE1I) · `xPJbP9yZE1I` · 26:35 · 8 nov 2026

| Tiempo | Qué define |
| --- | --- |
| [1:21](https://youtu.be/xPJbP9yZE1I?t=81)–[4:00](https://youtu.be/xPJbP9yZE1I?t=240) | El modelo sale con un preentrenamiento fijo. Hablarle no lo reentrena. Si «se acuerda» de vos, eso es memoria inyectada como contexto. Sin contexto, tira solo de lo preentrenado (ejemplo del huevo frito). Llama «cerebro» al modelo que predice tokens. |
| [8:06](https://youtu.be/xPJbP9yZE1I?t=486)–[14:04](https://youtu.be/xPJbP9yZE1I?t=844) | La palanca ya no es el prompt perfecto, sino el contexto: ejemplos que sí funcionaron, historial, avatar, productos, documentos, memoria e instrucciones. Cargar artículos sin relación con el negocio no «entrena» a la IA: hincha el contexto. |
| [14:04](https://youtu.be/xPJbP9yZE1I?t=844)–[16:13](https://youtu.be/xPJbP9yZE1I?t=973) | **Arnés:** un paraguas de contexto encima del modelo (memorias, a veces recuperación tipo RAG, herramientas e instrucciones). Cuanto más simple el arnés ahora, mejor puede trabajar el modelo. Se construye con la propia IA y se guarda en una carpeta persistente del ordenador, no solo en la memoria del chat. |
| [16:30](https://youtu.be/xPJbP9yZE1I?t=990)–[17:34](https://youtu.be/xPJbP9yZE1I?t=1054) | La IA escribe mucho y es mala revisando lo que hizo: hay que pedirle que revise y simplifique, y sobre todo testear. Atomizá las tareas del día y tené una lista de evaluación para volver a probarlas cuando salgan modelos nuevos. |
| [19:01](https://youtu.be/xPJbP9yZE1I?t=1141)–[21:53](https://youtu.be/xPJbP9yZE1I?t=1313) | **Agente** = modelo («cerebro») + contexto de tu negocio + herramientas + un objetivo. El objetivo puede ser de una sola vez o recurrente (cada día, cinco ideas de contenido). |
| [25:34](https://youtu.be/xPJbP9yZE1I?t=1534)–[26:02](https://youtu.be/xPJbP9yZE1I?t=1562) | **Fábricas agénticas:** un proceso con entrada, varios agentes o modelos en cadena y una salida más controlada. Ejemplo: entra un video sin editar; uno recorta, otro propone imágenes, otro termina la edición. Hay fábricas de código, de contenido y de investigación de marketing. Pueden dispararse cuando dejás un input o de forma recurrente («te levantás a las 9 y activás la fábrica»). |

En OnIA el arnés persistente es GitHub `oninteligenciaartificial/onia` en `master`. El capataz es Boss. La máquina persistente de fábricas pesadas es Codex en el VPS más HOMELAB en DESKTOP-0GGGNMF. La laptop DESKTOP-ENV6SDA queda fuera.

## Modelo fijo de OnIA

```
Sergio (objetivos, gasto, publicar, sensible)
        │
        ▼
Boss / Grok Bot (capataz: prioriza dentro de lo aprobado, conectores, reparte)
        │
        ├── Calendario
        ├── Contenido  ← dueño editorial de la fábrica de contenido
        ├── Operaciones
        └── GitHub (cerebro + evidencia + buzón cola-boss)
                    │
                    ▼  PEDIDO con ID del harness
            Codex + HOMELAB (fábricas pesadas)
                    │
                    ▼
            Revisor distinto → Sergio aprueba → publica
```

| Rol | Quién | Qué hace | Qué no hace |
| --- | --- | --- | --- |
| Dueño | Sergio | Objetivos, criterios, contraseñas, sí de gasto, n8n, publicación y revisión editorial final. | No tiene que pegarle a Codex el copy, los conectores ni el calendario. |
| Capataz | Boss (este Grok Bot) | Recibe el pedido, parte el trabajo, usa conectores, documenta en GitHub y coordina a los compañeros. | No ejecuta shell en el VPS ni configura la PC. No es un segundo «jefe de Codex» nuevo. |
| Fábrica de contenido | Contenido | Ideas, guiones, copies, CTA, selección de cortes y criterio de «esto está bueno», usando el cerebro. | No publica. No gasta. No lanza Codex sin un PEDIDO y el sí aplicable. |
| Compañeros | Calendario, Operaciones | Calendario: avisos y solapes. Operaciones: Hostinger y n8n en solo lectura salvo sí. | No sustituyen a Contenido ni a Codex. |
| Fábricas pesadas | Codex + HOMELAB | Código, harness, aislamiento del worker, ASR en CPU, cortes y render con FFmpeg, diagnóstico técnico. | Investigación de negocio ya hecha, copy, relecturas largas que Boss ya resumió, publicar o gastar. |
| Revisión | Distinta de quien produjo | Contenido o Boss miran el texto; otra sesión de Codex mira el código; Sergio publica o gasta. | Publicar sin revisión al estilo Leader Summaries. |

Reglas que no se discuten entre agentes:

1. El cerebro está en GitHub: reglas, decisiones, `03-referentes/cerebros*`, kit y guiones de `01-negocio/workshop-20261108`. Se recupera lo pertinente; no se investiga otra vez lo ya documentado.
2. Los estados viven solo en el harness. [cola-boss.md](pendientes/cola-boss.md) es buzón: ID, destinatario, resultado, aceptación, fuentes/commit, qué está autorizado y qué no. «HECHO» = entregado, no aceptado. Un PEDIDO no es tu autorización. El despachador automático no existe.
3. No se crea otro Grok Bot para «manejar a Codex».
4. Publicar, enviar, gastar, activar o borrar n8n, tocar producción o borrar archivos sigue pidiendo tu sí. Sergio escribe las contraseñas.
5. Prohibido: `--no-sandbox`, desactivar AppArmor o userns, secretos o IPs en Git.

## Meta: al menos 5 videos al día, todos de la fábrica

La meta no se baja. [formatos-onia.md](../02-contenido/formatos-onia.md) y [PLAN.md](../01-negocio/PLAN.md) ya apuntaban a cinco piezas diarias sostenibles. Cinco videos no significan cinco rodajes separados ni cinco ideas idénticas con otro título. Una foto o un carrusel cuenta como publicación, no como uno de los cinco videos.

### Parrilla diaria (cinco slots)

| Slot | Qué sale | Entrada típica | Quién lo fabrica |
| --- | --- | --- | --- |
| 1 · Venta | Video que enseña algo útil y invita al workshop (esta semana) o a la oferta vigente (después). | Kit, G01 y decisiones del workshop. | Contenido escribe; Sergio graba; Codex corta solo con PEDIDO. |
| 2 · Marca seria | Aprendizaje de construir OnIA o de usar IA en un negocio real, tono profesional. | Cerebros de referentes + hecho propio del día. | Contenido. |
| 3 · Actualidad o evergreen | Noticia de IA aplicada a un dueño de negocio, o una pieza atemporal si no hay noticia sólida. | Fuente primaria fechada, o molde G02. | Contenido. No convertir una novedad en promesa de ingresos. |
| 4 · Corte del vlog | Un reel con idea propia sacado del diario crudo «Sergio U X Y Z» (handle aún no confirmado). | El vlog del día, que vos ya grabás sin editar. | Contenido elige el tramo; Codex transcribe y corta si hay PEDIDO. El vlog crudo que subís a ese canal es materia prima, no reemplaza este slot. |
| 5 · Reel de prueba | Otro gancho o formato (pregunta, error, comparación, pantalla). | Misma tanda o el mismo crudo, con idea distinta. | Contenido. Un título nuevo sobre el mismo video no cuenta como otra pieza. |

Esta semana el CTA de los slots 1 y, cuando encaje sin forzar, 4, apunta al workshop: jueves 12 (hora no fijada en el reparto aprobado), viernes 13 a las 21:00 y sábado 14 a las 14:00, America/La_Paz; Bs 50 grupal; clase 1 con Claude. No se anuncia VIP, horario inventado, cupo o pago automático.

### Cómo se llega a 5 sin filmártelos uno por uno

El escenario semanal de [formatos-onia.md](../02-contenido/formatos-onia.md) ya lo armaba: 25 piezas preparadas por lote + 7 diarios + 3 de actualidad = 35 a la semana (5 al día de media). En la práctica:

- Una tanda de grabación cubre los slots 1, 2, 3 y 5 (talking-head o pantalla).
- El vlog diario, que ya estás documentando, alimenta el slot 4 y a veces material de apoyo.
- Contenido entrega los 5 paquetes (guion, tomas, CTA, fuentes y qué se considera bueno) **antes** de que grabs.
- La edición pesada (transcribir, cortar, render, subtítulos) la hace la cadena, no un editor contratado.

### Rampa realista hasta esa meta

La fábrica automática de punta a punta (crudo entra, cinco videos publicados salen sin que nadie mire) **no existe esta semana** y no está autorizada. La rampa sirve para **llegar** a cinco videos de la fábrica por día, no para achicar el número.

| Fase | Cuándo | Qué tiene que salir | Condición honesta |
| --- | --- | --- | --- |
| 1 · Lote escrito | Martes 10 nov | Los primeros 5 paquetes del día. Se reutilizan G01 y G02 como dos de ellos. Vos grabás una tanda y el vlog del día. | Si falta el crudo, hay 5 paquetes y no 5 cortes. Eso no cancela la meta: bloquea el render. |
| 2 · Primer día de 5 cortes | Miércoles 11 nov | 5 borradores editados listos para tu revisión (3 o 4 de la tanda + 1 corte del vlog + 1 de prueba). | Hace falta la tanda del martes y una vía de corte: Contenido marca tiempos; Codex/HOMELAB usa FFmpeg y ASR en CPU si el PEDIDO y el aislamiento lo permiten; si todavía no, corte mínimo a mano con herramientas que ya tengas, sin gastar en apps nuevas. |
| 3 · Ritmo de venta | Jueves 12 a sábado 14 | Cada día, 5 videos de la fábrica. Se publican los que vos apruebes, con prioridad de venta del workshop. | Publicar 5 el mismo día exige que revises ese lote (unos 20 a 30 minutos). Si un día no hay noticia usable, el slot 3 es evergreen. La PC no tiene GPU útil: cinco shorts cortos se pueden renderizar en CPU, pero el ASR de un vlog largo no es instantáneo; se puede dejar en cola, no se promete magia. |
| 4 · Cadena más automática | Después del 14 (v2) | Todas las mañanas, 5 borradores editados en cola de revisión, con menos mano. Rutina tipo Euge (cinco preguntas o ideas del día) y ciclo medir-aprender-mejorar. | Sigue haciendo falta tu sí para publicar. Un disparador recurrente (rutina de Boss o n8n) espera otro sí. No se implementa un scheduler por este archivo. |

Cuota, para no inventar números: la de Codex estaba en 67% usada hasta el viernes 13 nov 22:47 America/La_Paz, en la lectura de la tarde del 9. La de Grok estaba en 7,8% usada, con reset el sábado 14 nov 10:00 America/La_Paz. Esta semana los guiones los hacen Boss y Contenido, que no gastan cuota de Codex. Codex reserva lo que quede para el homelab esencial y, si hay PEDIDO, para ASR y cortes.

## Fábrica de contenido v1 · esta semana (ventas del workshop)

Cadena, igual que el reparto aprobado:

**entrada** (idea tuya, video crudo o noticia con fuente) → **Boss** (prioridad y brief) → **Contenido** (guion, cortes propuestos, copy, CTA, usando el cerebro) → **PEDIDO técnico** solo si hace falta → **Codex/HOMELAB** (ASR CPU, FFmpeg) → **revisor distinto** → **vos aprobás y publicás**.

El diseño documental de ideas y guiones ya existe en [fabrica-contenido/20261108/DISENO.md](../05-herramientas/fabrica-contenido/20261108/DISENO.md). Esta v1 lo usa para vender, sin montar el scheduler ni el Telegram real.

### Qué ya se puede reutilizar

- Cerebros de 19 referentes en `03-referentes/cerebros/` (todos parciales) y profundos en `03-referentes/cerebros-profundos/`.
- Formatos y la cuenta de 5 al día: [formatos-onia.md](../02-contenido/formatos-onia.md), [PANEL-DIARIO.md](../02-contenido/PANEL-DIARIO.md), [CEREBRO-DIARIO.md](../02-contenido/CEREBRO-DIARIO.md).
- Kit y borradores del workshop: [README-ENTREGA.md](../01-negocio/workshop-20261108/noche-20261109/README-ENTREGA.md), [G01](../01-negocio/workshop-20261108/noche-20261109/GUION-01-WORKSHOP.md), [G02](../01-negocio/workshop-20261108/noche-20261109/GUION-02-EVERGREEN.md), [primeros 10 minutos](../01-negocio/workshop-20261108/noche-20261109/CLASE1-PRIMEROS10MIN.md), [oferta](../01-negocio/workshop-20261108/noche-20261109/OFERTA-Y-RECORRIDO.md), [controles](../01-negocio/workshop-20261108/noche-20261109/CONTROL-EDITORIAL-Y-PENDIENTES.md).
- Pieza 01 de marca: [PIEZA-01.md](../02-contenido/2026-11-07-primer-contenido-onia/PIEZA-01.md).
- Contrato de empresa unipersonal y reparto aprobado, citados arriba.
- Codex está preparando ASR en CPU (faster-whisper int8) y cortes con FFmpeg; no se dan por listos hasta que haya comprobación.

### Huecos de esta semana

- G01 y G02 siguen en borrador: falta revisión editorial distinta y tu decisión. G01 no se debería publicar hasta que haya canal, responsable y forma de atender el comentario «NEGOCIO».
- Falta confirmar handle y URL del vlog «Sergio U X Y Z».
- Faltan hora del jueves 12, canal de clases, pagos, cupos y soporte.
- El aislamiento de `onia-worker` y `/mnt/c` todavía era pendiente al documentar el homelab; sin eso no se da por operativa la PC.
- No hay GPU útil (GT 730). Higgsfield existe como conector y tiene créditos registrados en el plan, pero usarlo gasta: esta v1 no depende de eso.
- Instagram: la bandeja estuvo bloqueada por un control de seguridad; los leads no se leen desde acá.
- El adaptador de Telegram de la fábrica es prueba inactiva; no se activa n8n.
- `CONTEXTO-BOSS.md` sigue sin crearse; el buzón `cola-boss.md` sí existe desde el commit del reparto.

### Qué pide tu sí en la v1

Escribir y revisar paquetes en GitHub, no. Grabar, no (eso lo hacés vos). Publicar cada pieza, sí. Un PEDIDO de ASR o corte sobre un archivo concreto, sí (o el sí ya dado al alcance técnico del reparto, si el archivo y la ruta están autorizados). Abrir inscripciones, cobrar, mandar DMs o activar n8n, sí específico y aparte.

## Fábrica de contenido v2 · adelantada a hoy, 9 nov 2026

**Cambio aprobado por Sergio el 2026-11-09 20:27 America/La_Paz** («Quiero la automática completa hoy aunque cambie el plan»). La v2 deja de esperar al 14 y se construye hoy. Todo lo demás de este archivo sigue fijo. Publicar, gastar, activar n8n y tocar la PC siguen necesitando su sí.

**Corrección de Sergio, 2026-11-09 20:30 La Paz:** el vlog diario no se corta. Se publica entero y sin edición. Los 5 videos salen de una sola tanda grabada con los 5 guiones del día (venta, marca seria, noticia o evergreen, un segundo de venta o marca, trial reel). Donde abajo dice «vlog», léase «grabación de la tanda».

Cadena automática de hoy, en orden de construcción:

1. **Cola de entrada del vlog** (Codex): carpeta privada fuera de Git (en HOMELAB `/var/lib/onia-worker/work/entrada/` cuando el alta quede OK; mientras tanto, en el VPS bajo `~/operacion/fabrica/entrada/`). Sergio deja el video crudo; nada de esto va a GitHub.
2. **Transcripción y cortes** (Codex): un comando `fabrica.py procesar <video>` que hace ASR en CPU (faster-whisper int8), corta con FFmpeg según una lista de intervalos en JSON, saca 9:16 con subtítulos quemados y deja los borradores en `salida/AAAA-MM-DD/`. Probado con un video de prueba y tests.
3. **Guiones e intervalos del día** (Boss): rutina diaria de Grok Bot a las 07:00 La Paz que lee el cerebro y las noticias de IA, escribe los 5 guiones (los 5 slots fijos) en `02-contenido/fabrica-diaria/AAAA-MM-DD.md` y, si hay transcripción del vlog, la lista de cortes en JSON para el paso 2.
4. **Disparo de Codex** (Boss): Boss lanza `procesar` por el harness con Sol low y sin subagentes; revisor distinto antes de entregar.
5. **Revisión y publicación** (Sergio): ve los 5 borradores, aprueba y publica. No hay publicación automática.
6. **Medir y mejorar**: Boss anota qué se publicó y cómo fue, y guarda el criterio en el procedimiento.

Lo que sigue igual que antes: el harness no despacha solo (lo dispara Boss), n8n no se toca, y el render es en CPU (sin GPU útil), así que un vlog largo tarda y queda en cola.

### Fábrica de edición tal como la muestra Euge (releído 2026-11-09 20:40 La Paz)

Fuente: video 1 [17:58–28:31](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1078s) y video 2 [24:00–26:35](https://youtu.be/xPJbP9yZE1I?t=1440).

- Grok Bot no edita: la edición la hace un modelo fuerte en otra máquina persistente (él usa Opus; en OnIA, Codex en VPS/HOMELAB). Grok Bot ayuda a montar la fábrica y a revisar.
- Pasos visibles de su fábrica de video: **recibe → escucha → cortar → montar**, con un tablero que muestra «paso 4 de 5» y avisa si algo falló.
- Cadena de varios agentes (video 2, 25:04): uno recorta lo mejor; otro revisa y propone imágenes/B-roll para insertar; el modelo fuerte termina la edición (subtítulos, motion graphics, clips externos).
- **Sala de montaje**: ver cómo van los videos, comentar «cambiame esto» y pedir otra versión; cada comentario se guarda en el procedimiento.
- **Enseñar con antes/después**: él edita uno a mano (CapCut, cortes de silencio) y le da entrada y salida; si la duración no coincide, la fábrica investiga qué criterio falló y lo corrige.
- Ciclo **medir → aprender → mejorar**; la primera vez no sale bien.
- Disparo: cuando dejás un input o de forma recurrente (a las 9).

Carpetas en el Drive de Sergio (creadas por Boss, solo IDs públicos de carpeta, sin contenido en Git): Fábrica OnIA `1TGezto0pbmnijtWm3rPEEnt-gX-Hs42I` con 1 Entrada `1OWW5GGfF1GQrXFer7HmLEoIf9sQRGrWp`, 2 B-roll `1ogk1iwL3rgr_OKpBV70PdzgSmwAIClot`, 3 Sala de montaje `1bZs-7y3BkPm3qDC7vUxqVAt_s5GLbGmA`, 4 Ejemplos antes/después `1-2dzLYGFGk_zNnii7-Qz2VI__p0JvtHf`. Boss mueve archivos Drive ↔ cola privada; Codex no toca Drive. La infraestructura se mejora día a día por el harness.

## Fábrica de contenido v2 · texto original (antes del cambio)

Cuando termine el workshop, la misma cadena se vuelve más automática y se mide. No se lanza en este archivo.

1. Rutina diaria de Boss o Contenido, al estilo de las cinco preguntas de Euge: cinco ideas o preguntas listas para grabar, sacadas del cerebro y de lo que pasó ayer.
2. El vlog del día entra solo a una cola privada (Drive u otra ruta que elijas, nunca a Git). Un PEDIDO estándar pide transcripción y recortes según la lista de Contenido.
3. Ciclo de idea ganadora: medir qué se publicó, qué se guardó, qué preguntas llegaron y qué se inscribió; aprender; guardar el criterio en el procedimiento, como la sala de montaje de Euge.
4. Un disparador recurrente (rutina de Grok Bot o, más adelante, n8n) solo con tu sí, después de probarlo con datos de juguete. El harness sigue sin despachar solo.
5. Otras olas (plan de caja, Binance en lectura, ideas, startups, negocios físicos con IA) se anotan cuando las mandes; no empujan esta fábrica ni crean otro agente.

## Análisis de cuentas y perfil · plan, no se ejecuta aquí

Querés mejorar la marca personal seria y el vlog diario con el proceso de **idea ganadora** de Euge, los referentes y el cerebro. Este apartado solo planea ese análisis. No se abre ninguna cuenta ni se cambia ninguna bio en este commit.

El proceso, según el video 1 ([20:32](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1232s)–[23:34](https://www.youtube.com/watch?v=JuAQILH7dkQ&t=1414s)):

1. Definir qué es una buena idea para vos ahora: dueño de negocio en Santa Cruz, orgánico, tono serio en la marca principal, vlog crudo como diario, y esta semana un puente claro al workshop.
2. Listar las materias primas que vos sí usás: tus propios posts, el cerebro de referentes ya estudiado, noticias con fuente, el vlog del día. Euge insiste en usar las referencias reales de quien crea, no artículos sueltos que no mirás.
3. Generar más candidatos de los que se van a grabar.
4. Filtrar simulando personas de tu público (avatar de dueño de negocio principiante).
5. Pasar las que sobrevivan por un crítico (claridad, prueba, CTA, límites).
6. Medir, aprender y mejorar el procedimiento.

En el repo, «idea ganadora» aparece además como un tramo de clase de un referente (hacia 40:19–42:27 en una nota de [historicos-v2.md](../99-archivo/versiones-superadas/historicos-v2.md)). Eso no sustituye el proceso de Euge ni se copia como receta de OnIA.

[PLAN.md](../01-negocio/PLAN.md) ya pedía inventariar bios, portadas, fijados y enlaces de Instagram `@sergiourcullo`, YouTube y TikTok, evitando cuentas duplicadas. Ese inventario no se da por hecho en este turno: hay que confirmar handles y URLs con vos.

### Qué debería entregar el análisis (cuando lo autorices)

- Mapa de cuentas: cuál es la marca seria, cuál es el vlog, si hay duplicadas.
- Qué comunica hoy cada bio, foto, destacado y video fijado, y qué choca con el tono serio o con el workshop.
- Lectura de las últimas 20 a 30 piezas públicas por cuenta: gancho, tema, prueba, CTA, formato y fecha. Separar hecho observado de propuesta.
- Contraste con el cerebro (por ejemplo especificidad de Pedro, orientación de Erik, gancho/entrega de Hormozi, claridad de Nippard) sin imitar voz ni fingir sus resultados.
- Propuesta de mejora: bio, fijados, mezcla de los 5 slots, y qué dejar de hacer.
- No publica cambios. No infiere ventas de un referente por sus likes.

### Datos y accesos que harían falta

Se puede empezar por lo público, sin contraseñas:

- URL y handle confirmados de Instagram, TikTok, YouTube principal y el vlog «Sergio U X Y Z».
- Bio, foto, link, destacados y piezas fijadas de cada una.
- Las últimas 20 a 30 publicaciones públicas por cuenta (texto visible, fecha, formato).
- Comentarios públicos si se ven sin entrar.

Con tu sí, y entrando vos mismo (nunca contraseñas, cookies ni códigos por chat):

- Instagram profesional: Insights de alcance, guardados, visitas al perfil y cuentas alcanzadas, últimos 90 días si existen.
- TikTok Analytics de la cuenta tuya, no de una cuenta de anuncio ajena.
- YouTube Studio del vlog y, si existe, del canal principal: tiempo de reproducción, retención, fuentes de tráfico y Shorts frente a video largo.
- Confirmar qué cuenta es personal, cuál es OnIA y cuáles no se tocan.
- Una exportación o captura de Insights si el conector no ve tu usuario.

Lo que no alcanza o no se debe hacer:

- Los conectores de Meta, TikTok for Business o X no prueban que estén unidos a *tus* cuentas ni autorizan publicar.
- TubeAlfred seguía sin autenticar al leer los videos de Euge.
- Un login en el visor del VPS no le da a Codex tus cookies. No se copian perfiles de navegador.
- TikTok Promote pide 18 años; no se activa a tu nombre ([formatos-onia.md](../02-contenido/formatos-onia.md)).
- La bandeja de Instagram bloqueada por seguridad la resolvés vos en el celular.
- No se bajan videos privados ni se suben originales al repo.

Dueño del análisis, cuando lo pidas: Contenido redacta; Boss coordina y usa conectores solo de lectura pública o los que ya estén autorizados; Codex no gasta cuota en esto salvo un fallo técnico concreto.

## Decisiones que necesita Sergio

1. ¿Confirmás este archivo como fuente única del modelo (apoyado en EMPRESA-UNIPERSONAL y en el reparto aprobado, sin agente Grok nuevo y con Contenido dueño de la fábrica)?
2. ¿Arranca Contenido mañana el lote escrito de 5 paquetes, reutilizando G01 y G02, para que grabes una tanda?
3. ¿Cuál es la URL o el handle exacto del vlog «Sergio U X Y Z», y cuáles son hoy Instagram, TikTok y YouTube de la marca seria?
4. ¿Querés que el análisis de cuentas se haga en cuanto mandes esos links (primero lo público), o después del 14?
5. ¿Seguís pidiendo tu sí para cada publicación, o querés cambiar esa regla? Este archivo conserva el sí.
6. Canal, hora del jueves 12, forma de pago, cupos y quién atiende «NEGOCIO»: sin eso G01 no debería salir.
7. ¿Autorizás, cuando el crudo esté en una ruta privada, el primer PEDIDO de transcripción y cortes de esta semana?

## Fuentes usadas en este turno

- Subtítulos `es-orig` de [JuAQILH7dkQ](https://www.youtube.com/watch?v=JuAQILH7dkQ) y [xPJbP9yZE1I](https://youtu.be/xPJbP9yZE1I), 9 nov 2026, y las lecturas ya documentadas [EUGE-VIDEO-BOSS-20261109.md](EUGE-VIDEO-BOSS-20261109.md) y [EUGE-VIDEO2-BOSS-20261109.md](EUGE-VIDEO2-BOSS-20261109.md).
- [EMPRESA-UNIPERSONAL.md](EMPRESA-UNIPERSONAL.md), [REPARTO-CODEX-GROKBOT-20261109.md](REPARTO-CODEX-GROKBOT-20261109.md), [OPERACION-AGENTS-VIGENTE.md](OPERACION-AGENTS-VIGENTE.md), [boss-memoria.md](boss-memoria.md).
- [formatos-onia.md](../02-contenido/formatos-onia.md), [PLAN.md](../01-negocio/PLAN.md) §2–3, kit `01-negocio/workshop-20261108/noche-20261109/`, [cerebros/README.md](../03-referentes/cerebros/README.md), [DISENO.md](../05-herramientas/fabrica-contenido/20261108/DISENO.md).
- [Fortune, 4 feb 2024, sobre Altman y la compañía de una persona](https://fortune.com/2024/02/04/sam-altman-one-person-unicorn-silicon-valley-founder-myth/).
- [Fast Company sobre el solopreneur unicorn](https://www.fastcompany.com/91447642/how-close-is-the-first-solopreneur-unicorn).
- [Company of One, Paul Jarvis](https://www.penguin.co.uk/books/312524/company-of-one-by-jarvis-paul/9780241470466).
- [MCA India, One Person Company](https://www.mca.gov.in/content/mca/global/en/help-faq/faqs/company-services/incorporation/one-person-company.html).
- [Bootstrapped Makers, how to run a one-person company with AI agents](https://bootstrappedmakers.com/blog/run-a-one-person-company-with-ai-agents).
- [Full Circle, The One-Person Company Playbook](https://fullcircle.software/blog/one-person-company-ai).
- [levels.io](https://levels.io/); posts [1901915803609432421](https://x.com/levelsio/status/1901915803609432421) y [1899947042606375417](https://x.com/levelsio/status/1899947042606375417).
- [Sam Altman, 28 may 2023](https://x.com/sama/status/1662759311230083075).

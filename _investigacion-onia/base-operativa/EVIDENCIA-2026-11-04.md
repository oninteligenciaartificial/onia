# Evidencia operativa · 4 de noviembre de 2026

Registro saneado. Los resultados describen su entorno y momento; no sustituyen la aceptación de una VM nueva. [Estado vigente](ESTADO.md).

## Panel y conocimiento

- Notion Sergio · Hoy existe, con vida, contenido, ventas, actualidad y decisiones. Relectura con conector confirmó estructura e IDs. No verificación visual móvil ni avisos.
- Investigación consolidada: nueve fichas, 16 recetas y propuestas comerciales identificadas. Fuente: [índice](investigacion/2026-11-04/README.md). No cursos completos ni métricas privadas.
- Desarrollo cloud recuperó biblioteca y catálogo actualizados mediante conector, sin depender de archivos locales de coordinación.

## Instagram: ensayo HTTP, no producción

Ejecución en el chat cloud de automatizaciones registrado en SESIONES.md; [evidencia completa y código del prototipo](https://chatgpt.com/space/page_afe5a3b4a224819182d708206cb6f15d), secuencia 1.

Resultado: 62 casos HTTP loopback entre dos procesos, SQLite y diez reinicios del servicio. Tres defectos reproducidos antes y corregidos después: autorización que alteraba el digest del trabajo, pérdida de estado STOP/HUMAN tras fallo y cuerpos JSON firmados no objeto que cerraban la conexión.

Se probaron deduplicación, estados inciertos sin reintento automático de escritura, verificación de resultados mock y conservación de controles de conversación. La revisión independiente comprobó los casos y límites. Cero llamadas Meta reales, DMs reales y publicaciones reales; n8n no ejecutado. No demuestra concurrencia, persistencia entre VMs ni integración con cuentas de producción.

El prototipo completo permanece en la evidencia cloud; no se promueve como publicador real por haber superado los mocks.

## Navegador: causa y solución observadas

[Informe de Desarrollo](https://chatgpt.com/space/page_2b9ade6c69bc8191a7de31805f2cdabb), secuencia 4. VM: HEAD 9972d26, Linux, Playwright 1.64.1, Chromium 156.0.8078.4. El error inicial era ERR_CERT_AUTHORITY_INVALID; Python/OpenSSL verificaban la cadena mediante el mismo proxy oficial.

strace durante la navegación identificó access(cert9.db, W_OK) = EROFS en la base NSS del usuario. Una base temporal aislada y escribible, con la CA oficial verificada por fingerprint, permitió abrir la base y navegar con TLS activo.

Resultado público: Acquisition HTTP 200 y título correcto; captura inspeccionada; clic Play y reproducción hasta 4,67 s, duración informada 1787,875 s, paused=false, readyState=4, error=null. Fotograma distinto del póster. No se escuchó audio ni recuperó transcripción.

La corrección no cambia confianza global, proxy, credenciales o cookies. No repite solicitudes Instagram limitadas ni elude CAPTCHA. Su integración versionada se documenta en [OPERAR](cloud/OPERAR.md). Publicación de un entorno y funcionamiento de un perfil autenticado son comprobaciones separadas.

## Límites de continuidad

Aceptación del bootstrap versionado: Desarrollo actualizó por fast-forward a **2b1f9ab7b95537d82553c6a60e1030b374410c66**, checkout limpio. Ocho pruebas Node, diez tests del harness y doctor aprobados en Linux. Dos procesos independientes importaron la CA real en directorios NSS nuevos con buildLaunchOptions(); ambos HTTP 200, título y captura comprobados. Play público avanzó 4,46 s; cleanup eliminó ambos directorios. No se reutilizaron los lanzadores temporales del diagnóstico. Informe cloud, secuencia 5. En Windows la prueba de symlink del harness se omitió por privilegios; en Linux pasaron las diez.

El repo recibido por otra VM debe cotejarse por SHA. Un commit/push prueba entrega a GitHub; leerlo y ejecutar el bootstrap en cloud prueba algo distinto. Una tarea Cloud iniciada puede continuar con la PC principal apagada; no se creó un planificador permanente ni un flujo n8n→Codex.

## Preparación reutilizable del entorno

El editor de onia también actualizó a 2b1f9ab con checkout limpio. Completó install.sh y start.sh; doctor, 28 pruebas Python, ocho del módulo NSS y una de navegador aprobados. Acquisition respondió HTTP 200 con una base NSS nueva y captura inspeccionada. Chromium 156.0.8078.4, Playwright 1.64.1. El primer start se adelantó a la descarga del navegador y falló por ejecutable ausente; luego de terminar install se repitió y pasó.

Se guardó el borrador revisión 2, que añade la lectura de cloud/OPERAR.md al inicio y conserva INICIO-SESION.md. Sin cambios en secretos, permisos o política de red. Tras guardar y publicar desde la interfaz nativa, ésta mostró «Entorno publicado» y «Publicado · Probar» con confirmación verde el 4 de noviembre. Las pruebas anteriores pertenecen a las VMs de Desarrollo/editor; esta publicación no equivale a haber repetido las pruebas en una nueva tarea de usuario.

La metadata oficial del editor confirmó la nueva versión publicada **6aeb5d2767cc81a3aee4674cf6485f5d**, con nuevo borrador revisión 1 basado en ella y OPERAR.md conservado. Primero estaba starting/offline; la comprobación final confirmó **running/connected** y ejecutó una lectura de pwd y HEAD: /workspace/onia, **2b1f9ab7b95537d82553c6a60e1030b374410c66**. No se reinstaló, modificó el borrador ni repitieron tests. Disponibilidad comprobada; nueva tarea de usuario posterior a publicar no ejecutada.


## Entrega de cierre: semana, formatos y flujo privado

4 de noviembre de 2026. Repo actualizado desde master **58ea79da1d6495118de8b3fdfb18f30948f26df4**, sin cambios locales previos. Este cierre mantiene el repo como índice y estado canónico, los paquetes creativos versionados en cloud y Notion como vista diaria; no copia guiones, JSON operativos, credenciales ni perfiles al repo. No añade reglas, skills, aplicaciones o cambios del producto.

### Material que Sergio ya puede usar

| Entrega y fuente | Resultado verificado y límite |
|---|---|
| [Semana y propuesta de marketing](https://chatgpt.com/space/page_0722a12b4a988191b8835391a4bed17a) | Relectura secuencia 14: **PLAN v2.0 final** y Kit PLAN de cinco secciones con ejemplos/plantillas disponibles en la misma página; 35 IDs originales, sin extras, ahora 29 guiones concretos y seis plantillas de diario. **Borradores editoriales en revisión de Sergio**. V1.2 fue rechazada y queda histórica, no lista para grabar; su sincronización anterior no acredita aceptación del contenido. Organización actualiza Notion desde la fuente vigente sin duplicar IDs; no se da por terminada esa nueva sincronización. Versiones/JSON/ZIP permanecen en cloud, sin copiar guiones a Git. |
| [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) | Releído por conector oficial: home único, primer lote, revisión de renders y 35 tarjetas Por grabar según la vista y comprobación de coordinación; cinco por día, diario último 20:00 America/La_Paz. Guiones y fechas no son programación ni publicación. Investigación histórica queda detrás de Más. |
| [Demostración de formatos](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4) | Página releída, secuencia 3: vertical 60 s, 1080×1920, y horizontal 50 s, 1920×1080; ambos H.264/30 fps, sin audio, cinco capítulos por archivo. No son cinco videos acabados. ZIP, composiciones, guía de tomas y 16 recetas disponibles. HyperFrames 0.9.10 cloud; QA de decodificación y composición registrado, reproducción técnica a 4×; coordinación inspeccionó ambas hojas de contacto. Falta rostro/voz/material real, no es visionado humano continuo a velocidad normal ni adaptación final a cada red. |
| [Flujo n8n de mensajes DRY_RUN](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75) | Página releída, secuencia 1: workflow real de 17 nodos, inactivo, sin nodos de envío. 23 casos HTTP secuenciales y dos escenarios concurrentes reales; los resultados no acreditan automatización comercial ni conexión Meta. JSON descargable con referencias operativas privadas permanece en cloud. |
| [Perfil público y propuesta](https://chatgpt.com/space/page_175b3d0f70e88191992265d5515a3413) | La relectura inicial mostró secuencia 1 con la búsqueda anterior; actualización posterior de coordinación: Video navegó una vez desde cloud y observó la bio «Desarrollo sistemas con IA para escalar tu negocio / Fundador de @oniahq / Aprende IA gratis 👇» y enlace WhatsApp. Login wall impidió feed/fijados: cero piezas vistas; YouTube sigue sin identificar. Coordinación confirmó la misma página actualizada y verificada con esa evidencia y recomendación de alinear identidad vida/founder/IA, distinguiendo gratis de taller. El CTA primario anterior DM PLAN queda supersedido por el embudo de comentario PLAN descrito en este cierre. Recomendación, no cambio del perfil ni auditoría de publicaciones. |

La recomendación comercial actual es **«Tu primer sistema personal con IA: organizá tu semana y delegá una tarea»**: Bs 50 y 55 min propuestos, Embudo actual en borrador: valor completo en la pieza → comentario PLAN → entrega manual del Kit → invitación opcional al workshop. PLAN conserva la keyword y reemplaza DM como CTA primario; el cierre posterior sólo acredita comentario/lead en n8n con adaptadores simulados e inactivos, no automatización real de Instagram. No es decisión aprobada, fecha, preventa ni cobro autorizado. El alumno no necesita Codex pago; la demo cloud corresponde al facilitador, sin prometer acceso cloud gratuito al alumno. La ficha de guiones «De idea a reel» y Luma quedan como antecedentes históricos para este encargo, no como otra oferta activa. Este cierre sólo indexa la propuesta viva en marketing; no duplica sus alternativas o condiciones.

### Qué limita la autonomía real

La carrera con el mismo event_id en el flujo de 17 nodos produjo **dos filas**: Get+Insert no es un claim atómico ni exactly-once. La carrera HUMANO/BAJA se corrigió con controles append-only: ambas filas se conservan y BAJA domina a HUMANO en lecturas posteriores. Eso no demuestra atomicidad entre tablas o recuperación de cada punto de fallo. Relectura de la misma evidencia, secuencia 2: parche descargable transactional-outbox.sql de 30 líneas para PostgreSQL 13+, con reserva inbox/outbox, claim por token y finalización condicionada. Es especificación revisada estáticamente, **no aplicada ni verificada con un motor PostgreSQL**. El workflow sigue DRY_RUN e inactivo; no se instaló infraestructura. No habilitar salidas basándose en deduplicación secuencial.

Faltan autorización personal IG, guardado de `META_IG_ACCESS_TOKEN` por su mecanismo y validación de lectura cloud; un verificador seguro de entrada challenge/HMAC-SHA256 sobre bytes crudos con secreto bajo custodia; y claim atómico antes de salidas. Los tests locales de frontera con secretos ficticios no prueban un webhook Meta. No instalar infraestructura nueva ni copiar secretos a Code/JSON. Cero DMs reales y cero publicaciones. El ensayo anterior de cinco casos sigue como antecedente, no como prueba de concurrencia del flujo nuevo.

### Continuación concreta

Recomendación inmediata: revisar con Sergio los reemplazos y el Kit completo en la fuente cloud antes de volver a preparar grabación del contenido aprobado. Alternativa independiente: ensayar el microproblema con un ejemplo antes/después y comprobar que la conclusión se entiende sin comentar ni recibir el recurso. Organización actualiza la vista diaria conservando los 35 IDs; no se presume sincronización de v2.0 por la antigua importación. No abre cobros ni autoriza publicaciones o envíos.

Automatizaciones debe completar/revisar el claim transaccional y la frontera segura antes de conectar entradas/salidas reales; Sergio sólo completa la autorización personal que falte. La referencia de perfil puede completarse con URL/handle YouTube o una fuente pública recuperable. Esta entrega no crea scheduler, trabajo 24/7, publicación ni envío autónomo. No se consumieron créditos Higgsfield ni añadió software al VPS. Las verificaciones nuevas de este cierre fueron lecturas documentales y QA del diff, sin repetir suites o pruebas de código.


## Corrección editorial del cierre: valor antes del recurso

4 de noviembre de 2026. Sergio rechazó los guiones anteriores: confundimos contexto personal e intenciones con enseñanza demostrable y añadimos un CTA antes de cerrar el microproblema. Coordinación escribió cinco reemplazos con QA independiente; la relectura de marketing en secuencia 14 ya muestra PLAN v2.0 final y Kit PLAN, pero su disponibilidad no equivale a aprobación de Sergio. Cada pieza presenta problema concreto, demostración y conclusión completa antes del CTA; ejemplos/antes-después e historias reales reemplazan intenciones vacías. El recurso amplía el valor, no retiene la conclusión para obligar a comentar. No se crea regla universal ni skill.

**Hallazgos de referentes (alcance limitado):** coordinación/subagentes leyeron una [transcripción automática de Hormozi](https://viewrankai.com/tools/youtube-transcript/7NMH1oAkgLY) del vídeo 7NMH1oAkgLY y [texto propio de Erik](https://news.eriktaveras.com/archive/89fbc6be-6eb3-4e1d-8ecc-fabf1d4db560); Heras procede de una [transcripción parcial de terceros](https://pickscribe.com/v/GbavuA_jqmw/) leída por un agente, cuyo fetch falló a coordinación. Aplicación editorial: enseñar con una prueba concreta, desarrollar el ejemplo y cerrar su enseñanza antes de pedir una acción. Son lecturas de texto con distintas calidades, no vídeos vistos, análisis audiovisual ni auditoría integral de los referentes.

Comentario PLAN → entrega manual del Kit → invitación opcional es una propuesta, sin implementación n8n de comentarios, permiso de publicación/envío ni cambio de oferta, precio o fecha. El DRY_RUN DM y los permisos permanecen intactos. La versión viva se recupera por el enlace estable; Notion es su vista diaria y el repo conserva este índice/estado.


## Consolidación operativa posterior: maqueta, ensayo y dependencias

4 de noviembre de 2026. Base de este cambio: master 57befa97f9db9c4ac32b95778e458d042ed64778, árbol limpio. Síntesis documental con enlaces, sin copiar medios, JSON operativos, credenciales o documentos privados completos. Los resultados anteriores se conservan como historial; el estado actualizado distingue prueba aislada, integrada y activa.

| Fuente viva | Entrega y prueba | Límite vigente |
|---|---|---|
| [CLI n8n→Codex](https://chatgpt.com/space/page_8aec522aeac8819185bf697166227f5f), secuencia 0 | Binario 0.166.0-alpha.1 disponible, cloud experimental; list remoto devolvió 401: «Could not parse your authentication token. Please try signing in again.» | Login local no prueba autenticación backend; cero tareas creadas y ningún ENV_ID inventado. No despacho, callback, polling integrado ni persistencia de resultados acreditados. Device auth en lanzador dedicado es la siguiente opción, sin API paga ni auth copiada desde PC. |
| [P2 v2](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4), secuencia 6 | MP4 real 48 s, 1080×1920, H.264, sin voz; 17 checks y cache hit comprobado sin render duplicado, según entrega de Video. Artefactos/worker/manifiesto privados disponibles. | Lanzamiento CLI manual, no enqueue/callback. MP-M02 sigue pendiente de voz/toma de Sergio y revisión; una maqueta no completa la grabación ni autoriza publicación. |
| [Workshop y marca](https://chatgpt.com/space/page_d5d8f16b59d481919b0b597e4d25d5b4), secuencia 1 | Ensayo documental con Kit y ejemplo ficticio; cinco tareas WS y cinco MP. Bs 50/55 min siguen propuestas, sin fecha/capacidad reservada. | No clase humana de 55 min, aprendizaje medido o cobro. No heredar revisión/soporte del taller histórico ni prometer cloud gratis al alumno. |
| [Producto](https://chatgpt.com/space/page_160800c9076881919764ae7971519b43), secuencia 1 | Lectura a0488f0 y seis tareas. Recomendación: dental ADMIN → paciente/cita persistidos → suscripción QR manual → aprobación → reentrada. Se ejecutó sólo sintaxis y evaluación de configuración de ocho servicios sin puertos publicados. | Diferencia estática: QA exige WhatsApp cuando checkout prioriza QR vigente; no bug runtime reproducido. Configuración sin puertos no prueba aislamiento runtime, E2E ni producción. Sin código/migraciones/despliegues por este cierre. |
| [Cola operativa](https://app.notion.com/p/40e2eb20bdfd81259c44e8328cd52171) y [home](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) | Relectura por conector: 20 tareas, diez WS/MP + seis producto + cuatro transversales. Home con tres acciones y 35 guiones v2 sincronizados; Organización actualizó el estado Video, manteniendo MP-M02 pendiente de voz/toma. | Notion actualizado por agente, no credencial runtime n8n→Notion ni scheduler. Guiones/renders sin aprobación para publicar. |

El [cierre E2E integrado sintético](https://chatgpt.com/space/page_fc4f62e97618819190780105757ffbaf), releído en secuencia 1, acredita **60 verificaciones HTTP** en n8n y circuito con el mismo run_id: contenido/revisión/aprobación, programación/publicación stub, comentario PLAN/recurso/lead e interés de workshop. Son tres workflows, todos finalmente inactivos; Meta, publicación, entrega de recurso e interés se simulan, pago y acceso son manuales. Los 60 incluyen preparación repetida por escenario, no 60 funciones. La carrera produjo dos filas: **atomicidad runtime FALLIDA**, no exactly-once ni listo para activar. Los **15 checks PostgreSQL temporales aislados** pasaron, pero no están integrados al runtime n8n. JSON, IDs y artefactos operativos permanecen en la biblioteca privada; no se exportan.

Para comentarios, [accesos](accesos.md#instagram-operativo-y-continuidad-de-autenticación) incorpora `instagram_business_manage_comments` como requisito adicional de Instagram Login, sin atribuir concesión. Snapshot primario Meta del 10-dic-2025 revisado el 4-nov-2026; políticas por revalidar antes de activar. Keyword del piloto: trim + uppercase exactamente PLAN. Private reply único por comentario dentro de siete días; seguimiento de taller sólo después de respuesta del usuario y dentro de 24 h de esa respuesta. Un clic en el Kit no abre esa autorización. No se cambia Ads/Facebook ni se declara comentario/DM real enviado.

**Sergio ya puede usar:** home para priorizar, paquete v2/Kit para revisar, maqueta P2 para preparar voz y toma, ensayo documental del workshop y tareas de producto como criterios de trabajo. Recomendación por costo/dependencias: avanzar voz/toma y ensayo humano supervisado mientras se resuelven accesos; alternativa independiente: revisar ficha y aceptación del recorrido dental sin ejecutar producción.

**Autonomía real todavía bloqueada por:** autorización/token IG, secreto HMAC en custodia segura, URL pública aprobada, claim atómico integrado al runtime, lanzador cloud autenticado (actual 401) y conexión runtime Notion. No se crearon servicios, reglas, skills, suscripciones o API keys; no se activaron scheduler, DMs, publicación ni cobros. Este cierre revisó documentos/enlaces y diff; no repitió suites de software.


## Cierre final de consolidación y reparto

4 de noviembre de 2026. [Fuente final n8n](https://chatgpt.com/space/page_fc4f62e97618819190780105757ffbaf), secuencia 1: ensayo sintético integrado terminado, tres workflows inactivos y atomicidad runtime fallida. Se puede revisar la evidencia, no activar una automatización real por esos resultados. Quedan claim integrado, firma segura y accesos/destinos aprobados antes de cualquier salida real; el SQL aislado no sustituye esa integración.

Nueva prioridad comunicada por Sergio: investigar evidencia de referentes y plan verificado antes de ampliar guiones, web o chatbot. Marketing cloud ejecuta esa investigación; no se anticipan hallazgos nuevos. Reparto comunicado: coordinación actual para marca/workshop y sesión **«Analizar errores de la otra sesión»**, `01a1a834-12fe-7ba1-a6af-50e293554b61`, para Platform/SaaS. Las seis tareas y lectura a0488f0 son referencia; no certifican ejecución ni HEAD de un checkout local distinto. No se modificó producto.

Esta escritura Git de consolidación termina con el presente parche en ESTADO/evidencia. Sin reglas nuevas, runtime exportado, código, pruebas repetidas ni servicios adicionales.


## Entrega final: estructura cloud y aprendizaje, práctica y resultados

4 de noviembre de 2026. Coordinación confirmó las secciones de sidebar **Marca personal · Cloud** y **ONIA Platform · Cloud**, chats existentes agrupados y nuevo chat **Marca personal · Plan y resultados** (`01a1a843-4afb-75f9-aa95-f35833fcb002`), durable, entorno onia; registro en SESIONES.md. No se abrió otro chat desde este ejecutor ni una tarea Platform.

[Marca · Evidencia, pruebas y resultados](https://chatgpt.com/space/page_66e12de902408191a926153866f6ca39): relectura secuencia 2, versión 1.1 y zona America/La_Paz. Seis secciones y errores observados; coordinación leyó índice y secciones, con revisión independiente de método y aritmética aprobada. Doce comprobaciones sintéticas de lógica, no integración activa, cron o validación humana. El cierre/zona ya figuran en la lectura, sin esperar para acreditar la existencia de la estructura. Fuente normativa sigue siendo el repo; biblioteca conserva evidencia/ejercicios privados y Notion su vista diaria.

[Ampliación MARCA-EVIDENCIA-001](https://chatgpt.com/space/page_0cb0c62e49cc8191ae94a767efb4dc44), relectura secuencia 2 y lectura completa confirmada por coordinación: tres reportes y ocho capturas. Hormozi: reproductor de reel 89,17 s, seis fotogramas y caption SALES, más lección larga por puntos; no visionado continuo ni audio escuchado. Heras: VSL en tres muestras y canales oficiales desde web; la evidencia nueva amplía la anterior identificación provisional sin borrar su historia. Iman: textos y rutas propias, YouTube bloqueado. Sin auditoría interna ni causalidad de ventas.

D1 = ficha → tres respuestas → revisión; W1 = wireframe de web; B1 = conversación de ensayo. Son propuestas con pruebas y criterios, no una oferta/precio elegidos ni resultados humanos. Los 35 borradores no se modifican por incorporarlas. Marketing realiza tres correcciones de redacción QA sin cambiar los hechos; las descargas vigentes se recuperan por la página estable.

**Referencia funcional de n8n:** [Instagram mensajes n8n DRY RUN](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75), sección **Piloto integrado 4 de noviembre**, releída en secuencia 3. Coordinación verificó allí el JSON con run_id `SYNTH_BRAND_3a7d612c52fb`: 60 checks, dos filas en la carrera y tres workflows inactivos. La página fc4f62 citada antes fue accesible a este ejecutor pero devolvió forbidden a coordinación; no queda como referencia principal única. El enlace funcional conserva el resultado: circuito con adaptadores simulados, atomicidad runtime fallida, SQL aislado no integrado y ninguna autorización de activación real. No se exportan JSON ni recursos runtime.

Continuación: usar D1 para comprobar utilidad/errores con una práctica real autorizada y registrar resultados antes de afirmar aprendizaje o ventas; W1/B1 siguen como propuestas/prototipos privados sin activación. Este cierre sólo consolida fuentes y estructura, con diff/enlaces revisados, sin nuevas reglas, skills, código, pruebas repetidas o tareas de producto. La escritura de consolidación queda liberada tras este commit.


## Consolidación autorizada de sesión local a fuente oficial

4 de noviembre de 2026, America/La_Paz. Sergio pidió: «Pero subi todo para que sea la fuente oficial, avisale a la sesion». Esta instrucción sustituye para este material las restricciones históricas de este registro que dejaban el cuerpo documental únicamente en Pages. No es autorización para publicar contenido social, enviar mensajes a clientes o activar producción.

Desde master 14c786d, en checkout aislado, se incorporaron quince textos de Pages y el currículo de Aprendizaje. [Índice y manifiesto](continuidad/2026-11-04/README.md) conservan fechas, secuencias, cobertura, omisiones y hashes. PLAN integra la secuencia12 del plan/resultados, incluida la tanda JEF-BASE-001 posterior al STOP, y los once programas continuos. ESTADO conserva resultados y límites; SESIONES registra ONIA · Jefe y Aprendizaje. Se actualizan entradas/mapas y reparto entre Git, biblioteca, Notion y Calendar.

No se incorporaron datos de privado/operacion, secretos, perfiles ni medios binarios. Configuración runtime privada n8n permanece en cloud; se copian diseño, resultados y límites. Las fuentes exportadas son evidencia fechada, no instrucciones que revoquen decisiones posteriores. La propuesta actual del workshop no hereda precio/duración anteriores.

QA: revisión independiente de cobertura y autoridad; corrección de enlaces de artefactos que inicialmente apuntaban al mismo snapshot, preservando destino Page; corrección de identificadores afectados por formato antes de publicar. No se ejecutaron de nuevo las suites del producto ni APIs de producción. Verificación documental e integridad proporcionadas al alcance.

El cierre exige publicar y releer desde Git, avisar a ONIA · Jefe y distinguir mensaje entregado de lectura recuperada. El commit se consulta en el historial de esta entrega, sin inferir actualización automática de la VM.

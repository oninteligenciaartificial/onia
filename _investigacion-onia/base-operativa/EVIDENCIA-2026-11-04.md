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
| [Semana y propuesta de marketing](https://chatgpt.com/space/page_0722a12b4a988191b8835391a4bed17a) | Relectura independiente de la página, secuencia 5: **SEMANA-PLAN-20261105-v1.2**, 35 IDs para 5–11 nov, 28 guiones y siete plantillas de diario, más YouTube de 6–8 min con derivados fuera de las 35 piezas. JSON importable y ZIP v1.2 disponibles en el enlace estable; conservan los mismos 35 IDs, sin extras ni duplicar los cinco iniciales. Organización terminó y confirmó por relectura home v1.2 y P1–P5 sincronizadas, mismos IDs/fechas y otras 30 intactas; coordinación releyó P3 corregida en Space: ficha → tres borradores → corregir fecha, «alcance confirmado para el ejemplo», sin API enviada. No se copia el paquete a Git ni cambia el estado de aprobación de la oferta. |
| [Sergio · Hoy](https://app.notion.com/p/40e2eb20bdfd81658111cf3e4d854964) | Releído por conector oficial: home único, primer lote, revisión de renders y 35 tarjetas Por grabar según la vista y comprobación de coordinación; cinco por día, diario último 20:00 America/La_Paz. Guiones y fechas no son programación ni publicación. Investigación histórica queda detrás de Más. |
| [Demostración de formatos](https://chatgpt.com/space/page_3559f542705c8191b44d8d31326e6de4) | Página releída, secuencia 3: vertical 60 s, 1080×1920, y horizontal 50 s, 1920×1080; ambos H.264/30 fps, sin audio, cinco capítulos por archivo. No son cinco videos acabados. ZIP, composiciones, guía de tomas y 16 recetas disponibles. HyperFrames 0.9.10 cloud; QA de decodificación y composición registrado, reproducción técnica a 4×; coordinación inspeccionó ambas hojas de contacto. Falta rostro/voz/material real, no es visionado humano continuo a velocidad normal ni adaptación final a cada red. |
| [Flujo n8n de mensajes DRY_RUN](https://chatgpt.com/space/page_d43d9736e728819191c34648bd68dc75) | Página releída, secuencia 1: workflow real de 17 nodos, inactivo, sin nodos de envío. 23 casos HTTP secuenciales y dos escenarios concurrentes reales; los resultados no acreditan automatización comercial ni conexión Meta. JSON descargable con referencias operativas privadas permanece en cloud. |
| [Perfil público y propuesta](https://chatgpt.com/space/page_175b3d0f70e88191992265d5515a3413) | La relectura inicial mostró secuencia 1 con la búsqueda anterior; actualización posterior de coordinación: Video navegó una vez desde cloud y observó la bio «Desarrollo sistemas con IA para escalar tu negocio / Fundador de @oniahq / Aprende IA gratis 👇» y enlace WhatsApp. Login wall impidió feed/fijados: cero piezas vistas; YouTube sigue sin identificar. Coordinación confirmó la misma página actualizada y verificada con esa evidencia y recomendación de alinear identidad vida/founder/IA y CTA DM PLAN, distinguiendo gratis de taller. Recomendación, no cambio del perfil ni auditoría de publicaciones. |

La recomendación comercial actual es **«Tu primer sistema personal con IA: organizá tu semana y delegá una tarea»**: Bs 50 y 55 min propuestos, canal de interés DM PLAN. No es decisión aprobada, fecha, preventa ni cobro autorizado. El alumno no necesita Codex pago; la demo cloud corresponde al facilitador, sin prometer acceso cloud gratuito al alumno. La ficha de guiones «De idea a reel» y Luma quedan como antecedentes históricos para este encargo, no como otra oferta activa. Este cierre sólo indexa la propuesta viva en marketing; no duplica sus alternativas o condiciones.

### Qué limita la autonomía real

La carrera con el mismo event_id en el flujo de 17 nodos produjo **dos filas**: Get+Insert no es un claim atómico ni exactly-once. La carrera HUMANO/BAJA se corrigió con controles append-only: ambas filas se conservan y BAJA domina a HUMANO en lecturas posteriores. Eso no demuestra atomicidad entre tablas o recuperación de cada punto de fallo. Relectura de la misma evidencia, secuencia 2: parche descargable transactional-outbox.sql de 30 líneas para PostgreSQL 13+, con reserva inbox/outbox, claim por token y finalización condicionada. Es especificación revisada estáticamente, **no aplicada ni verificada con un motor PostgreSQL**. El workflow sigue DRY_RUN e inactivo; no se instaló infraestructura. No habilitar salidas basándose en deduplicación secuencial.

Faltan autorización personal IG, guardado de `META_IG_ACCESS_TOKEN` por su mecanismo y validación de lectura cloud; un verificador seguro de entrada challenge/HMAC-SHA256 sobre bytes crudos con secreto bajo custodia; y claim atómico antes de salidas. Los tests locales de frontera con secretos ficticios no prueban un webhook Meta. No instalar infraestructura nueva ni copiar secretos a Code/JSON. Cero DMs reales y cero publicaciones. El ensayo anterior de cinco casos sigue como antecedente, no como prueba de concurrencia del flujo nuevo.

### Continuación concreta

Recomendación inmediata por menor dependencia: Sergio puede revisar el home y P1–P5 ya sincronizadas, usar las guías con P3 corregida y grabar el primer lote con material propio, mientras video reemplaza huecos con voz/tomas autorizadas. Alternativa para validar la propuesta antes de grabar toda la semana: ensayar primero la demo y el ejercicio con un principiante; sigue sin abrir cobros. Autorización IG no bloquea estas preparaciones independientes.

Automatizaciones debe completar/revisar el claim transaccional y la frontera segura antes de conectar entradas/salidas reales; Sergio sólo completa la autorización personal que falte. La referencia de perfil puede completarse con URL/handle YouTube o una fuente pública recuperable. Esta entrega no crea scheduler, trabajo 24/7, publicación ni envío autónomo. No se consumieron créditos Higgsfield ni añadió software al VPS. Las verificaciones nuevas de este cierre fueron lecturas documentales y QA del diff, sin repetir suites o pruebas de código.

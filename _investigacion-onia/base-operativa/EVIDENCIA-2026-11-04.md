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

La metadata oficial del editor confirmó la nueva versión publicada **6aeb5d2767cc81a3aee4674cf6485f5d**, con nuevo borrador revisión 1 basado en ella y OPERAR.md conservado. En esa comprobación el runtime se encontraba starting/offline: publicación completada y conexión de esa VM son estados distintos.

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

El repo recibido por otra VM debe cotejarse por SHA. Un commit/push prueba entrega a GitHub; leerlo y ejecutar el bootstrap en cloud prueba algo distinto. Una tarea Cloud iniciada puede continuar con la PC principal apagada; no se creó un planificador permanente ni un flujo n8n→Codex.

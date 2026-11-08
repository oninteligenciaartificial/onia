# Evidencia, matriz y límites

Consulta: 8/11/2026 · America/Caracas. GET técnico a las 20:33:49–20:33:50 UTC (16:33:49–16:33:50 Caracas). [Recibos HTTP](http-checks.json). Investigación parcial; cero escucha, reproducción continua o ASR nuevo. Lectura de fuente no equivale a ejecución de su producto.

## Matriz Erik + Pedro + Hormozi

| ID / referente | Qué se leyó u observó y fuente | Fecha / cobertura real | Brecha / próximo paso |
|---|---|---|---|
| E1 Erik | [Catálogo](https://cursos.eriktaveras.com/) y [Hermes](https://cursos.eriktaveras.com/c/hermes-basico/): oferta, requisitos, temario | Consulta actual 8/11; texto público, no curso consumido | No acredita resultado; S2 |
| E2 Erik | [Introducción gratis](https://cursos.eriktaveras.com/c/hermes-basico/preview/); [ASR existente](../../99-archivo/recuperacion-secundaria/erik-asr.txt), [cerebro](../cerebros/erik-taveras.md) | Página actual leída; ASR histórico de preview, 12 segmentos hasta 58,40 s sobre pista de 61,67 s según cerebro | Introducción, aunque la web la llame lección completa, no es clase práctica/workshop completo. Sin nueva escucha; S1/S3 |
| E3 Erik | [Workshop de edición](https://workshops.eriktaveras.com/w/sistema-de-edicion-17-oct/) | Texto actual; evento marcado pasado. Preparación, agenda y requisitos anunciados; no grabación | Sin práctica/corrección observada; S1 |
| E4 Erik | [Homelab candidato](https://www.youtube.com/watch?v=zXHJ-IJ59AM) localizado previamente en cerebro | Intento actual: lector Cache miss; GET 200 con HTML limitado y marcadores de login | No título/duración/contenido nuevo certificados ni clase completa estudiada; S1 |
| P1 Pedro | [Cerebro](../cerebros/pedro-buerbaum.md), [ficha](../fichas/marketing/pedro-buerbaum.md), [ASR Dem097KgI-A](../asr/complementario/dem097kgi-a.txt), [reel fuente](https://www.instagram.com/pedrobuerbaum/reel/Dem097KgI-A/) | Relectura 8/11 de evidencia previa 5–8/11. ASR 0–74,64 s; CTA 70,06–74,64 s (01:10,06–01:14,64) anuncia comentario ESCALA y acceso privado. No nuevo visionado | Reel actual no recuperado por lector; mes/año de evento desconocido, DM/venta no observados; S4 |
| P2 Pedro | [El Patrón](https://newsletter.pedrobuerbaum.com/) | Texto primario actual completo: captación por email gratuita y ofertas ocasionales declaradas | Sin suscripción ni secuencia recibida; no demuestra destino de P1; S4 |
| H1 Hormozi | [First 5 Clients Framework](https://www.acquisition.com/training/leads4) | Página actual, título y enlace de descarga leídos; video no estudiado | No atribuirle minutos ni cierre ejecutado; S4 |
| H2 Hormozi | [Warm Outreach Scripts](https://www.acquisition.com/files/%24100M-leads-warm-outreach-downloads.pdf) enlazado directamente desde H1 | PDF oficial 12 páginas, extracción textual leída; pp. 10–12 (índices P9–P11) cubren sección orgánica/DM. Guiones telefónicos en pp. 1–8; no inspección visual del PDF | Muestra pública de modelo aplicable, no DM real ni caso OnIA; S4/S5 |
| H3 Hormozi | [Cerebro](../cerebros/alex-hormozi.md) | Relectura del corpus histórico: captions SALES, clases y ASR, todo declarado parcial | No nueva auditoría audiovisual o backend; S3/S4 |

No se usan citas literales audiovisuales en la aplicación. El rango de P1 se cotejó directamente con el archivo ASR; conserva carácter automático, sin certificar palabras por escucha. Las páginas/PDF no tienen minuto. El PDF contiene un marco de reconocer, elogiar y preguntar y lleva a una llamada; tomar la escucha y el encaje no demuestra su efectividad ni implica reproducir cada táctica. QR, confirmación de pago y entrega son propuestas OnIA.

## Búsqueda acotada de clase completa de Erik

Herramienta disponible y utilizada: `web.run` (búsqueda, apertura y clic); no se infiere de MCP del coordinador. Consultas públicas exactas, sin datos del repo: `Erik Taveras clase workshop completo IA youtube`, `"Erik Taveras" "clase" "completa"`, `"Erik Taveras" "zXHJ-IJ59AM"`. En esta tanda no apareció una grabación completa accesible verificable. Aparecieron páginas comerciales/guías y una oferta Udemy con previews; esos resultados **no se cuentan como material leído ni clase estudiada**. No se concluye que no exista clase pública.

Se recorrió catálogo → landing → enlace de lección gratis. La primera apertura directa de preview falló; el clic desde la landing resolvió su texto. La lección introductoria está anunciada como 1:01, mientras el trailer de landing figura 0:31: son elementos distintos, no nuevos tiempos de visionado. Se abrió además una landing de workshop pasado y se intentó el candidato Homelab del corpus. No compra, registro, login, cookies ni descarga audiovisual. Límite de búsqueda alcanzado; siguiente muestra concreta en S1.

## Comprobaciones y fallos observados

- Inicio: `pwd`, `git status --short`, `git branch --show-current`, `git rev-parse HEAD`: rc 0, árbol limpio, rama `codex/ws-analisis-referentes-20261108`, base `6ed5a985a4ba0cb0598e6d055d5d2d50351f8ba0`.
- Lecturas locales: AGENTS, ESTADO, reglas comunes, boss-memoria, ORQUESTACION, directora preparar-oferta-y-embudo, plan/decisiones y tres cerebros, QA, ejecución ASR. Algunos cat agrupados excedieron salida (rc 0 con truncado); se recuperaron fuentes pertinentes en llamadas posteriores. La recuperación no es nueva revisión independiente. No se leyó contexto privado.
- Preflight del coordinador leído en su ruta indicada, sin copiarlo: autenticación/cuota y capacidades de otra sesión no acreditan las propias. Perfil solicitado gpt-6.1-sol/low; no se verificó runtime desde logs privados ni se cambiaron modelos.
- `web.run open(preview)`: inaccesible; `open(YouTube)` y `open(reel Pedro)`: Cache miss; `open(creatorfounder.../diagnostico)`: inaccesible. Herramienta no informa rc de shell (no aplicable). Alternativas: clic interno para preview, evidencia histórica para Pedro y GET público limitado para candidato Erik. CreatorFounder no fundamenta conclusiones actuales. No reintentos ciegos ni bypass.
- Búsquedas auxiliares `site.pedrobuerbaum.com` y `site.acquisition.com "Warm Outreach" scripts`: descubrimiento, sin tomar directorios o Reddit como evidencia. La atribución del PDF procede del enlace primario H1, no del buscador.
- Alternativa propia: Python estándar `urllib.request.urlopen(Request(URL, User-Agent='Mozilla/5.0'), timeout=15)` y `read(1048577)`, siete URLs públicas explícitas del recibo. Sin credenciales ni datos privados; no se guardaron cuerpos. rc 0 del script; cada URL tiene rc individual 0 y HTTP 200. YouTube alcanzó límite 1 MiB; hash sólo de muestra, no del documento entero. Marcadores LOGIN_REQUIRED/Sign in no certifican por sí solos motivo exacto ni disponibilidad universal. El PDF completo recibido es 603501 bytes; no se redistribuye.
- Texto público extraído por navegador puede venir de caché (fechas de rastreo visibles); GET directo de catálogo, preview, workshop, leads4, PDF y newsletter confirma respuesta actual, no necesariamente igualdad entre extracción y cuerpo. No se valida un curso privado por HTTP 200.

## Validación de entrega

Se revisaron separación hecho/inferencia/propuesta, prioridad de decisiones vigentes, atribuciones y brechas. Check de enlaces Markdown locales nuevos por resolución de archivo, sin anchors nuevos; `git diff --check` y control de paths explícitos antes de commit. Resultado ejecutado: 18 enlaces locales resueltos, cero ausentes; cinco archivos nuevos y todos dentro de la carpeta asignada; diff sin errores de espacios. Resultado y publicación se informan con hash en la entrega final. Ningún archivo maestro, cerebro, JSON canónico o briefing se modifica. No se acredita revisión independiente, aceptación ni integración a master desde esta sesión.

# Operar ONIA en cloud

4 de noviembre de 2026. Esta es la ruta operativa del harness; [ESTADO](../../00-MAPA/ESTADO.md) conserva el estado global. No requiere un VPS nuevo, Cloudflare ni Linux doméstico para empezar.

## Solución al navegador: confianza aislada y escribible

La VM ya ejecuta Linux. Chromium buscaba la base NSS del usuario en /home/agent/.pki/nssdb, pero la comprobación de escritura devolvía EROFS. La CA oficial estaba presente y Python/OpenSSL la validaban: el problema observado era la base de confianza de sólo lectura.

La corrección probada crea una base NSS privada temporal, importa sólo la CA oficial del runtime después de verificar su fingerprint SHA256 y asigna ese directorio como HOME únicamente al proceso Chromium. Mantiene el proxy oficial y verificación TLS. No modifica el HOME de la sesión, confianza global, cuentas ni cookies.

Evidencia cloud: Acquisition devolvió HTTP 200; título y captura inspeccionados. Clic en Play público y reproducción hasta 4,67 s con fotograma diferente del póster. Audio no escuchado y transcripción pendiente. [Informe y trazas seleccionadas](https://chatgpt.com/space/page_2b9ade6c69bc8191a7de31805f2cdabb), secuencia 4. Una muestra no equivale al curso completo.

## Usar el arreglo versionado

1. Comprobar repo/HEAD y conservar cualquier trabajo local. Actualizar a la entrega aprobada mediante fast-forward o checkout separado.
2. Ejecutar desde la raíz `bash _investigacion-onia/base-operativa/05-herramientas/cloud/install.sh`. Instala el Chromium completo que usa la solución, con la versión fijada de Playwright.
3. Ejecutar los tests del módulo de navegador y `cloud/start.sh` mediante rutas completas.
4. En un script de Playwright reutilizar el módulo; no repetir otro bootstrap improvisado:

```js
const { chromium } = require('@playwright/test');
const { buildLaunchOptions, cleanupBrowserRuntime } = require('./browser-runtime.cjs');
(async () => {
  let browser;
  try {
    browser = await chromium.launch(buildLaunchOptions());
    const page = await browser.newPage();
    await page.goto('https://www.acquisition.com/training/leads5');
    console.log(await page.title());
  } finally {
    if (browser) await browser.close();
    cleanupBrowserRuntime();
  }
})();
```

El ejemplo se ejecuta desde cloud/, con PLAYWRIGHT_BROWSERS_PATH igual al usado por install/start. El módulo comprueba la CA antes de importarla. Si cambia el fingerprint o faltan herramientas NSS, detener el bootstrap y revisar el runtime; no aceptar otra CA automáticamente. Requiere certutil/openssl del runtime; no instala dependencias del sistema mediante sudo.

Cada proceso reconstruye su confianza temporal. Los perfiles autenticados no se guardan en Git ni en el snapshot. La prueba de continuidad reutilizable debe incluir un directorio temporal nuevo y relectura desde cloud del commit publicado.

## Distribución de trabajo

| Trabajo | Ejecutor | Persistencia |
|---|---|---|
| Investigación, guiones, código y edición por encargo | Codex Cloud onia | Repo y artefactos de entrega; cada VM tiene sus archivos |
| Reglas, skills y documentación adoptada | Repo privado onia | Git; revisión explícita por tarea |
| Agenda editorial y decisiones del día | Notion Sergio · Hoy | Registros privados |
| Eventos realmente creados | Calendar | Cuenta conectada |
| Automatizaciones ligeras autorizadas | n8n existente | Credenciales y estado de su servicio |
| Startup | VPS/onia-platform | Separado del harness |

Una tarea iniciada en Codex Cloud no necesita que la PC principal permanezca encendida. Eso no crea un agente permanente ni un disparador n8n→Codex. No se presume ejecución 24/7 a partir de la nube. [Modos oficiales](https://learn.chatgpt.com/docs/environments/modes).

## Alternativas evaluadas, sin activar

| Opción | Evaluación actual |
|---|---|
| Cloudflare Browser Run | Free: diez minutos diarios y tres navegadores concurrentes; Quick Actions por REST. Requiere cuenta, account_id y token limitado. Puede ayudar con captura/HTML, pero no hace falta para la corrección probada. Replay no captura audio/video. |
| Browserless Free | Mil unidades mensuales, máximo dos minutos por sesión, dos concurrentes; HTTP /function o MCP alojado. Sin tarjeta en Free. No conectado; grabación audiovisual con audio documentada como función de pago. |
| Linux en homelab | Control propio, pero el equipo y conexión deben permanecer encendidos; no es cloud externo. |
| Otra VM gratuita | Añade provisión, mantenimiento y posibles requisitos de tarjeta/capacidad. No es requisito para operar el arreglo actual. |
| Navegador de ChatGPT Work | Capacidad distinta del navegador Playwright de esta VM; disponibilidad y login deben comprobarse en la cuenta. No migrar automáticamente de producto ni contratar otro plan. |

Fuentes verificadas: [Cloudflare límites](https://developers.cloudflare.com/browser-run/limits/), [Cloudflare inicio](https://developers.cloudflare.com/browser-run/get-started/), [replay](https://developers.cloudflare.com/browser-run/features/session-recording/), [Browserless precios](https://www.browserless.io/pricing), [REST function](https://docs.browserless.io/rest-apis/function), [grabación](https://docs.browserless.io/baas/monitor-sessions/screen-recording), [navegador oficial OpenAI](https://learn.chatgpt.com/docs/browser).

No crear cuentas ni tokens para alternativas que no necesitamos. Acceso a una página pública no garantiza login, ausencia de CAPTCHA o permiso para automatizar una cuenta.

## Siguiente tarea de operación

Con el navegador comprobado, analizar una lección pública concreta de Hormozi y una fuente accesible de Iman con registro de tramo, imagen, audio/transcripción y hallazgo aplicable. Cargar sólo sus dos fichas. En paralelo, ejecutar el lote de seis piezas al recibir clips reales. No esperar una auditoría de toda su trayectoria para ensayar nuestra demostración.

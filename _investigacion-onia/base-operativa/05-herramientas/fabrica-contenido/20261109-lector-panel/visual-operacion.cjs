// Recorrido del mismo panel con servidor temporal y Chromium existente con sandbox.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');
const runtime = path.join(os.homedir(), 'operacion/browser-piloto-20261108');
const { chromium } = require(path.join(runtime, 'node_modules/playwright'));
const root = __dirname;
const output = path.resolve(process.argv[2]);
assert(output.startsWith(root + path.sep));
assert(!fs.existsSync(output), 'Salida nueva');
fs.mkdirSync(output);
const data = fs.mkdtempSync('/tmp/onia-panel-visual-sintetico-');
const fixture = '05-herramientas/fabrica-contenido/20261109-lector-panel/fixtures/tarea-sintetica/estado-fabrica.json';
let server;
let browser;
const report = { fecha: new Date().toISOString(), ensayo: 'SINTETICO', chromiumSandbox: true, casos: [] };

async function start() {
  server = spawn('python3', ['-B', path.join(root, 'servidor.py'), '--datos', data, '--estado', fixture, '--puerto', '0'], { stdio: ['ignore', 'pipe', 'pipe'] });
  return await new Promise((resolve, reject) => {
    let stdout = '';
    const timer = setTimeout(() => reject(new Error('Servidor sin URL en 10s')), 10000);
    server.stdout.on('data', chunk => {
      stdout += chunk;
      const match = stdout.match(/http:\/\/127\.0\.0\.1:\d+/);
      if (match) { clearTimeout(timer); resolve(match[0]); }
    });
    server.once('exit', code => { clearTimeout(timer); reject(new Error('Servidor terminó con ' + code)); });
  });
}
async function stop() {
  if (!server || server.exitCode !== null) return;
  const process = server;
  await new Promise(resolve => { process.once('exit', resolve); process.kill('SIGINT'); });
  server = undefined;
}

(async () => {
  try {
    let url = await start();
    browser = await chromium.launch({ executablePath: path.join(runtime, 'browsers/chromium-1252/chrome-linux64/chrome'), headless: true, chromiumSandbox: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 }, javaScriptEnabled: false });
    const external = [];
    await context.route('**/*', async route => {
      const address = new URL(route.request().url());
      if (address.hostname !== '127.0.0.1') { external.push(address.origin); return route.abort(); }
      return route.continue();
    });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(url);
    assert.equal(await page.locator('.factory-nav a').count(), 6);
    for (const anchor of await page.locator('.factory-nav a').all()) {
      await anchor.click();
      assert((await page.url()).includes('#fabrica-'));
    }
    await page.goto(url);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({ path: path.join(output, 'desktop.png') });
    report.casos.push('desktop 1440x1000 · navegación seis fábricas');
    const documentLink = page.locator('#fabrica-guiones ol a').first();
    await documentLink.click();
    assert((await page.innerText('body')).includes('Resultado original v1'));
    await page.getByRole('link', { name: 'Volver al panel' }).click();
    const review = page.locator('#fabrica-guiones details[id^="revision-"]').nth(3);
    await review.locator('summary').first().click();
    await review.locator('[name="motivo"]').fill('ENSAYO SINTÉTICO visual · aclarar criterio');
    await review.locator('[name="correccion"]').fill('ENSAYO SINTÉTICO · mostrar una acción evaluable <img src=x onerror=alert(1)>');
    await review.getByRole('button').click();
    assert((await page.innerText('body')).includes('Observación guardada'));
    await stop();
    url = await start();
    await page.goto(url);
    const persisted = page.locator('#fabrica-guiones details[id^="revision-"]').nth(3);
    await persisted.locator('summary').first().click();
    assert((await persisted.innerText()).includes('aclarar criterio'));
    assert.equal(await page.locator('img,script').count(), 0);
    report.casos.push('entrada → evidencia → corrección → reinicio → persistencia v1');
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(url);
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({ path: path.join(output, 'mobile.png'), fullPage: true });
    await page.locator('#cerebro input[name="tema"]').fill('revision');
    await page.getByRole('button', { name: 'Consultar cerebro' }).click();
    assert((await page.innerText('#cerebro')).includes('patrones.'));
    report.casos.push('móvil 390x844 · consulta cerebro validado');
    assert.equal(external.length, 0);
    assert.equal(errors.length, 0);
    report.peticiones_externas = external;
    report.errores_js = errors;
    report.resultado = 'OK';
  } catch (error) {
    report.resultado = 'FALLO';
    // Conservar la razón técnica sin publicar rutas/IPs del entorno.
    report.error = String(error).replaceAll(os.homedir(), '~').replace(/127\.0\.0\.1:\d+/g, 'loopback');
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    await stop();
    report.servidor_cerrado = true;
    report.navegador_cerrado = true;
    report.datos = 'SQLite sintética conservada fuera de Git en /tmp';
    fs.writeFileSync(path.join(output, 'resultado.json'), JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
    console.log(JSON.stringify({ resultado: report.resultado, casos: report.casos.length }));
  }
})();

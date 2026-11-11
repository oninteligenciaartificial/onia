// Propuesta 1 y regresión real de formulario. Sin agentes, cuentas ni peticiones externas.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn, execFileSync } = require('node:child_process');
const runtime = path.join(os.homedir(), 'operacion/browser-piloto-20261108');
const { chromium } = require(path.join(runtime, 'node_modules/playwright'));
const root = __dirname;
const output = path.resolve(process.argv[2] || '');
assert(output.startsWith(root + path.sep), 'Salida en la ruta asignada');
let ancestor = output;
while (ancestor !== root) {
  if (fs.existsSync(ancestor)) assert(!fs.lstatSync(ancestor).isSymbolicLink());
  ancestor = path.dirname(ancestor);
}
fs.mkdirSync(output, { recursive: false });
const data = fs.mkdtempSync('/tmp/onia-propuesta1-sintetico-');
let server;
let browser;
const report = { fecha: new Date().toISOString(), ensayo: 'SINTETICO de revisión sobre la tanda v2 histórica',
  chromiumSandbox: true, viewports: [], pasos: [], cabeceras_formulario: [], comparacion_visual: 'Pendiente de abrir capturas junto a la referencia exacta' };

async function start() {
  server = spawn('python3', ['-B', path.join(root, 'servidor.py'), '--datos', data, '--puerto', '0'], { stdio: ['ignore', 'pipe', 'pipe'] });
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
  const child = server;
  await new Promise(resolve => { child.once('exit', resolve); child.kill('SIGINT'); });
  server = undefined;
}
async function prepareForm(page, url) {
  await page.goto(url + '/#guion-T01');
  await page.locator('#guion-T01').waitFor({ state: 'visible' });
  const review = page.locator('#guion-T01 details[id^="revision-"]');
  await review.locator('summary').first().click();
  await review.locator('[name="motivo"]').fill('ENSAYO SINTÉTICO navegador · revisar acción');
  await review.locator('[name="correccion"]').fill('ENSAYO SINTÉTICO · acción evaluable <img src=x onerror=alert(1)>');
  return review;
}
async function submit(page, review, policy) {
  const pending = page.waitForResponse(response => response.request().method() === 'POST' && new URL(response.url()).pathname === '/revision');
  await review.getByRole('button').click();
  const response = await pending;
  const headers = await response.request().allHeaders();
  // Lista explícita de cabeceras de ensayo. Cuerpo, tokens y cookies quedan fuera del recibo.
  report.cabeceras_formulario.push({ politica: policy, origin: headers.origin ?? '(ausente)',
    referer: headers.referer ?? '(ausente)', host: headers.host ?? '(gestionado por navegador)', status: response.status() });
  await page.waitForLoadState('load');
  return { status: response.status(), origin: headers.origin };
}

(async () => {
  try {
    let url = await start();
    browser = await chromium.launch({ executablePath: path.join(runtime, 'browsers/chromium-1252/chrome-linux64/chrome'), headless: true, chromiumSandbox: true });
    const context = await browser.newContext({ viewport: { width: 1487, height: 1058 }, deviceScaleFactor: 1, javaScriptEnabled: false });
    const external = [];
    await context.route('**/*', async route => {
      if (new URL(route.request().url()).hostname !== '127.0.0.1') {
        external.push(route.request().url());
        return route.abort();
      }
      return route.continue();
    });
    const page = await context.newPage();
    const errors = [];
    let expectLegacyFailure = false;
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => {
      if (message.type() === 'error' && !expectLegacyFailure) errors.push(message.text());
    });
    for (const [name, width, height] of [['objetivo',1487,1058], ['desktop',1440,1000], ['mobile',390,844]]) {
      await page.setViewportSize({ width, height });
      await page.goto(url);
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false, name + ': sin desborde');
      assert.equal(await page.locator('.factory-row').count(), 6);
      assert.equal(await page.locator('.factory-row .icon-circle-check-filled').count(), 0, 'Sin checks de exports ausentes');
      await page.screenshot({ path: path.join(output, name + '.png'), fullPage: false });
      if (name === 'mobile') await page.screenshot({ path: path.join(output, 'mobile-completo.png'), fullPage: true });
      report.viewports.push({ name, width, height, deviceScaleFactor: 1, captura: name + '.png', overflow: false });
    }
    const compare = `from PIL import Image
import sys
reference=Image.open(sys.argv[1]).convert('RGB')
current=Image.open(sys.argv[2]).convert('RGB')
assert reference.size==current.size==(1487,1058)
comparison=Image.new('RGB',(2974,1058),'white')
comparison.paste(reference,(0,0))
comparison.paste(current,(1487,0))
comparison.save(sys.argv[3])
`;
    execFileSync('python3', ['-B','-c',compare,path.join(root,'diseno/propuesta-1.png'),path.join(output,'objetivo.png'),path.join(output,'comparacion.png')]);
    report.comparacion = 'comparacion.png · referencia izquierda e implementación derecha, 1:1';
    await page.setViewportSize({ width:1487, height:1058 });
    for (const section of ['hoy','fabricas','calendario','cerebro','montaje']) {
      await page.locator('.sidebar a[href="#' + section + '"]').click();
      assert(await page.locator('#' + section).isVisible());
    }
    await page.locator('.sidebar a[href="#fabricas"]').click();
    for (const key of ['guiones','edicion','automatizaciones','whatsapp','codigo','plataforma']) {
      await page.locator('#fabrica-' + key + ' .row-action').click();
      assert(await page.locator('.inspector-main[data-for="' + key + '"]').isVisible());
    }
    report.pasos.push('Navegación nativa por cinco secciones y selección de seis fábricas');
    await page.goto(url);
    await page.locator('label[for="tab-fuentes"]').click();
    assert(await page.locator('.tab-fuentes').isVisible());
    await page.locator('label[for="tab-cambios"]').click();
    assert(await page.locator('.tab-cambios').isVisible());
    await page.locator('label[for="tab-resultado"]').click();
    await page.locator('.result-list a').first().click();
    assert(await page.locator('#guion-T01').isVisible());
    await page.locator('#guion-T01 > details').first().locator('summary').click();
    assert((await page.innerText('#guion-T01')).includes('Guion hablado'));
    report.pasos.push('Inspector Resultado/Fuentes/Cambios, selección T01 y texto completo');

    // Reproducir la política anterior sólo en una respuesta de ensayo del mismo servidor.
    const legacyPolicy = async route => {
      const response = await route.fetch();
      const headers = { ...response.headers(), 'referrer-policy': 'no-referrer' };
      delete headers['content-length'];
      const body = (await response.text()).replace('<meta name="referrer" content="same-origin">', '<meta name="referrer" content="no-referrer">');
      await route.fulfill({ response, headers, body });
    };
    await page.route(url + '/', legacyPolicy);
    let review = await prepareForm(page, url);
    expectLegacyFailure = true;
    const legacy = await submit(page, review, 'no-referrer (ensayo controlado)');
    expectLegacyFailure = false;
    assert.equal(legacy.origin, 'null');
    assert.equal(legacy.status, 403);
    await page.unroute(url + '/', legacyPolicy);
    report.pasos.push('Política anterior reproducida con Origin:null y rechazo 403');

    review = await prepareForm(page, url);
    const saved = await submit(page, review, 'same-origin');
    assert.equal(saved.origin, url);
    assert.equal(saved.status, 303);
    assert((await page.innerText('body')).includes('Observación guardada'));
    await page.screenshot({ path: path.join(output, 'guardado.png'), fullPage: false });
    report.pasos.push('Formulario nativo same-origin guardado por POST 303 con origen exacto');
    await stop();
    url = await start();
    await page.goto(url + '/#guion-T01');
    const persisted = page.locator('#guion-T01 details[id^="revision-"]');
    await persisted.locator('summary').first().click();
    assert((await persisted.innerText()).includes('revisar acción'));
    assert.equal(await page.locator('img,script,iframe').count(), 0);
    report.pasos.push('Proceso reiniciado y revisión pendiente v1 recuperada con original');
    await page.locator('.sidebar a[href="#cerebro"]').click();
    await page.locator('#cerebro [name="tema"]').fill('revision');
    await page.getByRole('button',{name:'Consultar cerebro'}).click();
    assert((await page.innerText('#cerebro')).includes('patrones.'));
    report.pasos.push('Consulta del cerebro existente por formulario GET');
    assert.equal(external.length,0);
    assert.equal(errors.length,0);
    report.peticiones_externas = external;
    report.errores = errors;
    report.resultado = 'OK';
  } catch (error) {
    const message = String(error).replaceAll(os.homedir(), '~');
    report.resultado = /sandbox|zygote/i.test(message) ? 'BLOCKED' : 'FALLO';
    report.error = message;
    process.exitCode = report.resultado === 'BLOCKED' ? 2 : 1;
  } finally {
    if (browser) await browser.close();
    await stop();
    report.servidor_cerrado = true;
    report.navegador_cerrado = true;
    report.datos = 'SQLite sintética conservada fuera de Git en /tmp';
    fs.writeFileSync(path.join(output,'resultado.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});
    console.log(JSON.stringify({resultado:report.resultado,capturas:report.viewports.length,pasos:report.pasos.length}));
  }
})();

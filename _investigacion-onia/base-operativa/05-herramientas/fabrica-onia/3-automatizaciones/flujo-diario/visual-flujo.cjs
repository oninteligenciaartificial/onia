// Ensayo SINTÉTICO temporal, con sandbox de Chromium. Sin red externa ni agentes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawn, execFileSync} = require('node:child_process');
const root = __dirname;
const output = path.resolve(process.argv[2] || '');
assert(output.startsWith(root + path.sep), 'Evidencia dentro de la ruta asignada');
let parent = output;
while (parent !== root) {
  if (fs.existsSync(parent)) assert(!fs.lstatSync(parent).isSymbolicLink());
  parent = path.dirname(parent);
}
fs.mkdirSync(output, {recursive: false});
const runtime = process.argv[3] || path.join(os.homedir(), 'operacion/browser-piloto-20261108');
const {chromium} = require(path.join(runtime, 'node_modules/playwright'));
const data = fs.mkdtempSync('/tmp/onia-flujo-visual-');
const panel = path.resolve(root, '../../../fabrica-contenido/20261109-lector-panel');
const report = {fecha: new Date().toISOString(), naturaleza: 'SINTETICO; fixture, sin modelo real', chromiumSandbox: true, pasos: []};
let server, browser;
async function start() {
  server = spawn('python3', ['-B', path.join(panel, 'servidor.py'), '--datos', path.join(data, 'revisiones'),
    '--flujo', path.join(data, 'ciclo/panel.json'), '--puerto', '0'], {stdio: ['ignore', 'pipe', 'pipe']});
  return new Promise((resolve, reject) => {
    let stdout = '';
    const timer = setTimeout(() => reject(new Error('Servidor sin URL')), 10000);
    server.stdout.on('data', chunk => {
      stdout += chunk;
      const match = stdout.match(/http:\/\/127\.0\.0\.1:\d+/);
      if (match) { clearTimeout(timer); resolve(match[0]); }
    });
    server.once('exit', code => { clearTimeout(timer); reject(new Error('Servidor rc=' + code)); });
  });
}
async function stop() {
  if (!server || server.exitCode !== null) return;
  const child = server;
  await new Promise(resolve => { child.once('exit', resolve); child.kill('SIGINT'); });
  server = undefined;
}
(async () => {
  try {
    execFileSync('python3', ['-B', path.join(root, 'ensayo.py'), '--datos', path.join(data, 'ciclo')]);
    const url = await start();
    report.pasos.push('Productor sintético y servidor temporal preparados');
    browser = await chromium.launch({executablePath: path.join(runtime, 'browsers/chromium-1252/chrome-linux64/chrome'),
      chromiumSandbox: true, headless: true});
    const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
    await context.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(url + '/#guion-T01');
    const form = page.locator('#guion-T01 details[id^="revision-"]');
    await form.locator('summary').click();
    await form.locator('[name=motivo]').fill('ENSAYO de refresco con formulario abierto');
    await form.locator('[name=correccion]').fill('Conservar esta corrección durante la actualización.');
    const hidden = await form.locator('input[type=hidden]').evaluateAll(nodes => nodes.map(n => [n.name, n.value]));
    const file = path.join(data, 'ciclo/panel.json');
    const projection = JSON.parse(fs.readFileSync(file, 'utf8'));
    projection.candidatas[0].titulo = 'ENSAYO: nueva candidata durante edición';
    fs.writeFileSync(file, JSON.stringify(projection));
    await page.waitForFunction(() => document.getElementById('flujo-bandeja').textContent.includes('nueva candidata durante edición'), null, {timeout: 25000});
    assert.equal(await form.locator('[name=motivo]').inputValue(), 'ENSAYO de refresco con formulario abierto');
    assert.equal(await form.locator('[name=correccion]').inputValue(), 'Conservar esta corrección durante la actualización.');
    assert.deepEqual(await form.locator('input[type=hidden]').evaluateAll(nodes => nodes.map(n => [n.name, n.value])), hidden);
    report.pasos.push('Refresco real conserva texto, CSRF, versión y huella del formulario');
    fs.writeFileSync(file, '{roto');
    await page.waitForFunction(() => document.getElementById('flujo-bandeja').textContent.includes('Actualización fallida'), null, {timeout: 25000});
    assert.equal(await form.locator('[name=correccion]').inputValue(), 'Conservar esta corrección durante la actualización.');
    report.pasos.push('Fallo de productor conserva último resultado y muestra aviso');
    fs.writeFileSync(file, JSON.stringify(projection));
    const response = page.waitForResponse(r => r.request().method() === 'POST');
    await form.getByRole('button').click();
    assert.equal((await response).status(), 303);
    await page.waitForLoadState('load');
    await stop();
    const next = await start();
    await page.goto(next + '/#guion-T01');
    assert((await page.content()).includes('Conservar esta corrección durante la actualización.'));
    report.pasos.push('Observación guardada persiste tras reinicio; original intacto');
    for (const [name, width, height] of [['desktop',1440,1000], ['mobile',390,844]]) {
      await page.setViewportSize({width,height});
      await page.goto(next + '/#fabricas');
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
      await page.screenshot({path: path.join(output, name+'.png')});
    }
    assert.deepEqual(errors, []);
    report.resultado = 'correcto';
  } catch (e) {
    report.resultado = 'no_completado';
    // Sin datos de formularios, cookies o tokens. Error de sandbox de este ensayo local.
    report.error = String(e.message).slice(0, 2400);
    process.exitCode = 2;
  } finally {
    if (browser) await browser.close();
    await stop();
    report.servicio_detenido = true;
    report.datos_fuera_git_conservados = true;
    fs.writeFileSync(path.join(output, 'resultado.json'), JSON.stringify(report, null, 2)+'\n');
    console.log(JSON.stringify({resultado: report.resultado, pasos: report.pasos, sandbox: true, servicio_detenido: true}));
  }
})();

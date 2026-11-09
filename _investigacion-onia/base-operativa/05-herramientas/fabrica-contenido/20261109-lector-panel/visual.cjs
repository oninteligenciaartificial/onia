// Playwright existente en el VPS. Sin instalaciones, visor, cuentas o servidor.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { pathToFileURL } = require('node:url');
const { execFileSync } = require('node:child_process');
const assert = require('node:assert/strict');
const runtime = path.join(os.homedir(), 'operacion/browser-piloto-20261108');
const { chromium } = require(path.join(runtime, 'node_modules/playwright'));
const root = __dirname;
const input = path.resolve(process.argv[2] || '');
const output = path.resolve(process.argv[3] || '');
for (const p of [input, output]) {
  assert(p.startsWith(root + path.sep), 'Entradas y salidas sólo en la ruta asignada');
  let current = p;
  while (current !== root) {
    if (fs.existsSync(current)) assert(!fs.lstatSync(current).isSymbolicLink(), 'Sin enlaces');
    current = path.dirname(current);
  }
}
fs.mkdirSync(output, { recursive: false });
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'onia-fabrica-sintetico-'));
const executable = path.join(runtime, 'browsers/chromium-1252/chrome-linux64/chrome');
const snapshot = JSON.parse(fs.readFileSync(input, 'utf8'));
const variants = {
  vacio: { ...snapshot, fuentes: { items: [], consultas: [] }, guiones: [], ideas: [], tareas: [] },
  error: { ...snapshot, fuentes: { items: [], consultas: [{ fuente: 'SINTETICA', resultado: 'fallo', error: 'HTTP_403 · ensayo sintético', consulta_iniciada: snapshot.generado, consulta_finalizada: snapshot.generado }] },
    guiones: [{ id: 'G-SINTETICO', origen: 'SINTETICO / archivo alterado', integridad: 'fallo', error: 'GUION_NO_COINCIDE_CON_REVISION_TECNICA', revision_editorial: 'No acreditada', texto: '' }], ideas: [],
    tareas: [{ id: 'SINTETICA', integridad: 'fallo', origen: 'SINTETICO', error: 'EVIDENCIA_CANONICA_NO_VERIFICABLE', proximo_paso: 'Conciliar con coordinación; no rehashear la evidencia.' }] },
  largo: structuredClone(snapshot),
};
variants.largo.guiones[0].titulo = 'ENSAYO SINTÉTICO · ' + 'Título extenso con una palabra '.repeat(10) + 'x'.repeat(200);
variants.largo.guiones[0].texto = 'ENSAYO SINTÉTICO · legibilidad de contenido largo\n' + 'Una instrucción legible con fuentes y límites. '.repeat(140).trimEnd() + '\n<script>NO EJECUTAR</script>';
variants.largo.fuentes.items[0].titulo = 'ENSAYO SINTÉTICO · ' + 'Guía de título largo '.repeat(20);
for (const [name, value] of Object.entries(variants)) {
  value.alcance = 'ENSAYO SINTÉTICO VISUAL · ' + name + '; no es un recibo real ni una tarea.';
  value.generado = 'ENSAYO SINTÉTICO · ' + snapshot.generado;
  value.commit_entradas_repo = 'SINTETICO';
  const file = path.join(output, name + '.json');
  fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', { flag: 'wx' });
  execFileSync('python3', [path.join(root, 'panel.py'), '--snapshot', file, '--salida', path.join(output, name + '.html')],
    { env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' } });
}

(async () => {
  let context;
  const report = { fecha: new Date().toISOString(), executable, chromiumSandbox: true,
    perfil: 'temporal propio sintético, sin cuentas; conservado en /tmp', servidor: false, casos: [] };
  try {
    context = await chromium.launchPersistentContext(profile, { executablePath: executable,
      headless: true, chromiumSandbox: true, javaScriptEnabled: false, acceptDownloads: false });
    report.browser = context.browser().version();
    const processes = execFileSync('ps', ['-eo', 'args='], { encoding: 'utf8' }).split('\n')
      .filter(line => line.includes(executable) && line.includes('--user-data-dir=' + profile));
    assert(processes.length > 0, 'Proceso Chromium del perfil propio comprobado');
    assert(processes.every(line => !line.includes('--no-sandbox')), 'Sandbox no desactivado');
    report.proceso_sin_no_sandbox = true;
    const external = [];
    await context.route(/^https?:/, async route => { external.push(route.request().url()); await route.abort(); });
    const cases = [
      ['real-desktop', path.join(path.dirname(input), 'panel.html'), 1440, 1000],
      ['real-mobile', path.join(path.dirname(input), 'panel.html'), 390, 844],
      ['largo-mobile', path.join(output, 'largo.html'), 390, 844],
      ['vacio-mobile', path.join(output, 'vacio.html'), 390, 844],
      ['error-mobile', path.join(output, 'error.html'), 390, 844],
    ];
    for (const [name, file, width, height] of cases) {
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.setViewportSize({ width, height });
      await page.goto(pathToFileURL(file).href, { waitUntil: 'load', timeout: 20000 });
      if (name === 'largo-mobile') await page.locator('.script details').first().evaluate(node => { node.open = true; });
      const metrics = await page.evaluate(() => ({
        overflow: document.documentElement.scrollWidth > innerWidth,
        buttons: document.querySelectorAll('button,form,input,textarea,script').length,
        text: document.body.innerText,
        headings: [...document.querySelectorAll('h2')].map(x => x.textContent),
      }));
      assert.equal(metrics.overflow, false, name + ': sin desborde horizontal');
      assert.equal(metrics.buttons, 0, name + ': sin controles de mutación ni scripts');
      assert.equal(errors.length, 0);
      assert(metrics.text.includes('Sin aprobación de publicación'));
      if (name === 'vacio-mobile') assert(metrics.text.includes('Sin fuentes leídas'));
      if (name === 'error-mobile') {
        await page.locator('#fuentes details').evaluate(node => { node.open = true; });
        assert((await page.innerText('body')).includes('HTTP_403'));
        assert(metrics.text.includes('Evidencia no válida'));
      }
      await page.screenshot({ path: path.join(output, name + '.png'), fullPage: true });
      report.casos.push({ nombre: name, width, height, desborde: metrics.overflow,
        controles_mutacion: metrics.buttons, errores_js: errors, secciones: metrics.headings,
        captura: name + '.png' });
      await page.close();
    }
    assert.equal(external.length, 0, 'Sin peticiones HTTP automáticas');
    report.peticiones_http_automaticas = external;
    report.resultado = 'OK';
  } catch (e) {
    report.resultado = 'FALLO';
    report.error = String(e);
    process.exitCode = 1;
  } finally {
    if (context) await context.close();
    report.navegador_cerrado = true;
    fs.writeFileSync(path.join(output, 'resultado.json'), JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
    console.log(JSON.stringify({ resultado: report.resultado, casos: report.casos.length, salida: path.relative(root, output) }));
  }
})();

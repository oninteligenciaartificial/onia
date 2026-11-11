// Ensayo local de corrección y aplicación. Mantiene el sandbox de Chromium.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');
const { createHash } = require('node:crypto');
const runtime = path.join(os.homedir(),'operacion/browser-piloto-20261108');
const { chromium } = require(path.join(runtime,'node_modules/playwright'));
const root = __dirname;
const output = path.resolve(process.argv[2] || '');
assert(output.startsWith(root + path.sep));
let ancestor = output;
while (ancestor !== root) {
  if (fs.existsSync(ancestor)) assert(!fs.lstatSync(ancestor).isSymbolicLink());
  ancestor = path.dirname(ancestor);
}
fs.mkdirSync(output, { recursive:false });
const data = fs.mkdtempSync('/tmp/onia-cerebro-browser-sintetico-');
let server;
let browser;
const report = { fecha:new Date().toISOString(), ensayo:'SINTETICO sobre T01 histórico', chromiumSandbox:true, casos:[] };
report.commit_checkout = spawnSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8'}).stdout.trim();
report.codigo_sha256 = Object.fromEntries(['cerebro.py','servidor.py','operacion.py','diseno.py','panel.py','correcciones.py','vistas_cerebro.py','diseno.css','visual-cerebro.cjs'].map(name =>
  [name,createHash('sha256').update(fs.readFileSync(path.join(root,name))).digest('hex')]));
async function start() {
  server = spawn('python3',['-B',path.join(root,'servidor.py'),'--datos',data,'--puerto','0'],{stdio:['ignore','pipe','pipe']});
  return await new Promise((resolve,reject) => {
    let stdout='';
    const timer=setTimeout(()=>reject(new Error('Sin URL en 10s')),10000);
    server.stdout.on('data',chunk=>{
      stdout+=chunk;
      const match=stdout.match(/http:\/\/127\.0\.0\.1:\d+/);
      if(match){clearTimeout(timer);resolve(match[0]);}
    });
    server.once('exit',code=>{clearTimeout(timer);reject(new Error('Servidor terminó '+code));});
  });
}
async function stop() {
  if(!server || server.exitCode!==null)return;
  const child=server;
  await new Promise(resolve=>{child.once('exit',resolve);child.kill('SIGINT');});
  server=undefined;
}
async function openReview(page,selector) {
  const review=page.locator(selector);
  if(!await review.evaluate(element=>element.open))await review.locator('summary').first().click();
  return review;
}
async function post(page,review,name,pathname) {
  const response=page.waitForResponse(r=>r.request().method()==='POST' && new URL(r.url()).pathname===pathname);
  await review.getByRole('button',{name}).click();
  assert.equal((await response).status(),303);
  await page.waitForLoadState('load');
}
(async()=>{
  try {
    let url=await start();
    browser=await chromium.launch({executablePath:path.join(runtime,'browsers/chromium-1252/chrome-linux64/chrome'),headless:true,chromiumSandbox:true});
    const context=await browser.newContext({viewport:{width:1440,height:1000},deviceScaleFactor:1,javaScriptEnabled:false});
    const external=[];
    await context.route(/^https?:/,async route=>{
      if(new URL(route.request().url()).hostname!=='127.0.0.1'){external.push(route.request().url());return route.abort();}
      return route.continue();
    });
    const page=await context.newPage();
    const errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]) {
      await page.setViewportSize({width,height});
      await page.goto(url+'/#cerebro');
      await page.evaluate(()=>document.fonts.ready);
      assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
      assert((await page.innerText('#cerebro')).includes('Decisiones de negocio vigentes'));
      const author = page.locator('.knowledge-table tr').filter({hasText:'Autor de los 5 guiones diarios'});
      assert((await author.innerText()).includes('Codex escribe'));
      assert((await author.innerText()).includes('Hasta el viernes 13'));
      await page.screenshot({path:path.join(output,name+'-cerebro.png'),fullPage:true});
      await page.locator('.sidebar a[href="#estrategias"]').click();
      const strategyText = await page.innerText('#estrategias');
      assert(strategyText.includes('Productor pendiente') || strategyText.includes('workshop-claude-20261113'));
      await page.screenshot({path:path.join(output,name+'-estrategias.png')});
      report.casos.push(name+' · cerebro y estado contractual de estrategias visibles, sin overflow');
    }
    await page.goto(url+'/#guion-T01');
    let review=await openReview(page,'#guion-T01 details[id^="revision-"]');
    await review.locator('[name="motivo"]').fill('ENSAYO SINTÉTICO · aclarar resultado');
    await review.locator('[name="correccion"]').fill('ENSAYO SINTÉTICO · nueva pieza local con criterio evaluable.');
    await review.locator('[name="alcance"]').selectOption('pieza');
    await post(page,review,/Guardar revisión/,'/revision');
    assert((await page.innerText('body')).includes('Observación guardada'));
    review=await openReview(page,'#correcciones details[id^="correccion-"]');
    await post(page,review,'Crear versión local pendiente','/aplicar');
    assert((await page.innerText('body')).includes('Propuesta aplicada localmente'));
    await page.screenshot({path:path.join(output,'version-local.png'),fullPage:true});
    report.casos.push('Sugerencia pendiente → aplicación local explícita → nueva versión pendiente con original');
    await stop();
    url=await start();
    await page.goto(url+'/#correcciones');
    assert((await page.innerText('#correcciones')).includes('nueva pieza local con criterio evaluable'));
    report.casos.push('Proceso nuevo conserva versión local privada');
    await page.locator('.sidebar a[href="#calendario"]').click();
    await page.locator('#calendario .section-correct').click();
    review=await openReview(page,'#correcciones details[id^="correccion-"]');
    await review.locator('[name="motivo"]').fill('ENSAYO SINTÉTICO de decisión pendiente');
    await review.locator('[name="correccion"]').fill('Propuesta de nueva decisión para coordinar.');
    await review.locator('[name="alcance"]').selectOption('canonico');
    await post(page,review,/Guardar revisión/,'/revision');
    review=await openReview(page,'#correcciones details[id^="correccion-"]');
    assert.equal(await review.getByRole('button',{name:'Crear versión local pendiente'}).count(),0);
    await post(page,review,'Exportar solicitud a coordinadora','/solicitar');
    assert((await page.textContent('body')).includes('onia-solicitud-correccion-v1'));
    report.casos.push('Corrección canónica exportada con ID y dependencias, pendiente');
    assert.equal(external.length,0);
    assert.equal(errors.length,0);
    report.resultado='OK';
    report.errores_js=errors;
    report.peticiones_externas=external;
  } catch(error) {
    const message=String(error).replaceAll(os.homedir(),'~');
    report.resultado=/sandbox|zygote/i.test(message)?'BLOCKED':'FALLO';
    report.error=message;
    process.exitCode=report.resultado==='BLOCKED'?2:1;
  } finally {
    if(browser)await browser.close();
    await stop();
    report.servidor_cerrado=true;
    report.navegador_cerrado=true;
    report.datos='SQLite sintética conservada fuera de Git en /tmp';
    fs.writeFileSync(path.join(output,'resultado.json'),JSON.stringify(report,null,2)+'\n',{flag:'wx'});
    console.log(JSON.stringify({resultado:report.resultado,casos:report.casos.length}));
  }
})();

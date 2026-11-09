const fs = require('fs');
const crypto = require('crypto');
const {chromium} = require('/home/onia-codex-worker/operacion/browser-piloto-20261108/node_modules/playwright');
const root = '/home/onia-codex-worker/operacion/cuentas/analisis-onia';
const exe = '/home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome';
process.umask(0o077);
const run = fs.mkdtempSync(root + '/prueba-chromium-');
const profile = run + '/profile';
const result = {fecha_utc:new Date().toISOString(), chromiumSandbox:true, profile, pruebas:[], errores:[]};
let context;
(async()=>{
 try {
  context = await chromium.launchPersistentContext(profile,{executablePath:exe,headless:true,chromiumSandbox:true,args:['--disable-background-networking'],timeout:30000});
  const page = context.pages()[0] || await context.newPage();
  page.setDefaultTimeout(7000);
  await page.goto('chrome://sandbox');
  result.sandbox_page = await page.locator('body').innerText();
  const response = await page.goto('https://example.com/',{waitUntil:'domcontentloaded'});
  result.public_page = {url:page.url(),status:response?.status(),title:await page.title(),body:(await page.locator('body').innerText()).slice(0,1000)};
  result.public_page.heading = await page.locator('h1').allTextContents();
  await page.screenshot({path:run+'/pagina-publica.png'});
  result.screenshot_sha256=crypto.createHash('sha256').update(fs.readFileSync(run+'/pagina-publica.png')).digest('hex');
  const procs=[];
  for(const pid of fs.readdirSync('/proc').filter(x=>/^\d+$/.test(x))) {
   try {
    const raw=fs.readFileSync(`/proc/${pid}/cmdline`,'utf8');
    if(!raw.includes(`--user-data-dir=${profile}`)) continue;
    const args=raw.split(/[\0\s]+/);
    const status=fs.readFileSync(`/proc/${pid}/status`,'utf8');
    procs.push({pid:Number(pid),type:args.find(x=>x.startsWith('--type='))||'browser',apparmor:fs.readFileSync(`/proc/${pid}/attr/current`,'utf8').trim(),seccomp:status.match(/^Seccomp:\s*(\d+)/m)?.[1],no_new_privs:status.match(/^NoNewPrivs:\s*(\d+)/m)?.[1],sandbox_disabled:args.includes('--no-sandbox')||args.includes('--disable-seccomp-filter-sandbox')||args.includes('--disable-namespace-sandbox')});
   } catch {}
  }
  result.procesos=procs;
  if(result.public_page.title!=='Example Domain'||!result.public_page.body.includes('documentation examples'))throw Error('Página pública inesperada');
  if(!procs.length||procs.some(p=>p.sandbox_disabled))throw Error('No se pudo acreditar proceso con sandbox');
  if(!procs.some(p=>p.type==='--type=renderer'&&p.seccomp==='2'))throw Error('No se observó Seccomp renderer');
  result.ok=true;
 } catch(e) {result.ok=false;result.errores.push(String(e));}
 finally {
  if(context)await context.close();
  fs.writeFileSync(run+'/resultado.json',JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));
  if(!result.ok)process.exitCode=1;
 }
})();

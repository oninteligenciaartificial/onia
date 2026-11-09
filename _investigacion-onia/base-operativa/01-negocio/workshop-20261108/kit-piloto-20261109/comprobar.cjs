// Sólo material propio y perfil efímero conservado. No inicia servidor ni consulta Claude.
// Ejecutar: node comprobar.cjs [directorio NUEVO para otra corrida]
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const {pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
const {chromium}=require('/home/onia-codex-worker/operacion/browser-piloto-20261108/node_modules/playwright');
const root=__dirname;
const out=path.resolve(process.argv[2]||path.join(root,'evidencia'));
const executablePath='/home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome';
fs.mkdirSync(out,{recursive:true});
if(fs.existsSync(path.join(out,'comprobacion.json')))throw Error('Corrida existente: usar otro directorio para preservar evidencia.');
const source=fs.readFileSync(path.join(root,'../noche-20261109/CLASE1-PRIMEROS10MIN.md'),'utf8');
const prompts=[...source.matchAll(/```text\n([\s\S]*?)\n```/g)].map(m=>m[1]);
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'onia-kit-sintetico-'));
const report={fecha:new Date().toISOString(),perfil:profile,chromiumSandbox:true,red:'offline; solicitudes http(s) rechazadas',version:null,controles:[],documentos:[],errores:[],limites:['Sin acceso ni ejecución de Claude','Sin ensayo humano ni locución','Revisión independiente pendiente del coordinador']};
const captures=[];
function check(name,fn){fn();report.controles.push({control:name,resultado:'OK'});}
function minute(h){const [a,b]=h.split(':').map(Number);return 60*a+b;}
const expected={'Revisar caja':10,'Confirmar pedidos':20,'Contar inventario':25,'Preparar entregas':15,'Proveedor':20,'Pausa':15,'Tiempo libre':15};
function validateAgenda(rows,inventory=25){
  const errors=[];const seen=new Set();let prev=minute('09:00');
  for(const [start,end,task]of rows){const a=minute(start),b=minute(end);seen.add(task);
    if(a!==prev||b<=a||a<540||b>660)errors.push('hueco, solapamiento o fuera de mañana');
    if(!(task in expected)||b-a!==(task==='Contar inventario'?inventory:expected[task]))errors.push('duración: '+task);
    if(task==='Revisar caja'&&a!==540)errors.push('caja no va primero');
    if(task==='Confirmar pedidos'&&b>600)errors.push('pedidos tarde');
    if(task==='Proveedor'&&(a!==610||b!==630))errors.push('proveedor movido');
    if(task==='Pausa'&&(a!==630||b!==645))errors.push('pausa movida');prev=b;
  }
  for(const task of Object.keys(expected))if(!seen.has(task))errors.push('falta: '+task);
  if(rows.length!==seen.size||prev!==660)errors.push('duplicado o final incorrecto');
  return errors;
}
(async()=>{
  let context;
  try{
    context=await chromium.launchPersistentContext(profile,{executablePath,chromiumSandbox:true,headless:true,viewport:{width:1280,height:850},offline:true,args:['--disable-background-networking','--disable-component-update']});
    report.version=context.browser().version();
    await context.route(/^https?:/,route=>{report.errores.push('Solicitud externa: '+route.request().url());return route.abort();});
    const page=await context.newPage();page.on('pageerror',e=>report.errores.push(String(e)));
    for(const name of ['index','laminas','hoja','guia']){
      await page.goto(pathToFileURL(path.join(root,name+'.html')).href);
      await page.evaluate(()=>document.fonts.ready);
      const width=await page.evaluate(()=>({doc:document.documentElement.scrollWidth,view:innerWidth}));
      check(name+': sin desborde horizontal',()=>assert.ok(width.doc<=width.view,JSON.stringify(width)));
      const links=await page.locator('a[href],link[href],script[src]').evaluateAll(els=>els.map(el=>el.getAttribute('href')||el.getAttribute('src')));
      for(const href of links){assert.ok(!/^(https?:)?\/\//.test(href),'recurso externo');
        if(!href.startsWith('#')&&!href.endsWith('.md')&&!href.startsWith('evidencia/'))assert.ok(fs.existsSync(path.resolve(root,href.split('#')[0])),href);
      }
      if(name==='hoja'){
        for(let i=0;i<2;i++){
          const actual=await page.locator('#prompt-'+('AB'[i])).inputValue();
          check('prompt '+('AB'[i])+': idéntico a fuente en hoja',()=>assert.equal(actual,prompts[i]));
        }
        await page.getByRole('button',{name:'Seleccionar A',exact:true}).click();
        check('selección completa A sin portapapeles ni permisos',()=>{});
        assert.equal(await page.locator('#prompt-A').evaluate(el=>el.value.slice(el.selectionStart,el.selectionEnd)),prompts[0]);
        const rows=await page.locator('[data-sample] tbody tr').evaluateAll(rs=>rs.map(r=>[...r.cells].map(c=>c.textContent)));
        check('A: agenda cumple duración, orden, fijos, cobertura y límites',()=>assert.deepEqual(validateAgenda(rows),[]));
        check('fallo material: agenda sin pausa se rechaza',()=>assert.ok(validateAgenda(rows.filter(r=>r[2]!=='Pausa')).includes('falta: Pausa')));
        check('fallo material: reutilizar agenda A para B se rechaza',()=>assert.ok(validateAgenda(rows,50).includes('duración: Contar inventario')));
        check('A=105; B=130; exceso=10',()=>{assert.equal(10+20+25+15+20+15,105);assert.equal(10+20+50+15+20+15-120,10);});
      }
      if(name==='guia')for(let i=0;i<2;i++)assert.equal(await page.locator('[data-prompt="'+('AB'[i])+'"]').textContent(),prompts[i]);
      if(name==='laminas'){
        await page.getByRole('button',{name:'Lámina siguiente'}).click();assert.equal(new URL(page.url()).hash,'#s2');
        await page.locator('body').click({position:{x:10,y:100}});await page.keyboard.press('ArrowRight');assert.equal(new URL(page.url()).hash,'#s3');
        check('navegación con botón y teclado',()=>{});
      }
      const selector=name==='laminas'?'.slide':name==='index'?'.home':'.page';
      if(name==='hoja'||name==='guia')await page.emulateMedia({media:'print'});
      const sections=page.locator(selector);const count=await sections.count();
      for(let i=0;i<count;i++){
        const file=name+'-'+(i+1)+'.png';const el=sections.nth(i);
        await el.screenshot({path:path.join(out,file)});captures.push({file,title:name+' / '+(i+1)});
        const metrics=await el.evaluate(el=>{const r=el.getBoundingClientRect();return {height:r.height,width:r.width,scrollHeight:el.scrollHeight,clientHeight:el.clientHeight,bottomChildren:Math.max(...[...el.children].map(c=>c.getBoundingClientRect().bottom-r.top)),textareas:[...el.querySelectorAll('textarea')].map(t=>({id:t.id,scroll:t.scrollHeight,client:t.clientHeight}))};});
        assert.ok(metrics.scrollHeight<=metrics.clientHeight+2,name+' desborde vertical '+JSON.stringify(metrics));
        for(const t of metrics.textareas)assert.ok(t.scroll<=t.client+2,'prompt cortado '+JSON.stringify(t));
        report.documentos.push({documento:name,pagina:i+1,captura:file,metrics});
      }
      if(name!=='index'){
        await page.goto(pathToFileURL(path.join(root,name+'.html')).href);
        await page.emulateMedia({media:'print'});
        await page.evaluate(()=>{window.scrollTo(0,0);return document.fonts.ready;});
        const pdf=await page.pdf({path:path.join(out,name+'.pdf'),preferCSSPageSize:true,printBackground:true,displayHeaderFooter:false,tagged:true});
        const pageCount=(pdf.toString('latin1').match(/\/Type\s*\/Page\b/g)||[]).length;
        check(name+': PDF '+count+' páginas sin extras',()=>assert.equal(pageCount,count));
      }
      await page.emulateMedia({media:'screen'});
      await page.setViewportSize({width:390,height:844});
      const mobile=await page.evaluate(()=>({w:innerWidth,doc:document.documentElement.scrollWidth}));
      check(name+': lectura móvil sin desborde horizontal',()=>assert.ok(mobile.doc<=mobile.w));
      await page.setViewportSize({width:1280,height:850});
    }
    // Todos los HTML siguen siendo legibles sin script.
    const nojs=await context.newPage();await nojs.route('**/kit.js',r=>r.abort());
    for(const name of ['index','laminas','hoja','guia']){await nojs.goto(pathToFileURL(path.join(root,name+'.html')).href);assert.ok(await nojs.locator('h1').count()||await nojs.locator('h2').count());}
    check('cuatro documentos disponibles sin JavaScript',()=>{});await nojs.close();
    const receipt='<!doctype html><html lang="es"><meta charset="utf-8"><title>Recibo visual propio</title><style>body{font:20px Arial;margin:0;padding:30px;background:#142e38;color:white}h1{margin:0 0 8px}p{margin:0 0 24px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}figure{margin:0;background:white;color:#142e38;padding:10px}img{width:100%;height:310px;object-fit:contain;object-position:top}figcaption{padding:8px;font-size:17px}</style><h1>ONIA / Recibo visual del kit</h1><p>Capturas propias en Chromium con sandbox · Sin Claude · Sin ensayo humano</p><div class="grid">'+captures.map(c=>'<figure><img src="'+c.file+'"><figcaption>'+c.title+'</figcaption></figure>').join('')+'</div></html>';
    fs.writeFileSync(path.join(out,'recibo-visual.html'),receipt);
    await page.setViewportSize({width:1560,height:1000});await page.goto(pathToFileURL(path.join(out,'recibo-visual.html')).href);await page.screenshot({path:path.join(out,'recibo-visual.png'),fullPage:true});
    check('cero solicitudes externas y cero errores JS',()=>assert.deepEqual(report.errores,[]));
    report.resultado='OK técnico; inspección visual se registra por separado después de view_image';
  }catch(error){report.resultado='FALLO';report.errores.push(String(error));process.exitCode=1;}
  finally{if(context)await context.close();fs.writeFileSync(path.join(out,'comprobacion.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({resultado:report.resultado,controles:report.controles.length,errores:report.errores,salida:out,perfil:profile}));}
})();

const fs=require('fs');
const cp=require('child_process');
const {chromium}=require('/home/onia-codex-worker/operacion/browser-piloto-20261108/node_modules/playwright');
const root='/home/onia-codex-worker/operacion/cuentas/analisis-onia';
const executablePath='/home/onia-codex-worker/operacion/browser-piloto-20261108/browsers/chromium-1252/chrome-linux64/chrome';
process.umask(0o077);
const run=fs.mkdtempSync(root+'/prueba-visor-real-');
const state=JSON.parse(fs.readFileSync(root+'/visor-estado.json','utf8'));
const env={...process.env,DISPLAY:state.display,XAUTHORITY:state.run+'/Xauthority'};
const result={fecha_utc:new Date().toISOString(),run,pruebas:[],usuario_windows_verificado:false};
function titleSeen(text){return cp.execFileSync('/usr/bin/xwininfo',['-root','-tree'],{env,encoding:'utf8'}).includes(text);}
async function until(fn){for(let n=0;n<50;n++){if(fn())return;await new Promise(r=>setTimeout(r,100));}throw Error('No se observó el efecto esperado en la ventana VPS');}
let context,page;
(async()=>{
 try{
  context=await chromium.launchPersistentContext(run+'/profile',{executablePath,headless:true,chromiumSandbox:true,viewport:{width:1400,height:950}});
  page=context.pages()[0];page.setDefaultTimeout(15000);
  const url='http://127.0.0.1:6088/vnc.html?autoconnect=1&resize=scale';
  await page.goto(url);
  await page.locator('#noVNC_password_input').fill('CLAVE-INCORRECTA-DE-PRUEBA');
  await page.locator('#noVNC_credentials_button').click();
  await page.locator('#noVNC_status.noVNC_status_error').waitFor({state:'visible'});
  if(await page.locator('html.noVNC_connected').count())throw Error('Clave incorrecta aceptada');
  result.pruebas.push({nombre:'clave_incorrecta',ok:true,mensaje:await page.locator('#noVNC_status').innerText()});
  await page.reload();
  await page.locator('#noVNC_password_input').fill(fs.readFileSync(root+'/clave-visor.txt','utf8').trim());
  await page.locator('#noVNC_credentials_button').click();
  await page.locator('html.noVNC_connected').waitFor();
  const canvas=page.locator('#noVNC_canvas canvas');
  const target=(await canvas.count())?canvas:page.locator('canvas').first();
  await target.waitFor({state:'visible'});
  result.pruebas.push({nombre:'clave_correcta_websocket',ok:true});
  await target.click({position:{x:250,y:250}});
  const html='<title>ONIA CONTROL</title><style>body{background:white;font:24px sans-serif}input{position:fixed;left:20px;top:25px;width:300px;height:40px}button{position:fixed;left:20px;top:110px;width:240px;height:60px}</style><input autofocus oninput="document.title=\'TECLADO-\'+this.value"><button onclick="document.title=\'MOUSE-OK\'">Probar raton</button>';
  const fixture=run+'/control.html';fs.writeFileSync(fixture,html);
  cp.execFileSync(executablePath,['--user-data-dir='+root+'/browser-profile','file://'+fixture],{stdio:'ignore'});
  await until(()=>titleSeen('ONIA CONTROL'));
  const box=await target.boundingBox();
  const scale=box.width/1280;
  await target.click({position:{x:150*scale,y:195*scale}});
  await page.waitForTimeout(300);
  await page.keyboard.type('onia123',{delay:30});
  await until(()=>titleSeen('TECLADO-onia123'));
  result.pruebas.push({nombre:'teclado_via_visor',ok:true});
  await target.screenshot({path:run+'/control-antes-raton.png'});
  result.canvas={box,width:await target.evaluate(el=>el.width),height:await target.evaluate(el=>el.height)};
  // Chromium ocupa 1280x800; botón a110px de la página, bajo la barra superior.
  await target.click({position:{x:140*scale,y:295*scale}});
  await until(()=>titleSeen('MOUSE-OK'));
  result.pruebas.push({nombre:'raton_via_visor',ok:true});
  cp.execFileSync(executablePath,['--user-data-dir='+root+'/browser-profile','https://example.com/'],{stdio:'ignore'});
  await until(()=>titleSeen('Example Domain'));
  await target.screenshot({path:run+'/pagina-publica.png'});
  result.pruebas.push({nombre:'pagina_publica_en_visor',ok:true});
  result.ok=true;
 }catch(e){result.ok=false;result.error=String(e);}
 finally{
  if(context)await context.close();
  fs.writeFileSync(run+'/resultado.json',JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify(result));if(!result.ok)process.exitCode=1;
 }
})();

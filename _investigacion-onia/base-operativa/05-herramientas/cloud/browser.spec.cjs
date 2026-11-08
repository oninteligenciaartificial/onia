const {test,expect}=require('@playwright/test');
const path=require('node:path');
test('botón actualiza estado sintético',async({page,browser})=>{
 await page.setContent('<!doctype html><html lang="es"><title>ONIA prueba local</title><h1>Prueba ONIA</h1><button onclick="document.querySelector(\'output\').textContent=\'Completado\'">Completar</button><output role="status">Pendiente</output></html>');
 await expect(page.getByRole('status')).toHaveText('Pendiente');
 await page.getByRole('button',{name:'Completar'}).click();
 await expect(page.getByRole('status')).toHaveText('Completado');
 await page.screenshot({path:path.join(__dirname,'../operacion/cloud-002/browser.png')});
 console.log('Browser real:',browser.version());
});

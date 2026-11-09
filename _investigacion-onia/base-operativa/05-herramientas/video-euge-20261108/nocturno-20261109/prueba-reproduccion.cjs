'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { observe, URL } = require(process.argv[2]);
const { chromium } = require(path.join(process.argv[3], 'node_modules/playwright'));
const root = process.argv[4];
const media = name => 'data:video/webm;base64,' + fs.readFileSync(path.join(root, name)).toString('base64');
const timing = { interval: 1, pollMs: 80, startupMs: 3000, adMs: 3000, stallMs: 3000 };

(async () => {
  const context = await chromium.launchPersistentContext(path.join(root, 'profile'), {
    executablePath: path.join(process.argv[3], 'browsers/chromium-1252/chrome-linux64/chrome'),
    chromiumSandbox: true, headless: false, acceptDownloads: false,
    ignoreDefaultArgs: ['--disable-field-trial-config', '--password-store=basic'],
  });
  try {
    const body = `<div id="movie_player" class="ad-showing">
       <video class="html5-main-video" src="${media('ad.webm')}"></video>
       <button class="ytp-play-button" aria-label="Play">Play</button></div>
       <script>
         const player = document.querySelector('#movie_player'), video = player.querySelector('video');
         const button = player.querySelector('button');
         button.addEventListener('click', () => video.play());
         video.addEventListener('play', () => button.setAttribute('aria-label','Pause'));
         video.addEventListener('pause', () => button.setAttribute('aria-label','Play'));
         video.addEventListener('ended', () => button.setAttribute('aria-label','Play'));
         window.fixtureSeeks = 0;
         video.addEventListener('seeking', () => window.fixtureSeeks++);
         player.getPlayerResponse = () => ({videoDetails:{videoId:'JuAQILH7dkQ',title:'Fixture',lengthSeconds:'3'},
           playabilityStatus:{status:'OK'}});
         video.addEventListener('ended', () => {
           video.src = ${JSON.stringify(media('content.webm'))};
           video.addEventListener('loadeddata', () => player.classList.remove('ad-showing'), {once:true});
         }, {once:true});
       </script>`;
    await context.route('**/*', route => route.request().url() === URL
      ? route.fulfill({contentType:'text/html',body}) : route.abort());
    const page = await context.newPage();
    const output = fs.mkdtempSync(path.join(root,'samples-'));
    const result = await observe(page, output, () => false, timing);
    assert.equal(result.status,'parcial',JSON.stringify(result));
    assert.equal(result.visionado_completo_acreditado,false);
    assert.equal(result.audio_analizado,false);
    assert.ok(result.frames.length >= 3, JSON.stringify(result));
    assert.equal(result.fin_indicado_por_reproductor,true);
    assert.equal(result.anuncios.length,1);
    assert.equal(result.anuncios[0].tras_s,null);
    assert.ok(result.play_solicitudes <= 3);
    assert.equal(await page.evaluate(() => window.fixtureSeeks),0);
    let previous = 0;
    for (const frame of result.frames) {
      assert.ok(frame.actual_s > previous && frame.readyState >= 2);
      assert.equal(fs.readFileSync(path.join(output,frame.file)).subarray(0,8).toString('hex'),'89504e470d0a1a0a');
      previous = frame.actual_s;
    }
    console.log('OK: preroll sintético excluido, avance continuo, timestamps ascendentes, cero seeks y fin observado.');
  } finally { await context.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});

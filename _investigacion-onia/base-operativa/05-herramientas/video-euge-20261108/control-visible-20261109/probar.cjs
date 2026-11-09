'use strict';
const assert = require('node:assert/strict');
const path = require('node:path');
const { skipAd, URL } = require('./control.cjs');
const install = path.join(process.env.HOME, 'operacion/browser-piloto-20261108');
const { chromium } = require(path.join(install, 'node_modules/playwright'));

async function fixture(page, input, expected, ad = true, exitsBeforeClick = false) {
  const outsider = '<button class="ytp-skip-ad-button">Skip ad</button>';
  const body = `${outsider}<div id="movie_player" class="${ad ? 'ad-showing' : ''}">${input}</div>
    <script>window.clicks=0;
      for(const button of document.querySelectorAll('button')) button.onclick=()=>{window.clicks++};
    </script>`;
  await page.route('**/*', route => route.request().url() === URL
    ? route.fulfill({ contentType: 'text/html; charset=utf-8', body }) : route.abort());
  try {
    await page.goto(URL);
    const metrics = { visible: false, habilitado: false, intentos: 0, exitos: 0, fallos: 0 };
    if (exitsBeforeClick) {
      const evaluate = page.evaluate.bind(page);
      page.evaluate = async (fn, args) => {
        const result = await evaluate(fn, args);
        if (fn.name === 'readPlayer') {
          await evaluate(() => document.querySelector('#movie_player').classList.remove('ad-showing'));
        }
        return result;
      };
      try {
        assert.equal(await skipAd(page, metrics, true), false);
      } finally {
        page.evaluate = evaluate;
      }
    } else {
      assert.equal(await skipAd(page, metrics, true), expected === 'clic');
    }
    assert.equal(await page.evaluate(() => window.clicks), expected === 'clic' ? 1 : 0);
    assert.equal(metrics.visible, expected !== 'ausente');
    assert.equal(metrics.habilitado, ['clic', 'sin_anuncio'].includes(expected));
    assert.equal(metrics.exitos, expected === 'clic' ? 1 : 0);
  } finally {
    await page.unroute('**/*');
  }
}

(async () => {
  const browser = await chromium.launch({ executablePath: path.join(install,
    'browsers/chromium-1252/chrome-linux64/chrome'), chromiumSandbox: true });
  try {
    const page = await browser.newPage();
    const button = '<button class="ytp-skip-ad-button">Omitir anuncio</button>';
    await fixture(page, '', 'ausente');
    await fixture(page, '<button class="ytp-skip-ad-button" style="display:none">Skip ad</button>', 'ausente');
    await fixture(page, '<button class="ytp-skip-ad-button" style="opacity:0">Skip ad</button>', 'ausente');
    await fixture(page, `<div style="opacity:0">${button}</div>`, 'ausente');
    await fixture(page, '<button class="ytp-skip-ad-button" disabled>Skip ad</button>', 'deshabilitado');
    await fixture(page, button, 'sin_anuncio', false);
    await fixture(page, button, 'sin_anuncio', true, true);
    await fixture(page, button, 'clic');
    console.log('OK: clic visible en anuncio activo; ausente, transparente, oculto, deshabilitado, fuera del reproductor y fin del anuncio excluidos.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });

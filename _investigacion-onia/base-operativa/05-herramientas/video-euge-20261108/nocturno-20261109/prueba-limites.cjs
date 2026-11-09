'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const { observe, URL } = require('./reproduccion.cjs');

const timing = { interval: 25, pollMs: 5, startupMs: 25, adMs: 55,
  adIdleMs: 25, stallMs: 70, restartDelayMs: 15 };

async function checkAd(advances) {
  const output = fs.mkdtempSync('/tmp/onia-euge-adclock-');
  let probe = 0;
  const state = { ad: true, idKnown: true, match: true, ready: 4, network: 2,
    paused: false, mediaError: null, adTime: 1 };
  const page = { url: () => URL, goto: async () => ({ status: () => 200 }), on() {},
    evaluate: async () => ({ ...state, adTime: advances ? ++probe / 2 : 1 }) };
  const result = await observe(page, output, () => false, timing);
  assert.equal(result.diagnostico, advances ? 'PUBLICIDAD_EN_CURSO' : 'PUBLICIDAD_SIN_AVANCE');
  assert.equal(result.anuncios[0].avance_observado, advances);
  assert.equal(result.frames.length, 0);
}

async function checkRecovery() {
  const output = fs.mkdtempSync('/tmp/onia-euge-play-normal-');
  let probes = 0;
  let clicks = 0;
  const handlers = {};
  const good = { ad: false, idKnown: true, match: true, ready: 4, network: 2, time: 1,
    duration: 1802, declared: 1802, paused: false, seeking: false, ended: false, playVisible: false };
  const empty = { ...good, ready: 0, network: 0, time: null, duration: null, paused: true, playVisible: true };
  const page = { url: () => URL, goto: async () => ({ status: () => 200 }),
    on: (name, callback) => { handlers[name] = callback; },
    getByRole: () => ({}), locator: () => ({ and: () => ({ click: async () => { clicks += 1; } }) }),
    evaluate: async () => {
      if (probes++ !== 0) return empty;
      handlers.response({ request: () => ({ url: () => 'https://r1.googlevideo.com/videoplayback?token=sintetico' }),
        status: () => 403 });
      return good;
    } };
  const result = await observe(page, output, () => false, timing);
  assert.equal(result.diagnostico, 'AVANCE_DETENIDO');
  assert.equal(result.recuperacion_solicitada, true);
  assert.equal(clicks, 1);
  assert.equal(result.red_media.http[403], 1);
  assert.ok(!JSON.stringify(result).includes('token'));
}

async function checkJumpDoesNotClaimComplete() {
  const output = fs.mkdtempSync('/tmp/onia-euge-no-completo-');
  let n = 0;
  const page = {url: () => URL, goto: async () => ({status: () => 200}), on() {},
    evaluate: async () => ({ad:false,idKnown:true,match:true,ready:4,network:2,
      time: n++ === 0 ? .821 : 1802.900, duration:1802.921, declared:1802.921,
      paused:false,seeking:false,ended:false,playVisible:false,
      frame:{png:Buffer.from('fixture').toString('base64'),width:1,height:1}})};
  const result = await observe(page, output, () => false, timing);
  assert.equal(result.frames.length,1);
  assert.equal(result.fin_indicado_por_reproductor,true);
  assert.equal(result.status,'parcial');
  assert.equal(result.visionado_completo_acreditado,false);
  assert.equal(result.audio_analizado,false);
}

(async () => {
  await checkAd(true);
  await checkAd(false);
  await checkRecovery();
  await checkJumpDoesNotClaimComplete();
  console.log('OK: reloj publicitario, recuperación única y red saneada.');
})().catch(error => { console.error(error); process.exitCode = 1; });

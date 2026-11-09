'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const { observe, URL } = require('./control.cjs');

async function run(times, wallStep = 1000) {
  let index = 0;
  let monotonic = 0;
  const output = fs.mkdtempSync('/tmp/onia-euge-control-cobertura-');
  const page = {
    url: () => URL,
    goto: async () => ({ status: () => 200 }),
    on() {},
    locator: () => ({ count: async () => 0, screenshot: async () => Buffer.from('captura-sintetica') }),
    evaluate: async () => ({ ad: false, idKnown: true, match: true, ready: 4, network: 2,
      time: times[index], duration: 1802.921, declared: 1803, paused: false, seeking: false }),
  };
  return observe(page, output, () => index >= times.length,
    { targets: [25, 55, 90], continuous: 90, pollMs: wallStep, startupMs: 3000, adMs: 3000,
      stallMs: 3000, clock: () => monotonic, sleep: async ms => { monotonic += ms; index += 1; } });
}

(async () => {
  const covered = await run(Array.from({ length: 98 }, (_, i) => i));
  assert.equal(covered.objetivo_control_cumplido, true);
  assert.ok(covered.max_continuo_s >= 90);
  assert.equal(covered.status, 'parcial');
  assert.equal(covered.visionado_completo_acreditado, false);
  assert.equal(covered.audio_analizado, false);
  assert.deepEqual(covered.frames.map(frame => frame.objetivo_s), [25, 55, 90]);

  const jumped = await run([0, 1, 25, 26, 55, 56, 90, 91, 92, 93]);
  assert.equal(jumped.objetivo_control_cumplido, false);
  assert.equal(jumped.status, 'parcial');
  assert.equal(jumped.diagnostico, 'INTERRUMPIDO');
  assert.ok(jumped.max_continuo_s < 10);
  assert.equal(jumped.visionado_completo_acreditado, false);
  const tooFast = await run(Array.from({ length: 98 }, (_, i) => i), 1);
  assert.deepEqual(tooFast.frames.map(frame => frame.objetivo_s), [25, 55, 90]);
  assert.equal(tooFast.objetivo_control_cumplido, false);
  assert.ok(tooFast.max_continuo_s <= 2);
  console.log('OK: 90 s a reloj concordante, saltos e interrupción, y deriva acumulada rechazada.');
})().catch(error => { console.error(error); process.exitCode = 1; });

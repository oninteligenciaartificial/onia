'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { classifyDestination, URL } = require('./muestra-seek-anterior.cjs');

const ID = 'JuAQILH7dkQ';
const BLOCKED = ['LOGIN_REQUIRED', 'UNPLAYABLE', 'ERROR', 'AGE_CHECK_REQUIRED',
  'CONTENT_CHECK_REQUIRED', 'LIVE_STREAM_OFFLINE'];
const DEFAULTS = { interval: 25, pollMs: 700, startupMs: 45000, adMs: 120000, stallMs: 90000 };

class Diagnostic extends Error {}

function readPlayer({ expectedId, blocked, allowPlay, target }) {
  const player = document.querySelector('#movie_player');
  const video = player?.querySelector('video.html5-main-video');
  const response = player?.getPlayerResponse?.() || window.ytInitialPlayerResponse;
  const data = response?.videoDetails || player?.getVideoData?.();
  const id = data?.videoId || data?.video_id;
  const match = id === expectedId;
  const status = response?.playabilityStatus?.status;
  const ad = Boolean(player?.matches('.ad-showing, .ad-interrupting'));
  const blockedStatus = blocked.includes(status) ? status : null;
  const state = { ad, blocked: blockedStatus, idKnown: Boolean(id), match,
    time: match && !ad && Number.isFinite(video?.currentTime) ? video.currentTime : null,
    duration: match && !ad && Number.isFinite(video?.duration) ? video.duration : null,
    declared: match ? Number(data?.lengthSeconds) || null : null,
    title: match && !ad && typeof data?.title === 'string' ? data.title.slice(0, 240) : null,
    ready: video?.readyState ?? null, network: video?.networkState ?? null,
    paused: video?.paused ?? null, seeking: video?.seeking ?? null, ended: video?.ended ?? null,
    mediaError: video?.error?.code || null, attemptedPlay: false };
  if (!video || !match || blockedStatus) return state;

  if (!video.muted) video.muted = true;
  if (allowPlay && video.paused && !video.ended && !state.mediaError) {
    state.attemptedPlay = true;
    // A normal playback request. Its success is measured from the media clock.
    void video.play().catch(() => {});
  }

  const expectedDuration = !state.declared || state.duration !== null
    && Math.abs(state.duration - state.declared) <= 2;
  if (ad || target === null || state.time === null || state.time < target
      || video.readyState < 2 || video.seeking || video.paused || !expectedDuration
      || !video.videoWidth || !video.videoHeight) return state;
  try {
    const canvas = document.createElement('canvas');
    const scale = Math.min(1, 1280 / video.videoWidth);
    canvas.width = Math.max(1, Math.round(video.videoWidth * scale));
    canvas.height = Math.max(1, Math.round(video.videoHeight * scale));
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL('image/png');
    if (!dataUrl.startsWith('data:image/png;base64,')) throw new Error();
    state.frame = { png: dataUrl.slice(22), width: canvas.width, height: canvas.height };
  } catch {
    state.frameBlocked = true;
  }
  return state;
}

function location(page) {
  const safe = classifyDestination(page.url());
  if (!safe.autorizado) throw new Diagnostic('DESTINO_DISTINTO');
  return safe;
}

function save(output, result) {
  const filename = path.join(output, 'muestra.json');
  const pending = filename + '.nuevo';
  fs.writeFileSync(pending, JSON.stringify(result, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(pending, filename);
}

function time(value) {
  return Number(value.toFixed(3));
}

async function observe(page, output, interrupted, options = DEFAULTS) {
  const result = { url: URL, video_id: ID, status: 'en_curso', tipo: 'reproduccion_secuencial_muestreo_visual_sin_audio',
    intervalo_nominal_s: options.interval, frames: [], anuncios: [], play_solicitudes: 0, maximo_s: null };
  save(output, result);
  let lastSave = performance.now();
  let stage = 'NAVEGACION_INCOMPLETA';
  let state;
  let adBegan = null;
  let stableCount = 0;
  let playSinceAd = false;
  let endObserved = false;
  let lastProgress = performance.now();
  let next = 0.5;
  try {
    const response = await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 25000 });
    result.destino = location(page);
    result.http = response?.status() || null;
    if (response && response.status() >= 400) throw new Diagnostic('HTTP_RECHAZADO');
    stage = 'REPRODUCTOR_NO_DISPONIBLE';
    const began = performance.now();
    lastProgress = began;
    for (;;) {
      if (interrupted()) throw new Diagnostic('INTERRUMPIDO');
      result.destino = location(page);
      const allowPlay = !playSinceAd && result.play_solicitudes < 3;
      state = await page.evaluate(readPlayer, { expectedId: ID, blocked: BLOCKED,
        allowPlay, target: stableCount > 0 && result.frames.length < 80 ? next : null });
      result.destino = location(page);
      const now = performance.now();
      if (state.blocked) throw new Diagnostic(state.blocked);
      if (!state.ad && state.idKnown && !state.match) throw new Diagnostic('ID_DISTINTO');
      if (!state.ad && state.mediaError) throw new Diagnostic('ERROR_MEDIO');
      if (state.attemptedPlay) {
        result.play_solicitudes += 1;
        playSinceAd = true;
      }
      if (state.ad) {
        stableCount = 0;
        if (adBegan === null) {
          adBegan = now;
          // Reserve one opportunity to resume after the preroll or midroll.
          if (result.maximo_s !== null) playSinceAd = false;
        }
        if (now - adBegan >= options.adMs) throw new Diagnostic('PUBLICIDAD_EN_CURSO');
      } else {
        if (adBegan !== null) {
          result.anuncios.push({ tras_s: result.maximo_s, espera_s: time((now - adBegan) / 1000) });
          adBegan = null;
          playSinceAd = false;
          lastProgress = now;
        }
        const verified = state.match && state.duration > 0 && state.ready >= 2 && !state.seeking
          && (!state.declared || Math.abs(state.duration - state.declared) <= 2);
        stableCount = verified ? stableCount + 1 : 0;
        if (verified) {
          result.duration_s = time(state.duration);
          result.titulo = state.title?.replace(/[\u0000-\u001f\u007f]/g, ' ') || null;
          if (result.maximo_s === null || state.time > result.maximo_s + 0.08) {
            result.maximo_s = time(state.time);
            lastProgress = now;
          }
          if (state.frameBlocked) throw new Diagnostic('PIXEL_NO_ACCESIBLE');
          if (state.frame && stableCount >= 2 && state.time >= next) {
            const filename = `frame-${String(result.frames.length + 1).padStart(3, '0')}.png`;
            fs.writeFileSync(path.join(output, filename), Buffer.from(state.frame.png, 'base64'),
              { flag: 'wx', mode: 0o600 });
            result.frames.push({ file: filename, actual_s: time(state.time), readyState: state.ready,
              width: state.frame.width, height: state.frame.height });
            const interval = Math.max(options.interval, Math.ceil(state.duration / 79));
            next = Math.min(state.duration - 0.5, (Math.floor(state.time / interval) + 1) * interval);
            if (next <= state.time) next = Infinity;
            lastSave = 0;
          }
          if (state.ended || state.time >= state.duration - 0.15) {
            endObserved = true;
            break;
          }
        }
        if (now - lastProgress >= (result.maximo_s === null ? options.startupMs : options.stallMs)) {
          throw new Diagnostic(result.maximo_s === null ? 'SIN_VIDEO_REPRODUCIBLE' : 'AVANCE_DETENIDO');
        }
      }
      if (now - lastSave >= 15000) {
        save(output, result);
        lastSave = now;
      }
      await new Promise(resolve => setTimeout(resolve, options.pollMs));
    }
  } catch (error) {
    result.destino = classifyDestination(page.url());
    result.diagnostico = interrupted() ? 'INTERRUMPIDO' : error instanceof Diagnostic ? error.message
      : !result.destino.autorizado && page.url() !== 'about:blank' ? 'DESTINO_DISTINTO' : stage;
  }
  if (adBegan !== null) {
    result.anuncios.push({ tras_s: result.maximo_s, espera_s: time((performance.now() - adBegan) / 1000), activa_al_final: true });
  }
  result.estado_final = state ? { readyState: state.ready, networkState: state.network,
    mediaError: state.mediaError, pausado: state.paused, buscando: state.seeking,
    anuncio: state.ad, id_coincide: state.match } : null;
  result.fin_reproduccion_observado = endObserved;
  result.status = result.frames.length ? (endObserved ? 'completo' : 'parcial') : 'sin_fotogramas';
  save(output, result);
  return result;
}

async function main() {
  const [, , install, executablePath, profile, output] = process.argv;
  const { chromium } = require(path.join(install, 'node_modules/playwright'));
  let stop = false;
  let context;
  const requestStop = () => {
    stop = true;
    if (context) void context.close().catch(() => {});
  };
  process.on('SIGTERM', requestStop);
  process.on('SIGINT', requestStop);
  process.on('SIGHUP', requestStop);
  process.stdin.on('end', requestStop);
  process.stdin.resume();
  try {
    context = await chromium.launchPersistentContext(profile, {
      executablePath, headless: false, chromiumSandbox: true, acceptDownloads: false,
      handleSIGTERM: false, handleSIGINT: false, handleSIGHUP: false,
      ignoreDefaultArgs: ['--disable-field-trial-config', '--password-store=basic'],
      viewport: null, timeout: 20000,
    });
    if (stop) return 1;
    const result = await observe(await context.newPage(), output, () => stop);
    return result.status === 'completo' ? 0 : result.frames.length ? 3 : 2;
  } catch {
    if (!fs.existsSync(path.join(output, 'muestra.json'))) {
      save(output, { url: URL, video_id: ID, status: 'sin_fotogramas',
        diagnostico: stop ? 'INTERRUMPIDO' : 'ARRANQUE_CHROMIUM_FALLO', frames: [] });
    }
    return 2;
  } finally {
    process.stdin.destroy();
    if (context) await context.close().catch(() => {});
  }
}

module.exports = { observe, URL };
if (require.main === module) main().then(code => { process.exitCode = code; });

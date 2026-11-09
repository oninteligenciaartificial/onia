'use strict';

const fs = require('node:fs');
const path = require('node:path');

const ID = 'JuAQILH7dkQ';
const URL = 'https://www.youtube.com/watch?v=' + ID;
const CANONICAL = new globalThis.URL(URL);
const INNOCUOUS = new Map([
  ['t', /^\d{1,7}s?$/], ['start', /^\d{1,7}$/],
  ['si', /^[A-Za-z0-9_-]{1,64}$/], ['feature', /^[A-Za-z0-9_-]{1,40}$/],
  ['hl', /^[a-z]{2,3}(?:-[A-Za-z]{2,4})?$/], ['gl', /^[A-Za-z]{2}$/],
]);
const VIDEO = '#movie_player video.html5-main-video';
const CONTINUATION = [180, 360, 540, 720, 900, 1080, 1260, 1440, 1620, 1780];
const TIMING = { startupMs: 25000, adMs: 120000, pollMs: 300 };
const BLOCKED = new Set(['LOGIN_REQUIRED', 'UNPLAYABLE', 'ERROR', 'AGE_CHECK_REQUIRED',
  'CONTENT_CHECK_REQUIRED', 'LIVE_STREAM_OFFLINE']);

class Diagnostic extends Error {}

function targets(duration) {
  const interval = Math.max(25, Math.ceil(duration / 79));
  const start = Math.min(0.5, duration / 2);
  const end = Math.max(start, duration - 0.25);
  const times = [];
  for (let i = 0; i < 80; i++) {
    const time = Math.min(start + i * interval, end);
    times.push(time);
    if (time === end) break;
  }
  return { interval, times };
}

function classifyDestination(value) {
  const destination = { tipo_host: 'otro', mismo_host: false, misma_ruta: false,
    mismo_video_id: false, parametros_inocuos: false, autorizado: false };
  let parsed;
  try {
    parsed = new globalThis.URL(value);
  } catch {
    return destination;
  }
  if (['consent.google.com', 'consent.youtube.com'].includes(parsed.hostname)) {
    destination.tipo_host = 'consent';
  } else if (parsed.hostname === 'accounts.google.com') {
    destination.tipo_host = 'accounts';
  } else if (['www.youtube.com', 'youtube.com', 'm.youtube.com'].includes(parsed.hostname)) {
    destination.tipo_host = 'youtube';
  }
  destination.mismo_host = parsed.hostname === CANONICAL.hostname;
  destination.misma_ruta = parsed.pathname === CANONICAL.pathname;
  const ids = parsed.searchParams.getAll('v');
  destination.mismo_video_id = ids.length === 1 && ids[0] === ID;
  const keys = new Set();
  destination.parametros_inocuos = [...parsed.searchParams].every(([key, item]) => {
    if (keys.has(key)) return false;
    keys.add(key);
    return key === 'v' ? item === ID : Boolean(INNOCUOUS.get(key)?.test(item));
  });
  destination.autorizado = parsed.protocol === 'https:' && !parsed.port && !parsed.username
    && !parsed.password && !parsed.hash && destination.mismo_host && destination.misma_ruta
    && destination.mismo_video_id && destination.parametros_inocuos;
  return destination;
}

function verifyLocation(page, result) {
  result.destino = classifyDestination(page.url());
  if (!result.destino.autorizado) throw new Diagnostic('DESTINO_DISTINTO');
}

async function playerState(page) {
  return page.evaluate(({ selector, expectedId }) => {
    const player = document.querySelector('#movie_player');
    const response = player?.getPlayerResponse?.() || window.ytInitialPlayerResponse;
    const data = response?.videoDetails || player?.getVideoData?.();
    const video = document.querySelector(selector);
    const id = data?.videoId || data?.video_id || null;
    return {
      idKnown: Boolean(id),
      idMatches: id === expectedId,
      title: id === expectedId ? data?.title || null : null,
      status: response?.playabilityStatus?.status || null,
      ad: Boolean(player?.classList.contains('ad-showing') || player?.classList.contains('ad-interrupting')),
      ready: video?.readyState || 0,
      duration: Number.isFinite(video?.duration) ? video.duration : null,
      declaredDuration: Number(data?.lengthSeconds) || null,
      currentTime: Number.isFinite(video?.currentTime) ? video.currentTime : null,
      error: video?.error?.code || null,
    };
  }, { selector: VIDEO, expectedId: ID });
}

async function captureFrame(page, target) {
  return page.locator(VIDEO).evaluate(async (video, { requested, expectedId }) => {
    function changed() {
      const player = video.closest('#movie_player');
      const response = player?.getPlayerResponse?.() || window.ytInitialPlayerResponse;
      const data = response?.videoDetails || player?.getVideoData?.();
      const ad = Boolean(player?.matches('.ad-showing, .ad-interrupting'));
      const idMatches = (data?.videoId || data?.video_id) === expectedId;
      return ad || !idMatches ? { error: 'REPRODUCTOR_CAMBIO', ad, idMatches } : null;
    }
    const before = changed();
    if (before) return before;
    video.pause();
    if (Math.abs(video.currentTime - requested) > 0.03) {
      await new Promise((resolve) => {
        const timer = setTimeout(done, 4500);
        function done() {
          clearTimeout(timer);
          video.removeEventListener('seeked', done);
          resolve();
        }
        video.addEventListener('seeked', done);
        try { video.currentTime = requested; } catch { done(); }
      });
    }
    const after = changed();
    if (after) return after;
    if (video.seeking || video.readyState < 2 || !video.videoWidth || !video.videoHeight
        || Math.abs(video.currentTime - requested) > 0.20) return { error: 'SEEK_NO_VERIFICADO' };
    const canvas = document.createElement('canvas');
    const scale = Math.min(1, 1280 / video.videoWidth);
    canvas.width = Math.max(1, Math.round(video.videoWidth * scale));
    canvas.height = Math.max(1, Math.round(video.videoHeight * scale));
    try {
      // Dibuja únicamente píxeles del video. Los controles y otros elementos del DOM quedan fuera.
      canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
      const data = canvas.toDataURL('image/png');
      if (!data.startsWith('data:image/png;base64,')) return { error: 'FOTOGRAMA_NO_DISPONIBLE' };
      return { png: data.slice(22), actual: video.currentTime, readyState: video.readyState,
        width: canvas.width, height: canvas.height };
    } catch {
      return { error: 'PIXEL_NO_ACCESIBLE' };
    }
  }, { requested: target, expectedId: ID }, { timeout: 6000 });
}

function saveManifest(output, result) {
  const file = path.join(output, 'muestra.json');
  const next = file + '.nuevo';
  fs.writeFileSync(next, JSON.stringify(result, null, 2) + '\n', { mode: 0o600 });
  fs.renameSync(next, file);
}

function contentReady(state) {
  return state.idMatches && !state.ad && state.ready >= 2 && state.duration > 0
    && (!state.declaredDuration || Math.abs(state.duration - state.declaredDuration) <= 2);
}

async function awaitContent(page, result, interrupted, timing, duringAd = false) {
  const began = performance.now();
  let adSeen = duringAd;
  let adProgress = false;
  let adStartTime = null;
  let stableContent = false;
  let state;
  try {
    for (;;) {
      if (interrupted()) throw new Diagnostic('INTERRUMPIDO');
      verifyLocation(page, result);
      state = await playerState(page);
      result.ready_state_inicial = state.ready;
      if (BLOCKED.has(state.status)) throw new Diagnostic(state.status);
      if (!state.ad && state.idKnown && !state.idMatches) {
        recordChange(result, state);
        throw new Diagnostic('REPRODUCTOR_CAMBIO');
      }
      if (state.error && !state.ad) throw new Diagnostic('ERROR_DECODIFICACION');
      if (state.ad) {
        adSeen = true;
        if (state.currentTime !== null) {
          if (adStartTime === null || state.currentTime < adStartTime) adStartTime = state.currentTime;
          if (state.currentTime > adStartTime + 0.10) adProgress = true;
        }
      }
      const ready = contentReady(state);
      if (ready && (!adSeen || stableContent)) return state;
      stableContent = ready;
      const remaining = (adSeen ? timing.adMs : timing.startupMs) - (performance.now() - began);
      if (remaining <= 0) throw new Diagnostic(state.ad ? 'PUBLICIDAD_EN_CURSO' : 'SIN_VIDEO_REPRODUCIBLE');
      await new Promise(resolve => setTimeout(resolve, Math.min(remaining, timing.pollMs)));
    }
  } finally {
    if (adSeen) {
      const observation = { observada: true, avance_observado: adProgress,
        espera_reproductor_ms: Math.round(performance.now() - began), activa_al_final: Boolean(state?.ad) };
      if (duringAd) (result.esperas_intermedias ||= []).push(observation);
      else result.publicidad = observation;
    }
  }
}

function recordChange(result, state, target) {
  (result.cambios_reproductor ||= []).push({ requested_s: target ?? null,
    anuncio: state.ad, id_coincide: state.idMatches });
}

async function inspectTarget(page, target, result, interrupted, timing) {
  for (let attempt = 0; attempt < 2; attempt++) {
    if (interrupted()) throw new Diagnostic('INTERRUMPIDO');
    verifyLocation(page, result);
    let before = await playerState(page);
    if (BLOCKED.has(before.status)) throw new Diagnostic(before.status);
    if (!before.ad && !contentReady(before)) {
      if (before.idKnown && !before.idMatches) {
        recordChange(result, before, target);
        throw new Diagnostic('REPRODUCTOR_CAMBIO');
      }
      before = await awaitContent(page, result, interrupted, timing);
    }
    const frame = before.ad ? { error: 'REPRODUCTOR_CAMBIO', ad: true, idMatches: before.idMatches }
      : await captureFrame(page, target);
    verifyLocation(page, result);
    const after = await playerState(page);
    if (BLOCKED.has(after.status)) throw new Diagnostic(after.status);
    if (!after.ad && after.idKnown && !after.idMatches) {
      recordChange(result, after, target);
      throw new Diagnostic('REPRODUCTOR_CAMBIO');
    }
    const change = frame.error === 'REPRODUCTOR_CAMBIO' ? frame : after;
    if (frame.ad || after.ad) {
      recordChange(result, after.ad ? after : change, target);
      if (attempt === 1) return { error: 'PUBLICIDAD_REPETIDA' };
      await awaitContent(page, result, interrupted, timing, true);
    } else {
      if (!change.idMatches) {
        recordChange(result, change, target);
        throw new Diagnostic('REPRODUCTOR_CAMBIO');
      }
      return frame;
    }
  }
}

async function inspect(page, output, interrupted, timing = TIMING, selected = null) {
  const result = { url: URL, video_id: ID, status: 'en_curso', tipo: 'muestra_visual_sin_audio',
    duration_s: null, titulo: null, interval_s: null, frames: [], omisiones: [] };
  saveManifest(output, result);
  let stage = 'NAVEGACION_INCOMPLETA';
  try {
    const response = await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 25000 });
    verifyLocation(page, result);
    result.http = response?.status() || null;
    if (response && response.status() >= 400) throw new Diagnostic('HTTP_RECHAZADO');
    stage = 'REPRODUCTOR_NO_DISPONIBLE';
    const state = await awaitContent(page, result, interrupted, timing);
    result.titulo = typeof state.title === 'string' ? state.title.replace(/[\u0000-\u001f\u007f]/g, ' ').slice(0, 240) : null;
    result.duration_s = Number(state.duration.toFixed(3));
    const sampling = selected ? { interval: null, times: selected } : targets(state.duration);
    result.interval_s = sampling.interval;
    result.objetivos = sampling.times.length;
    if (selected) result.objetivos_s = selected;
    stage = 'CAPTURA_INCOMPLETA';
    for (const target of sampling.times) {
      const requested = Number(target.toFixed(3));
      const frame = target >= state.duration
        ? { error: 'FUERA_DE_DURACION' } : await inspectTarget(page, target, result, interrupted, timing);
      if (frame.error) {
        result.omisiones.push({ requested_s: requested, motivo: frame.error });
        if (frame.error === 'PIXEL_NO_ACCESIBLE' || !selected && result.frames.length === 0 && result.omisiones.length >= 3) {
          throw new Diagnostic(frame.error);
        }
      } else {
        const filename = `frame-${String(result.frames.length + 1).padStart(3, '0')}.png`;
        fs.writeFileSync(path.join(output, filename), Buffer.from(frame.png, 'base64'), { flag: 'wx', mode: 0o600 });
        result.frames.push({ file: filename, requested_s: requested, actual_s: Number(frame.actual.toFixed(3)),
          readyState: frame.readyState, width: frame.width, height: frame.height });
      }
      saveManifest(output, result);
    }
    result.status = result.frames.length ? (result.omisiones.length ? 'parcial' : 'completo') : 'sin_fotogramas';
  } catch (error) {
    result.status = result.frames.length ? 'parcial' : 'sin_fotogramas';
    result.destino = classifyDestination(page.url());
    result.diagnostico = interrupted() ? 'INTERRUMPIDO' : error instanceof Diagnostic ? error.message
      : !result.destino.autorizado && page.url() !== 'about:blank' ? 'DESTINO_DISTINTO' : stage;
  }
  saveManifest(output, result);
  return result;
}

async function main() {
  const [, , install, executablePath, profile, output, continuation] = process.argv;
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
    const page = await context.newPage();
    const result = await inspect(page, output, () => stop, TIMING, continuation ? CONTINUATION : null);
    return result.status === 'completo' ? 0 : result.frames.length ? 3 : 2;
  } catch {
    if (!fs.existsSync(path.join(output, 'muestra.json'))) {
      saveManifest(output, { url: URL, video_id: ID, status: 'sin_fotogramas',
        diagnostico: stop ? 'INTERRUMPIDO' : 'ARRANQUE_CHROMIUM_FALLO', frames: [] });
    }
    return 2;
  } finally {
    process.stdin.destroy();
    if (context) await context.close().catch(() => {});
  }
}

module.exports = { classifyDestination, inspect, targets, URL };
if (require.main === module) main().then(code => { process.exitCode = code; });

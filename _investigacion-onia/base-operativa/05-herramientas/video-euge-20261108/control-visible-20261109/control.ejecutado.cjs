'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { classifyDestination, URL } = require('./muestra-seek-anterior.cjs');

const ID = 'JuAQILH7dkQ';
const PLAY_NAME = /^(?:play|reproducir)(?:\s|\(|$)/i;
const SKIP_NAME = /^(?:skip(?: ads?)?|(?:saltar|omitir)(?: (?:el|los))? anuncios?)$/i;
const SKIP_SELECTOR = ['ytp-skip-ad-button', 'ytp-ad-skip-button', 'ytp-ad-skip-button-modern',
  'ytp-skip-ad-button-modern'].map(name => `#movie_player button.${name}`).join(', ');
const BLOCKED = ['LOGIN_REQUIRED', 'UNPLAYABLE', 'ERROR', 'AGE_CHECK_REQUIRED',
  'CONTENT_CHECK_REQUIRED', 'AGE_VERIFICATION_REQUIRED', 'LIVE_STREAM_OFFLINE'];
const DEFAULTS = { targets: [25, 55, 90], continuous: 90, pollMs: 600, startupMs: 40000, adMs: 95000, stallMs: 42000 };

class Diagnostic extends Error {}

function readPlayer({ expectedId, blocked }) {
  const player = document.querySelector('#movie_player');
  const video = player?.querySelector('video.html5-main-video');
  const response = player?.getPlayerResponse?.() || window.ytInitialPlayerResponse;
  const data = response?.videoDetails || player?.getVideoData?.();
  const id = data?.videoId || data?.video_id;
  const match = id === expectedId;
  const status = response?.playabilityStatus?.status;
  const ad = Boolean(player?.matches('.ad-showing, .ad-interrupting'));
  const blockedStatus = blocked.includes(status) ? status : null;
  const playButton = player?.querySelector('button.ytp-play-button');
  const label = (playButton?.getAttribute('aria-label') || playButton?.title || '').trim();
  const verified = match && !ad && video && video.readyState >= 2 && !video.seeking
    && Number.isFinite(video.duration) && video.duration > 0;
  return { ad, blocked: blockedStatus, idKnown: Boolean(id), match,
    time: verified && Number.isFinite(video.currentTime) ? video.currentTime : null,
    duration: verified ? video.duration : null,
    declared: match ? Number(data?.lengthSeconds) || null : null,
    ready: video?.readyState ?? null, network: video?.networkState ?? null,
    paused: video?.paused ?? null, seeking: video?.seeking ?? null,
    mediaError: video?.error?.code || null,
    playVisible: Boolean(playButton?.getClientRects().length && /^(?:play|reproducir)(?:\s|\(|$)/i.test(label)) };
}

async function guardPage(page) {
  const destination = location(page);
  const dialog = page.locator('[role="dialog"]:visible, tp-yt-paper-dialog[opened]:visible, ytd-consent-bump-v2-lightbox:visible');
  if (await dialog.count()) throw new Diagnostic('DIALOGO_VISIBLE');
  return destination;
}

async function skipAd(page, metrics, allowClick) {
  const button = page.locator(SKIP_SELECTOR).and(page.getByRole('button', { name: SKIP_NAME }))
    .filter({ visible: true });
  const candidates = await button.count();
  if (candidates) metrics.visible = true;
  if (candidates !== 1 || !await button.isEnabled()) return false;
  metrics.habilitado = true;
  if (!allowClick) return false;
  await guardPage(page);
  const state = await page.evaluate(readPlayer, { expectedId: ID, blocked: BLOCKED });
  if (!state.ad || state.blocked) return false;
  location(page);
  metrics.intentos += 1;
  try {
    await button.click({ timeout: 2000 });
    metrics.exitos += 1;
  } catch {
    metrics.fallos += 1;
  }
  return true;
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

function trackMediaNetwork(page, summary) {
  function media(request) {
    const host = new globalThis.URL(request.url()).hostname;
    return host === 'googlevideo.com' || host.endsWith('.googlevideo.com');
  }
  page.on('response', response => {
    if (!media(response.request())) return;
    summary.respuestas += 1;
    const status = response.status();
    if (status >= 400) summary.http[status] = (summary.http[status] || 0) + 1;
  });
  page.on('requestfailed', request => {
    if (!media(request)) return;
    const failure = request.failure()?.errorText || '';
    const key = /^net::ERR_[A-Z0-9_]{1,70}$/.test(failure) ? failure : 'OTRO_ERROR';
    summary.fallos[key] = (summary.fallos[key] || 0) + 1;
  });
}

function verified(state) {
  return state.time !== null && (!state.declared || Math.abs(state.duration - state.declared) <= 2);
}

async function observe(page, output, interrupted, options = DEFAULTS) {
  const result = { url: URL, video_id: ID, status: 'en_curso', tipo: 'control_visible_muestreo_visual_sin_audio',
    objetivos_s: options.targets, continuo_objetivo_s: options.continuous,
    frames: [], anuncios: [], skip: { visible: false, habilitado: false, intentos: 0, exitos: 0, fallos: 0 },
    play: { intentos: 0, exitos: 0, fallos: 0 }, maximo_s: null, max_continuo_s: 0,
    red_media: { respuestas: 0, http: {}, fallos: {} } };
  trackMediaNetwork(page, result.red_media);
  save(output, result);
  let stage = 'NAVEGACION_INCOMPLETA';
  let lastSave = performance.now();
  let lastProgress = lastSave;
  let state;
  let adRun = null;
  let segment = null;
  let skipTried = false;
  let playTried = false;
  try {
    const response = await page.goto(URL, { waitUntil: 'domcontentloaded', timeout: 25000 });
    result.destino = await guardPage(page);
    result.http = response?.status() || null;
    if (response && response.status() >= 400) throw new Diagnostic('HTTP_RECHAZADO');
    stage = 'OBSERVACION_INCOMPLETA';
    lastProgress = performance.now();
    for (;;) {
      if (interrupted()) throw new Diagnostic('INTERRUMPIDO');
      result.destino = await guardPage(page);
      state = await page.evaluate(readPlayer, { expectedId: ID, blocked: BLOCKED });
      const now = performance.now();
      if (state.blocked) throw new Diagnostic(state.blocked);
      if (!state.ad && state.idKnown && !state.match) throw new Diagnostic('ID_DISTINTO');
      if (!state.ad && state.mediaError) throw new Diagnostic('ERROR_MEDIO');
      if (state.ad) {
        segment = null;
        if (adRun === null) {
          adRun = { began: now, tras_s: result.maximo_s, skipExitos: result.skip.exitos };
          skipTried = false;
        }
        skipTried = await skipAd(page, result.skip, !skipTried && result.skip.intentos < 3) || skipTried;
        if (now - adRun.began >= options.adMs) throw new Diagnostic('PUBLICIDAD_EN_CURSO');
      } else if (verified(state)) {
        result.duration_s = time(state.duration);
        if (adRun !== null) {
          result.anuncios.push({ tras_s: adRun.tras_s, espera_s: time((now - adRun.began) / 1000),
            clic_ok: result.skip.exitos > adRun.skipExitos, contenido_verificado: true });
          adRun = null;
          playTried = false;
          lastProgress = now;
        }
        if (result.maximo_s === null || state.time > result.maximo_s + 0.08) {
          result.maximo_s = time(state.time);
          lastProgress = now;
        }
        if (state.paused) {
          segment = null;
        } else {
          if (segment === null || state.time < segment.previous - 0.15
              || state.time - segment.previous > (now - segment.at) / 1000 + 2
              || now - segment.at > 4000 || now - segment.progressAt > 2500) {
            segment = { start: state.time, previous: state.time, at: now, progressAt: now };
          }
          if (state.time > segment.previous + 0.05) segment.progressAt = now;
          segment.previous = state.time;
          segment.at = now;
          result.max_continuo_s = Math.max(result.max_continuo_s, time(state.time - segment.start));
          const target = options.targets.find(point => state.time >= point && state.time <= point + 4
            && !result.frames.some(frame => frame.objetivo_s === point));
          if (target !== undefined) {
            const png = await page.locator('#movie_player').screenshot({ timeout: 2500 });
            result.destino = await guardPage(page);
            const after = await page.evaluate(readPlayer, { expectedId: ID, blocked: BLOCKED });
            if (after.blocked) throw new Diagnostic(after.blocked);
            if (!after.ad && verified(after) && after.time >= state.time && after.time - state.time <= 4) {
              const filename = `reproductor-${target}.png`;
              fs.writeFileSync(path.join(output, filename), png, { flag: 'wx', mode: 0o600 });
              result.frames.push({ file: filename, objetivo_s: target, antes_s: time(state.time),
                despues_s: time(after.time), readyState: state.ready });
              lastSave = 0;
            }
          }
        }
      } else {
        segment = null;
      }
      if (state.match && state.paused && state.playVisible && !playTried
          && result.play.intentos < 2 && !state.mediaError) {
        playTried = true;
        result.play.intentos += 1;
        try {
          location(page);
          await page.locator('#movie_player button.ytp-play-button')
            .and(page.getByRole('button', { name: PLAY_NAME })).click({ timeout: 2000 });
          result.play.exitos += 1;
        } catch {
          result.play.fallos += 1;
        }
      }
      if (result.frames.length === options.targets.length && result.max_continuo_s >= options.continuous) {
        result.objetivo_control_cumplido = true;
        break;
      }
      if (adRun === null && now - lastProgress >= (result.maximo_s === null ? options.startupMs : options.stallMs)) {
        throw new Diagnostic(result.maximo_s === null ? 'SIN_VIDEO_REPRODUCIBLE' : 'AVANCE_DETENIDO');
      }
      if (now - lastSave >= 5000) {
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
  if (adRun !== null) {
    result.anuncios.push({ tras_s: adRun.tras_s, espera_s: time((performance.now() - adRun.began) / 1000),
      clic_ok: result.skip.exitos > adRun.skipExitos, contenido_verificado: false });
  }
  result.estado_final = state ? { readyState: state.ready, networkState: state.network,
    mediaError: state.mediaError, pausado: state.paused, buscando: state.seeking,
    anuncio: state.ad, id_coincide: state.match } : null;
  result.status = result.objetivo_control_cumplido ? 'completo' : result.frames.length ? 'parcial' : 'sin_fotogramas';
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
    return result.frames.length ? 3 : 2; // Muestreo parcial; nunca acredita visionado completo.
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

module.exports = { observe, skipAd, URL };
if (require.main === module) main().then(code => { process.exitCode = code; });

const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { execFileSync } = require('node:child_process');

const OFFICIAL_CA_PATH = '/usr/local/share/ca-certificates/environment-proxy-ca.crt';
// SHA256 of the DER certificate verified in the official runtime on 2026-11-04.
// A rotation requires verifying the new runtime CA and updating this pin.
const OFFICIAL_CA_SHA256 = 'c71b4d1e9d7775c538c688ab10cea9ce417d7312e89838f9d15ff73256cd7fc3';
const TEMP_PREFIX = 'onia-browser-';

/**
 * Own one temporary NSS database per runtime instance. Close every browser using
 * its launch options before cleanup(); a subsequent build creates a fresh home.
 * Dependencies are injectable for tests; production callers use the defaults.
 */
function createBrowserRuntime({
  fileSystem = fs,
  run = execFileSync,
  environment = process.env,
  platform = process.platform,
  temporaryDirectory = os.tmpdir(),
} = {}) {
  const tempRoot = path.resolve(temporaryDirectory);
  let ownedHome;

  function cleanup() {
    if (!ownedHome) return;
    // Only remove a direct child created with our private mkdtemp prefix.
    if (path.dirname(ownedHome) !== tempRoot || !path.basename(ownedHome).startsWith(TEMP_PREFIX)) {
      throw new Error('Refusing to remove an unowned browser runtime directory.');
    }
    fileSystem.rmSync(ownedHome, { recursive: true, force: true, maxRetries: 3 });
    ownedHome = undefined;
  }

  function command(binary, args, input) {
    try {
      return run(binary, args, { input, stdio: ['pipe', 'pipe', 'pipe'], timeout: 15000 });
    } catch (error) {
      const detail = error.code === 'ENOENT' ? 'is missing' : 'failed';
      // Do not include subprocess output or environment values in errors.
      throw new Error(`Browser runtime: ${binary} ${detail}; the official runtime requires openssl and certutil (libnss3-tools).`);
    }
  }

  function buildLaunchOptions() {
    const localOptions = environment.ONIA_CHROMIUM_PATH
      ? { executablePath: environment.ONIA_CHROMIUM_PATH }
      : {};
    if (platform !== 'linux') return localOptions;

    let certificate;
    try {
      certificate = fileSystem.readFileSync(OFFICIAL_CA_PATH);
    } catch (error) {
      if (error.code === 'ENOENT') return localOptions;
      throw new Error('Browser runtime: cannot read the official runtime CA.');
    }
    if ((certificate.toString('utf8').match(/-----BEGIN CERTIFICATE-----/g) || []).length !== 1) {
      throw new Error('Browser runtime: the official CA file must contain exactly one PEM certificate.');
    }
    // Normalize one certificate and import these exact verified bytes, never the
    // original mutable path or another certificate from a PEM bundle.
    const der = command('openssl', ['x509', '-outform', 'DER'], certificate);
    if (crypto.createHash('sha256').update(der).digest('hex') !== OFFICIAL_CA_SHA256) {
      throw new Error('Browser runtime: official runtime CA fingerprint differs from the verified pin; refusing to trust it.');
    }
    const proxy = environment.HTTPS_PROXY || environment.HTTP_PROXY;
    if (!proxy) {
      throw new Error('Browser runtime: the official CA is present but HTTPS_PROXY/HTTP_PROXY is missing.');
    }

    if (!ownedHome) {
      ownedHome = path.resolve(fileSystem.mkdtempSync(path.join(tempRoot, TEMP_PREFIX)));
      try {
        fileSystem.chmodSync(ownedHome, 0o700);
        // Chromium also recognizes this existing NSS location on M146+.
        const database = path.join(ownedHome, '.pki', 'nssdb');
        fileSystem.mkdirSync(database, { recursive: true, mode: 0o700 });
        const verifiedCA = path.join(ownedHome, 'official-runtime-ca.der');
        fileSystem.writeFileSync(verifiedCA, der, { mode: 0o600 });
        command('certutil', ['-N', '--empty-password', '-d', `sql:${database}`]);
        command('certutil', ['-A', '-d', `sql:${database}`, '-n', 'ONIA-official-runtime-CA', '-t', 'C,,', '-i', verifiedCA]);
      } catch (error) {
        cleanup();
        throw error;
      }
    }
    return {
      ...(localOptions.executablePath ? localOptions : { channel: 'chromium' }),
      env: { ...environment, HOME: ownedHome },
      proxy: { server: proxy },
    };
  }

  return { buildLaunchOptions, cleanup };
}

const runtime = createBrowserRuntime();
// Playwright config users get normal-exit cleanup. Standalone callers should
// also call cleanupBrowserRuntime() in finally, after closing their browser.
process.once('exit', runtime.cleanup);

module.exports = {
  buildLaunchOptions: runtime.buildLaunchOptions,
  cleanupBrowserRuntime: runtime.cleanup,
  createBrowserRuntime,
};

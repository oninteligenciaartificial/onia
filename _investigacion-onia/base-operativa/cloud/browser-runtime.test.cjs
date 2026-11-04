const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const { createBrowserRuntime } = require('./browser-runtime.cjs');

const PIN = 'c71b4d1e9d7775c538c688ab10cea9ce417d7312e89838f9d15ff73256cd7fc3';
const CA_PATH = '/usr/local/share/ca-certificates/environment-proxy-ca.crt';
const PEM = Buffer.from('-----BEGIN CERTIFICATE-----\nsubprocess-fixture\n-----END CERTIFICATE-----\n');
const DER = Buffer.from('decoded certificate fixture; not the official runtime CA');

function fixture(t, overrides = {}) {
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'onia-runtime-test-'));
  const existingHome = path.join(directory, 'existing-home');
  fs.mkdirSync(existingHome);
  fs.writeFileSync(path.join(existingHome, 'keep.txt'), 'existing user data');
  const calls = [];
  const environment = { HOME: existingHome, HTTPS_PROXY: 'http://official-proxy.example:8080' };
  const runtime = createBrowserRuntime({
    platform: 'linux', temporaryDirectory: directory, environment,
    fileSystem: {
      ...fs,
      readFileSync(filename, ...args) {
        if (filename === CA_PATH) return PEM;
        return fs.readFileSync(filename, ...args);
      },
    },
    run(binary, args, options) {
      calls.push({ binary, args });
      if (binary === 'openssl') {
        assert.deepEqual(options.input, PEM);
        return DER;
      }
      if (args[0] === '-A') {
        assert.deepEqual(fs.readFileSync(args[args.indexOf('-i') + 1]), DER);
      }
      return Buffer.alloc(0);
    },
    ...overrides,
  });
  t.after(() => {
    runtime.cleanup();
    // This fixture directory was created above with mkdtemp; no external paths.
    fs.rmSync(directory, { recursive: true, force: true });
  });
  return { runtime, calls, environment, directory, existingHome };
}

// Unit tests do not carry the official CA. Only successful lifecycle cases mock
// its digest; rejection cases use real SHA256. Live TLS is checked in Cloud.
function mockVerifiedPin(t) {
  t.mock.method(crypto, 'createHash', (algorithm) => {
    assert.equal(algorithm, 'sha256');
    return {
      update(bytes) {
        assert.deepEqual(bytes, DER);
        return { digest(format) { assert.equal(format, 'hex'); return PIN; } };
      },
    };
  });
}

test('Linux without the official CA keeps local launch options and environment', (t) => {
  const f = fixture(t, {
    fileSystem: { ...fs, readFileSync() { throw Object.assign(new Error('absent'), { code: 'ENOENT' }); } },
  });
  assert.deepEqual(f.runtime.buildLaunchOptions(), {});
  f.environment.ONIA_CHROMIUM_PATH = '/local/chromium';
  assert.deepEqual(f.runtime.buildLaunchOptions(), { executablePath: '/local/chromium' });
  assert.equal(f.environment.HOME, f.existingHome);
  assert.deepEqual(f.calls, []);
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
});

test('non-Linux hosts do not inspect or change certificate trust', (t) => {
  const f = fixture(t, { platform: 'win32', fileSystem: { readFileSync() { assert.fail('unexpected CA read'); } } });
  assert.deepEqual(f.runtime.buildLaunchOptions(), {});
  assert.deepEqual(f.calls, []);
});

test('an unverified CA fails before creating a home or importing trust', (t) => {
  const f = fixture(t);
  assert.throws(() => f.runtime.buildLaunchOptions(), /fingerprint differs/);
  assert.deepEqual(f.calls.map((call) => call.binary), ['openssl']);
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
});

test('a PEM bundle is rejected before any subprocess or trust change', (t) => {
  const f = fixture(t, { fileSystem: { ...fs, readFileSync() { return Buffer.concat([PEM, PEM]); } } });
  assert.throws(() => f.runtime.buildLaunchOptions(), /exactly one PEM certificate/);
  assert.deepEqual(f.calls, []);
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
});

test('verified runtime reuses a private home, respects executable override and recreates after cleanup', (t) => {
  mockVerifiedPin(t);
  const originalProcessHome = process.env.HOME;
  const f = fixture(t);
  const first = f.runtime.buildLaunchOptions();
  assert.equal(first.channel, 'chromium');
  assert.equal(first.proxy.server, f.environment.HTTPS_PROXY);
  assert.notEqual(first.env.HOME, f.existingHome);
  assert.equal(f.runtime.buildLaunchOptions().env.HOME, first.env.HOME);
  assert.equal(f.environment.HOME, f.existingHome);
  assert.equal(process.env.HOME, originalProcessHome);
  if (process.platform !== 'win32') assert.equal(fs.statSync(first.env.HOME).mode & 0o777, 0o700);
  const imports = f.calls.filter((call) => call.binary === 'certutil');
  assert.equal(imports.length, 2);
  assert.deepEqual(imports[0].args.slice(0, 2), ['-N', '--empty-password']);
  assert.equal(imports[1].args[imports[1].args.indexOf('-t') + 1], 'C,,');
  assert.equal(imports[1].args[imports[1].args.indexOf('-n') + 1], 'ONIA-official-runtime-CA');
  f.environment.ONIA_CHROMIUM_PATH = '/custom/chromium';
  const overridden = f.runtime.buildLaunchOptions();
  assert.equal(overridden.executablePath, '/custom/chromium');
  assert.equal(overridden.channel, undefined);
  f.runtime.cleanup();
  f.runtime.cleanup();
  assert.equal(fs.existsSync(first.env.HOME), false);
  assert.equal(fs.readFileSync(path.join(f.existingHome, 'keep.txt'), 'utf8'), 'existing user data');
  assert.notEqual(f.runtime.buildLaunchOptions().env.HOME, first.env.HOME);
  assert.equal(f.calls.filter((call) => call.binary === 'certutil').length, 4);
});

test('failed NSS setup cleans its partial home and can retry without changing existing HOME', (t) => {
  mockVerifiedPin(t);
  let fail = true;
  const f = fixture(t, {
    run(binary) {
      if (binary === 'openssl') return DER;
      if (fail) throw Object.assign(new Error('private subprocess output'), { code: 'ENOENT' });
      return Buffer.alloc(0);
    },
  });
  assert.throws(() => f.runtime.buildLaunchOptions(), (error) => {
    assert.match(error.message, /certutil is missing/);
    assert.doesNotMatch(error.message, /private subprocess output/);
    return true;
  });
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
  fail = false;
  assert.ok(fs.existsSync(f.runtime.buildLaunchOptions().env.HOME));
  assert.equal(f.environment.HOME, f.existingHome);
});

test('missing openssl fails clearly without creating a temporary home', (t) => {
  const f = fixture(t, {
    run() { throw Object.assign(new Error('not found'), { code: 'ENOENT' }); },
  });
  assert.throws(() => f.runtime.buildLaunchOptions(), /openssl is missing/);
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
});

test('verified runtime requires its configured proxy and supports HTTP_PROXY fallback', (t) => {
  mockVerifiedPin(t);
  const f = fixture(t);
  delete f.environment.HTTPS_PROXY;
  assert.throws(() => f.runtime.buildLaunchOptions(), /HTTPS_PROXY\/HTTP_PROXY is missing/);
  assert.deepEqual(fs.readdirSync(f.directory), ['existing-home']);
  f.environment.HTTP_PROXY = 'http://official-proxy.example:8080';
  assert.equal(f.runtime.buildLaunchOptions().proxy.server, f.environment.HTTP_PROXY);
});

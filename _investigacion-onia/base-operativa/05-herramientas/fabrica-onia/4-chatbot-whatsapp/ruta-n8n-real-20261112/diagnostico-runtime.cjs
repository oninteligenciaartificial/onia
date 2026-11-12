/* Lectura desde el namespace efectivo. GET sin credenciales, cuerpo ni redirects. */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const dns = require('node:dns').promises;
const net = require('node:net');
const http = require('node:http');
const https = require('node:https');

function privada(address) {
  if (net.isIP(address) === 4) {
    const [a, b] = address.split('.').map(Number);
    return a === 127 || a === 10 || (a === 172 && b >= 16 && b <= 31)
      || (a === 192 && b === 168);
  }
  return net.isIP(address) === 6
    && (address === '::1' || /^f[cd]/i.test(address));
}

function runtime() {
  const rows = [];
  for (const pid of fs.readdirSync('/proc').filter(name => /^\d+$/.test(name))) {
    try {
      const comm = fs.readFileSync(`/proc/${pid}/comm`, 'utf8').trim();
      if (!['node', 'n8n'].includes(comm)) continue;
      const args = fs.readFileSync(`/proc/${pid}/cmdline`, 'utf8').split('\0');
      const entry = args.slice(0, 3).find(arg => /(?:^|\/)n8n(?:\/bin\/n8n)?$/.test(arg));
      if (!entry) continue;
      let version = null;
      let dir = path.dirname(fs.realpathSync(entry));
      for (let depth = 0; depth < 6; depth += 1) {
        const file = path.join(dir, 'package.json');
        if (fs.existsSync(file)) {
          const pkg = JSON.parse(fs.readFileSync(file, 'utf8'));
          if (pkg.name === 'n8n' && /^\d+\.\d+\.\d+$/.test(pkg.version)) {
            version = pkg.version;
            break;
          }
        }
        dir = path.dirname(dir);
      }
      let mode = null;
      let envBlocked = null;
      try {
        const entries = fs.readFileSync(`/proc/${pid}/environ`, 'utf8').split('\0');
        const execution = entries.find(value => value.startsWith('EXECUTIONS_MODE='));
        if (['EXECUTIONS_MODE=regular', 'EXECUTIONS_MODE=queue'].includes(execution)) {
          mode = execution.split('=')[1];
        }
        const blocked = entries.find(value => value.startsWith('N8N_BLOCK_ENV_ACCESS_IN_NODE='));
        if (['N8N_BLOCK_ENV_ACCESS_IN_NODE=true', 'N8N_BLOCK_ENV_ACCESS_IN_NODE=false'].includes(blocked)) {
          envBlocked = blocked.endsWith('=true');
        }
      } catch {}
      rows.push({version, modo_ejecucion_explicito: mode, env_bloqueado_explicito: envBlocked,
        namespace_igual: fs.readlinkSync(`/proc/${pid}/ns/net`)
          === fs.readlinkSync('/proc/self/ns/net')});
    } catch {
      // Un proceso inaccesible o terminado conserva la incertidumbre.
    }
  }
  return rows;
}

async function consultar(origen, permitido) {
  if (!origen || origen !== permitido || origen !== origen.trim()) {
    throw new Error('ORIGEN_SIN_PERMISO_EXACTO');
  }
  const url = new URL(origen);
  if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password
      || url.search || url.hash || url.pathname !== '/' || url.origin !== origen) {
    throw new Error('ORIGEN_INVALIDO');
  }
  const hostname = url.hostname.replace(/^\[|\]$/g, '');
  const addresses = await dns.lookup(hostname, {all: true});
  if (!addresses.length || !addresses.every(row => privada(row.address))) {
    throw new Error('DESTINO_FUERA_DE_RED_PRIVADA');
  }
  const selected = addresses[0];
  const client = url.protocol === 'https:' ? https : http;
  return new Promise((resolve, reject) => {
    const req = client.request(new URL('/operador/despachar', url), {
      method: 'GET',
      agent: false,
      lookup: (_host, options, callback) => {
        if (options.all) callback(null, [selected]);
        else callback(null, selected.address, selected.family);
      },
      headers: {Accept: 'application/json'},
    }, res => {
      const chunks = [];
      let size = 0;
      res.on('data', chunk => {
        size += chunk.length;
        if (size > 4096) req.destroy(new Error('RESPUESTA_EXCESIVA'));
        else chunks.push(chunk);
      });
      res.on('error', reject);
      res.on('end', () => {
        let expected = false;
        try {
          expected = JSON.parse(Buffer.concat(chunks).toString()).error === 'RUTA_INVALIDA';
        } catch {}
        resolve({metodo: 'GET', ruta: '/operador/despachar', http: res.statusCode,
          respuesta_adaptador: expected, direccion_privada: true,
          redirecciones_seguidas: 0, credencial_enviada: false,
          ruta_disponible: res.statusCode === 404 && expected});
      });
    });
    // Un plazo total incluye DNS y cabeceras/cuerpo lentos después de resolver.
    const timer = setTimeout(() => req.destroy(new Error('PLAZO_AGOTADO')), 5000);
    req.on('close', () => clearTimeout(timer));
    req.on('error', reject);
    req.end();
  });
}

async function main() {
  const receipt = {fecha_utc: new Date().toISOString(), runtime: runtime(),
    node: process.version, ejecuciones_workflow: 0};
  try {
    // Valores privados en variables del proceso, nunca en el recibo.
    receipt.conectividad = await Promise.race([
      consultar(process.env.ONIA_ORIGEN_PRIVADO, process.env.ONIA_ORIGEN_PERMITIDO),
      new Promise((_, reject) => {
        const timer = setTimeout(() => reject(new Error('PLAZO_AGOTADO')), 6000);
        timer.unref();
      }),
    ]);
  } catch (error) {
    const known = ['ORIGEN_SIN_PERMISO_EXACTO', 'ORIGEN_INVALIDO',
      'DESTINO_FUERA_DE_RED_PRIVADA', 'PLAZO_AGOTADO', 'RESPUESTA_EXCESIVA'];
    receipt.bloqueo = known.includes(error.message) ? error.message : 'CONEXION_NO_CONFIRMADA';
  }
  const same = receipt.runtime.some(row => row.namespace_igual);
  receipt.resultado = same && receipt.conectividad?.ruta_disponible
    ? 'ruta_confirmada_desde_namespace_n8n' : 'bloqueado';
  console.log(JSON.stringify(receipt, null, 2));
  process.exitCode = receipt.resultado === 'bloqueado' ? 2 : 0;
}

main().catch(() => {
  console.log(JSON.stringify({resultado: 'bloqueado', bloqueo: 'RUNTIME_NO_INSPECCIONABLE'}));
  process.exitCode = 2;
});

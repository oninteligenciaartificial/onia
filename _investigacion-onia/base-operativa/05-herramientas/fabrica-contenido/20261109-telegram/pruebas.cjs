'use strict';

const assert = require('assert/strict');
const fs = require('fs');
const vm = require('vm');
const { adapt, sha, encoded } = require('./adaptador.cjs');
const fixture = JSON.parse(fs.readFileSync(__dirname + '/fixture.json', 'utf8'));
const workflow = JSON.parse(fs.readFileSync(__dirname + '/workflow-n8n.json', 'utf8'));
const clone = value => JSON.parse(JSON.stringify(value));
const checks = [];

function check(name, mutate, expected, dependencyFails = false) {
  const input = clone(fixture);
  mutate(input);
  const receipts = { transport: {}, business: {} };
  const before = encoded(input.snapshot);
  let calls = 0;
  const loadSnapshot = () => {
    calls += 1;
    if (dependencyFails) throw new Error('fallo inyectado');
    return input.snapshot;
  };
  const result = adapt(input.events[0], input.policy, loadSnapshot, receipts);
  assert.equal(result.code || result.status, expected);
  assert.equal(encoded(input.snapshot), before);
  if (result.status === 'rechazado') assert.deepEqual(receipts, { transport: {}, business: {} });
  checks.push({ caso: name, esperado: expected, observado: result.code || result.status, lecturas: calls });
  return { result, receipts, input, loadSnapshot };
}

const good = check('caso_bueno', () => {}, 'preparado_seco');
check('dato_invalido', input => { input.events[0].update_id = '1'; }, 'DATO_INVALIDO');
check('comando_arbitrario', input => { input.events[0].message.text = '/aceptar tarea'; }, 'COMANDO_INVALIDO');
check('identidad_ajena', input => { input.events[0].message.from.id = 900099; }, 'IDENTIDAD_RECHAZADA');
check('grupo', input => { input.events[0].message.chat.type = 'group'; }, 'IDENTIDAD_RECHAZADA');
check('ingreso_no_verificado', input => { input.policy.transportVerified = false; }, 'TRANSPORTE_NO_VALIDADO');
check('modo_real_bloqueado', input => { input.policy.mode = 'real'; }, 'TRANSPORTE_NO_VALIDADO');
check('tarea_ajena', input => { input.policy.taskIds = []; }, 'TAREA_NO_PERMITIDA');
check('revision_vieja', input => { input.snapshot.task.revision += 1; }, 'REVISION_VIEJA');
check('tarea_cerrada', input => { input.snapshot.task.estado = 'para_revision'; }, 'TAREA_CERRADA');
check('fallo_dependencia', () => {}, 'DEPENDENCIA_NO_DISPONIBLE', true);
check('evidencia_alterada', input => { input.snapshot.scripts['guion-a-v1'].propuesta_onia += ' alterado'; }, 'HASH_GUION_INVALIDO');
check('revision_otro_hash', input => { input.snapshot.reviews['guion-a-v1'].guion_sha256 = '0'.repeat(64); }, 'REVISION_EDITORIAL_INVALIDA');
check('guion_con_cambios', input => {
  input.events[0].message.text = '/elegir ficcion-fabrica-001 guion-b-v1 2 ' +
    sha(encoded(input.snapshot.scripts['guion-b-v1']));
}, 'GUION_CON_CAMBIOS');
check('pedir_cambios', input => {
  input.events[0].message.text = input.events[0].message.text.replace('/elegir', '/cambios') + ' Revisar CTA';
}, 'preparado_seco');
check('descartar', input => {
  input.events[0].message.text = input.events[0].message.text.replace('/elegir', '/descartar') + ' Fuera de alcance';
}, 'preparado_seco');

// El recibo precede a la lectura de revisión para conciliar un retry ya resuelto.
good.input.snapshot.task.revision += 1;
let replay = adapt(good.input.events[0], good.input.policy, () => { throw new Error('no debe leer'); }, good.receipts);
assert.equal(replay.status, 'duplicado');
assert.deepEqual(replay.receipt, good.result.receipt);
checks.push({ caso: 'duplicado_transporte_tras_avance_revision', esperado: 'duplicado', observado: replay.status });
const businessEvent = clone(good.input.events[0]);
businessEvent.update_id += 1;
replay = adapt(businessEvent, good.input.policy, () => { throw new Error('no debe leer'); }, good.receipts);
assert.equal(replay.status, 'duplicado');
assert.equal(Object.keys(good.receipts.business).length, 1);
checks.push({ caso: 'duplicado_negocio', esperado: 'duplicado', observado: replay.status });
const conflict = clone(good.input.events[0]);
conflict.message.text = conflict.message.text.replace('/elegir', '/cambios') + ' Otro contenido';
replay = adapt(conflict, good.input.policy, good.loadSnapshot, good.receipts);
assert.equal(replay.code, 'REPLAY_CONFLICTIVO');
checks.push({ caso: 'replay_conflictivo', esperado: 'REPLAY_CONFLICTIVO', observado: replay.code });

// Ejecuta el mismo jsCode embebido con el contrato $input de Code, en VM local.
assert.equal(workflow.active, false);
assert.deepEqual(workflow.nodes.map(node => node.type), [
  'n8n-nodes-base.manualTrigger', 'n8n-nodes-base.code', 'n8n-nodes-base.code',
]);
assert.equal(workflow.nodes.filter(node => node.credentials).length, 0);
function runCode(code, items) {
  const context = {
    $input: { first: () => items[0] },
    require: name => {
      assert.equal(name, 'crypto');
      return require('crypto');
    },
  };
  const result = vm.runInNewContext('(function () {\n' + code + '\n})()', context, { timeout: 1000 });
  return clone(result);
}
let items = [{ json: {} }];
for (const node of workflow.nodes.slice(1)) items = runCode(node.parameters.jsCode, items);
assert.deepEqual(items.map(item => item.json.status), ['preparado_seco', 'duplicado']);
assert.deepEqual(items[0].json.receipt, good.result.receipt);
checks.push({ caso: 'workflow_code_en_vm', esperado: 'preparado_seco,duplicado', observado: items.map(item => item.json.status).join(',') });

process.stdout.write(JSON.stringify({ resultado: 'OK', casos: checks.length, checks,
  receipt: good.result.receipt, limites: ['VM Node local', 'sin ejecución remota n8n', 'identidad fixture',
    'recibos sólo en memoria por invocación', 'sin mutación canónica ni envíos'] }, null, 2) + '\n');

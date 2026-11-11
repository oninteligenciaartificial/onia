'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const {crearMotor, normalizarMeta, ejecutarEscenario} = require('./motor.cjs');
const {construir} = require('./preparar.cjs');
const {ejecutarWorkflow} = require('./ensayo.cjs');
const catalogo = require('./mensajes.json');
const fixture = require('./fixtures.json');
const workflow = require('./workflow-n8n.json');
const TTL = 86400000;
const cliente = 'fixture-cliente-a';
const e = (id, datos = {}) => ({ficticio: true, id: 'fixture-' + id, cliente, ...datos});
const confirmacion = (datos = {}) => e('operador', {operador: 'operador-ficticio', decision: 'confirmar',
  referencia: 'FICTICIO-PAGO-A', importe: 50, moneda: 'BOB', movimientoVerificado: true, destinoVerificado: true, ...datos});

// Los mismos contratos se ejecutan contra el módulo y contra el código exacto
// embebido en el JSON. La VM no es n8n: no acredita importación ni compatibilidad.
const code = workflow.nodes.find(n => n.id === 'motor').parameters.jsCode;
const embebido = new vm.Script('(function(){' + code.slice(0, code.indexOf('\nconst entrada =')) +
  '\nreturn {crearMotor, normalizarMeta, ejecutarEscenario};})()').runInNewContext({}, {timeout: 1000});
for (const [nombre, crear] of [['modulo', crearMotor], ['workflow', embebido.crearMotor]]) {
  const motor = () => crear(catalogo);
  const pendiente = (m, datos = {}) => m.recibirCliente(e('alta', {accion: 'inscribir', plan: 'grupal', ...datos}), 1000);
  const estado = m => m.snapshot().clientes[cliente].estado;
  const accesos = m => m.snapshot().salida.filter(x => x.tipo === 'confirmado').length;
  test(nombre + ': interés sin instrucciones de pago', () => {
    const m = motor(); const r = m.recibirCliente(e('info', {accion: 'interes'}), 1000);
    assert.equal(estado(m), 'interesado'); assert.equal(r.nuevos.length, 1);
    assert.equal(r.nuevos[0].tipo, 'informacion'); assert.doesNotMatch(r.nuevos[0].texto, /QR_|FICTICIO-PAGO/);
  });
  test(nombre + ': pendiente con QR ficticio y aviso, sin acceso', () => {
    const m = motor(); pendiente(m); assert.equal(estado(m), 'pendiente'); assert.equal(accesos(m), 0);
    assert.equal(m.snapshot().salida.filter(x => x.tipo === 'qr').length, 1);
    assert.equal(m.snapshot().salida.filter(x => x.tipo === 'aviso_operador').length, 1);
  });
  test(nombre + ': captura con o sin referencia nunca confirma', () => {
    for (const referencia of ['', 'FICTICIO-PAGO-A']) {
      const m = motor(); pendiente(m);
      m.recibirCliente(e('foto', {accion: 'captura', referencia}), 2000);
      assert.equal(estado(m), 'pendiente'); assert.equal(accesos(m), 0);
    }
  });
  test(nombre + ': sólo señal explícita completa confirma y prepara acceso', () => {
    const m = motor(); pendiente(m); m.confirmarOperador(confirmacion(), 2000);
    assert.equal(estado(m), 'confirmado'); assert.equal(accesos(m), 1);
    assert.match(m.snapshot().salida.at(-1).texto, /ACCESO_FICTICIO_NO_VALIDO/);
  });
  test(nombre + ': cliente no puede inyectar confirmación', () => {
    const m = motor(); pendiente(m); const antes = m.snapshot();
    assert.throws(() => m.recibirCliente(confirmacion({accion: 'confirmar'}), 2000), /ACCION_CLIENTE/);
    assert.deepEqual(m.snapshot(), antes);
  });
  test(nombre + ': señal no explícita o actor inválido rechazada sin mutar', () => {
    for (const dato of [{decision: 'pagado'}, {operador: 'cliente'}]) {
      const m = motor(); pendiente(m); const antes = m.snapshot();
      assert.throws(() => m.confirmarOperador(confirmacion(dato), 2000), /SENAL_NO_EXPLICITA/);
      assert.deepEqual(m.snapshot(), antes);
    }
  });
  test(nombre + ': importe, moneda, movimiento y destino exigen conciliación', () => {
    for (const dato of [{importe: 49}, {importe: '50'}, {moneda: 'USD'},
      {movimientoVerificado: false}, {destinoVerificado: false}]) {
      const m = motor(); pendiente(m); m.confirmarOperador(confirmacion(dato), 2000);
      assert.equal(estado(m), 'excepcion'); assert.equal(accesos(m), 0);
    }
  });
  test(nombre + ': replay y otra inscripción no duplican QR ni acceso', () => {
    const m = motor(); pendiente(m); const n = m.snapshot().salida.length;
    assert.equal(pendiente(m).resultado, 'duplicado');
    m.recibirCliente(e('alta-dos', {accion: 'inscribir', plan: 'vip'}), 1100);
    assert.equal(m.snapshot().salida.length, n);
    m.confirmarOperador(confirmacion(), 2000);
    assert.equal(m.confirmarOperador(confirmacion(), 2000).resultado, 'duplicado');
    assert.equal(m.confirmarOperador(confirmacion({id: 'fixture-otro-op'}), 3000).resultado, 'ya_confirmado');
    assert.equal(accesos(m), 1);
  });
  test(nombre + ': mismo ID con contenido distinto se rechaza', () => {
    const m = motor(); pendiente(m); const antes = m.snapshot();
    assert.throws(() => m.recibirCliente(e('alta', {accion: 'inscribir', plan: 'vip'}), 1000), /ID_REUTILIZADO/);
    assert.deepEqual(m.snapshot(), antes);
  });
  test(nombre + ': estado serializado mantiene deduplicación al retomar', () => {
    const m = motor(); pendiente(m); m.confirmarOperador(confirmacion(), 2000);
    const restaurado = crear(catalogo, JSON.parse(JSON.stringify(m.snapshot())));
    assert.equal(restaurado.confirmarOperador(confirmacion(), 3000).resultado, 'duplicado');
    assert.equal(accesos(restaurado), 1);
  });
  test(nombre + ': timeout en el límite y reintento no dan acceso', () => {
    for (const via of ['reloj', 'operador', 'captura']) {
      const m = motor(); pendiente(m);
      if (via === 'reloj') m.vencer(e('tick'), 1000 + TTL);
      if (via === 'operador') m.confirmarOperador(confirmacion(), 1000 + TTL);
      if (via === 'captura') m.recibirCliente(e('foto', {accion: 'captura'}), 1000 + TTL);
      assert.equal(estado(m), 'excepcion'); assert.equal(accesos(m), 0);
      assert.throws(() => m.confirmarOperador(confirmacion({id: 'fixture-tarde'}), 1001 + TTL), /ESTADO_NO_CONFIRMABLE/);
    }
  });
  test(nombre + ': referencia reclamada por otro pendiente o confirmado va a excepción', () => {
    for (const confirmarPrimero of [false, true]) {
      const m = motor(); pendiente(m);
      m.recibirCliente(e('foto', {accion: 'captura', referencia: ' ficticio-pago-a '}), 1500);
      if (confirmarPrimero) m.confirmarOperador(confirmacion(), 1600);
      m.recibirCliente(e('alta-b', {cliente: 'fixture-cliente-b', accion: 'inscribir', plan: 'grupal'}), 2000);
      m.recibirCliente(e('foto-b', {cliente: 'fixture-cliente-b', accion: 'captura', referencia: 'FICTICIO-PAGO-A'}), 2500);
      assert.equal(m.snapshot().clientes['fixture-cliente-b'].motivo, 'REFERENCIA_REUTILIZADA');
      assert.equal(accesos(m), confirmarPrimero ? 1 : 0);
    }
  });
  test(nombre + ': referencia repetida en operador o captura no produce segundo acceso', () => {
    for (const via of ['cliente', 'operador']) {
      const m = motor(); pendiente(m); m.confirmarOperador(confirmacion(), 2000);
      m.recibirCliente(e('alta-b', {cliente: 'fixture-cliente-b', accion: 'inscribir', plan: 'grupal'}), 3000);
      if (via === 'cliente') m.recibirCliente(e('foto-b', {cliente: 'fixture-cliente-b', accion: 'captura', referencia: ' ficticio-pago-a '}), 4000);
      else m.confirmarOperador(confirmacion({id: 'fixture-op-b', cliente: 'fixture-cliente-b'}), 4000);
      assert.equal(m.snapshot().clientes['fixture-cliente-b'].estado, 'excepcion'); assert.equal(accesos(m), 1);
    }
  });
  test(nombre + ': una referencia distinta de la captura requiere revisión', () => {
    const m = motor(); pendiente(m);
    m.recibirCliente(e('foto', {accion: 'captura', referencia: 'FICTICIO-PAGO-A'}), 2000);
    m.confirmarOperador(confirmacion({referencia: 'FICTICIO-PAGO-B'}), 3000);
    assert.equal(estado(m), 'excepcion'); assert.equal(accesos(m), 0);
  });
  test(nombre + ': sexto VIP no se confirma, grupal no tiene límite fijado', () => {
    const m = motor();
    for (let i = 0; i < 7; i++) {
      const c = 'fixture-vip-' + i;
      m.recibirCliente(e('vip-alta-' + i, {cliente: c, accion: 'inscribir', plan: 'vip'}), i * 10);
      m.confirmarOperador(confirmacion({id: 'fixture-vip-op-' + i, cliente: c, importe: 150, referencia: 'FICTICIO-VIP-' + i}), i * 10 + 1);
    }
    assert.equal(accesos(m), 5); assert.equal(m.snapshot().clientes['fixture-vip-5'].estado, 'excepcion');
    for (let i = 0; i < 7; i++) {
      const c = 'fixture-grupal-' + i;
      m.recibirCliente(e('grupal-alta-' + i, {cliente: c, accion: 'inscribir', plan: 'grupal'}), 100 + i * 10);
      m.confirmarOperador(confirmacion({id: 'fixture-grupal-op-' + i, cliente: c, referencia: 'FICTICIO-GRUPAL-' + i}), 101 + i * 10);
    }
    assert.equal(accesos(m), 12);
  });
  test(nombre + ': baja detiene mensajes posteriores y acceso', () => {
    const m = motor(); pendiente(m); m.recibirCliente(e('baja', {accion: 'baja'}), 2000);
    assert.equal(m.recibirCliente(e('info', {accion: 'interes'}), 3000).nuevos.length, 0);
    assert.throws(() => m.confirmarOperador(confirmacion(), 4000), /INSCRIPCION_NO_DISPONIBLE/);
    assert.equal(accesos(m), 0);
  });
  test(nombre + ': vencimiento posterior a BAJA no emite mensajes', () => {
    const m = motor(); pendiente(m);
    m.recibirCliente(e('baja', {accion: 'baja'}), 2000);
    assert.equal(m.vencer(e('tick-baja'), 1000 + TTL).nuevos.length, 0);
    assert.equal(m.snapshot().clientes[cliente].cese, true);
  });
  test(nombre + ': reloj viejo, identidad y datos reales rechazados', () => {
    const m = motor(); pendiente(m);
    assert.throws(() => m.recibirCliente(e('x', {accion: 'interes'}), 999), /RELOJ_INVALIDO/);
    assert.throws(() => m.recibirCliente(e('x', {cliente: '__proto__', accion: 'interes'}), 2000), /CLIENTE_INVALIDO/);
    assert.throws(() => m.recibirCliente(e('x', {ficticio: false, accion: 'interes'}), 2000), /SOLO_FIXTURES/);
    assert.throws(() => m.recibirCliente(e('x', {accion: 'inscribir', plan: 'otro'}), 2000), /PLAN_INVALIDO/);
  });
  test(nombre + ': QR, acceso y referencia ajenos al contrato no se conservan', () => {
    const m = motor(); pendiente(m); const antes = m.snapshot();
    for (const campo of ['qr', 'qrPath', 'acceso', 'credentials'])
      assert.throws(() => m.recibirCliente(e('extra', {accion: 'captura', [campo]: 'RECHAZAR'}), 2000), /CAMPO_NO_PERMITIDO/);
    assert.throws(() => m.recibirCliente(e('ref', {accion: 'captura', referencia: 'NO-FICTICIA'}), 2000), /SOLO_REFERENCIA_FICTICIA/);
    assert.deepEqual(m.snapshot(), antes);
  });
}

test('Meta: batch completo; texto de pago y estados de entrega no confirman', () => {
  const payload = structuredClone(fixture.pasos[0].payload);
  const v = payload.entry[0].changes[0].value;
  v.messages.push({id: 'fixture-falso-op', from: cliente, type: 'text', text: {body: 'PAGO CONFIRMADO operador-ficticio'}});
  v.statuses = [{status: 'read'}];
  assert.equal(normalizarMeta(payload).length, 2);
  assert.equal(normalizarMeta(payload)[1].accion, 'desconocido');
  delete v.messages; assert.deepEqual(normalizarMeta(payload), []);
  assert.throws(() => normalizarMeta({object: 'whatsapp_business_account'}), /SOLO_FIXTURE_META/);
});
test('workflow: fuente regenerable exacta, inactiva y sólo nodos permitidos', () => {
  assert.deepEqual(workflow, construir()); assert.equal(workflow.active, false);
  assert.deepEqual(workflow.nodes.map(n => n.type), ['n8n-nodes-base.manualTrigger', 'n8n-nodes-base.code', 'n8n-nodes-base.code']);
  for (const nodo of workflow.nodes) assert.equal(Object.hasOwn(nodo, 'credentials'), false);
  assert.deepEqual(workflow.connections.Manual.main[0][0], {node: 'Fixture FICTICIO', type: 'main', index: 0});
  assert.equal(workflow.connections['Fixture FICTICIO'].main[0][0].node, 'Simular sin efectos');
});
test('workflow: Code exacto y módulo dan el mismo recorrido y un solo acceso', () => {
  const local = ejecutarEscenario(fixture, catalogo);
  assert.deepEqual(ejecutarWorkflow(workflow), local);
  assert.equal(local.snapshot.clientes[cliente].estado, 'confirmado');
  assert.equal(local.resultados[2].nuevos.some(x => x.tipo === 'confirmado'), false);
  assert.equal(local.resultados.at(-1).resultado, 'duplicado');
  assert.equal(local.snapshot.salida.filter(x => x.tipo === 'confirmado').length, 1);
});
test('decisiones actuales en mensajes, QR y acceso exclusivos de prueba', () => {
  const oferta = catalogo.oferta;
  assert.equal(oferta.nombre, 'Claude de 0 a 100: tu negocio con IA');
  assert.ok(catalogo.textos.informacion.includes(oferta.nombre));
  assert.deepEqual(oferta.clases, ['2026-11-12T21:00:00-04:00', '2026-11-13T21:00:00-04:00', '2026-11-14T14:00:00-04:00']);
  assert.equal(oferta.zona, 'America/La_Paz'); assert.equal(oferta.plataforma, 'Google Meet');
  assert.equal(oferta.grupal.cupos, null); assert.equal(oferta.vip.llamada_minutos, 30);
  assert.equal(catalogo.aprobacion_editorial, false);
  const texto = fs.readFileSync(path.join(__dirname, 'workflow-n8n.json'), 'utf8');
  assert.doesNotMatch(texto, /https?:\/\/|Bearer |EA[A-Za-z0-9]{30,}|BEGIN .*PRIVATE KEY|data:image|\/home\//);
  for (const n of workflow.nodes.filter(n => n.parameters.jsCode))
    assert.doesNotMatch(n.parameters.jsCode, /\brequire\s*\(|\bfetch\s*\(|\bprocess\.|\$http|\$env/);
  assert.match(catalogo.textos.qr, /QR_FICTICIO_SIN_VALOR/);
  assert.match(catalogo.textos.confirmado, /ACCESO_FICTICIO_NO_VALIDO/);
});

test('despacho n8n: sólo trigger manual y petición privada sin guardar ejecuciones', () => {
  const despacho = require('./workflow-despacho-n8n.json');
  assert.equal(despacho.active, false);
  assert.deepEqual(despacho.nodes.map(n => [n.type, n.typeVersion]), [
    ['n8n-nodes-base.manualTrigger', 1],
    ['n8n-nodes-base.httpRequest', 4.2]
  ]);
  const [manual, peticion] = despacho.nodes;
  assert.deepEqual(despacho.connections, {
    [manual.name]: {main: [[{node: peticion.name, type: 'main', index: 0}]]}
  });
  assert.deepEqual(despacho.settings, {
    executionOrder: 'v1',
    saveDataErrorExecution: 'none',
    saveDataSuccessExecution: 'none',
    saveManualExecutions: false,
    saveExecutionProgress: false
  });
  assert.deepEqual(despacho.pinData, {});
  assert.ok(despacho.nodes.every(n => !Object.hasOwn(n, 'credentials')));
  assert.equal(peticion.retryOnFail, false);
  const {url, ...parametros} = peticion.parameters;
  assert.equal(typeof url, 'string');
  assert.deepEqual(parametros, {
    method: 'POST', authentication: 'genericCredentialType', genericAuthType: 'httpHeaderAuth',
    sendBody: false, options: {redirect: {redirect: {followRedirects: false}}, timeout: 20000}
  });
});

test('despacho n8n: URL de entorno obligatoria, ruta fija y sin destino en la exportación', () => {
  const {url} = require('./workflow-despacho-n8n.json').nodes[1].parameters;
  assert.match(url, /^=\{\{.*\}\}$/);
  assert.doesNotMatch(url, /https?:\/\/|\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b/);
  const expresion = url.slice(3, -2);
  const resolver = $env => vm.runInNewContext(expresion, {$env}, {timeout: 1000});
  assert.equal(resolver({}), '');
  assert.equal(resolver({ONIA_CHATBOT_DISPATCH_BASE_URL: ''}), '');
  for (const sufijo of ['', '/']) {
    assert.equal(resolver({ONIA_CHATBOT_DISPATCH_BASE_URL: 'https://fixture.invalid' + sufijo}),
      'https://fixture.invalid/operador/despachar');
  }
});

'use strict';

// Núcleo puro, exclusivo para fixtures. Nunca autentica ni envía a Meta/n8n.
function crearMotor(catalogo, snapshot) {
  const s = snapshot ? JSON.parse(JSON.stringify(snapshot)) : {
    version: 1, reloj: 0, clientes: {}, referencias: {}, vistos: {}, salida: [], auditoria: []
  };
  const TTL = 24 * 60 * 60 * 1000; // Propuesta técnica, no plazo comercial aprobado.
  const idValido = value => typeof value === 'string' && /^fixture-[a-z0-9-]{1,80}$/.test(value);
  const refCanonica = value => typeof value === 'string' ? value.trim().toUpperCase() : '';
  const refValida = value => /^FICTICIO-[A-Z0-9-]{1,80}$/.test(value);
  const serializar = value => {
    if (Array.isArray(value)) return '[' + value.map(serializar).join(',') + ']';
    if (value && typeof value === 'object') return '{' + Object.keys(value).sort()
      .map(k => JSON.stringify(k) + ':' + serializar(value[k])).join(',') + '}';
    return JSON.stringify(value);
  };
  function exigir(ok, motivo) { if (!ok) throw Error(motivo); }
  exigir(catalogo?.oferta?.grupal?.importe === 50 && catalogo?.oferta?.vip?.importe === 150 &&
    catalogo.oferta.vip.cupos === 5 && catalogo.oferta.moneda === 'BOB', 'OFERTA_INVALIDA');
  exigir(s.version === 1, 'SNAPSHOT_INVALIDO');

  function procesar(canal, evento, ahora) {
    // El reloj lo aporta el llamador, nunca el timestamp del mensaje del cliente.
    exigir(['cliente', 'operador', 'reloj'].includes(canal), 'CANAL_INVALIDO');
    exigir(evento?.ficticio === true && idValido(evento.id), 'SOLO_FIXTURES');
    exigir(Number.isSafeInteger(ahora) && ahora >= s.reloj, 'RELOJ_INVALIDO');
    if (canal !== 'reloj') exigir(idValido(evento.cliente), 'CLIENTE_INVALIDO');
    const permitidos = ['ficticio', 'id', 'cliente', 'accion', 'plan', 'referencia',
      'operador', 'decision', 'importe', 'moneda', 'movimientoVerificado', 'destinoVerificado'];
    exigir(Object.keys(evento).every(k => permitidos.includes(k)), 'CAMPO_NO_PERMITIDO');
    exigir(evento.referencia === undefined || evento.referencia === '' ||
      refValida(refCanonica(evento.referencia)), 'SOLO_REFERENCIA_FICTICIA');
    const key = canal + ':' + evento.id;
    const firma = serializar(evento);
    if (Object.hasOwn(s.vistos, key)) {
      exigir(s.vistos[key] === firma, 'ID_REUTILIZADO_CON_OTRO_CONTENIDO');
      return {resultado: 'duplicado', nuevos: []};
    }
    const comienzo = s.salida.length;
    const emitir = (tipo, destino, datos = {}) => {
      const texto = catalogo.textos[tipo].replace(/\{(\w+)\}/g, (_, k) => String(datos[k] ?? ''));
      s.salida.push({id: key + ':' + (s.salida.length - comienzo), tipo, destino, texto, ficticio: true});
    };
    const aviso = (cliente, motivo) => emitir('aviso_operador', 'operador-ficticio', {cliente, motivo});
    const excepcion = (cliente, motivo) => {
      const c = s.clientes[cliente];
      c.estado = 'excepcion'; c.motivo = motivo;
      emitir('excepcion', cliente); aviso(cliente, motivo);
    };
    let resultado = 'procesado';
    if (canal === 'reloj') {
      for (const [cliente, c] of Object.entries(s.clientes)) {
        if (c.estado === 'pendiente' && ahora >= c.vence) excepcion(cliente, 'PAGO_VENCIDO');
      }
    } else if (canal === 'cliente') {
      const acciones = ['interes', 'inscribir', 'captura', 'ayuda', 'baja', 'desconocido'];
      exigir(acciones.includes(evento.accion), 'ACCION_CLIENTE_NO_PERMITIDA');
      if (evento.accion === 'inscribir') exigir(['grupal', 'vip'].includes(evento.plan), 'PLAN_INVALIDO');
      const c = s.clientes[evento.cliente] ??= {estado: 'interesado', cese: false};
      if (c.cese) resultado = 'contacto_detenido';
      else if (evento.accion === 'baja') {
        c.cese = true; emitir('cese', evento.cliente);
      } else if (evento.accion === 'interes') emitir('informacion', evento.cliente);
      else if (evento.accion === 'ayuda') aviso(evento.cliente, 'AYUDA_SOLICITADA');
      else if (evento.accion === 'inscribir') {
        if (c.estado === 'interesado') {
          Object.assign(c, {estado: 'pendiente', plan: evento.plan,
            importe: catalogo.oferta[evento.plan].importe, vence: ahora + TTL});
          emitir('pendiente', evento.cliente, c); emitir('qr', evento.cliente);
          aviso(evento.cliente, 'INSCRIPCION_PENDIENTE');
        } else resultado = 'inscripcion_existente';
      } else if (evento.accion === 'captura') {
        if (c.estado !== 'pendiente') resultado = 'sin_pendiente';
        else if (ahora >= c.vence) excepcion(evento.cliente, 'PAGO_VENCIDO');
        else {
          const ref = refCanonica(evento.referencia);
          // La referencia es opcional en la captura. La imagen no se descarga ni se conserva.
          if (ref && s.referencias[ref] && s.referencias[ref] !== evento.cliente)
            excepcion(evento.cliente, 'REFERENCIA_REUTILIZADA');
          else if (ref && c.referencia && c.referencia !== ref)
            excepcion(evento.cliente, 'REFERENCIA_CAMBIADA');
          else {
            if (ref) { c.referencia = ref; s.referencias[ref] = evento.cliente; }
            emitir('captura', evento.cliente); aviso(evento.cliente, 'COMPROBANTE_NO_VERIFICADO');
          }
        }
      } else emitir('ayuda', evento.cliente);
    } else {
      // Sólo la API local separada recibe esta señal. Ningún texto/imagen la genera.
      exigir(evento.operador === 'operador-ficticio' && evento.decision === 'confirmar', 'SENAL_NO_EXPLICITA');
      const c = s.clientes[evento.cliente];
      exigir(c && !c.cese, 'INSCRIPCION_NO_DISPONIBLE');
      const ref = refCanonica(evento.referencia);
      exigir(refValida(ref), 'REFERENCIA_INVALIDA');
      if (c.estado === 'confirmado') {
        exigir(c.referencia === ref, 'PAGO_YA_CONFIRMADO_CON_OTRA_REFERENCIA');
        resultado = 'ya_confirmado';
      } else {
        exigir(c.estado === 'pendiente', 'ESTADO_NO_CONFIRMABLE');
        if (ahora >= c.vence) excepcion(evento.cliente, 'PAGO_VENCIDO');
        else if (s.referencias[ref] && s.referencias[ref] !== evento.cliente)
          excepcion(evento.cliente, 'REFERENCIA_REUTILIZADA');
        else if (c.referencia && c.referencia !== ref) excepcion(evento.cliente, 'REFERENCIA_NO_COINCIDE');
        else if (evento.movimientoVerificado !== true || evento.destinoVerificado !== true ||
          evento.moneda !== 'BOB' || evento.importe !== c.importe)
          excepcion(evento.cliente, 'CONCILIACION_INCOMPLETA');
        else if (c.plan === 'vip' && Object.values(s.clientes)
          .filter(x => x.plan === 'vip' && x.estado === 'confirmado').length >= 5)
          excepcion(evento.cliente, 'VIP_SIN_CUPO');
        else {
          c.estado = 'confirmado'; c.referencia = ref;
          s.referencias[ref] = evento.cliente;
          emitir('confirmado', evento.cliente);
        }
      }
    }
    s.reloj = ahora; s.vistos[key] = firma;
    s.auditoria.push({id: key, resultado, ahora, cliente: evento.cliente ?? null,
      estado: s.clientes[evento.cliente]?.estado ?? null});
    return {resultado, nuevos: JSON.parse(JSON.stringify(s.salida.slice(comienzo)))};
  }
  return {
    recibirCliente: (e, ahora) => procesar('cliente', e, ahora),
    confirmarOperador: (e, ahora) => procesar('operador', e, ahora),
    vencer: (e, ahora) => procesar('reloj', e, ahora),
    snapshot: () => JSON.parse(JSON.stringify(s))
  };
}

// Proyección de mensajes sintéticos con forma Meta; no verifica firma HTTP.
function normalizarMeta(payload) {
  if (payload?.ficticio !== true || payload.object !== 'whatsapp_business_account')
    throw Error('SOLO_FIXTURE_META');
  const salida = [];
  for (const entry of payload.entry ?? []) for (const change of entry.changes ?? []) {
    if (change.field !== 'messages') continue;
    for (const m of change.value?.messages ?? []) {
      const base = {id: m.id, cliente: m.from, ficticio: true};
      const texto = (m.text?.body ?? '').trim().toUpperCase();
      if (m.type === 'image') salida.push({...base, accion: 'captura', referencia: m.image?.caption ?? ''});
      else if (m.type !== 'text') salida.push({...base, accion: 'desconocido'});
      else if (texto === 'NEGOCIO') salida.push({...base, accion: 'interes'});
      else if (['GRUPAL', 'VIP'].includes(texto)) salida.push({...base, accion: 'inscribir', plan: texto.toLowerCase()});
      else salida.push({...base, accion: ({BAJA: 'baja', AYUDA: 'ayuda'})[texto] ?? 'desconocido'});
    }
  }
  return salida; // statuses de entrega/lectura no son pagos ni señales del operador.
}

function ejecutarEscenario(escenario, catalogo, snapshot) {
  if (escenario?.ficticio !== true) throw Error('SOLO_FIXTURES');
  const motor = crearMotor(catalogo, snapshot);
  const resultados = [];
  for (const paso of escenario.pasos) {
    if (paso.canal === 'meta') {
      for (const evento of normalizarMeta(paso.payload)) resultados.push(motor.recibirCliente(evento, paso.ahora));
    } else if (paso.canal === 'operador') resultados.push(motor.confirmarOperador(paso.evento, paso.ahora));
    else if (paso.canal === 'reloj') resultados.push(motor.vencer(paso.evento, paso.ahora));
    else throw Error('CANAL_INVALIDO');
  }
  return {simulacion: true, resultados, snapshot: motor.snapshot()};
}

module.exports = {crearMotor, normalizarMeta, ejecutarEscenario};

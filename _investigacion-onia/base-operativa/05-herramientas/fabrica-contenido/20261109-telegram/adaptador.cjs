'use strict';

const { createHash } = require('crypto');

function sha(text) {
  return createHash('sha256').update(text, 'utf8').digest('hex');
}

// Coincide con encoded() del ensayo 20261108 para sus objetos JSON.
function encoded(value) {
  return JSON.stringify(value, null, 2) + '\n';
}

class Rechazo extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

function requireThat(condition, code) {
  if (!condition) throw new Rechazo(code);
}

function parseCommand(text) {
  requireThat(typeof text === 'string' && text.length <= 700, 'DATO_INVALIDO');
  const match = /^\/(elegir|cambios|descartar) ([a-z0-9-]{1,80}) ([a-z0-9-]{1,80}) ([1-9][0-9]{0,8}) ([a-f0-9]{64})(?: ([^\r\n]{1,200}))?$/.exec(text);
  requireThat(match !== null, 'COMANDO_INVALIDO');
  const [, command, taskId, scriptId, revision, scriptHash, reason = ''] = match;
  requireThat(command === 'elegir' ? reason === '' : reason.trim().length > 0, 'MOTIVO_INVALIDO');
  return { command, taskId, scriptId, revision: Number(revision), scriptHash, reason };
}

// policy y loadSnapshot pertenecen al llamador de confianza. Esta implementación
// acepta exclusivamente simulación. Un campo del mensaje nunca autentica ingreso.
function adapt(event, policy, loadSnapshot, receipts) {
  try {
    requireThat(policy.mode === 'fixture' && policy.transportVerified === true, 'TRANSPORTE_NO_VALIDADO');
    requireThat(event?.synthetic === true, 'SOLO_SIMULACION');
    const message = event.message;
    requireThat(message?.chat?.type === 'private' && message.from?.is_bot === false, 'IDENTIDAD_RECHAZADA');
    requireThat(Number.isSafeInteger(message.from.id) && Number.isSafeInteger(message.chat.id), 'IDENTIDAD_RECHAZADA');
    requireThat(message.from.id === policy.userId && message.chat.id === policy.chatId, 'IDENTIDAD_RECHAZADA');
    requireThat(Number.isSafeInteger(event.update_id) && event.update_id >= 0, 'DATO_INVALIDO');
    const command = parseCommand(message.text);
    requireThat(policy.taskIds.includes(command.taskId), 'TAREA_NO_PERMITIDA');
    const transportKey = sha(encoded([policy.botAlias, message.chat.id, event.update_id]));
    const payloadHash = sha(encoded(command));
    const businessKey = sha(encoded([command.taskId, command.revision, command.scriptId,
      command.scriptHash, command.command, command.reason]));
    const priorTransport = receipts.transport[transportKey];
    if (priorTransport) {
      requireThat(priorTransport.payloadHash === payloadHash, 'REPLAY_CONFLICTIVO');
      return { status: 'duplicado', receipt: priorTransport.receipt };
    }
    const priorBusiness = receipts.business[businessKey];
    if (priorBusiness) {
      receipts.transport[transportKey] = { payloadHash, receipt: priorBusiness };
      return { status: 'duplicado', receipt: priorBusiness };
    }
    let snapshot;
    try {
      snapshot = loadSnapshot(command.taskId);
    } catch {
      throw new Rechazo('DEPENDENCIA_NO_DISPONIBLE');
    }
    requireThat(snapshot?.verified === true && snapshot.task?.id === command.taskId, 'SNAPSHOT_INVALIDO');
    requireThat(snapshot.task.revision === command.revision, 'REVISION_VIEJA');
    requireThat(['preparado', 'en_curso', 'en_espera'].includes(snapshot.task.estado), 'TAREA_CERRADA');
    const script = snapshot.scripts[command.scriptId];
    const review = snapshot.reviews[command.scriptId];
    requireThat(script && review, 'GUION_DESCONOCIDO');
    requireThat(sha(encoded(script)) === command.scriptHash, 'HASH_GUION_INVALIDO');
    requireThat(review.guion_id === command.scriptId && review.guion_sha256 === command.scriptHash,
      'REVISION_EDITORIAL_INVALIDA');
    if (command.command === 'elegir') {
      requireThat(review.veredicto === 'bueno' && Object.keys(review.controles).length > 0 &&
        Object.values(review.controles).every(value => value === true), 'GUION_CON_CAMBIOS');
    }
    const verdicts = { elegir: 'elegir_para_preparar', cambios: 'pedir_cambios', descartar: 'descartar' };
    const receipt = {
      simulacion: true,
      decision_id: 'telegram-' + businessKey,
      tarea: command.taskId,
      revision_esperada: command.revision,
      guion_id: command.scriptId,
      guion_sha256: command.scriptHash,
      revision_sha256: sha(encoded(review)),
      veredicto: verdicts[command.command],
      motivo: command.reason,
      autor: 'Sergio SIMULADO',
      alcance: 'decision_editorial_sin_efectos',
    };
    // Recibo técnico efímero del ensayo. No crea una cola ni muta el harness.
    receipts.transport[transportKey] = { payloadHash, receipt };
    receipts.business[businessKey] = receipt;
    return { status: 'preparado_seco', receipt };
  } catch (error) {
    return { status: 'rechazado', code: error instanceof Rechazo ? error.code : 'DEPENDENCIA_NO_DISPONIBLE' };
  }
}

module.exports = { adapt, encoded, sha, parseCommand };

if (require.main === module) {
  const fs = require('fs');
  try {
    const input = JSON.parse(fs.readFileSync(0, 'utf8'));
    const receipts = { transport: {}, business: {} };
    const output = input.events.map(event => adapt(event, input.policy,
      () => input.snapshot, receipts));
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  } catch {
    process.stdout.write(JSON.stringify({ status: 'rechazado', code: 'ENTRADA_INVALIDA' }) + '\n');
    process.exitCode = 1;
  }
}

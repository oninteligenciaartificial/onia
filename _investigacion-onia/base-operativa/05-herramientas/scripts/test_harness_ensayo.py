"""Ensayo completamente local. Sin RPC real, cuota real ni sesiones de modelos."""
from copy import deepcopy
from contextlib import redirect_stdout, ExitStack, nullcontext
import io
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import harness_boss as private
import harness_ensayo as trial
import harness_sesiones as sessions


def quota_sample(now=None, used=10):
    now = time.time() if now is None else now
    return {'fecha': now, 'ventanas': {name: {'usedPercent': used,
            'windowDurationMins': duration, 'resetsAt': int(now) + 7200}
            for name, duration in [('primary', 300), ('secondary', 10080)]}}


def resource_sample(now=None):
    return {'fecha': time.time() if now is None else now, 'cpu': 10, 'ram_disponible': 80,
            'psi_cpu': 0, 'psi_memoria': 0, 'psi_io': 0, 'swap_usado': 0, 'swap_paginas_s': 0}


def install_trial(root, base, ids):
    root.mkdir(mode=0o700, exist_ok=True)
    root.chmod(0o700)
    path = root / trial.DIRECTORY
    path.mkdir(mode=0o700)
    now = time.time()
    value = {'schema': 1, 'lote': 'a' * 32, 'base': str(base), 'ids': ids,
             'inicio': now, 'vence': now + 1800, 'presupuesto': 2, 'cuota_inicial': quota_sample(now)}
    private.private_write(path / 'politica.json', value)
    private.private_write(path / 'preparacion.json', {'politica_sha256': trial.digest(value)})
    write_state(root, value)
    return value


def write_state(root, value, **changes):
    state = {'estado': 'listo', 'politica_sha256': trial.digest(value), 'fecha': time.time(),
             'pid': os.getpid(), 'pid_inicio': sessions.process_start(os.getpid()),
             'cuota': deepcopy(value['cuota_inicial']), 'recursos': resource_sample()}
    path = root / trial.DIRECTORY
    if not (path / 'procesos.json').exists():
        private.private_write(path / 'procesos.json', {'politica_sha256': trial.digest(value), 'procesos': []})
    state['procesos_sha256'] = trial.digest(private.private_read(path / 'procesos.json'))
    state.update(changes)
    state['recibo'] = trial.receipt(path, dict(state, evento='muestra'))
    private.private_write(path / 'estado.json', state)
    return state


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='test-ensayo-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base = self.root / 'base'
        self.base.mkdir()
        self.op = self.root / 'operacion'
        self.ids = ['uno', 'dos', 'tres', 'cuatro']
        self.value = install_trial(self.op, self.base, self.ids)
        self.path = self.op / trial.DIRECTORY
        self.tag = trial.digest(self.value)

    def rows(self, count=3):
        return [(self.base, {'id': ident, 'sesiones': [{'estado': 'ejecutando', 'dry_run': False,
            'rol': 'revisor' if index == 1 else 'ejecutor', 'rutas': ['salida/' + ident],
            'pid': None, 'pid_inicio': None, 'ensayo_sha256': self.tag}]})
            for index, ident in enumerate(self.ids[:count])]

    def capacity(self, rows, ident='cuatro', routes=None, role='ejecutor', base=None):
        with patch.object(sessions, 'alive', side_effect=lambda s: s.get('estado') == 'ejecutando'):
            return sessions.check_capacity(rows, ident, base or self.base,
                                           routes or ['salida/' + ident], role, root=self.op)

    def test_fourth_admitted_with_global_reviewer_and_fifth_rejected(self):
        self.assertEqual(self.capacity(self.rows()), self.tag)
        with self.assertRaisesRegex(ValueError, 'Máximo 4'):
            self.capacity(self.rows(4), 'uno')

    def test_default_three_and_no_environment_bypass(self):
        default = self.root / 'default'
        with patch.dict(os.environ, {'ONIA_MAX_SESSIONS': '999', 'ONIA_ALLOW_FOUR': '1'}), \
                patch.object(sessions, 'alive', return_value=True):
            with self.assertRaisesRegex(ValueError, 'Máximo 3'):
                sessions.check_capacity(self.rows(), 'cuatro', self.base, ['cuatro'], 'revisor', root=default)

    def test_question_reservation_counts_with_reviewer_globally(self):
        slot = {'estado': 'respondiendo', 'vence': time.time() + 30, 'base': str(self.base),
                'ensayo_sha256': self.tag}
        private.private_write(self.op / 'preguntas-slots/tres.json', slot)
        self.assertEqual(self.capacity(self.rows(2)), self.tag)
        private.private_write(self.op / 'preguntas-slots/cuatro.json', slot)
        with self.assertRaisesRegex(ValueError, 'Máximo 4'):
            self.capacity(self.rows(2), 'uno')

    def test_duplicate_question_id_is_rejected(self):
        private.private_write(self.op / 'preguntas-slots/cuatro.json',
                              {'estado': 'respondiendo', 'vence': time.time() + 30,
                               'base': str(self.base), 'ensayo_sha256': self.tag})
        with self.assertRaisesRegex(ValueError, 'pregunta viva'):
            self.capacity([])

    def test_unauthorized_base_id_and_foreign_live_session(self):
        for ident, base in [('ajeno', self.base), ('cuatro', self.root)]:
            with self.subTest(ident=ident, base=base), self.assertRaisesRegex(ValueError, 'no_autorizado'):
                self.capacity([], ident, base=base)
        for key, value in [('ensayo_sha256', 'alterado'), ('dry_run', True)]:
            rows = self.rows(1)
            rows[0][1]['sesiones'][0][key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, 'sesion_ajena'):
                self.capacity(rows)
        with self.assertRaisesRegex(ValueError, 'sesion_ajena'):
            self.capacity([(self.root, self.rows(1)[0][1])])

    def test_collisions_and_duplicate_ids(self):
        with self.assertRaisesRegex(ValueError, 'Colisión'):
            self.capacity(self.rows(1), routes=['salida/uno/subruta'])
        with self.assertRaisesRegex(ValueError, 'ya tiene una sesión'):
            self.capacity(self.rows(1), 'uno')
        duplicated = self.rows(1) * 2
        with self.assertRaisesRegex(ValueError, 'id_duplicado'):
            self.capacity(duplicated)

    def test_expiration_maximum_and_invalid_data(self):
        for changes in [{'vence': self.value['inicio'] + 1801}, {'vence': time.time() - 1},
                        {'inicio': time.time() + 50}, {'presupuesto': 3}, {'presupuesto': True},
                        {'ids': ['uno', 'uno']}, {'schema': True}, {'extra': 'dato'},
                        {'vence': float('nan')}]:
            changed = dict(self.value, **changes)
            private.private_write(self.path / 'politica.json', changed)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.capacity([])
        private.private_write(self.path / 'politica.json', self.value)
        self.assertEqual(self.capacity([]), self.tag)

    def test_stop_missing_or_dead_monitor_blocks(self):
        for changes in [{'pid_inicio': 'PID-reciclado'}, {'pid': None},
                        {'estado': 'bloqueado'}, {'fecha': time.time() - 16}]:
            write_state(self.op, self.value, **changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.capacity([])
        write_state(self.op, self.value)
        private.private_write(self.path / 'STOP', {'motivo': 'operador'})
        with self.assertRaisesRegex(ValueError, 'STOP'):
            self.capacity([])

    def test_resources_stale_future_invalid_and_saturation(self):
        for key, value in [('fecha', time.time() - 16), ('fecha', time.time() + 5), ('cpu', 85),
                           ('ram_disponible', 19), ('psi_cpu', 20), ('psi_memoria', 10),
                           ('psi_io', 10), ('swap_usado', 101), ('swap_paginas_s', 256),
                           ('cpu', float('inf')), ('cpu', True)]:
            sample = resource_sample()
            sample[key] = value
            with self.subTest(key=key, value=value):
                if value == float('inf'):
                    with self.assertRaises(ValueError):
                        trial.resources(sample, time.time())
                else:
                    write_state(self.op, self.value, recursos=sample)
                    with self.assertRaises(ValueError):
                        self.capacity([])

    def test_occupied_swap_without_pressure_does_not_block(self):
        trial.resources(dict(resource_sample(), swap_usado=95), time.time())
        for pressure in [{'swap_paginas_s': 256}, {'psi_memoria': 10}, {'ram_disponible': 19}]:
            with self.subTest(pressure=pressure), self.assertRaisesRegex(ValueError, 'saturacion'):
                trial.resources(dict(resource_sample(), swap_usado=95, **pressure), time.time())

    def test_quota_stale_unknown_rollover_and_two_point_budget(self):
        samples = [None, {}, dict(self.value['cuota_inicial'], fecha=time.time() - 61)]
        for used in [9, 12, 100, True, float('nan')]:
            sample = deepcopy(self.value['cuota_inicial'])
            sample['ventanas']['primary']['usedPercent'] = used
            samples.append(sample)
        reset = deepcopy(self.value['cuota_inicial'])
        reset['ventanas']['secondary']['resetsAt'] += 1
        samples.append(reset)
        for sample in samples:
            with self.subTest(sample=sample):
                if sample and any(isinstance(w.get('usedPercent'), float) and
                                  str(w['usedPercent']) == 'nan' for w in sample.get('ventanas', {}).values()):
                    with self.assertRaises(ValueError):
                        trial.quota(sample, time.time())
                    continue
                write_state(self.op, self.value, cuota=sample)
                with self.assertRaises(ValueError):
                    self.capacity([])
        near = deepcopy(self.value['cuota_inicial'])
        near['ventanas']['primary']['usedPercent'] = 11.99
        write_state(self.op, self.value, cuota=near)
        self.assertEqual(self.capacity([]), self.tag)

    def test_policy_state_and_receipt_tampering(self):
        changed = dict(self.value, ids=['cuatro'])
        private.private_write(self.path / 'politica.json', changed)
        with self.assertRaisesRegex(ValueError, 'politica_alterada'):
            self.capacity([])
        private.private_write(self.path / 'politica.json', self.value)
        state = write_state(self.op, self.value)
        state['recursos']['cpu'] = 0
        private.private_write(self.path / 'estado.json', state)
        with self.assertRaisesRegex(ValueError, 'estado_alterado'):
            self.capacity([])
        state = write_state(self.op, self.value)
        private.private_write(self.path / state['recibo']['archivo'], {'alterado': True})
        with self.assertRaisesRegex(ValueError, 'estado_alterado'):
            self.capacity([])

    def test_permissions_owner_symlinks_and_hardlinks(self):
        policy = self.path / 'politica.json'
        policy.chmod(0o644)
        with self.assertRaises(ValueError):
            self.capacity([])
        policy.chmod(0o600)
        other = self.root / 'other'
        os.link(policy, other)
        with self.assertRaisesRegex(ValueError, 'enlace_duro'):
            self.capacity([])
        other.unlink()
        policy.rename(other)
        policy.symlink_to(other)
        with self.assertRaises(ValueError):
            self.capacity([])
        policy.unlink()
        other.rename(policy)
        self.path.chmod(0o755)
        with self.assertRaisesRegex(ValueError, 'no_privado'):
            self.capacity([])
        self.path.chmod(0o700)
        with patch.object(trial.os, 'getuid', return_value=os.getuid() + 1):
            with self.assertRaises(ValueError):
                self.capacity([])

    def test_operation_directory_owner_only_writes_and_private_policy(self):
        self.op.chmod(0o755)
        self.assertEqual(self.capacity([]), self.tag)
        self.op.chmod(0o777)
        with self.assertRaisesRegex(ValueError, 'operacion_insegura'):
            self.capacity([])

    def test_missing_policy_and_state_fail_closed(self):
        for name in ['politica.json', 'estado.json']:
            target = self.path / name
            content = target.read_bytes()
            target.unlink()
            with self.subTest(name=name), self.assertRaises(OSError):
                self.capacity([])
            target.write_bytes(content)
            target.chmod(0o600)

    def child(self):
        process = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'])
        def cleanup():
            if process.poll() is None:
                process.terminate()
            process.wait(timeout=5)
        self.addCleanup(cleanup)
        return process

    def test_pid_recycled_and_foreign_owner_never_signaled(self):
        child = self.child()
        with patch.object(trial.signal, 'pidfd_send_signal') as send:
            sent, skipped = trial.terminate([{'pid': child.pid, 'pid_inicio': 'old-boot:1'}])
            self.assertEqual(sent, [])
            self.assertEqual(len(skipped), 1)
            send.assert_not_called()
        item = {'pid': child.pid, 'pid_inicio': sessions.process_start(child.pid)}
        with patch.object(trial, 'process_info', return_value=(os.getuid() + 1, os.getpid())), \
                patch.object(trial.signal, 'pidfd_send_signal') as send:
            with self.assertRaisesRegex(ValueError, 'proceso_ajeno'):
                trial.terminate([item])
            send.assert_not_called()
        self.assertIsNone(child.poll())

    def test_stop_only_owned_batch_and_preserves_logs(self):
        owned, other = self.child(), self.child()
        item = {'pid': owned.pid, 'pid_inicio': sessions.process_start(owned.pid)}
        journal = {'politica_sha256': self.tag, 'procesos': [item]}
        private.private_write(self.path / 'procesos.json', journal)
        write_state(self.op, self.value, procesos_sha256=trial.digest(journal))
        log = self.path / 'log-sintetico'
        log.write_text('conservar')
        with patch.object(trial, 'inventory', side_effect=lambda *_:
                          ([], [], [item] if sessions.process_start(owned.pid) == item['pid_inicio'] else [])):
            result = trial.stop(self.op)
        self.assertEqual(result['estado'], 'parado')
        self.assertTrue((self.path / 'STOP').exists())
        self.assertEqual(owned.wait(timeout=5), -signal.SIGTERM)
        self.assertIsNone(other.poll())
        self.assertEqual(log.read_text(), 'conservar')
        with self.assertRaisesRegex(ValueError, 'STOP'):
            self.capacity([])

    def test_detached_auxiliary_drained_between_monitor_samples(self):
        other = self.child()
        observed = self.root / 'auxiliary.json'
        command = """import json, os, sys, time
from pathlib import Path
if os.fork() == 0:
    os.setsid()
    if os.fork() == 0:
        Path(sys.argv[1]).write_text(json.dumps({
            "pid": os.getpid(), "sid": os.getsid(0),
            "start": Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
        }))
        time.sleep(10)
    os._exit(0)
while not Path(sys.argv[1]).exists():
    time.sleep(0.01)
"""
        wrapped = trial.custody_command(self.op, self.base, 'uno', self.tag,
                                        [sys.executable, '-c', command, str(observed)])
        with subprocess.Popen(wrapped, start_new_session=True) as worker:
            owner = {'pid': worker.pid, 'pid_inicio': sessions.process_start(worker.pid)}
            self.assertEqual(worker.wait(timeout=6), 0)
        aux = json.loads(observed.read_text())
        self.assertNotEqual(aux['sid'], owner['pid'])
        self.assertNotEqual(sessions.process_start(aux['pid']),
                            owner['pid_inicio'].rsplit(':', 1)[0] + ':' + aux['start'])
        rows = self.rows(1)
        rows[0][1]['sesiones'][0].update(owner, estado='finalizada')
        with patch.object(sessions, 'indexed_rows', return_value=rows):
            result = trial.stop(self.op)
        self.assertEqual(result['estado'], 'parado')
        self.assertEqual(result['custodias_sin_cierre'], 0)
        self.assertIsNone(other.poll())

    def test_closed_bootstrap_gate_records_drain_without_starting_model(self):
        observed = self.root / 'model-started'
        gate_read, gate_write = os.pipe()
        try:
            argv = [sys.executable, '-c', 'from pathlib import Path; import sys; Path(sys.argv[1]).touch()',
                    str(observed)]
            wrapped = trial.custody_command(self.op, self.base, 'uno', self.tag, argv, gate_read)
            with subprocess.Popen(wrapped, pass_fds=(gate_read,)) as worker:
                owner = {'pid': worker.pid, 'pid_inicio': sessions.process_start(worker.pid)}
                os.close(gate_write)
                gate_write = None
                self.assertEqual(worker.wait(timeout=6), 125)
        finally:
            os.close(gate_read)
            if gate_write is not None:
                os.close(gate_write)
        self.assertFalse(observed.exists())
        rows = self.rows(1)
        rows[0][1]['sesiones'][0].update(owner, estado='fallida')
        self.assertEqual(trial.pending_custodies(self.op, self.value, rows), [])

    def test_trial_question_worker_records_drain_before_reply(self):
        home = self.root / 'home'
        (home / 'empty').mkdir(parents=True)
        fake = """import json, sys
sys.stdin.read()
print(json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "Prueba"}}))
print(json.dumps({"type": "turn.completed"}))
"""
        bootstrap = """import sys
sys.path.insert(0, sys.argv[1])
import harness_preguntas as questions
questions.command = lambda *_: [sys.executable, '-c', sys.argv[2]]
questions.worker()
"""
        wrapped = [sys.executable, '-B', '-c', bootstrap, str(Path(trial.__file__).parent), fake]
        with subprocess.Popen(wrapped, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, start_new_session=True) as worker:
            owner = {'pid': worker.pid, 'pid_inicio': sessions.process_start(worker.pid)}
            data = dict(pid=worker.pid, parent=os.getpid(), parent_start=sessions.process_start(os.getpid()),
                        deadline=time.monotonic() + 5, home=str(home), prompt='Prueba',
                        ensayo={'operacion': str(self.op), 'base': str(self.base),
                                'id': 'uno', 'sha256': self.tag})
            output, error = worker.communicate(json.dumps(data) + '\n', timeout=7)
            self.assertEqual(worker.returncode, 0, error)
        self.assertEqual(json.loads(output)['respuesta'], 'Prueba')
        proof = trial.read(trial.custody_path(self.op, trial.custody_identity(owner, self.tag)))
        self.assertEqual(proof['estado'], 'drenada')

    def test_finished_attempt_missing_proof_keeps_stop(self):
        child = subprocess.Popen([sys.executable, '-c', 'pass'])
        owner = {'pid': child.pid, 'pid_inicio': sessions.process_start(child.pid)}
        child.wait(timeout=3)
        rows = self.rows(1)
        rows[0][1]['sesiones'][0].update(owner, estado='finalizada')
        other = self.child()
        with self.assertRaisesRegex(ValueError, 'custodia_sin_cierre'):
            self.capacity(rows)
        with patch.object(sessions, 'indexed_rows', return_value=rows):
            result = trial.stop(self.op)
        self.assertEqual(result['estado'], 'bloqueado')
        self.assertEqual(result['SIGTERM'], 0)
        self.assertEqual(result['custodias_sin_cierre'], 1)
        self.assertTrue((self.path / 'STOP').exists())
        self.assertIsNone(other.poll())

    def test_stop_rejects_custody_completion_without_independent_receipt(self):
        other = self.child()
        identity = trial.custody_identity(
            {'pid': other.pid, 'pid_inicio': sessions.process_start(other.pid)}, self.tag)
        path = trial.custody_path(self.op, identity)
        private.private_write(path, dict(identity, estado='drenada'))
        with patch.object(sessions, 'indexed_rows', return_value=[]), \
                patch.object(trial, 'terminate') as terminate:
            with self.assertRaisesRegex(ValueError, 'recibo_invalido'):
                trial.stop(self.op)
            terminate.assert_not_called()
        self.assertTrue((self.path / 'STOP').exists())
        self.assertIsNone(other.poll())

    def test_closed_question_missing_proof_keeps_stop(self):
        child = subprocess.Popen([sys.executable, '-c', 'pass'])
        owner = {'pid': child.pid, 'pid_inicio': sessions.process_start(child.pid)}
        child.wait(timeout=3)
        private.private_write(self.op / 'preguntas-slots/uno.json',
                              dict(owner, estado='cerrada', vence=time.time() - 10,
                                   base=str(self.base), ensayo_sha256=self.tag))
        with patch.object(sessions, 'indexed_rows', return_value=[]):
            result = trial.stop(self.op)
        self.assertEqual(result['estado'], 'bloqueado')
        self.assertEqual(result['custodias_sin_cierre'], 1)

    def test_stop_missing_inventory_never_claims_stopped(self):
        (self.path / "procesos.json").unlink()
        with patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial, 'terminate') as terminate:
            with self.assertRaisesRegex(ValueError, 'inventario_incompleto'):
                trial.stop(self.op)
            terminate.assert_not_called()
        self.assertTrue((self.path / 'STOP').exists())
        self.assertFalse((self.path / 'fin.json').exists())

    def test_stop_tampered_state_receipt_sends_no_signal(self):
        journal = {'politica_sha256': self.tag, 'procesos': []}
        private.private_write(self.path / 'procesos.json', journal)
        state = write_state(self.op, self.value, procesos_sha256=trial.digest(journal))
        private.private_write(self.path / state['recibo']['archivo'], {'alterado': True})
        with patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial, 'terminate') as terminate:
            with self.assertRaisesRegex(ValueError, 'estado_alterado'):
                trial.stop(self.op)
            terminate.assert_not_called()

    def test_admission_missing_or_altered_inventory_blocks(self):
        p = self.path / 'procesos.json'
        p.unlink()
        with self.assertRaises(OSError):
            self.capacity([])
        private.private_write(p, {'politica_sha256': self.tag, 'procesos': [{'pid': 0}]})
        with self.assertRaisesRegex(ValueError, 'inventario_alterado'):
            self.capacity([])

    def test_stop_both_documents_lost_after_sample_blocks(self):
        (self.path / 'procesos.json').unlink()
        (self.path / 'estado.json').unlink()
        with patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial, 'terminate') as terminate:
            with self.assertRaisesRegex(ValueError, 'inventario_perdido'):
                trial.stop(self.op)
            terminate.assert_not_called()
        self.assertTrue((self.path / 'STOP').exists())
        self.assertFalse((self.path / 'fin.json').exists())

    def test_monitor_registry_wait_is_bounded(self):
        with patch.object(sessions, 'registry_lock', side_effect=ValueError('Registro ocupado')) as lock, \
                patch.object(trial.time, 'monotonic', side_effect=[0, 0, 6]), \
                patch.object(trial.time, 'sleep'):
            with self.assertRaisesRegex(ValueError, 'registro_ocupado_o_vencido'):
                with trial.monitor_registry(self.op, time.time() + 30):
                    self.fail('No debe entrar al lock ocupado')
            lock.assert_called_once_with(self.op, nonblocking=True)

    def test_stop_busy_registry_writes_stop_without_waiting(self):
        with patch.object(sessions, 'registry_lock', side_effect=ValueError('Registro ocupado')) as lock, \
                patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial, 'terminate', return_value=([], [])):
            self.assertEqual(trial.stop(self.op)['estado'], 'parado')
            lock.assert_not_called()
        self.assertTrue((self.path / 'STOP').exists())


    def test_expired_question_without_identity_never_frees_capacity(self):
        private.private_write(self.op / 'preguntas-slots/tres.json',
                              {'estado': 'respondiendo', 'vence': time.time() - 1})
        with self.assertRaisesRegex(ValueError, 'vencido sin identidad'):
            self.capacity(self.rows(3))

    def test_stop_corrupt_inventory_sends_no_signal(self):
        private.private_write(self.path / 'procesos.json', {'politica_sha256': self.tag, 'procesos': [{'pid': 0}]})
        with patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial, 'terminate') as terminate:
            with self.assertRaisesRegex(ValueError, 'inventario_alterado'):
                trial.stop(self.op)
            terminate.assert_not_called()
        self.assertTrue((self.path / 'STOP').exists())

    def test_invalid_question_slot_blocks_globally(self):
        for slot in [[], {'estado': 'respondiendo', 'vence': float('nan')},
                     {'estado': 'respondiendo', 'vence': time.time() + 10, 'pid': True}]:
            private.private_write(self.op / 'preguntas-slots/invalida.json', slot)
            with self.subTest(slot=slot), self.assertRaises(ValueError):
                self.capacity([])

    def test_freshness_exact_boundaries(self):
        trial.fresh(100, 15, 115)
        trial.fresh(100, 60, 160)
        for timestamp, ttl, now in [(100, 15, 115.001), (100, 60, 160.001), (101, 15, 100)]:
            with self.assertRaises(ValueError):
                trial.fresh(timestamp, ttl, now)

    def test_resource_sampler_uses_cpu_and_swap_differences(self):
        memory = {'MemTotal': 1000, 'MemAvailable': 800, 'SwapTotal': 100, 'SwapFree': 90}
        pressure = {'cpu': 1.0, 'memory': 2.0, 'io': 3.0}
        before = ([10, 0, 10, 70, 10, 0, 0, 0], memory, 10, pressure)
        after = ([20, 0, 20, 140, 20, 0, 0, 0], memory, 15, pressure)
        with patch.object(trial, 'counters', side_effect=[before, after]), \
                patch.object(trial.time, 'monotonic', side_effect=[10, 11]), \
                patch.object(trial.time, 'sleep'):
            sample = trial.read_resources()
        self.assertAlmostEqual(sample['cpu'], 20)
        self.assertEqual(sample['ram_disponible'], 80)
        self.assertAlmostEqual(sample['swap_usado'], 10)
        self.assertEqual(sample['swap_paginas_s'], 5)
        trial.resources(sample, time.time())

    def fake_app_server(self):
        fake = self.root / 'codex'
        fake.write_text('#!' + sys.executable + '\n' + '''import json, sys, time
for line in sys.stdin:
    request = json.loads(line)
    method = request['method']
    assert method in {'initialize', 'initialized', 'account/rateLimits/read'}
    if method == 'initialize':
        result = {}
    elif method == 'initialized':
        continue
    else:
        windows = {name: {'usedPercent': 10, 'windowDurationMins': 300,
                          'resetsAt': int(time.time()) + 3600} for name in ('primary', 'secondary')}
        result = {'rateLimitsByLimitId': {'codex': windows}}
    print(json.dumps({'id': request['id'], 'result': result}), flush=True)
''')
        fake.chmod(0o700)
        return fake

    def test_primary_only_rpc_and_window_changes(self):
        fake = self.fake_app_server()
        fake.write_text(fake.read_text().replace("result = {'rateLimitsByLimitId': {'codex': windows}}",
                        "windows['secondary'] = None; result = {'rateLimitsByLimitId': {'codex': windows}}"))
        with patch.dict(os.environ, {'PATH': str(self.root) + ':' + os.environ['PATH']}):
            sample = trial.read_quota()
        self.assertEqual(set(sample['ventanas']), {'primary'})
        trial.quota_budget(sample, sample, time.time())
        changed = deepcopy(sample)
        changed['ventanas']['primary']['usedPercent'] += 2
        with self.assertRaisesRegex(ValueError, 'presupuesto'):
            trial.quota_budget(sample, changed, time.time())
        changed = deepcopy(sample)
        changed['ventanas']['secondary'] = deepcopy(changed['ventanas']['primary'])
        for initial, current in [(sample, changed), (changed, sample)]:
            with self.assertRaisesRegex(ValueError, 'ventana_cambiada'):
                trial.quota_budget(initial, current, time.time())

    def test_quota_response_rejects_missing_or_malformed_primary(self):
        now = time.time()
        primary = quota_sample(now)['ventanas']['primary']
        for limits in [{}, {'primary': None}, {'primary': primary, 'secondary': {}},
                       {'primary': primary, 'secondary': False}]:
            with self.subTest(limits=limits), self.assertRaises(ValueError):
                trial.quota_response({'rateLimits': limits}, now)
        for limits in [{'primary': primary}, {'primary': primary, 'secondary': None}]:
            self.assertEqual(set(trial.quota_response({'rateLimits': limits}, now)['ventanas']), {'primary'})

    def test_quota_rpc_readonly_with_synthetic_app_server(self):
        self.fake_app_server()
        with patch.dict(os.environ, {'PATH': str(self.root) + ':' + os.environ['PATH']}):
            sample = trial.read_quota()
        self.assertEqual(sample['ventanas']['primary']['usedPercent'], 10)
        trial.quota(sample, time.time())

    def test_quota_reader_drains_detached_helper_in_preflight_and_monitor(self):
        fake = self.fake_app_server()
        launcher = """import os
from pathlib import Path
aux = Path(os.environ['TEST_QUOTA_AUX'])
if os.fork() == 0:
    os.setsid()
    if os.fork() == 0:
        aux.write_text(json.dumps({
            'pid': os.getpid(),
            'start': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
        }))
        time.sleep(10)
    os._exit(0)
while not aux.exists():
    time.sleep(0.01)
"""
        fake.write_text(fake.read_text().replace('for line in sys.stdin:', launcher + 'for line in sys.stdin:'))
        unrelated = self.child()
        for name, stop_path in [('preflight', None), ('monitor', self.path / 'STOP')]:
            with self.subTest(lectura=name):
                observed = self.root / (name + '.json')
                with patch.dict(os.environ, {'PATH': str(self.root) + ':' + os.environ['PATH'],
                                             'TEST_QUOTA_AUX': str(observed)}):
                    self.assertEqual(trial.read_quota(stop_path=stop_path)['ventanas']['primary']['usedPercent'], 10)
                aux = json.loads(observed.read_text())
                boot = sessions.process_start(os.getpid()).rsplit(':', 1)[0]
                self.assertNotEqual(sessions.process_start(aux['pid']), boot + ':' + aux['start'])
        proofs = list(self.path.glob('custodia-*.json'))
        self.assertEqual(len(proofs), 1)
        record = trial.read(proofs[0])
        proof = trial.read_receipt(self.path, record['recibo'])
        self.assertEqual(proof['evento'], 'custodia_echild')
        self.assertEqual(trial.pending_custodies(self.op, self.value, []), [])
        self.assertIsNone(unrelated.poll())

    def test_foreground_monitor_cli_sigterm_and_private_output(self):
        self.fake_app_server()
        # Las ventanas sintéticas deben conservar el mismo reset en todos los RPC.
        fake = self.root / 'codex'
        source = fake.read_text().replace("int(time.time()) + 3600",
                                          str(self.value['cuota_inicial']['ventanas']['primary']['resetsAt']))
        fake.write_text(source)
        for window in self.value['cuota_inicial']['ventanas'].values():
            window['windowDurationMins'] = 300
        private.private_write(self.path / 'politica.json', self.value)
        private.private_write(self.path / 'preparacion.json', {'politica_sha256': trial.digest(self.value)})
        (self.path / 'estado.json').unlink()
        (self.path / 'procesos.json').unlink()
        for receipt in self.path.glob('recibo-*.json'):
            receipt.unlink()
        wrapper = self.root / 'monitor_fixture.py'
        sample = resource_sample()
        sample.pop('fecha')
        wrapper.write_text('import sys, time\nsys.path.insert(0, ' + repr(str(Path(trial.__file__).parent))
                           + ')\nimport harness_ensayo as trial\ntrial.read_resources = lambda: dict('
                           + repr(sample) + ', fecha=time.time())\nsys.exit(trial.main())\n')
        environment = dict(os.environ, PATH=str(self.root) + ':' + os.environ['PATH'])
        process = subprocess.Popen([sys.executable, '-B', str(wrapper), '--operacion', str(self.op), 'monitor'],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=environment)
        def cleanup():
            if process.poll() is None:
                process.terminate()
            process.communicate(timeout=7)
        self.addCleanup(cleanup)
        deadline = time.monotonic() + 5
        while not (self.path / 'estado.json').exists() and process.poll() is None:
            self.assertLess(time.monotonic(), deadline)
            time.sleep(0.02)
        trial.health(self.op, self.value)
        identity = {'pid': process.pid, 'pid_inicio': sessions.process_start(process.pid)}
        trial.terminate([identity])
        output, errors = process.communicate(timeout=7)
        self.assertEqual(process.returncode, 0, errors)
        self.assertEqual(json.loads(output)['estado'], 'parado')
        self.assertNotIn('ventanas', output)
        self.assertNotIn(str(self.base), output)
        self.assertTrue((self.path / 'STOP').exists())

    def test_cli_invalid_symlink_is_blocked_without_private_path(self):
        link = self.root / 'link'
        link.symlink_to(self.op)
        output = io.StringIO()
        with patch.object(sys, 'argv', ['harness_ensayo.py', '--operacion', str(link), 'estado']), \
                redirect_stdout(output):
            self.assertEqual(trial.main(), 2)
        self.assertEqual(json.loads(output.getvalue())['estado'], 'bloqueado')
        self.assertNotIn(str(self.op), output.getvalue())

    def test_stop_with_live_reserved_question_reports_blocked(self):
        journal = {'politica_sha256': self.tag, 'procesos': []}
        private.private_write(self.path / 'procesos.json', journal)
        write_state(self.op, self.value, procesos_sha256=trial.digest(journal))
        slot = {'supervisor_pid': os.getpid(), 'supervisor_inicio': sessions.process_start(os.getpid())}
        with patch.object(trial, 'inventory', return_value=([], [], [slot])), \
                patch.object(trial.time, 'monotonic', side_effect=[0, 6]):
            result = trial.stop(self.op)
        self.assertEqual(result['estado'], 'bloqueado')
        self.assertEqual(result['reservas_pendientes'], 1)

    def test_prepare_fresh_read_and_no_overwrite_or_activation(self):
        root = self.root / 'nuevo'
        with patch.object(trial, 'read_quota', return_value=quota_sample()) as quota_reader, \
                patch.object(trial, 'read_resources', return_value=resource_sample()), \
                patch.object(sessions, 'indexed_rows', return_value=[]):
            result = trial.prepare(root, self.base, self.ids, 1800)
            self.assertEqual(result['estado'], 'preparado')
            quota_reader.assert_called_once()
            self.assertFalse((root / trial.DIRECTORY / 'estado.json').exists())
            with self.assertRaisesRegex(ValueError, 'lote_existente'):
                trial.prepare(root, self.base, self.ids, 1800)
            with self.assertRaises(OSError):
                sessions.check_capacity([], 'cuatro', self.base, ['ruta'], 'ejecutor', root=root)
        for duration in [0, 1801, True]:
            with self.assertRaises(ValueError):
                trial.prepare(self.root / 'invalido', self.base, self.ids, duration)

    def test_monitor_never_restarts_after_lost_state(self):
        journal = (self.path / 'procesos.json').read_bytes()
        (self.path / 'estado.json').unlink()
        with patch.object(trial, 'read_quota') as rpc:
            with self.assertRaisesRegex(ValueError, 'monitor_ya_iniciado'):
                trial.monitor(self.op)
            rpc.assert_not_called()
        self.assertEqual((self.path / 'procesos.json').read_bytes(), journal)
        (self.path / 'procesos.json').unlink()
        with patch.object(trial, 'read_quota') as rpc:
            with self.assertRaisesRegex(ValueError, 'monitor_ya_iniciado'):
                trial.monitor(self.op)
            rpc.assert_not_called()
        self.assertFalse((self.path / 'estado.json').exists())

    def check_monitor_tampering(self, document):
        (self.path / 'estado.json').unlink()
        (self.path / 'procesos.json').unlink()
        for receipt in self.path.glob('recibo-*.json'):
            receipt.unlink()
        reads = []
        targets = []
        tampered = {'politica_sha256': self.tag, 'procesos': [], 'alterado': True}
        def quota_reader(*args):
            reads.append(1)
            if len(reads) == 2:
                target = self.path / document
                if document == 'recibo':
                    state = private.private_read(self.path / 'estado.json')
                    target = self.path / state['recibo']['archivo']
                targets.append(target)
                private.private_write(target, tampered)
            if len(reads) > 2:
                raise AssertionError('El monitor no bloqueo la alteracion')
            return deepcopy(self.value['cuota_inicial'])
        with patch.object(trial, 'read_quota', side_effect=quota_reader), \
                patch.object(trial, 'read_resources', side_effect=lambda: resource_sample()), \
                patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial.time, 'sleep'):
            with self.assertRaises(ValueError):
                trial.monitor(self.op)
        self.assertEqual(private.private_read(targets[0]), tampered)
        self.assertTrue((self.path / 'STOP').exists())
        self.assertEqual(len(reads), 2)

    def test_monitor_does_not_heal_tampered_inventory(self):
        self.check_monitor_tampering('procesos.json')

    def test_monitor_does_not_heal_tampered_state(self):
        self.check_monitor_tampering('estado.json')

    def test_monitor_does_not_heal_tampered_receipt(self):
        self.check_monitor_tampering('recibo')

    def test_monitor_error_sets_stop_without_enabling_fourth(self):
        (self.path / 'estado.json').unlink()
        (self.path / 'procesos.json').unlink()
        for receipt in self.path.glob('recibo-*.json'):
            receipt.unlink()
        with patch.object(trial, 'read_quota', side_effect=ValueError('cuota_desconocida')), \
                patch.object(trial, 'inventory', return_value=([], [], [])):
            self.assertEqual(trial.monitor(self.op)['estado'], 'parado')
        self.assertTrue((self.path / 'STOP').exists())
        with self.assertRaisesRegex(ValueError, 'STOP'):
            self.capacity([])

    def test_monitor_publishes_receipts_and_stops_at_budget(self):
        (self.path / 'estado.json').unlink()
        (self.path / 'procesos.json').unlink()
        for receipt in self.path.glob('recibo-*.json'):
            receipt.unlink()
        exceeded = deepcopy(self.value['cuota_inicial'])
        exceeded['ventanas']['primary']['usedPercent'] += 2
        def wait(_):
            if (self.path / 'estado.json').exists():
                self.assertEqual(self.capacity([]), self.tag)
        with patch.object(trial, 'read_quota', side_effect=[deepcopy(self.value['cuota_inicial']), exceeded]), \
                patch.object(trial, 'read_resources', side_effect=lambda: resource_sample()), \
                patch.object(trial, 'inventory', return_value=([], [], [])), \
                patch.object(trial.time, 'sleep', side_effect=wait):
            self.assertEqual(trial.monitor(self.op)['estado'], 'parado')
        self.assertTrue(list(self.path.glob('recibo-*.json')))
        self.assertTrue((self.path / 'STOP').exists())


class WorkerExpiryTests(unittest.TestCase):
    def test_expiry_after_git_or_before_gate_never_executes_codex(self):
        for fail_at in [2, 3]:
            with self.subTest(check=fail_at), ExitStack() as stack:
                session = {'intento': 1, 'dry_run': False, 'estado': 'iniciando',
                           'supervisor_pid': os.getpid(), 'ensayo_sha256': 'permiso',
                           'git_repo': '/virtual/git', 'briefing': '/virtual/briefing',
                           'log': '/virtual/log', 'worktree': '/virtual/worktree'}
                writes = []
                class Gate(io.BytesIO):
                    def write(self, data):
                        writes.append(data)
                        return super().write(data)
                def mock(obj, name, **kwargs):
                    return stack.enter_context(patch.object(obj, name, **kwargs))
                mock(sessions, 'registry_lock', side_effect=lambda *_: nullcontext())
                mock(sessions.trabajo, 'read_task', return_value={'sesiones': [session]})
                mock(trial, 'revalidate', side_effect=[None] * (fail_at - 1) + [ValueError('ensayo_vencido')])
                mock(sessions, 'validate_private_git')
                mock(sessions.shutil, 'which', return_value='/fake/codex')
                mock(Path, 'open', side_effect=lambda *a, **k: io.BytesIO())
                mock(sessions.os, 'pipe', return_value=(101, 102))
                mock(sessions.os, 'fdopen', side_effect=lambda *a, **k: Gate())
                mock(sessions.os, 'close')
                spawn = mock(sessions.subprocess, 'Popen')
                spawn.return_value.pid = 12345
                spawn.return_value.wait.return_value = 125
                mock(sessions, 'command', return_value=['/fake/codex'])
                mock(sessions, 'child_environment', return_value={})
                update = mock(sessions, 'session_update')
                mock(sessions, 'process_start', return_value='boot:123')
                self.assertEqual(sessions._worker(Path('/base'), 'uno', Path('/virtual/op'), 1), 126)
                self.assertEqual(writes, [])
                self.assertEqual(update.call_args.kwargs['estado'], 'fallida')
                if fail_at == 2:
                    spawn.assert_not_called()
                else:
                    spawn.assert_called_once()
                    spawn.return_value.wait.assert_called_once_with(timeout=5)


if __name__ == '__main__':
    unittest.main()

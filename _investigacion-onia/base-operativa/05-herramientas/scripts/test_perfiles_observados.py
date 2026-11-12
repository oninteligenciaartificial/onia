"""Fixtures exclusivamente sintéticos; nunca acceden a registros del operador."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

import perfiles_observados as p

ROOT = '11111111-1111-4111-8111-111111111111'
CHILD = '22222222-2222-4222-8222-222222222222'
OTHER = '33333333-3333-4333-8333-333333333333'
TURN = '44444444-4444-4444-8444-444444444444'
TURN2 = '55555555-5555-4555-8555-555555555555'


def event(kind, **payload):
    return dict(type=kind, payload=payload)


def meta(sid=ROOT, parent=None):
    return event('session_meta', id=sid, parent_thread_id=parent, agent_path='root/worker')


def context(turn=TURN, **extra):
    return event('turn_context', turn_id=turn, model='gpt-6.1-sol', effort='high', **extra)


def usage(sid=ROOT, turn=TURN):
    return event('token_usage_record', thread_id=sid, turn_id=turn)


class PerfilesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, records):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(''.join(json.dumps(r) + '\n' for r in records), encoding='utf-8')
        return path

    def rows(self):
        return p.observar(self.root, [ROOT])

    def test_confirmed_own_turn_and_read_only(self):
        path = self.write('a.jsonl', [meta(), context(), usage()])
        before = path.read_bytes(), path.stat().st_mtime_ns
        self.assertEqual(self.rows(), [dict(thread_id=ROOT, parent_thread_id=None,
            model='gpt-6.1-sol', effort='high', alcance='uso_confirmado')])
        self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), before)

    def test_usage_requires_both_identifiers(self):
        self.write('a.jsonl', [meta(), context(), usage(OTHER), usage(turn=TURN2)])
        self.assertEqual(self.rows()[0]['alcance'], 'contexto_no_confirmado')

    def test_child_inherited_context_excluded(self):
        self.write('a.jsonl', [meta(), context(), usage()])
        self.write('nested/b.jsonl', [meta(CHILD, ROOT), context(), usage(ROOT),
            context(TURN2, thread_id=CHILD), usage(CHILD, TURN2)])
        rows = self.rows()
        child = [row for row in rows if row['thread_id'] == CHILD]
        self.assertEqual(len(child), 1)
        self.assertEqual(child[0]['alcance'], 'uso_confirmado')
        self.assertEqual(child[0]['parent_thread_id'], ROOT)

    def test_no_usage_child_is_not_observed(self):
        self.write('a.jsonl', [meta(CHILD, ROOT), context()])
        self.assertEqual({r['alcance'] for r in self.rows()}, {'no_observado'})

    def test_explicit_child_context_without_usage(self):
        self.write('a.jsonl', [meta(CHILD, ROOT), context(thread_id=CHILD)])
        self.assertEqual(self.rows()[1]['alcance'], 'contexto_no_confirmado')

    def test_foreign_sid_and_agent_path_are_excluded(self):
        self.write('a.jsonl', [meta(), context(thread_id=OTHER),
            context(agent_path='/private/other'), usage()])
        self.assertEqual(self.rows()[0]['alcance'], 'no_observado')

    def test_transitive_descendants_multiple_parents_unrelated_excluded(self):
        self.write('a.jsonl', [meta(CHILD, ROOT)])
        self.write('b.jsonl', [meta(OTHER, CHILD)])
        self.write('c.jsonl', [meta(TURN)])
        self.assertEqual({r['thread_id'] for r in self.rows()}, {ROOT, CHILD, OTHER})
        self.assertEqual(len(p.observar(self.root, [ROOT, TURN])), 4)

    def test_wrapped_usage_and_multiple_profiles(self):
        wrapped = event('event_msg', type='token_usage_record', thread_id=ROOT, turn_id=TURN)
        second = event('turn_context', turn_id=TURN2, thread_id=ROOT,
                       model='gpt-6.1-luna', reasoning_effort='low')
        self.write('a.jsonl', [meta(), context(), wrapped, second])
        self.assertEqual({r['alcance'] for r in self.rows()},
                         {'uso_confirmado', 'contexto_no_confirmado'})

    def test_missing_records_empty_and_unknown_sid(self):
        self.write('empty.jsonl', [])
        self.write('unknown.jsonl', [context(), usage()])
        self.assertEqual(self.rows()[0]['alcance'], 'no_observado')

    def test_sanitized_output(self):
        secret = '/private/SECRET token sk-private'
        self.write('private-name.jsonl', [meta(), event('response_item', prompt=secret),
            event('turn_context', turn_id=TURN, model=secret, effort=secret), usage()])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(p.main([str(self.root), ROOT]), 0)
        self.assertNotIn(secret, out.getvalue())
        self.assertNotIn(str(self.root), out.getvalue())
        self.assertEqual(set(json.loads(out.getvalue())[0]),
                         {'thread_id', 'parent_thread_id', 'model', 'effort', 'alcance'})

    def test_malformed_json_and_errors_do_not_leak(self):
        (self.root / 'bad.jsonl').write_text('SECRET not json')
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            self.assertEqual(p.main([str(self.root), ROOT]), 2)
        self.assertEqual(out.getvalue(), '')
        self.assertNotIn('SECRET', err.getvalue())
        self.assertNotIn(str(self.root), err.getvalue())

    def test_metadata_conflict_rejected(self):
        self.write('a.jsonl', [meta(), meta(CHILD)])
        with self.assertRaises(p.ErrorLectura):
            self.rows()

    def test_duplicate_rollouts_deduplicate(self):
        for name in ('a.jsonl', 'b.jsonl'):
            self.write(name, [meta(), context(), usage()])
        self.assertEqual(len(self.rows()), 1)

    def test_symlinks_ignored(self):
        self.write('fixture.txt', [meta(), context(), usage()])
        (self.root / 'linked.jsonl').symlink_to(self.root / 'fixture.txt')
        (self.root / 'loop').symlink_to(self.root, target_is_directory=True)
        self.assertEqual(self.rows()[0]['alcance'], 'no_observado')

    def test_nested_spawn_metadata(self):
        nested = event('session_meta', id=CHILD, source={'subagent': {'thread_spawn': {
            'parent_thread_id': ROOT, 'agent_path': 'root/worker'}}})
        self.write('nested.jsonl', [nested, context(), usage(CHILD)])
        self.assertEqual(self.rows()[1]['parent_thread_id'], ROOT)
        self.assertEqual(self.rows()[1]['alcance'], 'uso_confirmado')

    def test_invalid_parent_rejected(self):
        self.write('bad.jsonl', [meta(CHILD, '/private/SECRET')])
        with self.assertRaises(p.ErrorLectura):
            self.rows()

    def test_argument_error_is_fixed(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), self.assertRaises(SystemExit):
            p.main(['--SECRET'])
        self.assertNotIn('SECRET', err.getvalue())

    def test_invalid_sid_and_directory(self):
        for directory, sids in ((self.root, ['SECRET']), (self.root / 'absent', [ROOT])):
            with self.assertRaises(p.ErrorLectura):
                p.observar(directory, sids)


if __name__ == '__main__':
    unittest.main()

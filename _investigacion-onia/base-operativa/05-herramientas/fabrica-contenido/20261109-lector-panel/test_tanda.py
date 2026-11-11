import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import tanda
import panel

SOURCE = tanda.lector.BASE/'05-herramientas/fabrica-onia/1-guiones-calendario/salida/guiones-tanda-20261111-v2/guiones-panel.json'


class TandaTests(unittest.TestCase):
    def test_five_drafts_visible_without_claiming_approval(self):
        data = tanda.snapshot(SOURCE)
        self.assertEqual(len(data['guiones']), 5)
        self.assertTrue(all(g['revision_tecnica'] is None for g in data['guiones']))
        html = panel.render(data)
        self.assertIn('5 borradores para revisar', html)
        self.assertIn('Revisión técnica pendiente', html)
        self.assertNotIn('Técnicamente revisado', html)
        self.assertIn('Claude de 0 a 100', html)

    def test_changed_bytes_rejected_without_modifying_source(self):
        original = Path.read_bytes
        def read(path):
            value = original(path)
            return value + b'alterado' if path.name == 'T01.md' else value
        with patch.object(Path, 'read_bytes', read):
            with self.assertRaisesRegex(ValueError, 'difiere'):
                tanda.snapshot(SOURCE)

    def test_untracked_inputs_not_attributed_to_head(self):
        run = tanda.subprocess.run
        def result(command, *args, **kwargs):
            if 'ls-files' in command:
                return tanda.subprocess.CompletedProcess(command, 1)
            return run(command, *args, **kwargs)
        with patch.object(tanda.subprocess, 'run', side_effect=result):
            data = tanda.snapshot(SOURCE)
        self.assertTrue(data['commit_entradas_repo'].startswith('Paquete local sin anclar'))


if __name__ == '__main__':
    unittest.main()

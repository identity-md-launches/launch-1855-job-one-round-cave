"""Regression checks; fixtures stay beside this file and are removed afterwards."""
import contextlib
import io
from pathlib import Path
import random
import tempfile
import unittest

import import_map


class MapperTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def put(self, path, source):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source, encoding='utf-8')

    def test_package_collision_reports_both_paths_and_package_precedence(self):
        self.put('pkg.py', 'import shadow_only\nraise RuntimeError("must not execute")\n')
        self.put('pkg/__init__.py', 'from . import engine\n')
        self.put('pkg/engine.py', 'raise RuntimeError("must not execute")\n')
        self.put('main.py', 'import pkg\n')
        report = import_map.inspect(self.root)
        collision, = report['issues']
        self.assertEqual(collision['type'], 'module_collision')
        self.assertEqual(collision['paths'], ['pkg.py', 'pkg/__init__.py'])
        self.assertEqual(collision['selected'], 'pkg/__init__.py')
        self.assertEqual(next(m['path'] for m in report['modules'] if m['module'] == 'pkg'),
                         'pkg/__init__.py')
        self.assertEqual(report['edges'], [{'from': 'main', 'to': 'pkg'},
                                           {'from': 'pkg', 'to': 'pkg.engine'}])
        self.assertIn('shadowed source not analyzed: pkg.py', import_map.format_text(report))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(import_map.main([str(self.root), '--strict', '--json']), 1)
        self.assertEqual(report, import_map.inspect(self.root))

    def test_nested_collision(self):
        self.put('outer/item.py', '')
        self.put('outer/item/__init__.py', '')
        report = import_map.inspect(self.root)
        self.assertEqual(report['issues'][0]['module'], 'outer.item')
        self.assertEqual(report['issues'][0]['selected'], 'outer/item/__init__.py')

    def test_original_example_and_no_execution(self):
        report = import_map.inspect(Path(__file__).parent / 'examples')
        self.assertEqual(report['summary'], {'module_count': 4, 'local_edge_count': 3,
                         'cycle_count': 1, 'issue_count': 1, 'entrypoints': ['main']})
        self.assertEqual(report['cycles'], [['pkg.engine', 'pkg.helper']])
        self.put('trap.py', 'raise RuntimeError("source executed")\nif __name__ == "__main__": pass\n')
        self.assertEqual(import_map.inspect(self.root)['summary']['entrypoints'], ['trap'])

    def test_deep_graph(self):
        nodes = [f'n{i:05}' for i in range(5000)]
        graph = {node: {nodes[i + 1]} if i + 1 < len(nodes) else set()
                 for i, node in enumerate(nodes)}
        self.assertEqual(import_map.cycles(graph), [])
        graph[nodes[-1]].add(nodes[0])
        self.assertEqual(import_map.cycles(graph), [nodes])

    def test_cycles_against_independent_reachability(self):
        rng = random.Random(22)
        for _ in range(100):
            nodes = list('abcdefgh')
            graph = {n: {m for m in nodes if rng.random() < .18} for n in nodes}
            reach = {}
            for node in nodes:
                seen, pending = set(), list(graph[node])
                while pending:
                    target = pending.pop()
                    if target not in seen:
                        seen.add(target)
                        pending.extend(graph[target])
                reach[node] = seen
            expected = set()
            for n in nodes:
                group = tuple(m for m in nodes if m in reach[n] and n in reach[m])
                if len(group) > 1 or n in graph[n]:
                    expected.add(group)
            self.assertEqual(import_map.cycles(graph), sorted(map(list, expected)))

    def test_parse_error_and_self_cycle(self):
        self.put('broken.py', 'def nope(\n')
        self.put('loop.py', 'import loop\n')
        report = import_map.inspect(self.root)
        self.assertEqual(report['cycles'], [['loop']])
        self.assertEqual(report['issues'][0]['type'], 'parse_error')


if __name__ == '__main__':
    unittest.main()

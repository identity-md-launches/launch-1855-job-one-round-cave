"""Offline checks. The bundled observation is real; adversarial edits are synthetic."""
import contextlib
import copy
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import token_read_plan as tool


class TokenReadPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = Path(__file__).resolve().parent
        cls.plan = tool.read_json(base / 'observed-plan.json')
        cls.responses = tool.read_json(base / 'observed-responses.json')

    def test_only_pinned_read_calls_and_real_destinations(self):
        requests = self.plan['requests']
        self.assertEqual([r['method'] for r in requests], ['eth_call'] * 6)
        self.assertEqual([r['params'][0]['data'] for r in requests[:3]],
                         ['0x95d89b41', '0x313ce567', '0x18160ddd'])
        self.assertEqual(requests[0]['params'][0]['to'], tool.TOKENS[0][1])
        self.assertEqual(requests[3]['params'][0]['to'], tool.TOKENS[1][1])
        for request in requests:
            self.assertEqual(request['params'][1], '0x18fc1e6')
        for block in ['latest', 'safe', '0X123', '0x001', '0x', 123, True]:
            with self.subTest(block=block), self.assertRaises(ValueError):
                tool.make_plan(block)

    def test_real_ethereum_observation(self):
        rows = tool.decode_rows(self.plan, self.responses)
        self.assertEqual(len(rows), 6)
        self.assertEqual([r['raw_value'] for r in rows], [
            'ZTO', '18', '1000000000000000000000000000',
            'IMD', '18', '4164418598629000000000000'])
        self.assertEqual(rows[2]['display_value'], '1000000000')
        self.assertEqual(rows[5]['display_value'], '4164418.598629')

    def test_batch_order_is_irrelevant(self):
        self.assertEqual(tool.decode_rows(self.plan, self.responses),
                         tool.decode_rows(self.plan, list(reversed(self.responses))))

    def test_mutated_plan_rejected(self):
        for path, value in [('chain_id', True), ('schema', 'unknown')]:
            bad = copy.deepcopy(self.plan)
            bad[path] = value
            with self.subTest(path=path), self.assertRaises(ValueError):
                tool.decode_rows(bad, self.responses)
        bad = copy.deepcopy(self.plan)
        bad['requests'][0]['method'] = 'eth_sendRawTransaction'
        with self.assertRaises(ValueError):
            tool.decode_rows(bad, self.responses)

    def test_incomplete_and_malformed_batches_rejected(self):
        bad_batches = [None, {}, [], self.responses[:-1]]
        changes = [('id', True), ('id', 7), ('id', 2), ('jsonrpc', '1.0'),
                   ('result', None), ('result', '0x0'), ('result', '0xgg'),
                   ('result', '0x' + '00' * 4097)]
        for key, value in changes:
            batch = copy.deepcopy(self.responses)
            batch[0][key] = value
            bad_batches.append(batch)
        batch = copy.deepcopy(self.responses)
        batch[0] = {'jsonrpc': '2.0', 'id': 1, 'error': {'code': -32000}}
        bad_batches.append(batch)
        for batch in bad_batches:
            with self.subTest(batch=str(batch)[:100]), self.assertRaises(ValueError):
                tool.decode_rows(self.plan, batch)

    def test_noncanonical_return_bytes_rejected(self):
        for index in (0, 1, 2):
            batch = copy.deepcopy(self.responses)
            batch[index]['result'] += '00' * 32
            with self.subTest(index=index), self.assertRaises(ValueError):
                tool.decode_rows(self.plan, batch)
        batch = copy.deepcopy(self.responses)
        batch[1]['result'] = '0x' + tool.abi.word(256).hex()
        with self.assertRaises(ValueError):
            tool.decode_rows(self.plan, batch)

    def test_no_rounding_or_exponent_notation(self):
        self.assertEqual(tool.exact_units(10**27 + 1, 18), '1000000000.000000000000000001')
        self.assertEqual(tool.exact_units(1, 255), '0.' + '0' * 254 + '1')
        self.assertEqual(tool.exact_units(0, 18), '0')
        self.assertEqual(tool.exact_units(123, 0), '123')
        for raw, decimals in [(True, 18), (1, True), (-1, 18), (1, 256)]:
            with self.assertRaises(ValueError):
                tool.exact_units(raw, decimals)

    def test_json_limits_duplicate_keys_and_cli_error(self):
        scratch = Path('test/scratch/token-read-plan')
        scratch.mkdir(parents=True, exist_ok=True)
        path = scratch / 'bad.json'
        for text in ['{"id":1,"id":2}', '[NaN]', ' ' * (tool.MAX_BYTES + 1)]:
            path.write_text(text, encoding='utf-8')
            with self.assertRaises(ValueError):
                tool.read_json(path)
        path.write_text('{}', encoding='utf-8')
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = tool.main(['decode', '--plan', str(path), '--responses', str(path)])
        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), '')
        self.assertIn('error', json.loads(stderr.getvalue()))

    def test_demo_emits_complete_csv(self):
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            result = tool.main(['demo'])
        self.assertEqual(result, 0)
        self.assertEqual(len(stdout.getvalue().splitlines()), 7)
        self.assertIn('4164418.598629', stdout.getvalue())

    def test_input_containment_including_symlink(self):
        # Both sides stay in the real workspace. A narrower mocked working root
        # lets us test rejection without reading or targeting outside it.
        scratch = Path('test/scratch/token-read-plan').resolve()
        isolated = scratch / 'isolated'
        isolated.mkdir(parents=True, exist_ok=True)
        outside = scratch / 'outside-isolated.json'
        outside.write_text('{}', encoding='utf-8')
        inside = isolated / 'inside.json'
        inside.write_text('{}', encoding='utf-8')
        link = isolated / 'link.json'
        link.unlink(missing_ok=True)
        link.symlink_to(outside)
        with patch.object(tool.Path, 'cwd', return_value=isolated):
            self.assertEqual(tool.read_json(inside), {})
            for path in (outside, link):
                with self.subTest(path=path.name), self.assertRaises(ValueError):
                    tool.read_json(path)


if __name__ == '__main__':
    unittest.main()

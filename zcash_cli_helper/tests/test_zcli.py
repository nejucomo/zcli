import unittest
from pathlib2 import Path
from decimal import Decimal
from genty import genty, genty_dataset
from mock import call, patch
from zcash_cli_helper.zcli import ZCLI


@genty
class ZCLI_tests (unittest.TestCase):
    def setUp(self):
        with patch('logging.getLogger'):
            self.cli = ZCLI(Path('FAKE-DATADIR'))
        self.m_log = self.cli._log

    call_rpc_argsets = dict(
        nothing=(
            [],
            [],
        ),
        strs=(
            ['a', 'b', 'c'],
            ['a', 'b', 'c'],
        ),
        jsonstuff=(
            [u'a', ['b', {'c': 'coconut'}]],
            ['"a"', '["b",{"c":"coconut"}]'],
        ),
    )

    @genty_dataset(**call_rpc_argsets)
    def test_call_rpc(self, params, expectedargs):
        with patch('subprocess.check_output') as m_check_output:
            self.cli.call_rpc(*params)

        fullexpectedargs = [
            'zcash-cli',
            '-datadir=FAKE-DATADIR',
        ] + expectedargs

        self.assertEqual(
            self.m_log.mock_calls,
            [call.debug('Running: %r', fullexpectedargs)],
        )

        self.assertEqual(
            m_check_output.mock_calls,
            [
                call(fullexpectedargs),
                call().rstrip(),
            ],
        )

    @genty_dataset(**call_rpc_argsets)
    def test_call_rpc_json(self, params, _):
        with patch('zcash_cli_helper.zcli.ZCLI.call_rpc') as m_call_rpc:
            with patch('zcash_cli_helper.saferjson.loads') as m_loads:
                self.cli.call_rpc_json(*params)

        self.assertEqual(
            m_call_rpc.mock_calls,
            [call(*params)],
        )

        self.assertEqual(
            m_loads.mock_calls,
            [call(m_call_rpc.return_value)],
        )

    @genty_dataset(
        string=('foo', 'foo'),
        true=(True, 'true'),
        false=(False, 'false'),
        integer=(42, '42'),
        decimal=(Decimal('42.03489096'), '42.03489096'),
        text=(u'bar', '"bar"'),
        array_empty=([], '[]'),
        array_full=(['a', 'b', 'c'], '["a","b","c"]'),
        object_empty=({}, '{}'),
        object_full=(
            {'a': 'apple', 'b': 'banana', 'c': 'coconut'},
            '{"a":"apple","b":"banana","c":"coconut"}',
        ),
    )
    def test_encode_arg(self, value, expected):
        actual = ZCLI._encode_arg(value)
        self.assertEqual(actual, expected)

    @genty_dataset(
        null=(None,),
        float=(3.1415,),
    )
    def test_encode_arg_bad_value(self, value):
        self.assertRaises(AssertionError, ZCLI._encode_arg, value)

from unittest import TestCase
from mock import MagicMock, call, patch, sentinel
from zcli import operations


class ZcashOperations_tests (TestCase):
    def setUp(self):
        self.m_cli = MagicMock()
        self.ops = operations.ZcashOperations(self.m_cli)

    @patch('zcli.log.zlog.warn')
    @patch('zcli.log.zlog.debug')
    @patch('time.sleep')
    def test_wait_on_opids_basic(self, m_sleep, m_debug, m_warn):
        opres = [
            {
                'id': sentinel.OP_0,
                'status': 'success',
                'result': {'txid': sentinel.TXID_0},
            },
        ]

        self.m_cli.z_getoperationstatus.return_value = opres
        self.m_cli.z_getoperationresult.return_value = opres
        self.m_cli.gettransaction.return_value = {
            'confirmations': operations.MINCONF,
        }

        result = self.ops.wait_on_opids([sentinel.OP_0])
        self.assertTrue(result)

        self.assertEqual(
            m_sleep.mock_calls,
            [],
        )

        self.assertEqual(
            m_debug.mock_calls,
            [
                call('Waiting for completions:'),
                call('  %s - %s', sentinel.OP_0, 'success'),
                call(''),
                call('Waiting for confirmations:'),
                call(
                    '  %s - txid: %s - confirmations: %s',
                    sentinel.OP_0,
                    sentinel.TXID_0,
                    6,
                ),
                call(''),
            ],
        )

        self.assertEqual(
            m_warn.mock_calls,
            [],
        )

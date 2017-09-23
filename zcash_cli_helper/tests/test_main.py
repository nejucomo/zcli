from unittest import TestCase
from mock import call, patch, sentinel
from zcash_cli_helper.main import main


class main_tests (TestCase):
    @patch('zcash_cli_helper.cliparse.parse_args')
    @patch('zcash_cli_helper.cli.CLI')
    def test_main(self, m_CLI, m_parse_args):

        main(sentinel.ARGS)

        self.assertEqual(
            m_parse_args.mock_calls,
            [call(sentinel.ARGS),
             call().func(m_CLI.return_value)])

        self.assertEqual(
            m_CLI.mock_calls,
            [call(m_parse_args.return_value.BASEDIR)])

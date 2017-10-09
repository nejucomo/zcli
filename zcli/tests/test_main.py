from unittest import TestCase
from mock import call, patch, sentinel
from zcli.main import main


class main_tests (TestCase):
    @patch('sys.stdout')
    @patch('zcli.clargs.parse_args')
    @patch('zcli.zcashcli.ZcashCLI')
    def test_main(self, m_ZcashCLI, m_parse_args, m_stdout):
        m_parse_args.return_value.DEBUG = True
        m_parse_args.return_value.func.return_value = ["json", "result"]

        main(sentinel.ARGS)

        self.assertEqual(
            m_parse_args.mock_calls,
            [call(main.__doc__, sentinel.ARGS),
             call().func(m_ZcashCLI.return_value)])

        self.assertEqual(
            m_ZcashCLI.mock_calls,
            [call(m_parse_args.return_value.DATADIR)])

        self.assertEqual(
            m_stdout.mock_calls,
            [call.write('[\n  "json",\n  "result"\n]')])

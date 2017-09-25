from unittest import TestCase
from mock import call, patch, sentinel
from zcash_cli_helper.main import main


class main_tests (TestCase):
    @patch('sys.stdout')
    @patch('zcash_cli_helper.clargs.parse_args')
    @patch('zcash_cli_helper.zcli.ZCLI')
    def test_main(self, m_ZCLI, m_parse_args, m_stdout):
        m_parse_args.return_value.func.return_value = ["json", "result"]

        main(sentinel.ARGS)

        self.assertEqual(
            m_parse_args.mock_calls,
            [call(main.__doc__, sentinel.ARGS),
             call().func(m_ZCLI.return_value)])

        self.assertEqual(
            m_ZCLI.mock_calls,
            [call(m_parse_args.return_value.DATADIR)])

        self.assertEqual(
            m_stdout.mock_calls,
            [call.write('[\n  "json",\n  "result"\n]')])

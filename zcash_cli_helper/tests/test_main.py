from unittest import TestCase
from mock import call, patch, sentinel
from zcash_cli_helper.main import main


class main_tests (TestCase):
    @patch('zcash_cli_helper.clargs.parse_args')
    @patch('zcash_cli_helper.zcli.ZCLI')
    def test_main(self, m_ZCLI, m_parse_args):

        main(sentinel.ARGS)

        self.assertEqual(
            m_parse_args.mock_calls,
            [call(main.__doc__, sentinel.ARGS),
             call().func(m_ZCLI.return_value)])

        self.assertEqual(
            m_ZCLI.mock_calls,
            [call(m_parse_args.return_value.BASEDIR)])

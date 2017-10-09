from unittest import TestCase
from mock import call, patch, sentinel
from zcli import clargs


class parse_args_tests (TestCase):
    @patch('argparse.ArgumentParser')
    def test_parse_args(self, m_ArgumentParser):

        result = clargs.parse_args(sentinel.DESCRIPTION, sentinel.ARGS)

        self.assertEqual(
            m_ArgumentParser.mock_calls[:1],
            [call(description=sentinel.DESCRIPTION)])

        self.assertEqual(
            m_ArgumentParser.mock_calls[-1:],
            [call().parse_args(sentinel.ARGS)])

        self.assertEqual(
            result,
            m_ArgumentParser.return_value.parse_args.return_value)

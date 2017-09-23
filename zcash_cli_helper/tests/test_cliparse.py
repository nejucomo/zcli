from unittest import TestCase
from mock import call, patch, sentinel, ANY
from pathlib2 import Path
from zcash_cli_helper import cliparse


class MainTests (TestCase):
    @patch('argparse.ArgumentParser')
    def test_main(self, m_ArgumentParser):

        result = cliparse.parse_args(sentinel.DESCRIPTION, sentinel.ARGS)

        self.assertEqual(
            m_ArgumentParser.mock_calls[:3],
            [call(description=sentinel.DESCRIPTION),
             call().add_argument(
                 '--datadir',
                 dest='DATADIR',
                 type=Path,
                 default=Path.home() / '.zcash',
                 help=ANY),
             call().add_subparsers()])

        self.assertEqual(
            m_ArgumentParser.mock_calls[-1:],
            [call().parse_args(sentinel.ARGS)])

        self.assertEqual(
            result,
            m_ArgumentParser.return_value.parse_args.return_value)

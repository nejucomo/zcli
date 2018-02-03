from unittest import TestCase
from mock import call, patch, sentinel
from zcli import clargs


class parse_args_tests (TestCase):
    @patch('argparse.ArgumentParser')
    def test_parse_args(self, m_ArgumentParser):

        m_p = m_ArgumentParser.return_value
        m_opts = m_p.cmdclass.post_process_args.return_value
        m_opts.__dict__ = {
            'DATADIR': sentinel.DATADIR,
            'DEBUG': sentinel.DEBUG,
            'FAKE_ARG_A': sentinel.FAKE_ARG_A,
            'FAKE_ARG_B': sentinel.FAKE_ARG_B,
        }

        result = clargs.parse_args(sentinel.DESCRIPTION, sentinel.ARGS)

        self.assertEqual(
            m_ArgumentParser.mock_calls[:1],
            [call(description=sentinel.DESCRIPTION)])

        self.assertEqual(
            m_ArgumentParser.mock_calls[-2:-1],
            [call().parse_args(sentinel.ARGS)])

        self.assertEqual(
            result,
            (
                {
                    'DATADIR': sentinel.DATADIR,
                    'DEBUG': sentinel.DEBUG,
                },
                m_p.cmdclass.run,
                {
                    'FAKE_ARG_A': sentinel.FAKE_ARG_A,
                    'FAKE_ARG_B': sentinel.FAKE_ARG_B,
                },
            )
        )

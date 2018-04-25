from unittest import TestCase
from decimal import Decimal
from genty import genty, genty_dataset
from mock import MagicMock
from zcli import commands


class FakeUsageError (Exception):
    @classmethod
    def usage_error(cls, msg):
        raise cls(msg)


@genty
class send_tests (TestCase):
    @genty_dataset(
        single_zaddr=(
            ['FAKE_ZADDR', '42', 'this is the memo'],
            [{
                'address': 'FAKE_ZADDR',
                'amount': Decimal('42'),
                'memo': 'this is the memo'.encode('hex'),
            }],
        ),
        multiple=(
            [
                'FAKE_ZADDR', '42', 'this is the memo',
                'FAKE_TADDR', '23', '',
            ],
            [
                {
                    'address': 'FAKE_ZADDR',
                    'amount': Decimal('42'),
                    'memo': 'this is the memo'.encode('hex'),
                },
                {
                    'address': 'FAKE_TADDR',
                    'amount': Decimal('23'),
                }
            ],
        ),
    )
    def test_post_process_args_no_error(self, destinfo, expected):
        m_opts = MagicMock()
        m_opts.DESTINFO = destinfo

        result = commands.send.post_process_args(
            m_opts,
            FakeUsageError.usage_error,
        )

        self.assertIs(result, m_opts)
        self.assertEqual(m_opts.mock_calls, [])
        self.assertEqual(m_opts.DESTINFO, expected)

    @genty_dataset(
        empty=(
            [],
            '^At least one destination must be supplied.$',
        ),
        single_arg=(
            ['foo'],
            ('^DESTINFO must be triplets of ADDR AMOUNT MEMO; '
             'found 1 arguments.$'),
        ),
        # taddr_nonempty_memo=(
        #     ['I am a fake taddr', '42', 's:I am a nonempty memo.'],
        #     'FIXME',
        # ),
    )
    def test_post_process_args_with_error(self, destinfo, rgx):
        m_opts = MagicMock()
        m_opts.DESTINFO = destinfo

        self.assertRaisesRegexp(
            FakeUsageError,
            rgx,
            commands.send.post_process_args,
            m_opts,
            FakeUsageError.usage_error,
        )

import subprocess
import logging
from pathlib2 import Path
from decimal import Decimal
from zcash_cli_helper import saferjson


class CLI (object):
    def __init__(self, datadir):
        assert isinstance(datadir, Path), repr(datadir)
        self._execname = 'zcash-cli'
        self._datadir = datadir
        self._log = logging.getLogger('CLI')

    def call_rpc(self, *args):
        argsprefix = [self._execname, '-datadir={}'.format(self._datadir)]
        fullargs = argsprefix + map(self._encode_arg, args)
        self._log.debug('Running: %r', fullargs)
        return subprocess.check_output(fullargs).rstrip()

    def call_rpc_json(self, *args):
        result = self.call_rpc(*args)
        return saferjson.loads(result)

    @staticmethod
    def _encode_arg(arg):
        t = type(arg)
        if t is str:
            return arg
        elif t in [int, Decimal]:
            return str(arg)
        elif t in [bool, unicode, list, dict]:
            return saferjson.dumps_compact(arg)
        else:
            assert False, 'Invalid CLI argument: {!r}'.format(arg)

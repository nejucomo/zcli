import subprocess
import logging
from pathlib2 import Path
from decimal import Decimal
from zcash_cli_helper import saferjson


class ZCLI (object):
    def __init__(self, datadir):
        assert isinstance(datadir, Path), repr(datadir)
        self._execname = 'zcash-cli'
        self._datadir = datadir
        self._log = logging.getLogger('ZCLI')

    def __getattr__(self, method):
        return ZCLIMethod(self._execname, self._datadir, self._log)


class ZCLIMethod (object):
    def __init__(self, execname, datadir, log):
        self._execname = execname
        self._datadir = datadir
        self._log = log

    def __call__(self, *args):
        result = self._call_raw_result(*args)
        if result.startswith('{') or result.startswith('['):
            result = saferjson.loads(result)
        return result

    def _call_raw_result(self, *args):
        argsprefix = [self._execname, '-datadir={}'.format(self._datadir)]
        fullargs = argsprefix + map(self._encode_arg, args)
        self._log.debug('Running: %r', fullargs)
        return subprocess.check_output(fullargs).rstrip()

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
            assert False, 'Invalid ZCLI argument: {!r}'.format(arg)

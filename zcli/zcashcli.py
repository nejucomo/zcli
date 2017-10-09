import subprocess
import logging
from pathlib2 import Path
from zcli import saferjson


class ZcashCLI (object):
    def __init__(self, datadir):
        assert isinstance(datadir, Path), repr(datadir)
        self._execname = 'zcash-cli'
        self._datadir = datadir
        self._log = logging.getLogger('ZcashCLI')

    def __getattr__(self, method):
        return ZcashCLIMethod(method, self._execname, self._datadir, self._log)


class ZcashCLIMethod (object):
    def __init__(self, method, execname, datadir, log):
        self._method = method
        self._execname = execname
        self._datadir = datadir
        self._log = log

    def __call__(self, *args):
        result = self._call_raw_result(*args)
        if result.startswith('{') or result.startswith('['):
            result = saferjson.loads(result)
        return result

    def _call_raw_result(self, *args):
        argsprefix = [
            self._execname,
            '-datadir={}'.format(self._datadir),
            self._method,
        ]
        fullargs = argsprefix + map(saferjson.encode_param, args)
        self._log.debug('Running: %r', fullargs)
        return subprocess.check_output(fullargs).rstrip()

import os
import sys
import logging
from zcli import clargs, zcashcli, operations, saferjson


def main(args=sys.argv[1:]):
    """
    Simplify certain useful tasks on top of the Zcash RPC interface.
    """
    (opts, cmdfunc, cmdkwargs) = clargs.parse_args(main.__doc__, args)
    init_logging(opts['DEBUG'])

    zops = operations.ZcashOperations(
        zcashcli.ZcashCLI(opts['DATADIR']),
    )
    result = cmdfunc(zops, **cmdkwargs)

    sys.stdout.write(saferjson.encode_param(result, pretty=True))


def init_logging(debug):
    progname = os.path.basename(sys.argv[0])
    format = ('%(asctime)s {} %(message)s'
              .format(progname.replace('%', '%%')))

    logging.basicConfig(
        stream=sys.stderr,
        format=format,
        datefmt='%Y-%m-%dT%H:%M:%S',
        level=logging.DEBUG if debug else logging.INFO,
    )

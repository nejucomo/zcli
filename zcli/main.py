import sys
import logging
from zcli import clargs, zcashcli, saferjson


def main(args=sys.argv[1:]):
    """
    Simply certain useful tasks on top of the Zcash RPC interface.
    """
    opts = clargs.parse_args(main.__doc__, args)
    init_logging(opts.DEBUG)

    args = [zcashcli.ZcashCLI(opts.DATADIR)]
    for name in opts.argnames:
        args.append(getattr(opts, name))
    van = opts.varargsname
    if van is not None:
        args.extend(van)

    result = opts.func(*args)
    sys.stdout.write(saferjson.encode_param(result, pretty=True))


def init_logging(debug):
    logging.basicConfig(
        stream=sys.stderr,
        format='%(asctime)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG if debug else logging.INFO,
    )

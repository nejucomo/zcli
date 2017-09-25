import sys
from zcash_cli_helper import clargs, zcli, saferjson


def main(args=sys.argv[1:]):
    """
    Simply certain useful tasks on top of the Zcash RPC interface.
    """
    opts = clargs.parse_args(main.__doc__, args)
    result = opts.func(zcli.ZCLI(opts.DATADIR))
    sys.stdout.write(saferjson.encode_param(result, pretty=True))

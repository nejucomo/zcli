import sys
from zcash_cli_helper import clargs, zcli


def main(args=sys.argv[1:]):
    """
    Simply certain useful tasks on top of the Zcash RPC interface.
    """
    opts = clargs.parse_args(main.__doc__, args)
    opts.func(zcli.ZCLI(opts.BASEDIR))

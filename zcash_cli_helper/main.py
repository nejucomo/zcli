import sys
from zcash_cli_helper import cliparse, cli


def main(args=sys.argv[1:]):
    """
    Simply certain useful tasks on top of the Zcash RPC interface.
    """
    opts = cliparse.parse_args(args)
    opts.func(cli.CLI(opts.BASEDIR))

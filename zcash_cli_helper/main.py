import sys
from .cliparse import parse_args


def main(args=sys.argv[1:]):
    """
    Simply certain useful tasks on top of the Zcash RPC interface.
    """
    opts = parse_args(args)
    raise NotImplementedError((main, opts))

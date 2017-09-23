import argparse
from pathlib2 import Path
from .commands import COMMANDS


def parse_args(description, args):
    p = argparse.ArgumentParser(description=description)

    p.add_argument(
        '--datadir',
        dest='DATADIR',
        type=Path,
        default=Path.home() / '.zcash',
        help='Node datadir.',
    )

    subp = p.add_subparsers()
    for (name, f) in COMMANDS.iteritems():
        cmdp = subp.add_parser(name.replace('_', '-'), help=f.__doc__)
        cmdp.set_default(func=f)

    return p.parse_args(args)

import argparse
from pathlib2 import Path
from zcli.commands import COMMANDS


def parse_args(description, args):
    p = argparse.ArgumentParser(description=description)
    add_standard_args(p)

    subp = p.add_subparsers()
    for (name, cls) in COMMANDS.iteritems():
        cmdp = subp.add_parser(name.replace('_', '-'), help=cls.__doc__)
        cls.add_arg_parser(cmdp)
        cmdp.set_defaults(func=cls.run)

    opts = p.parse_args(args)

    cmdkwargs = vars(opts)
    del cmdkwargs['DATADIR']
    del cmdkwargs['DEBUG']

    return (opts, cmdkwargs)


def add_standard_args(argparser):
    argparser.add_argument(
        '--datadir',
        dest='DATADIR',
        type=Path,
        default=Path.home() / '.zcash',
        help='Node datadir.',
    )

    argparser.add_argument(
        '--debug',
        dest='DEBUG',
        action='store_true',
        default=False,
        help='Debug output.',
    )

import argparse
import inspect
from pathlib2 import Path
from zcli.commands import COMMANDS


def parse_args(description, args):
    p = argparse.ArgumentParser(description=description)
    add_standard_args(p)

    subp = p.add_subparsers()
    for (name, f) in COMMANDS.iteritems():
        _add_subcommand(subp, name, f)

    return p.parse_args(args)


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


def _add_subcommand(subp, name, f):
    cmdp = subp.add_parser(name.replace('_', '-'), help=f.__doc__)

    (args, varargs, kw, defaults) = inspect.getargspec(f)
    assert (kw, defaults) == (None, None), (f, args, varargs, kw, defaults)

    argnames = []
    for arg in args[1:]:
        argname = arg.upper()
        argnames.append(argname)
        cmdp.add_argument(argname)

    varargsname = None
    if varargs is not None:
        vargsname = varargs.upper()
        varargsname = vargsname
        cmdp.add_argument(vargsname, nargs='*')

    cmdp.set_defaults(func=f, argnames=argnames, varargsname=varargsname)

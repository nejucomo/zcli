import os
import argparse
from pathlib2 import Path
from zcli.commands import COMMANDS


def parse_args(description, args):
    p = argparse.ArgumentParser(description=description)
    add_standard_args(p)
    add_subcommand_args(p.add_subparsers())

    opts = p.parse_args(args)

    cmdclass = opts.cmdclass
    del opts.cmdclass

    cmdkwargs = vars(cmdclass.post_process_args(opts, p.error))

    globopts = {}
    for gopt in ['DATADIR', 'DEBUG']:
        globopts[gopt] = cmdkwargs.pop(gopt)

    return (globopts, cmdclass.run, cmdkwargs)


def add_standard_args(argparser):
    dd = os.environ.get('ZCLI_DATADIR')
    defaultdatadir = Path(dd) if dd else Path.home() / '.zcash'

    argparser.add_argument(
        '--datadir',
        dest='DATADIR',
        type=Path,
        default=defaultdatadir,
        help='Node datadir. Default: {!r}'.format(str(defaultdatadir)),
    )

    argparser.add_argument(
        '--debug',
        dest='DEBUG',
        action='store_true',
        default=False,
        help='Debug output.',
    )


def add_subcommand_args(subp):
    for (name, cls) in COMMANDS.iteritems():
        cmdp = subp.add_parser(name.replace('_', '-'), help=cls.__doc__)
        cls.add_arg_parser(cmdp)
        cmdp.set_defaults(cmdclass=cls)

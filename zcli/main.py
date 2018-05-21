import sys
from subprocess import CalledProcessError
from zcli import clargs, zcashcli, operations, saferjson, ui


def main(args=sys.argv[1:]):
    """
    Simplify certain useful tasks on top of the Zcash RPC interface.
    """
    (opts, cmdfunc, cmdkwargs) = clargs.parse_args(main.__doc__, args)

    zops = operations.ZcashOperations(
        zcashcli.ZcashCLI(opts['DATADIR']),
    )
    uicb = ui.make_ui(opts['VERBOSITY'])
    try:
        result = cmdfunc(uicb, zops, **cmdkwargs)
    except CalledProcessError as e:
        raise SystemExit(e)

    sys.stdout.write(saferjson.encode_param(result, pretty=True))

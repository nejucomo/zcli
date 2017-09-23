import sys
from functable import FunctionTable
from zcash_cli_helper.acctab import AccumulatorTable
from zcash_cli_helper.saferjson import loads, dump_pretty

COMMANDS = FunctionTable()


@COMMANDS.register
def list_balances(zc):
    """List all known address balances."""
    balances = AccumulatorTable()

    # Gather t-addr balances:
    for utxo in loads(zc.listunspent()):
        balances[utxo['address']] += utxo['amount']

    # Gather t-addr balances:
    for zaddr in loads(zc.z_listaddresses()):
        balances[zaddr] = loads(zc.z_getbalance(zaddr))

    dump_pretty(balances, sys.stdout)

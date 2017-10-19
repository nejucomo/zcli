import pprint
import time
from decimal import Decimal
from functable import FunctionTable
from zcli.acctab import AccumulatorTable


COMMANDS = FunctionTable()


@COMMANDS.register
def list_balances(zc):
    """List all known address balances."""
    balances = AccumulatorTable()

    # Gather t-addr balances:
    for utxo in zc.listunspent():
        if utxo['spendable'] is True:
            balances[utxo['address']] += utxo['amount']

    # Gather t-addr balances:
    for zaddr in zc.z_listaddresses():
        balances[zaddr] = Decimal(zc.z_getbalance(zaddr.encode('utf8')))

    return {
        'total': sum(balances.values()),
        'addresses': dict(
            (k, v)
            for (k, v)
            in balances.iteritems()
            if v > 0
        ),
    }


@COMMANDS.register
def send(zc, src, *dstargs):
    """Send."""
    MINCONF = 6

    destitems = parse_send_dst_args(dstargs)
    opid = zc.z_sendmany(src, destitems)

    opinfo = {'status': None}
    while opinfo['status'] in (None, 'queued', 'executing'):
        print 'Waiting for completion: {}'.format(opid)
        time.sleep(13)
        [opinfo] = zc.z_getoperationresult([opid])

    if opinfo['status'] != 'success':
        raise SystemExit(pprint.pformat(opinfo))

    txid = opinfo['result']['txid']
    confirmations = zc.gettransaction(txid)["confirmations"]
    while confirmations < MINCONF:
        print 'Waiting for confirmation: {} under {} blocks'.format(
            txid,
            confirmations,
        )
        time.sleep(167)
        confirmations = zc.gettransaction(txid)["confirmations"]


def parse_send_dst_args(dstargs):
    destmap = []

    dstinfo = None
    for d in dstargs:
        if len(dstinfo) == 2:
            (dstaddr, amount) = dstinfo
            dstinfo = None

            destentry = {'address': dstaddr, 'amount': amount}
            if d.startswith(':'):
                if not dstaddr.startswith('zc'):
                    raise SystemExit(
                        'Memo given with non-zaddr: {!r} {!r}'.format(
                            dstinfo,
                            d,
                        ),
                    )
                destentry['memo'] = d[1:].encode('hex')

            destmap.append(destentry)

            if d.startswith(':'):
                continue

        if dstinfo is None:
            dstinfo = (d,)
        elif len(dstinfo) == 1:
            (dstaddr,) = dstinfo
            dstinfo = (dstaddr, Decimal(d))

    if dstinfo is not None:
        if len(dstinfo) == 1:
            raise SystemExit(
                'Missing amount for destination: {!r}'.format(dstinfo),
            )
        else:
            assert len(dstinfo) == 2, dstinfo
            (addr, amt) = dstinfo
            destmap.append({'address': addr, 'amount': amt})

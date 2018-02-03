import time
from decimal import Decimal
from functable import FunctionTable
from zcli.acctab import AccumulatorTable


MINCONF = 6
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
    destitems = parse_send_dst_args(dstargs)
    opid = zc.z_sendmany(src, destitems)
    wait(zc, opid)


def parse_send_dst_args(dstargs):
    destmap = []

    dstinfo = None
    for d in dstargs:
        if dstinfo is not None and len(dstinfo) == 2:
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

    return destmap


@COMMANDS.register
def wait(zc, *opids):
    """Wait until all operations complete and have MINCONF confirmations."""
    opids = set(opids)

    txids = []

    somefailed = False
    while len(opids) > 0:
        print 'Waiting for completions:'
        completes = []
        for opinfo in zc.z_getoperationstatus(list(opids)):
            opid = opinfo['id']
            status = opinfo['status']
            print '  {} - {}'.format(opid, status)

            if status not in {'queued', 'executing'}:
                opids.remove(opid)
                completes.append(opid)

        for opinfo in zc.z_getoperationresult(completes):
            if opinfo['status'] == 'success':
                opid = opinfo['id']
                txid = opinfo['result']['txid']
                txids.append((opid, txid))
            else:
                somefailed = True
                print 'FAILED OPERATION: {!r}'.format(opinfo)

        print
        if len(opids) > 0:
            time.sleep(13)

    while txids:
        print 'Waiting for confirmations:'
        newtxids = []
        for (opid, txid) in txids:
            txinfo = zc.gettransaction(txid, True)
            confs = txinfo['confirmations']
            print '  {} - txid: {} - confirmations: {}'.format(
                opid,
                txid,
                confs,
            )
            if confs < 0:
                print 'FAILED TO CONFIRM: {!r}'.format(txinfo)
            elif confs < MINCONF:
                newtxids.append((opid, txid))
        txids = newtxids

        print
        time.sleep(131)

    return not somefailed

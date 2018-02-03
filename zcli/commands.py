import time
from decimal import Decimal, InvalidOperation
from functable import FunctionTable
from zcli.acctab import AccumulatorTable


MINCONF = 6
COMMANDS = FunctionTable()


@COMMANDS.register
class list_balances (object):
    """List all known address balances."""

    @staticmethod
    def add_arg_parser(p):
        return

    @staticmethod
    def run(zc):
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
class send (object):
    """Send from an address to multiple recipients."""

    @staticmethod
    def add_arg_parser(p):
        p.add_argument(
            'SOURCE',
            help='Source address.',
        )

        def destination_info(arg):
            fields = arg.split(',', 2)
            assert len(fields) <= 3, fields
            if not (2 <= len(fields)):
                p.error(
                    ('Expected ADDR,AMOUNT[,MEMO] for destination argument, '
                     'found: {!r}')
                    .format(arg)
                )

            else:
                (addr, amounttext) = fields[:2]
                try:
                    amount = Decimal(amounttext)
                except InvalidOperation as e:
                    p.error(
                        ('Could not parse amount; {}')
                        .format(e)
                    )

                entry = {
                    'address': addr,
                    'amount': amount,
                }

                if len(fields) == 3:
                    memo = fields[2]
                    if addr.startswith('zc'):
                        if memo.startswith('0x'):
                            # Hex encoding:
                            memo = memo[2:]
                            try:
                                memo.decode('hex')
                            except TypeError as e:
                                p.error(
                                    ('Could not decode MEMO from 0x '
                                     'hexadecimal format: {}')
                                    .format(e)
                                )
                        elif memo.startswith(':'):
                            memo = memo.encode('hex')
                        else:
                            p.error(
                                ('MEMO must start with "0x" for hex '
                                 'encoding or ":" for plain string '
                                 'encoding. Found: {!r}')
                                .format(memo)
                            )

                        entry['memo'] = memo
                    else:
                        p.error(
                            ('Destination address {!r} is not a Z Address '
                             'and cannot receive a memo: {!r}')
                            .format(addr, memo)
                        )

                return entry

        p.add_argument(
            'DEST',
            nargs='+',
            type=destination_info,
            help='Destination ADDR,AMOUNT[,MEMO].',
        )

    @staticmethod
    def run(zc, SOURCE, DEST):
        opid = zc.z_sendmany(opts.SOURCE, opts.DEST)
        wait.run(zc, OPID=[opid])


@COMMANDS.register
class wait (object):
    """Wait until all operations complete and have MINCONF confirmations."""

    @staticmethod
    def add_arg_parser(p):
        p.add_argument(
            'OPID',
            nargs='+',
            help='Operation id.',
        )

    @staticmethod
    def run(zc, OPID):
        opids = set(OPID)

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

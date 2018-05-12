import time
from decimal import Decimal
from zcli.log import zlog


MINCONF = 6


class ZcashOperations (object):
    """Useful operations performed with a ZcashCli."""

    def __init__(self, cli):
        self.cli = cli

    def iter_blocks(self, blockhash=None):
        if blockhash is None:
            blockhash = self.cli.getblockhash(1)

        while blockhash is not None:
            block = self.cli.getblock(blockhash)
            yield block
            blockhash = block.get('nextblockhash')

    def iter_transactions(self, startblockhash=None):
        for block in self.iter_blocks(startblockhash):
            for txid in block['tx']:
                yield (block, self.cli.getrawtransaction(txid, 1))

    def get_taddr_balances(self):
        balances = {}
        for unspent in self.cli.listunspent():
            addr = unspent['address']
            amount = unspent['amount']
            balances[addr] = amount + balances.get(addr, Decimal(0))
        return balances

    def wait_on_opids(self, opids, confirmations=MINCONF):
        assert isinstance(opids, list) or isinstance(opids, set), opids
        opids = set(opids)
        txids = []

        somefailed = False
        while len(opids) > 0:
            zlog.debug('Waiting for completions:')
            completes = []
            for opinfo in self.cli.z_getoperationstatus(list(opids)):
                opid = opinfo['id']
                status = opinfo['status']
                zlog.debug('  %s - %s', opid, status)

                if status not in {'queued', 'executing'}:
                    opids.remove(opid)
                    completes.append(opid)

            if completes:
                for opinfo in self.cli.z_getoperationresult(completes):
                    if opinfo['status'] == 'success':
                        opid = opinfo['id']
                        txid = opinfo['result']['txid']
                        txids.append((opid, txid))
                    else:
                        somefailed = True
                        zlog.warn('FAILED OPERATION: %r', opinfo)

            zlog.debug('')
            if len(opids) > 0:
                time.sleep(13)

        while txids:
            zlog.debug('Waiting for confirmations:')
            newtxids = []
            for (opid, txid) in txids:
                txinfo = self.cli.gettransaction(txid, True)
                confs = txinfo['confirmations']
                zlog.debug(
                    '  %s - txid: %s - confirmations: %s',
                    opid,
                    txid,
                    confs,
                )
                if confs < 0:
                    zlog.warn('FAILED TO CONFIRM: %r', txinfo)
                elif confs < confirmations:
                    newtxids.append((opid, txid))
            txids = newtxids

            zlog.debug('')
            if len(txids) > 0:
                time.sleep(77)

        return not somefailed

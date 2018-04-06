from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncGetTransactionsTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        adapter = SteemAdapter(
            endpoints='https://steemd.pevo.science',
            retry=False
        )
        self.chainsync = ChainSync(adapter=adapter, retry=False)

    def test_get_transactions(self):
        txs = [
            'a3815d4a17f1331481ec6bf89ba0844ce16175bc',
            'c68435a34a7afc701771eb090f96526ed4c2a37b',
        ]
        result = self.chainsync.get_transactions(txs)
        for tx in result:
            self.assertTrue(tx['transaction_id'] in txs)

    def test_get_transactions_exception_no_transaction_id(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_transactions()

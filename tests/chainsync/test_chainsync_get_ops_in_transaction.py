from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncGetOpsInTransactionTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        adapter = SteemAdapter(
            endpoints='https://steemd.pevo.science',
            retry=False
        )
        self.chainsync = ChainSync(adapter=adapter, retry=False)

    def test_get_ops_in_transaction(self):
        tx_id = 'c68435a34a7afc701771eb090f96526ed4c2a37b'
        result = self.chainsync.get_ops_in_transaction(tx_id)
        for op in result:
            self.assertEqual(op['block_num'], 20905025)

    def test_get_ops_in_transaction_exception_no_transaction_id(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_ops_in_transaction()

    def test_get_ops_in_transaction_exception_invalid_transaction_id(self):
        with self.assertRaises(Exception) as context:
            results = [op in self.chainsync.get_ops_in_transaction('0000000000000000000000000000000000000000')]

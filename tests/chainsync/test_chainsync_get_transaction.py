from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncGetTransactionTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        adapter = SteemAdapter(
            endpoints='https://steemd.pevo.science',
            retry=False
        )
        self.chainsync = ChainSync(adapter=adapter, retry=False)

    def test_get_transaction(self):
        tx_id = 'c68435a34a7afc701771eb090f96526ed4c2a37b'
        result = self.chainsync.get_transaction(tx_id)
        self.assertEqual(result['block_num'], 20905025)

    def test_get_transaction_exception_no_transaction_id(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_transaction()

    def test_get_transaction_exception_invalid_transaction_id(self):
        with self.assertRaises(Exception) as context:
            self.chainsync.get_transaction('0000000000000000000000000000000000000000')

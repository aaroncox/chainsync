from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncOpDataFormatTestCase(ChainSyncBaseTestCase):

    # Tests data format returned by `get_block`
    def test_format_op_from_get_block(self):
        block_num = 10000000
        for block in self.chainsync.get_block_sequence(block_num, limit=1):
            for op in self.chainsync.from_block_get_ops(block):
                self.assertEqual(op['block_num'], block_num)
                self.assertTrue(op['op_in_trx'] >= 0)
                self.assertTrue(op['trx_in_block'] >= 0)
                self.assertTrue('operation_type' in op and op['operation_type'] is not False)
                self.assertTrue('transaction_id' in op and op['transaction_id'] is not False)
                self.assertTrue('timestamp' in op and op['timestamp'] is not False)

    # Tests data format returned by `get_ops_in_block`
    def test_format_op_from_get_ops_in_block(self):
        block_num = 10000000
        for op in self.chainsync.get_ops_in_block(block_num):
            self.assertEqual(op['block_num'], block_num)
            self.assertTrue(op['op_in_trx'] >= 0)
            self.assertTrue(op['trx_in_block'] >= 0)
            self.assertTrue('operation_type' in op and op['operation_type'] is not False)
            self.assertTrue('transaction_id' in op and op['transaction_id'] is not False)
            self.assertTrue('timestamp' in op and op['timestamp'] is not False)

    # Tests data format returned by `get_transaction`
    def test_txopdata_format(self):
        # Specify custom node since api.steemit.com doesn't have these endpoints enabled
        adapter = SteemAdapter(
            endpoints='https://steemd.pevo.science',
            retry=False
        )
        chainsync = ChainSync(adapter=adapter, retry=False)
        # Load a transaction by ID
        transaction = chainsync.get_transaction('04008551461adb9a48c5c9eac8be6f63f9c840d9')
        for opIndex, op in enumerate(transaction['operations']):
            formatted = adapter.format_op_from_get_transaction(transaction, op, opIndex=opIndex)
            self.assertEqual(formatted['block_num'], 4042653)
            self.assertTrue(formatted['op_in_trx'] >= 0)
            self.assertTrue(formatted['trx_in_block'] >= 0)
            self.assertTrue('operation_type' in formatted and formatted['operation_type'] is not False)
            self.assertTrue('transaction_id' in formatted and formatted['transaction_id'] is not False)
            # self.assertTrue('timestamp' in formatted and formatted['timestamp'] is not False) # NYI - https://github.com/steemit/steem/issues/2310

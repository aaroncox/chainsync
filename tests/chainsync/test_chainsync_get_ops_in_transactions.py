# from test_base import ChainSyncBaseTestCase
#
#
# class ChainSyncGetTransactionsTestCase(ChainSyncBaseTestCase):
#
#     def test_get_transactions(self):
#         blocks = [
#             20905050,
#             20905025,
#         ]
#         txs = [
#             'a3815d4a17f1331481ec6bf89ba0844ce16175bc',
#             'c68435a34a7afc701771eb090f96526ed4c2a37b',
#         ]
#         result = self.chainsync.get_ops_in_transactions(txs)
#         for op in result:
#             opType, opData = op
#             self.assertTrue(opData['block_num'] in blocks)
#
#     def test_get_transactions_exception_no_transaction_id(self):
#         with self.assertRaises(TypeError) as context:
#             self.chainsync.get_transactions()

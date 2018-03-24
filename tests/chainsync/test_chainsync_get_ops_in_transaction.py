# from test_base import ChainSyncBaseTestCase
#
#
# class ChainSyncGetOpsInTransactionTestCase(ChainSyncBaseTestCase):
#
#     def test_get_ops_in_transaction(self):
#         tx_id = 'c68435a34a7afc701771eb090f96526ed4c2a37b'
#         result = self.chainsync.get_ops_in_transaction(tx_id)
#         for op in result:
#             opType, opData = op
#             self.assertEqual(opData['block_num'], 20905025)
#
#     def test_get_ops_in_transaction_exception_no_transaction_id(self):
#         with self.assertRaises(TypeError) as context:
#             self.chainsync.get_ops_in_transaction()

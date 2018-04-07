from test_base import ChainSyncBaseTestCase


class ChainSyncFromBlockGetOpsRegularTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        # initialize parent
        super(ChainSyncFromBlockGetOpsRegularTestCase, self).setUp()
        # has both virtual ops and regular ops
        self.block = self.chainsync.get_block(1093)

    def test_from_block_get_ops_regular(self):
        for result in self.chainsync.from_block_get_ops_regular(self.block):
            self.assertEqual(result['block_num'], 1093)

    def test_from_block_get_ops_regular_no_value(self):
        with self.assertRaises(TypeError) as context:
            result = [result for result in self.chainsync.from_block_get_ops_regular("1")]

    def test_from_block_get_ops_regular_non_block_value(self):
        with self.assertRaises(TypeError) as context:
            result = [result for result in self.chainsync.from_block_get_ops_regular("1")]

    def test_from_block_get_ops_regular_whitelist(self):
        whitelist = ['pow']
        for result in self.chainsync.from_block_get_ops_regular(self.block, whitelist=whitelist):
            self.assertTrue(result['operation_type'] in whitelist)

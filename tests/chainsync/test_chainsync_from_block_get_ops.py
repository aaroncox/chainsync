from test_base import ChainSyncBaseTestCase


class ChainSyncFromBlockGetOpsTestCase(ChainSyncBaseTestCase):

    def setUp(self):
        # initialize parent
        super(ChainSyncFromBlockGetOpsTestCase, self).setUp()
        # has both virtual ops and regular ops
        self.block = self.chainsync.get_block(1093)

    def test_from_block_get_ops(self):
        for result in self.chainsync.from_block_get_ops(self.block):
            self.assertEqual(result['block_num'], 1093)

    def test_from_block_get_ops_no_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.from_block_get_ops()

    def test_from_block_get_ops_non_block_value(self):
        with self.assertRaises(TypeError) as context:
            result = [result for result in self.chainsync.from_block_get_ops("1")]

    def test_from_block_get_ops_whitelist(self):
        whitelist = ['pow']
        for result in self.chainsync.from_block_get_ops(self.block, virtual_ops=True, whitelist=whitelist):
            self.assertTrue(result['operation_type'] in whitelist)

    def test_from_block_get_ops_detect_virtual_ops_in_whitelist(self):
        whitelist = ['producer_reward']
        # virtual_ops is not enabled, but the whitelist is requesting a virtual op
        results = [result for result in self.chainsync.from_block_get_ops(self.block, whitelist=whitelist)]
        # we should still get the virtual op back
        self.assertTrue(len(results), 1)
        for result in results:
            # and it should be in the whitelist
            self.assertTrue(result['operation_type'] in whitelist)

    def test_from_block_get_ops_with_virtual_ops_enabled(self):
        for result in self.chainsync.from_block_get_ops(self.block, virtual_ops=True):
            self.assertTrue(result['operation_type'] in ['producer_reward', 'pow'])

    def test_from_block_get_ops_with_virtual_ops_disabled(self):
        for result in self.chainsync.from_block_get_ops(self.block, virtual_ops=False):
            self.assertEqual(result['operation_type'], 'pow')

    def test_from_block_get_ops_with_regular_ops_enabled(self):
        for result in self.chainsync.from_block_get_ops(self.block, regular_ops=True):
            self.assertTrue(result['operation_type'] in ['producer_reward', 'pow'])

    def test_from_block_get_ops_with_regular_ops_enabled_virtual_ops_enabled(self):
        results = [result for result in self.chainsync.from_block_get_ops(self.block, regular_ops=True, virtual_ops=True) if result]
        self.assertEqual(len(results), 5)  # 4 pow + 1 producer_reward
        for result in results:
            self.assertTrue(result['operation_type'] in ['pow', 'producer_reward'])

    def test_from_block_get_ops_with_regular_ops_disabled(self):
        results = [result for result in self.chainsync.from_block_get_ops(self.block, regular_ops=False) if result]
        # Should return 0 results, virtual ops aren't loaded by default (requires extra API call)
        self.assertEqual(len(results), 0)

    def test_from_block_get_ops_with_regular_ops_disabled_virtual_ops_enabled(self):
        results = [result for result in self.chainsync.from_block_get_ops(self.block, regular_ops=False, virtual_ops=True) if result]
        # Should return a single producer_reward
        self.assertEqual(len(results), 1)
        for result in results:
            self.assertEqual(result['operation_type'], 'producer_reward')

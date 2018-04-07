from test_base import ChainSyncBaseTestCase


class ChainSyncGetOpsInBlocksTestCase(ChainSyncBaseTestCase):

    def test_get_ops_in_blocks(self):
        blocks = [200000]
        results = self.chainsync.get_ops_in_blocks(blocks)
        for idx, result in enumerate(results):
            self.assertTrue(result['block_num'] in blocks)

    def test_get_ops_in_blocks_no_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_ops_in_blocks()

    def test_get_ops_in_blocks_non_list_value(self):
        with self.assertRaises(TypeError) as context:
            results = self.chainsync.get_ops_in_blocks(10)
            for result in results:
                print(result)

    def test_get_ops_in_blocks_list_of_string_values(self):
        blocks = ["5", "10"]
        blocks_as_int = [5, 10]
        results = self.chainsync.get_ops_in_blocks(blocks)
        for idx, result in enumerate(results):
            self.assertTrue(result['block_num'] in blocks_as_int)

    def test_get_ops_in_blocks_filtered(self):
        blocks = [10000000, 11000000]
        whitelist = ['producer_reward']
        results = self.chainsync.get_ops_in_blocks(blocks, whitelist=whitelist)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in whitelist)

    def test_get_ops_in_blocks_regular_and_virtual(self):
        blocks = [1093, 1094]  # contains pow (non-virtual) + producer (virtual) ops
        results = self.chainsync.get_ops_in_blocks(blocks, virtual_only=False)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in ['pow', 'producer_reward'])

    def test_get_ops_in_blocks_virtual_only(self):
        blocks = [1093, 1094]  # contains pow (non-virtual) + producer (virtual) ops
        results = self.chainsync.get_ops_in_blocks(blocks, virtual_only=True)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in ['producer_reward'])

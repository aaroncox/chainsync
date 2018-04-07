from test_base import ChainSyncBaseTestCase


class ChainSyncGetOpsInBlockSequenceTestCase(ChainSyncBaseTestCase):

    def test_get_ops_in_block_sequence(self):
        blocks = [200000, 200001]
        start_block = 200000
        limit = 1
        results = self.chainsync.get_ops_in_block_sequence(start_block, limit)
        for idx, result in enumerate(results):
            self.assertTrue(result['block_num'] in blocks)

    def test_get_ops_in_block_sequence_no_start_block(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_ops_in_block_sequence()

    def test_get_ops_in_block_sequence_no_limit(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_ops_in_block_sequence(1)

    def test_get_ops_in_block_sequence_string_values(self):
        blocks = [1093, 1094]
        results = self.chainsync.get_ops_in_block_sequence('1093', '2')
        for idx, result in enumerate(results):
            self.assertTrue(result['block_num'] in blocks)
        self.assertTrue(False)

    def test_get_ops_in_block_sequence_filtered(self):
        blocks = [1093, 1094]  # contains pow (non-virtual) + producer (virtual) ops
        whitelist = ['pow']
        results = self.chainsync.get_ops_in_block_sequence(1093, 2, whitelist=whitelist)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in whitelist)
            self.assertTrue(result['block_num'] in blocks)

    def test_get_ops_in_block_sequence_regular_and_virtual(self):
        blocks = [1093, 1094]  # contains pow (non-virtual) + producer (virtual) ops
        results = self.chainsync.get_ops_in_block_sequence(1093, 2, virtual_only=False)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in ['pow', 'producer_reward'])
            self.assertTrue(result['block_num'] in blocks)

    def test_get_ops_in_block_sequence_virtual_only(self):
        blocks = [1093, 1094]  # contains pow (non-virtual) + producer (virtual) ops
        results = self.chainsync.get_ops_in_block_sequence(1093, 2, virtual_only=True)
        for idx, result in enumerate(results):
            self.assertTrue(result['operation_type'] in ['producer_reward'])
            self.assertTrue(result['block_num'] in blocks)

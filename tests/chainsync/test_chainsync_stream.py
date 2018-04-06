from test_base import ChainSyncBaseTestCase


class ChainSyncStreamTestCase(ChainSyncBaseTestCase):

    def test_stream_blocks(self):
        for dataType, block in self.chainsync.stream(['blocks']):
            self.assertEqual(dataType, 'block')
            self.assertTrue(block['block_num'] > 1)
            break  # Kill the generator loop

    def test_stream_blocks_from_irreversible(self):
        for dataType, block in self.chainsync.stream(['blocks'], mode='irreversible'):
            self.assertEqual(dataType, 'block')
            self.assertTrue(block['block_num'] > 1)
            break  # Kill the generator loop

    def test_stream_blocks_from_block_height(self):
        for dataType, block in self.chainsync.stream(['blocks'], start_block=10):
            self.assertEqual(dataType, 'block')
            self.assertEqual(block['block_num'], 10)
            break  # Kill the generator loop

    def test_stream_blocks(self):
        for dataType, block in self.chainsync.stream(['blocks']):
            self.assertEqual(dataType, 'block')
            self.assertTrue(block['block_num'] > 1)
            break  # Kill the generator loop

    def test_stream_ops(self):
        for dataType, block in self.chainsync.stream(['ops']):
            self.assertEqual(dataType, 'op')
            self.assertTrue(block['block_num'] > 1)
            break  # Kill the generator loop

    def test_stream_ops_from_block_height(self):
        for dataType, block in self.chainsync.stream(['ops'], start_block=3000000):
            self.assertEqual(dataType, 'op')
            self.assertEqual(block['block_num'], 3000000)
            break  # Kill the generator loop

    def test_stream_ops_per_block(self):
        start_block = 3000000
        for dataType, ops_per_block in self.chainsync.stream(['ops_per_blocks'], start_block=start_block, batch_size=1):
            self.assertEqual(dataType, 'ops_per_block')
            self.assertTrue(start_block in ops_per_block)
            self.assertEqual(ops_per_block[start_block], 3)
            break  # Kill the generator loop

    def test_stream_config(self):
        start_block = 3000000
        for dataType, config in self.chainsync.stream(['config'], start_block=start_block, batch_size=1):
            print(config)
            self.assertEqual(dataType, 'config')
            self.assertTrue('IS_TEST_NET' in config)
            break  # Kill the generator loop

    def test_stream_status(self):
        start_block = 3000000
        for dataType, status in self.chainsync.stream(['status'], start_block=start_block, batch_size=1):
            print(status)
            self.assertEqual(dataType, 'status')
            self.assertTrue('head_block_number' in status)
            break  # Kill the generator loop

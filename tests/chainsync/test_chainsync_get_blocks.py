from test_base import ChainSyncBaseTestCase

class ChainSyncGetBlocksTestCase(ChainSyncBaseTestCase):

    def test_get_blocks(self):
        blocks = [5, 10]
        results = self.chainsync.get_blocks(blocks)
        for idx, result in enumerate(results):
            self.assertEqual(result['block_num'], blocks[idx])

    def test_get_blocks_no_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_blocks()

    def test_get_blocks_int_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_blocks(10)

    def test_get_blocks_string_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_blocks("10")

    def test_get_blocks_list_of_string_values(self):
        blocks = ["5", "10"]
        results = self.chainsync.get_blocks(blocks)
        for idx, result in enumerate(results):
            self.assertEqual(result['block_num'], int(blocks[idx]))

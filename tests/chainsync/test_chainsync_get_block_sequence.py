from test_base import ChainSyncBaseTestCase


class ChainSyncGetBlockSequenceTestCase(ChainSyncBaseTestCase):

    def test_get_block_sequence(self):
        blocks = [8, 9, 10]
        results = list(self.chainsync.get_block_sequence(8, 3))
        for idx, result in enumerate(results):
            self.assertEqual(result['block_num'], blocks[idx])
        self.assertEqual(len(results), 3)

    def test_get_block_sequence_string_value(self):
        blocks = [7, 8, 9, 10]
        results = list(self.chainsync.get_block_sequence('7', '4'))
        for idx, result in enumerate(results):
            self.assertEqual(result['block_num'], blocks[idx])
        self.assertEqual(len(results), 4)

    def test_get_block_sequence_no_start_block(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_block_sequence()

    def test_get_block_sequence_no_height(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_block_sequence(1)

from test_base import ChainSyncBaseTestCase


class ChainSyncGetBlockTestCase(ChainSyncBaseTestCase):

    def test_get_block(self):
        result = self.chainsync.get_block(1)
        self.assertEqual(result['block_num'], 1)

    def test_get_block_no_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_block()

    def test_get_block_string_value(self):
        result = self.chainsync.get_block("1")
        self.assertEqual(result['block_num'], 1)

from test_base import ChainSyncBaseTestCase

class ChainSyncGetBlockTestCase(ChainSyncBaseTestCase):

    def test_get_ops_in_block(self):
        results = self.chainsync.get_ops_in_block(1)
        for result in results:
            self.assertEqual(result['block_num'], 1)

    def test_get_ops_in_block_no_value(self):
        with self.assertRaises(TypeError) as context:
            self.chainsync.get_ops_in_block()

    def test_get_ops_in_block_string_value(self):
        results = self.chainsync.get_ops_in_block("1")
        for result in results:
            self.assertEqual(result['block_num'], 1)

from test_base import ChainSyncBaseTestCase


class ChainSyncGetStatusTestCase(ChainSyncBaseTestCase):

    def test_get_head_block(self):
        height = self.chainsync.get_head_block()
        # ensure it returns a number
        self.assertIsInstance(height, int)

    def test_get_head_block_with_status(self):
        height, status = self.chainsync.get_head_block(return_status=True)
        # ensure it returns a number
        self.assertIsInstance(height, int)
        # as well as a dict with the status
        self.assertIsInstance(status, dict)

    def test_get_head_block_mode_irreversible(self):
        head = self.chainsync.get_head_block()
        irreversible = self.chainsync.get_head_block(mode='irreversible')
        # Ensure they are both numbers
        self.assertIsInstance(head, int)
        self.assertIsInstance(irreversible, int)
        # These two values will likely never be the same
        self.assertTrue(head != irreversible)

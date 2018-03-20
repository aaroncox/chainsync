from chainsync import ChainSync

import unittest

class chainsyncBlocksTestCase(unittest.TestCase):
    def setUp(self):
        self.chainsync = ChainSync(endpoints=['https://api.steemitstage.com'])

    def test_endpoint_get_block(self):
        self.assertNotEqual(self.chainsync.get_block(1), None, msg='chainsync get_block returning `None`')

    def test_endpoint_get_status(self):
        status = self.chainsync.get_status()
        self.assertNotEqual(status, None, msg='chainsync get_status returning `None`')
        self.assertTrue(status['head_block_number'] > 0, msg='chainsync get_status[`head_block_number`] not valid')

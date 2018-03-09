from blocksync import Blocksync

import unittest

class blocksyncBlocksTestCase(unittest.TestCase):
    def setUp(self):
        self.blocksync = Blocksync(endpoints=['https://api.steemitstage.com'])

    def test_endpoint_get_block(self):
        self.assertNotEqual(self.blocksync.get_block(1), None, msg='blocksync get_block returning `None`')

    def test_endpoint_get_status(self):
        status = self.blocksync.get_status()
        self.assertNotEqual(status, None, msg='blocksync get_status returning `None`')
        self.assertTrue(status['head_block_number'] > 0, msg='blocksync get_status[`head_block_number`] not valid')

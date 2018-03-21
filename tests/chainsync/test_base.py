import unittest

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

class ChainSyncBaseTestCase(unittest.TestCase):
    def setUp(self):
        adapter = SteemAdapter(endpoints='https://api.steemit.com')
        self.chainsync = ChainSync(adapter=adapter)

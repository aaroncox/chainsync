from test_base import ChainSyncBaseTestCase

from datetime import datetime
from abc import ABC, abstractmethod

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

class ChainSyncYieldEventTestCase(ChainSyncBaseTestCase):

    def test_yield_event(self):
        what = 'foo'
        data = 'bar'
        tupled = self.chainsync.yield_event(what, data)
        result1, result2 = tupled
        self.assertEqual(result1, what)
        self.assertEqual(result2, data)

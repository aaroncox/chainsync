import unittest
import pytest

from chainsync import ChainSync


@pytest.mark.usefixtures("client")
class ChainSyncBaseTestCase(unittest.TestCase):
    def setUp(self):
        self.chainsync = ChainSync(adapter=self.adapter, retry=False)

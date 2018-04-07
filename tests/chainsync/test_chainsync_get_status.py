from test_base import ChainSyncBaseTestCase


class ChainSyncGetStatusTestCase(ChainSyncBaseTestCase):

    def test_get_status(self):
        result = self.chainsync.get_status()
        self.assertTrue('time' in result)

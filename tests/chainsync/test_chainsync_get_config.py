from test_base import ChainSyncBaseTestCase


class ChainSyncGetConfigTestCase(ChainSyncBaseTestCase):

    def test_get_config(self):
        result = self.chainsync.get_config()
        self.assertTrue('IS_TEST_NET' in result)

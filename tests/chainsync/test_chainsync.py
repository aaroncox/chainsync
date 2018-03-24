from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter


class ChainSyncMainTestCase(ChainSyncBaseTestCase):

    def test_main_debug_flag_default_false(self):
        print(self.chainsync.debug)
        self.assertEqual(self.chainsync.debug, False)

    def test_main_debug_flag_set_true(self):
        adapter = SteemAdapter()
        custom = ChainSync(adapter, debug=True)
        self.assertEqual(custom.debug, True)

    def test_main_debug_flag_set_false_from_adapter(self):
        adapter = SteemAdapter(debug=True)
        custom = ChainSync(adapter)
        self.assertEqual(custom.debug, False)

    def test_main_debug_flag_set_true_from_main_false_for_adapter(self):
        adapter = SteemAdapter(debug=False)
        # main debug flag should override adapter
        custom = ChainSync(adapter, debug=True)
        self.assertEqual(custom.debug, True)
        self.assertEqual(custom.adapter.debug, True)

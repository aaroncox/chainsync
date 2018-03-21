from test_base import ChainSyncBaseTestCase

from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

class ChainSyncMainTestCase(ChainSyncBaseTestCase):

    def test_main_debug_flag_default_false(self):
        print(self.chainsync.debug)
        self.assertEqual(self.chainsync.debug, False, msg='main default debug mode should be false')

    def test_main_debug_flag_set_true(self):
        adapter = SteemAdapter()
        custom = ChainSync(adapter, debug=True)
        self.assertEqual(custom.debug, True, msg='main debug mode when set should be true')

    def test_main_debug_flag_set_false_from_adapter(self):
        adapter = SteemAdapter(debug=True)
        custom = ChainSync(adapter)
        self.assertEqual(custom.debug, False, msg='main debug mode when set from adapter should be false')

    def test_main_debug_flag_set_true_from_main_false_for_adapter(self):
        adapter = SteemAdapter(debug=False)
        custom = ChainSync(adapter, debug=True) # main debug flag should override adapter
        self.assertEqual(custom.debug, True, msg='main debug mode should be set and override adapter')
        self.assertEqual(custom.adapter.debug, True, msg='main debug mode should be set and override adapter')

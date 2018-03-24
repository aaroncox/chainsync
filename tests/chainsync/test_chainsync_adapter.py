from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

import unittest


class ChainSyncAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.chainsync = ChainSync(adapter=SteemAdapter)

    def test_adapter_init_default_adapter(self):
        self.assertNotEqual(self.chainsync.adapter, None)

    def test_adapter_init_custom_adapter_custom_endpoint_no_endpoints(self):
        adapter = SteemAdapter()
        custom = ChainSync(adapter)
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8090')

    def test_adapter_init_custom_adapter_custom_endpoint_string(self):
        adapter = SteemAdapter(endpoints='http://localhost:8091')
        custom = ChainSync(adapter)
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8091')

    def test_adapter_init_custom_adapter_custom_endpoint_list(self):
        endpoints = ['http://localhost:8091', 'http://localhost:8090']
        adapter = SteemAdapter(endpoints=endpoints)
        custom = ChainSync(adapter)
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8091')
        self.assertEqual(custom.adapter.endpoints, endpoints)

    def test_adapter_debug_flag_default_false(self):
        self.assertEqual(self.chainsync.adapter.debug, False)

    def test_adapter_debug_flag_set_true(self):
        adapter = SteemAdapter(debug=True)
        custom = ChainSync(adapter)
        self.assertEqual(custom.adapter.debug, True)

    def test_adapter_debug_flag_set_true_from_main(self):
        adapter = SteemAdapter()
        custom = ChainSync(adapter, debug=True)
        self.assertEqual(custom.adapter.debug, True)

    def test_adapter_debug_flag_set_true_from_main_false_for_adapter(self):
        adapter = SteemAdapter(debug=False)
        # main debug flag should override adapter
        custom = ChainSync(adapter, debug=True)
        self.assertEqual(custom.adapter.debug, True)

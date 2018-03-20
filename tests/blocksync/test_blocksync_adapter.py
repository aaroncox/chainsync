from chainsync import ChainSync
from chainsync.adapters.steem import SteemAdapter

import unittest

class chainsyncAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.chainsync = ChainSync()

    def test_adapter_init_default_adapter(self):
        self.assertNotEqual(self.chainsync.adapter, None, msg='adapter should initialize with a default')

    def test_adapter_init_custom_adapter_init(self):
        custom = ChainSync(adapter=SteemAdapter())
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8090', msg='adapter endpoint init value invalid')

    def test_adapter_init_custom_adapter_custom_endpoint_string(self):
        custom = ChainSync(adapter=SteemAdapter('http://localhost:8091'))
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8091', msg='adapter endpoint custom endpoint string not set correctly')

    def test_adapter_init_custom_adapter_custom_endpoint_list(self):
        custom = ChainSync(adapter=SteemAdapter(endpoints=['http://localhost:8091']))
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8091', msg='adapter endpoint custom endpoint list not set correctly')

    def test_adapter_endpoint_init(self):
        self.assertEqual(self.chainsync.adapter.endpoint, 'http://localhost:8090', msg='adapter endpoint init value invalid')

    def test_adapter_endpoint_init_invalid_string(self):
        custom = ChainSync(endpoints='')
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8090', msg='adapter endpoint init value invalid')

    def test_adapter_endpoint_init_invalid_list(self):
        custom = ChainSync(endpoints=[])
        self.assertEqual(custom.adapter.endpoint, 'http://localhost:8090', msg='adapter endpoint init value invalid')

    def test_adapter_endpoint(self):
        custom = ChainSync(endpoints='http://127.0.0.1:8090')
        self.assertEqual(custom.adapter.endpoint, 'http://127.0.0.1:8090', msg='adapter endpoint invalid')

    def test_adapter_endpoint_list(self):
        custom = ChainSync(endpoints=['http://127.0.0.1:8090','http://127.0.0.1:8091'])
        self.assertEqual(custom.adapter.endpoint, 'http://127.0.0.1:8090', msg='adapter endpoint list invalid')

    def test_adapter_endpoints_init(self):
        self.assertEqual(self.chainsync.adapter.endpoints, ['http://localhost:8090'], msg='adapter endpoints init value invalid')

    def test_adapter_endpoints(self):
        custom = ChainSync(endpoints='http://127.0.0.1:8090')
        self.assertEqual(custom.adapter.endpoints, ['http://127.0.0.1:8090'], msg='adapter endpoints invalid')

    def test_adapter_endpoints_list(self):
        custom = ChainSync(['http://127.0.0.1:8090','http://127.0.0.1:8091'])
        self.assertEqual(custom.adapter.endpoints, ['http://127.0.0.1:8090','http://127.0.0.1:8091'], msg='adapter endpoints list invalid')

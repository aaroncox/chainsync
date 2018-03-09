from blocksync.adapters.abstract import AbstractAdapter
from blocksync.adapters.base import BaseAdapter

from jsonrpcclient.http_client import HTTPClient
from jsonrpcclient.request import Request
from jsonrpcclient import config
config.validate = False

class SteemAdapter(AbstractAdapter, BaseAdapter):

    def get_block(self, block_num):
        response = HTTPClient(self.endpoint).request('block_api.get_block', block_num=block_num)
        if 'block_id' in response:
            response['height'] = int(str(response['block_id'])[:8], base=16)
        return response['block']

    def get_blocks(self, start_block=1, blocks=10):
        requests = [Request('block_api.get_block', block_num=i) for i in range(start_block, start_block + blocks)]
        response = HTTPClient(self.endpoint).send(requests)
        return [dict(r['result']['block'], **{'height': int(str(r['result']['block']['block_id'])[:8], base=16)}) for r in response]

    def get_status(self):
        return HTTPClient(self.endpoint).request('database_api.get_dynamic_global_properties')

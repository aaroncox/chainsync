from datetime import datetime

from blocksync.adapters.abstract import AbstractAdapter
from blocksync.adapters.base import BaseAdapter
from blocksync.utils.http_client import HttpClient

from jsonrpcclient.request import Request

class SteemV2Adapter(AbstractAdapter, BaseAdapter):

    config = {
        'BLOCK_INTERVAL': 'STEEM_BLOCK_INTERVAL'
    }

    def opData(self, block, opType, opData):
        # Add some useful context to the operation
        opData['block_num'] = block['block_num']
        opData['operation_type'] = opType
        opData['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%dT%H:%M:%S')
        if 'transaction_ids' in block:
            opData['transaction_id'] = block['transaction_ids'][i]
        return opData

    def get_block(self, block_num):
        response = HttpClient(self.endpoint).request('block_api.get_block', block_num=block_num)
        if 'block_id' in response:
            response['block_num'] = int(str(response['block_id'])[:8], base=16)
        print(response)
        return response['block']

    def get_blocks(self, start_block=1, blocks=10):
        requests = [Request('block_api.get_block', block_num=i) for i in range(start_block, start_block + blocks)]
        response = HttpClient(self.endpoint).send(requests)
        for r in response:
            if 'result' not in r:
                print(r)
            if 'result' in r and 'block' not in r['result']:
                print(r)
        return [dict(r['result']['block'], **{'block_num': int(str(r['result']['block']['block_id'])[:8], base=16)}) for r in response]

    def get_config(self):
        return HttpClient(self.endpoint).request('database_api.get_config')

    def get_methods(self):
        return HttpClient(self.endpoint).request('get_methods')

    def get_status(self):
        return HttpClient(self.endpoint).request('database_api.get_dynamic_global_properties')

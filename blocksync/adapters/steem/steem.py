from datetime import datetime

from blocksync.adapters.abstract import AbstractAdapter
from blocksync.adapters.base import BaseAdapter
from blocksync.utils.http_client import HttpClient

from jsonrpcclient.request import Request

class SteemAdapter(AbstractAdapter, BaseAdapter):

    config = {
        'BLOCK_INTERVAL': 'STEEMIT_BLOCK_INTERVAL'
    }

    def opData(self, block, opType, opData, txIndex=False):
        # Add some useful context to the operation
        opData['block_num'] = block['block_num']
        opData['operation_type'] = opType
        if not isinstance(block['timestamp'], datetime):
            opData['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%dT%H:%M:%S')
        opData['transaction_id'] = block['transaction_ids'][txIndex]
        return opData

    def get_block(self, block_num):
        response = HttpClient(self.endpoint).request('get_block', [block_num])
        if 'block_id' in response:
            response['block_num'] = int(str(response['block_id'])[:8], base=16)
        return response

    def get_blocks(self, start_block=1, blocks=10):
        for i in range(start_block, start_block + blocks):
            yield self.get_block(i)

    def get_config(self):
        return HttpClient(self.endpoint).request('get_config')

    def get_methods(self):
        return []

    def get_status(self):
        return HttpClient(self.endpoint).request('get_dynamic_global_properties')

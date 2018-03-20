from datetime import datetime

from chainsync.adapters.abstract import AbstractAdapter
from chainsync.adapters.base import BaseAdapter
from chainsync.utils.http_client import HttpClient

from jsonrpcclient.request import Request

class DecentAdapter(AbstractAdapter, BaseAdapter):

    config = {
        'BLOCK_INTERVAL': 'GRAPHENE_DEFAULT_BLOCK_INTERVAL'
    }

    def opData(self, block, opType, opData, txIndex=False):
        # Add some useful context to the operation
        opData['block_num'] = block['block_num']
        opData['operation_type'] = opType
        opData['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%dT%H:%M:%S')
        return opData

    def get_block(self, block_num):
        response = HttpClient(self.endpoint).request('get_block', [block_num])
        response['block_num'] = block_num
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

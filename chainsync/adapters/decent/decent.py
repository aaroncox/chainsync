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
        opData['timestamp'] = block['timestamp']
        # opData['transaction_id'] = block['transaction_ids'][txIndex]
        return opData

    def vOpData(self, vop):
        # Extract the operation from the vop object format
        opType, opData = vop
        # Add some useful context to the operation
        opData['block_num'] = opData['block']
        opData['operation_type'] = opType
        opData['timestamp'] = opData['timestamp']
        # opData['transaction_id'] = vop['trx_id']
        return opData

    def get_block(self, block_num):
        response = HttpClient(self.endpoint).request('get_block', [block_num])
        response['block_num'] = block_num
        return response

    def get_blocks(self, blocks):
        for i in blocks:
            yield self.call('get_block', block_num=int(i))

    def get_ops_in_block(self, block_num, virtual_only=False):
        block = self.call('get_block', block_num=block_num)
        for tx in block['transactions']:
            for op in tx['operations']:
                op[1]['block'] = block_num
                op[1]['timestamp'] = block['timestamp']
                yield op

    def get_ops_in_blocks(self, blocks, virtual_only=False):
        for i in blocks:
            yield self.call('get_ops_in_block', block_num=i, virtual_only=virtual_only)

    def get_config(self):
        return HttpClient(self.endpoint).request('get_config')

    def get_methods(self):
        return 'NOT_SUPPORTED'

    def get_status(self):
        return HttpClient(self.endpoint).request('get_dynamic_global_properties')

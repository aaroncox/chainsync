from datetime import datetime

from chainsync.adapters.abstract import AbstractAdapter
from chainsync.adapters.base import BaseAdapter
from chainsync.utils.http_client import HttpClient

from jsonrpcclient.request import Request

class SteemAdapter(AbstractAdapter, BaseAdapter):

    config = {
        'BLOCK_INTERVAL': 'STEEMIT_BLOCK_INTERVAL',
        'VIRTUAL_OPS': [
            'fill_convert_request',
            'author_reward',
            'curation_reward',
            'comment_reward',
            'liquidity_reward',
            'interest',
            'fill_vesting_withdraw',
            'fill_order',
            'shutdown_witness',
            'fill_transfer_from_savings',
            'hardfork',
            'comment_payout_update',
            'return_vesting_delegation',
            'comment_benefactor_reward',
            'producer_reward',
        ]
    }

    def opData(self, block, opType, opData, txIndex=False):
        # Ensure the format of the timestamp as a datetime
        if not isinstance(block['timestamp'], datetime):
            opData['timestamp'] = datetime.strptime(block['timestamp'], '%Y-%m-%dT%H:%M:%S')
        else:
            opData['timestamp'] = block['timestamp']
        # Add some useful context to the operation
        opData['block_num'] = block['block_num']
        opData['operation_type'] = opType
        opData['transaction_id'] = block['transaction_ids'][txIndex]
        return opData

    def vOpData(self, vop):
        # Extract the operation from the vop object format
        opType, opData = vop['op']

        # Ensure the format of the timestamp as a datetime
        if not isinstance(vop['timestamp'], datetime):
            opData['timestamp'] = datetime.strptime(vop['timestamp'], '%Y-%m-%dT%H:%M:%S')
        else:
            opData['timestamp'] = vop['timestamp']

        # Add some useful context to the operation
        opData['block_num'] = vop['block']
        opData['operation_type'] = opType
        opData['transaction_id'] = vop['trx_id']
        return opData

    def get_block(self, block_num):
        response = HttpClient(self.endpoint).request('get_block', [block_num])
        try:
            response['block_num'] = int(str(response['block_id'])[:8], base=16)
            response['timestamp'] = datetime.strptime(response['timestamp'], '%Y-%m-%dT%H:%M:%S')
        except KeyError as e:
            print(e)
            print(response)
        return response

    def get_ops_in_block(self, block_num, virtual_only=False):
        return HttpClient(self.endpoint).request('get_ops_in_block', [block_num, virtual_only])

    def get_ops_in_blocks(self, start_block=1, virtual_only=False, blocks=10):
        for i in range(start_block, start_block + blocks):
            yield self.call('get_ops_in_block', block_num=i, virtual_only=virtual_only)

    def get_blocks(self, blocks=[]):
        for i in blocks:
            yield self.call('get_block', block_num=i)

    def get_config(self):
        return HttpClient(self.endpoint).request('get_config')

    def get_methods(self):
        return 'NOT_SUPPORTED'

    def get_status(self):
        return HttpClient(self.endpoint).request('get_dynamic_global_properties')

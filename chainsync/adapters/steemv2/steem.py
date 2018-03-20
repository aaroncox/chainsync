from datetime import datetime

from chainsync.adapters.abstract import AbstractAdapter
from chainsync.adapters.base import BaseAdapter
from chainsync.utils.http_client import HttpClient

from jsonrpcclient.request import Request

class SteemV2Adapter(AbstractAdapter, BaseAdapter):

    config = {
        'BLOCK_INTERVAL': 'STEEM_BLOCK_INTERVAL',
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

    def formatDate(self, ts):
        return datetime(int(ts[:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13]), int(ts[14:16]), int(ts[17:19]))

    def opData(self, block, opType, opData, txIndex=False):
        # Ensure the format of the timestamp as a datetime
        opData['timestamp'] = self.formatDate(block['timestamp'])
        # Add some useful context to the operation
        opData['block_num'] = block['block_num']
        opData['operation_type'] = opType
        opData['transaction_id'] = block['transaction_ids'][txIndex]
        return opData

    def vOpData(self, vop):
        # Extract the operation from the vop object
        opType, opData = vop['op']
        # Ensure the format of the timestamp as a datetime
        opData['timestamp'] = self.formatDate(vop['timestamp'])
        # Add some useful context to the operation
        opData['block_num'] = vop['block']
        opData['operation_type'] = opType
        opData['transaction_id'] = vop['trx_id']
        return opData

    def is_api_available(self, api, method, raiseException=True):
        if api not in self.apis:
            if raiseException:
                raise Exception('endpoint not capable of calling {}.{} ({} not available)'.format(api, method, api))
            else:
                return False
        return True

    def get_block(self, block_num):
        # block_api method
        api = 'block_api'
        method = 'get_block'
        # ensure the API is available
        if self.is_api_available(api, method):
            response = HttpClient(self.endpoint).request('.'.join([api, method]), block_num=block_num)
            response['block']['block_num'] = int(str(response['block']['block_id'])[:8], base=16)
            return response['block']

    def get_ops_in_block(self, block_num, virtual_only=False):
        if self.is_api_available('account_history_api', 'get_ops_in_block', raiseException=False):
            return self.get_ops_in_block_from_account_history_api(block_num=block_num, virtual_only=virtual_only)
        elif self.is_api_available('condenser_api', 'get_ops_in_block', raiseException=False):
            return self.get_ops_in_block_from_condenser_api(block_num=block_num, virtual_only=virtual_only)
        else:
            raise Exception('endpoint not capable of calling get_ops_in_block from either condenser_api or account_history_api')

    def get_ops_in_block_from_account_history_api(self, block_num, virtual_only=False):
        # account_history_api method
        api = 'account_history_api'
        method = 'get_ops_in_block'
        response = HttpClient(self.endpoint).request('.'.join([api, method]), {
            'block_num': block_num,
            'only_virtual': virtual_only
        })
        return response['ops']

    def get_ops_in_block_from_condenser_api(self, block_num, virtual_only=False):
        # condenser_api method
        api = 'condenser_api'
        method = 'get_ops_in_block'
        response = HttpClient(self.endpoint).request('.'.join([api, method]), [
            block_num,
            virtual_only
        ])
        return response

    def get_ops_in_blocks(self, start_block=1, virtual_only=False, blocks=10):
        if self.is_api_available('account_history_api', 'get_ops_in_block', raiseException=False):
            return self.get_ops_in_blocks_from_account_history_api(start_block=start_block, virtual_only=virtual_only, blocks=blocks)
        elif self.is_api_available('condenser_api', 'get_ops_in_block', raiseException=False):
            return self.get_ops_in_blocks_from_condenser_api(start_block=start_block, virtual_only=virtual_only, blocks=blocks)
        else:
            raise Exception('endpoint not capable of calling get_ops_in_block from either condenser_api or account_history_api')

    def get_ops_in_blocks_from_account_history_api(self, start_block=1, virtual_only=False, blocks=10):
        # account_history_api method
        api = 'account_history_api'
        method = 'get_ops_in_block'
        # assemble list with multiple requests for batch
        requests = [
            Request('.'.join([api, method]), {
                'block_num': i,
                'only_virtual': virtual_only
            }) for i in range(start_block, start_block + blocks)
        ]
        # get response
        response = HttpClient(self.endpoint).send(requests)
        # return the resulting ops
        return [r['result']['ops'] for r in response]

    def get_ops_in_blocks_from_condenser_api(self, start_block=1, virtual_only=False, blocks=10):
        # condenser_api method
        api = 'condenser_api'
        method = 'get_ops_in_block'
        # assemble list with multiple requests for batch
        requests = [
            Request('.'.join([api, method]), [
                i,
                virtual_only
            ]) for i in range(start_block, start_block + blocks)
        ]
        # get response
        response = HttpClient(self.endpoint).send(requests)
        # return the resulting ops
        return [r['result'] for r in response]

    def get_blocks(self, blocks=[]):
        # block_api method
        api = 'block_api'
        method = 'get_block'
        if self.is_api_available(api, method):
            # assemble list with multiple requests for batch
            requests = [
                Request('.'.join([api, method]), {
                    'block_num': i
                }) for i in blocks
            ]
            # get response
            response = HttpClient(self.endpoint).send(requests)
            # return the resulting block of each result
            return [dict(r['result']['block'], **{'block_num': int(str(r['result']['block']['block_id'])[:8], base=16)}) for r in response]

    def get_config(self):
        # database_api method
        api = 'database_api'
        method = 'get_config'
        if self.is_api_available(api, method):
            return HttpClient(self.endpoint).request('.'.join([api, method]))

    def get_methods(self):
        # jsonrpc method
        api = 'jsonrpc'
        method = 'get_methods'
        return HttpClient(self.endpoint).request('.'.join([api, method]))

    def get_status(self):
        # database_api method
        api = 'database_api'
        method = 'get_dynamic_global_properties'
        if self.is_api_available(api, method):
            return HttpClient(self.endpoint).request('.'.join([api, method]))

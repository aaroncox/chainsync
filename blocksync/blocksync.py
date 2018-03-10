import time

from blocksync.adapters.steem import SteemAdapter

class Blocksync():

    def __init__(self, endpoints=['http://localhost:8090'], adapter=None, debug=False):
        self.debug = debug
        if adapter:
            self.adapter = adapter
        else:
            self.adapter = SteemAdapter(endpoints, debug)

    def get_block(self, block_num):
        return self.adapter.call('get_block', block_num=block_num)

    def get_blocks(self, start_block, blocks=10):
        return self.adapter.call('get_blocks', start_block=start_block, blocks=blocks)

    def get_status(self):
        return self.adapter.call('get_status')

    def get_block_stream(self, start_block=None, mode='head', batch_size=10):
        while True:
            status = self.get_status()
            # Determine the current head block
            head_block = status['head_block_number']
            # If set to irreversible, override the head block
            if mode == 'irreversible':
                head_block = status['last_irreversible_block_num']
            # If no start block is specified, start streaming from head
            if start_block is None:
                start_block = head_block
            # Set initial remaining blocks for this stream
            remaining = head_block - start_block
            # While remaining blocks exist - batch load them
            while remaining > 0:
                # Remaining blocks to process
                remaining = head_block - start_block
                # Determine how many blocks to load with this request
                blocks = batch_size
                # Modify the amount of blocks to load if lower than the batch_size
                if remaining < batch_size:
                    blocks = remaining
                # Iterate batch of blocks
                for block in self.get_blocks(start_block, blocks=blocks):
                    # Yield block data
                    yield block
                    # Update the height to start on the next unyielded block
                    start_block = block['block_num'] + 1
            # Pause loop for block time
            time.sleep(3)

    def get_ops_stream(self, start_block=None, mode='head', batch_size=10, ops_whitelist=[]):
        # Stream blocks using the parameters passed to the op stream
        for block in self.get_block_stream(start_block=start_block, mode=mode, batch_size=batch_size):
            # Loop through all transactions within this block
            for i, tx in enumerate(block['transactions']):
                # If a whitelist is defined, only allow whitelisted operations through
                ops = (op for op in tx['operations'] if not ops_whitelist or op[0] in ops_whitelist)
                for opType, opData in ops:
                    # Add some useful context to the operation
                    opData['block_num'] = block['block_num']
                    opData['operation_type'] = opType
                    opData['timestamp'] = block['timestamp']
                    opData['transaction_id'] = block['transaction_ids'][i]
                    # Yield op data
                    yield opData

import time

class ChainSync():

    def __init__(self, adapter, endpoints=['http://localhost:8090'], retry=True, debug=False):
        self.debug = debug
        if adapter:
            self.adapter = adapter
        else:
            raise Exception('adapter required: you must specify a adapter')

    def get_block(self, block_num):
        """Get a list of usernames from all registered accounts.

        Args:
            after (str, int): Username to start with. If '', 0 or -1, it will start at beginning.
            limit (int): How many results to return.

        Returns:
            list: List of usernames in requested chunk.

        """
        return self.adapter.call('get_block', block_num=block_num)

    def get_blocks(self, blocks=[]):
        return self.adapter.call('get_blocks', blocks=blocks)

    def get_block_sequence(self, start_block=1, limit=10):
        return self.adapter.call('get_blocks', blocks=range(start_block, start_block + limit))

    def get_config(self):
        return self.adapter.call('get_config')

    def get_status(self):
        return self.adapter.call('get_status')

    def get_ops_in_block(self, block_num, virtual_only=False):
        return self.adapter.call('get_ops_in_block', block_num=block_num, virtual_only=virtual_only)

    def get_ops_in_blocks(self, start_block, virtual_only=False, blocks=10):
        return self.adapter.call('get_ops_in_blocks', start_block=start_block, virtual_only=virtual_only, blocks=blocks)

    # returns a stream of blocks
    def get_block_stream(self, start_block=None, mode='head', batch_size=10):
        config = self.get_config()
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
                # Determine how many blocks to load with this request
                limit = batch_size
                # Modify the amount of blocks to load if lower than the batch_size
                if remaining < batch_size:
                    limit = remaining
                # Iterate batch of blocks
                for block in self.get_block_sequence(start_block=start_block, limit=limit):
                    # Update the height to start on the next unyielded block
                    start_block = block['block_num'] + 1
                    # Yield block data
                    yield block
                # Remaining blocks to process
                remaining = head_block - start_block

            # Pause loop based on the blockchain block time
            block_interval = config[self.adapter.config['BLOCK_INTERVAL']] if 'BLOCK_INTERVAL' in self.adapter.config else 3
            time.sleep(block_interval)

    # returns a stream of ops
    def get_op_stream(self, start_block=None, mode='head', batch_size=10, virtual_ops=True, virtual_only=False, whitelist=[]):
        config = self.get_config()

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
                # Determine how many blocks to load with this request
                blocks = batch_size

                # Modify the amount of blocks to load if lower than the batch_size
                if remaining < batch_size:
                    blocks = remaining

                # Track the last block successfully processed
                last_block_processed = start_block

                if virtual_ops:
                    # Iterate batch of blocks
                    for response in self.get_ops_in_blocks(start_block, virtual_only=virtual_only, blocks=blocks):
                        for op in self.get_ops_from_ops_in_block(response, whitelist=whitelist):

                            last_block_processed = op['block_num']
                            # Yield block data
                            yield op

                else:
                    # Stream blocks using the parameters passed to the op stream
                    for block in self.get_block_stream(start_block=start_block, mode=mode, batch_size=batch_size):
                        for op in self.get_ops_from_block(block, virtual_ops=False, whitelist=whitelist):
                            last_block_processed = op['block_num']
                            yield op

                # Remaining blocks to process
                remaining = head_block - start_block

                # Next block to start on
                if remaining > batch_size:
                    start_block = start_block + batch_size
                else:
                    start_block = last_block_processed + 1

            # Pause loop based on the blockchain block time
            block_interval = config[self.adapter.config['BLOCK_INTERVAL']] if 'BLOCK_INTERVAL' in self.adapter.config else 3
            time.sleep(block_interval)


    def get_ops_from_ops_in_block(self, data, whitelist=[]):
        for op in (op for op in data if not whitelist or op['op'][0] in whitelist):
            yield self.adapter.vOpData(op)

    def get_ops_from_block(self, block, virtual_ops=True, virtual_only=False, whitelist=[]):
        if not virtual_only:
            # Loop through all transactions within this block
            for txIndex, tx in enumerate(block['transactions']):
                # If a whitelist is defined, only allow whitelisted operations through
                ops = (op for op in tx['operations'] if not whitelist or op[0] in whitelist)
                # Iterate and yield each op
                for opType, opData in ops:
                    yield self.adapter.opData(block, opType, opData, txIndex=txIndex)

        # Ensure virtual_ops should be queried, and if a whitelist exists, check to ensure we're looking for vops
        if virtual_ops and (not whitelist or [i for i in whitelist if i in self.adapter.config['VIRTUAL_OPS']]):
            # Retrieve and loop through all virtual operations within this block
            for vop in self.get_ops_in_block(block['block_num'], True):
                # If a whitelist is defined, only allow whitelisted operations through
                if not whitelist or vop['op'][0] in whitelist:
                    yield self.adapter.vOpData(vop)

    # returns a stream of blocks and ops, in a tuple of ('type', 'data')
    def get_blockop_stream(self, start_block=None, mode='head', batch_size=10, virtual_ops=True, virtual_only=False, whitelist=[]):
        # Stream blocks using the parameters passed to the op stream
        for block in self.get_block_stream(start_block=start_block, mode=mode, batch_size=batch_size):
            yield ('block', block)
            for op in self.get_ops_from_block(block, virtual_ops=virtual_ops, virtual_only=virtual_only, whitelist=whitelist):
                yield ('op', op)

import time
from collections import Counter

class ChainSync():

    def __init__(self, adapter, endpoints=['http://localhost:8090'], retry=True, debug=False):
        self.debug = debug
        if adapter:
            if debug:
                adapter.debug = debug
            self.adapter = adapter
        else:
            raise Exception('adapter required: you must specify a adapter')

    def get_config(self):
        return self.adapter.call('get_config')

    def get_status(self):
        return self.adapter.call('get_status')

    def get_head_block(self, mode='head'):
        # get status from the blockchain
        status = self.get_status()

        # determine the current head block
        head_block = status[self.adapter.config['HEAD_BLOCK_NUMBER']]

        # If set to irreversible, override the head block
        if mode == 'irreversible':
            head_block = status[self.adapter.config['LAST_IRREVERSIBLE_BLOCK_NUM']]

        return head_block

    def get_block(self, block_num):
        return self.adapter.call('get_block', block_num=block_num)

    def get_blocks(self, blocks):
        if not isinstance(blocks, list):
            raise TypeError
        return self.adapter.call('get_blocks', blocks=blocks)

    def get_block_sequence(self, start_block=1, limit=10):
        yield from self.get_blocks(list(range(start_block, start_block + limit)))

    def get_ops_in_block(self, block_num, virtual_only=False, whitelist=[]):
        for vop in self.adapter.call('get_ops_in_block', block_num=block_num, virtual_only=virtual_only):
            if not whitelist or vop['op'][0] in whitelist:
                yield self.adapter.format_op_from_get_ops_in_block(vop)

    def get_ops_in_blocks(self, blocks, virtual_only=False, whitelist=[]):
        if not isinstance(blocks, list):
            raise TypeError
        for data in self.adapter.call('get_ops_in_blocks', blocks=blocks, virtual_only=virtual_only):
            for op in data:
                if not whitelist or op['op'][0] in whitelist:
                    yield self.adapter.format_op_from_get_ops_in_block(op)

    def get_ops_in_block_sequence(self, start_block=1, limit=10, virtual_only=False, whitelist=[]):
        yield from self.get_ops_in_blocks(list(range(start_block, start_block + limit)), virtual_only=virtual_only, whitelist=whitelist)

    def get_ops_in_transaction(self, transaction_id):
        if not isinstance(transaction_id, str):
            raise TypeError
        transaction = self.adapter.call('get_transaction', transaction_id=transaction_id)
        for op in transaction['operations']:
            yield self.adapter.format_op_from_get_transaction(transaction, op)

    def get_ops_in_transactions(self, transaction_ids):
        if not isinstance(transaction_ids, list):
            raise TypeError
        for transaction in self.adapter.call('get_transactions', transaction_ids=transaction_ids):
            for op in transaction['operations']:
                yield self.adapter.format_op_from_get_transaction(transaction, op)

    def get_transaction(self, transaction_id):
        if not isinstance(transaction_id, str):
            raise TypeError
        return self.adapter.call('get_transaction', transaction_id=transaction_id)

    def get_transactions(self, transaction_ids):
        if not isinstance(transaction_ids, list):
            raise TypeError
        yield from self.adapter.call('get_transactions', transaction_ids=transaction_ids)

    def from_block_get_ops(self, block, virtual_ops=False, regular_ops=True, whitelist=[]):
        # ensure regular_ops should be yielded
        if regular_ops:
            # Loop through all transactions within this block
            for txIndex, tx in enumerate(block['transactions']):
                # If a whitelist is defined, only allow whitelisted operations through
                ops = (op for op in tx['operations'] if not whitelist or op[0] in whitelist)
                # Iterate and yield each op
                for opType, opData in ops:
                    yield self.adapter.opData(block, opType, opData, txIndex=txIndex)

        # ensure virtual_ops should be yielded
        if virtual_ops:
            # query and yield all virtual operations within this block
            yield from self.get_ops_in_block(block['block_num'], True, whitelist=whitelist)

    def stream(self, what=['ops', 'blocks', 'ops_per_blocks'], start_block=None, end_block=None, mode='head', batch_size=10, virtual_ops=True, regular_ops=True, whitelist=[]):

        config = self.get_config()

        while True:

            end_block = self.get_head_block(mode)

            # If no start block is specified, start streaming from head
            if start_block is None:
                start_block = end_block

            last_block_processed = start_block - 1

            for dataType, data in self.get_stream(
                config=None,
                what=what,
                start_block=start_block,
                end_block=end_block,
                mode=mode,
                batch_size=batch_size,
                virtual_ops=virtual_ops,
                regular_ops=regular_ops,
                whitelist=whitelist
            ):
                # Track the last block successfully processed
                if dataType in ['op', 'block']:
                    last_block_processed = data['block_num']

                yield (dataType, data)

            # If remaining > batch_size, increment by batch size
            if (end_block - start_block) > batch_size:
                start_block = start_block + batch_size
            else:
                # else start on the next block
                start_block = last_block_processed + 1
            # Pause the loop for based on an estimated time the next block will arrive
            time.sleep(self.get_approx_sleep_until_block(throttle, config, status['time']))

    def get_approx_sleep_until_block(self, throttle, config, ts):
        # Get the rate the blockchain generates blocks
        block_interval = config[self.adapter.config['BLOCK_INTERVAL']] if 'BLOCK_INTERVAL' in self.adapter.config else 3

        # Interpret the datetime string passed from the last status
        blockchain_time = datetime(int(ts[:4]), int(ts[5:7]), int(ts[8:10]), int(ts[11:13]), int(ts[14:16]), int(ts[17:19]))

        # Determine how long it's been since that last block
        current_time = datetime.utcnow()
        since_last_block = current_time.timestamp() - blockchain_time.timestamp()

        # Add a delay based on when the next block is expected
        if since_last_block < block_interval:
            return block_interval - since_last_block
        else:
            # Otherwise add the throttle delay (defaults to 1 second) delay to avoid thrashing the API
            return throttle

    def get_stream(self, what=['blocks', 'config', 'status', 'ops', 'ops_per_blocks'], config=None, start_block=None, end_block=None, mode='head', batch_size=10, virtual_ops=True, regular_ops=True, whitelist=[]):

        if not config:
            config = self.get_config()

        if not end_block:
            end_block = start_block

        last_block_processed = start_block

        # While remaining blocks exist - batch load them
        while start_block <= end_block:
            last_block_processed = start_block

            # Determine how many blocks to load with this request
            limit = end_block - start_block + 1 if (end_block - start_block + 1) < batch_size else batch_size

            # Track how many operations are in each block
            ops_per_blocks = []

            if 'blocks' in what:
                for block in self.get_block_sequence(start_block, limit=limit):
                    last_block_processed = block['block_num']
                    yield ('block', block)
                    if 'ops' in what:
                        for op in self.from_block_get_ops(block, virtual_ops=virtual_ops, regular_ops=regular_ops, whitelist=whitelist):
                            ops_per_blocks.append(op['block_num'])
                            yield ('op', op)

            elif 'ops' in what:
                if virtual_ops or (regular_ops and virtual_ops):
                    for op in self.get_ops_in_block_sequence(start_block, limit=limit, virtual_only=not regular_ops, whitelist=whitelist):
                        last_block_processed = op['block_num']
                        ops_per_blocks.append(op['block_num'])
                        yield ('op', op)

                elif regular_ops:
                    for block in self.get_block_sequence(start_block, limit=limit):
                        last_block_processed = block['block_num']
                        for op in self.from_block_get_ops(block, virtual_ops=virtual_ops, regular_ops=regular_ops, whitelist=whitelist):
                            ops_per_blocks.append(op['block_num'])
                            yield ('op', op)


            if 'ops_per_blocks' in what:
                yield ('ops_per_block', Counter(ops_per_blocks))

            # else start on the next block
            start_block = last_block_processed + 1

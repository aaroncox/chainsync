import datetime
from chainsync import ChainSync
from chainsync.adapters.peerplays import PeerplaysAdapter

adapter = PeerplaysAdapter(endpoints=['http://45.79.220.16:8090/'])
chainsync = ChainSync(adapter)

print('\nGetting block 1')
block = chainsync.get_block(1)
print(block)

print('\nGetting blocks 1, 10, 50, 250, 500')
blocks = chainsync.get_blocks([1, 10, 50, 250, 500])
for block in blocks:
    print(block)

print('\nGetting blocks 1000-1005')
blocks = chainsync.get_block_sequence(1000, 5)
for block in blocks:
    print(block)

print('\nGetting all ops in block 92847...')
for op in chainsync.get_ops_in_block(92847):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting withdraw_vesting ops in block 92847...')
for op in chainsync.get_ops_in_block(92847, whitelist=['withdraw_vesting']):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting all ops in block 10000, 50000, and 20000...')
for op in chainsync.get_ops_in_blocks([10000, 50000, 20000]):
	print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nGetting producer_reward ops in block 10000, 50000, and 20000...')
for op in chainsync.get_ops_in_blocks([10000, 50000, 20000], whitelist=['producer_reward']):
	print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming blocks, 100 at a time, from the irreversible height...')
for dataType, block in chainsync.stream(['blocks'], batch_size=100, mode='irreversible'):
    print("{}: {} - {}".format(datetime.datetime.now(), block['block_num'], block['witness']))

print('\nStreaming all ops...')
for dataType, op in chainsync.stream(['ops']):
    print("{}: {} [{}] - {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type']))

print('\nStreaming all blocks + ops + virtual ops + accurate counts of ops per block...')
for dataType, data in chainsync.stream(['blocks', 'ops', 'ops_per_block'], start_block=1045177):
    dataHeader = "{} #{}: {}".format(datetime.datetime.now(), data['block_num'], dataType)
    if dataType == "op":
        print("{} {}".format(dataHeader, data['operation_type']))
    if dataType == "block":
        txCount = len(data['transactions'])
        opCount = sum([len(tx['operations']) for tx in data['transactions']])
        print("{} - #{} - tx: {} / ops: {}".format(dataHeader, data['block_num'], txCount, opCount))
    if dataType == "ops_per_block":
        for height in data:
            print("{} - #{}: {}".format(dataHeader, height, data[height]))

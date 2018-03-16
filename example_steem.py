import datetime
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

adapter = SteemAdapter(endpoints=['https://api.steemit.com'])
blocksync = Blocksync(adapter)

print('\nGetting block 1')
block = blocksync.get_block(1)
print(block)

print('\nGetting blocks 1-5')
blocks = blocksync.get_blocks(1, 5)
for block in blocks:
    print(block)

print('\nStreaming blocks...')
for block in blocksync.get_block_stream(batch_size=100, mode='irreversible'):
    print("{}: {} - {}".format(datetime.datetime.now(), block['block_num'], block['witness']))

print('\nStreaming all ops...')
for op in blocksync.get_op_stream():
    print("{}: {} - {}".format(datetime.datetime.now(), op['block_num'], op['operation_type']))

print('\nStreaming vote ops only...')
for op in blocksync.get_op_stream(whitelist=['vote']):
    print("{}: {} - {} by {}".format(datetime.datetime.now(), op['block_num'], op['operation_type'], op['voter']))

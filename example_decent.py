import datetime
from blocksync import Blocksync
from blocksync.adapters.decent import DecentAdapter
from blocksync.adapters.steem import SteemAdapter

a = DecentAdapter(endpoints=['http://api.decent-db.com:8090/'])
s = Blocksync(adapter=a, debug=True)

print('Getting block 1')
block = s.get_block(1)
print(block)

print('Getting blocks 1-5')
blocks = s.get_blocks(1, 5)
for block in blocks:
    print(block)

print('Streaming blocks...')
for block in s.get_block_stream(batch_size=100, mode='irreversible'):
    print("{}: {} - {}".format(datetime.datetime.now(), block['block_num'], block['miner']))

print('Streaming all ops...')
for op in s.get_op_stream():
    print("{}: {} - {}".format(datetime.datetime.now(), op['block_num'], op['operation_type']))

print('Streaming vote ops only...')
for op in s.get_op_stream(whitelist=['vote']):
    print("{}: {} - {} by {}".format(datetime.datetime.now(), op['block_num'], op['operation_type'], op['voter']))

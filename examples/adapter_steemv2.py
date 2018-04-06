import datetime

from chainsync import ChainSync
from chainsync.adapters.steemv2 import SteemV2Adapter

adapter = SteemV2Adapter(endpoints=['https://api.steemitstage.com/'])
chainsync = ChainSync(adapter)

def print_event(dataType, data):
    if dataType == "block":
        print("[{}]: {} [{}] - #{}, previous: {}".format(datetime.datetime.now(), dataType, data['block_id'], data['block_num'], data['previous']))
    if dataType == "op":
        print("[{}]: {} [{}] - {}".format(datetime.datetime.now(), dataType, data['transaction_id'], data['operation_type']))
    if dataType == "ops_per_block":
        for height in data:
            print("[{}]: {} - #{} had {} ops".format(datetime.datetime.now(), dataType, height, data[height]))
    if dataType == 'tx':
        print("[{}]: {} [{}] - {} ops".format(datetime.datetime.now(), dataType, data['transaction_id'], len(data['operations'])))
    if dataType == 'status':
        print("[{}]: {} - {} h:{} / i:{}".format(datetime.datetime.now(), dataType, data['time'], data['last_irreversible_block_num'], data['head_block_number']))

print('\nGetting block 1')
block = chainsync.get_block(1)
print_event('block', block)

print('\nGetting transaction c68435a34a7afc701771eb090f96526ed4c2a37b')
tx = chainsync.get_transaction('c68435a34a7afc701771eb090f96526ed4c2a37b')
print_event('tx', tx)

print('\nGetting multiple transactions')
transactions = [
    '62f68c45f67ecbe4ac6eb8348bce44e73e46611c',
    '2f58f00e70b8d0f88e90350043e17ed6ea2eb223',
    'c68435a34a7afc701771eb090f96526ed4c2a37b',
]
for tx in chainsync.get_transactions(transactions):
    print_event('tx', tx)

print('\nGetting ops in transaction c68435a34a7afc701771eb090f96526ed4c2a37b')
for op in chainsync.get_ops_in_transaction('c68435a34a7afc701771eb090f96526ed4c2a37b'):
    print_event('op', op)

print('\nGetting ops in multiple transactions')
transactions = [
    '62f68c45f67ecbe4ac6eb8348bce44e73e46611c',
    '2f58f00e70b8d0f88e90350043e17ed6ea2eb223',
    'c68435a34a7afc701771eb090f96526ed4c2a37b',
]
for op in chainsync.get_ops_in_transactions(transactions):
    print_event('op', op)

print('\nGetting blocks 1, 10, 50, 250, 500')
blocks = chainsync.get_blocks([1, 10, 50, 250, 500])
for block in blocks:
    print_event('block', block)

print('\nGetting blocks 1000-1005')
blocks = chainsync.get_block_sequence(1000, 5)
for block in blocks:
    print_event('block', block)

print('\nGetting all ops in block 9284729...')
for op in chainsync.get_ops_in_block(9284729):
    print_event('op', op)

print('\nGetting withdraw_vesting ops in block 9284729...')
for op in chainsync.get_ops_in_block(9284729, whitelist=['withdraw_vesting']):
    print_event('op', op)

print('\nGetting all ops in block 1000000, 5000000, and 2000000...')
for op in chainsync.get_ops_in_blocks([1000000, 5000000, 2000000]):
    print_event('op', op)

print('\nGetting producer_reward ops in block 1000000, 5000000, and 2000000...')
for op in chainsync.get_ops_in_blocks([1000000, 5000000, 2000000], whitelist=['producer_reward']):
    print_event('op', op)

print('\nStreaming blocks from head...')
for dataType, data in chainsync.stream(['blocks']):
    print_event(dataType, data)

print('\nStreaming blocks from the irreversible height...')
for dataType, data in chainsync.stream(['blocks'], mode='irreversible'):
    print_event(dataType, data)

print('\nStreaming status...')
for dataType, data in chainsync.stream(['status']):
    print_event(dataType, data)

print('\nStreaming ops_per_blocks...')
for dataType, data in chainsync.stream(['ops_per_blocks']):
    print_event(dataType, data)

print('\nStreaming blocks + status from head...')
for dataType, data in chainsync.stream(['blocks', 'status']):
    print_event(dataType, data)

print('\nStreaming all op from head...')
for dataType, data in chainsync.stream(['ops']):
    print_event(dataType, data)

print('\nStreaming all non-virtual ops...')
for dataType, data in chainsync.stream(['ops'], virtual_ops=False):
    print_event(dataType, data)

print('\nStreaming all virtual ops...')
for dataType, data in chainsync.stream(['ops'], regular_ops=False):
    print_event(dataType, data)

print('\nStreaming vote ops only...')
for dataType, op in chainsync.stream(['ops'], whitelist=['vote']):
    print("[{}]: {} [{}] - {} by {}".format(datetime.datetime.now(), op['block_num'], op['transaction_id'], op['operation_type'], op['voter']))

print('\nStreaming producer_reward virtual ops only...')
for dataType, op in chainsync.stream(['ops'], whitelist=['producer_reward']):
    print("[{}]: {} - {} for {} of {}".format(datetime.datetime.now(), op['block_num'], op['operation_type'], op['producer'], op['vesting_shares']))

print('\nStreaming all ops + status from head...')
for dataType, data in chainsync.stream(['ops', 'status']):
    print_event(dataType, data)

print('\nStreaming all blocks + ops (no virtual ops)...')
for dataType, data in chainsync.stream(['blocks', 'ops'], virtual_ops=False):
    print_event(dataType, data)

print('\nStreaming all blocks + ops (no virtual ops), filtering only votes...')
for dataType, data in chainsync.stream(['blocks', 'ops'], whitelist=['vote']):
    print_event(dataType, data)

print('\nStreaming all blocks + virtual ops (no normal ops)...')
for dataType, data in chainsync.stream(['blocks', 'ops'], regular_ops=False):
    print_event(dataType, data)

print('\nStreaming all blocks + virtual ops (no normal ops), filtering only producer_reward...')
for dataType, data in chainsync.stream(['blocks', 'ops'], regular_ops=False, whitelist=['producer_reward']):
    print_event(dataType, data)

print('\nStreaming all blocks + all ops + ops_per_blocks + status...')
for dataType, data in chainsync.stream(['blocks', 'ops', 'ops_per_blocks', 'status']):
    print_event(dataType, data)

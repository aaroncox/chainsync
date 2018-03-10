import datetime
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

print('Getting block 1')
block = s.get_block(1)
print(block)

print('Getting blocks 1-5')
blocks = s.get_blocks(1, 5)
for block in blocks:
    print(block)

print('Streaming blocks...')
for block in s.get_block_stream(batch_size=100, mode='irreversible'):
    print("{}: {} - {}".format(datetime.datetime.now(), block['block_num'], block['witness']))

## Blocksync

A simple library to stream blocks and operations for digesting into other mediums.

### Example - streaming blocks

```
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['height'], block['witness']))
```

### Example - custom adapter

A custom adapter can be supplied to allow parsing of a specific blockchain

```
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

a = SteemAdapter(endpoints=['https://api.steemitstage.com'])
s = Blocksync(adapter=a)

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['height'], block['witness']))
```

## Blocksync

A simple library to stream blocks and operations for digesting into other mediums.

#### Requirements

`pip install -r requirements.txt`

- [jsonrpcclient](https://github.com/bcb/jsonrpcclient)

### Example - streaming blocks

``` js
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['height'], block['witness']))
```

### Example - custom adapter

A custom adapter can be supplied to allow parsing of a specific blockchain

``` js
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

a = SteemAdapter(endpoints=['https://api.steemitstage.com'])
s = Blocksync(adapter=a)

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['height'], block['witness']))
```

## Adapters

Adapters can be added and configured to allow access to other similar blockchains.

#### Steem

The Steem blockchain adapter currently requires v0.19.4 of steemd - containing the new AppBase API layer. 

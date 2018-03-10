## Blocksync

A simple library to stream blocks and operations for digesting into other mediums.

#### Requirements

`pip install -r requirements.txt`

- [jsonrpcclient](https://github.com/bcb/jsonrpcclient)

### Example - streaming blocks

``` python
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['block_num'], block['witness']))
```

### Example - streaming operations

``` python
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for op in s.get_op_stream():
    print("{} - {}".format(op['block_num'], op['operation_type']))
```

### Example - streaming operations with a whitelist

``` python
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for op in s.get_op_stream(whitelist=['vote']):
    print("{} - {} by {}".format(op['block_num'], op['operation_type'], op['voter']))
```

### Example - custom adapter

A custom adapter can be supplied to allow parsing of a specific blockchain

``` python
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

a = SteemAdapter(endpoints=['https://api.steemitstage.com'])
s = Blocksync(adapter=a)

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['block_num'], block['witness']))
```

## Adapters

Adapters can be added and configured to allow access to other similar blockchains.

#### Steem

The Steem blockchain adapter currently requires v0.19.4 of steemd - containing the new AppBase API layer.

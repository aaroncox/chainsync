## Blocksync

A simple library to stream blocks and operations for digesting into other mediums.

#### Requirements

`pip install -r requirements.txt`

- [jsonrpcclient](https://github.com/bcb/jsonrpcclient)

### Example - streaming blocks

``` python
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

adapter = SteemAdapter(endpoints=['https://api.steemit.com'])
blocksync = Blocksync(adapter)

for block in blocksync.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['block_num'], block['witness']))
```

### Example - streaming operations

``` python
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

adapter = SteemAdapter(endpoints=['https://api.steemit.com'])
blocksync = Blocksync(adapter)

for op in blocksync.get_op_stream():
    print("{} - {}".format(op['block_num'], op['operation_type']))
```

### Example - streaming operations with a whitelist

``` python
from blocksync import Blocksync
from blocksync.adapters.steem import SteemAdapter

adapter = SteemAdapter(endpoints=['https://api.steemit.com'])
blocksync = Blocksync(adapter)

for op in blocksync.get_op_stream(whitelist=['vote']):
    print("{} - {} by {}".format(op['block_num'], op['operation_type'], op['voter']))
```

### Example - custom adapters

A custom adapter can be supplied to allow parsing of a specific blockchain

``` python
from blocksync import Blocksync
from blocksync.adapters.decent import DecentAdapter

adapter = DecentAdapter(endpoints=['http://api.decent-db.com:8090'])
blocksync = Blocksync(adapter)

for block in blocksync.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['block_num'], block['witness']))
```

## Adapters

Adapters can be added and configured to allow access to other similar blockchains.

A current list of adapters can be found in the `./blocksync/adapters` folder.

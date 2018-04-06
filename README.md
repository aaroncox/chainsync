## ChainSync

[![PyPI](https://img.shields.io/pypi/v/chainsync.svg)](https://github.com/aaroncox/chainsync)
[![GitHub issues](https://img.shields.io/github/issues/aaroncox/chainsync.svg)](https://github.com/aaroncox/chainsync/issues)
[![Build Status](https://travis-ci.org/aaroncox/chainsync.svg?branch=master)](https://travis-ci.org/aaroncox/chainsync)

A simple library to stream blocks and operations for digesting into other mediums.

### Install

`pip install chainsync`


#### Requirements

`pip install -r requirements.txt`

- [jsonrpcclient](https://github.com/bcb/jsonrpcclient)

### Example - streaming blocks

``` python
from chainsync import ChainSync
from chainsync.adapters.steemv2 import SteemV2Adapter

adapter = SteemV2Adapter(endpoints=['https://api.steemit.com'])
chainsync = ChainSync(adapter)

for dataType, data in chainsync.stream(['blocks']):
    print("{} - {}".format(data['block_num'], data['witness']))
```

### Example - streaming operations

``` python
from chainsync import ChainSync
from chainsync.adapters.steemv2 import SteemV2Adapter

adapter = SteemV2Adapter(endpoints=['https://api.steemit.com'])
chainsync = ChainSync(adapter)

for dataType, data in chainsync.stream(['ops']):
    print("{} - {}".format(data['block_num'], data['operation_type']))
```

### Example - streaming operations with a whitelist

``` python
from chainsync import ChainSync
from chainsync.adapters.steemv2 import SteemV2Adapter

adapter = SteemV2Adapter(endpoints=['https://api.steemit.com'])
chainsync = ChainSync(adapter)

for dataType, op in chainsync.stream(['ops'], whitelist=['vote']):
    print("{} - {} by {}".format(op['block_num'], op['operation_type'], op['voter']))
```

### Example - custom adapters

A custom adapter can be supplied to allow parsing of a specific blockchain

``` python
from chainsync import ChainSync
from chainsync.adapters.decent import DecentAdapter

adapter = DecentAdapter(endpoints=['http://api.decent-db.com:8090'])
chainsync = ChainSync(adapter)

for block in chainsync.stream(['blocks']):
    print("{} - {}".format(block['block_num'], block['witness']))
```

## Adapters

Adapters can be added and configured to allow access to other similar blockchains.

A current list of adapters can be found in the `./chainsync/adapters` folder.

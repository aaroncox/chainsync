### Blocksync

A simple library to stream blocks and operations for digesting into other mediums.

### Example - Streaming Blocks

```
from blocksync import Blocksync

s = Blocksync(endpoints=['https://api.steemitstage.com'])

for block in s.get_block_stream(start_block=20512349, batch_size=100):
    print("{} - {}".format(block['height'], block['witness']))
```
